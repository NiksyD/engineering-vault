---
title: "CodeMentorAI Competition Readiness (CRC/CRA): Implementation Plan"
category: Implementation Plan
status: In Progress
priority: P0
created: 2026-11-08
updated: 2026-11-08
tags:
  - roadmap
  - todo
  - codementorai
  - competency-profile
  - cra
  - web
  - mobile
---

# CodeMentorAI Competition Readiness (CRC/CRA): Implementation Plan

> **For AI Agents & Developers:** A task may only be marked `[x]` after `npx tsc --noEmit` passes in `codementorai-web`, the CRA unit tests pass on web and mobile, and `flutter analyze` is clean for touched Dart files. Obey `AGENTS.md` (no "curriculum", "course", "syllabus"; no "Capstone"; WCAG text rules). Pre-existing unrelated failures (`app/api/submissions/route.ts(103,65)`, Flutter CI format check) are not part of this work.

**Source of truth:** `docs/CodeMentorAI_CRC_Criteria_and_Historical_Metrics.pdf`. It replaces the earlier working spec (solve-rate consistency, fixed 6-topic breadth target, 70 mark). Where the code and the PDF disagree, the PDF wins.

**Goal:** One calculation, identical on web and mobile, that produces the Competition Readiness Score (0 to 100) shown on the Competency Profile.

---

## 1. The method (from the PDF)

**Solved rule.** A challenge is *correctly solved* only when it passes **all** automated test cases **and** its AI correctness score is **at least 80%**. This is separate from Accuracy and from any assessment's own pass mark.

| Criterion | Historical formula | Notes |
|---|---|---|
| Accuracy (A) | `Σ Cᵢ / Σ Tᵢ × 100` | Cᵢ = solved challenges in assessment i, Tᵢ = challenges attempted in assessment i |
| Efficiency (E) | `Σ Eⱼ / K` | Eⱼ = AI efficiency score of solved challenge j; K = solved challenges that have a valid efficiency score. The efficiency score itself does not need to reach 80%. |
| Problem Breadth (PB) | `D_h / T_h × 100` | D_h = unique topics demonstrated, T_h = unique topics assessed, across historical assessments. Repeats count once. |
| Consistency (C) | `100 − MAD` | MAD = `Σ|Aᵢ − Ā| / N`, where Aᵢ is the accuracy of assessment i and Ā the average of those accuracies |

**Final score:**

```
CRA = A × 0.2557 + E × 0.2590 + PB × 0.2393 + C × 0.2460
```

The four weights sum to exactly 1.0000. Result is the **Competition Readiness Score (CRS)**, 0 to 100.

**Topic credit rules (Breadth).** A tag is credited only when all hold: the activity genuinely requires the concept, the submitted code contains the construct, the construct is meaningfully used to solve the problem, all tests pass, and AI correctness is at least 80%. Each challenge carries 1 to 3 tags.

**Worked examples to turn into tests** (all from the PDF):

| Case | Input | Expected |
|---|---|---|
| Efficiency | Challenges rated 85, 90, 80, 95, 75; the 95 has accuracy below 80% | `(85+90+80+75)/4 = 82.5` |
| Breadth | 5 unique topics assessed, 4 demonstrated | `4/5 × 100 = 80` |
| Consistency | Assessment accuracies 70, 70, 30, 40, 90 (mean 60) | MAD = `(10+10+30+20+30)/5 = 20`, so C = `80` |

---

## 2. Gap analysis: current code vs the PDF

Current web implementation: `codementorai-web/lib/competency/cra.ts`. Mobile port: `codementorai-mobile/lib/src/features/learn/domain/cra.dart`. Both were written to the earlier working spec.

