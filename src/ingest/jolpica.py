"""Rate-limited, disk-cached client for the Jolpica API (Ergast successor).

Cache-before-request is a hard rule: a cached page is never re-fetched. The
cache lives under data/raw/ and is gitignored.
"""

from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from pathlib import Path

from src import config

_last_request_at = 0.0


def _throttle() -> None:
    global _last_request_at
    wait = config.JOLPICA_MIN_INTERVAL_S - (time.monotonic() - _last_request_at)
    if wait > 0:
        time.sleep(wait)
    _last_request_at = time.monotonic()


def _cache_path(path: str, offset: int) -> Path:
    slug = path.strip("/").replace("/", "_") or "root"
    return config.JOLPICA_CACHE / f"{slug}__off{offset}.json"


def _fetch(path: str, offset: int, retries: int = 5) -> dict:
    """Fetch one page, honouring the cache. Backs off on 429/5xx."""
    cached = _cache_path(path, offset)
    if cached.exists():
        return json.loads(cached.read_text(encoding="utf-8"))

    url = (
        f"{config.JOLPICA_BASE}/{path.strip('/')}/"
        f"?format=json&limit={config.JOLPICA_PAGE_LIMIT}&offset={offset}"
    )
    delay = 2.0
    for attempt in range(retries):
        _throttle()
        try:
            req = urllib.request.Request(url, headers={"User-Agent": config.USER_AGENT})
            with urllib.request.urlopen(req, timeout=60) as resp:
                payload = json.load(resp)
            cached.write_text(json.dumps(payload), encoding="utf-8")
            return payload
        except urllib.error.HTTPError as exc:
            if exc.code in (429, 500, 502, 503, 504) and attempt < retries - 1:
                time.sleep(delay)
                delay *= 2
                continue
            raise
        except (urllib.error.URLError, TimeoutError):
            if attempt < retries - 1:
                time.sleep(delay)
                delay *= 2
                continue
            raise
    raise RuntimeError(f"unreachable: {url}")


def get_all(path: str) -> list[dict]:
    """Page through an endpoint, returning every Race entry.

    Jolpica splits a season's results across pages *mid-race*, so races appearing
    in more than one page are merged by (season, round) rather than concatenated.
    """
    merged: dict[tuple[str, str], dict] = {}
    offset, total = 0, None

    while total is None or offset < total:
        page = _fetch(path, offset)["MRData"]
        total = int(page["total"])
        for race in page.get("RaceTable", {}).get("Races", []):
            key = (race["season"], race["round"])
            if key not in merged:
                merged[key] = {k: v for k, v in race.items()}
            else:
                for field in ("QualifyingResults", "Results", "Laps"):
                    if field in race:
                        merged[key].setdefault(field, []).extend(race[field])
        if not page.get("RaceTable", {}).get("Races") and total:
            break
        offset += config.JOLPICA_PAGE_LIMIT

    return list(merged.values())


def qualifying(season: int) -> list[dict]:
    return get_all(f"{season}/qualifying")


def races(season: int) -> list[dict]:
    return get_all(f"{season}/races")


def constructors(season: int) -> list[dict]:
    """Constructors entered in a season, from the dedicated endpoint."""
    merged: dict[str, dict] = {}
    offset, total = 0, None
    while total is None or offset < total:
        page = _fetch(f"{season}/constructors", offset)["MRData"]
        total = int(page["total"])
        for c in page.get("ConstructorTable", {}).get("Constructors", []):
            merged[c["constructorId"]] = c
        offset += config.JOLPICA_PAGE_LIMIT
    return list(merged.values())
