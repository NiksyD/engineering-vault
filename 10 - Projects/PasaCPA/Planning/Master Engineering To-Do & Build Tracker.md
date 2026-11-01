---
title: "PasaCPA Master Engineering To-Do & Build Tracker"
category: Project Management & Execution Tracker
status: Active
priority: P0
created: 2026-10-31
updated: 2026-10-31
tags:
  - roadmap
  - todo
  - engineering-tracker
  - pasacpa
---

# PasaCPA Master Engineering To-Do & Build Tracker

> **For AI Agents & Developers:** Always consult and update this tracker at the start and completion of every engineering task. A task may only be marked `[x]` after both `flutter analyze` (0 issues) and `flutter test` (100% passing) are verified.

**Related Core Specs:**
- [[Systems & AI Architecture Blueprint]]
- [[Frontend Design & UI Architecture]]
- [[00 - Feature Map & Roadmap]]
- [[00 - Master CPALE Syllabus & Table of Specifications]]

---

## ✅ Milestone 1: Foundation, Design System & Core Exam UI (COMPLETED)
*Specs: [[Frontend Design & UI Architecture]], [[Frontend Implementation Plan]], [[01 - Zero-Latency Mock Exam Engine]], [[06 - Offline Accounting Scratchpad & Basic Calculator]]*

- [x] **1.1 Project Standards & Agent Memory Anchoring**
  - [x] Create `GEMINI.md` workspace coding standards (Ponytail + Superpowers + Deterministic Math).
  - [x] Create `.agents/rules/obsidian_vault.md` pointing to the Obsidian Vault source of truth.
- [x] **1.2 Utility Neo-Brutalist Theme System (`lib/core/theme/`)**
  - [x] Implement `AppColors` (`#FAF9F6` canvas, `#00E676` Volt Green, `#FF3D00` Radical Orange, `#1A1C1A` ink).
  - [x] Implement `AppTypography` (Anton display, Space Mono tabular numerals, Geist body).
  - [x] Implement `AppTheme` (0px border radius, 2px solid borders, hard offset shadows).
  - [x] Build & test `BrutalistButton` and `BrutalistCard`.
- [x] **1.3 MCQ Option Card & Distractor Strikethrough (`lib/core/theme/widgets/`)**
  - [x] Build `McqOptionCard` with long-press distractor elimination strikethrough and collision guard.
- [x] **1.4 Persistent 4-Tab Navigation Shell (`lib/features/navigation/`)**
  - [x] Build `MainNavigationScreen` and `BrutalistBottomNavBar` (EXAM, STUDY HUB, CARDS, ANALYTICS).
- [x] **1.5 Exam Launchpad & Session Configuration (`lib/features/exam/`)**
  - [x] Build `ExamLaunchpadScreen` with crash-recovery Resume Banner, 6 CPALE Subject selector (70 MCQs vs 100 MCQs for RFBT), and Mode selector (Timed Board Sim, Untimed Practice, Weak-Topic Drill).
- [x] **1.6 Zero-Latency Exam Workspace & Grouped Caselet Viewer (`lib/features/exam/`)**
  - [x] Build `AccountingLedgerTable` with tabular Space Mono alignment and double-ruled accounting totals.
  - [x] Build `CaseletViewer` with independent scroll isolation and sub-question chips.
  - [x] Build `QuestionNavigatorSheet` (1–70 / 1–100 grid with answered, flagged, and L1/L2/L3 triage badges).
  - [x] Assemble `ExamWorkspaceScreen` with docked bottom action strip.
- [x] **1.7 Deterministic Casio JW-200SC Calculator & T-Account Scratchpad (`lib/core/calculator/`, `lib/features/scratchpad/`)**
  - [x] Implement pure Dart `CasioCalculatorEngine` (`GT` Grand Total, `÷ ÷ =` and `× × =` K-Constant registers, `M+/M-/MRC`).
  - [x] Build `ScratchpadSheet` with auto-summing two-column Debit/Credit T-Account ledger and embedded Casio keypad.

---

## ✅ Milestone 2: Official PRC BOA Syllabus & TOS Knowledge Base (COMPLETED)
*Specs: [[00 - Master CPALE Syllabus & Table of Specifications]]*

