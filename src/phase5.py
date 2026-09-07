"""Phase 5 — confirmatory tests (ANALYSIS_PLAN.md sections 8.2-8.4).

PRIMARY METRIC: M2 (robust field spread, IQR). Frozen by the analyst before
this ran, on the grounds that the estimand is whole-field convergence and M2
measures that construct directly. M3 is a pre-registered DESIGNATED SECONDARY,
reported at every boundary, not competing for a confirmatory slot.

CONFIRMATORY FAMILY — 2 tests, Holm-Bonferroni at alpha = 0.05:
    1. pooled mu for b2 (H1, level)
    2. pooled mu for b3 (H2, slope) -- reported as a DESCRIPTIVE estimate per
       section 8.5.1; the slot is retained so the budget is not quietly reduced.

SECONDARY FAMILY -- 10 per-boundary estimates (5 boundaries x {b2, b3}),
Holm-corrected within family.

Pooling is random-effects (DerSimonian-Laird tau^2) with the
Hartung-Knapp-Sidik-Jonkman small-k adjustment, because k = 5.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats

from src import config

PRIMARY = "M2_iqr"
SECONDARY = "M3_midfield_pct"
WINDOW = 4
NBOOT = 10000
RNG = np.random.default_rng(config.RANDOM_SEED)


def its_fit(ev: pd.DataFrame, metric: str, boundary: int,
            window: int = WINDOW) -> dict:
    """Segmented interrupted time series on event-level values.

    metric ~ b0 + b1*(t) + b2*I[t>=0] + b3*(t)*I[t>=0], t = season - boundary.
    Standard errors by cluster bootstrap over EVENTS within season.
    """
    d = ev[(ev.season >= boundary - window)
           & (ev.season < boundary + window)][["season", metric]].dropna()
    if d.season.nunique() < 4:
        return {"boundary": boundary, "metric": metric, "b2": np.nan,
                "b3": np.nan, "se2": np.nan, "se3": np.nan, "n_events": len(d)}

    def design(seasons: np.ndarray) -> np.ndarray:
        t = seasons - boundary
        post = (t >= 0).astype(float)
        return np.column_stack([np.ones_like(t, dtype=float), t, post, t * post])

    y = d[metric].to_numpy(dtype=float)
    X = design(d.season.to_numpy(dtype=float))
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)

    seasons = d.season.unique()
    boots2, boots3 = [], []
    idx_by_season = {s: np.flatnonzero(d.season.to_numpy() == s) for s in seasons}
    for _ in range(NBOOT):
        take = np.concatenate([
            RNG.choice(idx_by_season[s], size=len(idx_by_season[s]), replace=True)
            for s in seasons])
        Xb, yb = X[take], y[take]
        try:
            bb, *_ = np.linalg.lstsq(Xb, yb, rcond=None)
        except np.linalg.LinAlgError:
            continue
        boots2.append(bb[2])
        boots3.append(bb[3])

    return {"boundary": boundary, "metric": metric,
            "b2": float(beta[2]), "b3": float(beta[3]),
            "se2": float(np.std(boots2, ddof=1)),
            "se3": float(np.std(boots3, ddof=1)),
            "b2_lo": float(np.percentile(boots2, 2.5)),
            "b2_hi": float(np.percentile(boots2, 97.5)),
            "b3_lo": float(np.percentile(boots3, 2.5)),
            "b3_hi": float(np.percentile(boots3, 97.5)),
            "n_events": len(d), "n_seasons": int(d.season.nunique())}


def pre_slope(ev: pd.DataFrame, metric: str, boundary: int,
              window: int = WINDOW) -> float:
    """Pre-boundary slope: the secular trend a level shift is read against."""
    d = ev[(ev.season >= boundary - window)
           & (ev.season < boundary)][["season", metric]].dropna()
    if d.season.nunique() < 3:
        return np.nan
    return float(np.polyfit(d.season.to_numpy(dtype=float),
                            d[metric].to_numpy(dtype=float), 1)[0])


def pool_hksj(est: np.ndarray, se: np.ndarray) -> dict:
    """Random-effects pooling with the Hartung-Knapp-Sidik-Jonkman adjustment.

    HKSJ rather than DerSimonian-Laird CIs because k is small (5): DL is
    anti-conservative there, and this is the confirmatory estimate.
    """
    ok = np.isfinite(est) & np.isfinite(se) & (se > 0)
    est, se = est[ok], se[ok]
    k = len(est)
    if k < 2:
        return {"k": k, "mu": np.nan}
    w = 1 / se ** 2
    mu_fe = float((w * est).sum() / w.sum())
    Q = float((w * (est - mu_fe) ** 2).sum())
    C = float(w.sum() - (w ** 2).sum() / w.sum())
    tau2 = max(0.0, (Q - (k - 1)) / C) if C > 0 else 0.0
    ws = 1 / (se ** 2 + tau2)
    mu = float((ws * est).sum() / ws.sum())
    # HKSJ variance
    q = float((ws * (est - mu) ** 2).sum() / (k - 1))
    se_hksj = float(np.sqrt(q / ws.sum()))
    tcrit = float(stats.t.ppf(0.975, k - 1))
    tstat = mu / se_hksj if se_hksj > 0 else np.nan
    p = float(2 * (1 - stats.t.cdf(abs(tstat), k - 1))) if np.isfinite(tstat) else np.nan
    I2 = float(max(0.0, (Q - (k - 1)) / Q) * 100) if Q > 0 else 0.0
    return {"k": k, "mu": mu, "se": se_hksj,
            "lo": mu - tcrit * se_hksj, "hi": mu + tcrit * se_hksj,
            "p": p, "tau2": tau2, "I2": I2, "Q": Q}


def holm(pvals: dict[str, float], alpha: float = 0.05) -> pd.DataFrame:
    items = sorted(((k, v) for k, v in pvals.items() if np.isfinite(v)),
                   key=lambda kv: kv[1])
    m = len(items)
    rows, reject_all = [], True
    for i, (name, p) in enumerate(items):
        thresh = alpha / (m - i)
        rej = bool(p < thresh and reject_all)
        if not rej:
            reject_all = False
        rows.append({"test": name, "p": p, "holm_threshold": thresh,
                     "reject_at_0.05": rej})
    return pd.DataFrame(rows)


def run(tier: str = "a") -> dict:
    ev = pd.read_parquet(
        config.DATA_PROCESSED / f"tier_{tier}_event_metrics.parquet")
    out: dict = {}
    for metric, label in ((PRIMARY, "primary"), (SECONDARY, "secondary")):
        fits = [its_fit(ev, metric, b) for b in config.RESET_BOUNDARIES]
        f = pd.DataFrame(fits)
        f["label"] = [config.RESET_BOUNDARIES[b]["label"] for b in f.boundary]
        f["pre_slope"] = [pre_slope(ev, metric, b) for b in f.boundary]
        f["role"] = label
        out[metric] = f
    return out


def main() -> None:
    res = run("a")
    pd.set_option("display.width", 250)

    print("### PHASE 5 — CONFIRMATORY (Tier A, primary metric M2_iqr) ###\n")
    pvals = {}
    for metric, f in res.items():
        role = f.role.iloc[0]
        print(f"--- {metric} ({role}) — per-boundary segmented ITS ---")
        print(f[["label", "b2", "b2_lo", "b2_hi", "b3", "b3_lo", "b3_hi",
                 "pre_slope", "n_events", "n_seasons"]].round(4).to_string(index=False))
        p2 = pool_hksj(f.b2.to_numpy(), f.se2.to_numpy())
        p3 = pool_hksj(f.b3.to_numpy(), f.se3.to_numpy())
        print(f"\n  POOLED b2 (H1, level): mu={p2['mu']:+.4f} "
              f"[{p2['lo']:+.4f}, {p2['hi']:+.4f}]  p={p2['p']:.4f}  "
              f"tau2={p2['tau2']:.5f}  I2={p2['I2']:.1f}%  k={p2['k']}")
        print(f"  POOLED b3 (H2, slope): mu={p3['mu']:+.4f} "
              f"[{p3['lo']:+.4f}, {p3['hi']:+.4f}]  p={p3['p']:.4f}  "
              f"tau2={p3['tau2']:.5f}  I2={p3['I2']:.1f}%  k={p3['k']}\n")
        if role == "primary":
            pvals["pooled_b2_H1_level"] = p2["p"]
            pvals["pooled_b3_H2_slope"] = p3["p"]
            pd.DataFrame([p2, p3], index=["b2", "b3"]).to_parquet(
                config.DATA_PROCESSED / "phase5_pooled_primary.parquet")
        f.to_parquet(
            config.DATA_PROCESSED / f"phase5_boundaries_{metric}.parquet",
            index=False)

    print("=== CONFIRMATORY FAMILY — 2 tests, Holm-Bonferroni at 0.05 ===")
    h = holm(pvals)
    print(h.round(5).to_string(index=False))
    h.to_parquet(config.DATA_PROCESSED / "phase5_holm.parquet", index=False)

    # Secondary family: 10 per-boundary estimates on the primary metric.
    f = res[PRIMARY]
    sec = {}
    for _, r in f.iterrows():
        for coef, se in (("b2", "se2"), ("b3", "se3")):
            if np.isfinite(r[coef]) and r[se] > 0:
                z = r[coef] / r[se]
                sec[f"{r.label}_{coef}"] = float(2 * (1 - stats.norm.cdf(abs(z))))
    print(f"\n=== SECONDARY FAMILY — {len(sec)} per-boundary estimates, "
          "Holm within family ===")
    hs = holm(sec)
    print(hs.round(5).to_string(index=False))
    hs.to_parquet(config.DATA_PROCESSED / "phase5_holm_secondary.parquet",
                  index=False)
    print(f"\nEXACT TEST COUNT: {len(pvals)} confirmatory + {len(sec)} secondary "
          f"= {len(pvals) + len(sec)} formally corrected tests.")


if __name__ == "__main__":
    main()
