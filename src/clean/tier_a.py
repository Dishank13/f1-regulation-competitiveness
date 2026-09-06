"""Phase 2 — Tier A cleaning: qualifying times to a team-event pace table.

Implements ANALYSIS_PLAN.md sections 4.1, 4.1.1, 3.2 and 6.3.

EVERY filter logs the count it removes, individually and in order, and the
ledger is tracked on THREE units in parallel — events, driver-event-segment
cells, and team-events. Event-level attrition is invisible in a cell-level
ledger, which is how a lost event escaped the first version of this file.

Step kinds are distinguished because conflating them is the failure the ledger
exists to prevent:
    baseline   establishes a starting count; removes nothing by definition
    filter     removes rows; carries a removal count and percentage
    transform  changes values, not row counts
    aggregate  collapses rows; has not *lost* anything
    guard      a filter that cannot fire given upstream construction

Pipeline:
    events -> drop events with no parseable time
    driver-event-segment cells
      -> segment eligibility by era (Q3 ineligible 2006-09)
      -> session viability
      -> per-event evolution offsets, referenced to Q1  [transform]
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
# reading the Tier B ledger. R7 sweeps them regardless.
MIN_MULTI_SEGMENT_DRIVERS = 5   # to estimate an evolution offset
MIN_TEAMS_PER_EVENT = 6         # below this an event has no usable spread
MIN_ENTRIES_PER_SESSION = 12    # below this the session is treated as disrupted

SEGMENTS = ("Q1", "Q2", "Q3")


def eligible_segments(season: int) -> tuple[str, ...]:
    """Plan section 4.1.1. Q3 in 2006-09 was run on race fuel and is not an
    observation of low-fuel maximum-attack pace."""
    return ("Q1", "Q2") if season <= 2009 else SEGMENTS


def build() -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    ledger: list[dict] = []
    notes: dict = {}

    def log(step: str, unit: str, before: int, after: int, note: str = "",
            kind: str = "filter") -> None:
        removes = kind in ("filter", "guard")
        ledger.append({
            "step": step, "kind": kind, "unit": unit,
            "before": before, "after": after,
            "removed": (before - after) if removes else None,
            "pct_removed": (round(100 * (before - after) / before, 3)
                            if removes and before else None),
            "note": note,
        })

    # ---- EVENT TRACK ---------------------------------------------------------
    raw_events: list[dict] = []
    for season in range(config.TIER_A_SEASON_MIN, config.TIER_A_SEASON_MAX + 1):
        for race in jolpica.qualifying(season):
            results = race.get("QualifyingResults", [])
            n_times = sum(
                1 for r in results for seg in SEGMENTS
                if parse_time(r.get(seg)) is not None
            )
            raw_events.append({
                "season": season, "round": int(race["round"]),
                "event": race.get("raceName", ""),
                "n_entries": len(results), "n_times": n_times,
                "results": results,
            })
    ev = pd.DataFrame(raw_events)
    log("E0 events returned by qualifying endpoint", "events", len(ev), len(ev),
        "baseline; reconciles with coverage report section 1", kind="baseline")

    before = len(ev)
    dropped_no_times = ev[ev.n_times == 0][["season", "round", "event", "n_entries"]]
    ev = ev[ev.n_times > 0]
    notes["events_no_parseable_times"] = dropped_no_times.to_dict("records")
    log("E1 events with no parseable qualifying time", "events", before, len(ev),
        "; ".join(f"{r.season} r{r['round']} {r.event}"
                  for _, r in dropped_no_times.iterrows()) or "none")

    # ---- CELL TRACK ----------------------------------------------------------
    cells: list[dict] = []
    for e in ev.itertuples():
        for r in e.results:
            for seg in SEGMENTS:
                t = parse_time(r.get(seg))
                if t is None:
                    continue
                cells.append({
                    "season": e.season, "round": getattr(e, "round"),
                    "event": e.event,
                    "driver": r["Driver"]["driverId"],
                    "constructor": r["Constructor"]["constructorId"],
                    "segment": seg, "time": t, "n_entries": e.n_entries,
                })
    df = pd.DataFrame(cells)
    log("L0 driver-event-segment cells carrying a time", "cells", len(df), len(df),
        "baseline", kind="baseline")

    before = len(df)
    df = df[[s in eligible_segments(y) for s, y in zip(df.segment, df.season)]]
    log("L1 segment eligibility (Q3 ineligible 2006-09, plan 4.1.1)", "cells",
        before, len(df), "race-fuel qualifying; not the estimand")

    before = len(df)
    df = df[df.n_entries >= MIN_ENTRIES_PER_SESSION]
    log(f"L2 session viability (>= {MIN_ENTRIES_PER_SESSION} entries)", "cells",
        before, len(df), "disrupted/red-flagged sessions")

    # ---- L3 evolution adjustment: TRANSFORM, not a filter ---------------------
    offsets: dict[tuple[int, int], dict[str, float]] = {}
    fallbacks: list[dict] = []
    for (season, rnd), grp in df.groupby(["season", "round"]):
        wide = grp.pivot_table(index="driver", columns="segment", values="time",
                               aggfunc="min")
        off = {"Q1": 0.0}
        failed: list[str] = []
        for lo, hi in (("Q1", "Q2"), ("Q2", "Q3")):
            if hi not in eligible_segments(season):
                continue
            # Only a REAL failure if the segment carries times we must adjust.
            if hi not in wide.columns or wide[hi].notna().sum() == 0:
                continue
            if lo in wide.columns:
                pair = (wide[hi] - wide[lo]).dropna()
                if len(pair) >= MIN_MULTI_SEGMENT_DRIVERS:
                    off[hi] = off.get(lo, 0.0) + median(pair)
                    continue
            failed.append(f"{lo}->{hi}")
        if failed:
            fallbacks.append({"season": season, "round": rnd,
                              "event": grp.event.iloc[0], "failed": ",".join(failed)})
        for seg in eligible_segments(season):
            off.setdefault(seg, 0.0)
        offsets[(season, rnd)] = off

    df = df.assign(
        offset=[offsets[(y, r)].get(s, 0.0)
                for y, r, s in zip(df.season, df["round"], df.segment)])
    df["time_adj"] = df["time"] - df["offset"]
    notes["adjustment_fallbacks"] = fallbacks
    log("L3 evolution adjustment applied (plan 4.1)", "cells", len(df), len(df),
        f"{len(fallbacks)} events could not estimate a needed offset"
        if fallbacks else "all needed offsets estimated", kind="transform")

    # ---- TEAM-EVENT TRACK ----------------------------------------------------
    df["team_continuity"] = df.constructor.map(team_mapping.continuity)
    df["team_strict"] = df.constructor
    idx = df.groupby(["season", "round", "team_continuity"])["time_adj"].idxmin()
    teams = df.loc[idx].copy().rename(
        columns={"time_adj": "q_adj", "segment": "source_segment"})
    log("T0 team-event observations formed", "cells -> team-events",
        len(df), len(teams),
        "AGGREGATION, not loss: best adjusted lap, either driver (plan 4.1)",
        kind="aggregate")

    before = len(teams)
    counts = teams.groupby(["season", "round"]).size()
    keep = counts[counts >= MIN_TEAMS_PER_EVENT].index
    teams = teams.set_index(["season", "round"]).loc[keep].reset_index()
    log(f"T1 event viability (>= {MIN_TEAMS_PER_EVENT} teams)", "team-events",
        before, len(teams), "")

    teams["q_best_event"] = teams.groupby(["season", "round"])["q_adj"].transform("min")
    teams["delta"] = 100 * (teams["q_adj"] / teams["q_best_event"] - 1)

    before = len(teams)
    teams = teams[teams.delta.notna() & (teams.delta >= 0)]
    log("T2 non-finite or negative delta", "team-events", before, len(teams),
        "TAUTOLOGICAL GUARD: delta is built from a per-event min, so it is "
        "non-negative and finite by construction. Cannot fire; retained as an "
        "assertion. NOT validated against a screened distribution, unlike "
        "L2/T1 — it has no distribution to screen.", kind="guard")

    # ---- attach the Decision D format-version indicator (changes no counts) ---
    fmt_path = config.DATA_PROCESSED / "session_formats.parquet"
    if fmt_path.exists():
        fmt = pd.read_parquet(fmt_path)[["season", "round", "format_version",
                                         "has_sprint_race"]]
        n_before = len(teams)
        teams = teams.merge(fmt, on=["season", "round"], how="left")
        assert len(teams) == n_before, "format merge changed row count"
        log("F0 format-version indicator attached (Decision D)", "team-events",
            n_before, len(teams),
            "one qualifying session per round in every season; sprint weekends "
            "do not duplicate rows", kind="transform")

    # ---- event-track close-out ----------------------------------------------
    final_events = teams.groupby(["season", "round"]).ngroups
    log("E2 events surviving to the final table", "events",
        len(ev), final_events, "reconciliation check", kind="baseline")

    return teams, pd.DataFrame(ledger), notes


def write_markdown_ledger(teams: pd.DataFrame, led: pd.DataFrame, notes: dict) -> None:
    """Committed documentation of the ledger; the Parquet is gitignored."""
    teams = teams.assign(
        era=["2006-09" if s <= 2009 else "2010+" for s in teams.season])
    src = (teams.groupby("era")["source_segment"].value_counts(normalize=True)
           .mul(100).round(1).unstack(fill_value=0))
    # NB: events must be counted as distinct (season, round) PAIRS. Counting
    # distinct round numbers undercounts badly — round 1 recurs in all 21
    # seasons — and made the events column sum to 46 against 411.
    fmt = None
    if "format_version" in teams.columns:
        fmt = (teams.assign(_ev=list(zip(teams.season, teams["round"])))
               .groupby("format_version")
               .agg(team_events=("delta", "size"), events=("_ev", "nunique")))
        assert fmt.events.sum() == teams.groupby(["season", "round"]).ngroups, (
            "format-version event counts do not reconcile with the final table")
        assert fmt.team_events.sum() == len(teams), (
            "format-version team-event counts do not reconcile")

    drop = notes.get("events_no_parseable_times", [])
    fb = notes.get("adjustment_fallbacks", [])

    lines = [
        "# Phase 2 — Tier A row-loss ledger",
        "",
        "Generated by `python -m src.clean.tier_a`. Plan §6 requires every filter",
        "log the count it removes, individually and in order.",
        "",
        "## Step kinds",
        "",
        "| kind | meaning |",
        "|---|---|",
        "| `baseline` | establishes a starting count; removes nothing by definition |",
        "| `filter` | removes rows; carries a removal count and percentage |",
        "| `transform` | changes values, not row counts |",
        "| `aggregate` | collapses rows; has not *lost* anything |",
        "| `guard` | a filter that cannot fire given upstream construction |",
        "",
        "Only `filter` and `guard` carry a removal percentage. An aggregation",
        "that turns 18k lap cells into 4k team-events has not lost 76% of",
        "anything, and a baseline has removed nothing at all.",
        "",
        "## Three parallel unit tracks",
        "",
        "Events, cells, and team-events are tracked separately. **Event-level",
        "attrition is invisible in a cell-level ledger** — that is precisely how",
        "a lost event escaped the first version of this file.",
        "",
        led.to_markdown(index=False),
        "",
        f"**Final:** {len(teams):,} team-event observations across "
        f"{teams.groupby(['season', 'round']).ngroups} events, "
        f"{teams.season.min()}–{teams.season.max()}.",
        "",
        "## Event reconciliation",
        "",
        "The qualifying endpoint returns **412** events for 2006–2026, matching",
        "the sum of the Rounds column in coverage report §1. Of those:",
        "",
    ]
    for d in drop:
        lines.append(
            f"- **{d['season']} r{d['round']} {d['event']}** removed at E1: the "
            f"source returns {d['n_entries']} classified entries but **every** "
            "`Q1`/`Q2`/`Q3` field is an empty string. This is an upstream data "
            "gap, not a format or parsing issue — other sprint-weekend rounds in "
            "the same season carry full times.")
    lines += [
        "",
        f"That leaves **{len(teams.groupby(['season', 'round']))}** events in the "
        "final table. The count now reconciles, and the E-track rows make any "
        "future event-level attrition visible instead of silent.",
        "",
        "## L3 adjustment fallbacks",
        "",
    ]
    if fb:
        for f in fb:
            lines.append(f"- {f['season']} r{f['round']} {f['event']}: "
                         f"could not estimate {f['failed']}")
    else:
        lines.append(
            "**None.** Every offset the adjustment actually needs was estimated.")
        lines.append("")
        lines.append(
            "The previous version reported one fallback, at **2015 r16 United "
            "States Grand Prix**. That was a bug in the flag, not a failure of "
            "the adjustment: Austin 2015 was rain-disrupted and produced Q1 (20 "
            "times) and Q2 (15 times) but **no Q3 times at all**, so the Q2→Q3 "
            "offset was unestimable — and also unnecessary, because there were "
            "no Q3 times to adjust. The flag now fires only when an offset is "
            "needed for a segment that actually carries times. The event's Q1 "
            "and Q2 observations are adjusted on the same basis as every other "
            "event and carry no special measurement status.")
        lines.append("")
        lines.append(
            "**Related gap, surfaced not papered over.** Austin 2015 should have "
            "been caught by the plan §6.1 wet-session flag. It was not, because "
            "**Tier A has no weather source**: Jolpica exposes no weather field, "
            "and FastF1 weather begins in 2018. Systematic wet-session detection "
            "is therefore unavailable for Tier A before 2018. A spread-based "
            "proxy is explicitly rejected as circular — spread is the metric. "
            "This needs an analyst decision and is raised with the Tier B ledger.")
    lines += [
        "",
        "## Filters that removed nothing — which were validated, and how",
        "",
        "| step | treatment |",
        "|---|---|",
        "| L2 (≥12 entries) | **Validated** against the screened distribution: "
        "smallest session in 2006–2026 has 18 entries. Live, correctly idle. |",
        "| T1 (≥6 teams) | **Validated** against the screened distribution: "
        "smallest event has 9 teams. Live, correctly idle. |",
        "| T2 (delta guard) | **Not validated — tautological.** `delta` is built "
        "from a per-event minimum, so it is non-negative and finite by "
        "construction. It has no distribution to screen. Retained as a runtime "
        "assertion, not evidence of anything. |",
        "",
        "## Session format versions (Decision D)",
        "",
        "Jolpica's qualifying endpoint returns **exactly one session per round in "
        "every season 2006–2026**; no round yields two qualifying sessions. It "
        "returns the Grand Prix qualifying that sets the race grid — sprint "
        "shootouts are not in this endpoint, and sprint races live on a separate "
        "`/sprint` endpoint. **Sprint weekends therefore add, duplicate, and "
        "remove no rows, and do not interact with the event-reconciliation fix "
        "above.** Miami 2025 was a sprint weekend, but so were five other 2025 "
        "rounds that carry full times; the gap is unrelated to format.",
        "",
        "Format version is derived empirically from two cross-checked sources — "
        "the Jolpica `/sprint` endpoint (all seasons) and FastF1 `EventFormat` "
        "(2018+) — with **zero disagreements**. It is attached as an event-level "
        "column on the team-event table.",
        "",
    ]
    if fmt is not None:
        lines += [fmt.to_markdown(), ""]
    lines += [
        "## Representative-time source segment, by era",
        "",
        src.to_markdown(),
        "",
        "Q3 is 0% before 2010 by construction (plan §4.1.1).",
    ]
    (config.DATA_PROCESSED / "row_loss_ledger.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    teams, led, notes = build()
    teams.to_parquet(config.DATA_PROCESSED / "tier_a_team_event.parquet", index=False)
    led.to_parquet(config.DATA_PROCESSED / "tier_a_row_loss_ledger.parquet", index=False)
    write_markdown_ledger(teams, led, notes)
    print(led.to_string(index=False))
    print(f"\nfinal: {len(teams):,} team-events, "
          f"{teams.groupby(['season','round']).ngroups} events")


if __name__ == "__main__":
    main()
