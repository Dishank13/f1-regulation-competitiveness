# Did F1's regulation resets actually close up the field?

Formula 1 rewrites its technical regulations every few years, and each time the
stated goal is closer racing. This project tests whether that happened, using
timing data rather than the two measures usually reached for. Championship points
lag actual car performance by up to a full season and are distorted by
reliability, crashes, and changes to the scoring system. Overtake counts are
inflated by DRS trains and pit-stop cycles, and they count position changes that
involved no racing at all. Neither measures what the regulations are supposed to
affect: how far apart the cars actually are. So the analytical core of this
project is designing a defensible competitiveness metric from lap and qualifying
times, then testing whether it moved at each regulation boundary. The metric
design is as much the deliverable as the answer.

## Status

**In progress. No results yet.**

Current phase: **Phase 0 — analysis plan under review.** No data has been
acquired and no analysis code has been written.

| Phase | State |
|---|---|
| 0 — Analysis plan (pre-registration) | Drafted, under review |
| 1 — Acquisition and coverage report | Not started |
| 2 — Cleaning and representative-lap filter | Not started |
| 3 — Pace model | Not started |
| 4 — Competitiveness metrics | Not started |
| 5 — Reset analysis | Not started |
| 6 — Red team and robustness battery | Not started |
| 7 — Memo and deliverables | Not started |

## Finding

<!-- PLACEHOLDER — to be filled from memo.md once Phase 5 and the Phase 6
     robustness battery are complete. Nothing goes here until then, including
     partial or preliminary results. -->

_Not yet available._ This section will state the finding in the first sentence,
carried over from `memo.md`, once the analysis has run and survived the
robustness checks in section 11 of the analysis plan. A claim that survives
fewer than 8 of the 12 robustness checks will be labelled "suggestive" rather
than "finding," in those words.

## Method

Lap-level timing data does not reach back far enough to cover the older
regulation resets, so the analysis runs as two independent tiers and compares
them.

**Tier A — long history, coarse metric.** Qualifying-derived field spread,
sourced from Jolpica. Each team is represented by its best qualifying lap at an
event, normalised to a percentage off the fastest team so that circuits of
different lap length are comparable. Lower resolution, wider coverage; brackets
several regulation resets. Qualifying is low fuel, fresh tyres, maximum attack
and minimal traffic, which makes it a clean read on car performance — this tier
is a serious candidate for the primary metric, not a fallback.

**Tier B — recent history, rich metric.** Fuel- and tyre-corrected race pace from
FastF1, 2018–2026 (floor verified empirically: 2014–2017 return no lap data at
all). A per-race regression strips out fuel load, tyre compound, and tyre age to
recover underlying car pace, which is then normalised the same way as Tier A.
Higher resolution, narrower coverage; brackets the two most recent resets.

> **Tier B is corroboration only. It cannot carry an independent conclusion.**
> Its placebo pool is two boundaries, and the 2021–22 boundary has just one
> unflagged pre-season (2018; 2019 and 2020 are both flagged discontinuities).
> Tier B can support or undercut a Tier A result. It cannot establish one on its
> own, and no claim in this repository rests on Tier B alone.

Where the tiers agree, confidence rises. Where they disagree, the disagreement is
reported as a finding rather than reconciled away.

Regulation boundaries are tested with segmented interrupted time-series models,
estimating both the level change at the boundary and the slope change after it.
Confidence intervals come from a cluster bootstrap over events. A placebo test
fits the same model at non-reset season boundaries: if real resets do not produce
larger shifts than arbitrary ones, that is the answer.

## Analysis plan

[`ANALYSIS_PLAN.md`](ANALYSIS_PLAN.md) contains the question, the hypotheses, the
metric formulas, the exclusion rules, the statistical tests, the confounds known
in advance, and — importantly — what result would prove the hypothesis wrong.

**It was committed before any analysis code existed.** That commit is tagged
[`pre-registration`](../../releases/tag/pre-registration) and the history before
it is never rewritten. The point is that the conclusions cannot have been
reverse-engineered from the results. If the plan changes after that tag, the
change is a new commit stating what changed and why, never an amendment.

## Reproduction

```bash
git clone https://github.com/Dishank13/f1-regulation-competitiveness.git
cd f1-regulation-competitiveness
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
make all
```

`make all` rebuilds every intermediate table from scratch. Raw API responses are
cached locally and are not committed; the cache is populated on first run and
reused afterwards. Processed tables are written to `data/processed/` as Parquet,
each accompanied by a data dictionary that is committed. Random seeds for all
bootstraps are fixed and recorded.

The pipeline does not exist yet. This section documents the intended entry point.

## Data sources

**[FastF1](https://github.com/theOehrly/Fast-F1)** — lap times, sector times,
tyre compounds, stint structure, pit stops, track status, weather, and telemetry
for recent seasons. Used for Tier B. FastF1 is an independent open-source project
and is not affiliated with Formula 1.

**[Jolpica-F1](https://github.com/jolpica/jolpica-f1)** (`api.jolpi.ca/ergast/f1/`)
— the community-maintained successor to the Ergast Developer API, which was
deprecated at the end of the 2024 season. Provides an Ergast-compatible interface
to race results, qualifying times, and standings across a much longer history
than FastF1's lap data. Used for Tier A. Requests are rate-limited and cached.

Thanks to the maintainers of both projects, and to Chris Newell for Ergast, which
underpins most public F1 analysis including this one.

This project is unofficial and unaffiliated with Formula 1. F1, FORMULA ONE, and
related marks are trademarks of Formula One Licensing BV.

## License

[MIT](LICENSE)