- [x] **2.1 Parse PRC BOA Resolution No. 2022-30 (Effective Oct 2022)**
  - [x] Extract and structure all 1,122 hierarchical syllabus items across all 6 subjects.
  - [x] Create `00 - Master CPALE Syllabus & Table of Specifications.md` (3-Day schedule, GWA >= 75% & >= 60% Conditioned rules).
  - [x] Create `01 - Financial Accounting and Reporting (FAR) Syllabus.md` (157 items).
  - [x] Create `02 - Advanced Financial Accounting and Reporting (AFAR) Syllabus.md` (168 items).
  - [x] Create `03 - Management Services (MS) Syllabus.md` (106 items).
  - [x] Create `04 - Auditing (AUD) Syllabus.md` (158 items).
  - [x] Create `05 - Regulatory Framework for Business Transactions (RFBT) Syllabus.md` (427 items).
  - [x] Create `06 - Taxation (TAX) Syllabus.md` (106 items).

---

## ✅ Milestone 3: Local-First Data Layer & Seed Question Bank (COMPLETED)
*Specs: [[Systems & AI Architecture Blueprint]], [[01 - Zero-Latency Mock Exam Engine]]*

- [x] **3.1 Pure Dart Local-First Database & WAL Engine (`lib/core/database/`)**
  - [x] Define `SyllabusNode` entity and `kOfficialBoaSyllabusNodes` index (mapping all 1,122 BOA syllabus nodes with parent/child DAG pointers).
  - [x] Define `ExamCaselet` and `ExamQuestion` entities (supporting `dependsOnQuestionId` and `distractorTrapMap` diagnostics).
  - [x] Define `ExamSession` and `AttemptEvent` WAL store (synchronous `<2ms` state persistence for crash recovery, option strikethrough bitmasks, and dwell telemetry).
- [x] **3.2 Seed Data Compiler & Repository Wiring (`lib/features/exam/data/`)**
  - [x] Compile the 1,122 parsed syllabus items into `lib/core/database/syllabus_seed_data.dart`.
  - [x] Create curated seed caselets and standalone MCQs across all 6 subjects (`FAR`, `AFAR`, `MS`, `AUD`, `RFBT`, `TAX`) with `distractorTrapMap` annotations in `lib/core/database/question_seed_data.dart`.
  - [x] Wire `ExamLaunchpadScreen` and `ExamWorkspaceScreen` to read/write live sessions from `ExamRepository` (including dynamic 100-item count for `RFBT` vs 70-item count for other subjects).
  - [x] Write unit and widget tests verifying the 1,122-node DAG, cascading caselet navigation, distractor trap feedback, and WAL persistence (24/24 tests passing).

---

## ✅ Milestone 4: Neuro-Symbolic AI Rationalizer & Local AI Bridge (COMPLETED)
*Specs: [[02 - AI-Powered Rationalizer & ELI5]], [[Systems & AI Architecture Blueprint]]*

