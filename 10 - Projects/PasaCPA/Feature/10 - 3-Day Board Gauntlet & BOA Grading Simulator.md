---
title: 3-Day Board Gauntlet & BOA Grading Simulator
category: Simulation & Exam Science
status: Planned
priority: P1
created: 2026-10-28
target_subjects:
  - MAS
  - AUD
  - TAX
  - RFBT
  - FAR
  - AFAR
---

# 3-Day Board Gauntlet & BOA Grading Simulator

## 1. Overview & Problem Statement
Most examinees prepare by taking single, isolated 70-item quizzes. However, the Philippine CPALE is a **3-day marathon of mental endurance**. Examinees regularly experience severe cognitive decline during the afternoon sessions—especially on **Day 3 Afternoon (AFAR)** after already enduring 15 hours of grueling calculations.

The **3-Day Board Gauntlet** simulates the exact schedule, fatigue dynamics, and grading formulas established by the Professional Regulation Commission (PRC) Board of Accountancy (BOA).

---

## 2. The Official BOA 3-Day Schedule Simulation

Examinees can schedule a formal "Pre-Board Weekend" adhering to the official PRC testing timetable:

| Day | Slot | Subject | Duration | Core Cognitive Demand |
| :---: | :---: | :--- | :---: | :--- |
| **Day 1** | 8:00 AM – 11:00 AM | **MAS (Management Advisory Services)** | 3 Hours | Quantitative modeling, capital budgeting, working capital |
| **Day 1** | 1:00 PM – 4:00 PM | **AUD (Auditing Theory & Problems)** | 3 Hours | Audit standards, substantive testing, adjusting entries |
| **Day 2** | 8:00 AM – 11:00 AM | **TAX (Taxation)** | 3 Hours | NIRC, TRAIN, CREATE, EOPT, tax computations |
| **Day 2** | 1:00 PM – 4:00 PM | **RFBT (Regulatory Framework)** | 3 Hours | Fast reading, legal thresholds, codal recall |
| **Day 3** | 8:00 AM – 11:00 AM | **FAR (Financial Accounting & Reporting)** | 3 Hours | Comprehensive PFRS standards, financial statements |
| **Day 3** | 1:00 PM – 4:00 PM | **AFAR (Advanced Financial Accounting)** | 3 Hours | Consolidations, partnerships, cost accounting, derivatives |

---

## 3. Cognitive Fatigue Analytics (The Afternoon Dip)
- **Fatigue Index:** Analyzes the drop in accuracy and spike in calculation latency between Morning Sessions (8:00–11:00 AM) and Afternoon Sessions (1:00–4:00 PM).
- **Day 3 AFAR Vulnerability Metric:** Specifically models how physical exhaustion on Day 3 leads to careless arithmetic slips in long partnership or consolidation problems.

---

## 4. PRC BOA Composite Scorecard & Grading Logic

### A. The Statutory Passing Criteria
```dart
enum BoaResultStatus {
  PASSED,       // GWA >= 75.0% AND every subject >= 60.0%
  CONDITIONED,  // GWA >= 75.0% BUT 1 or 2 subjects < 60.0%
  FAILED        // GWA < 75.0% OR 3 or more subjects < 60.0%
}
```

### B. Standardized IRT Curving Engine
The simulator applies a realistic percentile-equating curve based on historical CPALE batch statistics:
1. Raw scores are normalized against subject historical difficulty weights.
2. Standardized ratings are generated for each subject.
3. If an examinee lands in "CONDITIONED" territory, the app clearly highlights the exact subject needing removal examination and the time window permitted under PRC rules (re-examination within 2 years).

### C. Cohort Percentile Benchmarking (When Online)
- Anonymized exam results sync to Supabase to calculate a national batch percentile rank.
- Reviewees see where they stand against thousands of other reviewees nationwide (e.g., *"Top 8% Batch Percentile — Projected PRC Board Pass"*).

---

## 5. Engineering Constraints & Database Architecture
```dart
class BoardGauntletSession {
  int id;
  DateTime startedAt;
  DateTime? completedAt;
  Map<String, int> subjectRawScores;     // "MAS": 52, "AUD": 58, etc.
  Map<String, double> subjectBoaRatings; // "MAS": 81.5, "AUD": 85.0
  double generalWeightedAverage;
  String resultStatus;                   // "PASSED", "CONDITIONED", "FAILED"
  List<String> conditionedSubjects;      // e.g., ["RFBT"]
  double morningVsAfternoonFatigueDrop; // e.g., -14.2% drop in accuracy
  bool isFullyCompleted;
}
```

- **Offline Resiliency:** An examinee can complete all 3 days completely offline. State, partial timestamps, and fatigue logs are stored locally in ObjectBox/Drift. Syncing to the national percentile leaderboard occurs automatically when an internet connection is established.

