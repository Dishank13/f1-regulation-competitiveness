"""Diagnostic D1 — era-dependent attack bias (ANALYSIS_PLAN.md section 4.1.2).

The §4.1.1 rule measures front-running teams on a Q1/Q2 lap in 2006-09 and can
measure them on a full-attack Q3 lap from 2010. Because front-runners do not
fully attack in Q1/Q2, that is an era-dependent bias concentrated at the ranks
M4 and M5 measure.

Equal median Q1->Q2 offsets across eras do NOT establish equal composition of
those offsets. The offset is a sum of track evolution and change in attack
level, and two eras can share a median while mixing those components
differently. D1 tests composition directly.

D1a  Offset by competitive stratum. Track evolution improves the track for
     everyone equally; sandbagging does not. If E(Q1->Q2) is larger for
     front-runners than for backmarkers, the excess is attack-level change, not
     evolution. The quantity of interest is whether that excess SHIFTS across
     the 2010 line.
D1b  Segment-source composition by field position.
D1c  Front-of-field metrics tested for a step at 2010, with whole-field metrics
     as controls.

Results are reported regardless of what they show (plan 4.1.2).
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from src import config
from src.clean.tier_a import MIN_MULTI_SEGMENT_DRIVERS, eligible_segments
from src.coverage_tier_a import parse_time
from src.ingest import jolpica

RNG = np.random.default_rng(config.RANDOM_SEED)


def load_cells() -> pd.DataFrame:
    rows = []
    for season in range(config.TIER_A_SEASON_MIN, config.TIER_A_SEASON_MAX + 1):
        for race in jolpica.qualifying(season):
            rnd = int(race["round"])
            for r in race.get("QualifyingResults", []):
                rec = {"season": season, "round": rnd,
                       "driver": r["Driver"]["driverId"],
                       "constructor": r["Constructor"]["constructorId"],
                       "position": int(r["position"])}
                for seg in ("Q1", "Q2", "Q3"):
                    rec[seg] = parse_time(r.get(seg))
                rows.append(rec)
    return pd.DataFrame(rows)


def d1a(cells: pd.DataFrame) -> pd.DataFrame:
    """E(Q1->Q2) by competitive stratum, per event, then summarised by era.

    Stratum is defined by whether the driver reached Q3 — an in-session,
    era-invariant definition that does not depend on the metric being tested.
    """
    out = []
    for (season, rnd), g in cells.groupby(["season", "round"]):
        g = g[g.Q1.notna() & g.Q2.notna()].copy()
        if len(g) < MIN_MULTI_SEGMENT_DRIVERS * 2:
            continue
        g["gain"] = g.Q2 - g.Q1
        front = g[g.Q3.notna()]["gain"]
        back = g[g.Q3.isna()]["gain"]
        if len(front) < 3 or len(back) < 3:
            continue
        out.append({
            "season": season, "round": rnd,
            "E_front": front.median(), "E_back": back.median(),
            "delta_strat": front.median() - back.median(),
            "n_front": len(front), "n_back": len(back),
        })
    return pd.DataFrame(out)


def boot_ci(x: np.ndarray, n: int = 10000) -> tuple[float, float]:
    if len(x) == 0:
        return (np.nan, np.nan)
    idx = RNG.integers(0, len(x), size=(n, len(x)))
    meds = np.median(x[idx], axis=1)
    return (float(np.percentile(meds, 2.5)), float(np.percentile(meds, 97.5)))


def main() -> None:
    cells = load_cells()
    a = d1a(cells)
    a["era"] = np.where(a.season <= 2009, "2006-09", "2010+")

    print("=== D1a — Q1->Q2 offset by competitive stratum ===")
    print("E_front / E_back are within-driver medians (negative = faster in Q2).")
    print("delta_strat = E_front - E_back. Near zero => offset is track evolution.")
    print("Negative => front-runners gain MORE than backmarkers, i.e. sandbagging.\n")

    summ = a.groupby("era").agg(
        events=("delta_strat", "size"),
        E_front=("E_front", "median"),
        E_back=("E_back", "median"),
        delta_strat=("delta_strat", "median"),
    ).round(4)
    print(summ.to_string())

    early = a[a.era == "2006-09"]["delta_strat"].to_numpy()
    late = a[a.era == "2010+"]["delta_strat"].to_numpy()
    lo_e, hi_e = boot_ci(early)
    lo_l, hi_l = boot_ci(late)
    print(f"\n  2006-09 delta_strat median {np.median(early):+.4f} s "
          f"[95% CI {lo_e:+.4f}, {hi_e:+.4f}]  (n={len(early)} events)")
    print(f"  2010+   delta_strat median {np.median(late):+.4f} s "
          f"[95% CI {lo_l:+.4f}, {hi_l:+.4f}]  (n={len(late)} events)")

    # Difference-in-medians across the 2010 line, bootstrapped.
    n = 10000
    de = np.median(early[RNG.integers(0, len(early), size=(n, len(early)))], axis=1)
    dl = np.median(late[RNG.integers(0, len(late), size=(n, len(late)))], axis=1)
    diff = de - dl
    lo, hi = np.percentile(diff, [2.5, 97.5])
    print(f"\n  SHIFT across the 2010 line: {np.median(early) - np.median(late):+.4f} s "
          f"[95% CI {lo:+.4f}, {hi:+.4f}]")
    verdict = ("COMPOSITION DIFFERS across the 2010 line — confound 15 is live"
               if (lo > 0 or hi < 0) else
               "no detectable composition shift at this resolution")
    print(f"  -> {verdict}")

    print("\n=== D1b — representative-time source segment by era ===")
    teams = pd.read_parquet(config.DATA_PROCESSED / "tier_a_team_event.parquet")
    teams["era"] = np.where(teams.season <= 2009, "2006-09", "2010+")
    teams["front_third"] = teams.groupby(["season", "round"])["delta"].rank(
        pct=True) <= (1 / 3)
    comp = (teams.groupby(["era", "front_third"])["source_segment"]
            .value_counts(normalize=True).mul(100).round(1)
            .unstack(fill_value=0))
    print(comp.to_string())

    a.to_parquet(config.DATA_PROCESSED / "d1a_stratum_offsets.parquet", index=False)
    print(f"\nwrote {config.DATA_PROCESSED / 'd1a_stratum_offsets.parquet'}")


if __name__ == "__main__":
    main()
