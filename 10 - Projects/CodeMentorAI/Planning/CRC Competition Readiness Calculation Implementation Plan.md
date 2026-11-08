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

### Phase 0: Lock the spec into tests first (done 2026-11-08)
- [x] 0.1 Web tests from the PDF examples: `codementorai-web/lib/competency/__tests__/cra.test.ts` (run `npx tsx --test lib/competency/__tests__/cra.test.ts`)
- [x] 0.2 Same cases in `codementorai-mobile/test/cra_test.dart` ("PDF worked examples")
- [x] 0.3 Confirmed the tests failed on the old code (mark 70, weight 0.2459, efficiency included the 79% challenge)
- Consistency and Breadth examples are marked todo (web) and skip (mobile) until Phases 2 and 3. Switch them on there.

### Phase 1: Threshold and weights (done 2026-11-08)
- [x] 1.1 `SOLID_RATING_MARK` 70 to 80 (`cra.ts`, `cra.dart`)
- [x] 1.2 Consistency weight 0.2459 to 0.2460 on both; weights sum to exactly 1
- [x] 1.3 Searched for other hardcoded solved marks. None found. The 70 in the profile screens is the readiness tier band (70 to 84%), a different thing, and was left alone.
- [x] 1.4 No UI copy mentioned 70 as the solved mark.
- [x] Mobile parity numbers re-derived from the web calculation on the same scenario (accuracy 50, efficiency 75, breadth 50, consistency 67, index 61).
- [ ] Add the short in-app note that scores can change because the solved mark moved from 70 to 80 (Phase 5.5).

### Phase 2: New Consistency (`100 − MAD`) (done 2026-11-08)
- [x] 2.1 Per assessment `Aᵢ = solved ÷ (solved + missed) × 100`; assessments with no rated problem are skipped and pending problems stay out
- [x] 2.2 `C = 100 − MAD`, MAD = mean absolute deviation from the average accuracy, clamped to 0 to 100, rounded once at the end
- [x] 2.3 Kept the minimum of 3 assessments, first attempt of each assessment (retakes ignored) and the last 10 (D1, D2, D6)
- [x] 2.4 Removed `CONSISTENCY_SUCCESS_SHARE`. Result now exposes `consistencyMeanAccuracy`, `consistencyMad`, `consistencyAssessments` (web) and `consistencyMad`, `consistencyAssessments` (mobile) instead of `consistencySuccesses`
- [x] 2.5 Web profile hint now reads "Your accuracy varies by about N points between M assessments"
- [x] 2.6 Mirrored in `cra.dart`; PDF example (70, 70, 30, 40, 90 gives 80) passes on both, plus steady-vs-swinging and retake/pending cases
- [ ] 2.7 Add the PDF's caveat to the UI help text: Consistency measures variation, not improvement. Mobile still shows the old hint wording ("How steady results are from one assessment to the next"), which is still accurate.
- Parity scenario re-derived: accuracy 50, efficiency 75, breadth 50, consistency 93, index 67.

### Phase 3: New Problem Breadth (`D_h / T_h`) (done 2026-11-08, code check still open)
- [x] 3.1 **Assessed set (T_h):** unique topics on every rated problem across the pooled attempts, solved or not. "Other" never counts. A pending problem (AI rating not in yet) is left out until it arrives, same rule as every other figure.
- [x] 3.2 **Demonstrated set (D_h):** unique topics on solved problems (all tests pass and AI correctness at least 80%). Interim rule, see 3.4.
- [x] 3.3 `PB = D_h / T_h × 100`, rounded once. Null when no rated problem carries a topic tag.
- [ ] 3.4 **Concept verification (new capability).** The PDF also requires the code to contain the tagged construct and use it meaningfully. Until this ships, "solved" counts as "demonstrated". Plan:
  - Add a per-topic verdict to the AI feedback output ("construct present and used: yes/no") or a deterministic source/AST check per language. *To confirm:* what the current AI audit record stores for each submission.
  - Store the per-topic result in the attempt snapshot beside `topics`.
  - Do not describe Breadth as code-verified until this ships.
- [x] 3.5 Removed `BREADTH_TARGET_TOPICS` / `craBreadthTargetTopics`. Web hint now reads "N of M topics demonstrated". Mobile shows no counts yet (it exposes `topicsCovered` / `topicsAssessed`).
- [x] 3.6 Mirrored in `cra.dart`. PDF example (4 of 5 gives 80) passes on both, plus repeat, "other", pending and null cases.
- [x] Only tags from the current list count: attempts saved with old-list tags (before the list was fixed) are ignored on both platforms (`sanitizeTopicTags` in `craData.ts` and `_attachCraProblems`), so their Breadth shows "—" until retaken.
- Parity scenario re-derived and checked by hand: accuracy 50, efficiency 75, breadth 60, consistency 93, index 69.

### Phase 4: Wire-up and data checks (checked 2026-11-08)
- [x] 4.1 The attempt snapshot lists every problem with its tags (web take page and mobile repository both write `topics` per challenge, solved or not), so T_h has what it needs.
- [x] 4.2 **Attempts without a snapshot:** the live database currently has **0** saved attempts (the earlier wipe of Niko's assessments removed the 9 that existed). Nothing to migrate. Breadth builds up as learners take assessments.
- [x] 4.3 Growth chart (`computeCraGrowth`) replays `computeCra` per attempt, so it picks up the new Consistency and Breadth with no change. A point shows once it has the minimum data.
- [x] 4.4 Mentor views (gradebook route, hub learner readiness) read the same `computeCra` through `craData.ts`; type check passes, no edits needed.
- [x] 4.5 **Tagged the existing challenges (2026-11-08).** The AI suggestions were saved to 13 of the 14 challenges (7 in published assessments, 6 drafts). Still untagged: "Algorithmic Challenge" (C, published, in "Java & C Programming Fundamentals Benchmark"), a placeholder with no reference solution that needs real content first. Mentors can change any tag in the studio. Weak fits to revisit: "Secure Vault Encapsulation Auditor" (no encapsulation tag in the list) and the three near-identical "Create a Coding Challenge" drafts.
- [x] `suggest-topics` route now accepts a bare list as well as `{ "topics": [...] }` (the model answered both ways).

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
