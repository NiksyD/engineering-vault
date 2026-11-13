---
title: "Anneal - Master Build Tracker"
category: Project Management & Execution Tracker
doc-status: Active
priority: P0
created: 2026-11-13
updated: 2026-11-13
tags:
  - anneal
  - roadmap
  - todo
  - engineering-tracker
---

# Anneal - Master Build Tracker

> **For AI agents and developers:** read this tracker at the start of every task and update it at the end. Check a box only after `npx tsc --noEmit`, `npm run lint`, and the tests all pass. If a task turns out to be wrong or unneeded, strike it through and say why. Do not delete it.

**Related notes**
- [[Anneal - Overview & Roadmap]]
- [[Anneal - Architecture & Data Model]]
- [[Anneal - Open Decisions]]

**How to read a milestone**
- **Done when** is the test for the whole milestone. If it is not true, the milestone is not finished, whatever the boxes say.
- **Skills** names the Claude skills in `anneal-ui/.claude/skills` that apply. Load them before starting the work.
- Milestones are in build order. Do not start one before the previous one's **Done when** is true, except where a task says it can run in parallel.

---

## Milestone 0: Foundation and decisions

*Specs: [[Anneal - Open Decisions]], [[Anneal - Architecture & Data Model]]*
*Skills: `environment-setup-guide`, `architecture-decision-records`, `ci-cd-and-automation`, `github-actions-templates`, `secrets-management`, `nextjs-best-practices`, `lint-and-validate`*

**Done when:** a change pushed to the main branch is type-checked, linted, tested, and deployed to a preview address, and that page renders an Astryx component in light and dark mode.

- [ ] **0.1 Settle the blocking decisions**
  - [x] D1 styling decided (Astryx only, 2026-11-13).
  - [x] D2 backend shape, D4 student accounts, D9 hosting decided 2026-11-13. Recorded in [[Anneal - Open Decisions]].
  - [ ] Confirm the name and domain (D10).
- [ ] **0.2 Finish the Astryx setup**
  - [x] Install `@astryxdesign/theme-neutral` and `@astryxdesign/cli` (both 0.7.15, matching core).
  - [x] Run `npx astryx init` so the component index is written into `AGENTS.md` (it also wrote `GEMINI.md`) and `npx astryx theme add neutral` to generate `astryx-themes.ts`.
  - [x] Replace the default `app/globals.css` with the Astryx reset and base stylesheets. The theme's own CSS is imported by the generated `astryx-themes.ts`, so only two imports are needed.
  - [x] Add `app/providers.tsx` with the theme provider and link provider, and wrap the root layout.
  - [x] Trial: app shell (`shell-side-nav`) and workspace (`ide`) scaffolded and screenshotted in headless Chrome with Astryx only. Both rendered correctly. Trial pages deleted.
  - [x] Remove Tailwind and its Turbopack rule.
- [ ] **0.3 Project rules**
  - [x] Write the Anneal section of `anneal-ui/AGENTS.md` (short, always loaded) and the full `docs/standards/coding-standard.md`. `CLAUDE.md` imports `AGENTS.md`.
  - [x] Create `docs/adr/` and record D1 (`0001-astryx-only-styling.md`).
  - [x] Record D2 (`0002-single-app-with-supabase.md`) and D12 (`0003-single-file-submissions-stored-as-files.md`).
  - [ ] Decide whether `.claude/` stays ignored by git. Skills are currently not shared with other machines.
- [ ] **0.4 Tooling**
  - [x] Add Vitest and a first tested module (`lib/runner/compare.ts`, 7 tests).
  - [x] Add scripts: `typecheck`, `lint`, `test`, `format`, `format:check`, and `check` which runs all four.
  - [x] Add Prettier, `noUncheckedIndexedAccess`, and lint rules that block raw HTML elements, the `style` prop, and `console.log`.
  - [x] Add `.github/workflows/ci.yml`: typecheck, lint, format check, test, build on every push and pull request. Not yet run on GitHub because there is no remote yet.
  - [x] Scaffold the foundation: `lib/env.ts` (validated on first use), `lib/supabase/{server,client,admin}.ts`, `lib/runner/types.ts`, `supabase/migrations/`. Feature folders are created when their milestone starts.
