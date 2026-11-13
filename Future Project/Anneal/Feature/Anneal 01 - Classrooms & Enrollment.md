---
title: "Anneal 01 - Classrooms & Enrollment"
category: Feature Spec
doc-status: Draft
priority: P0
milestone: M2
created: 2026-11-13
updated: 2026-11-13
tags:
  - anneal
  - feature
---

# Anneal 01 - Classrooms & Enrollment

Part of [[Anneal - Overview & Roadmap]]. Built in Milestone 2 of [[Anneal - Master Build Tracker]].

## Purpose

A class is where everything else happens. Assignments are given to a class, and scores are read per class. It replaces the public Explore marketplace from CodeMentorAI.

## How it works

**Teacher**
1. Creates a class with a name and an optional section, for example "Programming 1" and "Section B".
2. Gets a join code and shares it in the room or in the school's group chat.
3. Sees join requests at the top of the student list and approves or rejects each one.
4. Can remove a student, regenerate the code, rename the class, or archive it at the end of the term.

**Student**
1. Opens `/join` and types the code.
2. Sees the class name and teacher name and confirms.
3. Sees the class as pending until the teacher approves.

## Rules

- A join code is 6 characters, using letters and digits that are hard to confuse. No `0`, `O`, `1`, `I`, or `L`.
- Regenerating a code makes the old one stop working. Students already in the class are not affected.
- A pending student sees the class name only. No assignments.
- A removed student keeps their past submissions in the teacher's records but loses access.
- An archived class is read-only for everyone. Scores can still be exported.
- A student can ask to join the same class again after being rejected. The teacher sees it as a new request.

## Why approval is required

Join codes get passed around. Without approval, a student from another section ends up in the score table and the teacher has to clean it up. Approval is one tap per student and can be done in bulk with "Approve all".

## Teacher-created accounts

Whether this is needed depends on D4 in [[Anneal - Open Decisions]]. If it is built:
- The teacher types or pastes a list of names.
- The system creates accounts with a generated sign-in name and password.
- The teacher prints or downloads the list to hand out.
- The student is asked to set a new password on first sign-in.

## Edge cases

| Case | Behaviour |
| :--- | :--- |
| Wrong code | A plain "No class found with that code" message. Limited attempts per minute. |
| Student is already a member | Go straight to the class. |
| Teacher account uses a join code | Refused, with a message that teacher accounts cannot join classes. |
| Class is archived | The code no longer works. |
| Two students use the same display name | Both are shown. The teacher can tell them apart by email or sign-in name. |

## Not included

- Co-teachers on one class.
- Moving a student between classes with their scores.
- Importing a class list from another system.
