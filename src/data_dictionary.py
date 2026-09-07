"""Generate the data dictionary for every processed table (plan §13).

Plan §13 commits to "a data dictionary naming every column, its units, and its
provenance" for each processed table. Hand-writing 40 of those would rot on the
first schema change, so this introspects the Parquet files for structure and
merges curated text for units and meaning. Re-running after a pipeline change
regenerates it.

Output: data/processed/dictionary.md (committed; the Parquet is not).
"""

from __future__ import annotations

import pandas as pd

from src import config

# table -> (producing module, what it is)
TABLES: dict[str, tuple[str, str]] = {
    "coverage_tier_a": ("src.coverage_tier_a", "Per-season Tier A coverage scan: rounds, entrants, segment population, and the within-driver segment deltas that revealed race-fuel qualifying in 2006-09."),
    "coverage_tier_b": ("src.coverage_tier_b", "FastF1 availability probe, two rounds per season, establishing the 2018 lap-data floor empirically."),
    "acquisition_ledger": ("src.ingest.fastf1_races", "One row per race session attempted, with status and error. A session absent from the lap table is always traceable to a row here."),
    "laps_raw": ("src.ingest.fastf1_races", "Every acquired race lap, unfiltered. Phase 2 input."),
    "weather_quali": ("src.ingest.weather", "Venue precipitation on each qualifying date (Open-Meteo). RETAINED BUT UNUSED - the wet flag was rejected (Amendment 3)."),
    "session_formats": ("src.clean.session_format", "Sprint format version per event, cross-checked between two sources with zero disagreements."),
    "tier_a_team_event": ("src.clean.tier_a", "PRIMARY TIER A TABLE. One row per team per event: evolution-adjusted best qualifying lap and its percentage off the fastest team."),
    "tier_a_driver_event": ("src.clean.tier_a", "As above but per driver. Feeds M7, the within-team driver spread."),
    "tier_a_row_loss_ledger": ("src.clean.tier_a", "Per-filter row counts for Tier A cleaning, on three parallel unit tracks."),
    "tier_b_laps": ("src.clean.tier_b", "PRIMARY TIER B TABLE. Representative race laps surviving all filters."),
    "tier_b_row_loss_ledger": ("src.clean.tier_b", "Per-filter row counts for Tier B cleaning."),
    "tier_b_threshold_sweep": ("src.clean.tier_b", "Laps retained at each candidate Decision A threshold."),
    "pace_coefs": ("src.pace_model", "Per-race driver fixed effects from the Huber regression - the recovered car pace."),
    "pace_diagnostics": ("src.pace_model", "Per-race fit quality: residual spread, pseudo-R2, estimated fuel coefficient, compounds dropped."),
    "pace_ship_gates": ("src.pace_model", "Plan §4.4 gates 3 and 4: recovered pace order against qualifying and finishing order."),
    "pace_team_best": ("src.pace_model", "Team race pace, faster of the two drivers (primary convention)."),
    "pace_team_mean": ("src.pace_model", "Team race pace, mean of both drivers (R14 variant)."),
    "pace_residuals": ("src.figures", "Model residuals with lap number and tyre age, for the gate-1 plots."),
    "tier_a_event_metrics": ("src.metrics", "M1-M7 per Tier A event."),
    "tier_a_season_metrics": ("src.metrics", "M1-M7 per season, median across events."),
    "tier_b_event_metrics": ("src.metrics", "M1-M7 per Tier B race."),
    "tier_b_season_metrics": ("src.metrics", "M1-M7 per season from race pace."),
    "d1c_results": ("src.metrics", "D1c: the pre-committed 2010 front-of-field test and whether the M4 restriction triggered."),
    "d1a_stratum_offsets": ("src.diagnostics_d1", "D1a: Q1->Q2 offset estimated separately for front and back of the field, per event."),
    "decision_a_traffic_curve": ("src.decision_a_evidence", "Lap-time penalty against gap to the car ahead, measured within driver-stint cells."),
    "traffic_retention_by_season": ("src.traffic_bias", "Share of laps surviving the traffic filter, per season. Used for the endogeneity finding."),
    "traffic_retention_by_circuit": ("src.traffic_bias", "Share of laps surviving the traffic filter, per circuit."),
    "gate3_investigation": ("src.gate3_investigation", "Evidence assembled for each race failing both gate-3 comparators."),
    "placebo_tier_a": ("src.placebo", "Level shift at every boundary: nine controls, one artifact boundary, five resets."),
    "placebo_percentiles_tier_a": ("src.placebo", "Each reset's shift as a percentile of the placebo distribution."),
    "phase5_boundaries_M2_iqr": ("src.phase5", "Segmented ITS per boundary on the PRIMARY metric M2."),
    "phase5_boundaries_M3_midfield_pct": ("src.phase5", "Segmented ITS per boundary on the designated secondary metric M3."),
    "phase5_pooled_primary": ("src.phase5", "Random-effects pooled estimate with HKSJ small-k adjustment. THE CONFIRMATORY RESULT."),
    "phase5_holm": ("src.phase5", "Holm-Bonferroni correction across the 2-test confirmatory family."),
    "phase5_holm_secondary": ("src.phase5", "Holm correction across the 9 per-boundary secondary estimates."),
    "robustness_battery": ("src.robustness", "The 16-check battery: what each varies and whether the headline survives."),
    "r16_stratified": ("src.r16_stratified", "R16: per-boundary estimates under field-wide versus stratified evolution offset."),
    "trend_decomposition": ("src.trend_decomposition", "Season-to-season change in M2, flagged by whether the transition enters a reset season. DESCRIPTIVE ONLY."),
    "finding_e_compounds": ("src.finding_e", "Q2 and Q3 fastest-lap tyre compound per driver per event, 2018-2026."),
    "finding_e_result": ("src.finding_e", "Share of Q3-reaching drivers whose Q2 compound differs from Q3, per season."),
}

