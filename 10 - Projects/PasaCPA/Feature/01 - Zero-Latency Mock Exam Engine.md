---
title: Zero-Latency Mock Exam Engine
category: Core Engine
status: Planned
priority: P0
created: 2026-10-28
updated: 2026-10-28
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
Examinees preparing for the Philippine CPALE must simulate high-stakes, 70-item board examinations under strict time constraints (180 minutes = ~2.5 minutes/question). 

The **Zero-Latency Mock Exam Engine** runs 100% locally on the device using a pre-cached local database. Item switching, financial table rendering, distractor elimination, and state saves occur with 0ms network latency.

---

## 2. Modes of Operation

1. **Board Simulation Mode (Formal Exam):**
   - Strictly timed (3 hours for 70 items).
   - Instant validation and AI explanations are **disabled**.
   - Reviewees can flag items, eliminate options, and return via the Question Navigator.
   - Diagnostic score report, answer key, and rationales unlocked only upon submission.
2. **Practice / Drill Mode (Targeted Study):**
   - Untimed or casual timer.
   - Instant option validation (green/red feedback).
   - "Ask On-Device AI" drawer unlocked immediately per item.
3. **PRC Scantron Transfer Drill Mode (Bubble-Sheet Anxiety Training):**
   - Simulates the physical PRC Sheet (Lead Pencil No. 2).
   - Disables direct tapping on the question card. Reviewees must tap-to-shade an on-screen replica of the PRC Bubble Sheet strip at the bottom of the screen.
   - Includes a **"Batch Shading Drill"** at the 20-minute warning mark to build muscle memory for transferring questionnaire answers to the answer sheet under adrenaline.

---

## 3. High-Stakes CPALE Realities & Features

### A. Grouped Caselet Engine (1 Fact Pattern $\rightarrow$ 3 to 5 Sub-Questions)
In **AFAR**, **Auditing**, and **FAR**, the BOA regularly tests multi-item comprehensive problems (e.g., a partnership dissolution, long-term construction contract, or audit of receivables):
- A single master case file (narrative + financial table) remains pinned on the left/top.
- Reviewees navigate between sub-questions (e.g., Item 18: Realized GP; Item 19: Ending CIP; Item 20: Provision for Loss) without re-scrolling or losing the master case context.

### B. Time Triage & The "3-Minute Trap" Alert
Time mismanagement is the #1 reason reviewees fail FAR and MAS:
- **Triage Classification:** Examinees can tag items on the fly:
  - **L1 (Theory):** Target $< 45\text{s}$.
  - **L2 (Direct Computation):** Target $1.5\text{m} - 2\text{m}$.
  - **L3 (Monster Case / Heavy Math):** Flag and save for the end.
- **Pacing Alarm:** If a reviewee remains active on a single item past **3.5 minutes**, an unobtrusive border pulse warns: `"⚠️ Time Trap: Flag and Move On."`

### C. Distractor Elimination (Strikethrough)
- Swipe or long-press an MCQ option to strike it through, narrowing 4 choices down to 2.

### D. Question Navigator Matrix
- 1–70 grid bottom-sheet showing: *Answered*, *Unanswered*, *Flagged*, and *Triage Level (L1/L2/L3)*.

---

## 4. Technical Architecture & Data Model

```dart
// Master Case File (for Grouped Caselets)
class ExamCaselet {
  int id;
  String subject;           // FAR, AFAR, AUD, etc.
  String title;             // e.g., "Apex Holdings Partnership Liquidation"
  String narrativePrompt;   // Master case story
  String? financialTableJson; // Structured accounting schedules / trial balances
  List<int> questionIds;    // Interlinked sub-questions
}

// Core Question Entity
class ExamQuestion {
  int id;
  int? caseletId;           // Null for standalone MCQs; linked for Caselets
  String subject;
  String topic;
  String questionText;
  List<String> options;     // ['A: ...', 'B: ...', 'C: ...', 'D: ...']
  int correctOptionIndex;
  String standardRationale;
  int difficultyTier;       // 1 (Easy), 2 (Moderate), 3 (Board-Level)
  int subQuestionSequence;  // Order within caselet (e.g., 1 of 4)
}

// Active Exam Session Entity
class ExamSession {
  int id;
  String mode;              // "SIMULATION" | "PRACTICE" | "SCANTRON_DRILL"
  String subject;
  DateTime startedAt;
  DateTime? completedAt;
  int timeRemainingSeconds;
  Map<int, int> selectedAnswers; // questionId -> selectedIndex
  List<int> flaggedQuestionIds;
  List<int> eliminatedOptionKeys; // Encoded questionId_optionIndex
  Map<int, String> triageTags;    // questionId -> "L1" | "L2" | "L3"
  Map<int, double> itemLatencies; // questionId -> seconds spent
}
```

---

## 5. Engineering Constraints & Edge Cases
- **Timer Drift:** Store absolute target end time (`DateTime targetEndTime`) to avoid OS background pausing.
- **Caselet Caching:** Caselet text and table data are retained in memory while transitioning between sub-questions (Items 18 $\rightarrow$ 20) with zero re-render overhead.
