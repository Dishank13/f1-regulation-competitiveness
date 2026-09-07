"""Is the fixed traffic gap a TIME-VARYING filter? (analyst-raised risk)

A fixed absolute gap of 5 s is far stricter at short, tight circuits — where
trains form and the whole field can sit inside 5 s of somebody — than at long
ones. Circuit strictness therefore varies, and if the calendar's mix of such
circuits changes across the Tier B window, the filter's strictness changes with
it: a time-varying exclusion rule inside a study built to detect time-varying
changes. Same failure class as Finding B, D1b and the weather flag.

This measures it. It does not fix it. Switching to a lap-time-relative gap
would be a metric change and is not made here.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats

from src import config
from src.clean.tier_b import PCT_OFF_BEST, TRAFFIC_GAP_S
from src.decision_a_evidence import base_laps


def retention() -> pd.DataFrame:
    df = base_laps()
    df = df[df.pct_of_best <= PCT_OFF_BEST]
    df["kept"] = df.gap_ahead_s.isna() | (df.gap_ahead_s >= TRAFFIC_GAP_S)
    return df


def main() -> None:
    df = retention()

    per_race = (df.groupby(["season", "round", "event"])["kept"]
                .agg(laps="size", kept="sum").reset_index())
    per_race["retention_pct"] = 100 * per_race.kept / per_race.laps

    print("=== retention at "
          f"{TRAFFIC_GAP_S} s, by SEASON ===")
    per_season = (per_race.groupby("season")
                  .apply(lambda g: pd.Series({
                      "races": len(g),
                      "retention_pct": 100 * g.kept.sum() / g.laps.sum()}),
                         include_groups=False)
                  .reset_index())
    print(per_season.round(2).to_string(index=False))

    # Trend test: does retention move systematically across seasons?
    x = per_season.season.to_numpy(dtype=float)
    y = per_season.retention_pct.to_numpy(dtype=float)
    lr = stats.linregress(x, y)
    print(f"\nseason trend: {lr.slope:+.3f} pp/season "
          f"(p = {lr.pvalue:.4f}, r = {lr.rvalue:+.3f})")
    verdict = ("TIME-VARYING: retention trends across seasons"
               if lr.pvalue < 0.05 else
               "no significant season trend in retention")
    print(f"  -> {verdict}")

    print("\n=== retention by CIRCUIT (lowest 12 = strictest filtering) ===")
    per_circ = (per_race.groupby("event")
                .apply(lambda g: pd.Series({
                    "races": len(g),
                    "retention_pct": 100 * g.kept.sum() / g.laps.sum()}),
                       include_groups=False)
                .reset_index().sort_values("retention_pct"))
    print(per_circ.head(12).round(2).to_string(index=False))
    print("\n(highest 5)")
    print(per_circ.tail(5).round(2).to_string(index=False))

    spread = per_circ.retention_pct.max() - per_circ.retention_pct.min()
    print(f"\ncircuit spread in retention: {spread:.1f} percentage points")

    per_season.to_parquet(
        config.DATA_PROCESSED / "traffic_retention_by_season.parquet", index=False)
    per_circ.to_parquet(
        config.DATA_PROCESSED / "traffic_retention_by_circuit.parquet", index=False)


if __name__ == "__main__":
    main()
