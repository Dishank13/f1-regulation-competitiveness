"""Trend decomposition — DESCRIPTIVE ONLY. Identifies nothing causally.

Question: of the total decline in M2 across the study window, what share occurs
across season transitions INTO a reset season, versus all other transitions?

If convergence is spread evenly regardless of proximity to a reset, the secular
trend looks exogenous to the resets. If it concentrates at resets, it does not.

This is the closest the design gets to the Decision H question. It is not a test.
There is no null hypothesis, no p-value, and no causal identification: reset
seasons are not randomly assigned, the transitions are not independent, and any
concentration is equally consistent with resets responding to convergence as
with resets causing it.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from src import config

METRIC = "M2_iqr"


def main() -> None:
    s = pd.read_parquet(config.DATA_PROCESSED / "tier_a_season_metrics.parquet")
    s = s.sort_values("season").reset_index(drop=True)

    d = s[["season", METRIC]].copy()
    d["prev"] = d[METRIC].shift(1)
    d["change"] = d[METRIC] - d["prev"]
    d = d.dropna(subset=["change"])
    d["into_reset"] = d.season.isin(config.RESET_SEASONS)

    pd.set_option("display.width", 200)
    print("=== season-to-season change in M2 (Tier A) ===")
    print(d[["season", METRIC, "change", "into_reset"]].round(4).to_string(index=False))

    for label, sub in (("EXCLUDING the partial 2026 season", d[d.season < 2026]),
                       ("INCLUDING 2026 (provisional)", d)):
        print(f"\n--- {label} ---")
        tot = sub.change.sum()
        res = sub[sub.into_reset]
        non = sub[~sub.into_reset]
        print(f"  total net change over the window: {tot:+.4f}")
        print(f"  transitions INTO a reset season   : n={len(res):>2}  "
              f"sum={res.change.sum():+.4f}  mean={res.change.mean():+.4f}")
        print(f"  all other transitions             : n={len(non):>2}  "
              f"sum={non.change.sum():+.4f}  mean={non.change.mean():+.4f}")

        # Share of the DECLINE (negative movements only), which is what the
        # Decision H question is about.
        dec = sub[sub.change < 0]
        dec_r = dec[dec.into_reset].change.sum()
        dec_n = dec[~dec.into_reset].change.sum()
        tot_dec = dec.change.sum()
        print(f"  total DECLINE (negative moves only): {tot_dec:+.4f}")
        if tot_dec != 0:
            print(f"    share occurring into a reset season: "
                  f"{100 * dec_r / tot_dec:.1f}%  (n={int((dec.into_reset).sum())})")
            print(f"    share occurring elsewhere          : "
                  f"{100 * dec_n / tot_dec:.1f}%  (n={int((~dec.into_reset).sum())})")
        # Expected share if declines were spread evenly across transitions.
        share_reset_transitions = 100 * len(res) / len(sub)
        print(f"  reset transitions are {share_reset_transitions:.1f}% of all "
              "transitions (the even-spread benchmark)")

    d.to_parquet(config.DATA_PROCESSED / "trend_decomposition.parquet", index=False)
    print("\nDESCRIPTIVE ONLY. This identifies nothing causally.")


if __name__ == "__main__":
    main()
