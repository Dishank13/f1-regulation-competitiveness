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


METRIC_LABELS = {
    "M1_sd": "M1 · field spread (sd)",
    "M2_iqr": "M2 · robust spread (IQR)",
    "M3_midfield_pct": "M3 · leader→midfield",
    "M4_frontgap_pct": "M4 · front group vs rest",
    "M5_front_pair": "M5 · front-pair gap",
    "M6_backmarker": "M6 · backmarker gap",
}


def decision_b() -> None:
    """Metric behaviour over time, for the Decision B package.

    Question each panel answers: does this metric move at regulation
    boundaries in a way that is distinguishable from ordinary season churn?
    """
    a = pd.read_parquet(config.DATA_PROCESSED / "tier_a_season_metrics.parquet")
    b = pd.read_parquet(config.DATA_PROCESSED / "tier_b_season_metrics.parquet")
    resets = list(config.RESET_BOUNDARIES)

    fig, axes = plt.subplots(2, 3, figsize=(16, 8), sharex=True)
    for ax, (col, label) in zip(axes.ravel(), METRIC_LABELS.items()):
        ax.plot(a.season, a[col], "o-", color="#4C72B0", lw=1.8, ms=4,
                label="Tier A (qualifying)")
        ax.plot(b.season, b[col], "s--", color="#DD8452", lw=1.6, ms=4,
                label="Tier B (race pace)")
        if col == "M7_teammate":
            pass
        # Driver-noise floor: M7 from Tier A.
        ax.plot(a.season, a["M7_teammate"], ":", color="#55A868", lw=1.4,
                label="M7 driver-noise floor")
        for r in resets:
            ax.axvline(r, color="#C44E52", lw=1.0, alpha=0.55)
        ax.axvline(2010, color="#8172B3", lw=1.0, ls="-.", alpha=0.8)
        ax.set_title(label, fontsize=10, loc="left")
        ax.set_ylabel("% off fastest")
        ax.grid(alpha=0.25)
        if col == "M5_front_pair":
            ax.set_title(label + "  — RETIRED: below driver-noise floor",
                         fontsize=10, loc="left", color="#C44E52")
        if col == "M4_frontgap_pct":
            ax.set_title(label + "  — no cross-2010 claims (D1c)",
                         fontsize=10, loc="left", color="#C44E52")
    axes[0, 0].legend(fontsize=8, loc="upper right")
    for ax in axes[1]:
        ax.set_xlabel("season")
    for ax in axes.ravel():
        ax.set_xticks([2006, 2010, 2014, 2018, 2022, 2026])
        ax.set_xticklabels(["2006", "2010", "2014", "2018", "2022", "2026"])
    fig.suptitle(
        "Decision B — metric candidates: does each move at regulation "
        "boundaries distinguishably from ordinary season churn?\n"
        "Red: regulation boundaries.   Purple dash-dot: 2010, a "
        "measurement-artifact boundary (grid 10→12 with three new backmarkers, "
        "refuelling ban, segment eligibility).\n"
        "Green dotted: the M7 driver-noise floor — a metric below it cannot "
        "resolve a car effect.", fontsize=10, y=0.995)
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    out = config.FIGURES / "decision_b_metrics.png"
    fig.savefig(out, dpi=130)
    plt.close(fig)
    print(f"wrote {out}")


