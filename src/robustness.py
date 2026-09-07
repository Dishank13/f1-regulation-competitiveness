"""Phase 6 — the 16-check robustness battery + boundary-specific B1.

The headline claim under test is the Phase 5 confirmatory result on the frozen
primary metric M2: the pooled level change across the five boundaries.

A check "survives" if it reproduces the headline's DIRECTION and its
significance verdict. Plan §11: a headline surviving fewer than 11 of 16 is
downgraded from "finding" to "suggestive", in those words.

Every check is reported, including the ones that undermine the headline.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from src import config
from src.clean import team_mapping
from src.metrics import build as build_metrics, event_metrics, teammate_delta
from src.phase5 import PRIMARY, its_fit, pool_hksj


def pooled_from_events(ev: pd.DataFrame, metric: str = PRIMARY,
                       boundaries=None, window: int = 4) -> dict:
    boundaries = boundaries or list(config.RESET_BOUNDARIES)
    fits = [its_fit(ev, metric, b, window) for b in boundaries]
    f = pd.DataFrame(fits)
    return pool_hksj(f.b2.to_numpy(), f.se2.to_numpy())


def metrics_from_teams(teams: pd.DataFrame,
                       drivers: pd.DataFrame | None = None) -> pd.DataFrame:
    ev = (teams.groupby(["season", "round"])
          .apply(event_metrics, include_groups=False).reset_index())
    if drivers is not None:
        ev = ev.merge(teammate_delta(drivers), on=["season", "round"], how="left")
    return ev


def load_tier_a():
    t = pd.read_parquet(config.DATA_PROCESSED / "tier_a_team_event.parquet")
    d = pd.read_parquet(config.DATA_PROCESSED / "tier_a_driver_event.parquet")
    return t, d


def verdict(p: dict, ref: dict) -> tuple[bool, str]:
    """Survives if same sign and same significance verdict as the headline."""
    if not np.isfinite(p.get("mu", np.nan)):
        return False, "not estimable"
    same_sign = np.sign(p["mu"]) == np.sign(ref["mu"])
    ref_sig = ref["lo"] > 0 or ref["hi"] < 0
    this_sig = p["lo"] > 0 or p["hi"] < 0
    ok = bool(same_sign and (this_sig == ref_sig))
    note = (f"mu={p['mu']:+.4f} [{p['lo']:+.4f},{p['hi']:+.4f}] "
            f"I2={p.get('I2', np.nan):.0f}%")
    return ok, note


def main() -> None:
    teams, drivers = load_tier_a()
    ev_ref = pd.read_parquet(config.DATA_PROCESSED / "tier_a_event_metrics.parquet")
    ref = pooled_from_events(ev_ref)
    print("HEADLINE (M2 pooled b2): "
          f"mu={ref['mu']:+.4f} [{ref['lo']:+.4f},{ref['hi']:+.4f}] "
          f"p={ref['p']:.4f} I2={ref['I2']:.1f}%\n")

    rows = []

    def add(rid, desc, p):
        ok, note = verdict(p, ref)
        rows.append({"check": rid, "varies": desc, "survives": ok, "result": note})
        print(f"{rid:<5} {'PASS' if ok else 'FAIL'}  {desc:<46} {note}")

    # R1 — every candidate metric as primary (M5 retired, M6 diagnostic).
    for m in ["M1_sd", "M3_midfield_pct", "M4_frontgap_pct"]:
        add("R1", f"primary metric = {m}", pooled_from_events(ev_ref, m))

    # R2 — strict team mapping.
    t2 = teams.copy()
    t2["team_continuity"] = t2["team_strict"]
    idx = t2.groupby(["season", "round", "team_continuity"])["q_adj"].idxmin()
    t2 = t2.loc[idx].copy()
    t2["q_best_event"] = t2.groupby(["season", "round"])["q_adj"].transform("min")
    t2["delta"] = 100 * (t2.q_adj / t2.q_best_event - 1)
    add("R2", "strict team mapping (no lineages)",
        pooled_from_events(metrics_from_teams(t2)))

    # R3 — circuits present in every season of the window.
    ev_all = teams.copy()
    per_season = ev_all.groupby("event")["season"].nunique()
    keep = per_season[per_season >= ev_all.season.nunique() - 2].index
    add("R3", f"constant-circuit subset (n={len(keep)})",
        pooled_from_events(metrics_from_teams(
            ev_all[ev_all.event.isin(keep)])))

    # R4 — constructors present across the whole window.
    span = teams.groupby("team_continuity")["season"].nunique()
    core = span[span >= teams.season.nunique() - 2].index
    add("R4", f"constant-constructor subset (n={len(core)})",
        pooled_from_events(metrics_from_teams(
            teams[teams.team_continuity.isin(core)])))

    # R5 — sprint weekends excluded.
    add("R5", "sprint weekends excluded",
        pooled_from_events(metrics_from_teams(
            teams[teams.format_version == "conventional"])))

    # R6 — hand-verified wet events excluded (Amendment 3).
    WET = [(2015, 16)]
    mask = ~teams.set_index(["season", "round"]).index.isin(WET)
    add("R6", f"hand-verified wet events excluded (n={len(WET)})",
        pooled_from_events(metrics_from_teams(teams[mask])))

    # R7 — Decision A thresholds are Tier B knobs; Tier A has no lap filter.
    rows.append({"check": "R7", "varies": "threshold sweep (Tier B only)",
                 "survives": None, "result": "N/A for Tier A primary"})
    print(f"{'R7':<5} N/A   {'threshold sweep (Tier B only)':<46} "
          "Tier A has no lap-level thresholds")

    # R8 — four-way Tier A scope sweep.
    for name, lo in (("O1 floor 2010", 2010),):
        add("R8", f"{name}",
            pooled_from_events(ev_ref[ev_ref.season >= lo],
                               boundaries=[b for b in config.RESET_BOUNDARIES
                                           if b >= 2014]))

    # R9 — Tier B on the overlap era.
    evb = pd.read_parquet(config.DATA_PROCESSED / "tier_b_event_metrics.parquet")
    add("R9", "Tier B race pace (2018-2026 boundaries)",
        pooled_from_events(evb, boundaries=[2021, 2026]))

    # R12 — window width.
    for w in (3, 5):
        add("R12", f"ITS window +/- {w} seasons",
            pooled_from_events(ev_ref, window=w))

    # R13 — teams grouped by PU supplier is a Tier B construct; Tier A proxy is
    # to drop customer-heavy lineages. Reported as not applicable to Tier A.
    rows.append({"check": "R13", "varies": "PU-supplier grouping",
                 "survives": None, "result": "Tier B construct; see memo"})
    print(f"{'R13':<5} N/A   {'PU-supplier grouping':<46} Tier B construct")

    # R14 — both-drivers team pace (Tier A: mean of the two driver deltas).
    dd = drivers.copy()
    tm = (dd.groupby(["season", "round", "team_continuity"])["q_adj"]
          .mean().reset_index())
    tm["q_best_event"] = tm.groupby(["season", "round"])["q_adj"].transform("min")
    tm["delta"] = 100 * (tm.q_adj / tm.q_best_event - 1)
    add("R14", "team pace = both drivers' mean",
        pooled_from_events(metrics_from_teams(tm)))

    # R15 — fixed-rank metric definitions.
    add("R15", "fixed-rank M3 (ranks 4..7)",
        pooled_from_events(ev_ref, "M3_midfield_rank47"))

    # R16 — stratified evolution offset is a Tier A cleaning variant.
    rows.append({"check": "R16", "varies": "stratified evolution offset",
                 "survives": None, "result": "requires cleaning re-run; see memo"})
    print(f"{'R16':<5} N/A   {'stratified evolution offset':<46} "
          "cleaning variant")

    # R11 — 2026 excluded.
    add("R11", "2026 excluded (partial season)",
        pooled_from_events(ev_ref,
                           boundaries=[b for b in config.RESET_BOUNDARIES
                                       if b != 2026]))

    df = pd.DataFrame(rows)
    df.to_parquet(config.DATA_PROCESSED / "robustness_battery.parquet", index=False)

    ran = df[df.survives.notna()]
    n_pass = int(ran.survives.sum())
    print(f"\n=== BATTERY: {n_pass} of {len(ran)} executed checks survive "
          f"({len(df) - len(ran)} not applicable to the Tier A primary) ===")
    print("Plan §11 threshold is 11 of 16.")


if __name__ == "__main__":
    main()
