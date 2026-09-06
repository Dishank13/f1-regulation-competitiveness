# Phase 1 — Coverage report

Generated from data, not written by hand. Regenerate with:

```
python -m src.coverage_tier_a
python -m src.coverage_tier_b
```

Everything below is empirical. Where the analysis plan recorded a working
assumption, this report either confirms it or replaces it.

---

## 1. Tier A — Jolpica qualifying, 2006–2026

All 21 seasons return per-segment qualifying times. No season is missing.

| Season | Rounds | Teams | Drivers | median(Q2−Q1) | median(Q3−Q2) |
|---:|---:|---:|---:|---:|---:|
| 2006 | 18 | 12 | 27 | −0.712 | **+0.452** |
| 2007 | 17 | 11 | 26 | −0.492 | **+0.814** |
| 2008 | 18 | 11 | 22 | −0.328 | **+1.695** |
| 2009 | 17 | 10 | 25 | −0.365 | **+1.487** |
| 2010 | 19 | 12 | 27 | −0.536 | −0.223 |
| 2011 | 19 | 12 | 28 | −0.610 | −0.374 |
| 2012 | 20 | 12 | 25 | −0.523 | −0.186 |
| 2013 | 19 | 11 | 23 | −0.569 | −0.290 |
| 2014 | 19 | 11 | 24 | −0.522 | −0.190 |
| 2015 | 19 | 10 | 22 | −0.427 | −0.186 |
| 2016 | 21 | 11 | 24 | −0.410 | −0.254 |
| 2017 | 20 | 10 | 25 | −0.583 | −0.266 |
| 2018 | 21 | 10 | 20 | −0.370 | −0.298 |
| 2019 | 21 | 10 | 20 | −0.377 | −0.310 |
| 2020 | 17 | 10 | 23 | −0.411 | −0.149 |
| 2021 | 22 | 10 | 21 | −0.359 | −0.196 |
| 2022 | 22 | 10 | 22 | −0.401 | −0.267 |
| 2023 | 22 | 10 | 22 | −0.509 | −0.321 |
| 2024 | 24 | 10 | 24 | −0.439 | −0.178 |
| 2025 | 24 | 10 | 21 | −0.329 | −0.169 |
| 2026 | 13 | 11 | 23 | −0.498 | −0.345 |

Negative = faster than the previous segment. Deltas are within-driver medians, so
car and driver quality cancel.

---

## 2. Finding A — no deleted-lap field exists (plan §6.3 resolved)

Plan §6.3 required an explicit probe rather than an assumption. Every qualifying
result across all 21 seasons carries exactly these fields:

```
number, position, Driver, Constructor, Q1, Q2, Q3
```

Unknown fields across all seasons: **NONE**.

There is no deleted-lap, invalidated-lap, or track-limits marker. **Per plan
§6.3 the deleted-lap filter is declared unimplementable and removed from the
plan**, rather than left as a rule that silently never fires.

**Resulting bias, stated:** a lap deleted for track limits that nonetheless
appears in the published times slightly flatters that team at that event. The
magnitude cannot be bounded from this source. The effect is plausibly larger in
the later seasons, when automated track-limits enforcement became more
aggressive — which means it is a *time-varying* bias, and it is therefore added
to the confound list rather than dismissed as noise.

---

## 3. Finding B — qualifying was run on race fuel in 2006–2009

This is the most consequential finding in Phase 1 and it was not anticipated in
the plan.

`median(Q3 − Q2)` is **positive in every season 2006–2009** (+0.45 to +1.70 s)
and **negative in every season 2010–2026** (−0.15 to −0.37 s). The eras do not
overlap at all. The sign flips exactly at 2010, the season the refuelling ban
took effect.

Drivers were *slower* in Q3 than in Q2 for four consecutive seasons. Under
low-fuel maximum attack on an improving track that is not possible. The
explanation is the race-fuel qualifying format of that era: Q3 was run with the
fuel load the car would start the race on.

**Q1→Q2 is unaffected.** `median(Q2 − Q1)` is statistically indistinguishable
across the eras — 2006–09 range −0.71 to −0.33 (median −0.428), 2010+ range
−0.61 to −0.33 (median −0.439). Q1 and Q2 were low-fuel sessions throughout.

### Why this actively breaks the current primary metric

Plan §4.1 estimates `offset(Q3) = E(Q1→Q2) + E(Q2→Q3)` and interprets it as
track evolution. In 2006–2009 the second term is **fuel load, not track
evolution**. Because the offset is positive there, the adjustment *subtracts*
up to 1.7 s from Q3 laps — crediting a heavy-fuel lap as though the track were
slow, and making teams that chose a heavy first stint look artificially fast.

This is not added noise. It is a systematic bias in the direction of whichever
teams ran long first stints, and fuel strategy correlates with car pace.

Diagnostic — share of team representative times supplied by each segment under
the evolution-adjusted rule:

