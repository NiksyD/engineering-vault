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

## Milestone 1: Accounts, roles, and app shell (DONE 2026-11-13, with open items below)

*Specs: [[Anneal - Architecture & Data Model]] sections 3, 5, 6*
*Skills: `auth-implementation-patterns`, `nextjs-app-router-patterns`, `database-design`, `frontend-security-coder`, `ui-states`, `ui-a11y`*

**Done when:** a new teacher and a new student can each sign up, sign in, and land on their own home screen, and neither can open the other's pages by typing the address.

**Verified:** 14 database access-rule tests (`npm run db:test`) and 24 end-to-end checks in headless Chrome (`npm run e2e:auth`) pass against the development project. The end-to-end run created two temporary users, signed each in through the real form, and deleted them. A student typing `/bank` is sent to `/classes`.

- [x] **1.1 Sign-in**
  - [x] Sign-up, sign-in, sign-out, and password reset as server actions (`features/auth/actions.ts`), with the login-card template adapted for the pages.
  - [x] Session read on the server with `getClaims`, cached per request, behind `Suspense` (works with `cacheComponents`).
  - [x] `proxy.ts` refreshes the session cookie and redirects signed-out visitors to `/sign-in?next=...`. The `next` address is checked so it cannot leave the site.
  - [x] Same message for a wrong password and an unknown email. Password reset always gives the same answer.
- [x] **1.2 Profiles and roles**
  - [x] Migration `20261113120000_profiles.sql`: `profiles` with `role` and `display_name`, row-level security, a trigger that creates the profile at sign-up, and privileges so a user can change only `display_name`. Applied to the development project.
  - [x] Tests: a student sees only their own profile, cannot change their role, cannot insert or delete, and signed-out visitors cannot read. A bad or missing role at sign-up becomes `student`.
- [x] **1.3 App shell**
  - [x] Frame with a top bar (account menu, sign out) and a side navigation, per role: teacher has Classes, Bank, Account; student has Classes, Account.
  - [x] Role guards on pages (`requireUser`, `requireRole`) and a first-pass redirect in the proxy.
  - [x] Loading (skeleton), empty (`EmptyState`), and error (`app/error.tsx`) states.
- [x] **1.4 Account page**
  - [x] Edit display name, email shown read-only, light, dark, and system switch saved in the browser.

**Open items (not verified yet)**
- [x] **Sign-up through the real form and the confirmation email.** Observed in the database: the owner signed up as a teacher with a real address, the profile was created with the right role and name, and the email was confirmed.
- [ ] **Password reset email.** The forgot-password and reset-password flow has not been run end to end. Try it once by hand.
- [ ] **Supabase redirect URLs.** (The confirmation link worked, so `localhost` is probably already allowed; still add the Vercel preview and production addresses later.) In the dashboard under Authentication, URL Configuration, add `http://localhost:3000/**` (and the Vercel preview and production addresses later). Without this the email links will not return to the app.
- [ ] **Decide teacher sign-up.** Anyone can choose "Teacher" when signing up. A student who does so can create classes but cannot see anyone else's data. Decide before the pilot whether teachers need approval or a school code.
- [ ] **Theme flash.** A saved dark choice shows light for a moment on first load when the system is light. Fix with a small inline script before paint, or accept it.
- [ ] Confirm the display name length and sign-up wording with teachers.

---

## Milestone 2: Classrooms and enrollment (DONE 2026-11-13, with open items below)

*Specs: [[Anneal 01 - Classrooms & Enrollment]]*
*Skills: `database-design`, `api-design-principles`, `api-rate-limit-handler`, `backend-security-coder`, `react-patterns`, `form-cro`*

**Done when:** a teacher creates a class, three test students join with the code, the teacher approves two and removes one, and only the two approved students see the class.

**Verified:** 39 class access-rule tests plus 14 profile tests (`npm run db:test`), and 36 end-to-end checks (`npm run e2e:classes`) in headless Chrome against the development project. The end-to-end run covers the done-when scenario and more: a rejected student asking again, a removed student unable to rejoin, a new join code, rename, archive and restore, and other teachers or students opening a class by its address (they get "Page not found"). Every new route is free of Next.js console insights in `next dev`.

- [x] **2.1 Data** (`20261113140000_classes.sql`, `20261113150000_private_schema_for_server.sql`)
  - [x] `classes` and `class_members` with row-level security. Students never read `classes` directly, so they cannot list classes or see a join code.
  - [x] Join code: six characters, no 0, O, 1, I, or L, unique, generated by the database. Teachers cannot choose or edit it.
  - [x] Joining, listing a student's classes, listing a class's members, and regenerating a code are database functions that check the caller first.
  - [x] Rate limit on join attempts: 10 a minute per student, kept in a Postgres table.
- [x] **2.2 Teacher screens**: class list (active and archived), create, class page with join code, copy, new code, requests with approve, reject, approve all, students with remove, removed students with restore, rename, archive and restore.
- [x] **2.3 Student screens**: `/join` in two steps (find the class, confirm teacher and name, then ask), class list with waiting and joined states. A waiting student cannot open the class.
- [ ] **2.4 Teacher-created accounts**: not built. Decide with the teachers' answers to the email question (D4).
- [ ] **2.5 Check the assumptions**: ask five teachers the questions in [[Anneal - Overview & Roadmap]] section 7.

**Notes and open items**
- [ ] **Join codes are shared secrets.** Anyone with the code can ask to join, and the teacher approves each request. Confirm with teachers that the approval step is enough.
- [ ] **Class page for students** shows "No assignments yet" until Milestone 5.
- [ ] **Student names are visible to the class's teacher with their email.** Tell students this on the join screen or in the pilot consent notes.
- Server reads of the database call `connection()` first, because the database client checks the session against the current time, which Next.js does not allow while prerendering. See the coding standard.

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

## Launch cutover: development project becomes production

The current Supabase project (`luazktalkqeoeouhxnpl`) is the development database until the app is ready for real classes. At launch it becomes production and a new project becomes development. Decided 2026-11-13.

- [ ] **Before launch, now:** check the project's region in the dashboard (Project Settings). A region cannot be changed later. If it is far from the schools, stop and create the production project in the right region instead of converting this one.
- [ ] Every change to the database goes through `supabase/migrations/`, never the dashboard. Do not edit tables by hand.
- [ ] Run `npx supabase db diff --remote` and confirm there is no difference between the project and the migration files.
- [ ] Delete every test user in the auth system. Delete all test rows. Keep the tables.
- [ ] Review auth settings and email templates that carry over: email confirmation on, custom email sending set up, sign-up rules.
- [ ] Rotate the anon key, the service role key, and the database password. Update `.env.local` and the hosting settings.
- [ ] Move the project to a paid plan and confirm backups are on. Check the plan terms on pausing and backups.
- [ ] Create a new project for development, run `npx supabase link` and `npx supabase db push --remote` against it, and point `.env.local` at it. If it builds cleanly from the migration files, the files are complete.
- [ ] Point the hosting production settings at this project and the preview settings at the new development project.

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
