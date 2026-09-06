"""Phase 1 — Tier A coverage report.

Answers, empirically and per season:
  * how many rounds have qualifying data at all
  * how many constructors and drivers actually appear
  * which qualifying segments are populated (verifies the knockout-format floor)
  * whether ANY season exposes a deleted / invalidated lap field
    (ANALYSIS_PLAN.md section 6.3 requires this probe)
  * whether Q3 runs slower than Q2, which would indicate race-fuel qualifying
    rather than low-fuel maximum attack

Nothing here filters or models. It reports what exists.
"""

from __future__ import annotations

import json
import re
from statistics import median

import pandas as pd

from src import config
from src.ingest import jolpica

TIME_RE = re.compile(r"^(?:(\d+):)?(\d+)\.(\d+)$")

# Fields we know about. Anything outside this set is surfaced loudly, because an
# unknown field might be the deleted-lap marker section 6.3 asks about.
KNOWN_RESULT_FIELDS = {
    "number", "position", "Driver", "Constructor", "Q1", "Q2", "Q3",
}


def parse_time(text: str | None) -> float | None:
    """'1:31.295' -> 91.295. Returns None for absent or unparseable values."""
    if not text or not isinstance(text, str):
        return None
    m = TIME_RE.match(text.strip())
    if not m:
        return None
    minutes, seconds, frac = m.groups()
    return int(minutes or 0) * 60 + int(seconds) + float(f"0.{frac}")


def scan_season(season: int) -> dict:
    quali = jolpica.qualifying(season)
    cons = jolpica.constructors(season)

    rounds_total = len(quali)
    unknown_fields: set[str] = set()
    constructor_ids: set[str] = set()
    driver_ids: set[str] = set()

    seg_set = {"Q1": 0, "Q2": 0, "Q3": 0}
    rows_total = 0
    rounds_with_q3 = 0
    q3_minus_q2: list[float] = []
    q2_minus_q1: list[float] = []

    for race in quali:
        results = race.get("QualifyingResults", [])
        if not results:
            continue
        has_q3 = False
        for r in results:
            rows_total += 1
            unknown_fields |= set(r.keys()) - KNOWN_RESULT_FIELDS
            constructor_ids.add(r["Constructor"]["constructorId"])
            driver_ids.add(r["Driver"]["driverId"])
            t = {s: parse_time(r.get(s)) for s in ("Q1", "Q2", "Q3")}
            for s in ("Q1", "Q2", "Q3"):
                if t[s] is not None:
                    seg_set[s] += 1
            if t["Q3"] is not None:
                has_q3 = True
            # Within-driver segment deltas: car and driver quality cancel.
            if t["Q2"] is not None and t["Q1"] is not None:
                q2_minus_q1.append(t["Q2"] - t["Q1"])
            if t["Q3"] is not None and t["Q2"] is not None:
                q3_minus_q2.append(t["Q3"] - t["Q2"])
        if has_q3:
            rounds_with_q3 += 1

    return {
        "season": season,
        "rounds_with_quali": rounds_total,
        "n_constructors_endpoint": len(cons),
        "n_constructors_in_quali": len(constructor_ids),
        "n_drivers": len(driver_ids),
        "quali_rows": rows_total,
        "rounds_with_q3": rounds_with_q3,
        "pct_rows_with_Q1": 100 * seg_set["Q1"] / rows_total if rows_total else 0.0,
        "pct_rows_with_Q2": 100 * seg_set["Q2"] / rows_total if rows_total else 0.0,
        "pct_rows_with_Q3": 100 * seg_set["Q3"] / rows_total if rows_total else 0.0,
        "median_Q2_minus_Q1": median(q2_minus_q1) if q2_minus_q1 else None,
        "median_Q3_minus_Q2": median(q3_minus_q2) if q3_minus_q2 else None,
        "n_pairs_Q3_Q2": len(q3_minus_q2),
        "unknown_fields": sorted(unknown_fields),
    }


def main() -> None:
    seasons = range(config.TIER_A_SEASON_MIN, config.TIER_A_SEASON_MAX + 1)
    rows = []
    for s in seasons:
        row = scan_season(s)
        rows.append(row)
        print(
            f"{s}  rounds={row['rounds_with_quali']:>2}  "
            f"teams={row['n_constructors_in_quali']:>2}  "
            f"drivers={row['n_drivers']:>2}  "
            f"Q3rows={row['pct_rows_with_Q3']:5.1f}%  "
            f"med(Q3-Q2)={row['median_Q3_minus_Q2'] if row['median_Q3_minus_Q2'] is None else round(row['median_Q3_minus_Q2'], 3)}",
            flush=True,
        )

    df = pd.DataFrame(rows)
    out = config.DATA_PROCESSED / "coverage_tier_a.parquet"
    df.drop(columns=["unknown_fields"]).to_parquet(out, index=False)

    unknown = sorted({f for r in rows for f in r["unknown_fields"]})
    (config.DATA_PROCESSED / "coverage_tier_a_unknown_fields.json").write_text(
        json.dumps(unknown, indent=2), encoding="utf-8"
    )
    print(f"\nwrote {out}")
    print(f"unknown qualifying-result fields across all seasons: {unknown or 'NONE'}")


if __name__ == "__main__":
    main()
