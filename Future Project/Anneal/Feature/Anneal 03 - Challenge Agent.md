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

## How the agent is built (decided 2026-11-13, see ADR 0006)

The model has **no tools**. Code runs a fixed workflow, and the model only answers in a shape we ask for:

| Part | Who does it |
| :--- | :--- |
| Order of the steps | Code |
| Writing a draft, a repair, or a wrong solution | The model, returning structured data checked against a schema |
| Running any code | Our code runner, never the model |
| Expected outputs | Produced by running the reference solution. The model only proposes test inputs |
| Deciding whether a draft is good enough | The verification check |

Why not give the model tools: it needs none, and a model that cannot take actions cannot be steered into taking one
by text hidden in pasted lesson notes. The notes are passed as marked reference material, and the instructions tell the
model to ignore any instructions inside them.

## The checks, and why each exists (built 2026-11-14)

| Check | What it catches | How it works |
| :--- | :--- | :--- |
| Reference solution runs | A draft that does not build, crashes, or runs forever | Run it on every input. If not, one repair round. |
| Same output every run | A solution that reads an unset variable, so grading would be unfair | Run it twice and compare. |
| An independent solution agrees | An ambiguous statement, or a wrong reference | A second solution is written from the statement alone and must match on every input. If not, the model is shown both outputs and asked to make the statement precise and fix the reference. |
| The tests catch realistic mistakes | Tests too weak to tell a right answer from a common wrong one | Wrong programs are written, each with an input where it fails. Code runs it to confirm. A confirmed mistake the tests miss becomes a new test. |

Expected outputs are never written by the model. They are what the reference solution printed.

Repairs share one budget of three rounds. When it runs out, the run stops, says what it found, and keeps the draft marked unverified.



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
| The model is busy | Tried again, then one named backup model is tried. If that also fails, the run fails and says so. Template content is never substituted. |
| Daily limit reached | The request is refused before any work starts, with the time the limit resets. |
| Description contains a student's personal details | Not sent anywhere beyond the AI request. Teachers are told in the form not to include student names. |

## Not included in the first release

- File upload for notes. Text paste only.
- A different version of the challenge for each student.
- Drafting several challenges in one request.
- Drafting in a language the teacher did not choose.
