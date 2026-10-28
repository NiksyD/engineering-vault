---
title: "PasaCPA - Mobile Coding Standards & Engineering Skill"
project: PasaCPA
platform: Flutter / Dart
category: Coding Standards
status: Active
created: 2026-10-28
tags:
  - flutter
  - dart
  - local-first
  - local-ai
  - standards
---

# 📱 PasaCPA: Mobile Coding Standards & Engineering Protocol

> **Purpose:** Synthesizes the core principles of **Ponytail** (pragmatic minimalism), **Superpowers** (TDD and verification), **Matt Pocock** (surgical debugging & grilling), and **UCJobs** (Definition of Done & advisory commits) into an immutable standard for developing `pasacpa_mobile`.

---

## 🏛️ 1. Architecture & Project Layout

The codebase follows a **Feature-First Layered Architecture**:

```text
lib/
├── core/                        # Global shared infrastructure
│   ├── database/                # Drift SQLite database, DAOs, schema migrations
│   ├── ai/                      # AICore / MediaPipe LLM & ML Kit OCR bridges
│   ├── calculator/              # Casio JW-200SC engine (GT, K-Constant, arithmetic)
│   ├── srs/                     # FSRS / SM-2 spaced repetition scheduler
│   └── theme/                   # Neo-brutalist styling tokens, palettes, typography
├── features/                    # Vertical feature slices
│   ├── exam/                    # Zero-latency mock exam engine & grouped caselets
│   │   ├── data/                # Repositories & Drift queries
│   │   ├── domain/              # Entities (ExamCaselet, ExamQuestion, ExamSession)
│   │   └── presentation/        # Widgets, state controllers, bottom sheets
│   ├── scratchpad/              # T-Account ledger & scribble canvas
│   ├── flashcards/              # 3D active recall decks & AI synthesis
│   ├── analytics/               # BOA grading curves & Ebbinghaus decay tracker
│   └── codal_vault/             # Search-indexed FTS5 tax & legal reference matrix
└── main.dart                    # App initialization & dependency container
```

---

## ⚡ 2. The 6 Non-Negotiable Engineering Rules

### Rule 1: The Smallest Complete Change (Ponytail)
- Prefer native Flutter widgets (`CustomPaint`, `DraggableScrollableSheet`, `Table`) over external pub.dev dependencies whenever possible.
- Never add a package for a trivial 20-line utility.
- No "for later" boilerplate or speculative wrappers.

### Rule 2: Surgical Scoping & Zero Shotgun Edits (UCJobs)
- Only edit files directly involved in the current task.
- Unrelated formatting, re-ordering, or refactoring in untouched files is strictly prohibited.
- Before editing any shared function/widget, grep all callers across `lib/` and `test/`.

### Rule 3: Strict Type Safety & Null Safety
- Zero usage of `dynamic` unless explicitly interfacing with raw platform channels or JSON decoding.
- Every domain model must be immutable (`@immutable` or `final` fields).
- Strongly typed database queries via Drift DAOs.

### Rule 4: Verification Before Completion (Superpowers)
An implementation task is **never complete** until:
1. `flutter analyze` runs with **zero warnings and zero errors**.
2. Relevant unit/widget tests are added and pass (`flutter test`).
3. Actual terminal output is produced and reported.

### Rule 5: Advisory Git Commits (UCJobs)
- Never autonomously execute `git add`, `git commit`, or `git push`.
- Format advisory commits using Conventional Commits:
  ```text
  <type>: <short imperative subject>

  - <plain-language user-visible outcome>
  - <plain-language secondary benefit>
  ```
- Allowed types: `feat`, `fix`, `refactor`, `perf`, `test`, `chore`.

### Rule 6: Mandatory Receipt & Residual Risk
Every response touching code or architecture must conclude with a 2-line receipt:
```text
*What was skipped / not checked:* [Explicit list of items deferred or unverified]
*Key risk:* [Primary runtime, memory, or platform risk the user must know]
```

---

## 🛠️ 3. Technology Stack Conventions

| Responsibility | Standard Tool / Pattern | Forbidden Antipattern |
| :--- | :--- | :--- |
| **Local Database** | **Drift (SQLite)** with FTS5 search | Unindexed raw JSON files or unmigrated raw SQLite strings |
| **State Management** | **ValueNotifier / ChangeNotifier** or **Riverpod** | Heavy nested boilerplate; mixing business logic inside UI build methods |
| **Styling** | Neo-brutalist theme tokens (0px radius, 2px solid black borders, hard drop-shadows) | Rounded bubbly corners, blurry soft shadows |
| **Math Calculations** | Deterministic Dart math (`CasioCalculatorEngine`) | Asking local LLMs to independently calculate arithmetic |
| **Background Work** | Dart `Isolate.run()` for heavy metrics & FTS searches | Blocking the main UI thread during timed exams |

---

## 📋 4. Definition of Done (DoD) Checklist

- [ ] Exact changed-file set isolated and identified.
- [ ] Logic implemented with minimum diff.
- [ ] No regression introduced to existing tests.
- [ ] `flutter analyze` passes clean.
- [ ] `flutter test` executed with verified green output.
- [ ] Advisory Conventional Commit drafted.
- [ ] Receipt stating what was skipped and key risks appended.

