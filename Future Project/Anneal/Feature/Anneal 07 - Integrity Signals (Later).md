---
title: "Anneal 07 - Integrity Signals (Later)"
category: Feature Spec
doc-status: Planned
priority: P2
milestone: After pilot
created: 2026-11-13
updated: 2026-11-13
tags:
  - anneal
  - feature
  - later
---

# Anneal 07 - Integrity Signals (Later)

Part of [[Anneal - Overview & Roadmap]]. Not scheduled. Listed under "After the pilot" in [[Anneal - Master Build Tracker]].

## Purpose

Help a teacher notice work that a student may not have written, such as an answer copied from a classmate or pasted from an AI tool.

This was not possible in CodeMentorAI because it was a public marketplace. In Anneal every submission belongs to a known class with a teacher who can act on it.

## Principle

**Signals, not verdicts.** No browser tool can prove cheating, and tools that claim to detect AI-written text are unreliable. Anneal collects evidence and shows it to the teacher. It never lowers a score or accuses a student by itself. A false accusation harms a student and the teacher's trust in the tool more than a missed case does.

## Planned parts, in build order

| # | Part | What it gives the teacher |
| :-: | :--- | :--- |
| 1 | Edit history and replay | A playback of how the code was written. A solution that appears in one paste looks different from one built over twenty minutes. |
| 2 | Paste and focus events | Size and time of each paste, and when the student left the tab, shown on the same timeline. |
| 3 | Similarity within a class | Pairs of submissions with the same structure, even when names were changed. |
| 4 | Per-student variants | The agent writes a slightly different version of the challenge for each student, so a copied answer fails. |
| 5 | Explain-your-code check | A short question the teacher can assign about the student's own submission. |

A review list per assignment sorts students by how much evidence there is. The teacher opens the replay, decides, and can write a private note.

## One thing to decide before Milestone 5

Edit history can only be replayed if it was recorded while the student worked. If part 1 is likely to be built, the workspace in [[Anneal 05 - Assignments & Student Workspace]] should store edit events from the start, even with no screen to view them. Adding it later means earlier work has no history.

- [ ] Decide before M5 starts whether to record edit events from the first release.

Recording has a cost: more stored data, and a duty to tell students. See the next section.

## Risks

| Risk | Handling |
| :--- | :--- |
| Students share lab computers and one network | Device and network address are never used as signals. |
| Innocent pasting and tab switching | No single signal flags a student. Looking something up is normal. |
| Beginner tasks have few correct answers | Similarity is weighted by the size of the task and never shown alone. |
| Recording activity of students who are minors | Tell students what is recorded. Agree consent and how long data is kept with the school. Delete it after the term. Check local privacy law before building. |
| Exams | A browser cannot be locked down. A teacher present in the room is more effective. Any exam mode must say this plainly. |
