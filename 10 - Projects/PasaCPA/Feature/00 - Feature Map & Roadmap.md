---
title: PasaCPA Feature Map & System Architecture
category: Architecture Overview
status: Active
created: 2026-10-28
---

# PasaCPA Feature Map & Architecture Overview

This directory contains the detailed engineering specifications, data models, and UI/UX flows for all features powering **PasaCPA**—a local-first, on-device AI reviewer for the Philippine Certified Public Accountant Licensure Examination (CPALE).

---

## Complete Feature Matrix

| # | Feature | Category | Priority | Target Subjects | Status |
| :-: | :--- | :--- | :-: | :--- | :-: |
| **01** | [[01 - Zero-Latency Mock Exam Engine]] | Core Engine | **P0** | All 6 CPALE Subjects | Planned |
| **02** | [[02 - AI-Powered Rationalizer & ELI5]] | Local AI | **P0** | All 6 CPALE Subjects | Planned |
| **03** | [[03 - On-Device Case Study Generator]] | Local AI | **P1** | AFAR, AUD, FAR, TAX, MAS | Planned |
| **04** | [[04 - Adaptive Flashcard Synthesizer & Spaced Repetition]] | Learning Science | **P0** | All 6 CPALE Subjects | Planned |
| **05** | [[05 - Local Analytics & Board Readiness Predictor]] | Analytics | **P1** | All 6 CPALE Subjects | Planned |
| **06** | [[06 - Offline Accounting Scratchpad & Basic Calculator]] | Reviewer Tooling | **P0** | FAR, AFAR, MAS, TAX, AUD | Planned |
| **07** | [[07 - Delta-Based Background Sync Engine]] | Data Architecture | **P1** | Global / Supabase | Planned |
| **08** | [[08 - Offline Document Ingestion & AI Note Synthesizer]] | Local AI / OCR | **P1** | TAX, RFBT, AUD, FAR, AFAR | Planned |

---

## Architectural Pillars

```
                                  [ PasaCPA Mobile (Flutter) ]
                                                │
             ┌──────────────────────────────────┼──────────────────────────────────┐
             ▼                                  ▼                                  ▼
   [ Core Exam Engine ]              [ Local-First Data Layer ]           [ 2-Stage Local AI Pipeline ]
- 70-item Board Simulation         - ObjectBox / Drift (SQLite)          - Stage 1: Google ML Kit / OCR
- Distractor Strikethrough         - Zero-lag Local WAL                  - Stage 2: Gemini Nano / Gemma 2B
- 4-Function Calculator + T-Acct   - Non-blocking Delta Sync (Supabase)  - ELI5, Case Mutator, Smart Notes
- FSRS Spaced Repetition Queue     - Offline-First by default            - 100% on-device (Zero Token Cost)
```

---

## Recommended Implementation Phases

### Phase 1: High-Yield MVP (P0s)
1. **Local Database & Question Bank Schema** ([[01 - Zero-Latency Mock Exam Engine]])
2. **Mobile Exam UI & Navigation** with Question Matrix & Distractor Elimination
3. **Basic Calculator & Two-Column T-Account Bottom Sheet** ([[06 - Offline Accounting Scratchpad & Basic Calculator]])
4. **On-Device AI Rationalizer Bridge** ([[02 - AI-Powered Rationalizer & ELI5]])

### Phase 2: Retention & Synthesis (P1s)
5. **Adaptive Flashcards with Spaced Repetition** ([[04 - Adaptive Flashcard Synthesizer & Spaced Repetition]])
6. **Local Document Ingestion (OCR $\rightarrow$ Local LLM)** ([[08 - Offline Document Ingestion & AI Note Synthesizer]])
7. **Parametric Case Study Generator** ([[03 - On-Device Case Study Generator]])

### Phase 3: Analytics & Ecosystem
8. **Board Readiness Predictor & Forgetting Curve** ([[05 - Local Analytics & Board Readiness Predictor]])
9. **Supabase Delta-Sync & Law Patching** ([[07 - Delta-Based Background Sync Engine]])

