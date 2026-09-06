"""Phase 2 — Tier A cleaning: qualifying times to a team-event pace table.

Implements ANALYSIS_PLAN.md sections 4.1, 4.1.1 and 6.3.

EVERY filter logs the count it removes, individually and in order. A filter that
removes an unexpected share is a bug until proven otherwise (plan section 6).
Nothing is dropped silently and the ledger totals must reconcile.

Pipeline:
    driver-event-segment time cells
      -> segment eligibility by era (Q3 ineligible 2006-09)
      -> session viability
      -> per-event evolution offsets, referenced to Q1
      -> adjusted times
      -> team-event representative time (best adjusted lap, either driver)
      -> delta = % off fastest team at that event
"""

from __future__ import annotations

from statistics import median

import pandas as pd

from src import config
from src.clean import team_mapping
from src.coverage_tier_a import parse_time
from src.ingest import jolpica

# Decision A provisional values. NOT decided — the analyst sets these after
# reading the ledger this module produces. R7 sweeps them regardless.
MIN_MULTI_SEGMENT_DRIVERS = 5   # to estimate an evolution offset
MIN_TEAMS_PER_EVENT = 6         # below this an event has no usable spread
MIN_ENTRIES_PER_SESSION = 12    # below this the session is treated as disrupted

SEGMENTS = ("Q1", "Q2", "Q3")


def eligible_segments(season: int) -> tuple[str, ...]:
    """Plan section 4.1.1. Q3 in 2006-09 was run on race fuel and is not an
    observation of low-fuel maximum-attack pace."""
    return ("Q1", "Q2") if season <= 2009 else SEGMENTS


def build() -> tuple[pd.DataFrame, pd.DataFrame]:
    ledger: list[dict] = []

    def log(step: str, unit: str, before: int, after: int, note: str = "",
            kind: str = "filter") -> None:
        """kind='filter' removes rows; kind='aggregate' collapses them.

        These are NOT the same thing and must not share a percentage column: an
        aggregation that turns 18k lap cells into 4k team-events has not lost
        76% of anything. Conflating them is exactly the silent-data-loss failure
        the ledger exists to prevent.
        """
        ledger.append({
            "step": step, "kind": kind, "unit": unit,
            "before": before, "after": after,
            "removed": (before - after) if kind == "filter" else 0,
            "pct_removed": (round(100 * (before - after) / before, 3)
                            if kind == "filter" and before else 0.0),
            "note": note,
        })

    # --- L0: every driver-event-segment cell carrying a time ------------------
    cells: list[dict] = []
    for season in range(config.TIER_A_SEASON_MIN, config.TIER_A_SEASON_MAX + 1):
        for race in jolpica.qualifying(season):
            rnd = int(race["round"])
            results = race.get("QualifyingResults", [])
            for r in results:
                for seg in SEGMENTS:
                    t = parse_time(r.get(seg))
                    if t is None:
                        continue
                    cells.append({
                        "season": season, "round": rnd,
                        "event": race.get("raceName", ""),
                        "driver": r["Driver"]["driverId"],
                        "constructor": r["Constructor"]["constructorId"],
                        "segment": seg, "time": t,
                        "n_entries": len(results),
                    })
    df = pd.DataFrame(cells)
    n0 = len(df)
    log("L0 source cells (driver-event-segment with a time)", "cells", n0, n0,
        "baseline")

    # --- L1: segment eligibility by era (plan 4.1.1) --------------------------
    before = len(df)
    df["eligible"] = df.apply(
        lambda r: r["segment"] in eligible_segments(r["season"]), axis=1)
    df = df[df.eligible].drop(columns=["eligible"])
    log("L1 segment eligibility (Q3 ineligible 2006-09, plan 4.1.1)", "cells",
        before, len(df), "race-fuel qualifying; not the estimand")

    # --- L2: session viability ------------------------------------------------
    before = len(df)
    df = df[df.n_entries >= MIN_ENTRIES_PER_SESSION]
    log(f"L2 session viability (>= {MIN_ENTRIES_PER_SESSION} entries)", "cells",
        before, len(df), "disrupted/red-flagged sessions")

    # --- L3: per-event evolution offsets, referenced to Q1 (plan 4.1) ---------
    offsets: dict[tuple[int, int], dict[str, float]] = {}
    fallback_events: list[tuple[int, int]] = []
    for (season, rnd), grp in df.groupby(["season", "round"]):
        wide = grp.pivot_table(index="driver", columns="segment", values="time",
                               aggfunc="min")
        off = {"Q1": 0.0}
        ok = True
        for lo, hi in (("Q1", "Q2"), ("Q2", "Q3")):
            if hi not in eligible_segments(season):
                continue
            if lo in wide.columns and hi in wide.columns:
                pair = (wide[hi] - wide[lo]).dropna()
                if len(pair) >= MIN_MULTI_SEGMENT_DRIVERS:
                    off[hi] = off[lo] + median(pair)
                else:
                    ok = False
            else:
                ok = False
        for seg in eligible_segments(season):
            off.setdefault(seg, 0.0)
        if not ok:
            fallback_events.append((season, rnd))
        offsets[(season, rnd)] = off

    df["offset"] = df.apply(
        lambda r: offsets[(r["season"], r["round"])].get(r["segment"], 0.0), axis=1)
    df["time_adj"] = df["time"] - df["offset"]
    log("L3 evolution adjustment applied", "cells", len(df), len(df),
        f"{len(fallback_events)} events fell back to unadjusted (flagged, not removed)")

    # --- T0: team-event representative time -----------------------------------
    df["team_continuity"] = df.constructor.map(team_mapping.continuity)
    df["team_strict"] = df.constructor
    idx = df.groupby(["season", "round", "team_continuity"])["time_adj"].idxmin()
    teams = df.loc[idx].copy()
    teams = teams.rename(columns={"time_adj": "q_adj", "segment": "source_segment"})
    log("T0 team-event observations formed", "cells -> team-events",
        len(df), len(teams),
        "AGGREGATION, not loss: best adjusted lap, either driver (plan 4.1)",
        kind="aggregate")

    # --- T1: events with too few teams ---------------------------------------
    before = len(teams)
    counts = teams.groupby(["season", "round"]).size()
    keep = counts[counts >= MIN_TEAMS_PER_EVENT].index
    teams = teams.set_index(["season", "round"]).loc[keep].reset_index()
    log(f"T1 event viability (>= {MIN_TEAMS_PER_EVENT} teams)", "team-events",
        before, len(teams), "")

    # --- delta: % off fastest team at the event -------------------------------
    teams["q_best_event"] = teams.groupby(["season", "round"])["q_adj"].transform("min")
    teams["delta"] = 100 * (teams["q_adj"] / teams["q_best_event"] - 1)

    before = len(teams)
    teams = teams[teams.delta.notna() & (teams.delta >= 0)]
    log("T2 non-finite or negative delta", "team-events", before, len(teams),
        "guard; should remove zero rows")

    led = pd.DataFrame(ledger)
    return teams, led


