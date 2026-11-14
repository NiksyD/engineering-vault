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

## Milestone 3: Challenge authoring and verification (DONE for C, 2026-11-13)

*Specs: [[Anneal 02 - Challenge Authoring & Verification]], [[Anneal 04 - Challenge Bank & Presets]]*
*Skills: `senior-architect`, `architecture-patterns`, `backend-security-coder`, `threat-modeling-expert`, `test-driven-development`, `testing-patterns`, `frontend-api-integration-patterns`*

**Done when:** a teacher writes a challenge by hand in each supported language, the system reports it as verified, and a challenge with a wrong expected output is reported as failed with the failing test named.

- [ ] **3.1 Decisions**
  - [x] D5 languages: C first (decided 2026-11-13).
  - [ ] D6 challenge style: proceeding with program style (standard input and output) as recommended. Confirm with the owner before the editor is built.
  - [ ] D3 runner host: the public Judge0 is fine for development. Load test in M7.
- [x] **3.2 Runner** (C only; `lib/runner/`)
  - [x] Runner interface and one adapter file per language (`languages/c.ts`), so Java and C++ are added without touching the rest. There is no test harness: grading is by standard input and output.
  - [x] Judge0 client (`judge0.ts`, the only file that talks to it): base64 in and out, one retry on a server error, no retry on "busy", clear error type when the runner is down.
  - [x] Result reading (`interpret.ts`): compile errors with the line number, time and memory limits, crashes named in plain words (segmentation fault, division by zero, abort, non-zero exit), output cut at 256 KB, and "the runner had a problem" kept separate from "the student's code is wrong".
  - [x] Run orchestration (`run.ts`): first case alone, skip the rest after a compile error, a time limit, or a runner failure, then a small pool for the other cases. Time limit capped at 10 seconds.
  - [x] Recorded real Judge0 responses for 16 situations (`npm run runner:record`), and 55 tests on them. Three deliberate code breakages were each caught by the tests.
  - [x] Opt-in live test against the real Judge0 (`npm run runner:live`): 6 checks pass.
  - [ ] Grading function that compares output with the expected output: `lib/runner/compare.ts` exists. Wire it into verification (3.5).
  - [ ] Java adapter and C++ adapter, later. The Java wrapper class from CodeMentorAI carries over when that comes.

**What the real Judge0 showed (affects the design)**
- Every crash arrives as one status, "Runtime Error (NZEC)". The cause is only in the exit code: 139 segmentation fault, 136 division by zero, 134 abort, 137 killed. The adapter translates these.
- A program using `sqrt` or `pow` fails to build without `-lm`, so the C adapter always passes it.
- Compiler warnings come back even when the build succeeds, so they can be shown to students.
- The shell wrapper prints a noise line into stderr. The adapter removes it.
- GCC 14 treats a missing `#include` (implicit declaration) as an error, which is stricter than older courses expect. Worth a sentence in the student guide.
- A program that returns a non-zero value from `main` counts as a runtime error. Teach `return 0`.

- [x] **3.3 Data** (`20261113160000_challenges.sql`, applied to the development project)
  - [x] `challenges`, `challenge_versions`, `test_cases` with row-level security. Teachers read only their own. Students have no access.
  - [x] Creating a challenge, saving a new version, and duplicating are database functions that do the whole job in one step (challenge, version, tests, pointer), so a failure leaves nothing half-saved.
  - [x] A saved version cannot change, not even by the server. A trigger enforces it. Only the verification result may be written afterwards, and only by the server.
  - [x] Saving a new version carries the verification result over when the code, tests, and limits are unchanged (a statement-only edit).
  - [x] 49 tests, and three deliberate breakages of the migration were each caught.
  - Language is stored as C, Java, or C++ already, so adding a language needs no migration.
- [x] **3.4 Editor** (rebuilt 2026-11-14 as a tabbed workspace, ADR 0008)
  - [x] Tabs: Statement (with a live Markdown preview), Starter code, Reference solution, Tests, Checks, Settings. Title, status, version, Save, and Verify stay in view. After Verify it goes to Checks. Each test shows Passed or Failed from the last verification, until it is edited.
  - [x] **Student view** switch: what a student would see, built from what is on screen now (statement, starter code, visible tests only). Hidden tests are counted but never shown, and the reference solution is not part of it. Tested.
  - [x] Code editor (CodeMirror 6, ADR 0005), expected outputs filled by running the reference solution, versions, duplicate and archive (in Settings).
  - [ ] Run output is a tab, not a bottom drawer. Decide again for the student workspace in M5.
  - [ ] A version history list is not built.