def readme_figures() -> None:
    """Three publication charts for the README. Captions are in the README."""
    a = pd.read_parquet(config.DATA_PROCESSED / "tier_a_season_metrics.parquet")
    resets = list(config.RESET_BOUNDARIES)

    # --- (a) M2 over time -----------------------------------------------------
    fig, ax = plt.subplots(figsize=(11, 5.4))
    for i, r in enumerate(resets):
        ax.axvline(r, color="#C0392B", lw=1.6, alpha=0.75, zorder=1,
                   label="season a new rule package took effect" if i == 0 else None)
    ax.axvline(2010, color="#7D3C98", lw=1.8, ls="-.", alpha=0.95, zorder=1,
               label="2010 — measurement changes, not a rule reset")
    ax.plot(a.season, a.M2_iqr, "o-", color="#2B4C7E", lw=2.4, ms=6, zorder=3,
            label="spread of car pace")
    ax.set_xlabel("season")
    ax.set_ylabel("spread of car pace across the field\n(% off the fastest car)")
    ax.set_title("How far apart the cars were, 2006–2026", fontsize=13, loc="left")
    ax.set_xticks(resets + [2006, 2018])
    ax.set_xticklabels([str(r) for r in resets] + ["2006", "2018"], fontsize=9)
    ax.grid(alpha=0.25)
    ax.margins(x=0.02)
    ax.legend(fontsize=9, loc="upper right", framealpha=0.95)
    fig.tight_layout()
    fig.savefig(config.FIGURES / "fig1_field_spread.png", dpi=140)
    plt.close(fig)

    # --- (b) per-boundary estimates, both specifications ----------------------
    fw = pd.read_parquet(config.DATA_PROCESSED / "phase5_boundaries_M2_iqr.parquet")
    r16 = pd.read_parquet(config.DATA_PROCESSED / "r16_stratified.parquet")
    m = fw[["label", "b2", "b2_lo", "b2_hi"]].merge(
        r16[["label", "b2_stratified", "b2_lo_stratified", "b2_hi_stratified"]],
        on="label")
    y = np.arange(len(m))[::-1]

    fig, ax = plt.subplots(figsize=(10, 4.6))
    for off, (est, lo, hi), col, lab in (
            (+0.15, ("b2", "b2_lo", "b2_hi"), "#2B4C7E", "main method"),
            (-0.15, ("b2_stratified", "b2_lo_stratified", "b2_hi_stratified"),
             "#E08A2E", "alternative method")):
        ax.errorbar(m[est], y + off,
                    xerr=[m[est] - m[lo], m[hi] - m[est]],
                    fmt="o", color=col, ms=7, capsize=4, lw=2, label=lab)
    ax.axvline(0, color="black", lw=1.4, zorder=0)
    ax.set_yticks(y)
    ax.set_yticklabels(m.label)
    ax.set_xlabel("change in field spread at the rule change\n"
                  "← cars got closer      cars spread apart →")
    ax.set_title("What happened to the field at each rule change",
                 fontsize=13, loc="left")
    ax.legend(fontsize=9, loc="lower right")
    ax.grid(axis="x", alpha=0.25)
    fig.tight_layout()
    fig.savefig(config.FIGURES / "fig2_boundary_estimates.png", dpi=140)
    plt.close(fig)

    # --- (c) placebo distribution with the resets inside it -------------------
    pl = pd.read_parquet(config.DATA_PROCESSED / "placebo_tier_a.parquet")
    pl = pl[pl.metric == "M2_iqr"]
    plac = pl[pl.kind == "placebo"]["shift"].dropna()
    res = pl[pl.kind == "reset"][["label", "shift"]].dropna()

    fig, ax = plt.subplots(figsize=(11, 4.6))
    ax.scatter(plac, np.zeros(len(plac)) + 0.06,
               s=90, color="#9AA5B1", edgecolor="white", zorder=3,
               label=f"ordinary seasons, no rule change (n={len(plac)})")
    colors = ["#C0392B" if s > 0 else "#1E8449" for s in res["shift"]]
    ax.scatter(res["shift"], np.zeros(len(res)) - 0.06, s=150, marker="D",
               color=colors, edgecolor="black", zorder=4,
               label="seasons with a rule change (n=5)")
    # Stagger labels so near-coincident points (2014 and 2021-22) do not collide.
    order = res.sort_values("shift").reset_index(drop=True)
    for i, r in order.iterrows():
        dy = -20 if i % 2 == 0 else -34
        ax.annotate(r.label, (r["shift"], -0.06), textcoords="offset points",
                    xytext=(0, dy), ha="center", fontsize=9)
    ax.axvline(0, color="black", lw=1.2)
    ax.set_ylim(-0.30, 0.16)
    ax.set_yticks([])
    ax.set_xlabel("change in field spread from one season to the next\n"
                  "← cars got closer      cars spread apart →")
    ax.set_title("Rule changes compared with ordinary seasons",
                 fontsize=13, loc="left")
    ax.legend(fontsize=9, loc="upper left")
    ax.grid(axis="x", alpha=0.25)
    fig.tight_layout()
    fig.savefig(config.FIGURES / "fig3_placebo_comparison.png", dpi=140)
    plt.close(fig)

    for f in ("fig1_field_spread.png", "fig2_boundary_estimates.png",
              "fig3_placebo_comparison.png"):
        print(f"wrote {config.FIGURES / f}")


def main() -> None:
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "decision_b":
        decision_b()
        return
    if len(sys.argv) > 1 and sys.argv[1] == "readme":
        readme_figures()
        return
    df = residual_frame()
    df.to_parquet(config.DATA_PROCESSED / "pace_residuals.parquet", index=False)
    print(f"residual rows: {len(df):,}")
    gate1(df)


if __name__ == "__main__":
    main()
