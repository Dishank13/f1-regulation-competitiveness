"""Phase 4 — competitiveness metrics (ANALYSIS_PLAN.md section 4.2).

Computes M1-M7 per event, aggregates to seasons by median, and runs D1c.

Metric definitions are PERCENTILE-based where a percentile definition is
meaningful, because grid size varies across the study window and fixed rank
windows are not comparable across seasons (plan 4.2). Fixed-rank forms are
retained as the R15 robustness variant and computed alongside.

NOTHING here chooses a primary metric. Decision B is the analyst's and is taken
after seeing these.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from src import config

RNG = np.random.default_rng(config.RANDOM_SEED)


def event_metrics(g: pd.DataFrame) -> pd.Series:
    """M1-M6 for one event. `g` is that event's team rows, column `delta`."""
    d = np.sort(g["delta"].to_numpy())
    n = len(d)
    out: dict[str, float] = {"n_teams": n}

    out["M1_sd"] = float(np.std(d, ddof=1)) if n > 1 else np.nan
    out["M2_iqr"] = float(np.percentile(d, 75) - np.percentile(d, 25))

    # M3 leader-to-midfield: median of the 30th-70th percentile band.
    lo, hi = np.percentile(d, 30), np.percentile(d, 70)
    band = d[(d >= lo) & (d <= hi)]
    out["M3_midfield_pct"] = float(np.median(band)) if len(band) else np.nan

    # M4 front-group vs rest, by percentile.
    cut = np.percentile(d, 20)
    front, rest = d[d <= cut], d[d > cut]
    out["M4_frontgap_pct"] = (float(np.mean(rest) - np.mean(front))
                              if len(front) and len(rest) else np.nan)

    out["M5_front_pair"] = float(d[1]) if n > 1 else np.nan
    out["M6_backmarker"] = float(d[-1])

    # R15 fixed-rank variants (plan 4.2, 11).
    out["M3_midfield_rank47"] = (float(np.median(d[3:7])) if n >= 7 else np.nan)
    out["M4_frontgap_top2"] = (float(np.mean(d[2:]) - np.mean(d[:2]))
                               if n > 2 else np.nan)
    return pd.Series(out)


def teammate_delta(drivers: pd.DataFrame) -> pd.DataFrame:
    """M7: median absolute within-team driver delta, per event."""
    rows = []
    for (season, rnd), g in drivers.groupby(["season", "round"]):
        diffs = []
        for _, tg in g.groupby("team_continuity"):
            if len(tg) >= 2:
                dd = np.sort(tg["delta"].to_numpy())
                diffs.append(abs(dd[1] - dd[0]))
        rows.append({"season": season, "round": rnd,
                     "M7_teammate": float(np.median(diffs)) if diffs else np.nan,
                     "n_pairs": len(diffs)})
    return pd.DataFrame(rows)


