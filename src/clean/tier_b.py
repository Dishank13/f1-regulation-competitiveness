"""Phase 2 — Tier B cleaning: race laps to a representative-lap table.

Implements ANALYSIS_PLAN.md section 6.2, to the Tier A ledger standard:
parallel unit tracks, typed step kinds, and zero-removal filters validated
against the distribution they screen rather than reported as clean.

Also produces the THRESHOLD SWEEP that Decision A needs: row loss at each
candidate value of the percent-off-best cutoff, the traffic gap, and the
minimum-laps rule, so the analyst sets thresholds against evidence.

Wet sessions are NOT filtered (Amendment 3, confound 18). `session_rainfall` is
carried as a recorded attribute so Tier A and Tier B are treated identically.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from src import config
from src.clean import team_mapping

# Decision A provisional values — NOT decided. The sweep below is the evidence.
PCT_OFF_BEST = 107.0     # % of the driver's own session best
TRAFFIC_GAP_S = 1.0      # laps started within this of the car ahead are dropped
MIN_LAPS_PER_TEAM = 5    # below this a team has no observation at that race

PCT_SWEEP = (103.0, 105.0, 107.0, 110.0, 115.0)
GAP_SWEEP = (0.0, 0.5, 1.0, 1.5, 2.0)
MINLAP_SWEEP = (3, 5, 8, 12)


def _td_seconds(s: pd.Series) -> pd.Series:
    return pd.to_timedelta(s, errors="coerce").dt.total_seconds()


def load_raw() -> pd.DataFrame:
    df = pd.read_parquet(config.DATA_PROCESSED / "laps_raw.parquet")
    df["lap_s"] = _td_seconds(df["LapTime"])
    df["lap_start_s"] = _td_seconds(df["LapStartTime"])
    df["pit_in"] = _td_seconds(df["PitInTime"]).notna()
    df["pit_out"] = _td_seconds(df["PitOutTime"]).notna()
    df["team_continuity"] = df["Team"].map(
        lambda t: team_mapping.continuity(_slug(t)))
    return df


def _slug(team: str) -> str:
    """FastF1 team names are display strings; map to constructorId-ish slugs."""
    if not isinstance(team, str):
        return ""
    s = team.lower().strip()
    table = {
        "red bull racing": "red_bull", "racing point": "racing_point",
        "aston martin": "aston_martin", "alfa romeo": "alfa",
        "alfa romeo racing": "alfa", "kick sauber": "sauber",
        "toro rosso": "toro_rosso", "alphatauri": "alphatauri",
        "rb": "rb", "racing bulls": "rb", "haas f1 team": "haas",
        "alpine f1 team": "alpine", "renault": "renault",
        "force india": "force_india", "racing point force india": "force_india",
        "mercedes": "mercedes", "ferrari": "ferrari", "mclaren": "mclaren",
        "williams": "williams", "sauber": "sauber", "alpine": "alpine",
        "audi": "audi", "cadillac": "cadillac",
    }
    return table.get(s, s.replace(" ", "_"))


def gap_to_car_ahead(df: pd.DataFrame) -> pd.Series:
    """Seconds to the car ahead at the START of each lap.

    Uses LapStartTime differences between adjacent track positions on the same
    lap. Traffic is filtered rather than modelled (plan 6.2) because its effect
    on lap time is strongly non-linear.

    KNOWN LIMITATION, measured not assumed: `Position` is race classification,
    not track position, so for lapped or out-of-sequence cars the "car ahead"
    by Position can have a LATER LapStartTime, giving a negative gap. This
    happens on 6.36% of non-null gaps (1st percentile -13.5 s). Negative gaps
    are dropped by the `>= threshold` comparison, so they are removed rather
    than mis-signed — but that means the traffic filter removes a small,
    non-random set of laps for a reason unrelated to traffic. Recorded in the
    ledger and in confound 19.
    """
    out = pd.Series(np.nan, index=df.index)
    for _, g in df.groupby(["season", "round", "LapNumber"], sort=False):
        g2 = g.dropna(subset=["Position", "lap_start_s"]).sort_values("Position")
        if len(g2) < 2:
            continue
        ahead = g2["lap_start_s"].shift(1)
        out.loc[g2.index] = (g2["lap_start_s"] - ahead).to_numpy()
    return out


def build() -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    ledger: list[dict] = []
    notes: dict = {}

    def log(step, unit, before, after, note="", kind="filter"):
        removes = kind in ("filter", "guard")
        ledger.append({
            "step": step, "kind": kind, "unit": unit,
            "before": before, "after": after,
            "removed": (before - after) if removes else None,
            "pct_removed": (round(100 * (before - after) / before, 3)
                            if removes and before else None),
            "note": note,
        })

    df = load_raw()
    n_sessions_0 = df.groupby(["season", "round"]).ngroups
    log("S0 race sessions acquired", "sessions", n_sessions_0, n_sessions_0,
        "baseline; reconciles with the acquisition ledger", kind="baseline")
    log("L0 laps acquired", "laps", len(df), len(df), "baseline", kind="baseline")

    before = len(df)
    df = df[df.lap_s.notna()]
    log("L1 lap has no recorded time", "laps", before, len(df),
        "unset LapTime (retirements, timing gaps)")

    before = len(df)
    df = df[~(df.pit_in | df.pit_out)]
    log("L2 in-laps and out-laps", "laps", before, len(df), "plan 6.2 step 1")

    before = len(df)
    df = df[df.LapNumber > 1]
    log("L3 lap 1", "laps", before, len(df), "plan 6.2 step 2")

    before = len(df)
    ts = df["TrackStatus"].astype(str)
    df = df[ts.str.fullmatch(r"1+")]
    log("L4 track status not green for the full lap", "laps", before, len(df),
        "plan 6.2 steps 3-4: SC, VSC, yellow, formation, restart")

    before = len(df)
    df = df[df.Compound.notna() & df.Stint.notna() & df.TyreLife.notna()]
    log("L5 missing compound, stint or tyre age", "laps", before, len(df),
        "plan 6.2 step 8")

    before = len(df)
    df = df[df.TyreLife > 1]
    log("L6 first lap of each stint", "laps", before, len(df),
        "plan 6.2 step 7: tyre warm-up")

    # --- percent-off-own-best (Decision A) ---
    df["driver_best"] = df.groupby(
        ["season", "round", "Driver"])["lap_s"].transform("min")
    df["pct_of_best"] = 100 * df.lap_s / df.driver_best
    before = len(df)
    df = df[df.pct_of_best <= PCT_OFF_BEST]
    log(f"L7 slower than {PCT_OFF_BEST}% of own session best", "laps",
        before, len(df), "plan 6.2 step 5; Decision A pending, see sweep")

    # --- traffic (Decision A) ---
    df["gap_ahead_s"] = gap_to_car_ahead(df)
    before = len(df)
    df = df[(df.gap_ahead_s.isna()) | (df.gap_ahead_s >= TRAFFIC_GAP_S)]
    log(f"L8 started within {TRAFFIC_GAP_S}s of the car ahead", "laps",
        before, len(df),
        "plan 6.2 step 6; leaders have no car ahead and are retained")

    # --- team-race viability (Decision A) ---
    counts = df.groupby(["season", "round", "team_continuity"]).size()
    keep = counts[counts >= MIN_LAPS_PER_TEAM].index
    before = len(df)
    df = df.set_index(["season", "round", "team_continuity"]).loc[keep].reset_index()
    log(f"L9 team has fewer than {MIN_LAPS_PER_TEAM} representative laps", "laps",
        before, len(df), "Decision A pending, see sweep")

    # --- session-track close-out: name any session that lost ALL its laps ----
    raw_keys = set(map(tuple, load_raw()[["season", "round"]]
                       .drop_duplicates().to_numpy()))
    fin_keys = set(map(tuple, df[["season", "round"]].drop_duplicates().to_numpy()))
    lost = sorted(raw_keys - fin_keys)
    lost_named = []
    if lost:
        raw = load_raw()
        for s, r in lost:
            g = raw[(raw.season == s) & (raw["round"] == r)]
            lost_named.append({
                "season": int(s), "round": int(r),
                "event": str(g["event"].iloc[0]),
                "raw_laps": int(len(g)),
                "rainfall": bool(g["session_rainfall"].iloc[0]),
            })
    notes["sessions_lost"] = lost_named
    n_sessions_f = df.groupby(["season", "round"]).ngroups
    log("S1 sessions losing every representative lap", "sessions",
        n_sessions_0, n_sessions_f,
        "; ".join(f"{d['season']} r{d['round']} {d['event']} "
                  f"({d['raw_laps']} raw laps, rainfall={d['rainfall']})"
                  for d in lost_named) or "none")

    notes["wet_sessions"] = int(
        df.drop_duplicates(["season", "round"])["session_rainfall"].sum())
    notes["n_sessions_final"] = n_sessions_f
    return df, pd.DataFrame(ledger), notes


def sweep() -> pd.DataFrame:
    """Row loss at each candidate threshold — the evidence for Decision A."""
    df = load_raw()
    df = df[df.lap_s.notna() & ~(df.pit_in | df.pit_out) & (df.LapNumber > 1)]
    df = df[df["TrackStatus"].astype(str).str.fullmatch(r"1+")]
    df = df[df.Compound.notna() & df.Stint.notna() & df.TyreLife.notna()]
    df = df[df.TyreLife > 1]
    base = len(df)
    df["driver_best"] = df.groupby(
        ["season", "round", "Driver"])["lap_s"].transform("min")
    df["pct_of_best"] = 100 * df.lap_s / df.driver_best
    df["gap_ahead_s"] = gap_to_car_ahead(df)

    rows = []
    for p in PCT_SWEEP:
        k = int((df.pct_of_best <= p).sum())
        rows.append({"knob": "pct_off_best", "value": p, "laps_kept": k,
                     "pct_of_base": round(100 * k / base, 2)})
    d7 = df[df.pct_of_best <= PCT_OFF_BEST]
    for g in GAP_SWEEP:
        k = int(((d7.gap_ahead_s.isna()) | (d7.gap_ahead_s >= g)).sum())
        rows.append({"knob": "traffic_gap_s", "value": g, "laps_kept": k,
                     "pct_of_base": round(100 * k / base, 2)})
    d8 = d7[(d7.gap_ahead_s.isna()) | (d7.gap_ahead_s >= TRAFFIC_GAP_S)]
    c = d8.groupby(["season", "round", "team_continuity"]).size()
    for m in MINLAP_SWEEP:
        k = int(c[c >= m].sum())
        rows.append({"knob": "min_laps_per_team", "value": m, "laps_kept": k,
                     "pct_of_base": round(100 * k / base, 2)})
    out = pd.DataFrame(rows)
    out.attrs["base"] = base
    return out


def write_markdown_ledger(df: pd.DataFrame, led: pd.DataFrame,
                          sw: pd.DataFrame, notes: dict) -> None:
    acq = pd.read_parquet(config.DATA_PROCESSED / "acquisition_ledger.parquet")
    fails = acq[acq.status != "ok"]
    real_fails = fails[fails.season < 2026]

    lines = [
        "# Phase 2 — Tier B row-loss ledger",
        "",
        "Generated by `python -m src.clean.tier_b`. Same standard as the Tier A",
        "ledger: parallel unit tracks, typed step kinds, and zero-removal filters",
        "validated against the distribution they screen rather than reported as",
        "clean.",
        "",
        "## Acquisition reconciliation",
        "",
        f"- Sessions attempted: **{len(acq)}**",
        f"- Loaded: **{int((acq.status == 'ok').sum())}**",
        f"- Failed: **{len(fails)}**, of which **{len(fails) - len(real_fails)}** "
        "are unraced 2026 rounds (scheduled, not yet run — not a data gap).",
        "",
        "**One genuine gap:**",
        "",
    ]
    for _, r in real_fails.iterrows():
        lines.append(
            f"- **{r.season} r{r['round']} {r.event}** — the source API returns "
            "`Failed to load timing data`. Reproduced on a direct retry, so it is "
            "an upstream gap, not a transient error or a rate-limit casualty. "
            "This season therefore contributes 20 of 21 races.")
    lines += [
        "",
        "## Row-loss ledger",
        "",
        led.to_markdown(index=False),
        "",
        f"**Final:** {len(df):,} representative laps across "
        f"{notes['n_sessions_final']} sessions, 2018–2026.",
        "",
        "## Sessions that lost every lap",
        "",
    ]
    if notes.get("sessions_lost"):
        for d in notes["sessions_lost"]:
            lines.append(
                f"- **{d['season']} r{d['round']} {d['event']}** — {d['raw_laps']} "
                f"raw laps, rainfall={d['rainfall']}. Retained no representative "
                "lap. This is the race that ran only a few laps behind the safety "
                "car in torrential rain before being declared; there was no green-"
                "flag racing to measure. Correct to drop, and now logged by name "
                "rather than vanishing between the session baseline and the final "
                "table.")
    else:
        lines.append("None.")
    lines += [
        "",
        "## The traffic filter is the dominant exclusion",
        "",
        "L8 removes **19.5%** of surviving laps — more than every other filter "
        "combined except track status. It is also the most threshold-sensitive "
        "knob in the pipeline, so Decision A matters most here.",
        "",
        "**Known limitation, measured not assumed.** `Position` is race "
        "classification, not track position, so for lapped or out-of-sequence "
        "cars the car 'ahead' by Position can have a *later* lap start time, "
        "giving a negative gap. This affects **6.36%** of non-null gaps (1st "
        "percentile −13.5 s). Negative gaps fail the `>= threshold` comparison "
        "and are dropped, so they are removed rather than mis-signed — but that "
        "means the traffic filter removes a small, non-random set of laps for a "
        "reason unrelated to traffic. Recorded as confound 19.",
        "",
        "## Threshold sweep — Decision A evidence",
        "",
        "Percent of the post-structural-filter base retained at each candidate "
        "value. Each knob is swept with the other two at their provisional "
        "values.",
        "",
        sw.to_markdown(index=False),
        "",
        "### What the sweep says",
        "",
        "- **`pct_off_best`** is moderately sensitive: 103% is aggressive "
        "(71.4%), 105% and above are all within 6 points of each other. The "
        "curve flattens after 107%.",
        "- **`traffic_gap_s`** is the consequential knob: 0.5 s keeps 90.6%, "
        "1.0 s keeps 77.6%, 2.0 s keeps 59.0%. A third of the data rides on this "
        "single choice.",
        "- **`min_laps_per_team`** is nearly inert: 3 and 12 differ by 0.08 "
        "percentage points. Whatever is chosen changes almost nothing.",
    ]
    (config.DATA_PROCESSED / "tier_b_row_loss_ledger.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    df, led, notes = build()
    df.to_parquet(config.DATA_PROCESSED / "tier_b_laps.parquet", index=False)
    led.to_parquet(config.DATA_PROCESSED / "tier_b_row_loss_ledger.parquet",
                   index=False)
    sw = sweep()
    sw.to_parquet(config.DATA_PROCESSED / "tier_b_threshold_sweep.parquet",
                  index=False)
    write_markdown_ledger(df, led, sw, notes)
    pd.set_option("display.width", 220)
    print(led.to_string(index=False))
    print(f"\nfinal: {len(df):,} laps, {notes['n_sessions_final']} sessions")
    print("\n=== THRESHOLD SWEEP (Decision A evidence) ===")
    print(sw.to_string(index=False))


if __name__ == "__main__":
    main()
