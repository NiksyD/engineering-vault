---
title: "Anneal - Open Decisions"
category: Decision Log
doc-status: Active
priority: P0
created: 2026-11-13
updated: 2026-11-13
tags:
  - anneal
  - decisions
---

# Anneal - Open Decisions

Choices that are not settled. Each has a recommendation so work can start, but none is final until its box is checked. When a decision is made, check the box, write the date and the choice, and update [[Anneal - Architecture & Data Model]] if it changes.

Decisions D1 to D5 block Milestone 0 or 1. The rest can wait until the milestone named in each.

---

## D1. Styling: Astryx alone, or Astryx with Tailwind
- [x] Decided 2026-11-13: Astryx alone. See `anneal-ui/docs/adr/0001-astryx-only-styling.md`.

`anneal-ui` currently has both Tailwind 4 and `@astryxdesign/core` installed. Astryx is a component library styled with StyleX and ships its own spacing, tokens, and dark mode.

| Option | For | Against |
| :--- | :--- | :--- |
| Astryx alone | One source of spacing, color, and type. No conflicts between two style systems. | Any layout Astryx does not cover must be written in StyleX or plain CSS. |
| Astryx with Tailwind | Fast one-off layout. Familiar from CodeMentorAI. | Two token systems that can drift apart. Tailwind's reset may clash with Astryx's reset layer. |

**Recommendation:** Astryx alone. Remove Tailwind in M0 after confirming the Astryx layout components cover the app shell and the workspace screen. This has not been tested yet, so M0 includes a short trial.

## D2. Backend shape
- [x] Decided 2026-11-13: one Next.js app plus Supabase, no Go service. See `anneal-ui/docs/adr/0002-single-app-with-supabase.md`.

**Recommendation:** one Next.js app (`anneal-ui`) with server-side route handlers, and a new Supabase project for the database and sign-in. No separate Go service at the start.

Reasons: the CodeMentorAI Go gateway on Render goes to sleep and needs a fallback path, which doubled the data code. One app has one deploy and one place for access rules. A separate service can be split out later if the code runner or the agent needs it.

If this is accepted, consider renaming the folder from `anneal-ui` to `anneal`, since it will hold more than the interface.

## D3. Code runner
- [ ] Decided (needed by M3)

| Option | For | Against |
| :--- | :--- | :--- |
| Public Judge0 instance | Already working in CodeMentorAI. No cost. | Shared with the public and has no uptime promise. A class of 40 submitting together is untested. |
| Self-hosted Judge0 | Full control of limits and capacity. | A server to run, patch, and pay for. |
| Hosted sandbox service | No server to manage. | Cost per run, and every language must be set up. |

**Recommendation:** write the runner behind one small interface so the choice can change without touching the rest of the app. Start on the public instance for development. Run a load test in M7 with 40 students submitting at once, and move to self-hosted Judge0 before the pilot if it fails.

## D4. Student accounts
- [x] Decided 2026-11-13: email sign-up first, tables ready for teacher-created accounts. Still confirm with teachers before M2 ends.

| Option | For | Against |
| :--- | :--- | :--- |
| Student signs up with email | Simple to build. | Fails if students have no email. |
| Teacher creates accounts | Works for any student. Teacher controls the names. | More work for the teacher, and passwords must be handed out. |
| Both | Covers every school. | Two flows to build and test. |

**Recommendation:** build email sign-up first, and design the tables so teacher-created accounts can be added without changes. Confirm with teachers before M2 ends. See the assumptions list in [[Anneal - Overview & Roadmap]].

## D5. Languages at the start
- [ ] Decided (needed by M3)

Every language adds verification work: the agent must write a correct solution in it, and the runner's error output must be handled.

**Recommendation:** Python, Java, and C++. This is a guess at what schools teach most and must be checked with teachers. The other four languages CodeMentorAI supports can be added one at a time later.

## D6. Challenge style
- [ ] Decided (needed by M3)

| Option | Description |
| :--- | :--- |
| Program style | The student's program reads input and prints output. The test compares printed output. |
| Function style | The student writes one function. A hidden harness calls it with arguments. |

**Recommendation:** program style only. It works the same way in every language and needs no harness. The function-style harness in CodeMentorAI is several hundred lines per language and was the source of most runner bugs. Add function style later if teachers ask for it.

## D7. Which submission counts
- [ ] Decided (needed by M6)

**Recommendation:** the best score among submissions made before the due date. Attempts are unlimited by default, and the teacher can set a limit per assignment. Late submissions are accepted, marked late, and left for the teacher to decide.

## D8. AI model and spending limit
- [x] Provider decided 2026-11-13: Gemini API. Model still to choose in M4.

Pick the model in M4 by drafting the same ten challenges on two Gemini models and comparing how many pass verification on the first try. Check three things before the pilot: that the model's function calling is reliable for the two-tool agent loop, the rate limits of the plan in use, and the data terms. Free tiers have historically allowed the provider to use prompts to improve its products. Teachers paste their own lesson notes into requests, so use a paid tier with terms that exclude this before real classes, and confirm that in Google's current terms. Record tokens used per draft from day one, and set a daily limit per teacher before the pilot. The cost per challenge is unknown until this is measured.

## D9. Hosting
- [x] Decided 2026-11-13: Vercel for the app, Supabase for data.

**Recommendation:** Vercel for the app, Supabase for data. Both have free tiers that cover development.

## D10. Name and domain
- [ ] Decided

In a DNS check on 2026-11-13, `anneal.com` had no name servers and `anneal.dev` was taken. A DNS check is only a hint, and a one-word `.com` with no name servers is often held by a reseller. Confirm at a registrar, and search GitHub, npm, and trademark records before using the name in public.

## D11. Pilot class
- [ ] Decided (needed by M7)

One teacher and one class that will use Anneal for real graded or practice work. Finding them early also answers the assumptions list.

## D12. Multi-file challenges
- [x] Decided 2026-11-13

Single file in the first release. OOP fits in one file. Starter code and submissions are stored as a list of files with one entry, so adding files later needs no migration. Revisit after the pilot. See `anneal-ui/docs/adr/0003-single-file-submissions-stored-as-files.md`.

---

## Decided

Move items here when settled, newest first.

| Date | Decision | Choice |
| :--- | :--- | :--- |
| 2026-11-13 | AI provider (D8) | Gemini API. Model chosen in M4. |
| 2026-11-13 | Data access, client state, rate limiting | `supabase-js` with generated types and no ORM, no Zustand by default, Postgres-based rate limiting with no Redis for the pilot. See ADR 0004. |
| 2026-11-13 | Multi-file challenges (D12) | Single file at the start. Code stored as a list of files, one entry for now. See ADR 0003. |
| 2026-11-13 | Hosting (D9) | Vercel and Supabase. |
| 2026-11-13 | Student accounts (D4) | Email sign-up first, teacher-created accounts later. |
| 2026-11-13 | Backend shape (D2) | One Next.js app plus Supabase. See ADR 0002. |
| 2026-11-13 | Styling (D1) | Astryx alone. Tailwind removed after a trial of the app shell and the workspace layout. |
| 2026-11-13 | Full class record | Not built. Score table with export instead. |
| 2026-11-13 | Explore marketplace | Removed. Classes with join codes instead. |
| 2026-11-13 | AI mentor feedback for students | Removed. |
| 2026-11-13 | Integrity features | Deferred until after the pilot. |
| 2026-11-13 | Prebuilt challenges | Not built. Presets feed the agent instead. |
