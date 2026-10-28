---
title: Offline Accounting Scratchpad & Basic Calculator
category: Reviewer UX & Tooling
status: Planned
priority: P0
created: 2026-10-28
target_subjects:
  - FAR
  - AFAR
  - MAS
  - TAX
  - AUD
---

# Offline Accounting Scratchpad & Basic Calculator

## 1. Overview & Problem Statement
In the actual CPALE, examinees are given scratch paper to write T-accounts, cash flow proofs, and adjusting journal entries, and are restricted to **non-programmable basic 4-function calculators**. 

On a mobile phone, forcing a user to leave the app to open a calculator or note app breaks examination state, risks app background killing, and ruins focus.

The **Offline Accounting Scratchpad & Basic Calculator** provides an integrated, non-intrusive bottom-sheet workspace that allows students to sketch T-accounts, compute arithmetic, and preserve their scratch work linked directly to the question item.

---

## 2. Core Components

### A. Non-Programmable 4-Function Tape Calculator
- Mimics the standard board-approved desktop calculator (Casio JW-200SC style).
- **Functions:** Basic arithmetic ($+, -, \times, \div$), percentage ($\%$, tax rate shortcut), square root ($\sqrt{}$), change sign ($+/-$), and Memory keys (`M+`, `M-`, `MRC`).
- **Calculation Tape:** A running history ribbon above the display showing previous steps so examinees can review where an arithmetic slip occurred.
- **Copy to Scratchpad:** One-tap button to transfer the calculated total directly into a T-account entry.

### B. Two-Column T-Account Ledger
- Standard accounting layout: **[ DEBIT (DR) ] | [ CREDIT (CR) ]**.
- Quick numeric entry without requiring extensive text descriptions during timed drills.
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
- **Zero Memory Bloat:** Canvas scribbles must be stored as compact path points or SVG strings, never uncompressed raster bitmap images, keeping each scratchpad record under 15KB.
- **Keyboard Handling:** On small mobile screens, the numeric keypad must not occlude the problem text. The calculator and T-account keypad should dock neatly at the bottom edge.

