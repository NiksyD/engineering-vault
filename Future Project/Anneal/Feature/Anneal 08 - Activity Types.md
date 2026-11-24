---
title: "Anneal 08 - Activity Types"
category: Feature Spec
doc-status: Predict the output built; the rest planned
priority: P1
milestone: 8
created: 2026-11-24
updated: 2026-11-24
tags:
  - anneal
  - feature
  - activities
---

# Anneal 08 - Activity Types

Part of [[Anneal - Overview & Roadmap]]. Tracked as Milestone 8 in [[Anneal - Master Build Tracker]].

## Purpose

Today a student can only write a program from a blank editor. That is the hardest thing a first-year is asked to do, and
relying on it alone is frustrating. Easier activities that come first (reading code, fixing code, completing code) build the
same skill with less frustration, and give a teacher a way to mix the difficulty inside one topic.

Nothing here has been tried with a student or a teacher yet. The order below is informed judgement. Ask the pilot teacher which
of these their students would enjoy before building past the first one.

## Principle

**An activity is a kind of challenge, not a separate feature.** It lives in the same bank, is assigned with the same dialog
(class, points, opens, due, attempts, access code, integrity monitoring), is scored in the same table and exported in the same
CSV. A teacher learns nothing new to assign it. What differs per kind is three things only:

| What differs | Why |
| :--- | :--- |
| How it is authored | The agent drafts a different shape for each kind |
| What the student sees | A different screen, with no code editor for some kinds |
| How the answer is checked | A text answer is compared, instead of a program being run |

The rule from the challenge agent still holds: **the model never writes an expected answer.** The code runner produces it, so it
is correct by construction.

## The kinds, in build order

| # | Kind | The student | Checked by | Notes |
| :-: | :--- | :--- | :--- | :--- |
| 1 | Predict the output | Reads a short program and types what it prints | Compare the answer with the runner's real output | Cheapest to build, no editor, works on a phone |
| 2 | Fix the bug | Gets code that fails its tests and makes them pass | Runner, as now | Needs a bug the agent plants and the runner confirms (fails before, passes after the fix) |
| 3 | Put the lines in order | Drags shuffled lines into the right order | Runner runs the ordered code | A new drag screen |
| 4 | Complete the code | Fills in a missing condition or step | Runner on the filled version | Close to a write-a-program challenge with a starter |
| - | Pattern printing | Prints stars, pyramids, tables | Output comparison, as now | **Not a new kind.** It is a write-a-program challenge, so it needs presets only (see [[Anneal 04 - Challenge Bank & Presets]]) |

Items 2 to 4 were already listed as other preset types in the Milestone 4 backlog. Build item 1 first, look at how students
and the teacher use it, then decide the rest.

## Status

**Predict the output is built** (2026-11-24, ADR 0016 in the repo) with the answer-reveal rule, hints, scratch space, drafting by the
agent, and a teacher view. The data sketch below is what was built. It has not been tried with a student or a teacher. Fix the bug,
put the lines in order, complete the code and practice sets are not started.

## Practice sets (later)

A set is an ordered group of activities on one topic, assigned together: a ladder from predict, to complete, to fix, to write.
"Make me a loops practice set" would have the agent draft the whole ladder, each activity verified before students see any of
it. This is the real selling point for a teacher, but it needs at least two kinds to exist first.

## How the first kind could fit the data (a sketch, to confirm when building)

- A `kind` on the challenge, default `write_program`, so everything that exists keeps working unchanged.
- The code the student reads is kept where starter code is kept today. Its expected output is one test, produced by running it.
- The student's answer is stored as the single file a submission already holds (for example `answer.txt`), so no new
  submission table is needed.
- Checking branches on `kind`: a predict answer is compared with the stored output (the comparison already ignores trailing
  spaces and blank lines at the end). Nothing is run at the student's request.
- **The expected output must not reach the student's browser until the teacher's rule allows it** (see the open question on
  revealing). Same discipline as hidden tests today.
- The existing database rules for access (students reach nothing directly, only through functions) apply as they are.

## Predict the output: what would make it enjoyable

The enjoyment comes from feedback and flow, not from decoration (the interface rules forbid emoji and raw colours anyway).

1. **A puzzle, not a quiz.** The code is a large, read-only block with line numbers. The answer box sits right under it, in a
   monospace font, with a placeholder that shows the format ("one number per line").
2. **Optional scratch space.** A collapsible area to write values down while tracing. Not graded. Tracing a loop is the skill,
   and on-paper working is how people do it.
3. **Check, do not judge.** A "Check my answer" button. When right, a calm success panel and the real output. When wrong, a
   side-by-side of "You wrote" and "It printed", with the first differing line marked, and an offer of a hint. No wall of red.
4. **The reveal is the reward.** Seeing what the loop really does is the payoff, so show it clearly after an answer.
5. **Forgiving about format.** Trailing spaces and blank lines at the end are ignored. Say so under the box, so nobody loses a
   point to whitespace.
6. **Low-stakes tries.** Two or three tries by default in practice, then the answer is shown. The teacher can set the attempt
   limit, which the assignment already supports.
7. **Momentum.** In a set, show "2 of 5" and put the next one right after a success. The first item is easy and takes under a
   minute.
8. **Hints on request.** Two levels, written when the agent drafts the activity, so they cost nothing per student and send no
   student data to an AI.
9. **Works on a phone.** No editor to fight, only a text box. Check it at 390 px wide.
10. **Plain, warm wording.** Short sentences, no jargon. "Nice, that matches." Not "Submission graded".
11. **Keyboard and screen readers.** Ctrl or Cmd with Enter checks, as in the workspace. The code block is readable by a screen
    reader.

## Risks and open questions

- **The answer is short and easy to share.** A predict answer is a few characters, so it is weak for graded work. Best as
  practice with low points or none. Per-student variants (see [[Anneal 07 - Integrity Signals (Later)]], part 4) would help later.
- **The explanation is not verified by the runner.** Only the expected output is guaranteed correct. A one-line "why" written by
  the model is not, so the teacher reads it in the draft review before any student sees it, and the screen says so.
- **When is the answer revealed?** After a correct answer, after the attempts run out, or only after the due time? This changes
  how much students can learn from it and how easily it can be shared. Decide with the pilot teacher.
- **Do ungraded activities exist?** Practice with no points may be what first-years want. The assignment needs a points value of
  zero to be allowed, which today it does not.
- **Which kinds does the pilot teacher want?** Unknown. Ask before building past the first.

## Done when (first kind)

A teacher asks for a predict-the-output activity (or picks a preset), reads the draft, and assigns it like any challenge. A
student answers it on a laptop and on a phone, sees the real output, and the score appears in the class table and the export.
The expected output is never in the browser before it may be. Tests cover who can see what, in each role.
