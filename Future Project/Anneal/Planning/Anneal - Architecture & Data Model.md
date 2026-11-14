---
title: "Anneal - Architecture & Data Model"
category: Architecture
doc-status: Draft
priority: P0
created: 2026-11-13
updated: 2026-11-13
tags:
  - anneal
  - architecture
  - database
---

# Anneal - Architecture & Data Model

This note describes how Anneal is built. It assumes the recommendations in [[Anneal - Open Decisions]] are accepted. If a decision goes another way, update this note in the same change.

Related: [[Anneal - Overview & Roadmap]], [[Anneal - Master Build Tracker]]

---

## 1. Stack

| Layer | Choice | State on 2026-11-13 |
| :--- | :--- | :--- |
| App | Next.js 16.4.6, App Router, React 19.3 | Installed in `anneal-ui` |
| Interface | `@astryxdesign/core` 0.7.15 (StyleX) | Installed. Theme package and CLI are not. |
| Database and sign-in | Supabase (PostgreSQL, row-level security) | Not created |
| Code runner | Judge0, behind a runner interface | Not ported |
| AI | Gemini, Interactions API, `@google/genai` pinned | Key added and working. Model chosen from `docs/agent-evals/`. See ADR 0006. |
| Hosting | Vercel | Not set up |

`anneal-ui/AGENTS.md` warns that this Next.js version differs from older ones. Read the guides in `node_modules/next/dist/docs/` before writing code. `next.config.ts` has `cacheComponents: true`, so any data that depends on the signed-in user must be read inside a `Suspense` boundary or it will fail the build.

## 2. System shape

```text
Browser (teacher or student)
        |
        v
Next.js app on Vercel
  - pages and components (Astryx)
  - server code: route handlers and server actions
        |
        +--> Supabase: database, sign-in, access rules
        +--> Runner interface --> Judge0
        +--> Gemini API (challenge agent only)
```

Three rules hold everywhere:

1. **The browser never calls the runner or the AI directly.** Both go through server code, which checks who is asking.
2. **Hidden tests and reference solutions never reach a student's browser.** They are read only by server code.
3. **Every table has row-level security.** Server code that needs wider access uses the service key, and only on the server.

## 3. Roles

| Role | Can do |
| :--- | :--- |
| Teacher | Everything in their own classes and their own challenge bank. |
| Student | See classes they are approved in, open assigned challenges, run and submit code, see their own results. |

A user has one role, set at sign-up. A person who is both creates two accounts. This keeps the access rules simple.

## 4. Data model

Names are working names. Every table also has `id`, `created_at`, and `updated_at`.

### People and classes

| Table | Key columns | Notes |
| :--- | :--- | :--- |
| `profiles` | `user_id`, `role`, `display_name`, `created_by` | `created_by` is empty for self sign-up and holds the teacher's id for teacher-created accounts. |
| `classes` | `teacher_id`, `name`, `section`, `join_code`, `archived_at` | `join_code` is unique and can be regenerated. |
| `class_members` | `class_id`, `student_id`, `status` | `status` is `pending`, `approved`, or `removed`. |

### Challenges

| Table | Key columns | Notes |
| :--- | :--- | :--- |
| `challenges` | `owner_id`, `title`, `language`, `tags`, `current_version_id`, `archived_at` | One row per challenge in a teacher's bank. |
| `challenge_versions` | `challenge_id`, `number`, `statement`, `starter_files`, `reference_files`, `time_limit_ms`, `verification_status`, `verification_report` | Never edited after it is created. An edit makes a new version. |
| `test_cases` | `version_id`, `position`, `input`, `expected_output`, `is_hidden`, `weight` | Belongs to one version. |
| `presets` | `title`, `topic`, `challenge_type`, `prompt_seed` | Supplied by the system. Read-only for teachers. |

**Why versions exist.** An assignment points at a version, not at the challenge. When a teacher edits a challenge after assigning it, students who already submitted are not affected, and their scores still match the tests they were graded on.

### Assigned work

| Table | Key columns | Notes |
| :--- | :--- | :--- |
| `assignments` | `class_id`, `version_id`, `points`, `opens_at`, `due_at`, `attempt_limit` | One row per class. Assigning to three classes makes three rows. |
| `submissions` | `assignment_id`, `student_id`, `files`, `status`, `score`, `is_late`, `submitted_at` | One row per attempt. |
| `submission_results` | `submission_id`, `test_case_id`, `passed`, `outcome`, `summary`, `error_line`, `actual_output`, `time_ms` | One row per test per attempt. Never returned to a student for a hidden test, except whether it passed. |
| `assignment_drafts` | `assignment_id`, `student_id`, `files`, `updated_at` | The student's saved work in progress. One copy each. Added in M5. |
| `score_overrides` | `assignment_id`, `student_id`, `score`, `comment`, `teacher_id` | The teacher's manual score. Wins over the computed score. |

**Files.** `starter_files`, `reference_files`, and `files` each hold a list of `{path, content}`. The first release always has exactly one entry. Storing a list now means multi-file challenges need no data migration later. See ADR 0003.

### Agent

