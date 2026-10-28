---
title: Offline Accounting Scratchpad & Basic Calculator
category: Reviewer UX & Tooling
status: Planned
priority: P0
created: 2026-10-28
updated: 2026-10-28
target_subjects:
  - FAR
  - AFAR
  - MAS
  - TAX
  - AUD
---

# Offline Accounting Scratchpad & Basic Calculator

## 1. Overview & Problem Statement
In the actual CPALE, examinees are given scratch paper to write T-accounts and adjusting journal entries, and are restricted to **non-programmable basic calculators** permitted under PRC BOA resolutions (e.g., Casio JW-200SC, AX-120ST). 

A generic calculator app without accountant-specific arithmetic shortcuts (`GT`, `K-Constant`, `M+`) is useless for Philippine CPALE reviewees, who are trained to compute Present Value (PV) factors and annuities in seconds using Casio hardware keystrokes.

The **Offline Accounting Scratchpad & Basic Calculator** provides an integrated, non-intrusive bottom-sheet workspace that emulates authentic Casio accounting hardware and preserves user scratch work per question item.

---

## 2. Core Components

### A. Casio JW-200SC Accounting Calculator Emulator
Examinees must solve problems within 2.5 minutes. The emulator supports standard review-center keystroke shortcuts:

1. **Grand Total (`GT`):**
   - Automatically accumulates products/quotients into a grand total register.
   - *Example:* Reviewee calculates multi-period cash flows ($CF_1 \times PV_1$, $CF_2 \times PV_2$, $CF_3 \times PV_3$). Pressing `GT` yields the exact present value of the stream in one keystroke without writing sub-totals.
2. **K-Constant Multiplication & Division:**
   - **Division Constant:** `1.10 [÷] [÷] [=]` yields $0.9091$ ($PVF_1$), pressing `[=]` yields $0.8264$ ($PVF_2$), pressing `[=]` yields $0.7513$ ($PVF_3$).
   - **Multiplication Constant:** `5000 [×] [×] 2 [=]` yields $10,000$; `3 [=]` yields $15,000$.
3. **Memory Registers:**
   - `M+`, `M-`, and `MRC` (Memory Recall/Clear).
4. **Accountant Utilities:**
   - `+/-` (Change sign), `%` (Percentage), `MU` (Mark Up / Margin).
5. **Running Tape Ribbon:**
   - History tape showing previous steps to verify arithmetic without re-typing.
   - **One-Tap Export:** Insert calculation result directly into an active T-Account entry.

### B. Two-Column T-Account Ledger
- Standard accounting layout: **[ DEBIT (DR) ] | [ CREDIT (CR) ]**.
- Quick numeric entry without requiring slow text descriptions during timed drills.
- Auto-summing running totals at the bottom showing net balance:
  $$\text{Net Balance} = \sum \text{Debits} - \sum \text{Credits}$$
- Visual highlighting when debits and credits do not balance.

### C. Freehand Scribble Canvas (Finger / Stylus)
- Lightweight canvas layer for quick formula jotting, timeline diagrams (for Leases / Revenue Recognition), and notes.
- Low-latency vector path rendering using Flutter's `CustomPainter`.

---

## 3. UI/UX Workflow & Ergonomics
- Accessed via a persistent button **"📐 Scratchpad"** on the question screen.
- Opens as an interactive **Draggable Bottom Sheet** that can be docked to half-height (split-screen with the question) or expanded to full-height.
- **Auto-Persistence:** All calculator tape entries, T-account balances, and canvas strokes are automatically serialized into the local database under `QuestionScratchpadRecord`. When navigating back to Question 44 later, the user's exact scratch work is restored.

---

## 4. Database Schema
```dart
class QuestionScratchpadRecord {
  int id;
  int questionId;
  int sessionId;
  String accountTitle;
  List<double> debitEntries;
  List<double> creditEntries;
  String? calculatorTapeJson; // List of operations performed
  String? scribbleSvgPaths;   // Vector strokes for freehand canvas
  DateTime updatedAt;
}
```

---

## 5. Engineering Constraints & Edge Cases
- **Hardware Keystroke Accuracy:** Casio constant division registers must behave exactly like physical hardware (`÷ ÷ =` sets the constant denominator).
- **Zero Memory Bloat:** Canvas scribbles are stored as compact SVG path strings, keeping each scratchpad record under 15KB.
- **Keyboard Docking:** The numeric keypad docks at the bottom edge so it never obscures the problem text.
