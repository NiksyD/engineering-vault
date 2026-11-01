---
title: "CodeMentorAI Module Creation: Intent Gatekeeper To-Do & Build Tracker"
category: Project Management & Execution Tracker
status: Completed
priority: P0
created: 2026-11-01
updated: 2026-11-01
tags:
  - roadmap
  - todo
  - engineering-tracker
  - codementorai
  - module-creation
---

# CodeMentorAI Module Creation: Intent Gatekeeper To-Do & Build Tracker

> **For AI Agents & Developers:** Consult and update this tracker at the start and completion of every task. A task may only be marked `[x]` after `npx tsc --noEmit` and `npm run lint` (0 errors) pass in `codementorai-web`, plus the unit tests for that task. Run `graphify update .` after code changes. Obey `AGENTS.md` (no "curriculum", "course", "syllabus"; no "Capstone").

**Problem:** `/mentor/new` fires the full 5-stage pipeline and saves a Supabase draft for ANY non-empty prompt. `"hi"` becomes `"JavaScript Mastery: Hi"` with 9 activities.

**Reference behavior:** Google Stitch (conversational reply + starter chips for greetings/nonsense) and PasaCPA (`LocalAiRationalizerBridge`: domain-grounded triage, deterministic fallback, quick-prompt chips, hallucination guard).

**Key Files:**
- `app/mentor/agents/intentInference.ts`
- `app/mentor/components/agentic/IntentCapture.tsx`
- `app/mentor/new/page.tsx`
- `app/mentor/agents/orchestrator.ts`
- `app/api/mentor/generate/route.ts`
- `app/mentor/agents/titleSynthesizer.ts`

---

## ✅ Milestone 1: Pre-Flight Intent Classifier (Client, Deterministic) (COMPLETED)
*Zero-latency, zero-cost triage before any job starts. Mirrors PasaCPA's deterministic Tier 3.*

- [x] **1.1 `classifyMentorPrompt()` in `intentInference.ts`**
  - [x] Return type `PromptVerdict = "valid" | "greeting_or_meta" | "gibberish" | "too_vague" | "off_domain"` plus `reason` and `confidence`.
  - [x] `greeting_or_meta`: `hi`, `hello`, `hey`, `help`, `what can you do`, `who are you`, `thanks`.
  - [x] `gibberish`: keyboard mash (low vowel ratio, repeated chars, `asdf`, `qwerty`), digits/symbols only, no dictionary-like tokens.
  - [x] `too_vague`: under 3 meaningful words AND no language/CS-concept signal (e.g. `test`, `ok`, `module`).
  - [x] `off_domain`: no programming signal and matches non-coding topics (cooking, essays, travel).
  - [x] `valid`: detected language, a CS concept lexicon hit (loops, recursion, pointers, API, sorting, async, OOP…), or an attached document.
- [x] **1.2 CS concept lexicon**
  - [x] Add `CS_CONCEPT_SIGNALS` (topics, data structures, algorithms, paradigms, tooling).
  - [x] Reuse existing `LANGUAGE_PATTERNS`, `BEGINNER/INTERMEDIATE/ADVANCED_SIGNALS` as positive evidence.
- [x] **1.3 Unit tests (`intentInference.test.ts`)**
  - [x] Table-driven: `hi`, `HELLO!!`, `asdfghjkl`, `12345`, `test`, `how to cook adobo` → rejected.
  - [x] `C pointers for beginners`, `Python asyncio`, `Binary search trees in Java`, `Design a module on recursion` → valid.
  - [x] No false positives on short valid prompts (`C loops`, `SQL joins`).

---

## ✅ Milestone 2: Stitch-Style Conversational Assistant Card (UI) (COMPLETED)
*Specs: Stitch screenshot (assistant reply bubble + `↪` starter chips).*

- [x] **2.1 Gate `handleSubmit` in `IntentCapture.tsx`**
  - [x] Run `classifyMentorPrompt()` before `onGenerate`. Non-`valid` verdicts MUST NOT call `onGenerate`, start a job, or create a draft.
  - [x] Bypass the gate when `attachedFileContent` exists.
