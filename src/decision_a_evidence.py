"""Decision A evidence: derive the thresholds from data, not from round numbers.

Three knobs, three diagnostics:

1. TRAFFIC GAP. Rather than assert a value, measure the lap-time penalty as a
   function of the gap to the car ahead. Where the penalty curve flattens is
   where dirty air stops mattering, and that is the defensible cutoff. The
   penalty is measured WITHIN driver-stint cells, so car pace, tyre age and fuel
   are held approximately fixed and the residual variation is attributable to
   traffic.

2. PCT-OFF-BEST. Show where the excluded laps sit relative to the normal
   race-pace distribution. A cutoff that starts biting into the bulk of the
   distribution is too tight.

3. MIN LAPS PER TEAM. The lap-level sweep showed this knob is nearly inert, but
   the relevant unit is the TEAM-RACE, not the lap: a team-race resting on three
   laps gives a noisy pace estimate even though it costs few rows.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from src import config
from src.clean.tier_b import gap_to_car_ahead, load_raw


def base_laps() -> pd.DataFrame:
    """Structural filters only — no Decision A knobs applied."""
    df = load_raw()
    df = df[df.lap_s.notna() & ~(df.pit_in | df.pit_out) & (df.LapNumber > 1)]
    df = df[df["TrackStatus"].astype(str).str.fullmatch(r"1+")]
    df = df[df.Compound.notna() & df.Stint.notna() & df.TyreLife.notna()]
    df = df[df.TyreLife > 1]
    df = df.copy()
    df["driver_best"] = df.groupby(
        ["season", "round", "Driver"])["lap_s"].transform("min")
    df["pct_of_best"] = 100 * df.lap_s / df.driver_best
    df["gap_ahead_s"] = gap_to_car_ahead(df)
    return df


def traffic_curve(df: pd.DataFrame) -> pd.DataFrame:
    """Lap-time penalty vs gap to car ahead, within driver-stint cells.

    Within one driver's stint the car, tyre compound and fuel trend are fixed,
    so deviation from that stint's own clean-air baseline isolates traffic.
    Baseline = the driver-stint's median lap time among laps with gap >= 3 s.
    """
    d = df[df.gap_ahead_s.notna() & (df.gap_ahead_s >= 0)].copy()
    d["cell"] = (d.season.astype(str) + "_" + d["round"].astype(str) + "_"
                 + d.Driver.astype(str) + "_" + d.Stint.astype(str))
    clean = d[d.gap_ahead_s >= 3.0].groupby("cell")["lap_s"].median()
    d["baseline"] = d["cell"].map(clean)
    d = d[d.baseline.notna()]
    d["penalty_s"] = d.lap_s - d.baseline

    edges = np.array([0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 2.5,
                      3.0, 4.0, 6.0, 10.0, 1e9])
    d["bin"] = pd.cut(d.gap_ahead_s, edges, right=False)
    out = (d.groupby("bin", observed=True)["penalty_s"]
           .agg(n="size", median="median", q25=lambda s: s.quantile(.25),
                q75=lambda s: s.quantile(.75)).reset_index())
    out["gap_lo"] = [iv.left for iv in out["bin"]]
    out["gap_hi"] = [min(iv.right, 999) for iv in out["bin"]]
    return out[["gap_lo", "gap_hi", "n", "median", "q25", "q75"]].round(4)


def pct_curve(df: pd.DataFrame) -> pd.DataFrame:
    q = [50, 75, 90, 95, 97, 98, 99, 99.5]
    vals = np.percentile(df.pct_of_best.dropna(), q)
    return pd.DataFrame({"percentile": q, "pct_of_own_best": np.round(vals, 2)})


def minlaps_curve(df: pd.DataFrame, gap: float) -> pd.DataFrame:
    d = df[(df.pct_of_best <= 107.0)
           & ((df.gap_ahead_s.isna()) | (df.gap_ahead_s >= gap))]
    counts = d.groupby(["season", "round", "team_continuity"]).size()
    total = len(counts)
    rows = []
    for k in (1, 3, 5, 8, 12, 20):
        kept = int((counts >= k).sum())
        rows.append({"min_laps": k, "team_races_kept": kept,
                     "team_races_dropped": total - kept,
                     "pct_dropped": round(100 * (total - kept) / total, 2)})
    return pd.DataFrame(rows)


def marginal_noise(df: pd.DataFrame, gap: float) -> pd.DataFrame:
    """How noisy is a team-race pace estimate as a function of its lap count?"""
    d = df[(df.pct_of_best <= 107.0)
           & ((df.gap_ahead_s.isna()) | (df.gap_ahead_s >= gap))]
    g = d.groupby(["season", "round", "team_continuity"])["lap_s"]
    stat = pd.DataFrame({"n": g.size(), "sd": g.std()}).dropna()
    stat["sem"] = stat["sd"] / np.sqrt(stat["n"])
    bins = [0, 3, 5, 8, 12, 20, 10000]
    stat["band"] = pd.cut(stat.n, bins, right=False)
    return (stat.groupby("band", observed=True)
            .agg(team_races=("n", "size"), median_sem=("sem", "median"))
            .round(4).reset_index())


def main() -> None:
    df = base_laps()
    print(f"base laps after structural filters only: {len(df):,}\n")

    tc = traffic_curve(df)
    print("=== 1. TRAFFIC: lap-time penalty vs gap to car ahead ===")
    print("(within driver-stint; baseline = that stint's median lap at gap >= 3s)")
    print(tc.to_string(index=False))

    print("\n=== 2. PCT-OFF-BEST distribution ===")
    print(pct_curve(df).to_string(index=False))

    print("\n=== 3a. MIN LAPS: team-races dropped (at traffic gap 1.5s) ===")
    print(minlaps_curve(df, 1.5).to_string(index=False))

    print("\n=== 3b. Noise in a team-race pace estimate by lap count ===")
    print(marginal_noise(df, 1.5).to_string(index=False))

    tc.to_parquet(config.DATA_PROCESSED / "decision_a_traffic_curve.parquet",
                  index=False)


if __name__ == "__main__":
    main()
