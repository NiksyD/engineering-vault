---
title: Zero-Latency Mock Exam Engine
category: Core Engine
status: Planned
priority: P0
created: 2026-10-28
target_subjects:
  - FAR
  - AFAR
  - AUD
  - TAX
  - RFBT
  - MAS
---

# Zero-Latency Mock Exam Engine

## 1. Overview & Problem Statement
Examinees preparing for the Philippine CPALE must simulate high-stakes, 70-item board examinations under strict time constraints. Traditional web reviewers stutter or fail completely on unstable mobile connections. 

The **Zero-Latency Mock Exam Engine** runs 100% locally on the device using a pre-cached local database. Item switching, financial table rendering, distractor elimination, and state saves occur with 0ms network latency.

---

## 2. Modes of Operation
To prevent the UX flaw of spoiling answers during a formal mock exam:

1. **Board Simulation Mode (Formal Exam):**
   - Strictly timed (e.g., 3 hours for 70 items).
   - Instant validation and AI explanations are **disabled**.
   - Reviewees can flag items, eliminate options, and return via the Question Navigator.
   - Full diagnostic score report, answer key, and step-by-step rationales are unlocked only upon submission.
2. **Practice / Drill Mode (Targeted Study):**
   - Untimed or casual timer.
   - Instant option validation (green/red feedback).
   - "Ask On-Device AI" drawer unlocked immediately upon submission of each item.

---

## 3. Core Mobile UX Features
- **Question Navigator Matrix:** 1–70 grid bottom-sheet showing item status: *Answered (dark)*, *Unanswered (blank)*, and *Flagged for Review (flag icon)*.
- **Distractor Elimination (Strikethrough):** Swipe or long-press on an MCQ option to strike it through with an outline, helping students narrow down 4 choices to 2.
- **Split-View / Case Study Paging:** For heavy problem scenarios (e.g., corporate tax tables or consolidated balance sheets), the case prompt stays pinned or accessible via a quick-toggle tab so examinees don't lose context while reading choices.
- **Auto-Save State:** Every selection, flag, and elapsed millisecond is written immediately to local storage. Force-closing the app preserves exact progress.

---

## 4. Technical Architecture & Data Model

### Data Entities (ObjectBox / Drift)
```dart
// Core Question Entity
class ExamQuestion {
  int id;
  String subject;           // FAR, AFAR, AUD, TAX, RFBT, MAS
  String topic;             // e.g., "CREATE Act - Corporate Income Tax"
  String casePrompt;        // Case narrative (Markdown supported)
  String? tableDataJson;    // Structured financial statements / ledger rows
  String questionText;      // The actual question stem
  List<String> options;     // ['A: ...', 'B: ...', 'C: ...', 'D: ...']
  int correctOptionIndex;   // 0 for A, 1 for B, etc.
  String standardRationale; // Static base explanation
  int difficultyTier;       // 1 (Easy), 2 (Moderate), 3 (Board-Level)
}

// Active Exam Session Entity
class ExamSession {
  int id;
  String mode;              // "SIMULATION" | "PRACTICE"
  String subject;
  DateTime startedAt;
  DateTime? completedAt;
  int timeRemainingSeconds;
  Map<int, int> selectedAnswers; // questionId -> selectedIndex
  List<int> flaggedQuestionIds;
  List<int> eliminatedOptionKeys; // Encoded questionId_optionIndex
}
```

---

## 5. Engineering Constraints & Edge Cases
- **Rendering Large Financial Tables:** Use lightweight tabular widgets with fixed column widths rather than deeply nested WebViews to maintain 60–120 FPS scrolling.
- **Timer Drift:** Store exam end timestamp (`DateTime targetEndTime`) rather than relying purely on an in-memory periodic timer that could drift or pause when the phone enters battery saver mode.
- **Memory Footprint:** Question assets are indexed by `subject` and `topic` so only active exam questions (e.g., 70 items) are loaded into memory, keeping RAM overhead under 30MB.

