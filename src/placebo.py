"""Phase 5 (partial) — placebo battery (ANALYSIS_PLAN.md section 8.6).

Runs the segmented level-shift estimate at EVERY eligible non-reset season
boundary, then reports each reset boundary's shift as a PERCENTILE within that
placebo distribution. The point is that a reset shift means nothing until you
know how large ordinary season-to-season shifts are.

This is not the confirmatory test. No primary metric is frozen yet, so every
metric is reported and none is privileged. The confirmatory pooled estimates in
plan 8.3-8.4 run only after Decision B.

2010 is reported SEPARATELY as a measurement-artifact boundary, not as an
ordinary placebo: it carries a grid expansion from 10 to 12 constructors with
three new backmarkers, the refuelling ban, and the segment-eligibility change,
all at once. Including it silently in the clean pool would let a boundary we
know to be contaminated set the scale everything else is judged against.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from src import config
from src.metrics import level_shift

# Plan 8.6: Tier A eligible control boundaries. 2016 excluded (elimination
# qualifying), 2010/2019/2020/2023 excluded as flagged discontinuities,
# reset seasons excluded.
TIER_A_PLACEBO = [2007, 2008, 2011, 2012, 2013, 2015, 2018, 2024, 2025]
ARTIFACT_BOUNDARIES = [2010]

METRICS = ["M1_sd", "M2_iqr", "M3_midfield_pct", "M4_frontgap_pct",
           "M5_front_pair", "M6_backmarker"]


def run(tier: str = "a") -> pd.DataFrame:
    ev = pd.read_parquet(
        config.DATA_PROCESSED / f"tier_{tier}_event_metrics.parquet")
    rows = []
    for m in METRICS:
        for b in TIER_A_PLACEBO:
            r = level_shift(ev, m, b)
            r["kind"] = "placebo"
            rows.append(r)
        for b in ARTIFACT_BOUNDARIES:
            r = level_shift(ev, m, b)
            r["kind"] = "artifact"
            rows.append(r)
        for b in config.RESET_BOUNDARIES:
            r = level_shift(ev, m, b)
            r["kind"] = "reset"
            r["label"] = config.RESET_BOUNDARIES[b]["label"]
            rows.append(r)
    return pd.DataFrame(rows)


def percentiles(df: pd.DataFrame) -> pd.DataFrame:
    """Each reset's |shift| as a percentile of the placebo |shift| distribution."""
    out = []
    for m, g in df.groupby("metric"):
        pl = g[g.kind == "placebo"]["shift"].dropna().abs().to_numpy()
        if len(pl) < 3:
            continue
        for _, r in g[g.kind.isin(["reset", "artifact"])].iterrows():
            if not np.isfinite(r["shift"]):
                continue
            pct = 100 * (pl < abs(r["shift"])).mean()
            out.append({
                "metric": m,
                "boundary": r.get("label", str(int(r["boundary"]))),
                "kind": r["kind"],
                "shift": round(r["shift"], 4),
                "ci_lo": round(r["lo"], 4), "ci_hi": round(r["hi"], 4),
                "abs_shift": round(abs(r["shift"]), 4),
                "placebo_median_abs": round(float(np.median(pl)), 4),
                "placebo_max_abs": round(float(pl.max()), 4),
                "pctile_in_placebo": round(pct, 1),
                "exceeds_all_placebos": bool(abs(r["shift"]) > pl.max()),
            })
    return pd.DataFrame(out)


def main() -> None:
    import sys
    tier = sys.argv[1].lower() if len(sys.argv) > 1 else "a"
    df = run(tier)
    df.to_parquet(config.DATA_PROCESSED / f"placebo_tier_{tier}.parquet",
                  index=False)
    pc = percentiles(df)
    pc.to_parquet(config.DATA_PROCESSED / f"placebo_percentiles_tier_{tier}.parquet",
                  index=False)

    pd.set_option("display.width", 230)
    print(f"### TIER {tier.upper()} PLACEBO BATTERY ###")
    print(f"eligible control boundaries: {TIER_A_PLACEBO} (n={len(TIER_A_PLACEBO)})")
    print(f"artifact boundary reported separately: {ARTIFACT_BOUNDARIES}\n")

    for m in METRICS:
        g = df[(df.metric == m)]
        pl = g[g.kind == "placebo"]["shift"].dropna()
        if pl.empty:
            continue
        print(f"--- {m} ---")
        print(f"  placebo |shift|: median={pl.abs().median():.4f} "
              f"max={pl.abs().max():.4f} (n={len(pl)})")
        sub = pc[(pc.metric == m)]
        if len(sub):
            print(sub[["boundary", "kind", "shift", "ci_lo", "ci_hi",
                       "pctile_in_placebo", "exceeds_all_placebos"]]
                  .to_string(index=False))
        print()


if __name__ == "__main__":
    main()
