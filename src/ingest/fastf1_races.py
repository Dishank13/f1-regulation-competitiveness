"""Phase 1 — full Tier B acquisition: every race session 2018-2026.

Resumable. FastF1's cache is enabled before the first request, so a re-run
re-reads from disk and never re-downloads. Sessions that fail are recorded with
their error rather than skipped silently — a session missing from the lap table
must be traceable to a logged reason.

Writes data/processed/laps_raw.parquet (gitignored) and an acquisition ledger.
No filtering happens here. This is acquisition only; Phase 2 owns exclusions.
"""

from __future__ import annotations

import time
import warnings

import fastf1
import pandas as pd

from src import config

try:
    from fastf1.req import RateLimitExceededError
except ImportError:  # pragma: no cover - defensive across fastf1 versions
    class RateLimitExceededError(Exception):  # type: ignore[no-redef]
        pass

try:
    from requests.exceptions import HTTPError
except ImportError:  # pragma: no cover
    class HTTPError(Exception):  # type: ignore[no-redef]
        pass


def _is_rate_limited(exc: BaseException) -> bool:
    """True for either rate limiter we can hit.

    FastF1 throttles its own live-timing API and raises RateLimitExceededError.
    But it ALSO makes unthrottled Ergast/Jolpica calls internally (to fill in
    first-lap times), and those return HTTP 429 once a full acquisition gets
    going. Found by running the pipeline from a genuinely fresh clone: the
    live-timing limiter was handled and the Ergast 429 was not, so sessions were
    being marked failed for a condition that just needed waiting out.
    """
    if isinstance(exc, RateLimitExceededError):
        return True
    if isinstance(exc, HTTPError):
        resp = getattr(exc, "response", None)
        return getattr(resp, "status_code", None) == 429
    return False

fastf1.Cache.enable_cache(str(config.FASTF1_CACHE))
warnings.filterwarnings("ignore")

# The live timing API allows 500 calls/hour and a session load costs several.
# A cached session costs none, so re-runs resume for free; we only ever wait
# for sessions not yet on disk.
RATE_LIMIT_SLEEP_S = 900
RATE_LIMIT_MAX_WAITS = 16

KEEP = [
    "Driver", "DriverNumber", "Team", "LapNumber", "LapTime", "Stint",
    "Compound", "TyreLife", "FreshTyre", "TrackStatus", "IsAccurate",
    "PitInTime", "PitOutTime", "Position", "Sector1Time", "Sector2Time",
    "Sector3Time", "LapStartTime",
]

SEASONS = range(2018, config.TIER_B_SEASON_MAX + 1)


def session_rainfall(session) -> bool | None:
    """Session-level wet flag. Phase 2 decides what to do with it."""
    try:
        w = session.weather_data
        if w is None or not len(w):
            return None
        return bool(w["Rainfall"].any())
    except Exception:  # noqa: BLE001
        return None


def main() -> None:
    frames: list[pd.DataFrame] = []
    ledger: list[dict] = []

    for season in SEASONS:
        try:
            sched = fastf1.get_event_schedule(season, include_testing=False)
        except Exception as exc:  # noqa: BLE001
            ledger.append({
                "season": season, "round": None, "event": "",
                "status": "schedule_failed", "n_laps": 0,
                "error": f"{type(exc).__name__}: {exc}"[:200],
            })
            print(f"{season}: SCHEDULE FAILED {exc}", flush=True)
            continue

        for _, ev in sched.iterrows():
            rnd = int(ev["RoundNumber"])
            name = str(ev["EventName"])
            fmt = str(ev.get("EventFormat", ""))
            rec = {"season": season, "round": rnd, "event": name,
                   "event_format": fmt, "status": "", "n_laps": 0, "error": ""}
            try:
                s = None
                for wait_n in range(RATE_LIMIT_MAX_WAITS + 1):
                    try:
                        s = fastf1.get_session(season, rnd, "R")
                        s.load(laps=True, telemetry=False, weather=True, messages=False)
                        break
                    except Exception as exc:  # noqa: BLE001
                        if not _is_rate_limited(exc):
                            raise
                        if wait_n == RATE_LIMIT_MAX_WAITS:
                            raise
                        which = ("live-timing"
                                 if isinstance(exc, RateLimitExceededError)
                                 else "Ergast/Jolpica 429")
                        print(
                            f"{season} r{rnd:<2} rate limited ({which}); sleeping "
                            f"{RATE_LIMIT_SLEEP_S // 60} min "
                            f"(wait {wait_n + 1}/{RATE_LIMIT_MAX_WAITS})",
                            flush=True,
                        )
                        time.sleep(RATE_LIMIT_SLEEP_S)
                laps = s.laps
                if laps is None or not len(laps):
                    rec["status"] = "no_laps"
                    print(f"{season} r{rnd:<2} {name[:34]:<34} NO LAPS", flush=True)
                else:
                    df = laps[[c for c in KEEP if c in laps.columns]].copy()
                    df["season"] = season
                    df["round"] = rnd
                    df["event"] = name
                    df["event_format"] = fmt
                    df["session_rainfall"] = session_rainfall(s)
                    frames.append(df)
                    rec["status"] = "ok"
                    rec["n_laps"] = len(df)
                    print(f"{season} r{rnd:<2} {name[:34]:<34} laps={len(df):>5} fmt={fmt}",
                          flush=True)
            except Exception as exc:  # noqa: BLE001
                rec["status"] = "failed"
                rec["error"] = f"{type(exc).__name__}: {exc}"[:200]
                print(f"{season} r{rnd:<2} {name[:34]:<34} FAILED {rec['error'][:70]}",
                      flush=True)
            ledger.append(rec)

    led = pd.DataFrame(ledger)
    led.to_parquet(config.DATA_PROCESSED / "acquisition_ledger.parquet", index=False)

    if frames:
        all_laps = pd.concat(frames, ignore_index=True)
        out = config.DATA_PROCESSED / "laps_raw.parquet"
        all_laps.to_parquet(out, index=False)
        print(f"\nwrote {out}  rows={len(all_laps):,}")

    print("\n=== acquisition summary (sessions per season by status) ===")
    print(led.groupby(["season", "status"]).size().to_string())
    print(f"\ntotal sessions attempted: {len(led)}")
    print(f"ok: {(led.status == 'ok').sum()}   "
          f"failed: {(led.status == 'failed').sum()}   "
          f"no_laps: {(led.status == 'no_laps').sum()}")


if __name__ == "__main__":
    main()