- [x] **4.1 Stage 1: Pure Dart Symbolic Diagnostic & Cascading Error Solver (`lib/core/calculator/diagnostic_solver.dart`)**
  - [x] Build the deterministic evaluator that inspects `distractorTrapMap` for the student's chosen wrong option.
  - [x] Build the **Cascading Error Auditor** for grouped caselets (re-evaluating downstream formulas with the student's upstream answer to detect valid downstream methods).
  - [x] Output verified `DiagnosticFactSheet` models with a post-generation regex currency number verifier (`verifyNoHallucinatedCurrency`).
- [x] **4.2 Stage 3: Tiered On-Device AI Bridge (`lib/core/ai/local_ai_rationalizer_bridge.dart`)**
  - [x] Define 3-tier routing (`Tier 1: Android AICore / Gemini Nano`, `Tier 2: MediaPipe Gemma-2-2B-IT`, `Tier 3: Deterministic AST Fallback`) with `<4GB` hardware RAM safety check.
  - [x] Implement automatic fallback to deterministic proof if an LLM emits an unverified `₱` currency figure.
  - [x] Implement memoization cache keyed by `(questionId, selectedOptionIndex, upstreamSelectedOptionIndex)`.
- [x] **4.3 Rationalizer Dual-Tab UI (`lib/features/exam/presentation/widgets/ai_rationalizer_sheet.dart`)**
  - [x] Build the Neo-Brutalist `"⚡ Ask On-Device AI"` panel with **STEP-BY-STEP DERIVATION** vs. **ELI5 BREAKDOWN** tabs, active inference tier badge, `0ms CACHE` indicator, and cascading error alert banner.

---

## ✅ Milestone 5: Offline Codal & Tax Matrix Quick-Vault (COMPLETED)
*Specs: [[09 - Offline Codal & Tax Matrix Quick-Vault]]*

- [x] **5.1 Offline Codal & Tax Matrix Search Engine (`lib/features/codal_vault/data/codal_vault_repository.dart`)**
  - [x] Define `QuickReferenceEntry` and seed high-yield matrices: CREATE Corporate/MSME Tax (`RA 11534`), EOPT Act 2024 Invoicing & Taxpayer Tiers (`RA 11976`), De Minimis/8% GIT/CGT (`NIRC`), RCCP Voting Quorums (`RA 11232`), AMLA & BP 22 Thresholds, PFRS 16/PAS 36, PFRS 3/10, PSA 700/705 Audit Opinion Matrix, and MS CVP/DOL formulas.
  - [x] Connect Stage 2 of `DiagnosticSolver` and `LocalAiRationalizerBridge` to pull grounded statutory citations and excerpts from `CodalVaultRepository`.
- [x] **5.2 Study Hub & Quick-Vault UI (`lib/features/codal_vault/presentation/screens/study_hub_screen.dart`)**
  - [x] Build the **STUDY HUB** tab combining instant `<5ms` Codal Search (with one-tap threshold copy chips) and the interactive **1,122-item PRC BOA Syllabus Checklist** across all 6 subjects.
  - [x] Wire `StudyHubScreen` into Tab 1 (`STUDY HUB`) of `MainNavigationScreen` (31/31 tests passing).

---

## ✅ Milestone 6: Adaptive Flashcard Synthesizer & FSRS Scheduler (COMPLETED)
*Specs: [[04 - Adaptive Flashcard Synthesizer & Spaced Repetition]]*

- [x] **6.1 Pure Dart FSRS / SM-2 Spaced Repetition Engine (`lib/core/srs/fsrs_scheduler.dart`)**
  - [x] Implement deterministic stability ($S$), difficulty ($D$), ease factor, and Ebbinghaus retrievability ($R = e^{-t/S}$) calculations across `RecallGrade` (`forgot +10m`, `hard +1d`, `good +3d`, `mastered +7d`).
- [x] **6.2 Adaptive Weak-Spot Synthesizer & Flashcard Deck UI (`lib/features/flashcards/`)**
  - [x] Build `FlashcardRepository.synthesizeFromWeakAttempts()` scanning missed exam attempts in `LocalExamDatabase` and generating targeted cards grounded with `CodalVaultRepository` citations.
  - [x] Build `FlashcardsScreen` and wire into Tab 2 (`CARDS`) of `MainNavigationScreen` (34/34 tests passing).

---

## ✅ Milestone 7: Local Analytics & BOA Readiness Predictor (COMPLETED)
*Specs: [[05 - Local Analytics & Board Readiness Predictor]]*

- [x] **7.1 Deterministic BOA Grading & IRT Engine (`lib/features/analytics/domain/`)**
  - [x] Implement General Weighted Average (GWA $\ge 75\%$) and Per-Subject Floor ($\ge 60\%$) evaluator (`BoaReadinessPredictor`).
  - [x] Implement the **"⚠️ CONDITIONED WARNING"** detector (triggers when GWA $\ge 75\%$ but 1 or 2 subjects $< 60\%$, and `FAILED` when $< 75\%$ or $\ge 3$ subjects $< 60\%$).
  - [x] Implement Triage Efficiency Audit (`L1` $<45\text{s}$, `L2` $90–120\text{s}$, `L3` $<210\text{s}$ and $>3.5\text{m}$ time-trap double-loss counter) and Raw vs. BOA IRT Scaled Rating toggle.
- [x] **7.2 Analytics Dashboard Screen (`lib/features/analytics/presentation/`)**
  - [x] Build the **ANALYTICS** tab (`AnalyticsDashboardScreen`) displaying the 6-Subject PRC BOA Readiness Matrix, Conditioned Status Alarm, Time-Trap Triage Audit, and Ebbinghaus Retention badges, wired into Tab 3 of `MainNavigationScreen` (39/39 tests passing).

---

## ✅ Milestone 8: 3-Day Board Gauntlet, Case Mutator & Scantron Mode (COMPLETED)
*Specs: [[10 - 3-Day Board Gauntlet & BOA Grading Simulator]], [[03 - On-Device Case Study Generator]]*

- [x] **8.1 3-Day Board Gauntlet Simulator & Scantron Shading Sheet**
  - [x] Implement multi-session schedule & fatigue analyzer (`BoardGauntletSimulator`) replicating the actual 3-day PRC schedule (Day 1: MAS + AUD; Day 2: TAX + RFBT; Day 3: FAR + AFAR) with cognitive fatigue tracking (Morning 8–11 AM vs Afternoon 1–4 PM accuracy drop-off).
  - [x] Implement **Scantron Shading Transfer Drill Mode** (`ScantronSheet`) with A/B/C/D OMR bubble shading, batch transfer from scratch, and transcription mismatch detection.
- [x] **8.2 Parametric Case Study Mutator (`lib/features/exam/domain/case_mutator.dart`)**
  - [x] Build pure Dart parametric number & entity mutator (`CaseMutator`) so repeated practice on a caselet or MCQ generates fresh figures (`isSynthetic: true`, `parentQuestionId`) and recalculates the answer key deterministically, preventing rote answer memorization (45/45 tests passing).

---

## ✅ Milestone 9: Supabase Delta-Sync & Offline Document OCR (COMPLETED)
*Specs: [[07 - Delta-Based Background Sync Engine]], [[08 - Offline Document Ingestion & AI Note Synthesizer]]*

- [x] **9.1 Delta-Based Background Sync Engine (`lib/core/database/sync/delta_sync_engine.dart`)**
  - [x] Implement downstream delta patch puller (`syncVersion > localSyncVersion`) for tax law errata and question updates.
  - [x] Implement upstream idempotent WAL batch uploader (`txId` UUIDv4) with a **"Strict Offline Privacy Mode"** toggle (`🔒 STRICT OFFLINE: ON`).
- [x] **9.2 Offline Handout OCR & Note Synthesizer (`lib/core/ai/offline_ocr_note_synthesizer.dart`)**
  - [x] Implement the 2-stage local OCR handout pipeline (Stage 1: boilerplate stripping & 500-word chunking; Stage 2: deterministic `₱` threshold & rate extraction + structured `QuickReferenceEntry` & `Flashcard` synthesis) wired into `StudyHubScreen` (49/49 tests passing).

---

## ✅ Milestone 10: Production Hardening, Honest Cold-Start & Local Persistence (COMPLETED)
*Audit Directive: Senior CPALE Reviewer & Board Exam Specialist Reality Check*

- [x] **10.1 Honest Zero-Data Cold-Start & Disclaimers (`lib/features/analytics/`)**
  - [x] Refactor `AnalyticsRepository` with `includeSyntheticCohortBaseline` flag and live-vs-benchmark toggle so the app doesn't present fake 58% RFBT alarm or fabricated 84% accuracy to new students.
  - [x] Implement honest cold-start state: evaluate `isColdStart` when `< 50` attempts recorded; show `⚡ INSUFFICIENT DATA (COLD START)` verdict hero card when zero attempts are present.
  - [x] Display an explicit statistical confidence interval / minimum sample size banner (`"⚡ COLD START STATE: X / 50 ITEMS RECORDED — PRC BOA readiness projections require at least 50 live question attempts across subjects to reach statistical significance"`).
  - [x] Clarify the BOA IRT standardizing toggle with an explicit illustrative statutory disclaimer (`"ESTIMATED PEDAGOGICAL MODEL: The PRC Board of Accountancy does not publish its confidential raw-to-scaled equating algorithms. This IRT equating curve is an illustrative pedagogical simulation"`).
- [x] **10.2 True Local Persistence Layer (`lib/core/database/persistence/`)**
  - [x] Implement `LocalStorageService` to serialize and persist WAL interaction records (`AttemptEvent`), exam sessions (`ExamSession` with options, option elimination bitmasks, flags, and triage tags) offline across app restarts via `shared_preferences`.
  - [x] Save and auto-hydrate syllabus checklist selections (`checkedSyllabusNodeIds`) in `StudyHubScreen` so student progress across the 1,122 BOA syllabus nodes survives app restarts and process kills.
  - [x] Auto-hydrate `LocalExamDatabase` on application boot in `main.dart` with automatic synchronization on session saves and WAL event pushes (54/54 tests passing).

---

## ✅ Milestone 11: Question Bank Bulk Ingestion Engine & Authentic Bundled Datasets (COMPLETED)
*Specs: [[01 - Zero-Latency Mock Exam Engine]], [[00 - Master CPALE Syllabus & Table of Specifications]]*

- [x] **11.1 Deterministic Question Bank Asset Structure (`assets/questions/`)**
  - [x] Author authentic, Board-level MCQ datasets across all 6 CPALE subjects:
    - `tax_questions.json`: RA 11976 (EOPT Act) VAT sales invoice substantiation, taxpayer tiers, RA 11534 (CREATE Act) MSME RCIT (20% vs 25%) and MCIT, TRAIN estate tax family home deductions.
    - `rfbt_questions.json`: BP 22 5 banking days notice rule, RA 11232 (Revised Corporation Code) board quorum baseline, RA 9160 (AMLA) ₱500,000 covered transaction threshold.
    - `far_questions.json`: PAS 12 income taxes temporary vs permanent differences, PAS 36 impairment of assets (higher of FVLCD and Value in Use).
    - `afar_questions.json`: PFRS 3 business combinations & proportionate goodwill, Statement of Affairs corporate liquidation & free asset recovery rate.
    - `aud_questions.json`: PSA 315 / PSA 200 Audit Risk Model (RoMM vs Detection Risk), PSA 705 modified auditor opinions (Qualified vs Adverse vs Disclaimer).
    - `mas_questions.json`: Cost-Volume-Profit pre-tax target profit sales units, Working Capital cash conversion cycle (DIO + DSO - DPO).
- [x] **11.2 Question Bank Importer & Offline Hydration (`lib/core/database/persistence/question_bank_importer.dart`)**
  - [x] Implement `QuestionBankImporter` with pure Dart JSON parsing, required field validation, and distractor trap map extraction.
  - [x] Support individual asset loading as well as aggregate `loadAllBundledQuestions()` across all 6 subjects.
  - [x] Wire `importQuestions()` into `LocalExamDatabase` and auto-hydrate in `main.dart` on application startup (58/58 tests passing).

---

## ✅ Milestone 12: Board-Scale Question Generator Engine & Confidence Tracking (COMPLETED)
*Specs: [[01 - Zero-Latency Mock Exam Engine]], [[00 - Master CPALE Syllabus & Table of Specifications]]*

- [x] **12.1 Explicit Confidence & Synthetic Metadata Tracking (`lib/features/exam/domain/entities/exam_question.dart`)**
  - [x] Add `verificationConfidence` (default `1.0` for pure-code verified calculations and certified codals) to `ExamQuestion`.
  - [x] Propagate `isSynthetic: true`, `parentQuestionId`, and `verificationConfidence: 1.0` across the mutation and importer pipelines.
- [x] **12.2 Full 70-Item / 100-Item Board Generator (`lib/features/exam/domain/question_generator_engine.dart`)**
  - [x] Implement `QuestionGeneratorEngine` capable of scaling authentic archetypes to full 70-item exams for FAR, AFAR, AUD, MAS, TAX, and 100-item exams for RFBT.
  - [x] Enforce psychometric Cognitive Tier distribution conforming to PRC BOA Resolution No. 2022-30 (L1 Knowledge ~30%, L2 Computation/Application ~40%, L3 Caselet Analysis ~30%).
  - [x] Implement `verifyQuestionIntegrity()` to automatically reject flawed options, duplicate options, or non-positive confidence before reaching the examinee.
  - [x] Integrate with `LocalExamDatabase.getQuestionForSubject()` with persistent in-memory session caching (62/62 tests passing).

---

## ⏳ Milestone 13: On-Device & Hybrid AI Engine Integration (Gemini Nano + MediaPipe + Socratic Tutor)
*Specs: [[02 - AI-Powered Rationalizer & ELI5]], [[Systems & AI Architecture Blueprint]]*

- [ ] **13.1 Grounded CPALE Prompt Assembler (`lib/core/ai/cpale_prompt_assembler.dart`)**
  - [ ] Implement the structured Board Exam Coach prompt builder injecting `[CASE CONTEXT]`, `[FINANCIAL DATA]`, `[QUESTION]`, `[CORRECT ANSWER]`, `[STUDENT SELECTED]`, `[PREVIOUS CASELET STEP RESULT]`, and grounded Codal Vault statutory text.
  - [ ] Enforce the neuro-symbolic constraint instructing the model to never compute standalone numbers and strictly narrate pre-verified figures from `DiagnosticFactSheet`.
- [ ] **13.2 Tiered AI Runtime & Persistent Rationale Cache (`lib/core/ai/local_ai_rationalizer_bridge.dart`)**
  - [ ] Wire the 3-tier execution cascade: **Tier 1 (Android AICore / Gemini Nano)** $\rightarrow$ **Tier 2 (MediaPipe Gemma 2B)** $\rightarrow$ **Tier 3 (Audited Deterministic Proof)**, plus optional online Gemini Flash fallback.
  - [ ] Replace the static string template in `_buildEli5Breakdown()` with adaptive AI explanation synthesis protected by `verifyNoHallucinatedCurrency()`.
  - [ ] Persist generated AI rationales into `LocalStorageService` by `factSheet.cacheKey` so reopening a reviewed question loads in `0ms` without re-running inference.
- [ ] **13.3 Interactive Socratic Reviewer Follow-Up (`lib/features/exam/presentation/widgets/ai_rationalizer_sheet.dart`)**
  - [ ] Add an interactive `"Ask Reviewer a Follow-Up"` Socratic Q&A bar inside `AiRationalizerSheet` with quick-prompt chips (e.g., *"Why is my chosen option a trap?"*, *"Cite the exact tax/PFRS rule"*, *"Show journal entry"*).

---

## ⏳ Milestone 14: AI Active-Recall Flashcard Synthesis & Handout OCR Scanner
*Specs: [[04 - Adaptive Flashcard Synthesizer & Spaced Repetition]], [[08 - Offline Document Ingestion & AI Note Synthesizer]]*

- [ ] **14.1 AI Active-Recall Flashcard Distillation (`lib/features/flashcards/data/flashcard_repository.dart`)**
  - [ ] Upgrade `synthesizeFromWeakAttempts()` to convert missed exam items and distractor traps into concise, high-yield active-recall Q&A cards via the AI bridge (replacing static stem truncation).
- [ ] **14.2 Review Center Handout Scanner & OCR Pipeline (`lib/core/ai/offline_ocr_note_synthesizer.dart`)**
  - [ ] Add image/handout scan simulation and file import flow in `StudyHubScreen` so reviewees can ingest physical review center handouts (CPAR, RESA, PRTC, Pinnacle) into Codal Vault entries and FSRS flashcards.

---

## ⏳ Milestone 15: Post-Exam Board Diagnostic Sheet & Mistake Drill Workflow
*Specs: [[01 - Zero-Latency Mock Exam Engine]], [[05 - Local Analytics & Board Readiness Predictor]]*

- [ ] **15.1 End-of-Exam Board Diagnostic Summary (`lib/features/exam/presentation/widgets/exam_summary_sheet.dart`)**
  - [ ] Present a comprehensive BOA Diagnostic Report when an examinee finishes or submits an exam session (Raw Score, BOA Scaled Score, Time-Trap breakdown, and Per-Topic accuracy).
  - [ ] Add a 1-click **"⚡ DRILL MISSED ITEMS"** action that launches an immediate targeted review session containing only the questions answered incorrectly or flagged during the exam.