# column -> (units, meaning). Applied across every table that has the column.
COLUMNS: dict[str, tuple[str, str]] = {
    "season": ("year", "Championship season."),
    "round": ("integer", "Championship round within the season."),
    "event": ("text", "Grand Prix name."),
    "driver": ("id", "Driver identifier."),
    "Driver": ("code", "Three-letter driver code (FastF1)."),
    "constructor": ("id", "Constructor identifier as published by the source."),
    "team_continuity": ("id", "Constructor lineage under the CONTINUITY mapping (primary). See src/clean/team_mapping.py."),
    "team_strict": ("id", "Constructor under the STRICT mapping (R2): each name its own entity."),
    "team": ("id", "Constructor lineage."),
    "Team": ("text", "Team display name (FastF1)."),
    "segment": ("Q1/Q2/Q3", "Qualifying segment the lap was set in."),
    "source_segment": ("Q1/Q2/Q3", "Which segment supplied this team's representative lap."),
    "time": ("seconds", "Raw lap time."),
    "time_adj": ("seconds", "Lap time after the segment-evolution adjustment (plan §4.1)."),
    "offset": ("seconds", "Evolution offset subtracted, referenced to Q1."),
    "q_adj": ("seconds", "Team's best adjusted qualifying lap at this event."),
    "q_best_event": ("seconds", "Fastest team's adjusted lap at this event."),
    "delta": ("percent", "Percentage off the fastest car at this event. 0 for the fastest team by construction. THE CORE QUANTITY."),
    "lap_s": ("seconds", "Lap time."),
    "lap_start_s": ("seconds", "Lap start, measured from session start."),
    "LapNumber": ("integer", "Lap of the race. Used as the fuel-burn proxy."),
    "TyreLife": ("laps", "Laps completed on the current tyre set."),
    "Compound": ("text", "Tyre compound."),
    "Stint": ("integer", "Stint number within the race."),
    "TrackStatus": ("code", "Marshalling status during the lap; '1' throughout means green."),
    "Position": ("integer", "Race classification position - NOT track position (confound 19)."),
    "gap_ahead_s": ("seconds", "Gap to the car ahead at lap start. Negative values arise from the classification-vs-track-position issue and are dropped."),
    "pct_of_best": ("percent", "Lap as a percentage of that driver's own session best."),
    "driver_best": ("seconds", "Driver's fastest lap in the session."),
    "session_rainfall": ("boolean", "Whether rain was recorded during the session. RECORDED, NOT FILTERED (Amendment 3)."),
    "format_version": ("text", "Session format: conventional, sprint, sprint_shootout, sprint_qualifying."),
    "has_sprint_race": ("boolean", "Whether the event held a sprint race."),
    "gamma": ("seconds", "Driver fixed effect from the pace model: recovered lap time net of fuel, compound and tyre age."),
    "pace_s": ("seconds", "Team pace from the model."),
    "best_event": ("seconds", "Fastest team's modelled pace at this event."),
    "resid_sd": ("seconds", "Standard deviation of model residuals for the race."),
    "resid_mad": ("seconds", "Median absolute deviation of residuals."),
    "r2_pseudo": ("fraction", "1 - var(residual)/var(lap time)."),
    "fuel_s_per_lap": ("seconds/lap", "Estimated fuel effect. Negative: cars speed up as fuel burns."),
    "rho_vs_quali": ("correlation", "Spearman correlation of recovered pace order against qualifying order (gate 3a)."),
    "rho_vs_finish": ("correlation", "Spearman correlation against finishing order (gate 3b)."),
    "fastest_team": ("id", "Team ranked fastest by the model (gate 4)."),
    "b2": ("percent", "ITS LEVEL change at the boundary. Positive = the field spread apart."),
    "b3": ("percent/season", "ITS SLOPE change after the boundary."),
    "b2_lo": ("percent", "Lower bound, 95% cluster-bootstrap interval."),
    "b2_hi": ("percent", "Upper bound, 95% cluster-bootstrap interval."),
    "se2": ("percent", "Bootstrap standard error of b2."),
    "se3": ("percent/season", "Bootstrap standard error of b3."),
    "pre_slope": ("percent/season", "Trend in the seasons BEFORE the boundary - the secular decline a level change is read against."),
    "shift": ("percent", "Simple pre/post median difference (no trend control)."),
    "mu": ("percent", "Random-effects pooled estimate."),
    "tau2": ("percent^2", "Between-boundary variance."),
    "I2": ("percent", "Share of variation due to between-boundary heterogeneity, not sampling error."),
    "p": ("probability", "Two-sided p-value."),
    "kind": ("text", "Row type: placebo, artifact, reset - or for ledgers: baseline, filter, transform, aggregate, guard."),
    "removed": ("rows", "Rows removed by this step. Null for non-removing step kinds."),
    "pct_removed": ("percent", "Share removed by this step."),
    "survives": ("boolean", "Whether the check reproduces the headline's direction and significance verdict."),
    "M1_sd": ("percent", "Standard deviation of team delta across the field."),
    "M2_iqr": ("percent", "Interquartile range of team delta. THE PRIMARY METRIC."),
    "M3_midfield_pct": ("percent", "Median delta among teams in the 30th-70th percentile band."),
    "M3_midfield_rank47": ("percent", "R15 variant: median delta of ranks 4-7."),
    "M4_frontgap_pct": ("percent", "Mean delta above the 20th percentile minus mean of the fastest 20%."),
    "M5_front_pair": ("percent", "Delta of the second-fastest team. RETIRED: below the driver-noise floor."),
    "M6_backmarker": ("percent", "Delta of the slowest team. Diagnostic for grid composition."),
    "M7_teammate": ("percent", "Median within-team driver delta. The driver-noise floor."),
    "precip_daily_mm": ("millimetres", "Total precipitation at the venue on the qualifying date."),
    "retention_pct": ("percent", "Share of laps surviving the traffic filter."),
    "differs": ("boolean", "Whether the driver's Q2 compound differs from their Q3 compound."),
}


