# One-command rebuild (ANALYSIS_PLAN.md section 13).
#
# Every target is idempotent and cache-first. Acquisition is rate-limited by the
# upstream API (500 calls/hour) and resumes from cache, so a re-run costs
# nothing for sessions already on disk.
#
#   make all        full pipeline, acquisition through deliverables
#   make analysis   everything downstream of acquisition (no network)
#   make findinge   the Q2 starting-tyre test (slow, rate-limited, optional)

PY := .venv/Scripts/python.exe
ifeq ($(wildcard $(PY)),)
PY := python
endif

.PHONY: all analysis acquire coverage clean_tables model metrics tests figures \
        diagnostics findinge deliverables

all: acquire analysis

# --- Phase 1: acquisition and coverage -------------------------------------
coverage:
	$(PY) -m src.coverage_tier_a
	$(PY) -m src.coverage_tier_b

acquire: coverage
	$(PY) -m src.ingest.weather        # retained, unused (Amendment 3)
	$(PY) -m src.ingest.fastf1_races

# --- Phases 2-6, no network ------------------------------------------------
analysis: clean_tables model metrics tests diagnostics figures

clean_tables:
	$(PY) -m src.clean.session_format
	$(PY) -m src.clean.tier_a
	$(PY) -m src.clean.tier_b

model: clean_tables
	$(PY) -m src.pace_model

metrics: model
	$(PY) -m src.metrics a
	$(PY) -m src.metrics b

tests: metrics
	$(PY) -m src.placebo a
	$(PY) -m src.phase5
	$(PY) -m src.robustness
	$(PY) -m src.r16_stratified
	$(PY) -m src.trend_decomposition

diagnostics: metrics
	$(PY) -m src.diagnostics_d1
	$(PY) -m src.decision_a_evidence
	$(PY) -m src.traffic_bias
	$(PY) -m src.gate3_investigation

figures: model metrics
	$(PY) -m src.figures
	$(PY) -m src.figures decision_b

# Optional: rate-limited, resumable, not required for the headline result.
findinge:
	$(PY) -m src.finding_e

# Ledger integrity — fails loudly on a duplicated or non-contiguous entry.
verify:
	$(PY) -m src.ledger verify