- [x] **3.5 Verification** (on screen)
  - [x] Verify and "Save and verify" buttons, and a report: each check with a badge, and for a failing reference solution the expected output against what it printed.
  - [x] A reference solution that does not build says so, with the line.
  - [ ] Block assigning a challenge whose reference solution fails (done in M5 when assigning exists).
  - [ ] Wrong-solution check (check 4) comes with the agent in M4.
- [x] **3.6 Bank**
  - [x] List with title, tags, language, test count, and verification status. Active and archived are separate.
  - [x] Duplicate, archive and restore. Search and filters are not built; add them when a bank has more than about 20 challenges.

**Verified:** 26 end-to-end checks (`npm run e2e:challenges`) in headless Chrome against the real database and the real Judge0, plus 49 database tests, 55 runner tests, and 33 verification and schema tests. The end-to-end run covers: expected output filled by running code, verify passing, a wrong solution failing with its test named, a solution that does not build (with line number), fixing it, version numbers 1 to 6, a statement-only edit keeping verification, a test change clearing it, duplicate, archive and restore, another teacher and a student unable to open the challenge. Every bank route is free of Next.js console insights in `next dev`.

**Done when:** a teacher writes a challenge by hand in C and the system reports it as verified, and a challenge with a wrong expected output is reported as failed with the failing test named. Both shown. Other languages follow when their adapters are built.

**Open items**
- [ ] **D6 (program style)** was assumed, as recommended. Confirm with the owner and with teachers.
- [ ] **No rate limit yet on "Fill from reference solution" and Verify.** Each runs code on the shared runner. Add a per-teacher limit before the pilot (M7).
- [ ] **Java and C++ adapters.** Java needs the wrapper class from CodeMentorAI.
- [ ] **Student guide note:** GCC 14 treats a missing `#include` as an error, and returning non-zero from `main` is a runtime error.
- [ ] **Public Judge0** is used for development. Load test and decide on self-hosting in M7.

---

## Milestone 4: Challenge agent

*Specs: [[Anneal 03 - Challenge Agent]], [[Anneal 04 - Challenge Bank & Presets]]*
*Skills: `senior-architect`, `api-security-best-practices`, `api-rate-limit-handler`, `observability-and-instrumentation`, `ui-states`, `systematic-debugging`. Before writing any Gemini API code, read the current Gemini API documentation, since model names and SDK calls change often.*

**Done when:** from a one-sentence description, the agent produces a challenge that passes verification without the teacher editing it, in at least 8 of 10 trial descriptions per language.

- [ ] **4.1 Decisions**
  - [x] Read the current Gemini documentation (2026-11-13). Decisions in ADR 0006: Interactions API, `@google/genai` pinned to an exact version, no tools, structured output only, fixed workflow driven by code.
  - [x] `lib/ai/gemini.ts`: one small interface in front of the SDK, with a timeout, one retry on busy or rate-limit errors, a named fallback model, and separate counts for hidden thinking tokens. 16 tests.
  - [x] Fixed evaluation set (10 descriptions, `features/agent/eval-set.ts`) and a live harness (`npm run agent:eval`). Results are in `docs/agent-evals/`.
  - [~] Choose the Gemini model. First-draft baseline (draft builds and runs on the real runner), measured twice: `gemini-3.5-flash-lite` 10/10, about 6 to 10 s per draft, no hidden thinking tokens. `gemini-4-hydrogen` 10/10, about 16 to 25 s per draft, about 7,000 hidden thinking tokens per ten drafts. `gemini-3.6-flash` could not be judged: on the free tier it was rate limited on 6 of 10 requests and took 1 to 4 minutes on the rest. **Pick (updated 2026-11-14): `gemini-3.5-flash-lite` as the main model and `gemini-3.1-flash-lite` as the pinned fallback. Not hydrogen.** Whole-agent measurement, `agent-2` prompts, 10 descriptions, one run each: both verified 7 and needed review 3, with no verified-but-wrong draft on the 6 descriptions that have a trusted answer. 3.5-flash-lite was faster (61 s against 80 s per challenge) and used no hidden thinking tokens (3.1 used about 3,900 even at the low setting). In 3 of 3.1's drafts every wrong program failed to build, which could not be reproduced afterwards and was not recorded (it is now), so it stays unexplained. The two models have separate free-tier quotas, which is useful in a fallback. Not measured: `gemini-3.5-flash`, because Google serves it from `gemini-3.6-flash`'s quota, which was used up (20 requests a day on the free tier). Hydrogen stays out: no better on any measure we have, slower, spends thinking tokens, and 20 requests a day on the free tier. Whole-agent measurement (2026-11-14, see 4.2): flash-lite verified 7 of 10 with no verified-but-wrong draft on the 6 descriptions that have a trusted answer. `gemini-4-hydrogen` could not be measured: Google's free tier allows only **20 requests a day** for it, and one challenge needs 3 to 5, so as a fallback it is unusable until the key is on a paid plan. This baseline only shows a draft builds and runs, not that its answers are correct, so the pick is final only after the correctness checks (second independent solution, wrong-solution check) are measured.
  - [x] A first measurement mistake was found and fixed: requiring every output to be non-empty marked a correct edge case (no primes below 2 prints nothing) as a failure. The first run's files are kept, labelled `baseline-1-old-rule`.
  - [x] **Pinned exact model names, and the model that answered is recorded.** `lib/ai/models.ts` holds `gemini-3.5-flash-lite` (main) and `gemini-3.1-flash-lite` (fallback), with no aliases. Each run stores the name asked for and the names the responses say answered. Google can serve one name from another model (`gemini-3.5-flash` answered as `gemini-3.6-flash`).
  - [ ] Choose the SDK: Google's own (`@google/genai`) or the Vercel AI SDK with its Google provider. Record it as an ADR.
  - [ ] **Before the pilot: move the Gemini key to a paid plan** (a Google Cloud project with billing). The key is on the free tier today, so only made-up content may be sent. Then set `GEMINI_TIER=paid`.
  - [ ] Ask the owner's advisers about the terms' under-18 clause (see ADR 0006). Teachers are the only people who use the agent, but students use the app.
  - [x] The agent screen shows a warning while `GEMINI_TIER` is `free`, and the paste-your-notes box is disabled on the free tier (to build with the screen).
