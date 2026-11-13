---
title: "Anneal 03 - Challenge Agent"
category: Feature Spec
doc-status: Draft
priority: P0
milestone: M4
created: 2026-11-13
updated: 2026-11-13
tags:
  - anneal
  - feature
  - ai
---

# Anneal 03 - Challenge Agent

Part of [[Anneal - Overview & Roadmap]]. Built in Milestone 4 of [[Anneal - Master Build Tracker]].

## Purpose

Turn a teacher's short description into a complete, verified challenge. This is the main reason a teacher would choose Anneal.

## What the teacher gives

| Input        | Required | Example                                                                       |
| :----------- | :------: | :---------------------------------------------------------------------------- |
| Description  |   Yes    | "Loops practice. Students compute the total cost of a list of canteen items." |
| Language     |   Yes    | C        |
| Level        |   Yes    | Beginner, intermediate, or advanced                                           |
| Preset       |    No    | "Loops: running total". See [[Anneal 04 - Challenge Bank & Presets]].         |
| Lesson notes |    No    | Pasted text from the teacher's own notes or outline                           |

## What the agent does

```text
1. Draft     Write the statement, starter code, reference solution, and tests.
2. Run       Run the reference solution against the tests.
3. Repair    If a test fails, decide whether the solution or the test is wrong,
             fix it, and run again. At most three rounds.
4. Stress    Write a few wrong solutions with mistakes students commonly make.
             Run each. If one passes every test, add a test that catches it.
5. Report    Save the challenge with a verification report.
```

Each step is shown to the teacher as it happens, so a wait of a minute or so has visible progress.

Step 4 is what a teacher rarely has time to do by hand. Typical wrong solutions are an off-by-one loop, a missing edge case for empty input, integer division where decimal division is needed, and wrong output formatting.

## What the agent is allowed to do

The agent has two tools and nothing else:

| Tool | What it does |
| :--- | :--- |
| Run code | Sends code and inputs to the runner and returns the results. |
| Save draft | Writes the challenge fields for this request. |

It cannot read other challenges, student data, or the network. This limit is the main protection against text in pasted notes that tries to give the agent instructions. Pasted notes are passed as reference material, marked as such, and never as instructions.

## Result

The draft opens in the editor from [[Anneal 02 - Challenge Authoring & Verification]] with the verification report at the top. The teacher can:
- Edit any field directly.
- Use "Revise" to ask for a change in words, for example "make the numbers larger" or "add a test for an empty list". The agent repeats steps 2 to 5 on the changed draft.
- Discard it.

Nothing is assigned automatically. The teacher always reviews first.

## Limits

- A daily limit per teacher on agent runs. The number is set in M4 once the cost per run is measured.
- One run at a time per teacher.
- A run stops after three repair rounds. If the draft still fails, it opens in the editor marked as failed, with the failing test shown, so the teacher can fix it by hand.
- Every run is recorded in `agent_runs` with the model, the steps, and the tokens used.

## Quality target

In at least 8 of 10 trial descriptions per language, the draft passes verification with no teacher edits. The ten trial descriptions per language are written once in M4 and kept as a fixed test set, so model or prompt changes can be compared against the same set.

Passing verification means the challenge is internally consistent. It does not mean the challenge is good teaching. The teacher's review is what covers that, which is why the result always opens in the editor.

## Edge cases

| Case | Behaviour |
| :--- | :--- |
| Description is too vague, for example "something about arrays" | The agent proceeds with reasonable choices and lists them at the top of the draft. It does not block on questions. |
| Description asks for something program style cannot test, for example a graphical program | The agent says so and offers the closest task that can be tested. |
| Teacher closes the page during a run | The run finishes on the server and the draft appears in the bank. |
| Runner is unavailable | The run stops with a clear message. No draft is saved. |
| Daily limit reached | The request is refused before any work starts, with the time the limit resets. |
| Description contains a student's personal details | Not sent anywhere beyond the AI request. Teachers are told in the form not to include student names. |

## Not included in the first release

- File upload for notes. Text paste only.
- A different version of the challenge for each student.
- Drafting several challenges in one request.
- Drafting in a language the teacher did not choose.
