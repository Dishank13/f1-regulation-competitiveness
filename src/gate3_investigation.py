"""Plan §4.4 gate 3 requires races failing BOTH comparators to be manually
investigated before inclusion — not auto-excluded.

For each failing race this assembles the evidence needed to tell a genuine model
failure from a race where the comparators are structurally uninformative:

  * laps retained and laps per driver (is the fit thin?)
  * teams surviving (did the field shrink?)
  * traffic retention at that event (is clean air scarce here?)
  * session rainfall (are the laps mixed-condition?)
  * spread of recovered pace (if every team is within noise of every other,
    a rank correlation against ANY comparator is meaningless)
  * finishing-order churn vs qualifying (did the race scramble?)
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from src import config


def main() -> None:
    g = pd.read_parquet(config.DATA_PROCESSED / "pace_ship_gates.parquet")
    laps = pd.read_parquet(config.DATA_PROCESSED / "tier_b_laps.parquet")
    tp = pd.read_parquet(config.DATA_PROCESSED / "pace_team_best.parquet")
    diag = pd.read_parquet(config.DATA_PROCESSED / "pace_diagnostics.parquet")
    ret = pd.read_parquet(
        config.DATA_PROCESSED / "traffic_retention_by_circuit.parquet")

    bad = g[(g.rho_vs_finish < 0.5)
            & ((g.rho_vs_quali < 0.5) | g.rho_vs_quali.isna())].copy()

    rows = []
    for _, r in bad.iterrows():
        s, rd = int(r.season), int(r["round"])
        lg = laps[(laps.season == s) & (laps["round"] == rd)]
        tg = tp[(tp.season == s) & (tp["round"] == rd)]
        dg = diag[(diag.season == s) & (diag["round"] == rd)]
        circ_ret = ret[ret.event == r.event]["retention_pct"]
        deltas = np.sort(tg["delta"].to_numpy())
        rows.append({
            "season": s, "round": rd, "event": r.event,
            "rho_quali": round(r.rho_vs_quali, 3),
            "rho_finish": round(r.rho_vs_finish, 3),
            "teams": int(r.n_teams),
            "laps": len(lg),
            "laps_per_driver": round(len(lg) / max(lg.Driver.nunique(), 1), 1),
            "resid_sd": round(float(dg.resid_sd.iloc[0]), 3) if len(dg) else np.nan,
            "wet": bool(lg["session_rainfall"].iloc[0]) if len(lg) else None,
            "circuit_retention_pct": (round(float(circ_ret.iloc[0]), 1)
                                      if len(circ_ret) else np.nan),
            # Pace spread across teams: if this is small relative to residual
            # noise, no comparator can rank them and rho is uninformative.
            "pace_spread_pct": round(float(deltas[-1] - deltas[0]), 3),
            "pace_iqr_pct": round(float(np.percentile(deltas, 75)
                                        - np.percentile(deltas, 25)), 3),
        })

    df = pd.DataFrame(rows).sort_values(["season", "round"])
    pd.set_option("display.width", 260)
    print("=== GATE 3: races failing BOTH comparators ===")
    print(df.to_string(index=False))

    # Context: what does a typical race look like?
    ok = g[(g.rho_vs_finish >= 0.5) | (g.rho_vs_quali >= 0.5)]
    okl = []
    for _, r in ok.iterrows():
        tg = tp[(tp.season == r.season) & (tp["round"] == r["round"])]
        if len(tg) < 2:
            continue
        d = np.sort(tg["delta"].to_numpy())
        okl.append(np.percentile(d, 75) - np.percentile(d, 25))
    print(f"\nreference: median pace IQR across PASSING races = "
          f"{np.median(okl):.3f}%  (n={len(okl)})")
    print(f"           median pace IQR across FAILING races = "
          f"{df.pace_iqr_pct.median():.3f}%")

    df.to_parquet(config.DATA_PROCESSED / "gate3_investigation.parquet",
                  index=False)


if __name__ == "__main__":
    main()