| Table | Key columns | Notes |
| :--- | :--- | :--- |
| `agent_runs` | `owner_id`, `status`, `request`, `prompt_version`, `model_requested`, `models_answered`, `steps`, `result`, token counts, `challenge_id` | One row per draft request. Starting one goes through `claim_agent_run`, which enforces the daily limit and one run at a time. Finished rows never change. |

## 5. Access rules

Written as row-level security policies. Each one needs a test in M1 to M6.

| Table | Teacher | Student |
| :--- | :--- | :--- |
| `classes` | Own classes: all actions | Read classes where membership is approved |
| `class_members` | Own classes: all actions | Create own pending row. Read own rows. |
| `challenges`, `challenge_versions` | Own: all actions | No direct access |
| `test_cases` | Own: all actions | No direct access |
| `assignments` | Read in own classes. Assign, change, close, remove through functions. | No direct access. Reads a class's list, and opens an assignment after `opens_at`, through functions (ADR 0010). |
| `submissions`, `submission_results`, `assignment_drafts` | Read in own classes (drafts: none) | No direct access. Own work only, through functions that return a hidden test as pass or fail and nothing else. |
| `score_overrides` | Read in own classes. Set or clear through functions. | No direct access. Reads its own score and comment through functions. |
| `agent_runs` | Own rows | None |

A student needs the statement, starter code, and visible tests to work on an assignment. Because the student has no direct access to `challenge_versions` or `test_cases`, server code reads them and returns only the safe fields. Hidden test inputs, expected outputs, and the reference solution are left out.

## 6. Routes

**Teacher**

| Route | Purpose |
| :--- | :--- |
| `/classes` | List of classes |
| `/classes/[classId]` | Students, assignments, and scores for one class |
| `/classes/[classId]/assignments/[assignmentId]` | Results and submissions for one assignment |
| `/bank` | The teacher's challenges |
| `/bank/new` | Start from a preset or a description |
| `/bank/[challengeId]` | Editor and verification report |

**Student**

| Route | Purpose |
| :--- | :--- |
| `/join` | Enter a join code |
| `/classes/[classId]` | Assigned work and own scores |
| `/work/[assignmentId]` | Workspace: statement, editor, run, submit |

**Shared:** `/sign-in`, `/sign-up`, `/account`.

## 7. Runner interface

One function, so the provider can be swapped (see D3 in [[Anneal - Open Decisions]]).

```ts
interface RunRequest {
  language: "c" | "java" | "cpp";
  files: { path: string; content: string }[];
  cases: { id: string; input: string }[];
  timeLimitMs: number;
}

interface CaseResult {
  id: string;
  stdout: string;
  stderr: string;
  compileOutput: string;
  outcome: "ok" | "compile_error" | "runtime_error" | "time_limit";
  timeMs: number;
}

type Run = (req: RunRequest) => Promise<CaseResult[]>;
```

The runner only runs code and reports what happened. Comparing output with the expected answer is done by a separate grading function, so the same runner serves student runs, submissions, and verification.

**Folder layout (decided 2026-11-13).** Grading is program style (standard input and output), so there is no per-language test harness. A language only needs an adapter for the things that really differ: how it compiles, how its errors are read, and what its output needs cleaning.

```text
lib/runner/
  types.ts           RunRequest, CaseResult, Run
  compare.ts         output comparison (language independent)
  run.ts             runs every case, stops after a first compile error or time limit
  judge0.ts          the only file that talks to Judge0
  languages/
    types.ts         LanguageAdapter: Judge0 language id, compile flags, readErrorLine, cleanOutput
    index.ts         registry: one entry per supported language
    c.ts             the C adapter (first)
    c.test.ts        tests against recorded real Judge0 responses
  fixtures/c/        recorded responses: ok, compile error, segfault, time limit, wrong answer
```

Behaviour carried over from CodeMentorAI:
- Stop after the first case when it is a compile error or a time limit, and report the rest as not evaluated.
- Wrap Java so the student's class can have any name.
- Report a time limit as a time limit, with a plain explanation.

## 8. Limits and safety

| Risk | Control |
| :--- | :--- |
| A student floods the runner | Rate limit per user on run and submit. |
| A teacher's agent use runs up cost | Daily limit per teacher, checked before each agent run. Token counts stored in `agent_runs`. |
| Text in a teacher's pasted notes tries to steer the agent | The agent's only tools are the runner and saving a draft. It cannot read other data or reach the network. |
| A second submission arrives while the first is grading | Each attempt is its own row. The score is computed from stored results, not from the latest request. |
| A student reads hidden tests in the network tab | Hidden test content is never sent. Only pass or fail is returned. |
| A student submits to an assignment in another class | Server code checks approved membership on every run and submit. |

## 9. Rules for building

- A task is done only when `npx tsc --noEmit`, `npm run lint`, and the tests pass.
- Every new table ships with its access rules and a test for them.
- Every screen handles four states: loading, empty, error, and filled.
- Text is at least 12px, contrast meets WCAG AA, and every action works from the keyboard.
- Record any structural choice as a short decision record in `anneal-ui/docs/adr/`.