- [ ] **0.5 Services**
  - [x] Create the Supabase project (done by the owner in the Supabase dashboard).
  - [x] Install the Supabase CLI and run `supabase init` (`supabase/config.toml`).
  - [x] Project URL, anon key, service role key, and Gemini key are in `.env.local` (verified set, and the auth and database endpoints accept them).
  - [ ] Put the same values in the hosting settings.
  - [x] Run `npx supabase login` and `npx supabase link --project-ref luazktalkqeoeouhxnpl`. Linked 2026-11-13.
  - [x] Add `npm run db:types`, which writes `lib/supabase/database.types.ts`. The three Supabase clients use it. Re-run it after every migration.
  - [x] Add an `.env.example` listing every variable with no values.
  - [ ] Connect the repository to hosting and confirm a preview deploy.
- [ ] **0.6 Replace the starter page**
  - [x] Set the real title and description in `app/layout.tsx`.
  - [x] Replace `app/page.tsx` with an Astryx placeholder page.
  - [ ] Add a link to sign-in once the sign-in page exists (M1).

---

## Milestone 1: Accounts, roles, and app shell

*Specs: [[Anneal - Architecture & Data Model]] sections 3, 5, 6*
*Skills: `auth-implementation-patterns`, `nextjs-app-router-patterns`, `database-design`, `frontend-security-coder`, `ui-states`, `ui-a11y`*

**Done when:** a new teacher and a new student can each sign up, sign in, and land on their own home screen, and neither can open the other's pages by typing the address.

- [ ] **1.1 Sign-in**
  - [ ] Supabase sign-up, sign-in, sign-out, and password reset.
  - [ ] Server-side session reading that works with `cacheComponents`.
  - [ ] Redirect signed-out users to `/sign-in`.
- [ ] **1.2 Profiles and roles**
  - [ ] Migration: `profiles` with `role`, `display_name`, `created_by`.
  - [ ] Role chosen at sign-up. Access rules: a user reads and edits only their own profile.
  - [ ] Test: a student session cannot read another profile.
- [ ] **1.3 App shell**
  - [ ] Teacher navigation: Classes, Bank, Account.
  - [ ] Student navigation: Classes, Account.
  - [ ] Route guards by role on every teacher and student page.
  - [ ] Shared loading, empty, and error components.
- [ ] **1.4 Account page**
  - [ ] Edit display name. Show email as read-only.
  - [ ] Light and dark mode switch.

---

## Milestone 2: Classrooms and enrollment

*Specs: [[Anneal 01 - Classrooms & Enrollment]]*
*Skills: `database-design`, `api-design-principles`, `api-rate-limit-handler`, `backend-security-coder`, `react-patterns`, `form-cro`*

**Done when:** a teacher creates a class, three test students join with the code, the teacher approves two and removes one, and only the two approved students see the class.

- [ ] **2.1 Data**
  - [ ] Migrations: `classes`, `class_members`, with access rules.
  - [ ] Join code generator: short, unambiguous characters, unique.
  - [ ] Tests for every access rule in the architecture note.
- [ ] **2.2 Teacher screens**
  - [ ] Class list with create, rename, and archive.
  - [ ] Class page: student list with pending requests at the top.
  - [ ] Approve, reject, and remove a student.
  - [ ] Show, copy, and regenerate the join code.
- [ ] **2.3 Student screens**
  - [ ] `/join`: enter a code, see the class name, confirm.
  - [ ] Class list showing pending and approved classes.
  - [ ] Rate limit on join attempts.
- [ ] **2.4 Teacher-created accounts** (only if D4 says so)
  - [ ] Add students by name, with generated sign-in details the teacher can print.
- [ ] **2.5 Check the assumptions**
  - [ ] Ask five teachers the questions in [[Anneal - Overview & Roadmap]] section 7 and record the answers.

---

## Milestone 3: Challenge authoring and verification

*Specs: [[Anneal 02 - Challenge Authoring & Verification]], [[Anneal 04 - Challenge Bank & Presets]]*
*Skills: `senior-architect`, `architecture-patterns`, `backend-security-coder`, `threat-modeling-expert`, `test-driven-development`, `testing-patterns`, `frontend-api-integration-patterns`*

**Done when:** a teacher writes a challenge by hand in each supported language, the system reports it as verified, and a challenge with a wrong expected output is reported as failed with the failing test named.

- [ ] **3.1 Decisions**
  - [ ] Close D3 runner, D5 languages, D6 challenge style.
