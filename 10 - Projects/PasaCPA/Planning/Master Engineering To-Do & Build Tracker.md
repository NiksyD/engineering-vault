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

## 🚧 Milestone 5: Offline Codal & Tax Matrix Quick-Vault (NEXT UP — P1)
*Specs: [[09 - Offline Codal & Tax Matrix Quick-Vault]]*

- [ ] **5.1 SQLite FTS5 Search Engine (`lib/features/codal_vault/data/`)**
  - [ ] Create virtual FTS5 table `codal_vault_fts` indexed by `syllabus_node_id`, statute code (NIRC, CREATE RA 11534, EOPT RA 11976, RCCP RA 11232, PFRS/PAS, PSA), and keywords.
  - [ ] Seed high-yield quick matrices: Corporate/Individual Tax Rates, EOPT 2024 Invoicing & Taxpayer Tiers, Estate/Donor Tax Deductions, RCCP Voting Quorums, AMLA Thresholds, and PSA 700/705 Audit Opinion Matrix.
- [ ] **5.2 Study Hub & Quick-Vault UI (`lib/features/codal_vault/presentation/`)**
  - [ ] Build the **STUDY HUB** tab combining interactive Syllabus Checklists (1,122 items) and instant `<10ms` FTS5 Codal Search with highlighted statutory thresholds.
  - [ ] Connect Stage 2 of the AI Rationalizer to pull grounded statutory excerpts from `codal_vault_fts`.

---

## 📋 Milestone 6: Adaptive Flashcard Synthesizer & FSRS Scheduler (P0)
*Specs: [[04 - Adaptive Flashcard Synthesizer & Spaced Repetition]]*

- [ ] **6.1 Pure Dart FSRS / SM-2 Spaced Repetition Engine (`lib/core/srs/`)**
  - [ ] Implement deterministic stability ($S$), difficulty ($D$), and Ebbinghaus retrievability ($R = e^{-t/S}$) calculations based on recall ratings (`Again`, `Hard`, `Good`, `Easy`) and response latency.
- [ ] **6.2 Weak-Topic Flashcard Deck UI (`lib/features/flashcards/presentation/`)**
  - [ ] Build the **CARDS** tab featuring Neo-Brutalist flip cards, active-recall prompts linked to weak `syllabus_node_id`s, and auto-queueing from missed exam questions.

---

## 📋 Milestone 7: Local Analytics & BOA Readiness Predictor (P1)
*Specs: [[05 - Local Analytics & Board Readiness Predictor]]*

- [ ] **7.1 Background Compute Isolate for BOA Grading & IRT (`lib/features/analytics/domain/`)**
  - [ ] Implement General Weighted Average (GWA $\ge 75\%$) and Per-Subject Floor ($\ge 60\%$) evaluator.
  - [ ] Implement the **"⚠️ CONDITIONED WARNING"** detector (triggers when GWA $\ge 75\%$ but 1 or 2 subjects $< 60\%$).
  - [ ] Implement Triage Efficiency Audit (`L1` $<45\text{s}$, `L2` $\sim 120\text{s}$, `L3` $>210\text{s}$ time-trap double-loss counter) and Raw vs. BOA IRT Scaled Rating toggle.
- [ ] **7.2 Analytics Dashboard Screen (`lib/features/analytics/presentation/`)**
  - [ ] Build the **ANALYTICS** tab displaying the 6-Subject Readiness Radar/Bars, Conditioned Status Alarm, Time-Trap Triage Audit, and Ebbinghaus Decay heatmap.

---

## 📋 Milestone 8: 3-Day Board Gauntlet, Case Mutator & Scantron Mode (P1)
*Specs: [[10 - 3-Day Board Gauntlet & BOA Grading Simulator]], [[03 - On-Device Case Study Generator]]*

- [ ] **8.1 3-Day Board Gauntlet Simulator**
  - [ ] Implement multi-session state machine replicating the actual 3-day PRC schedule (Day 1: MS + AUD; Day 2: TAX + RFBT; Day 3: FAR + AFAR) with cognitive fatigue tracking (Hour 1 vs Hour 3 accuracy drop-off).
  - [ ] Implement **Scantron Shading Transfer Drill Mode** (batch-shading bubble sheets under time pressure).
- [ ] **8.2 Parametric Case Study Mutator (`lib/features/exam/domain/case_mutator.dart`)**
  - [ ] Build pure Dart parametric number & entity mutator so repeated practice on a caselet generates fresh figures and recalculates the answer key deterministically, preventing rote answer memorization.

---

## 📋 Milestone 9: Supabase Delta-Sync & Offline Document OCR (P1)
*Specs: [[07 - Delta-Based Background Sync Engine]], [[08 - Offline Document Ingestion & AI Note Synthesizer]]*

- [ ] **9.1 Delta-Based Background Sync Engine (`lib/core/database/sync/`)**
  - [ ] Implement downstream delta patch puller (`sync_version > local_version`) for tax law errata and new questions.
  - [ ] Implement upstream idempotent WAL batch uploader (`tx_id` UUIDv4) with a **"Strict Offline Privacy Mode"** toggle.
- [ ] **9.2 Offline Handout OCR & Note Synthesizer**
  - [ ] Integrate Google ML Kit Text Recognition v2 for scanning physical review center handouts into local structured study notes and flashcards.

