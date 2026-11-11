---
title: Adaptive Flashcard Synthesizer & Spaced Repetition
category: Local AI & Learning Science
doc-status: Planned
priority: P0
created: 2026-10-28
target_subjects:
  - RFBT
  - AUD
  - TAX
  - FAR
  - AFAR
  - MAS
---

# Adaptive Flashcard Synthesizer & Spaced Repetition

## 1. Overview & Problem Statement
The Philippine CPALE requires intense memorization of hundreds of standards (PFRS/PAS), statutory laws (Corporation Code, NIRC, CREATE, EOPT), and auditing guidelines (PSA). Traditional static flashcard decks fail because:
1. They waste student time testing concepts the student already knows.
2. They don't adapt to individual memory decay.

The **Adaptive Flashcard Synthesizer** scans the examinee's weakest topics (based on wrong answers and slow response latency in the Exam Engine) and automatically synthesizes targeted active-recall cards using local AI. These cards are scheduled using a local **Spaced Repetition Algorithm (FSRS or SM-2)** to surface items right before recall failure.

---

## 2. Core User Experience
- **Interactive 3D Card Flip:** Clean card front showing prompt/difficulty; card back showing verified formulas, statutory legal basis, and criteria.
- **Recall Grading Buttons:**
  - `Forgot (+10m)`: Resets step, schedules card into the immediate review loop.
  - `Hard (+1d)`: Minor interval increase.
  - `Good (+3d)`: Standard interval multiplier.
  - `Mastered (+7d)`: Marks topic as consolidated; updates local mastery points.
- **Daily Due Badge:** Displays the exact count of cards due today based on the local spaced-repetition queue.

---

## 3. Local AI Synthesis Workflow
When the student scores $< 75\%$ in a specific topic (e.g., *Regulatory Framework: General Principles of Partnerships*), the app triggers background flashcard synthesis:

```
[ Local Analytics identifies Topic Blind Spot ]
                       │
                       ▼
[ Local LLM (Gemini Nano / Gemma 2B) ]
  Prompt: "Synthesize 3 active-recall flashcards on {Topic}. 
  Focus on the most heavily tested Philippine board exam exceptions, 
  thresholds, and formulas. Format as JSON."
                       │
                       ▼
[ Parsed JSON -> Saved into Local DB `Flashcard` table ]
                       │
                       ▼
[ Scheduled into the Spaced Repetition Review Queue ]
```

---

## 4. Spaced Repetition Mathematical Model
The system uses an on-device implementation of **FSRS (Free Spaced Repetition Scheduler)** or lightweight **SM-2**:

$$\text{Interval}_{n} = \text{Interval}_{n-1} \times \text{Ease Factor}$$

```dart
class Flashcard {
  int id;
  String subject;             // e.g., "RFBT"
  String topic;               // e.g., "Bouncing Checks Law (BP 22)"
  String promptFront;         // Front text / question
  String answerBack;          // Back text / formula / statutory criteria
  String statutoryReference;  // e.g., "BP Blg. 22, Sec. 2"
  
  // SRS Telemetry
  int repetitionCount;
  double easeFactor;          // Starts at 2.5
  int intervalDays;           // Days until next review
  DateTime nextReviewDueDate;
  DateTime lastReviewedAt;
  bool isAiSynthesized;
}
```

---

## 5. Engineering Constraints & Edge Cases
- **No Network Dependency:** All interval calculations, due-date sorting, and card reviews occur entirely inside the local SQLite/ObjectBox database.
- **Background Throttling:** Flashcard generation only triggers when the app is idle or plugged in to avoid competing for CPU/NPU cycles with an active timed mock exam.
- **Cap on Daily New Cards:** Prevent cognitive overload by capping new synthetic cards to a sensible user-configurable limit (default: 20 new cards/day).

