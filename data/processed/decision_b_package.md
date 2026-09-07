# Decision B — primary metric

**Nothing is frozen.** This presents the candidates, their behaviour, and my
reasoning. The choice is yours, and it must be made before the confirmatory
pooled tests in plan §8.3–8.4 run.

Figure: `figures/decision_b_metrics.png`.
Thresholds: 107% / 5.0 s / 3 laps (Decision A as re-estimated).

---

## Candidates, after exclusions

| metric | status | why |
|---|---|---|
| M1 field spread (sd) | **candidate** | |
| M2 robust spread (IQR) | **candidate** | |
| M3 leader→midfield | **candidate** | |
| M4 front group vs rest | **candidate, restricted** | D1c fired: no cross-2010 claims |
| M5 front-pair gap | **RETIRED** | at or below the M7 driver-noise floor in most seasons, in both tiers |
| M6 backmarker gap | diagnostic only | grid-size sensitive by construction; kept to detect confound 4 |
| M7 teammate delta | not a candidate | it is the denominator, not a measure of competitiveness |

**M5 is retired, not deleted.** It remains computed, plotted and reported, and
every M5 figure is marked as below the driver-noise floor. A metric that cannot
resolve its target is a reportable result about the limits of the measurement,
not an embarrassment to hide.

**M4's restriction bites harder than it first appears.** The D1c rule withdraws
any M4 estimate spanning 2010. The 2009 boundary's window is 2006–2013, which
contains 2010 in its post-period — so **M4 cannot carry the 2009 boundary
either**. M4 survives only for 2014 onward.

---

## Placebo battery — the context every shift must be read against

Nine eligible Tier A control boundaries: 2007, 2008, 2011, 2012, 2013, 2015,
2018, 2024, 2025. 2010 is reported separately as a measurement-artifact
boundary, never inside the clean pool.

Each reset's shift, as a percentile of the placebo |shift| distribution:

### M1 — field spread (sd) · placebo median |shift| 0.440, max 0.653

| boundary | shift | 95% CI | pctile | exceeds all placebos |
|---|---:|---|---:|:---:|
| *2010 (artifact)* | *+0.855* | *[0.695, 1.003]* | *100* | *yes* |
| 2009 | +0.719 | [0.608, 0.902] | 100 | **yes** |
| 2014 | −0.584 | [−0.714, −0.429] | 89 | no |
| 2017 | −0.263 | [−0.370, −0.140] | 44 | no |
| 2021–22 | −0.390 | [−0.460, −0.266] | 44 | no |
| 2026 | +0.653 | [0.434, 0.768] | 100 | **yes** |

### M2 — robust spread (IQR) · placebo median 0.186, max 0.586

| boundary | shift | 95% CI | pctile | exceeds all |
|---|---:|---|---:|:---:|
| *2010 (artifact)* | *+0.761* | *[0.523, 0.917]* | *100* | *yes* |
| 2009 | +0.659 | [0.338, 0.869] | 100 | **yes** |
| 2014 | −0.395 | [−0.561, −0.189] | 78 | no |
| 2017 | −0.066 | [−0.206, 0.058] | 11 | no |
| 2021–22 | −0.385 | [−0.504, −0.246] | 78 | no |
| 2026 | +0.608 | [0.352, 0.814] | 100 | **yes** |

### M3 — leader→midfield · placebo median 0.332, max 0.469

| boundary | shift | 95% CI | pctile | exceeds all |
|---|---:|---|---:|:---:|
| *2010 (artifact)* | *+0.413* | *[0.157, 0.577]* | *89* | *no* |
| 2009 | +0.005 | [−0.185, 0.409] | 0 | no |
| 2014 | +0.424 | [0.220, 0.629] | 89 | no |
| 2017 | +0.041 | [−0.146, 0.235] | 0 | no |
| **2021–22** | **−0.650** | **[−0.809, −0.454]** | **100** | **yes** |
| 2026 | +0.253 | [0.020, 0.391] | 33 | no |

