---
title: Local Analytics & Board Readiness Predictor
category: Core Engine & Analytics
status: Planned
priority: P1
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

# Local Analytics & Board Readiness Predictor

## 1. Overview & Problem Statement
Examinees often study blindly without knowing if their preparation meets the actual passing threshold set by the Professional Regulation Commission (PRC): **a general average of at least 75%, with no grade below 60% in any subject**.

The **Local Analytics & Board Readiness Predictor** calculates real-time passing probabilities, topic-level mastery, and time-triage efficiency entirely on-device, modeling both raw scores and estimated BOA standardized curves.

---

## 2. Key Dashboard Metrics

### 1. The BOA Passing Status & "Conditioned" Alarm
The PRC Board of Accountancy enforces a binary grading rule:
- **Passed:** General Weighted Average (GWA) $\ge 75\%$ AND no subject below $60\%$.
- **Conditioned:** GWA $\ge 75\%$ BUT one or two subjects fall below $60\%$. The examinee does not pass and must re-take those subjects.
- **Failed:** GWA $< 75\%$, or three or more subjects $< 60\%$.

> **UI Action:** If an examinee averages 84% across 5 subjects but scores 58% in RFBT, the dashboard flashes a blood-red **"⚠️ CONDITIONED WARNING"** instead of falsely projecting a passing score.

### 2. Raw Score vs. BOA Standardized Rating
BOA employs standardizing curves (Item Response Theory / percentile equatings):
- A raw score of 45/70 on a brutal AFAR exam often scales to an 81 rating.
- A raw score of 52/70 on an easy RFBT exam might only scale to a 75 rating.
- The engine offers a toggle: **[ Raw Percentage ] vs [ Estimated BOA Standardized Rating ]** based on historical cohort distributions.

### 3. Subject Matrix: Speed vs. Mastery
- **Cluster A (Financial & Assurance):** FAR, AFAR, AUD. Tracks calculation speed and adjusting journal entry accuracy.
- **Cluster B (Regulatory & Advisory):** TAX, MAS, RFBT. Tracks reading speed, memory recall, and threshold accuracy.

### 4. Triage Efficiency Audit
- Analyzes where time is bleeding: displays time spent on **Level 1 (Theory)** vs **Level 2 (Standard Computation)** vs **Level 3 (Time Traps)**.
- Flags questions where the user spent $> 3.5\text{ minutes}$ and still got the item wrong (the classic CPALE double-loss).

### 5. Ebbinghaus Memory Decay Index
- Measures predicted recall failure probability:

$$R = e^{-\frac{t}{S}}$$

---

## 3. Data Flow & Local Computation

```
[ Question Answered / Card Reviewed ]
                   │
                   ▼
[ Background Dart Isolate (Zero UI Lag) ]
  - Updates rolling average response latency
  - Calculates GWA and checks for < 60% Conditioned warning
  - Applies BOA IRT scaling curve
  - Recalculates decay index per syllabus topic
                   │
                   ▼
[ Written to Local Analytics Table ]
                   │
                   ▼
[ Reactive Flutter UI Updates Dashboard ]
```

---

## 4. Database Schema (ObjectBox / Drift)
```dart
class SubjectPerformanceMetric {
  int id;
  String subjectCode;           // "FAR", "TAX", etc.
  int totalAttempts;
  int correctAttempts;
  double rawAccuracyPercentage; // e.g., 68.5%
  double estimatedBoaRating;    // e.g., 78.2%
  double averageLatencySeconds; // e.g., 44.5s
  bool isBelowConditionFloor;   // True if rating < 60%
  DateTime lastCalculatedAt;
}

class TriageAuditRecord {
  int id;
  String subjectCode;
  int timeTrapCount;            // Items with > 3.5m spent & incorrect
  double avgL1LatencySeconds;   // Target < 45s
  double avgL2LatencySeconds;   // Target 90s - 120s
  double avgL3LatencySeconds;   // Time-sink questions
}
```

---

## 5. Engineering Constraints & Edge Cases
- **UI Thread Isolation:** Heavy regression and Bayesian updates run exclusively in a background Dart isolate.
- **Cold Start Behavior:** Display confidence intervals when data points are $< 50$ items.
