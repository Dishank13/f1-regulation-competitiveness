"""Uniform wet-qualifying flag for Tier A, 2006-2026 (confound 17).

WHY THIS EXISTS. Plan section 6.1 requires wet sessions be flagged. FastF1
weather begins in 2018. Applying section 6.1 as written would give a filter that
is strict from 2018 and absent before it — a TIME-VARYING EXCLUSION RULE inside
a study built to detect time-varying changes. That is the same failure class as
Finding B (race-fuel qualifying) and D1b (front-of-field segment sourcing),
except self-inflicted. Both eras must be treated identically.

SOURCE. Circuit latitude/longitude from Jolpica, qualifying date from Jolpica,
precipitation from the Open-Meteo historical reanalysis archive (free, keyless,
full window, hourly by coordinate). Derived entirely outside the timing data,
so it is non-circular — a spread-based proxy would launder the outcome into the
exclusion rule and is rejected.

TEMPORAL RESOLUTION — stated plainly, because it is the weak point.
    Qualifying DATE:  available for 100% of events in all 21 seasons.
    Qualifying TIME:  available only from 2022 (0% for 2006-2021).

A session-window flag is therefore impossible before 2022. Building one would
recreate the exact 2018-style strictness cliff this module exists to avoid, just
moved to 2022. The flag is consequently WHOLE-DAY precipitation at the venue on
the qualifying date, applied identically to every season.

REJECTED ALTERNATIVE: a fixed local-time afternoon window. It is uniform across
eras in its *rule* but not in its *accuracy* — night qualifying sessions
(Singapore from 2008, Bahrain from 2014, Las Vegas from 2023) grow as a share of
the calendar over time, so a fixed afternoon window would drift in accuracy
across exactly the study window. That reintroduces the failure class through the
calendar instead of the data source. Whole-day is coarser and genuinely uniform
in both dimensions.

The cost of whole-day resolution is over-flagging: rain overnight with a dry
session reads as wet. Validation against FastF1 2018+ quantifies that cost
rather than assuming it away.
"""

from __future__ import annotations

import datetime as _dt
import json
import time
import urllib.error
import urllib.request
from pathlib import Path

import pandas as pd

from src import config
from src.ingest import jolpica

ARCHIVE = "https://archive-api.open-meteo.com/v1/archive"


class PermanentWeatherError(RuntimeError):
    """A request that will never succeed on retry (bad/out-of-range date)."""


CACHE = config.DATA_RAW / "openmeteo"
CACHE.mkdir(parents=True, exist_ok=True)
MIN_INTERVAL_S = 0.2
TODAY = _dt.date.today().isoformat()

_last = 0.0


def _fetch(lat: float, lon: float, date: str) -> dict:
    global _last
    key = f"{lat:.4f}_{lon:.4f}_{date}.json"
    path: Path = CACHE / key
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))

    url = (f"{ARCHIVE}?latitude={lat}&longitude={lon}"
           f"&start_date={date}&end_date={date}"
           "&hourly=precipitation&timezone=auto")
    delay = 2.0
    for attempt in range(5):
        wait = MIN_INTERVAL_S - (time.monotonic() - _last)
        if wait > 0:
            time.sleep(wait)
        _last = time.monotonic()
        try:
            req = urllib.request.Request(
                url, headers={"User-Agent": config.USER_AGENT})
            with urllib.request.urlopen(req, timeout=60) as resp:
                payload = json.load(resp)
            path.write_text(json.dumps(payload), encoding="utf-8")
            return payload
        except urllib.error.HTTPError as exc:
            # 400 is permanent (e.g. a date outside the archive's range).
            # Retrying it five times is pointless; surface the reason instead.
            if exc.code == 400:
                try:
                    detail = json.load(exc).get("reason", "")
                except Exception:  # noqa: BLE001
                    detail = ""
                raise PermanentWeatherError(f"400: {detail}") from exc
            if attempt == 4:
                raise
            time.sleep(delay)
            delay *= 2
        except (urllib.error.URLError, TimeoutError):
            if attempt == 4:
                raise
            time.sleep(delay)
            delay *= 2
    raise RuntimeError("unreachable")


def build() -> pd.DataFrame:
    """One row per event: venue, qualifying date, precipitation summary."""
    rows: list[dict] = []
    for season in range(config.TIER_A_SEASON_MIN, config.TIER_A_SEASON_MAX + 1):
        for race in jolpica.races(season):
            q = race.get("Qualifying", {})
            qdate = q.get("date")
            loc = race.get("Circuit", {}).get("Location", {})
            lat, lon = loc.get("lat"), loc.get("long")
            rec = {
                "season": season, "round": int(race["round"]),
                "event": race.get("raceName", ""),
                "circuit": race.get("Circuit", {}).get("circuitId", ""),
                "locality": loc.get("locality", ""),
                "country": loc.get("country", ""),
                "quali_date": qdate,
                "quali_time_available": bool(q.get("time")),
                "lat": float(lat) if lat else None,
                "lon": float(lon) if lon else None,
            }
            rec["weather_status"] = "no_coords_or_date"
            if qdate and lat and lon:
                if qdate > TODAY:
                    # Scheduled but not yet run. Not a failure; not a session.
                    rec["weather_status"] = "future_session"
                else:
                    try:
                        j = _fetch(float(lat), float(lon), qdate)
                        p = [x for x in j["hourly"]["precipitation"]
                             if x is not None]
                        rec.update({
                            "tz": j.get("timezone"),
                            "precip_daily_mm": round(sum(p), 3),
                            "precip_max_hourly_mm": round(max(p), 3) if p else None,
                            "wet_hours_gt_0p1mm": sum(1 for x in p if x > 0.1),
                            "n_hours": len(p),
                        })
                        rec["weather_status"] = "ok" if p else "empty_series"
                    except PermanentWeatherError as exc:
                        rec["weather_status"] = f"unavailable ({exc})"
            rows.append(rec)
    return pd.DataFrame(rows)


def main() -> None:
    df = build()
    out = config.DATA_PROCESSED / "weather_quali.parquet"
    df.to_parquet(out, index=False)

    print(f"events: {len(df)}   with precipitation data: {df.precip_daily_mm.notna().sum()}")
    print("\nquali TIME availability by era (this is why the flag is whole-day):")
    print(df.groupby(df.season >= 2022)["quali_time_available"]
          .agg(["size", "sum"]).rename(index={False: "2006-2021", True: "2022-2026"})
          .to_string())

    print("\nprecipitation distribution (mm, daily total at venue on quali date):")
    print(df.precip_daily_mm.describe(
        percentiles=[.5, .75, .9, .95, .99]).round(3).to_string())

    print("\ncandidate flag counts at several thresholds:")
    for thr in (0.5, 1.0, 2.0, 5.0):
        n = int((df.precip_daily_mm >= thr).sum())
        print(f"  daily_total >= {thr:>4} mm -> {n:>3} events "
              f"({100*n/len(df):.1f}%)")
    for thr in (0.5, 1.0, 2.0):
        n = int((df.precip_max_hourly_mm >= thr).sum())
        print(f"  max_hourly  >= {thr:>4} mm -> {n:>3} events "
              f"({100*n/len(df):.1f}%)")
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
