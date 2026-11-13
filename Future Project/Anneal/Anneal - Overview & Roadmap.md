---
title: "Anneal - Overview & Roadmap"
category: Product Overview
doc-status: Active
priority: P0
created: 2026-11-13
updated: 2026-11-13
tags:
  - anneal
  - roadmap
  - overview
---

# Anneal - Overview & Roadmap

Anneal is a school-based tool that helps teachers create, assign, and grade coding challenges. A teacher describes the activity in plain words, an AI agent drafts the full challenge, and the system proves the challenge works before any student sees it.

This note is the entry point. Read it first, then follow the links.

**Planning notes**
- [[Anneal - Master Build Tracker]]: the milestone checklist. Update it at the start and end of every task.
- [[Anneal - Architecture & Data Model]]: stack, tables, routes, security rules.
- [[Anneal - Open Decisions]]: choices that are not settled yet, each with a recommendation.
- Coding standard: `anneal-ui/docs/standards/coding-standard.md`. The short version is in `anneal-ui/AGENTS.md`.

**Feature specs**
- [[Anneal 01 - Classrooms & Enrollment]]
- [[Anneal 02 - Challenge Authoring & Verification]]
- [[Anneal 03 - Challenge Agent]]
- [[Anneal 04 - Challenge Bank & Presets]]
- [[Anneal 05 - Assignments & Student Workspace]]
- [[Anneal 06 - Grading & Scores]]
- [[Anneal 07 - Integrity Signals (Later)]]

---

## 1. The problem

Teachers of programming classes lose time in three places:

| Pain point | What it looks like today | Status |
| :--- | :--- | :--- |
| Creating challenges | Writing the problem, a starter file, a correct solution, and test cases by hand. A wrong test case is often found during the lab. | Proven |
| Grading | Opening and running 40 submissions one by one. | Proven |
| Cheating | Students paste answers from a classmate or an AI tool. | Real, but built later |

Existing tools such as CodeRunner and CodeChum rely on prebuilt templates. Anneal's difference is that every challenge is written for the teacher's own lesson and is fully editable.

## 2. Who it is for

- **Teacher:** creates classes, authors challenges, assigns them, reviews scores. The teacher is the primary user and the product is designed around their time.
- **Student:** joins a class with a code, solves assigned challenges in the browser, sees test results.

There is no public marketplace and no AI mentor feedback for students. Both existed in CodeMentorAI and are removed on purpose.

## 3. What makes Anneal different

**A challenge is verified before it can be assigned.** The system runs the reference solution against every test, then runs deliberately wrong solutions to confirm the tests catch them. The teacher gets a short report of what was checked. This is the reason for the name: annealing is heating a material so its weak points show up, then letting it settle into a stronger form.

## 4. The core flow

1. The teacher creates a class and gets a join code.
2. Students join with the code. The teacher approves them.
3. The teacher picks a preset or types a description. The agent drafts the challenge.
4. The system verifies the draft. The teacher edits anything they want.
5. The teacher assigns the challenge to one or more classes with a due date.
6. Students solve it in the browser. Tests grade each submission.
7. The teacher reviews the score table, overrides where needed, and exports it.

## 5. Scope of the first release

**In scope**
- Teacher and student accounts, with roles.
- Classes, join codes, teacher approval.
- Manual challenge editor with verification.
- Challenge agent that fills the same editor.
- Private challenge bank per teacher, plus a small set of system presets.
- Assignments with due dates, across several classes.
- Student workspace: editor, run, submit, results.
- Score table with partial credit, teacher override, and CSV export.

**Out of scope for the first release**
- A full class record (grading periods, weighted categories, transmutation). Schools already have an official one. Anneal exports scores into it.
- A full LMS (announcements, attendance, lesson materials).
- Integrity features. See [[Anneal 07 - Integrity Signals (Later)]].
- Sharing challenges between teachers.
- A mobile app.
- School or department admin accounts.

## 6. Milestones

Details and checklists are in [[Anneal - Master Build Tracker]].

| # | Milestone | Result |
| :-: | :--- | :--- |
| M0 | Foundation and decisions | The project builds, deploys, and has its rules written down. |
| M1 | Accounts, roles, app shell | A teacher and a student can sign in and see the right screens. |
| M2 | Classrooms and enrollment | A teacher runs a class with approved students. |
| M3 | Authoring and verification | A teacher writes a challenge by hand and the system proves it works. |
| M4 | Challenge agent | The agent drafts a verified challenge from a description. |
| M5 | Assignments and student workspace | Students receive, solve, and submit work. |
| M6 | Grading and scores | The teacher sees, adjusts, and exports scores. |
| M7 | Pilot hardening | One real class uses it for real work. |

M3 comes before M4 on purpose. The agent writes into the same editor and uses the same verification as a teacher working by hand, so both must exist first.

## 7. Assumptions to check with teachers

These are guesses. Each one changes the design if it is wrong. Ask at least five teachers before M2 is finished.

- [ ] Do most students have an email address they can sign up with?
- [ ] Which programming languages are taught, and in which year levels?
- [ ] How large is a typical class, and do all students submit at the same time?
- [ ] Do students work on school lab computers, their own laptops, or phones?
- [ ] How reliable is the internet connection in the lab?
- [ ] What does the school's official class record look like, and what file format can be pasted or imported into it?
- [ ] Of creating, grading, and cheating, which costs the most time?

## 8. What carries over from CodeMentorAI

| Carries over | Notes |
| :--- | :--- |
| Browser code editor | Rebuilt with the Astryx design system. The logic is reused, the styling is not. |
| Code execution through Judge0 | Only the standard input and output path. See [[Anneal - Open Decisions]]. |
| Console output handling | Error labels, line numbers, time limit handling. |
| Java class wrapper | Lets a student name their class anything. |

| Does not carry over | Reason |
| :--- | :--- |
| Explore marketplace | Anneal is class-based. |
| AI mentor feedback for learners | Removed from the product. |
| Hubs, streaks, pretest baseline | Not part of the teacher's problem. |
| Go backend | See [[Anneal - Open Decisions]]. |
