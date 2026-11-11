---
title: PasaCPA Frontend Core Screens Implementation Plan
category: Implementation Plan
doc-status: Ready for Execution
priority: P0
created: 2026-10-28
platform: Flutter / Dart
---

# PasaCPA Frontend Core Screens Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the foundational Neo-Brutalist mobile UI screens for PasaCPA, including the 4-tab main shell, zero-latency exam workspace with grouped caselets and MCQ option strikethrough, question navigator grid, and the Casio JW-200SC / T-account scratchpad bottom sheet.

**Architecture:** Feature-first Flutter layered architecture with clean separation between shared atomic theme widgets (`lib/core/theme/`), the Casio calculator engine (`lib/core/calculator/`), and vertical feature screens (`lib/features/exam/`, `lib/features/scratchpad/`, `lib/features/navigation/`). Employs lightweight reactive state (`ValueNotifier` / `ChangeNotifier`) to guarantee zero-latency 60–120 FPS UI updates.

**Tech Stack:** Flutter SDK ^3.13.2 / Dart 3, Google Fonts (`google_fonts` or local font definitions for Anton, Space Mono, and Geist), pure Dart deterministic arithmetic, custom vector painters.

**Spec:**
- [[Frontend Design & UI Architecture]]
- [[01 - Zero-Latency Mock Exam Engine]]
- [[06 - Offline Accounting Scratchpad & Basic Calculator]]

## Global Constraints

- **Geometry:** 0px border-radius across all buttons, cards, dialogs, sheets, and inputs (`BorderRadius.zero`).
- **Borders:** 2px solid `#1A1C1A` (Light) or `#E0E0E0` (Dark).
- **Drop Shadows:** Hard offset perpendicular shadows (`BoxShadow(offset: Offset(2, 2), blurRadius: 0)`), zero blur.
- **Palette:** Canvas paper `#FAF9F6`, Volt Green `#00E676`, Radical Orange `#FF3D00`, Buffer Gray `#EFEEEB`.
- **Typography:** Display = Anton, Financials/Tables = Space Mono, Body/Case Reading = Geist/Inter (1.5 line height).
- **Verification Floor:** Zero errors or warnings on `flutter analyze`, 100% test passes on `flutter test`.
- **Advisory Commits:** Conventional Commits (`feat: <imperative>`), never run git add/commit autonomously.

## Review Focus

- **Input / State Edge Case 1 (Option Strikethrough & Selection Collision):** Long-pressing an option strikes it through (`isEliminated: true`). Tapping an eliminated option must not select it unless first un-eliminated.
- **Input / State Edge Case 2 (Caselet Scroll Isolation):** Scrolling through a long financial statement table in the pinned case section must not freeze or fight with the outer question page scroll controller.
- **Input / State Edge Case 3 (Calculator Constant Mode `K`):** Repeatedly pressing `[=]` after `1.10 [÷] [÷]` must generate compounding present value factors ($0.9091, 0.8264, 0.7513$) matching Casio hardware.
- **Input / State Edge Case 4 (T-Account Balance Recalculation):** Adding debit or credit rows with negative signs or floating point decimals must round deterministically to 2 decimal places with zero IEEE 754 precision drift.
- **Input / State Edge Case 5 (Screen Overflow on Small Devices):** Bottom navigation bar and docked action strip must fit on a 360px viewport without `A RenderFlex overflowed by X pixels` errors.

---

### Task 1: Neo-Brutalist Theme Tokens & Core Atomic Widgets
- **Files:**
  - Create: `lib/core/theme/app_colors.dart`
  - Create: `lib/core/theme/app_typography.dart`
  - Create: `lib/core/theme/app_theme.dart`
  - Create: `lib/core/theme/widgets/brutalist_button.dart`
  - Create: `lib/core/theme/widgets/brutalist_card.dart`
  - Test: `test/core/theme/widgets/brutalist_button_test.dart`
- **Output:** Working theme tokens and tactile button with micro-press animation.

### Task 2: MCQ Option Card with Strikethrough & Selection States
- **Files:**
  - Create: `lib/core/theme/widgets/mcq_option_card.dart`
  - Test: `test/core/theme/widgets/mcq_option_card_test.dart`
- **Output:** MCQ card with letter badges, green/orange feedback states, and long-press distractor strikethrough.

### Task 3: Main Navigation Shell & Persistent 4-Tab Bottom Bar
- **Files:**
  - Create: `lib/features/navigation/presentation/main_navigation_screen.dart`
  - Create: `lib/features/navigation/presentation/widgets/brutalist_bottom_nav_bar.dart`
  - Test: `test/features/navigation/presentation/main_navigation_screen_test.dart`
- **Output:** Persistent 4-tab shell (EXAM, STUDY HUB, CARDS, ANALYTICS) with 2px solid borders.

### Task 4: Accounting Ledger Table & Pinned Caselet Viewer
- **Files:**
  - Create: `lib/features/exam/presentation/widgets/accounting_ledger_table.dart`
  - Create: `lib/features/exam/presentation/widgets/caselet_viewer.dart`
  - Test: `test/features/exam/presentation/widgets/accounting_ledger_table_test.dart`
- **Output:** Tabular financial statements with Space Mono numbers and grouped sub-question navigation chips.

### Task 5: Question Navigator Matrix & Triage Drawer (1–70 Grid)
- **Files:**
  - Create: `lib/features/exam/presentation/widgets/question_navigator_sheet.dart`
  - Test: `test/features/exam/presentation/widgets/question_navigator_sheet_test.dart`
- **Output:** 1–70 grid bottom sheet displaying answered, flagged, and L1/L2/L3 triage states.

### Task 6: Casio JW-200SC Calculator Engine & T-Account Scratchpad
- **Files:**
  - Create: `lib/core/calculator/casio_calculator_engine.dart`
  - Create: `lib/features/scratchpad/presentation/widgets/scratchpad_sheet.dart`
  - Test: `test/core/calculator/casio_calculator_engine_test.dart`
  - Test: `test/features/scratchpad/presentation/widgets/scratchpad_sheet_test.dart`
- **Output:** Hardware-accurate Casio keystroke shortcuts (`GT`, `K-Constant`) and two-column auto-summing T-Account ledger.

### Task 7: Full Exam Workspace Integration Screen
- **Files:**
  - Create: `lib/features/exam/presentation/screens/exam_workspace_screen.dart`
  - Modify: `lib/features/navigation/presentation/main_navigation_screen.dart`
  - Modify: `lib/main.dart`
  - Test: `test/features/exam/presentation/screens/exam_workspace_screen_test.dart`
- **Output:** Fully assembled mobile exam workspace with caselet viewer, options, docked action strip, and clean `flutter analyze` & `flutter test` pass.