def load_tier(tier: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return (team-event, driver-event) tables with a common schema.

    Tier A is qualifying pace; Tier B is fuel- and tyre-corrected race pace.
    Both carry `delta` = % off the fastest team at that event, so M1-M7 are
    computed by identical code and the two tiers measure the same construct.
    """
    if tier == "a":
        teams = pd.read_parquet(config.DATA_PROCESSED / "tier_a_team_event.parquet")
        drivers = pd.read_parquet(
            config.DATA_PROCESSED / "tier_a_driver_event.parquet")
        return teams, drivers

    teams = pd.read_parquet(config.DATA_PROCESSED / "pace_team_best.parquet")
    teams = teams.rename(columns={"team": "team_continuity"})
    coefs = pd.read_parquet(config.DATA_PROCESSED / "pace_coefs.parquet")
    coefs = coefs.rename(columns={"team": "team_continuity"})
    coefs["best_event"] = coefs.groupby(["season", "round"])["gamma"].transform("min")
    coefs["delta"] = 100 * (coefs.gamma / coefs.best_event - 1)
    return teams, coefs


def build(tier: str = "a") -> tuple[pd.DataFrame, pd.DataFrame]:
    teams, drivers = load_tier(tier)

    ev = (teams.groupby(["season", "round"]).apply(event_metrics, include_groups=False)
          .reset_index())
    ev = ev.merge(teammate_delta(drivers), on=["season", "round"], how="left")

    metric_cols = [c for c in ev.columns
                   if c.startswith(("M1", "M2", "M3", "M4", "M5", "M6", "M7"))]
    season = ev.groupby("season")[metric_cols].median().reset_index()
    season["n_events"] = ev.groupby("season").size().to_numpy()
    return ev, season


def boot_median_ci(x: np.ndarray, n: int = 10000) -> tuple[float, float]:
    x = x[~np.isnan(x)]
    if len(x) < 3:
        return (np.nan, np.nan)
    idx = RNG.integers(0, len(x), size=(n, len(x)))
    m = np.median(x[idx], axis=1)
    return (float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5)))


def level_shift(ev: pd.DataFrame, metric: str, boundary: int,
                window: int = 4) -> dict:
    """Median metric after minus before a season boundary, event-level,
    with a cluster bootstrap over events."""
    pre = ev[(ev.season >= boundary - window) & (ev.season < boundary)][metric]
    post = ev[(ev.season >= boundary) & (ev.season < boundary + window)][metric]
    a, b = pre.dropna().to_numpy(), post.dropna().to_numpy()
    if len(a) < 5 or len(b) < 5:
        return {"metric": metric, "boundary": boundary, "shift": np.nan,
                "lo": np.nan, "hi": np.nan, "n_pre": len(a), "n_post": len(b)}
    n = 10000
    da = np.median(a[RNG.integers(0, len(a), size=(n, len(a)))], axis=1)
    db = np.median(b[RNG.integers(0, len(b), size=(n, len(b)))], axis=1)
    diff = db - da
    lo, hi = np.percentile(diff, [2.5, 97.5])
    return {"metric": metric, "boundary": boundary,
            "shift": float(np.median(b) - np.median(a)),
            "lo": float(lo), "hi": float(hi),
            "n_pre": len(a), "n_post": len(b)}


def d1c(ev: pd.DataFrame) -> pd.DataFrame:
    """D1c (plan 4.1.2, 4.1.3): do the front-of-field metrics step at 2010?

    2010 is where Tier A's front-of-field measurement basis changes (front-third
    Q3 sourcing 0% -> 57.7%) AND where the refuelling ban lands; the two cannot
    be separated. M1/M2 are whole-field controls: the bias signature is a step in
    M4/M5 that M1/M2 do not show.

    PRE-COMMITTED RULE (plan 4.1.3): if M4 or M5 shows a 2010 level shift at
    least half the median absolute reset-boundary shift on the same metric, that
    metric cannot carry a cross-2010 claim and is restricted to within-era
    comparison.
    """
    metrics = ["M4_frontgap_pct", "M5_front_pair", "M1_sd", "M2_iqr"]
    rows = []
    for m in metrics:
        art = level_shift(ev, m, 2010)
        resets = [level_shift(ev, m, b) for b in config.RESET_BOUNDARIES]
        ref = np.nanmedian([abs(r["shift"]) for r in resets])
        trig = (abs(art["shift"]) >= 0.5 * ref) if np.isfinite(art["shift"]) else False
        rows.append({
            "metric": m,
            "shift_2010": art["shift"], "lo": art["lo"], "hi": art["hi"],
            "median_abs_reset_shift": ref,
            "threshold_half_reset": 0.5 * ref,
            "front_of_field": m in ("M4_frontgap_pct", "M5_front_pair"),
            "RESTRICTION_TRIGGERED": bool(trig and m in ("M4_frontgap_pct",
                                                         "M5_front_pair")),
        })
    return pd.DataFrame(rows)


def main() -> None:
    import sys
    tier = sys.argv[1].lower() if len(sys.argv) > 1 else "a"
    ev, season = build(tier)
    ev.to_parquet(config.DATA_PROCESSED / f"tier_{tier}_event_metrics.parquet",
                  index=False)
    season.to_parquet(config.DATA_PROCESSED / f"tier_{tier}_season_metrics.parquet",
                      index=False)
    print(f"### TIER {tier.upper()} ###")

    pd.set_option("display.width", 200)
    print("=== SEASON-LEVEL METRICS (median across events, % off fastest) ===")
    show = ["season", "n_events", "M1_sd", "M2_iqr", "M3_midfield_pct",
            "M4_frontgap_pct", "M5_front_pair", "M6_backmarker", "M7_teammate"]
    print(season[show].round(3).to_string(index=False))

    if tier != "a":
        # D1c is a Tier A test by construction: the 2010 boundary predates the
        # Tier B window entirely. Running it here would write NaNs over the
        # Tier A result.
        print("\n(D1c skipped: it is a Tier A test; 2010 predates Tier B.)")
        return

    print("\n=== D1c — front-of-field step at 2010 (pre-committed rule) ===")
    d = d1c(ev)
    print(d.round(4).to_string(index=False))
    trig = d[d.RESTRICTION_TRIGGERED]
    if len(trig):
        print("\n*** RESTRICTION TRIGGERED for: "
              f"{', '.join(trig.metric)} — these metrics cannot carry a "
              "cross-2010 claim (plan 4.1.3). ***")
    else:
        print("\nNo restriction triggered: neither M4 nor M5 steps at 2010 by "
              "at least half the median absolute reset-boundary shift.")
    d.to_parquet(config.DATA_PROCESSED / "d1c_results.parquet", index=False)


if __name__ == "__main__":
    main()
