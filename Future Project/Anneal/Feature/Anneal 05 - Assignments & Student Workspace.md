---
title: "Anneal 05 - Assignments & Student Workspace"
category: Feature Spec
doc-status: Draft
priority: P0
milestone: M5
created: 2026-11-13
updated: 2026-11-13
tags:
  - anneal
  - feature
---

# Anneal 05 - Assignments & Student Workspace

Part of [[Anneal - Overview & Roadmap]]. Built in Milestone 5 of [[Anneal - Master Build Tracker]].

## Purpose

Get a verified challenge in front of students, and give them a place to solve and submit it.

## Assigning

From the bank or the editor, the teacher presses "Assign" and sets:

| Setting | Default | Notes |
| :--- | :--- | :--- |
| Classes | None | One or more. Each class gets its own assignment. |
| Points | 100 | The maximum score. |
| Opens | Now | Students cannot see it before this time. |
| Due | None | Required before saving. |
| Attempt limit | Unlimited | A number, if the teacher wants one. |

Only a challenge that passes verification check 2 can be assigned. See [[Anneal 02 - Challenge Authoring & Verification]].

After assigning, the teacher can change the due time, close the assignment early, or remove it. Removing an assignment that has submissions asks for confirmation.

## Student workspace

**Layout**
- One side: the statement, with visible tests listed below it.
- Other side: the code editor, with a console and test results underneath.
- On a narrow screen the two sides become tabs.

**Run**
- Runs the student's code against the visible tests only.
- Shows each test's input, expected output, and actual output.
- On an error, shows what kind it was and the line number, in plain words.
- Does not count as an attempt and is not stored.

**Submit**
- Runs every test on the server, visible and hidden.
- Shows each visible test in full and each hidden test as passed or failed, with no input or expected output.
- Shows the score for this attempt and the best score so far.
- Counts as an attempt.

**Saving**
- Code is saved as the student types, and restored when they come back, on any device.
- The starter code can be restored with "Reset to starter", after a confirmation.

## Assignment states for a student

| State | What the student sees |
| :--- | :--- |
| Not open yet | Listed with its opening time. Cannot be opened. |
| Open | Full workspace. |
| Past due | Can still submit. Each submission is marked late. A notice says so before they submit. |
| Attempt limit reached | Can read their code and results. Run still works. Submit is disabled with the reason. |
| Closed by teacher | Read-only. |

Late submissions are accepted and marked, and the teacher decides what to do with them. See [[Anneal 06 - Grading & Scores]]. Blocking late work entirely creates more requests to the teacher than it saves.

## Rules checked on the server

Every run and submit checks, in this order:
1. The student is signed in.
2. The student is an approved member of the assignment's class.
3. The assignment is open and not closed.
4. The student is under the rate limit.
5. For submit only, the student is under the attempt limit.

These are never left to the page alone, because a page can be bypassed.

## Edge cases

| Case | Behaviour |
| :--- | :--- |
| Submit pressed twice quickly | The second press is ignored while the first is grading. |
| Connection drops during a submit | The submission is graded on the server anyway and appears on reload. |
| Runner is unavailable | The attempt is not counted. The student sees a message to try again. |
| Program never finishes | Stopped at the time limit and reported as a time limit, with a hint to check for a loop that never ends. |
| Student is removed from the class during work | The next run or submit is refused. |
| Teacher updates the challenge version after submissions exist | Existing submissions are regraded against the new tests. |

## Not included

- An AI helper or hints for students.
- Working in pairs or groups.
- Timed exams and exam supervision. See [[Anneal 07 - Integrity Signals (Later)]].
- Comments from the teacher on specific lines of code.