| Era | from Q1 | from Q2 | from Q3 |
|---|---:|---:|---:|
| 2006–2009 | 48–55% | 21–27% | **24–26%** (contaminated) |
| 2010–2026 | 45–64% | 17–27% | 19–31% |

Roughly a quarter of all 2006–2009 team observations are affected.

**This requires an analyst decision — see section 7.**

---

## 4. Finding C — Tier B floor is 2018, verified

Probe of FastF1 race sessions, two rounds per season:

| Seasons | Result |
|---|---|
| 2014–2017 | **No lap data.** `DataNotLoadedError` on every probe, both rounds, all four seasons. |
| 2018–2026 | Full lap data, both rounds, every season. |

Field completeness for 2018–2026, across all probed sessions:

| Field | Completeness |
|---|---|
| `LapTime` | 92.6 – 99.9% |
| `Compound` | 100% in every session |
| `TyreLife` | 97.3 – 100% |
| `TrackStatus` | 100% in every session |
| `Stint`, `LapNumber`, `PitInTime`, `PitOutTime` | present in every session |

Every field the pace model in plan §4.3 requires is present and essentially
complete from 2018. **The commonly cited 2018 floor is confirmed rather than
assumed.** Tier B scope is 2018–2026, nine seasons.

---

## 5. Finding D — constructor counts per season (Decision E, stated as fact)

Plan §10 confound 4 previously speculated about grid expansion. It no longer
needs to. Counts below are from the data; the Jolpica constructors endpoint and
the qualifying results agree for every season, with no disagreements.

| Teams | Seasons |
|---:|---|
| 12 | 2006, 2010, 2011, 2012 |
| 11 | 2007, 2008, 2013, 2014, 2016, **2026** |
| 10 | 2009, 2015, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025 |

**2026 has 11 constructors, up from 10 in 2025** — the first grid expansion in
the Tier B window, arriving in the same season as the 2026 reset. This is
precisely the mechanism confound 4 describes: an eleventh team widens measured
field spread for reasons unrelated to the regulations. M2 (IQR) and R4
(constant-constructor subset) are the mitigations, and both are now known to be
load-bearing rather than precautionary.

The grid also contracted from 12 to 10 across 2012→2015 and from 11 to 10 across
2016→2017 — the latter inside the 2017 boundary's window.

2026 is partial: **13 of a planned full calendar**, so all 2026 figures are
provisional per Decision E.

---

## 6. Finding E — a confound not in the plan, flagged for verification

During Phase 1 a further time-varying qualifying contamination was identified
that plan §10 does not list: for part of the study period, the top ten drivers
were required to **start the race on the tyre they set their Q2 time on**. That
makes Q2 a strategically loaded session for exactly the teams that reach Q3, and
the rule was not in force for the whole period.

This is **not yet verified** and is not treated as established. Proposed test,
Phase 2: for 2018–2026, where FastF1 exposes qualifying lap compounds, check
whether top-ten teams set Q2 times on a slower compound in the seasons the rule
was in force than in the seasons it was not. If confirmed, it is added to the
confound list and to the robustness battery by amendment commit.

It matters directly to the section 7 decision: option 2 below leans on Q2, and
Q2 may carry its own time-varying contamination.

---

## 7. Decision required — Tier A qualifying scope and segment rule

Finding B invalidates the current primary rule for 2006–2009. Four options.
None is free.

| | Option | Boundaries retained | Tier A placebo pool | Cost |
|---|---|---:|---:|---|
| 1 | Raise Tier A floor to 2010 | 4 (loses 2009) | 7 | Loses the only boundary with no intruding reset (plan §8.5); starts the series at the refuelling-ban discontinuity |
| 2 | Use Q1+Q2 only, all seasons | 5 | 9 | Discards Q3 everywhere; leans on Q2, which Finding E suggests has its own time-varying contamination |
| 3 | Drop Q3 in 2006–2009 only; three segments from 2010 | 5 | 9 | Era-dependent realisation of the rule |
| 4 | Q1 only, all seasons | 5 | 9 | Front-runners demonstrably do not fully attack in Q1 (that is what the −0.43 s Q1→Q2 delta *is*); worst contamination at the front, where M4 and M5 measure |

Note that only option 1 changes the boundary count, and it removes the boundary
plan §8.5 identified as the cleanest natural experiment in the study.

---

## 8. Consequences for scope (Decision G)

Pending the section 7 decision:

- **Tier A: 2006–2026** (21 seasons) under options 2, 3 or 4; **2010–2026**
  (17 seasons) under option 1.
- **Tier B: 2018–2026** (9 seasons), covering the 2021–22 and 2026 boundaries.

**A hard limit on Tier B, now confirmed.** The 2021–22 boundary's Tier B
pre-period is 2018, 2019, 2020 — and 2019 and 2020 are both flagged
discontinuities. That leaves **one unflagged pre-season (2018)** on which to
estimate a pre-boundary level and slope. Combined with the two-boundary placebo
pool from plan §8.6, Tier B cannot carry an independent conclusion. It functions
as a corroboration check on Tier A and nothing more, and the memo must say so.
