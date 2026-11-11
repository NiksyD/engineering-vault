# CodeMentorAI Participant Results Analysis

  

Source: live Supabase tables `submissions`, `ai_audits`, `activities`, `topics`, `modules`, queried read-only on 2026-11-11. Users are anonymized (P1 to P16). Overall score is recomputed from the four stored criterion scores with the system's ACF weights (C 0.2484, R 0.2453, M 0.2516, E 0.2547), the same formula as `calculateACFCompositeScore`.

  

## 1. Executive Summary

  

The database holds 160 submissions from 16 accounts. The evaluation session took place on 2026-11-10, roughly 12:47 to 15:33 UTC. Three accounts (P3, P5, P6) completed the pretest and then trained in the same session. Their submission and audit timestamps look organic (median 18 to 20 s between submission and AI review).

  

**Classification: Insufficient Evidence of improvement (No Observable Improvement on the data that can be compared).**

  

| Participant | Language | Pretest overall | Training overall | Change (pp) |

|---|---|---|---|---|

| P3 | Java | 90.33 | 90.32 | -0.01 |

| P5 | C | 95.41 | 94.96 | -0.45 |

| P6 | Java | 95.77 | 96.39 | +0.62 |

  

All three began at or near the ceiling (90 to 96). Changes are within about 1 point, in both directions. The data neither shows nor rules out improvement. It mainly shows that the instrument cannot detect improvement for these learners (see Section 9).

  

Three further accounts (P7, P8, P15) are included at the owner's instruction. They have only partial pretest data (5 to 6 of 10 challenges) and no training submissions, so no pretest-to-training change can be computed for them. They are analyzed separately, as within-pretest progression (Section 5B). Their score trajectories were script-altered (Section 9), so this progression is not valid evidence of learner improvement.

  

## 2. Participant Overview

  

| ID | Language | Pretest submissions (reviewed) | Training submissions (reviewed) | Session span (min) | Notes |

|---|---|---|---|---|---|

| P3 | Java (+2 C pretest items after training) | 12 (10 Java, 2 C) | 8 | 80 | Full Java pretest |

| P5 | C | 10 | 5 | 85 | Full pretest, 5 Easy training items only |

| P6 | Java | 10 | 16 | 75 | Full pretest, most training exposure |

| P7 | C | 5 | 0 | 56 | Included per owner; test account; pretest only; script-altered |

| P8 | Java | 6 | 0 | 46 | Included per owner; test account; pretest only; script-altered |

| P15 | Java | 5 | 0 | 57 | Included per owner; test account; pretest only; trajectory not independently verifiable |

| P1, P2, P4, P9 to P14, P16 | Mixed | see note | see note | n/a | Dev/test or fragmentary use; no complete pretest plus training pair |

  

Only P3, P5 and P6 have a complete pretest and subsequent training. All reviewed submissions have an AI review (160 audits for 160 submissions), though some of P1 and P4's records lack the four criterion scores.

  

Not recorded in the database: `user_primary_language`, `user_pretest_status`, `user_research_consent` and `user_consent_*` are empty for every profile. Language here is inferred from `sub_language`. Consent is not documented in the data.

  

## 3. Initial Baseline Results (Pretest, 10 challenges)

  

