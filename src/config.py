"""Project-wide constants and paths.

Everything here is a *declaration*, not a finding. Season ranges are working
assumptions to be tested by the coverage report (ANALYSIS_PLAN.md section 5);
nothing downstream may treat them as verified until coverage confirms them.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

DATA_RAW = ROOT / "data" / "raw"
DATA_PROCESSED = ROOT / "data" / "processed"
FIGURES = ROOT / "figures"

JOLPICA_CACHE = DATA_RAW / "jolpica"
FASTF1_CACHE = DATA_RAW / "fastf1_cache"

for _p in (DATA_RAW, DATA_PROCESSED, FIGURES, JOLPICA_CACHE, FASTF1_CACHE):
    _p.mkdir(parents=True, exist_ok=True)

# --- Study window (working assumption; see ANALYSIS_PLAN.md section 5) ---------
# 2006 is the first knockout-qualifying season, the earliest with a format
# comparable to today. 2026 is in progress.
TIER_A_SEASON_MIN = 2006
TIER_A_SEASON_MAX = 2026

# Tier B floor is DELIBERATELY unset. It is an output of the coverage report,
# not an input. Do not put 2018 here.
TIER_B_SEASON_MIN: int | None = None
TIER_B_SEASON_MAX = 2026

# --- Regulation boundaries (ANALYSIS_PLAN.md section 2, DECISIONS.md 005) -----
# 2021 and 2022 are ONE boundary. Intent columns are sourced in the plan;
# Intent-C is what this analysis actually measures.
RESET_BOUNDARIES = {
    2009: {"label": "2009", "seasons": (2009,), "intent_r": True, "intent_c": False},
    2014: {"label": "2014", "seasons": (2014,), "intent_r": False, "intent_c": False},
    2017: {"label": "2017", "seasons": (2017,), "intent_r": False, "intent_c": False},
    2021: {"label": "2021-22", "seasons": (2021, 2022), "intent_r": True, "intent_c": True},
    2026: {"label": "2026", "seasons": (2026,), "intent_r": True, "intent_c": False},
}

# Every season touched by a reset — excluded from the placebo pool.
RESET_SEASONS = {s for b in RESET_BOUNDARIES.values() for s in b["seasons"]}

# Seasons with their own known discontinuities. Excluded from the placebo pool
# but NOT treated as resets. 2016 is Tier-A-specific (elimination qualifying).
FLAGGED_SEASONS = {
    2010: "refuelling ban",
    2019: "front wing simplification",
    2020: "COVID-affected calendar",
    2023: "floor edge raise",
}
FLAGGED_SEASONS_TIER_A_ONLY = {2016: "elimination qualifying experiment (opening rounds)"}

# --- Politeness ----------------------------------------------------------------
JOLPICA_BASE = "https://api.jolpi.ca/ergast/f1"
JOLPICA_MIN_INTERVAL_S = 0.5   # 2 req/s sustained, well under documented limits
JOLPICA_PAGE_LIMIT = 100
USER_AGENT = (
    "f1-regulation-competitiveness/0.1 "
    "(academic research; https://github.com/Dishank13/f1-regulation-competitiveness)"
)

RANDOM_SEED = 20260906