### M4 — front group vs rest · placebo median 0.343, max 0.599 · *2009 estimate withdrawn (D1c)*

| boundary | shift | 95% CI | pctile | exceeds all |
|---|---:|---|---:|:---:|
| *2010 (artifact)* | *+0.827* | *[0.645, 1.116]* | *100* | *yes* |
| ~~2009~~ | ~~+0.681~~ | — | — | **withdrawn: window spans 2010** |
| 2014 | −0.284 | [−0.504, −0.112] | 33 | no |
| 2017 | −0.066 | [−0.252, 0.055] | 0 | no |
| **2021–22** | **−0.642** | **[−0.760, −0.466]** | **100** | **yes** |
| 2026 | +0.612 | [0.464, 0.764] | 100 | **yes** |

### M5 — RETIRED · placebo median 0.087, max 0.325

No boundary exceeds the placebo maximum. Consistent with a metric operating
below its resolution floor: it does not move distinguishably anywhere.

### M6 — diagnostic only · placebo median 0.968, max 1.751

2010 (+2.397) and 2009 (+1.917) both exceed all placebos. M6 is doing exactly
the job it was kept for — flagging grid-composition change.

---

## What I would put to you, and what I would not

**I recommend M2 (robust spread, IQR) as primary, with M3 as the leading
alternative.** Reasoning, in the order I weight it:

1. **M2 is the only whole-field candidate that resists confound 4.** Three grid
   expansions fall inside the study window — 2010 (10→12), 2016, and 2026
   (10→11) — and one of them is the headline season. M1 is a standard deviation
   and is moved bodily by a single new backmarker; M6 is moved by construction.
   M2's interquartile range is insensitive to the tails where new entrants land.
   The 2010 artifact boundary shows the difference: M1 shifts +0.855 against a
   placebo max of 0.653, M2 shifts +0.761 against 0.586 — both are moved, but
   M1's whole distribution sits wider.

2. **M2 keeps all five boundaries.** M4 loses 2009 to the D1c restriction and
   M5 is retired. Any metric that cannot speak to 2009 forfeits the least
   contaminated boundary in the study.

3. **M2 and M3 disagree in a way you should see before choosing.** On M2 the
   2021–22 shift is −0.385 at the 78th placebo percentile — real but not
   exceptional. On M3 it is −0.650 and **exceeds every placebo**. M3 is more
   sensitive to precisely the convergence the 2021–22 package claimed to
   deliver, because M3 measures the leader-to-midfield gap rather than
   whole-field dispersion. If you think the interesting question is "did the
   midfield close on the leaders," M3 is the better instrument and I would not
   argue. I lead with M2 because it makes fewer structural assumptions about
   where in the field the effect should appear.

4. **M1 is the conventional choice and I am not recommending it**, which is
   worth saying plainly. It is the most familiar dispersion measure and the
   easiest to explain, and it is the most exposed to the one confound this
   study cannot design away.

**What I am not doing:** picking the metric whose 2021–22 result is largest.
On M3 the 2021–22 effect exceeds all placebos; on M2 it does not. Choosing M3 on
that basis would be selecting the metric for its answer. If you choose M3, the
reason should be that leader-to-midfield is the quantity of interest, decided
independently of what it shows.

---

## Two observations for Decision H, recorded not interpreted

**The placebo distribution is wide.** Ordinary season boundaries move M1 by a
median of 0.44 and up to 0.65. Two of the five resets (2017 at the 44th
percentile, and 2021–22 also at 44th on M1) sit inside that ordinary range.
Whether a reset that moves the field no more than an average season counts as
"no effect" is your call, but the comparison is now on the record for all nine
control boundaries rather than resting on 2010 alone.

**2026 widens the field on every whole-field metric, exceeding all placebos.**
It is also the season with an eleventh constructor and 13 of 23 rounds. Both
facts are recorded; neither is interpreted here.