Language-matched pretest only (P3's two C items excluded).

  

| ID | n | Correctness | Readability | Maintainability | Efficiency | Overall | Strongest | Weakest |

|---|---|---|---|---|---|---|---|---|

| P3 (Java) | 10 | 89.7 | 90.2 | 82.3 | 99.0 | 90.33 | Efficiency | Maintainability |

| P5 (C) | 10 | 100.0 | 93.9 | 88.7 | 99.0 | 95.41 | Correctness | Maintainability |

| P6 (Java) | 10 | 99.3 | 95.5 | 89.8 | 98.5 | 95.77 | Correctness | Maintainability |

  

All three show the same profile: Maintainability is the weakest criterion, and Efficiency and Correctness are strongest. Baselines are high, so the headroom for measurable gain is small (at most about 5 to 10 points).

  

**Pretest-only participants** (items completed so far, not the full 10; items 1 to 5 are the same for all three, P8 also did item 6):

  

| ID | n of 10 | Correctness | Readability | Maintainability | Efficiency | Overall | Strongest | Weakest |

|---|---|---|---|---|---|---|---|---|

| P7 (C) | 5 | 81.4 | 76.0 | 67.0 | 87.0 | 77.9 | Efficiency | Maintainability |

| P8 (Java) | 6 | 62.5 | 85.5 | 75.0 | 94.2 | 79.4 | Efficiency | Correctness |

| P15 (Java) | 5 | 89.6 | 78.8 | 75.2 | 79.6 | 80.8 | Correctness | Maintainability |

  

These three have lower, more variable scores than P3, P5 and P6, so they have more room to change. Their means cover only the easier early items (items 1 to 5 are all Easy; P8's item 6 is Medium), so they are not comparable with the full 10-item baselines above.

  

## 4. Subsequent Performance Results (Training Modules)

  

Training items come from the system modules, which are different challenges from the pretest.

  

| ID | n | Correctness | Readability | Maintainability | Efficiency | Overall | First half / second half (overall) |

|---|---|---|---|---|---|---|---|

| P3 | 8 | 93.8 | 93.5 | 81.3 | 92.9 | 90.32 | 94.7 / 85.9 |

| P5 | 5 | 97.6 | 95.2 | 87.0 | 100.0 | 94.96 | 93.6 / 95.8 |

| P6 | 16 | 99.4 | 97.0 | 93.3 | 95.9 | 96.39 | 95.5 / 97.2 |

  

Individual submission scores (not cumulative averages), in submission order:

  

- P3 training: 93, 100, 95, 91, 96, 77, 80, 90

- P5 training: 95, 92, 96, 96, 95

- P6 training: 100, 92, 99, 97, 98, 94, 89, 96, 96, 100, 98, 96, 99, 98, 99, 92

  

The Growth over Time chart shows a running (cumulative) average after each submission, not an individual result ([acf.ts](../codementorai-web/lib/competency/acf.ts) `computeAcfGrowth`). A cumulative average hides fluctuation. For example, P3's individual scores fall to 77 and 80 late in training, yet the running average declines only modestly.

  

## 5. Quantitative Comparison and Individual Analysis

  

Formula: Observed Score Change = Training mean (final observed) minus Pretest mean (baseline). Relative change = change / baseline x 100.

  

| ID | Baseline | Observed | Change (pp) | Relative | dC | dR | dM | dE |

|---|---|---|---|---|---|---|---|---|

| P3 | 90.33 | 90.32 | -0.01 | -0.01% | +4.1 | +3.3 | -1.0 | -6.1 |

| P5 | 95.41 | 94.96 | -0.45 | -0.47% | -2.4 | +1.3 | -1.7 | +1.0 |

| P6 | 95.77 | 96.39 | +0.62 | +0.65% | +0.1 | +1.5 | +3.5 | -2.6 |

  

**P3 (mixed, flat overall).** Correctness and Readability rose (+4.1, +3.3) while Efficiency fell (-6.1) and Maintainability slipped. The second half of training (85.9) is lower than the first (94.7), with scores of 77 and 80 near the end. Pretest and training also included different items, so a decline may reflect harder items. Classification: Mixed Performance.

  

**P5 (flat, ceiling).** Overall difference is -0.45. The 5 training items were all Easy, whereas the pretest spanned Easy to Hard, so the training sample is not comparable in difficulty. Only 5 submissions. Classification: Insufficient Evidence.

  

**P6 (small positive, within noise).** +0.62 overall, led by Maintainability (+3.5), with 16 training submissions. The pattern is consistent with slight improvement but equally with item differences. Individual scores sit between 89 and 100 throughout. Classification: Mixed Performance, trending slightly positive.

  

No difference above 1 point overall can be separated from scoring noise. The AI scorer is not shown to be reliable at that resolution.

  

### 5B. Pretest-only participants (P7, P8, P15): within-pretest progression

  

These accounts have no training submissions, so there is no baseline-versus-subsequent comparison. The only change that can be computed is across the pretest items in order. Change here = second-half mean minus first-half mean, and last item minus first item. It reflects item order and difficulty as much as learning, and the pretest challenges differ from one another.

  

Individual submission scores (overall), in order:

  

- P7 (C): 91.3, 73.2, 68.6, 66.4, 89.9

- P8 (Java): 60.2, 71.3, 96.3, 65.9, 89.9, 92.5

- P15 (Java): 62.3, 70.8, 82.0, 91.0, 97.8

  

| ID | First half | Second half | Change (pp) | First item | Last item | Change (pp) |

|---|---|---|---|---|---|---|

| P7 | 82.2 | 75.0 | -7.2 | 91.3 | 89.9 | -1.4 |

| P8 | 75.9 | 82.8 | +6.9 | 60.2 | 92.5 | +32.3 |

| P15 | 66.6 | 90.3 | +23.7 | 62.3 | 97.8 | +35.5 |

  

First-half to second-half change by criterion (pp):

  

| ID | dC | dR | dM | dE |

|---|---|---|---|---|

| P7 | -24.3 | +18.3 | -0.8 | -21.7 |

| P8 | +18.4 | +7.6 | +3.4 | -1.7 |

| P15 | +6.0 | +24.7 | +29.5 | +34.3 |

  

**P7 (fluctuating, no net gain).** Scores fall from 91.3 to 66.4 and recover to 89.9. The dip is driven by Correctness on Leap Year (20) and by Readability (45) on Format a Profile Line. Readability rose in the second half (+18.3) while Correctness and Efficiency fell. Classification: Mixed Performance. Only 5 of 10 items completed.

  

**P8 (fluctuating, upward).** Scores alternate (60, 71, 96, 66, 90, 92). The same item type that was weak for P7 (Leap Year, Correctness 15) is weak here, and the final two items are the highest-scoring besides Even or Odd. Correctness drove most of the second-half rise (+18.4). Classification: Mixed Performance with a net rise; the sequence is not monotonic and 6 of 10 items were completed.

  

**P15 (steady rise).** Overall rises monotonically (62.3, 70.8, 82.0, 91.0, 97.8), and all four criteria rise together, with Efficiency moving from 40 to 100 across five Easy items. Taken at face value this is Observable Improvement within the pretest. However, this is the only participant whose four criteria all climb in lockstep, which is atypical of AI scores for independently written solutions; P3, P5 and P6 show no comparable pattern. I could not verify from the database how P15's submissions were produced, so this rise cannot be relied on as learner growth.

  

**Why this is not pre/post evidence.** All three changes happen inside the pretest, before any training module. A rise here reflects familiarity with the task format, item order and the AI feedback on earlier items, not use of the training modules. And P7's and P8's later submissions were replaced by script (Section 9), so their curves partly reflect author-written code.

  

## 6. Comparative Analysis

  

- Trends differ in sign: P6 +0.62, P3 about 0, P5 -0.45. No shared direction.

- Most consistent criterion change: Readability rose for all three (+3.3, +1.3, +1.5). Maintainability and Efficiency moved in opposite directions across participants.

- Language: P5 used C, P3 and P6 used Java. Two Java users diverge (-0.01 vs +0.62), so language does not explain the pattern, but with n=3 nothing can be established.

- Exposure differs strongly (5, 8, 16 training items; Easy-only for P5), which confounds comparison.

  

The pretest-only group (P7, P8, P15) is not directly comparable with them: they lack training data, completed only 5 to 6 items, and show larger swings (item scores from 15 to 100 on single criteria) at lower averages (77.9 to 80.8). Within the pretest, two of three rose (P8 +6.9, P15 +23.7) and one fell (P7 -7.2); no consistent direction. Readability rose in the second half for all three (+18.3, +7.6, +24.7), which matches the direction seen in P3, P5 and P6.

  

These are six cases and do not generalize to other CodeMentorAI users.

  

## 7. Determination of Observable Improvement

  

| Question | Finding |

|---|---|

| Improved performance on the activities completed | Not demonstrated; scores were already high |

| Improvement in the four measured criteria | Mixed: Readability up for all, others inconsistent |

| Overall programming competency development | Not assessable with this design |

| Long-term learning or retention | Not assessable (single session, no delayed test) |

  

Per-participant classification:

  

| ID | Classification | Basis |

|---|---|---|

| P3 | Mixed Performance | Overall -0.01; C and R up, M and E down |

| P5 | Insufficient Evidence | Overall -0.45; Easy-only training, 5 items |

| P6 | Mixed Performance | Overall +0.62; within noise |

| P7 | Mixed Performance | Within-pretest only; -7.2 half-to-half |

| P8 | Mixed Performance | Within-pretest only; +6.9, non-monotonic |

| P15 | Insufficient Evidence | Within-pretest rise of +23.7 is not usable as growth (no training data; provenance unverified) |

  

Overall classification: **Insufficient Evidence**. No participant has an unaltered, comparable pretest-to-training increase that exceeds scoring noise. Even a positive change would not establish causation, given practice effects, familiarity with the pretest language, item differences and the very short interval (about 75 to 85 minutes).

  

Statistical significance is not claimed or tested. With n=3 and ceiling-level scores, an inferential test would not be justified.

  

## 8. Research Implications

  

The data supports a limited claim: the platform ran an end-to-end pretest, training and AI review flow for three learners, and the AI feedback produced differentiated criterion scores (Maintainability was consistently the weakest). It does not support a claim that CodeMentorAI improves programming performance. The current design needs lower-baseline learners and a comparable post-assessment before improvement can be evaluated.

  

## 9. Limitations and Data Integrity

  

1. **Altered data in the database.** The scripts [run-kim-growth.ts](../codementorai-web/scripts/run-kim-growth.ts), [run-joshua-growth.ts](../codementorai-web/scripts/run-joshua-growth.ts), [retake-submission.js](../codementorai-web/scripts/retake-submission.js) and [run-real-retake.ts](../codementorai-web/scripts/run-real-retake.ts) delete or replace submissions, backdate timestamps, or write audits directly. The scripts name P7 (`run-joshua-growth.ts`: replaces submissions 2, 3 and 5 with deliberately weaker, then stronger, code) and P8 (`run-kim-growth.ts`: replaces submissions 5 and 6 so the trend "shows improvement instead of a decline"). The usage example in `retake-submission.js` names P15's address (jmgigante35@gmail.com); I did not confirm that it was run against P15, so P15's provenance is unverified. P15's trajectory is monotonic in all four criteria, which is atypical of the other accounts. The owner identifies P7, P8 and P15 as test accounts and asked for them to be included. They are reported in Section 5B for completeness, but their within-pretest curves are author-influenced and must not be presented as independent learner growth. Any manuscript that reports them as participants must disclose this.

2. **Ceiling effect.** Baselines of 90 to 96 leave almost no room to improve.

3. **Different instruments.** Pretest and training use different challenges and different difficulty mixes ([pretest-blueprint.md](pretest-blueprint.md) states the changes are not like-for-like). P5's training was Easy only.

4. **No separate posttest** and no delayed retention measure.

5. **Single-session, n=3 usable cases.** No control group and no inferential test.

6. **AI scoring.** One model (Gemini) scores all four criteria; no inter-rater or human reliability check. Scores cluster at 90 to 100.

7. **Lenient output checking** and no subject-matter-expert review of the challenges.

8. **Missing records.** No consent, pretest status or declared language in `profiles`; 66 of 160 submissions reference activities that no longer exist (43 of them from P10) and cannot be categorized.

9. **Mixed languages.** P3 took part of the pretest in C after training.

10. **Identity of real participants not confirmed.** I treated P3, P5 and P6 as the evaluation participants because they alone have complete pretest and training data. This should be confirmed.

  

## 10. Conclusion

  

Among three learners who completed a pretest and subsequent training in a single session, overall observed changes were -0.01, -0.45 and +0.62 percentage points. Learners began near the maximum score, items differed between pretest and training, and no posttest was administered. The evidence is therefore insufficient to conclude that observable improvement occurred, and it cannot support any claim about CodeMentorAI's causal effect. Further evaluation should include learners with lower baselines, a matched-difficulty posttest, more participants and a delayed retention check, with all submissions left unaltered.