- [ ] **3.2 Runner**
  - [ ] Runner interface from the architecture note, with a Judge0 implementation.
  - [ ] Port the standard input path from CodeMentorAI's `app/api/execute/route.ts`: Java class wrapper, comment blanking, stop after a first-case compile error or time limit.
  - [ ] Port `consoleLog.ts`: status label, error line, runner output clean-up.
  - [ ] Grading function, separate from the runner: compares output with trailing-whitespace tolerance.
  - [ ] Tests using recorded runner responses for each language and each outcome.
- [ ] **3.3 Data**
  - [ ] Migrations: `challenges`, `challenge_versions`, `test_cases`, with access rules.
  - [ ] Saving an edit creates a new version. Old versions are never changed.
- [ ] **3.4 Editor**
  - [ ] Code editor component rebuilt with Astryx, logic carried over from CodeMentorAI's `BrowserIde`.
  - [ ] Challenge form: title, language, statement, starter code, reference solution, time limit.
  - [ ] Test case table: input, expected output, hidden or visible, weight. Add, remove, reorder.
  - [ ] "Fill expected output from reference solution" for a test case.
- [ ] **3.5 Verification**
  - [ ] Check 1: the starter code compiles.
  - [ ] Check 2: the reference solution passes every test within the time limit.
  - [ ] Check 3: at least one visible and one hidden test exist.
  - [ ] Verification report stored on the version and shown in the editor.
  - [ ] A version that fails check 2 cannot be assigned.
- [ ] **3.6 Bank**
  - [ ] Bank list with search, language filter, and tags.
  - [ ] Duplicate and archive a challenge.

---

## Milestone 4: Challenge agent

*Specs: [[Anneal 03 - Challenge Agent]], [[Anneal 04 - Challenge Bank & Presets]]*
*Skills: `senior-architect`, `api-security-best-practices`, `api-rate-limit-handler`, `observability-and-instrumentation`, `ui-states`, `systematic-debugging`. Before writing any Gemini API code, read the current Gemini API documentation, since model names and SDK calls change often.*

**Done when:** from a one-sentence description, the agent produces a challenge that passes verification without the teacher editing it, in at least 8 of 10 trial descriptions per language.

- [ ] **4.1 Decisions**
  - [ ] Choose the Gemini model: compare two models on the same ten descriptions and record first-try pass rate and tokens used.
  - [ ] Choose the SDK: Google's own (`@google/genai`) or the Vercel AI SDK with its Google provider. Record it as an ADR.
  - [ ] Confirm the plan's data terms are acceptable for teacher-pasted notes (see D8).
- [ ] **4.2 Agent core**
  - [ ] Define the draft format the agent must return: the same fields as the editor form.
  - [ ] Agent loop with two tools only: run code, save draft.
  - [ ] Step 1: write the draft. Step 2: run the reference solution. Step 3: repair, at most three rounds.
  - [ ] Step 4: write wrong solutions with common mistakes and confirm each fails a test. Add tests when one survives.
  - [ ] Write the result as a new challenge version with its verification report.
- [ ] **4.3 Limits and records**
  - [ ] Migration: `agent_runs`. Store request, steps, model, and token counts.
  - [ ] Daily limit per teacher, checked before a run starts.
  - [ ] A run that fails or is cancelled leaves no half-saved challenge.
- [ ] **4.4 Screens**
  - [ ] `/bank/new`: description box, language, level, and preset picker.
  - [ ] Live progress: drafting, running, repairing, checking tests.
  - [ ] Result opens in the editor from M3 with the report on top.
  - [ ] "Revise" box: ask the agent to change the current draft.
- [ ] **4.5 Presets**
  - [ ] Migration and seed: 15 to 20 presets across topics and challenge types.
  - [ ] Preset picker grouped by topic.
- [ ] **4.6 Paste lesson notes**
  - [ ] Optional text box for the teacher's notes or outline, passed to the agent as reference material.
  - [ ] Test that instructions hidden in pasted notes do not change what the agent does.

---

## Milestone 5: Assignments and student workspace

*Specs: [[Anneal 05 - Assignments & Student Workspace]]*
*Skills: `frontend-developer`, `react-best-practices`, `ui-states`, `ui-a11y`, `frontend-security-coder`, `api-rate-limit-handler`, `e2e-testing-patterns`*