- [x] **2.2 `AssistantReplyCard` component (`components/agentic/AssistantReplyCard.tsx`)**
  - [x] Verdict-specific copy (greeting, gibberish, too vague, off-domain).
  - [x] Greeting copy: "Hi! I'm your Module Architect. I can design guided practice, coding challenges, and automated test suites. What topic should we build?"
  - [x] Animate in/out (`animate-in fade-in`), respect reduced motion, `aria-live="polite"`.
  - [x] Dismiss when the mentor edits the prompt.
- [x] **2.3 Starter chips (`↪` icon, Stitch style)**
  - [x] 3 clickable chips per verdict; reuse/extend `PROMPT_SUGGESTIONS`.
  - [x] Click fills the textarea, sets language and audience, and auto-submits with full validated intent.
  - [x] Chips match the selected target language when one is locked (JavaScript, Python, C, C++, Java, C#, PHP).
- [x] **2.4 Submit-button state**
  - [x] Keep `canGenerate` for empty input only; the card handles the rest (no silent disabled state).
- [x] **2.5 Copy audit (AGENTS.md)**
  - [x] No "curriculum/course/syllabus"; use "module", "topic", "practice", "challenge".

---

## ✅ Milestone 3: Server-Side Refusal & Clarification Schema (LLM Guard) (COMPLETED)
*Second line of defense for prompts that slip past client heuristics.*

- [x] **3.1 Server re-validation in `api/mentor/generate/route.ts`**
  - [x] Run the same `classifyMentorPrompt()` server-side (shared module) and return `422` `{ isActionable:false, clarificationMessage, suggestedPrompts }` BEFORE any Gemini call (saves quota).
- [x] **3.2 LLM-level `isActionable` escape hatch**
  - [x] Extend the system prompt + JSON schema: allow `{ "isActionable": false, "clarificationMessage": "...", "suggestedPrompts": [..] }`.
  - [x] Remove the "returning fewer milestones is a FATAL ERROR" pressure for non-actionable input.
  - [x] Validate response shape; fall back to deterministic message if the model returns malformed refusal.
- [x] **3.3 Remove hardcoded API key fallback**
  - [x] Removed literal `AIzaSy…` default in `route.ts`; requires `GEMINI_API_KEY` from environment, returning clean 503 if unconfigured.
- [x] **3.4 Orchestrator handling (`orchestrator.ts`)**
  - [x] On `isActionable:false`, DO NOT run `runLocalFallbackPipeline`; surface the clarification to the UI.
  - [x] Distinguish "refused" (422 or `isActionable:false`) from "quota/error" (only the latter engages the offline fallback).
  - [x] Extended `AgentPipelineResult` with `isActionable?: boolean` and `clarification?: ClarificationGuidance`.

---

## ✅ Milestone 4: Prevent Junk Drafts & Fabricated Titles (COMPLETED)
*Specs: `new/page.tsx`, `titleSynthesizer.ts`, `useModuleGenerationStore`.*

- [x] **4.1 Guard `handleGenerate` in `new/page.tsx` & Stitch-Style Guidance UX**
  - [x] Return early on clarification refusal: dismissed store job cleanly, no `POST /api/mentor/drafts`, no `setModules` state mutation, no notification item, and no false "Module created" toast.
  - [x] Improvised UX: Replaced clunky Sonner toast with inline `AssistantReplyCard` inside `IntentCapture.tsx`. Displays server clarification message and interactive `↪` topic suggestion chips directly beneath the prompt cockpit.
  - [x] Lazy Agent Log Activation: Prevented premature opening of `FloatingGenerationDock` (`startJob`). The heavy multi-agent progress log no longer mounts while intent is still in pre-flight/analysis; it activates only after actionable intent is verified and sandbox verification begins.
  - [x] Tightened Heuristic Guard: Off-domain topics (politics, celebrities, sports, food) and conversational questions (`who`, `what`, `where`, etc.) are rejected even when a programming language is mentioned (e.g., "who is barrack obama in java?"), unless grounded by an explicit computer science concept.
  - [x] Auto-dismisses when user types, clicks a suggested chip, or taps the close button.
  - [x] Scroll Overflow Fix: Removed flexbox `justify-center` from the `overflow-y-auto` scroll container in `new/page.tsx` and used `my-auto` on `<IntentCapture>`. Prevents the "What module shall we design today?" heading from being pushed into unscrollable negative space when content expands.
- [x] **4.2 `titleSynthesizer.ts` hardening**
  - [x] Checked `isMeaninglessSubject` (greetings, gibberish, noise tokens). Does NOT fabricate synthetic titles like `"JavaScript Mastery: Hi"` or `"Python Foundations: Asdf"`. Defaults to genuine foundational paradigms (`"JavaScript Foundations: Logic, Decisions & Flow"`).
  - [x] Added unit test verifying `"hi"` does not fabricate junk title labels.
- [x] **4.5 Assessment Creation Intent Gatekeeping & Security Alignment (`/mentor/assessment/create`)**
  - [x] Pre-flight intent guard in `AssessmentIntentCapture.tsx`: Intercepts greetings ("hi"), gibberish, and off-domain topics ("who is barrack obama") before generating assessments.
  - [x] Google Stitch inline guidance: Integrated `AssistantReplyCard` beneath the prompt cockpit, offering instant topic clarification and interactive starter chips across all supported languages.
  - [x] Title Synthesizer integration: Replaced naive string slicing with `synthesizeAiTitle` in `create/page.tsx` to generate publication-grade benchmark titles (preventing junk titles like "Hi Benchmark" or "Who is barrack obama Benchmark").
  - [x] Scroll Overflow Bug Fix: Removed flexbox `justify-center` from the outer scroll container in `create/page.tsx` and applied `my-auto` in `AssessmentIntentCapture.tsx` so headers never clip into unscrollable negative space.
- [x] **4.4 In-Editor Copilot Intent Gatekeeping & Security Alignment**
  - [x] Removed hardcoded API key fallback in `/api/mentor/copilot/route.ts` (strictly requires `GEMINI_API_KEY` from environment, returns clean 503).
  - [x] Rate limiting: Added sliding-window limiter (20 requests/min per client IP on `/api/mentor/copilot`).
  - [x] Pre-flight intent guard (`classifyCopilotPrompt`): Intercepts greetings ("hi"), gibberish, and off-domain prompts ("who is barrack obama") on the client before calling the API.
  - [x] First-class clarification handling: Instead of throwing a generic error toast, opens the in-editor `# Agent Log` with an amber `Guidance` badge and instructional refinement suggestions.
  - [x] System prompt refusal clause: Allows LLM to return `action: "clarification"` if the prompt is nonsensical rather than hallucinating code modifications onto the selected activity.
- [x] **4.3 Cleanup script / one-off migration awareness**
  - [x] Verified draft creation pathway is strictly protected from saving unvetted conversational entries.

---

## ✅ Milestone 5: Quality, Telemetry & Regression Safety (COMPLETED)

- [x] **5.1 Telemetry events**
  - [x] Tracked `mentor_prompt_rejected` (verdict, reason, length), `mentor_prompt_accepted`, and `mentor_starter_chip_clicked` (chip label, stack, audience).
- [x] **5.2 Rate limiting:**
  - [x] Implemented in-memory sliding window rate limiter in `lib/rateLimiter.ts` (6 requests/min per mentor IP on `/api/mentor/generate`).
- [x] **5.3 Automated tests:**
  - [x] 7/7 test suites passing in `app/mentor/agents/__tests__/intentInference.test.ts`.
- [x] **5.4 Adversarial prompt matrix verified:**
  - [x] Tested table-driven prompts across greetings, gibberish, brief/vague tokens, off-domain topics, valid CS concepts, and attached document bypass.
- [x] **5.5 Docs & Knowledge Graph:**
  - [x] Synchronized knowledge graph via `graphify update .` (2,022 nodes, 7,645 edges).

---

## 🔭 Future (Post-MVP)

- [ ] Optional lightweight LLM intent classifier (flash-lite, <1s) for ambiguous prompts that pass heuristics.
- [ ] Multi-turn clarification ("Which language? What level?") in the card rather than a single refusal.
- [ ] Prompt-injection hardening for `documentContext` (strip instructions from attached documents).
- [ ] Mobile parity: not applicable (module creation is mentor/web only per `AGENTS.md`).