- [~] **4.2 Agent core** (`features/agent/pipeline.ts`; no screen yet)
  - [x] Draft format: `features/agent/schemas.ts`. The model proposes test INPUTS only. Expected outputs always come from running the reference solution.
  - [x] Fixed workflow run by code, with no tools for the model (decided in ADR 0006, replacing "two tools"): draft, run, check the output is stable, second independent solution written from the statement alone, wrong solutions, final report.
  - [x] Repair loop: at most three rounds in total, shared between a reference that does not run, output that changes between runs, and two solutions that disagree. When the budget is used the run stops and says what it found. Template content is never substituted.
  - [x] Wrong-solution check, redesigned after the first measurement. Each wrong program names a failing input and code checks the claim by running it. A mistake the tests miss but that input exposes becomes a new hidden test. A claim that does not hold is ignored, not counted against the tests. (First version: 3 of 10 verified, mostly noise. Now: 7 of 10.)
  - [x] 31 tests with a fake model and runner (repair, disagreement, weak tests, outages, cancellation). The pipeline was broken nine ways on purpose and the tests caught each.
  - [x] Planted-fault test with the real model (`npm run agent:eval:faults`): a build error, a crash, an endless loop, and wrong logic (`a - b` for "sum") were each repaired in one round, with no wrong expected output. The wrong-logic fault was found by the second solution disagreeing, then fixed by the resolve step.
  - [x] Whole-agent measurement (`npm run agent:eval:pipeline`), `agent-2` prompts, `gemini-3.5-flash-lite`, 10 descriptions: **7 verified, 3 needs review, 0 failed. Of the 6 descriptions with a trusted solution, 5 verified and agree with it, 0 verified and wrong, 1 needs review and agrees.** The 3 reviews were all "only 2 of 4 wrong solutions could be shown to be wrong, too few to judge the tests". About 60 s and 3 calls per challenge, most of it waiting on the public code runner.
  - [ ] **The "done when" bar is 8 of 10 verified without editing. We are at 7 of 10 on one run.** One run of ten is too small to say it is met or missed. Rerun a few times and on a paid plan before trusting the number.
  - [ ] Measure what verification cannot: whether a statement is clear and the starter code is a good starting point. A person has to read a sample.
  - [ ] Write the result as a new challenge version with its verification report (with the run record in 4.3, and the screen in 4.4).