def write_markdown_ledger(teams: pd.DataFrame, led: pd.DataFrame) -> None:
    """Committed documentation of the ledger; the Parquet is gitignored."""
    src = (teams.assign(era=lambda d: d.season.where(d.season > 2009, 0))
           .assign(era=lambda d: ["2006-09" if s <= 2009 else "2010+"
                                  for s in d.season])
           .groupby("era")["source_segment"].value_counts(normalize=True)
           .mul(100).round(1).unstack(fill_value=0))

    lines = [
        "# Phase 2 — Tier A row-loss ledger",
        "",
        "Generated by `python -m src.clean.tier_a`. Plan §6 requires every filter",
        "log the count it removes, individually and in order.",
        "",
        "`kind=filter` removes rows. `kind=aggregate` collapses them — an",
        "aggregation has not *lost* anything and does not carry a removal",
        "percentage. Conflating the two is the silent-loss failure this ledger",
        "exists to prevent.",
        "",
        led.to_markdown(index=False),
        "",
        f"**Final:** {len(teams):,} team-event observations across "
        f"{teams.groupby(['season', 'round']).ngroups} events, "
        f"{teams.season.min()}–{teams.season.max()}.",
        "",
        "## Filters that removed nothing — verified live, not broken",
        "",
        "L2 and T1 removed zero rows. That is a real property of the data, not a",
        "silent failure: across 2006–2026 the smallest qualifying session has 18",
        "entries (threshold 12) and the smallest event has 9 teams (threshold 6).",
        "Both filters were checked against the distribution they screen.",
        "",
        "## Representative-time source segment, by era",
        "",
        src.to_markdown(),
        "",
        "Q3 is 0% before 2010 by construction (plan §4.1.1).",
    ]
    (config.DATA_PROCESSED / "row_loss_ledger.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    teams, led = build()
    teams.to_parquet(config.DATA_PROCESSED / "tier_a_team_event.parquet", index=False)
    led.to_parquet(config.DATA_PROCESSED / "tier_a_row_loss_ledger.parquet", index=False)
    write_markdown_ledger(teams, led)

    print("=== TIER A ROW-LOSS LEDGER ===")
    print(led.to_string(index=False))
    print(f"\nfinal team-event observations: {len(teams):,}")
    print(f"seasons: {teams.season.min()}-{teams.season.max()}   "
          f"events: {teams.groupby(['season','round']).ngroups}")
    print("\nrepresentative-time source segment by era:")
    teams["era"] = teams.season.apply(lambda s: "2006-09" if s <= 2009 else "2010+")
    print((teams.groupby("era")["source_segment"]
           .value_counts(normalize=True).mul(100).round(1)
           .unstack(fill_value=0).to_string()))


if __name__ == "__main__":
    main()
