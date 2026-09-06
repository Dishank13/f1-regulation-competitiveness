# Confound 17 — uniform wet-qualifying flag: interim findings

**Status: INTERIM. The FastF1 validation required by condition 2 is queued behind
the 500 calls/hour rate limit** (the Tier B race acquisition holds the quota and
is not parallelised around, per instruction). This document reports what is
established without that quota. **No filtering decision has been made.**

## What was built

Uniform across all 21 seasons, as required: circuit latitude/longitude and
qualifying date from Jolpica, precipitation from the Open-Meteo historical
reanalysis archive. Derived entirely outside the timing data, so non-circular.
412 of 422 scheduled events have data; the 10 without are unraced 2026 rounds
with future dates, recorded as `future_session` rather than as failures.

## Condition 3 — temporal resolution, stated plainly

| | Coverage |
|---|---|
| Qualifying **date** | **100%**, all 21 seasons |
| Qualifying **time** | **only 2022–2026** (0% for 2006–2021) |
| Circuit coordinates | 100%, all 21 seasons |

A session-window flag is therefore **impossible** before 2022. Building one would
recreate the exact strictness cliff this exercise exists to remove, moved from
2018 to 2022.

The flag is consequently **whole-day precipitation at the venue on the qualifying
date**, applied identically to every season.

**A fixed local-time afternoon window was considered and rejected.** It is
uniform in its *rule* but not in its *accuracy*: night qualifying sessions
(Singapore from 2008, Bahrain from 2014, Las Vegas from 2023) grow as a share of
the calendar across the study window, so its error rate would drift with time.
That reintroduces the failure class through the calendar instead of the data
source. Whole-day is coarser but uniform in both dimensions.

## Three problems, in increasing severity

### 1. Over-flagging at low thresholds

| Threshold | Events flagged | Share |
|---|---:|---:|
| daily ≥ 0.5 mm | 172 | 40.8% |
| daily ≥ 1.0 mm | 142 | 33.6% |
| daily ≥ 2.0 mm | 108 | 25.6% |
| daily ≥ 5.0 mm | 66 | 15.6% |

Genuinely wet or mixed F1 qualifying sessions are a small minority of events.
A third of all sessions is not a plausible wet rate; it is trace and overnight
rain being counted as a wet session.

### 2. Condition 5 — exclusions cluster heavily by season

At daily ≥ 1.0 mm: 2018 flags **71.4%** of its events, 2010 **57.9%**, 2017
**50.0%** — against 2026 at 7.7% and 2006–07 at ~22%. At daily ≥ 5.0 mm: 2010
**42.1%** and 2018 **33.3%**, against **0.0%** for both 2007 and 2025.

This is not noise around a constant rate. Applying such a filter would remove
events at sharply different rates across the study window — which is the
time-varying exclusion problem the uniform source was supposed to solve,
re-entering through real meteorological and calendar variation rather than
through data availability.

Whether the clustering falls inside boundary windows is deferred to the full
validation, but 2010 and 2018 both sit inside boundary windows.

### 3. The date field is the scheduled date, not the actual date — and this
### fails hardest exactly where it matters

The two highest-precipitation events in the entire dataset were hand-verified
against contemporaneous reports (condition 4). Both were **postponed because of
the weather the flag is detecting**, and they fail in opposite directions.

**2019 r17 Japanese GP, Suzuka — 134.4 mm, the highest in the dataset.
FALSE POSITIVE.** All Saturday running on 12 October was cancelled for Typhoon
Hagibis; qualifying was rescheduled to Sunday 13 October and **ran in dry
conditions**. Jolpica records the qualifying date as the cancelled Saturday. The
flag reports the wettest session in the study; the session was dry.
Sources: [Sky Sports](https://www.skysports.com/f1/news/12040/11831808/japanese-gp-qualifying-moved-to-sunday-due-to-typhoon-hagibis),
[Formula1.com](https://www.formula1.com/en/latest/article/saturday-running-cancelled-in-japan-full-revised-timetable-for-sunday.7bCNvGLXjco9zJUIEKgtvu)

**2015 r16 United States GP, Austin — 91.7 mm. TRUE POSITIVE, WRONG DAY.**
Saturday 24 October qualifying was abandoned after repeated delays; the session
ran Sunday 25 October and **Q3 was cancelled by worsening rain**, giving Rosberg
pole on a Q2 time. The session was genuinely wet — but on a different day from
the one the flag measured. It is correct by coincidence.
Sources: [Formula1.com](https://www.formula1.com/en/latest/article/qualifying-postponed-until-sunday-morning-in-storm-swept-austin.5jSYeIam5qQqDUrtIaFKiV),
[RaceFans](https://www.racefans.net/2015/10/24/united-states-grand-prix-qualifying-postponed-to-sunday/)

**Why this is structural rather than two unlucky cases.** Sessions are postponed
*because of* severe weather. So the date field is systematically least reliable
on precisely the events a wet filter exists to catch, and the error is not
random — it correlates with the thing being measured.

## Correction to an earlier claim

The Phase 2 ledger stated that Austin 2015's Q1 and Q2 observations "are adjusted
on the same basis as every other event and carry no special measurement status."
**That was wrong.** Austin 2015 ran in wet conditions with Q3 cancelled by rain.
Its observations are wet-session observations. The L3 *flag* was still a genuine
bug and its fix stands; the reassurance attached to it did not.

## What the source does get right

The high end of the distribution is credible. The top of the list reads as a
genuine roll-call of wet weekends — Suzuka 2019 and 2010, Austin 2015, Monza 2008
and 2017, Sochi 2021, Styria 2020, Imola 2022, Interlagos 2010. The reanalysis is
measuring real rain at the right venues on the right weekends. The failure is one
of **resolution and date accuracy**, not of the underlying meteorology.

## Preliminary assessment — not a decision

Three independent problems point the same way: over-flagging at any usable
threshold, heavy season-level clustering, and a date field that is systematically
wrong on postponed sessions. The formal test is still the FastF1 agreement rate
required by condition 2, and it is queued, not skipped.

If that agreement rate is poor, the pre-agreed fallback applies: **no wet
filtering in either era, stated as a limitation, with wet-session contamination
added to the confound list.** On current evidence that is the likely outcome, and
it is the honest one — a filter that is wrong on the wettest event in the study
is worse than no filter, because it would remove real sessions while claiming
rigour.
