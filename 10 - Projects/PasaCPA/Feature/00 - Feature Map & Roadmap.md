---
title: PasaCPA Feature Map & System Architecture
category: Architecture Overview
status: Active
created: 2026-10-28
updated: 2026-10-28
---

# PasaCPA Feature Map & Architecture Overview

This directory contains the detailed engineering specifications, data models, and UI/UX flows for all features powering **PasaCPA**—a local-first, on-device AI reviewer for the Philippine Certified Public Accountant Licensure Examination (CPALE).

---

## Complete Feature Matrix

| # | Feature | Category | Priority | Target Subjects | Status |
| :-: | :--- | :--- | :-: | :--- | :-: |
| **01** | [[01 - Zero-Latency Mock Exam Engine]] | Core Engine | **P0** | All 6 CPALE Subjects | In Design |
| **02** | [[02 - AI-Powered Rationalizer & ELI5]] | Local AI | **P0** | All 6 CPALE Subjects | In Design |
| **03** | [[03 - On-Device Case Study Generator]] | Local AI | **P1** | AFAR, AUD, FAR, TAX, MAS | Planned |
| **04** | [[04 - Adaptive Flashcard Synthesizer & Spaced Repetition]] | Learning Science | **P0** | All 6 CPALE Subjects | Planned |
| **05** | [[05 - Local Analytics & Board Readiness Predictor]] | Analytics | **P1** | All 6 CPALE Subjects | Planned |
| **06** | [[06 - Offline Accounting Scratchpad & Basic Calculator]] | Reviewer Tooling | **P0** | FAR, AFAR, MAS, TAX, AUD | In Design |
| **07** | [[07 - Delta-Based Background Sync Engine]] | Data Architecture | **P1** | Global / Supabase | Planned |
| **08** | [[08 - Offline Document Ingestion & AI Note Synthesizer]] | Local AI / OCR | **P1** | TAX, RFBT, AUD, FAR, AFAR | Planned |
| **09** | [[09 - Offline Codal & Tax Matrix Quick-Vault]] | Reviewer Reference | **P1** | TAX, RFBT, AUD, FAR, AFAR | Planned |
| **10** | [[10 - 3-Day Board Gauntlet & BOA Grading Simulator]] | Exam Science | **P1** | All 6 CPALE Subjects | Planned |

---

## Architectural Pillars

```
                                  [ PasaCPA Mobile (Flutter) ]
                                                │
             ┌──────────────────────────────────┼──────────────────────────────────┐
             ▼                                  ▼                                  ▼
   [ Core Exam Engine ]              [ Local-First Data Layer ]           [ 2-Stage Local AI Pipeline ]
- 70-item Board Simulation         - ObjectBox / Drift (SQLite)          - Stage 1: Google ML Kit / OCR
- Grouped Caselets (AFAR/AUD)      - Zero-lag Local WAL                  - Stage 2: Gemini Nano / Gemma 2B
- Time-Trap Pacing (L1/L2/L3)      - Non-blocking Delta Sync (Supabase)  - Cascading Error Rationalizer
- Casio JW-200SC (GT, K-Constant)  - Offline-First by default            - Parametric Case Mutator
- Scantron Transfer Drill Mode     - Search-indexed FTS5 Quick-Vault     - 100% on-device (Zero Token Cost)
```

---

## Recommended Implementation Phases

### Phase 1: High-Yield MVP (P0s)
1. **Local Database & Question Bank Schema** ([[01 - Zero-Latency Mock Exam Engine]])
   - Standalone MCQs and Grouped Caselet support.
2. **Mobile Exam Engine & Navigation**
   - Question Matrix, Distractor Strikethrough, and Time-Trap Alert.
3. **Casio JW-200SC Calculator & T-Account Bottom Sheet** ([[06 - Offline Accounting Scratchpad & Basic Calculator]])
   - With `GT`, `K-Constant` multiplication/division, and auto-summing DR/CR ledger.
4. **On-Device AI Rationalizer Bridge** ([[02 - AI-Powered Rationalizer & ELI5]])
   - With distractor trap identification and cascading error detection.

### Phase 2: Retention, Reference & Documents (P1s)
5. **Adaptive Flashcards with FSRS Spaced Repetition** ([[04 - Adaptive Flashcard Synthesizer & Spaced Repetition]])
6. **Offline Codal & Tax Matrix Quick-Vault** ([[09 - Offline Codal & Tax Matrix Quick-Vault]])
   - Instant search for CREATE, EOPT, graduated tax brackets, and RCCP voting rules.
7. **Local Document Ingestion (OCR $\rightarrow$ Local LLM)** ([[08 - Offline Document Ingestion & AI Note Synthesizer]])
8. **Parametric Case Study Generator** ([[03 - On-Device Case Study Generator]])

### Phase 3: High-Stakes Simulation & Ecosystem
9. **3-Day Board Gauntlet & Cognitive Fatigue Analytics** ([[10 - 3-Day Board Gauntlet & BOA Grading Simulator]])
10. **Local Analytics Dashboard with BOA "Conditioned" Warning** ([[05 - Local Analytics & Board Readiness Predictor]])
11. **Supabase Delta-Sync & National Batch Benchmarking** ([[07 - Delta-Based Background Sync Engine]])
