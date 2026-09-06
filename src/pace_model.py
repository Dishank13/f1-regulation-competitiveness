"""Phase 3 — pace model (ANALYSIS_PLAN.md sections 4.3, 4.4).

Per race, on representative laps only, fit robustly (Huber):

    laptime = sum_d gamma_d * I[driver=d]
            + sum_c ( a_c + b_c * tyre_age ) * I[compound=c]
            + phi * lap_number
            + eps

gamma_d is the driver fixed effect and the quantity of interest. Tyre
degradation slopes b_c are ESTIMATED per compound, not assumed. phi is the
fuel-burn proxy, estimated per race rather than fixed at a folk constant.
Circuit, weather and surface are absorbed by fitting per race.

Team pace = the faster of the team's two drivers (plan 4.3), mirroring Tier A's
best-of-team convention. That imports driver quality, which is why M7 must be
reported alongside and why R14 re-runs with the both-drivers mean.

SHIP GATES (plan 4.4). The model does not ship until all four are produced and
reviewed. Gate 4 is a hard stop: if a known backmarker is ranked fastest, the
model is wrong and must be debugged, not shipped with a caveat.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.robust.robust_linear_model import RLM
from statsmodels.robust.norms import HuberT

from src import config

MIN_LAPS_FOR_FIT = 40      # per race, across all drivers
MIN_DRIVERS_FOR_FIT = 8


def fit_race(g: pd.DataFrame) -> tuple[pd.DataFrame | None, dict]:
    """Fit one race. Returns (driver coefficients, diagnostics)."""
    diag = {"n_laps": len(g), "n_drivers": g.Driver.nunique(), "status": ""}
    if len(g) < MIN_LAPS_FOR_FIT or g.Driver.nunique() < MIN_DRIVERS_FOR_FIT:
        diag["status"] = "too_few_laps"
        return None, diag

    drv = pd.get_dummies(g["Driver"], prefix="d", dtype=float)
    comp = pd.get_dummies(g["Compound"], prefix="c", dtype=float)
    age = pd.DataFrame(
        {f"age_{c}": comp[f"c_{c}"] * g["TyreLife"].to_numpy()
         for c in g["Compound"].unique()},
        index=g.index)

    # Driver dummies span the intercept, so no constant and drop one compound
    # dummy to avoid a second exact collinearity.
    comp_cols = list(comp.columns)[1:]
    X = pd.concat([drv, comp[comp_cols], age,
                   pd.Series(g["LapNumber"].to_numpy(), index=g.index,
                             name="lap_fuel")], axis=1)
    y = g["lap_s"].to_numpy()

    Xv = X.to_numpy(dtype=float)
    if np.linalg.matrix_rank(Xv) < Xv.shape[1]:
        diag["status"] = "rank_deficient"
        return None, diag

    try:
        res = RLM(y, Xv, M=HuberT()).fit()
    except Exception as exc:  # noqa: BLE001
        diag["status"] = f"fit_failed: {type(exc).__name__}"
        return None, diag

    params = pd.Series(res.params, index=X.columns)
    fitted = Xv @ res.params
    resid = y - fitted

    diag.update({
        "status": "ok",
        "resid_sd": float(np.std(resid, ddof=1)),
        "resid_mad": float(stats.median_abs_deviation(resid)),
        "fuel_s_per_lap": float(params.get("lap_fuel", np.nan)),
        "r2_pseudo": float(1 - np.var(resid) / np.var(y)),
    })
    deg = {k.replace("age_", ""): float(v)
           for k, v in params.items() if k.startswith("age_")}
    diag["deg_slopes"] = deg

    out = pd.DataFrame({
        "driver": [c[2:] for c in drv.columns],
        "gamma": [params[c] for c in drv.columns],
    })
    team = g.drop_duplicates("Driver").set_index("Driver")["team_continuity"]
    out["team"] = out.driver.map(team)
    out["resid_sd"] = diag["resid_sd"]
    return out, diag


def build() -> tuple[pd.DataFrame, pd.DataFrame]:
    laps = pd.read_parquet(config.DATA_PROCESSED / "tier_b_laps.parquet")
    coefs, diags = [], []
    for (season, rnd), g in laps.groupby(["season", "round"]):
        c, d = fit_race(g)
        d.update({"season": season, "round": rnd,
                  "event": g["event"].iloc[0]})
        diags.append(d)
        if c is not None:
            c["season"], c["round"] = season, rnd
            c["event"] = g["event"].iloc[0]
            coefs.append(c)
    return (pd.concat(coefs, ignore_index=True) if coefs else pd.DataFrame(),
            pd.DataFrame(diags))


def team_pace(coefs: pd.DataFrame, mode: str = "best") -> pd.DataFrame:
    """Collapse driver coefficients to team pace, then normalise per race.

    mode='best'  -> faster driver (plan 4.3 primary)
    mode='mean'  -> mean of both drivers (R14)
    """
    agg = "min" if mode == "best" else "mean"
    t = (coefs.groupby(["season", "round", "event", "team"])["gamma"]
         .agg(agg).reset_index().rename(columns={"gamma": "pace_s"}))
    t["best_event"] = t.groupby(["season", "round"])["pace_s"].transform("min")
    t["delta"] = 100 * (t.pace_s / t.best_event - 1)
    return t


def ship_gates(coefs: pd.DataFrame, diags: pd.DataFrame,
               laps: pd.DataFrame) -> pd.DataFrame:
    """Plan 4.4 gates 2 and 3, plus the gate-4 backmarker check."""
    t = team_pace(coefs)
    rows = []
    for (season, rnd), g in t.groupby(["season", "round"]):
        lg = laps[(laps.season == season) & (laps["round"] == rnd)]
        # Gate 3(b): recovered order vs finishing order of each team's lead car.
        fin = (lg.dropna(subset=["Position"])
               .sort_values("LapNumber").groupby("team_continuity")["Position"]
               .last())
        m = g.set_index("team")["delta"].to_frame().join(fin.rename("finish"))
        m = m.dropna()
        rho = (stats.spearmanr(m["delta"], m["finish"]).statistic
               if len(m) >= 4 else np.nan)
        rows.append({"season": season, "round": rnd,
                     "event": g["event"].iloc[0],
                     "rho_vs_finish": rho,
                     "n_teams": len(g),
                     "fastest_team": g.loc[g.delta.idxmin(), "team"]})
    return pd.DataFrame(rows)


def main() -> None:
    coefs, diags = build()
    laps = pd.read_parquet(config.DATA_PROCESSED / "tier_b_laps.parquet")
    coefs.to_parquet(config.DATA_PROCESSED / "pace_coefs.parquet", index=False)
    diags.to_parquet(config.DATA_PROCESSED / "pace_diagnostics.parquet", index=False)

    pd.set_option("display.width", 220)
    print("=== FIT STATUS ===")
    print(diags.status.value_counts().to_string())
    ok = diags[diags.status == "ok"]
    print(f"\nraces fitted: {len(ok)} / {len(diags)}")
    print("\n=== GATE 2: fit quality across races ===")
    print(ok[["resid_sd", "r2_pseudo", "fuel_s_per_lap"]]
          .describe(percentiles=[.05, .5, .95]).round(4).to_string())

    print("\nworst-fitting races by residual SD:")
    print(ok.nlargest(5, "resid_sd")[
        ["season", "round", "event", "resid_sd", "r2_pseudo"]]
        .round(3).to_string(index=False))

    print("\n=== GATE 3: recovered pace order vs finishing order ===")
    g = ship_gates(coefs, diags, laps)
    print(f"median Spearman rho = {g.rho_vs_finish.median():.3f}")
    bad = g[g.rho_vs_finish < 0.5]
    print(f"races with rho < 0.5 (flagged for investigation): {len(bad)}")
    if len(bad):
        print(bad[["season", "round", "event", "rho_vs_finish"]]
              .round(3).to_string(index=False))

    print("\n=== GATE 4: fastest-team sanity ===")
    print(g.fastest_team.value_counts().to_string())
    g.to_parquet(config.DATA_PROCESSED / "pace_ship_gates.parquet", index=False)

    for mode, name in (("best", "pace_team_best"), ("mean", "pace_team_mean")):
        team_pace(coefs, mode).to_parquet(
            config.DATA_PROCESSED / f"{name}.parquet", index=False)
    print("\nwrote team pace tables (best-of-team primary, both-drivers R14)")


if __name__ == "__main__":
    main()
