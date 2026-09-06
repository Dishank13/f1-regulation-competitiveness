"""Session format versioning (ANALYSIS_PLAN.md section 3.2, Decision D).

Decision D requires a format-VERSION indicator, not a binary sprint flag,
derived empirically from observed session structure rather than hardcoded.

Two independent sources are cross-checked:
  * Jolpica `/{season}/sprint` — which rounds held a sprint race. Available for
    every season in the Tier A window; empty before 2021.
  * FastF1 `get_event_schedule(...).EventFormat` — the format label. Available
    2018+, which covers every sprint season.

Observed EventFormat values, from the data:
    2018-2020  conventional
    2021-2022  conventional | sprint
    2023       conventional | sprint_shootout
    2024-2026  conventional | sprint_qualifying

Four versions, matching the plan's provisional expectation. The provisional
expectation is not what makes it true; the schedule data is.

IMPORTANT, established empirically: Jolpica's qualifying endpoint returns
exactly ONE session per round in every season 2006-2026 — no round yields two
qualifying sessions. The endpoint returns the Grand Prix qualifying (the session
that sets the race grid), not the sprint shootout; sprint results live on the
separate `/sprint` endpoint. So sprint weekends do not duplicate or displace
rows in the Tier A table. The format indicator is attached as an event-level
column, and it changes no row counts.
"""

from __future__ import annotations

import warnings

import fastf1
import pandas as pd

from src import config
from src.ingest import jolpica

fastf1.Cache.enable_cache(str(config.FASTF1_CACHE))
warnings.filterwarnings("ignore")

CONVENTIONAL = "conventional"


def sprint_rounds(season: int) -> set[int]:
    """Rounds holding a sprint race, from Jolpica. Empty before 2021."""
    try:
        return {int(r["round"]) for r in jolpica.get_all(f"{season}/sprint")}
    except Exception:  # noqa: BLE001
        return set()


def build_format_table() -> pd.DataFrame:
    """One row per (season, round) with its format version and source."""
    rows: list[dict] = []
    for season in range(config.TIER_A_SEASON_MIN, config.TIER_A_SEASON_MAX + 1):
        sprints = sprint_rounds(season)
        ff1: dict[int, str] = {}
        if season >= 2018:
            try:
                sch = fastf1.get_event_schedule(season, include_testing=False)
                ff1 = {int(r.RoundNumber): str(r.EventFormat) for r in sch.itertuples()}
            except Exception:  # noqa: BLE001
                ff1 = {}

        for race in jolpica.qualifying(season):
            rnd = int(race["round"])
            has_sprint = rnd in sprints
            fmt = ff1.get(rnd)
            if fmt is None:
                # Pre-2018: no FastF1 schedule. Sprint did not exist before 2021,
                # and the /sprint endpoint confirms it empirically.
                fmt = CONVENTIONAL if not has_sprint else "sprint_unlabelled"
                source = "jolpica_sprint_endpoint"
            else:
                source = "fastf1_event_format"
            rows.append({
                "season": season, "round": rnd,
                "event": race.get("raceName", ""),
                "format_version": fmt,
                "has_sprint_race": has_sprint,
                "format_source": source,
                # Cross-check: do the two sources agree on sprint presence?
                "sources_agree": (has_sprint == (fmt != CONVENTIONAL))
                if source == "fastf1_event_format" else None,
            })
    return pd.DataFrame(rows)


def main() -> None:
    df = build_format_table()
    out = config.DATA_PROCESSED / "session_formats.parquet"
    df.to_parquet(out, index=False)

    print("=== format version by season ===")
    print(pd.crosstab(df.season, df.format_version).to_string())
    dis = df[df.sources_agree == False]  # noqa: E712
    print(f"\ncross-source disagreements (2018+): {len(dis)}")
    if len(dis):
        print(dis[["season", "round", "event", "format_version",
                   "has_sprint_race"]].to_string(index=False))
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
