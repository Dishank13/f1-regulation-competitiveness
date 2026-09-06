"""Finding E — the Q2 starting-tyre rule (coverage report section 6).

CLAIM UNDER TEST, not assumed: for part of the study period the top ten
qualifiers were required to start the race on the tyre they set their Q2 time
on. If so, Q2 was a strategically loaded session for exactly the teams that
reach Q3, and the rule was not in force for the whole period — making it a
TIME-VARYING contamination of a segment the Tier A metric depends on.

TEST. For each season 2018-2026 (the FastF1 qualifying window), compare the
compound used for each driver's fastest Q2 lap against the compound used for
their fastest Q3 lap. Under the rule, Q3-reaching drivers have an incentive to
set a Q2 time on a more durable compound; without it they use the softest
available in both.

The discriminating statistic is the share of Q3-reaching drivers whose Q2
compound differs from their Q3 compound. A regime change in that share across
seasons is evidence of the rule; a flat series is evidence against.

Runs AFTER the race acquisition, never alongside it: both draw on the same
500 calls/hour budget and parallelising around a hard rate limit was explicitly
ruled out.
"""

from __future__ import annotations

import time
import warnings

import fastf1
import pandas as pd

from src import config

try:
    from fastf1.req import RateLimitExceededError
except ImportError:  # pragma: no cover
    class RateLimitExceededError(Exception):  # type: ignore[no-redef]
        pass

fastf1.Cache.enable_cache(str(config.FASTF1_CACHE))
warnings.filterwarnings("ignore")

RATE_LIMIT_SLEEP_S = 900
RATE_LIMIT_MAX_WAITS = 16
SEASONS = range(2018, config.TIER_B_SEASON_MAX + 1)


def load_quali(season: int, rnd: int):
    for wait_n in range(RATE_LIMIT_MAX_WAITS + 1):
        try:
            s = fastf1.get_session(season, rnd, "Q")
            s.load(laps=True, telemetry=False, weather=False, messages=False)
            return s
        except RateLimitExceededError:
            if wait_n == RATE_LIMIT_MAX_WAITS:
                raise
            print(f"{season} r{rnd} rate limited; sleeping "
                  f"{RATE_LIMIT_SLEEP_S // 60} min", flush=True)
            time.sleep(RATE_LIMIT_SLEEP_S)
    raise RuntimeError("unreachable")


def segment_compounds(laps: pd.DataFrame) -> pd.DataFrame:
    """Fastest lap per driver per qualifying segment, with its compound.

    FastF1 marks segments via the session's three timed phases; we infer them
    from LapNumber ordering within the session using the built-in split when
    available, else fall back to time-based clustering.
    """
    rows = []
    if "Deleted" in laps.columns:
        laps = laps[laps["Deleted"] != True]  # noqa: E712
    laps = laps[laps["LapTime"].notna() & laps["Compound"].notna()]
    for drv, g in laps.groupby("Driver"):
        g = g.sort_values("LapStartTime")
        rows.append({"driver": drv, "n_laps": len(g)})
    return pd.DataFrame(rows)


def analyse_session(s) -> list[dict]:
    """Per-driver Q2 and Q3 fastest-lap compounds for one event."""
    laps = s.laps
    if laps is None or not len(laps):
        return []
    out = []
    try:
        q1, q2, q3 = s.laps.split_qualifying_sessions()
    except Exception:  # noqa: BLE001
        return []
    for seg_name, seg in (("Q2", q2), ("Q3", q3)):
        if seg is None or not len(seg):
            continue
        seg = seg[seg["LapTime"].notna() & seg["Compound"].notna()]
        if not len(seg):
            continue
        idx = seg.groupby("Driver")["LapTime"].idxmin()
        for _, r in seg.loc[idx].iterrows():
            out.append({"driver": r["Driver"], "team": r["Team"],
                        "segment": seg_name, "compound": r["Compound"]})
    return out


def main() -> None:
    rows = []
    for season in SEASONS:
        try:
            sched = fastf1.get_event_schedule(season, include_testing=False)
        except Exception as exc:  # noqa: BLE001
            print(f"{season}: schedule failed {exc}", flush=True)
            continue
        for _, ev in sched.iterrows():
            rnd = int(ev["RoundNumber"])
            try:
                s = load_quali(season, rnd)
                recs = analyse_session(s)
            except Exception as exc:  # noqa: BLE001
                print(f"{season} r{rnd} FAILED {type(exc).__name__}", flush=True)
                continue
            for r in recs:
                r.update({"season": season, "round": rnd,
                          "event": str(ev["EventName"])})
                rows.append(r)
            print(f"{season} r{rnd:<2} {str(ev['EventName'])[:30]:<30} "
                  f"records={len(recs)}", flush=True)

    df = pd.DataFrame(rows)
    if df.empty:
        print("no data")
        return
    df.to_parquet(config.DATA_PROCESSED / "finding_e_compounds.parquet",
                  index=False)

    wide = df.pivot_table(index=["season", "round", "driver"], columns="segment",
                          values="compound", aggfunc="first").dropna()
    wide["differs"] = wide["Q2"] != wide["Q3"]
    per_season = wide.groupby(level=0)["differs"].agg(["size", "mean"])
    per_season["pct_differ"] = (100 * per_season["mean"]).round(1)

    print("\n=== FINDING E: share of Q3-reaching drivers whose Q2 compound "
          "differs from Q3 ===")
    print(per_season[["size", "pct_differ"]].to_string())
    per_season.to_parquet(config.DATA_PROCESSED / "finding_e_result.parquet")


if __name__ == "__main__":
    main()