| #   | Area             | Code today                                                                                                      | PDF                                                                         | Change                                                              |
| --- | ---------------- | --------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------- | ------------------------------------------------------------------- |
| G1  | Solved threshold | `SOLID_RATING_MARK = 70`                                                                                        | 80                                                                          | Change to 80 on both platforms                                      |
| G2  | Accuracy         | Solved ÷ attempted over the **latest attempt** of each assessment                                               | `ΣC / ΣT` over completed assessments                                        | Same shape. No formula change. Retake rule needs a decision (D1)    |
| G3  | Efficiency       | Mean of efficiency over solved problems with a rating                                                           | Same                                                                        | No formula change. Depends on solved threshold moving to 80 (G1)    |
| G4  | Problem Breadth  | `topics solved ÷ 6`, capped at 100 (`BREADTH_TARGET_TOPICS`)                                                    | `D_h / T_h`: demonstrated ÷ assessed                                        | **Rewrite.** Needs the set of topics *assessed*, not a fixed target |
| G5  | Breadth credit   | Topic credited when the problem is solved                                                                       | Also requires the construct to be present in the code and meaningfully used | New verification step (see Phase 3)                                 |
| G6  | "Other" topic    | Stored but excluded from Breadth                                                                                | Not mentioned                                                               | Decision (D3)                                                       |
| G7  | Consistency      | Share of assessments with at least 50% solved (`CONSISTENCY_SUCCESS_SHARE`), first attempts, last 10, minimum 3 | `100 − MAD` of per-assessment accuracy                                      | **Rewrite**                                                         |
| G8  | Weights          | Consistency `0.2459` (sum 0.9999)                                                                               | `0.2460` (sum 1.0000)                                                       | Fix constant on both platforms                                      |
| G9  | Missing criteria | Re-weights the remaining criteria to 100%                                                                       | Not specified                                                               | Keep, but confirm (D4)                                              |
| G10 | Rounding         | Whole numbers                                                                                                   | PDF example shows `82.5%`                                                   | Decision (D5)                                                       |

Consumers that will change output when the calculation changes (check each after Phase 1 and 2):

- Web: `app/learn/components/LearnerCompetencyProfile.tsx`, `CompetencyGrowthChart.tsx`, `lib/store/useCompetencyStore.ts`, `app/api/classrooms/[id]/gradebook/route.ts`, `app/mentor/hubs/[id]/learners/[learnerId]/components/LearnerReadinessSection.tsx`
- Mobile: `competency_profile_view.dart`, `assessment_report_screen.dart`, `supabase_assessment_repository.dart` (`_attachCraProblems`)

---

## 3. Decisions (not covered by the PDF)

Accepted as recommended on 2026-11-08.

- [x] **D1. Retakes.** Keep today's rule. Accuracy, Efficiency and Breadth use the latest attempt of each assessment; Consistency uses the first attempt, so retakes cannot raise stability.
- [x] **D2. Minimum data for Consistency.** With one assessment, MAD is 0 and Consistency would read 100, which says nothing. Keep the minimum of 3 assessments and show "—" with "needs 3 assessments" below that.
- [x] **D3. "Other" topic.** There is no "Other" tag in the new list (see 3a), so nothing vague can enter D_h or T_h. Keep the exclusion in `cra.ts` for old data.
- [x] **D4. Criteria with no data.** Keep re-weighting the remaining criteria and show "—" for the missing one. Scoring a missing criterion as 0 would punish new learners.
- [x] **D5. Display precision.** Whole numbers on cards. Compute with full precision and round once at the end, not per criterion, so the displayed total always matches the formula.
- [x] **D6. Consistency window.** Keep the window of the last 10 assessments so old results age out.

---

## 3a. Topic tags (prerequisite for Problem Breadth)

Problem Breadth needs T_h (topics assessed), so tags come first. Tags go on each **challenge and practice activity**, not on a whole module, because the PDF requires 1 to 3 tags per activity.