**Done when:** a teacher assigns a verified challenge to two classes, a student in each solves and submits it, and a student in neither class cannot open it.

- [ ] **5.1 Data**
  - [ ] Migrations: `assignments`, `submissions`, `submission_results`, with access rules.
  - [ ] Server function that returns only the student-safe fields of a challenge version.
  - [ ] Test: hidden test content and the reference solution never appear in any response to a student.
- [ ] **5.2 Assigning**
  - [ ] Assign dialog: pick classes, points, open time, due time, attempt limit.
  - [ ] Assignment list on the class page for teacher and student.
  - [ ] Edit due time and close an assignment.
- [ ] **5.3 Workspace**
  - [ ] Layout: statement on one side, editor and console on the other. Usable at laptop width.
  - [ ] Run: visible tests only. Console shows output, error label, and line number.
  - [ ] Submit: all tests, graded on the server. Hidden tests show pass or fail only.
  - [ ] Code is saved as the student types, and restored on reload.
  - [ ] Clear states: not open yet, open, past due, attempt limit reached.
- [ ] **5.4 Protection**
  - [ ] Rate limit on run and submit per student.
  - [ ] Membership and open-time check on every run and submit.

---

## Milestone 6: Grading and scores

*Specs: [[Anneal 06 - Grading & Scores]]*
*Skills: `database-design`, `react-patterns`, `ui-a11y`, `testing-patterns`*

**Done when:** the teacher opens a class, sees every student's score for every assignment, changes one score with a comment, exports the table, and the file opens correctly in a spreadsheet.

- [ ] **6.1 Scoring**
  - [ ] Close D7: which submission counts.
  - [ ] Score = points × (weight of passed tests ÷ total weight).
  - [ ] Late flag from the due time.
  - [ ] Tests for scoring, including zero tests passed and all tests passed.
- [ ] **6.2 Teacher screens**
  - [ ] Score table: students as rows, assignments as columns, with missing and late marked.
  - [ ] Assignment results page: per-student status, score, and attempts.
  - [ ] Submission viewer: the student's code and each test result.
  - [ ] Override a score with a comment. Migration: `score_overrides`.
- [ ] **6.3 Student screens**
  - [ ] Own scores per class, with the teacher's comment when present.
- [ ] **6.4 Export**
  - [ ] CSV export of the score table.
  - [ ] Column order adjusted to match what teachers said they paste into their class record.

---

## Milestone 7: Pilot hardening

*Skills: `e2e-testing-patterns`, `performance-engineer`, `accessibility-compliance-accessibility-audit`, `cc-skill-security-review`, `threat-modeling-expert`, `observability-and-instrumentation`, `deployment-procedures`, `code-review-checklist`*

**Done when:** one real class completes one real assignment from start to exported scores, and the teacher needs no help from the developer during it.

- [ ] **7.1 Load**
  - [ ] Load test: 40 students submitting within one minute.
  - [ ] Move to a self-hosted runner if the test fails (D3).
- [ ] **7.2 End-to-end tests**
  - [ ] Teacher path: create class, author, verify, assign, review, export.
  - [ ] Student path: join, open, run, submit, see score.
- [ ] **7.3 Review**
  - [ ] Security review of access rules, server functions, and the agent's tools.
  - [ ] Accessibility audit of the workspace and the score table.
  - [ ] Every screen checked for loading, empty, and error states.
- [ ] **7.4 Operations**
  - [ ] Error reporting and a simple view of runner failures and agent spending.
  - [ ] Database backups confirmed.
  - [ ] A written procedure for releasing and for rolling back.
- [ ] **7.5 Pilot**
  - [ ] Close D11: pick the teacher and class.
  - [ ] Short teacher guide, one page.
  - [ ] Run the pilot. Record every point where the teacher got stuck.
  - [ ] Decide what comes next from the pilot notes.

---

## After the pilot

Not scheduled. Order depends on what the pilot shows.

- [ ] Integrity signals. See [[Anneal 07 - Integrity Signals (Later)]].
- [ ] Per-student challenge variants written by the agent.
- [ ] File upload for lesson notes.
- [ ] Function-style challenges.
- [ ] More languages.
- [ ] Sharing challenges within a department.
- [ ] Score sync with Google Classroom or Moodle.
- [ ] School admin accounts.