- [~] **4.3 Limits and records** (migration `20261114100000_agent_runs.sql`, applied to the development project)
  - [x] `agent_runs`: request, prompt version, model asked for and models that answered, steps, result, tokens (input, output, hidden thinking), call counts, repair rounds, the challenge it made. Teachers read their own rows only and change nothing. A finished run is frozen by a trigger, so the record can be trusted.
  - [x] Starting a run is one database function (`claim_agent_run`, server only). It checks the daily limit and the one-run rule, then inserts, with claims for one teacher taken one at a time. The database also refuses a second running row for a teacher. 33 database tests, and four deliberate breakages of the migration were each caught.
  - [x] **Daily limit: 20 drafts per teacher in a rolling 24 hours, from `AGENT_DAILY_LIMIT`.** Measured cost per run is about 1,100 input and 1,400 output tokens and 3 to 5 model calls, so 20 is a cautious start, not a tuned number. A refusal says when the limit lifts. Runs that failed because the model or the code runner was down do not count.
  - [x] A run lost when the server stops is closed after 10 minutes, so it cannot block the teacher.
  - [x] A failed or cancelled run leaves no half-saved challenge: the challenge is created last, in one database function, and only for a run worth keeping. A run that passed every check is saved verified. A run that needs review is saved as not verified. Tested against the real database (`npm run agent:runs:live`, 8 tests, no tokens used).
  - [x] Pasted notes are used for the run but never stored. On the free tier they are dropped, and the run says so.
  - [x] `features/agent/execute.ts` (21 tests, five deliberate breakages caught), `run-store.ts`, and the server action `startAgentRun` (narrow answer: never the draft, reference solution, or tests).
  - [x] **Cancelling a run.** A teacher asks through a database function (`request_agent_run_cancel`, 12 tests). The run looks for the request every 2 seconds and stops after the step it is on, with no challenge made. The step in progress finishes first, which can take up to about 25 seconds.
  - [x] **How a long run is delivered.** `startAgentRun` claims the run and answers at once. The run then carries on after the response (`after()` from `next/server`) and writes progress to `agent_runs` after every step. The screen asks for progress every 1.5 seconds, so closing or reloading the page loses nothing. The page sets `maxDuration = 300`. **Only tested locally (`next start`).** Check what the hosting plan allows, and that `after()` work survives there, in Milestone 7.

- [x] **4.4 Screens** (`/bank/new` and `/bank/[id]`). **Rebuilt twice on 2026-11-14: first as a chat (ADR 0007), then as one studio after the owner's screenshots showed layout problems at 2560 px (ADR 0008).**
  - [x] **Empty page** (`ai-chat-landing`): the question, the composer, and the presets in one centred column that lines up at any width. The free-plan note is one quiet line under the composer.
  - [x] **Studio:** with a run or a challenge, the conversation sits on the left in a resizable panel and the challenge on the right. A finished draft opens on the right without leaving the page, and the address becomes `/bank/<id>`, so a reload opens it.
  - [x] **Conversation:** one live line ("Step 4 of about 6" with the step beneath), collapsing to "Checked 6 things in 46 s". The steps open out from it. The result is a card (title, status, tests, "See checks"). Stop button while running. Reloading or another tab picks up a run in progress with its request.
  - [x] **Enter adds a line, Ctrl or Cmd with Enter sends**, so a stray key press cannot spend one of the daily drafts.
  - [x] **Revise** is the same composer once a challenge is open. It makes a full new draft, runs the same checks, and saves it as a new version of the same challenge. A change is refused while there are unsaved edits, so they cannot be silently lost. A fresh challenge with nothing said shows ideas for a change.
  - [x] Free-plan warning, daily limit with the time it lifts, "Write it by hand".
  - [x] `npm run e2e:agent`: **44 checks with the real Gemini and the real code runner** (about 9 requests). New in this version: composer and preset cards line up, the draft opens beside the conversation and the address changes, See checks, Student view, the workspace moves to version 2 by itself, and a reload reopens the challenge. The auth (24), classes (36), and challenges (26) suites pass. Every state is clean in the `next dev` console. No text is under 12 px on any new screen, checked at 1280 px.
  - [ ] **Not tried with a teacher.** Whether this beats a form, whether the Enter rule is understood, and how the wording reads are untested.
  - [ ] **Phone and narrow windows are not designed or checked.** Only 1280 and 2560 px have been looked at. The resizable panel's keyboard use has not been checked.
  - [ ] **Revision quality is unmeasured.** One real request in the end-to-end test. Write an evaluation set (make it harder, change the output format, add an edge case) before relying on it.
  - [ ] The conversation on screen is kept for the visit only. Every run is in `agent_runs`.
- [~] **4.5 Presets**
  - [x] 18 presets in six topics (input and output, conditions, loops, strings, arrays, functions), each saying exactly what to read and print. **A draft list.** The spec says the final topics are confirmed with teachers first.
  - [x] **Decision: presets are code (`features/agent/presets.ts`), not a database table.** The spec does not let teachers save their own, so a migration and seed add nothing.
  - [ ] Only "write a program" is offered. "Complete the code" and "fix the bug" differ in the starter code and need new prompts and checks first.
  - [ ] Confirm the topics with teachers (D4).
- [ ] **4.6 Paste lesson notes**
  - [ ] Optional notes for the agent, passed as reference material. The composer's drawer (`ChatComposerDrawer`) is built for attached context, so notes belong there. Disabled on the free plan, as the server already drops them.
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
