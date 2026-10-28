---
title: Local Analytics & Board Readiness Predictor
category: Core Engine & Analytics
status: Planned
priority: P1
created: 2026-10-28
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

The **Local Analytics & Board Readiness Predictor** calculates real-time passing probabilities and topic-level mastery entirely on-device. It analyzes accuracy, response latency (speed vs. accuracy trade-off), and memory decay without sending sensitive student score history to the cloud.

---

## 2. Key Dashboard Metrics

### 1. Projected CPALE Board Score
- An aggregate percentage calculated across simulated exams weighted by PRC subject units.
- Flags "Conditioned" status warnings if any subject falls below the statutory 60% floor, even if the general average is $\ge 75\%$.

### 2. Subject Matrix: Speed vs. Mastery
Tracks each of the 6 core syllabi divided into two analytical clusters:
- **Cluster A (Financial & Assurance):** FAR, AFAR, AUD. Emphasizes calculation latency, adjusting entries, and standard balance derivations.
- **Cluster B (Regulatory & Advisory):** TAX, MAS, RFBT. Emphasizes reading speed, legal threshold recall, and managerial decision trees.

### 3. Ebbinghaus Memory Decay Index
- Measures the predicted probability of recall failure for previously mastered topics over elapsed time:

$$R = e^{-\frac{t}{S}}$$

- Where $t$ is time elapsed and $S$ is memory stability determined by past repetition intervals.

---

## 3. Data Flow & Local Computation

```
[ Question Answered / Card Reviewed ]
                   │
                   ▼
[ Background Dart Isolate (Zero UI Lag) ]
  - Updates rolling average response latency
  - Updates Bayesian topic mastery weight
  - Recalculates decay index per syllabus topic
                   │
                   ▼
[ Written to Local Analytics Table ]
                   │
                   ▼
[ Reactive Flutter UI Stream (ValueNotifier / Bloc) Updates Dashboard ]
```

---

## 4. Database Schema (ObjectBox / Drift)
```dart
class SubjectPerformanceMetric {
  int id;
  String subjectCode;         // "FAR", "TAX", etc.
  int totalAttempts;
  int correctAttempts;
  double accuracyPercentage;  // e.g., 89.2%
  double averageLatencySeconds; // e.g., 44.5s
  double projectedBoardScore;   // Estimated scaled board rating
  DateTime lastCalculatedAt;
}

class TopicDecayRecord {
  int id;
  String topicName;
  String subjectCode;
  double currentRecallProbability; // 0.0 to 1.0
  DateTime lastReviewedAt;
  bool isUrgentReviewDue;
}
```

---

## 5. Engineering Constraints & Edge Cases
- **UI Thread Isolation:** Never run rolling regressions or heavy statistical recalculations on the Flutter main UI thread. All Bayesian updates must run inside a background `Isolate`.
- **Cold Start Behavior:** When a user is new (< 50 questions answered), display clear onboarding confidence intervals (e.g., *"Confidence: Low - Complete 50 more items to calibrate your predicted score"*).

