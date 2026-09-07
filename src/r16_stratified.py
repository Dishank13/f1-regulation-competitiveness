"""R16 — stratified evolution offset (confound 16, plan §4.1.4).

The §4.1 primary estimates ONE field-wide `E(Q1->Q2)` offset per event. D1a
established that this is misspecified by stratum: front-runners gain ~0.3 s more
between Q1 and Q2 than backmarkers, so the field-wide median is a weighted
average of track evolution and a position-dependent sandbagging differential.

R16 re-estimates the offset SEPARATELY by competitive stratum — drivers who set
a Q3 time versus those who did not — and re-runs everything. The stratum is
defined from the SOURCE data (did this driver set any Q3 time at this event),
so it is available in 2006-09 where Q3 is excluded from the metric, and it does
not depend on the metric being tested.

The red team named a sign flip here as the first thing that would change its
mind. If any per-boundary estimate flips sign, that supersedes the Phase 5
result.
"""

from __future__ import annotations

from statistics import median

import numpy as np
import pandas as pd

from src import config
from src.clean import team_mapping
from src.clean.tier_a import (MIN_ENTRIES_PER_SESSION, MIN_MULTI_SEGMENT_DRIVERS,
                              MIN_TEAMS_PER_EVENT, SEGMENTS, eligible_segments)
from src.coverage_tier_a import parse_time
from src.ingest import jolpica
from src.metrics import event_metrics
from src.phase5 import PRIMARY, its_fit

MIN_PER_STRATUM = 3


def build(stratified: bool) -> pd.DataFrame:
    """Rebuild the Tier A team-event table. `stratified` toggles R16."""
    cells = []
    for season in range(config.TIER_A_SEASON_MIN, config.TIER_A_SEASON_MAX + 1):
        for race in jolpica.qualifying(season):
            res = race.get("QualifyingResults", [])
            if len(res) < MIN_ENTRIES_PER_SESSION:
                continue
            for r in res:
                t = {s: parse_time(r.get(s)) for s in SEGMENTS}
                if all(v is None for v in t.values()):
                    continue
                # Stratum from SOURCE data, before segment exclusion.
                front = t["Q3"] is not None
                for s in SEGMENTS:
                    if t[s] is None or s not in eligible_segments(season):
                        continue
                    cells.append({
                        "season": season, "round": int(race["round"]),
                        "driver": r["Driver"]["driverId"],
                        "constructor": r["Constructor"]["constructorId"],
                        "segment": s, "time": t[s], "front": front,
                    })
    df = pd.DataFrame(cells)

    offsets: dict[tuple, dict] = {}
    for (season, rnd), g in df.groupby(["season", "round"]):
        wide = g.pivot_table(index=["driver", "front"], columns="segment",
                             values="time", aggfunc="min").reset_index()
        off = {}
        for lo, hi in (("Q1", "Q2"), ("Q2", "Q3")):
            if hi not in eligible_segments(season):
                continue
            if lo not in wide.columns or hi not in wide.columns:
                continue
            base = off.get(lo, {True: 0.0, False: 0.0}) if lo != "Q1" else {
                True: 0.0, False: 0.0}
            if not stratified:
                pair = (wide[hi] - wide[lo]).dropna()
                if len(pair) >= MIN_MULTI_SEGMENT_DRIVERS:
                    m = median(pair)
                    off[hi] = {k: base[k] + m for k in (True, False)}
            else:
                res = {}
                for strat in (True, False):
                    w = wide[wide["front"] == strat]
                    pair = (w[hi] - w[lo]).dropna()
                    res[strat] = (base[strat] + median(pair)
                                  if len(pair) >= MIN_PER_STRATUM else None)
                # Backmarkers never set Q3, so the Q2->Q3 offset has only the
                # front stratum; reuse it for both rather than dropping the term.
                if res[True] is None and res[False] is None:
                    continue
                if res[True] is None:
                    res[True] = res[False]
                if res[False] is None:
                    res[False] = res[True]
                off[hi] = res
        offsets[(season, rnd)] = off

    def get_off(row):
        o = offsets.get((row.season, row["round"]), {})
        if row.segment == "Q1":
            return 0.0
        d = o.get(row.segment)
        return 0.0 if d is None else d[row.front]

    df["offset"] = df.apply(get_off, axis=1)
    df["time_adj"] = df["time"] - df["offset"]
    df["team_continuity"] = df.constructor.map(team_mapping.continuity)

    idx = df.groupby(["season", "round", "team_continuity"])["time_adj"].idxmin()
    teams = df.loc[idx].copy()
    counts = teams.groupby(["season", "round"]).size()
    keep = counts[counts >= MIN_TEAMS_PER_EVENT].index
    teams = teams.set_index(["season", "round"]).loc[keep].reset_index()
    teams["best"] = teams.groupby(["season", "round"])["time_adj"].transform("min")
    teams["delta"] = 100 * (teams.time_adj / teams.best - 1)
    return teams


def per_boundary(teams: pd.DataFrame) -> pd.DataFrame:
    ev = (teams.groupby(["season", "round"])
          .apply(event_metrics, include_groups=False).reset_index())
    rows = [its_fit(ev, PRIMARY, b) for b in config.RESET_BOUNDARIES]
    f = pd.DataFrame(rows)
    f["label"] = [config.RESET_BOUNDARIES[b]["label"] for b in f.boundary]
    return f


def main() -> None:
    pd.set_option("display.width", 220)
    base = per_boundary(build(stratified=False))
    strat = per_boundary(build(stratified=True))

    m = base[["label", "b2", "b2_lo", "b2_hi"]].merge(
        strat[["label", "b2", "b2_lo", "b2_hi"]], on="label",
        suffixes=("_fieldwide", "_stratified"))
    m["sign_flip"] = np.sign(m.b2_fieldwide) != np.sign(m.b2_stratified)
    m["delta"] = m.b2_stratified - m.b2_fieldwide

    print("=== R16 — per-boundary b2 under field-wide vs stratified offset ===")
    print(m.round(4).to_string(index=False))

    flips = m[m.sign_flip]
    print(f"\nSIGN FLIPS: {len(flips)}")
    if len(flips):
        print(flips[["label", "b2_fieldwide", "b2_stratified"]].round(4)
              .to_string(index=False))
        print("\n*** A SIGN FLIP SUPERSEDES THE PHASE 5 RESULT — STOP AND REPORT ***")
    else:
        print("No per-boundary estimate changes sign under the stratified offset.")
    m.to_parquet(config.DATA_PROCESSED / "r16_stratified.parquet", index=False)


if __name__ == "__main__":
    main()
