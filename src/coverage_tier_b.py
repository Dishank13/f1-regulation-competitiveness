"""Phase 1 — Tier B (FastF1) coverage probe.

Establishes EMPIRICALLY which seasons carry the lap-level fields the pace model
in ANALYSIS_PLAN.md section 4.3 requires. The plan deliberately does not assume
a floor season; this script produces it.

Required per lap for the pace model:
    LapTime, Driver, Team, Compound, TyreLife, Stint, LapNumber, TrackStatus,
    PitInTime / PitOutTime   (to identify in/out laps)

Probes a sample of rounds per season rather than every race: enough to establish
whether a season is usable, cheap enough to run before committing to a full
acquisition.
"""

from __future__ import annotations

import warnings

import fastf1
import pandas as pd

from src import config

# Cache MUST be enabled before the first request.
fastf1.Cache.enable_cache(str(config.FASTF1_CACHE))
warnings.filterwarnings("ignore")

REQUIRED = [
    "LapTime", "Driver", "Team", "Compound", "TyreLife",
    "Stint", "LapNumber", "TrackStatus", "PitInTime", "PitOutTime",
]

PROBE_ROUNDS = (1, 8)
SEASONS = range(2014, config.TIER_B_SEASON_MAX + 1)


def probe(season: int, rnd: int) -> dict:
    row = {"season": season, "round": rnd, "loaded": False, "error": "",
           "n_laps": 0, "n_drivers": 0, "n_teams": 0}
    row.update({f"has_{c}": False for c in REQUIRED})
    row.update({f"pct_{c}": 0.0 for c in REQUIRED})
    try:
        s = fastf1.get_session(season, rnd, "R")
        s.load(laps=True, telemetry=False, weather=False, messages=False)
        laps = s.laps
        row["loaded"] = True
        row["n_laps"] = len(laps)
        if len(laps):
            row["n_drivers"] = laps["Driver"].nunique() if "Driver" in laps else 0
            row["n_teams"] = laps["Team"].nunique() if "Team" in laps else 0
            for c in REQUIRED:
                if c in laps.columns:
                    row[f"has_{c}"] = True
                    row[f"pct_{c}"] = round(100 * laps[c].notna().mean(), 1)
    except Exception as exc:  # noqa: BLE001 - we want the message, whatever it is
        row["error"] = f"{type(exc).__name__}: {exc}"[:200]
    return row


def main() -> None:
    rows = []
    for season in SEASONS:
        for rnd in PROBE_ROUNDS:
            r = probe(season, rnd)
            rows.append(r)
            status = "OK " if r["loaded"] and r["n_laps"] else "FAIL"
            print(
                f"{status} {season} r{rnd:<2} laps={r['n_laps']:>5} "
                f"drv={r['n_drivers']:>2} teams={r['n_teams']:>2} "
                f"LapTime={r['pct_LapTime']:>5}% Compound={r['pct_Compound']:>5}% "
                f"TyreLife={r['pct_TyreLife']:>5}% TrackStatus={r['pct_TrackStatus']:>5}% "
                f"{r['error']}",
                flush=True,
            )
    df = pd.DataFrame(rows)
    out = config.DATA_PROCESSED / "coverage_tier_b.parquet"
    df.to_parquet(out, index=False)
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