**Decisions (2026-11-08):**
- Taxonomy: 36 tags in 7 groups, grounded in CS2023 (Software Development Fundamentals, Algorithmic Foundations). Source file: `codementorai-web/lib/competency/topicTags.ts`, mirrored in `codementorai-mobile/lib/src/features/learn/domain/topic_tags.dart`. `test/topic_tags_test.dart` fails if the two drift.
- "Control Structures" is its own group: Conditional Statements, For, While and Nested Loops, split out of Programming Fundamentals. This matches the 7 groups that count toward Breadth.
- Recursion appears once, under Functions and Modularity.
- Efficiency concepts (Time Complexity, Space Complexity, Big-O, Time-Space Tradeoffs) are **not** tags. Efficiency is scored separately by the AI review; as tags they would inflate Breadth.
- No "Other" tag. Mentors pick from the list only; unknown values are dropped. Labels from the AI are mapped to ids.
- Tags are language-neutral and stored as ids, never labels.
- "At least one tag" is enforced at publish, not in the database, so already-published items keep working. Publishing a fix to a published assessment also requires tags.
- Assessment challenges first (they feed CRA), module practice activities second.

**Progress:**
- [x] Taxonomy file (web) and mirror (mobile) with parity test
- [x] Migration `codementorai-web/supabase/migrations/037_topic_tags.sql`: `topic_tags TEXT[]` on `assessment_challenges` and `activities`, at most 3. **Written, not yet run on the live database.**
- [x] Assessment Studio: topic picker in the challenge title row (`app/mentor/components/TopicTagPicker.tsx`), saved with the challenge, publish blocked until every challenge has a topic. Drafts still save if the migration has not run.
- [x] Attempt snapshot saves each challenge's tags at submit time (web take page, mobile repository)
- [ ] Run migration 037 in the Supabase SQL editor
- [ ] Tag the 11 existing assessment challenges (Breadth stays "—" for attempts on untagged challenges)
- [ ] Module practice activities: same picker in the module editor, publish gate on activities
- [x] AI suggests tags for assessment challenges. "Suggest topics" button in the picker (`POST /api/mentor/assessment/suggest-topics`, reads the reference solution first, then statement, starter code and sample tests) and tags returned with AI-generated assessments (`topic_tags` in the generate route). The server keeps only listed ids; the mentor reviews and edits. Checked against 5 real challenges: valid ids and sensible reasons.
- [ ] AI tags in the copilot's "add challenge" action and in module generation (not done yet; the Suggest button covers hand edits)
- [ ] Show tags to learners (challenge header, report) on web and mobile

---

## 4. Implementation phases

### Phase 0: Lock the spec into tests first
- [ ] 0.1 Add a web test file for `cra.ts` using the three PDF worked examples (table in section 1), plus the weights-sum-to-1 check.
- [ ] 0.2 Mirror the same cases in `codementorai-mobile/test/cra_test.dart`. Keep web and mobile parity checks (run web through node strip-types as before).
- [ ] 0.3 Confirm the tests fail on current code for G1, G4, G7, G8. That proves they test the new behavior.

### Phase 1: Threshold and weights (small, safe)
- [ ] 1.1 `SOLID_RATING_MARK` 70 to 80 in `cra.ts`; mirror in `cra.dart`. Update the comment ("Initial value, pending expert validation").
- [ ] 1.2 `CRA_WEIGHTS.consistency` 0.2459 to 0.2460 in both.
- [ ] 1.3 Search both codebases for any other hardcoded 70 used as a solved mark (gradebook route, mobile screens, AI audit copy) and route them through the one constant.
- [ ] 1.4 Update UI copy that mentions 70 or "solid rating".

### Phase 2: New Consistency (`100 − MAD`)
- [ ] 2.1 Per assessment, compute `Aᵢ = solved ÷ attempted × 100`, skipping assessments with no rated problems (same skip rule as today).
- [ ] 2.2 Compute `Ā`, then `MAD = Σ|Aᵢ − Ā| / N`, then `C = 100 − MAD`, clamped to 0 to 100.
- [ ] 2.3 Keep the minimum-assessments guard (D2) and the first-attempt, last-10 selection (D1, D6).
- [ ] 2.4 Remove `CONSISTENCY_SUCCESS_SHARE`. Rename result fields (`consistencySuccesses` no longer makes sense; expose `meanAccuracy` and `mad` instead so the screen can explain the number).
- [ ] 2.5 Update the one-sentence explanation on the Competency Profile, for example "Your accuracy varies by about 20 points between assessments."
- [ ] 2.6 Mirror in `cra.dart`. Verify with the PDF example (C = 80).
- [ ] 2.7 Note the PDF's own limitation in the UI help text: Consistency measures variation, not improvement.

