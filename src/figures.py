"""Figures. Every chart answers a stated question (ANALYSIS_PLAN.md Phase 7).

Currently produces the plan §4.4 gate-1 diagnostics for the pace model:
residuals against fitted values, lap number, and tyre age. Gate 1 is the one
ship gate that cannot be reduced to a summary statistic — the point is to see
whether the fuel and degradation terms have absorbed the structure they claim
to absorb, or left it in the residuals.
"""

from __future__ import annotations

import warnings

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from statsmodels.robust.norms import HuberT  # noqa: E402
from statsmodels.robust.robust_linear_model import RLM  # noqa: E402

from src import config  # noqa: E402
from src.pace_model import MIN_LAPS_PER_COMPOUND  # noqa: E402

warnings.filterwarnings("ignore")


def residual_frame() -> pd.DataFrame:
    """Refit every race, keeping residuals with their lap number and tyre age."""
    laps = pd.read_parquet(config.DATA_PROCESSED / "tier_b_laps.parquet")
    out = []
    for (season, rnd), g in laps.groupby(["season", "round"]):
        counts = g["Compound"].value_counts()
        thin = counts[counts < MIN_LAPS_PER_COMPOUND].index.tolist()
        if thin:
            g = g[~g["Compound"].isin(thin)]
        if len(g) < 40 or g.Driver.nunique() < 8:
            continue
        drv = pd.get_dummies(g["Driver"], prefix="d", dtype=float)
        comp = pd.get_dummies(g["Compound"], prefix="c", dtype=float)
        age = pd.DataFrame(
            {f"age_{c}": comp[f"c_{c}"] * g["TyreLife"].to_numpy()
             for c in g["Compound"].unique()}, index=g.index)
        X = pd.concat([drv, comp[list(comp.columns)[1:]], age,
                       pd.Series(g["LapNumber"].to_numpy(), index=g.index,
                                 name="lap_fuel")], axis=1)
        Xv = X.to_numpy(dtype=float)
        y = g["lap_s"].to_numpy()
        if np.linalg.matrix_rank(Xv) < Xv.shape[1]:
            continue
        try:
            res = RLM(y, Xv, M=HuberT()).fit()
        except Exception:  # noqa: BLE001
            continue
        fitted = Xv @ res.params
        out.append(pd.DataFrame({
            "season": season, "round": rnd,
            "fitted": fitted, "resid": y - fitted,
            "lap": g["LapNumber"].to_numpy(),
            "age": g["TyreLife"].to_numpy(),
            "compound": g["Compound"].to_numpy(),
        }))
    return pd.concat(out, ignore_index=True)


def binned(x: np.ndarray, y: np.ndarray, nbins: int = 30):
    ok = np.isfinite(x) & np.isfinite(y)
    x, y = x[ok], y[ok]
    if len(x) < nbins * 5:
        return np.array([]), np.array([])
    qs = np.linspace(0, 100, nbins + 1)
    edges = np.unique(np.percentile(x, qs))
    idx = np.digitize(x, edges[1:-1])
    cx = np.array([x[idx == i].mean() for i in range(len(edges) - 1)
                   if (idx == i).sum() > 5])
    cy = np.array([np.median(y[idx == i]) for i in range(len(edges) - 1)
                   if (idx == i).sum() > 5])
    return cx, cy


def gate1(df: pd.DataFrame) -> None:
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.4))
    specs = [
        ("fitted", "Fitted lap time (s)",
         "Q: is the model unbiased across the lap-time range?"),
        ("lap", "Lap number (fuel proxy)",
         "Q: has the linear fuel term absorbed the fuel effect?"),
        ("age", "Tyre age (laps into stint)",
         "Q: have the per-compound slopes absorbed degradation?"),
    ]
    samp = df.sample(min(len(df), 40000), random_state=config.RANDOM_SEED)
    for ax, (col, xlabel, q) in zip(axes, specs):
        ax.scatter(samp[col], samp["resid"], s=1, alpha=0.05,
                   color="#4C72B0", rasterized=True)
        cx, cy = binned(df[col].to_numpy(), df["resid"].to_numpy())
        if len(cx):
            ax.plot(cx, cy, color="#C44E52", lw=2, label="binned median")
            ax.legend(loc="upper right", fontsize=8)
        ax.axhline(0, color="black", lw=0.8, ls="--")
        ax.set_xlabel(xlabel)
        ax.set_ylabel("Residual (s)")
        ax.set_ylim(-3, 3)
        ax.set_title(q, fontsize=9, loc="left")
    fig.suptitle(
        "Pace model gate 1 — residual structure (plan §4.4). A flat red line "
        "means the term absorbed its effect; a sloped or curved one means it "
        "did not.", fontsize=10)
    fig.tight_layout()
    out = config.FIGURES / "gate1_residuals.png"
    fig.savefig(out, dpi=130)
    plt.close(fig)
    print(f"wrote {out}")

    # Slope of residual on each axis: should be ~0 if the term did its job.
    print("\nresidual slope diagnostics (should be near zero):")
    for col, _, _ in specs:
        x = df[col].to_numpy(dtype=float)
        y = df["resid"].to_numpy(dtype=float)
        ok = np.isfinite(x) & np.isfinite(y)
        b = np.polyfit(x[ok], y[ok], 1)[0]
        print(f"  d(resid)/d({col}) = {b:+.5f}")


def main() -> None:
    df = residual_frame()
    df.to_parquet(config.DATA_PROCESSED / "pace_residuals.parquet", index=False)
    print(f"residual rows: {len(df):,}")
    gate1(df)


if __name__ == "__main__":
    main()