def main() -> None:
    files = sorted(config.DATA_PROCESSED.glob("*.parquet"))
    lines = [
        "# Data dictionary",
        "",
        "Generated by `python -m src.data_dictionary`. Plan §13 commits to a data",
        "dictionary naming every column, its units, and its provenance for each",
        "processed table.",
        "",
        "Structure is read from the Parquet files; units and meaning are curated in",
        "`src/data_dictionary.py`. The Parquet files themselves are gitignored and",
        "rebuilt by `python -m src.pipeline`; this document is committed.",
        "",
        f"**{len(files)} processed tables.**",
        "",
        "---",
        "",
    ]
    undocumented: set[str] = set()

    for f in files:
        name = f.stem
        module, purpose = TABLES.get(name, ("(unknown)", "(undocumented table)"))
        try:
            df = pd.read_parquet(f)
        except Exception as exc:  # noqa: BLE001
            lines += [f"## `{name}`", "", f"could not be read: {exc}", ""]
            continue
        lines += [
            f"## `{name}.parquet`",
            "",
            f"{purpose}",
            "",
            f"**Produced by:** `{module}` — **{len(df):,} rows, "
            f"{len(df.columns)} columns**",
            "",
            "| column | type | non-null | units | meaning |",
            "|---|---|---:|---|---|",
        ]
        for c in df.columns:
            units, meaning = COLUMNS.get(c, ("", ""))
            if not meaning:
                undocumented.add(c)
                meaning = "_(structural / self-describing)_"
            nn = f"{100 * df[c].notna().mean():.0f}%"
            lines.append(f"| `{c}` | {df[c].dtype} | {nn} | {units} | {meaning} |")
        lines += ["", "---", ""]

    if undocumented:
        lines += [
            "## Columns without a curated description",
            "",
            "Structural or self-describing columns (indices, counts, labels, and "
            "per-table bookkeeping). Listed for completeness so the audit is honest "
            "about what is and is not curated.",
            "",
            "```",
            ", ".join(sorted(undocumented)),
            "```",
            "",
        ]

    out = config.DATA_PROCESSED / "dictionary.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {out}  ({len(files)} tables, "
          f"{len(undocumented)} uncurated column names)")


if __name__ == "__main__":
    main()