### Phase 3: New Problem Breadth (`D_h / T_h`)
- [ ] 3.1 **Assessed set (T_h):** unique topics across every problem in the pooled attempts, whether solved or not, excluding "Other" (D3).
- [ ] 3.2 **Demonstrated set (D_h):** the subset credited under the topic rules. Phase 3.4 adds the code-level check; until then, credit = solved.
- [ ] 3.3 `PB = D_h / T_h × 100`. Return null when no problem carries topic tags, as today.
- [ ] 3.4 **Concept verification (new capability).** The PDF requires the code to contain the tagged construct and use it meaningfully. Plan:
  - Add a per-topic verdict to the AI feedback output ("construct present and used: yes/no") or a deterministic source/AST check per language, whichever the audit pipeline can support. *To confirm:* what the current AI audit record stores for each submission, and whether a per-topic field can be added without a migration.
  - Store the per-topic result in the attempt snapshot beside `topics`, so later edits to a problem or rubric do not rewrite history.
  - Until this ships, keep the interim rule (solved implies credited) and mark it in the UI help text as "based on solved problems".
- [ ] 3.5 Remove `BREADTH_TARGET_TOPICS`. Update the "N of 6 topics covered" copy to "N of M topics demonstrated" with the topic names and a suggestion for the next one.
- [ ] 3.6 Mirror in `cra.dart`; verify with the PDF example (4 of 5 gives 80).

### Phase 4: Wire-up and data checks
- [ ] 4.1 Confirm the attempt snapshot (`user_assessment_attempts.snapshot`) contains **every** problem with its topics, including unsolved and unsubmitted ones. T_h depends on it. If not, extend the snapshot write on web and in `supabase_assessment_repository.dart`.
- [ ] 4.2 Decide how to treat attempts that have no snapshot (older ones, and attempts from before the mobile port). Either skip them with a note or recompute from `submissions` and `ai_audits`. Count how many exist before choosing.
- [ ] 4.3 Check `computeCraGrowth` (growth chart) still produces sensible points: it replays `computeCra` per attempt, so the new Consistency and Breadth need at least the minimum data before a point shows.
- [ ] 4.4 Mentor-side views (gradebook, hub learner readiness) read the same function. Confirm they pick up the change with no extra edits.

### Phase 5: Verification
- [ ] 5.1 Web: `npx tsc --noEmit`, lint, unit tests green.
- [ ] 5.2 Mobile: `flutter analyze`, `flutter test`, parity cases match web byte for byte.
- [ ] 5.3 Pick two real learner accounts, compute the score by hand from the PDF formulas, and compare with web and phone.
- [ ] 5.4 Screenshot the Competency Profile on both platforms for the docs; update `04_mobile` captures and the user manual if the card text changed.
- [ ] 5.5 Record the before and after score for existing learners. The 80 threshold and new Consistency will move numbers, so tell users why.

---

## 5. Risks

- **Scores will shift for existing learners.** Raising the mark to 80 lowers Accuracy for anyone scoring 70 to 79. Plan a short in-app note.
- **Breadth depends on a capability that may not exist yet** (per-topic code verification). The interim rule keeps the feature working but is weaker than the PDF's intent. Do not describe it as AST-verified until 3.4 ships.
- **Parity drift.** Two implementations of one formula. The shared test vectors in Phase 0 are the guard; keep them identical on both sides.
- **The 80% mark is provisional.** The PDF says it will be validated by experts. Keep it as a single constant so a change is one line per platform.

---

## 6. Suggested order

1. Phase 0 (tests), then Phase 1 (threshold and weights). Quick, low risk, visible.
2. Phase 2 (Consistency).
3. Phase 3.1 to 3.3, 3.5, 3.6 (Breadth with the interim credit rule), then Phase 4 data checks.
4. Phase 3.4 (concept verification) as its own follow-up once the audit pipeline question is answered.
5. Phase 5 verification and screenshots.
