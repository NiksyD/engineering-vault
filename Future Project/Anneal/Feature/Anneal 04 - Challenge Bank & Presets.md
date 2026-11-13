---
title: "Anneal 04 - Challenge Bank & Presets"
category: Feature Spec
doc-status: Draft
priority: P1
milestone: M3, M4
created: 2026-11-13
updated: 2026-11-13
tags:
  - anneal
  - feature
---

# Anneal 04 - Challenge Bank & Presets

Part of [[Anneal - Overview & Roadmap]]. The bank is built in Milestone 3 and presets in Milestone 4 of [[Anneal - Master Build Tracker]].

## Purpose

- **Bank:** the teacher's own store of challenges, so work done this term can be reused next term.
- **Presets:** starting points that remove the blank page without turning Anneal into a library of fixed templates.

## Bank

Every challenge a teacher writes or the agent drafts for them is saved in their bank. The bank is private. No other teacher can see it.

**List view**
- Title, language, tags, verification status, and where it is assigned.
- Search by title. Filter by language, tag, and status.

**Actions**

| Action | Result |
| :--- | :--- |
| Open | Goes to the editor. |
| Duplicate | Makes an independent copy, for adapting a challenge to another section or level. |
| Assign | Opens the assign dialog. See [[Anneal 05 - Assignments & Student Workspace]]. |
| Archive | Hides it from the list. Existing assignments keep working. |

**Tags** are free text chosen by the teacher, for example "week 3" or "loops". There is no fixed list, because each school organises its subject differently.

## Presets

A preset is a topic, a challenge type, and a short piece of guidance for the agent. It is not a finished challenge. Choosing one fills in the request form, and the teacher adds their own context before the agent drafts.

**Example**

| Field | Value |
| :--- | :--- |
| Topic | Loops |
| Type | Write a program |
| Title | Running total |
| Guidance for the agent | Read a count, then that many numbers. Print their sum. Include a test with a count of zero. |

The teacher adds "use prices of canteen items" and gets a challenge about canteen prices. Two teachers using the same preset get different challenges.

**Challenge types at the start**

| Type | What the student does |
| :--- | :--- |
| Write a program | Starts from an almost empty file. |
| Complete the code | Fills in a marked gap in working code. |
| Fix the bug | Starter code runs but gives wrong output. |

All three are program style and are graded the same way. They differ only in what the starter code contains.

**Starting set:** 15 to 20 presets across input and output, conditions, loops, strings, lists or arrays, and functions. The exact list is written in M4 after teachers confirm which topics they teach.

## Why not a library of finished challenges

Finished challenges are what CodeRunner and CodeChum already offer, and answers to widely shared challenges spread among students quickly. A preset gives the teacher the same quick start while the result stays specific to their class.

## Not included

- Sharing a challenge with another teacher or a department.
- Teachers saving their own presets.
- Folders. Tags cover the same need with less to manage.
- Importing challenges from other tools.
