---
title: "Anneal 02 - Challenge Authoring & Verification"
category: Feature Spec
doc-status: Draft
priority: P0
milestone: M3
created: 2026-11-13
updated: 2026-11-13
tags:
  - anneal
  - feature
---

# Anneal 02 - Challenge Authoring & Verification

Part of [[Anneal - Overview & Roadmap]]. Built in Milestone 3 of [[Anneal - Master Build Tracker]].

## Purpose

Let a teacher write a challenge by hand and know it works before students see it. This is built before the agent because [[Anneal 03 - Challenge Agent]] fills the same form and uses the same checks.

## What a challenge contains

| Part | Description | Seen by students |
| :--- | :--- | :-: |
| Title | Short name | Yes |
| Language | One language per challenge | Yes |
| Statement | The task, the input format, the output format, and at least one worked example | Yes |
| Starter code | What the editor shows when the student opens the challenge | Yes |
| Reference solution | A correct answer, used to check the tests | No |
| Time limit | How long one test may run | Yes |
| Visible tests | Input and expected output the student can see and run | Yes |
| Hidden tests | Used only when grading | Pass or fail only |
| Weight per test | How much each test counts toward the score | No |

Challenges are program style at the start: the program reads from standard input and prints to standard output. See D6 in [[Anneal - Open Decisions]].

## Verification

Verification runs when the teacher presses "Verify" and automatically before assigning.

| # | Check | If it fails |
| :-: | :--- | :--- |
| 1 | The starter code compiles or parses. | Warning. A teacher may want broken starter code for a "fix the bug" task. |
| 2 | The reference solution passes every test within the time limit. | Blocks assigning. The failing test is named, with expected and actual output side by side. |
| 3 | There is at least one visible and one hidden test. | Warning. |
| 4 | Wrong solutions fail at least one test each. | Warning. Run only when the agent or the teacher supplies wrong solutions. |

The result is stored as a verification report on the challenge version. The report lists each check, its result, and when it ran.

**Why check 2 blocks and the others warn.** A reference solution that fails its own tests means either the answer or the tests are wrong, and students would be graded against an error. The other checks are about quality, and the teacher may have a good reason to proceed.

## Helpers in the editor

- **Fill expected output:** runs the reference solution on a test's input and writes the result as the expected output. This removes the most common hand-typing mistake.
- **Run reference:** runs the reference solution against all tests and shows the same result view students get.
- **Try as student:** opens the challenge in the student workspace with the starter code, without saving a submission.

## Versions

Every save creates a new version. An assignment keeps pointing at the version it was created with. The editor shows a notice when the current version is newer than one that is assigned, with an option to update the assignment. Updating an assignment after students have submitted asks for confirmation and regrades their existing submissions.

## Output comparison

- Trailing spaces on a line and trailing blank lines are ignored.
- Everything else must match exactly, including letter case.
- A stricter or looser comparison per challenge is not part of the first release.

## Edge cases

| Case | Behaviour |
| :--- | :--- |
| Reference solution exceeds the time limit | Check 2 fails with "time limit" on that test. |
| Runner is unavailable | Verification shows "could not run" and keeps the previous report. It does not mark the challenge as failed. |
| Teacher edits only the title or statement | New version, and the previous verification result carries over because the code and tests did not change. |
| Test input is empty | Allowed. Some programs take no input. |
| All weights are zero | Refused on save. |

## Not included

- Function-style challenges.
- Challenges that span several files.
- Checking output with custom code, for tasks with more than one correct answer.
