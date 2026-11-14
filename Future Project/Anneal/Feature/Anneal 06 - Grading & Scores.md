---
title: "Anneal 06 - Grading & Scores"
category: Feature Spec
doc-status: Draft
priority: P0
milestone: M6
created: 2026-11-13
updated: 2026-11-16
tags:
  - anneal
  - feature
---
[]()
# Anneal 06 - Grading & Scores

Part of [[Anneal - Overview & Roadmap]]. Built in Milestone 6 of [[Anneal - Master Build Tracker]].

## Purpose

Remove the work of running and checking each submission, and give the teacher scores in a form they can move into their school's class record.

## How a score is calculated

```text
score = points × (total weight of passed tests ÷ total weight of all tests)
```

Example: an assignment is worth 100 points and has five tests with equal weight. A submission that passes four gets 80.

The score that counts for a student is the best one among their submissions before the due time. Decided as D7 in [[Anneal - Open Decisions]]. Ties go to the earliest submission. Whether a submission is late is worked out from the due time as it is now, so extending a due date takes the lateness off work that now falls inside it.

If a student has only late submissions, the best late score is shown, marked late. The teacher decides whether to accept it, reduce it, or set it to zero with an override.

## Score table

One table per class.

- Rows are students, sorted by name.
- Columns are assignments, sorted by due time.
- Each cell shows the score, with a mark for late, missing, or changed by the teacher.
- The last column is the total of points earned over points possible.

Selecting a cell opens that student's submissions for that assignment.

## Reviewing one assignment

| View | Shows |
| :--- | :--- |
| Summary | How many students submitted, how many passed every test, and which tests failed most often. |
| Per student | Status, score, number of attempts, and time of the counted submission. |
| Submission | The student's code, read-only, with each test's result including hidden tests. |

The "tests failed most often" figure tells the teacher what to reteach, and can also reveal a test that is unfair.

## Override

The teacher can replace any computed score with their own and add a comment. The override:
- Is shown to the student with the comment.
- Is kept if the student submits again. The teacher is shown a notice that a newer submission exists.
- Can be cleared, which returns the cell to the computed score.

## Export

- A CSV file of the score table: student name, sign-in name or email, then one column per assignment, then the total.
- Late and missing are an option: a status column after each assignment, off by default so the score columns paste cleanly. Missing work is an empty cell and counts as zero in the total.
- Removed students are left out unless asked for.
- A name that starts with `=`, `+`, `-`, or `@` is written as plain text, so it cannot run as a formula.
- The file opens correctly in Excel and Google Sheets, including names with accented letters.

## What Anneal does not calculate

- Final grades for a term.
- Weighted categories such as written work and performance tasks.
- Transmuted grades.
- Attendance.

These rules differ between schools, and the school's official class record already applies them. Anneal supplies the raw scores.

## Edge cases

| Case | Behaviour |
| :--- | :--- |
| Student never submitted | Cell shows "missing". Counts as zero in the total. |
| Student joined after the due time | Cell shows "missing". The teacher can extend the due time or override. |
| Assignment removed | Its column is removed from the table and the export. |
| Challenge edited after assigning | Nothing changes. The assignment keeps the version it was made from. Assign again to use new tests. |
| Student removed from the class | Row is hidden from the table. A filter shows removed students for the record. |

## Not included

- Similarity checks between submissions.
- Rubrics for code style or readability.
- Sending scores to another system automatically.
