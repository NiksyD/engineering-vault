---
title: On-Device Case Study Generator
category: Local AI
status: Planned
priority: P1
created: 2026-10-28
target_subjects:
  - AFAR
  - AUD
  - FAR
  - TAX
  - MAS
---

# On-Device Case Study Generator (Parametric Scenario Mutator)

## 1. Overview & Problem Statement
A notorious trap in CPALE review is **rote memorization**. Students who answer the same test banks repeatedly begin recognizing problem stems by company names or memorized figures (e.g., remembering that "Apex Holdings = ₱840,000") without actually computing or understanding the accounting principles.

The **On-Device Case Study Generator** uses structured templates combined with local LLM synthesis to dynamically mutate variables, transaction conditions, and tax years. This ensures examinees always face fresh, un-memorized scenarios that test true conceptual mastery.

---

## 2. Key Use Cases by Subject
* **AFAR (Partnership Liquidation & Installment Sales):** Altering partner profit/loss ratios, capital deficiency balances, or inventory repossession default percentages.
* **FAR (Leases & Financial Instruments):** Modifying incremental borrowing rates, lease terms, residual value guarantees, and amortization tables.
* **TAX (Corporate & Individual Income Tax):** Flipping MSME threshold tests (e.g., increasing total assets from ₱85M to ₱115M to trigger standard 25% RCIT instead of 20%).
* **AUD (Substantive Testing & Sampling):** Synthesizing different audit findings (e.g., unrecorded liabilities or cutoff errors) to test adjusting journal entries.

---

## 3. Architecture & Generation Pipeline
To prevent LLM hallucination in accounting math, a **Hybrid Parametric Engine** is used:

```
[ Base Template (Verified Formula Model) ]
                    │
                    ▼
[ Parametric Variable Mutator (Deterministic Math Engine in Dart) ]
  - Generates new compliant numbers & calculates verified ground-truth key
                    │
                    ▼
[ Local LLM (Gemini Nano / Gemma 2B) ]
  - Rewrites narrative case study, company story, and distractor options
                    │
                    ▼
[ Validated Generated Question Saved to Local DB ]
```

### Why Hybrid beats Pure LLM:
Never allow a small local LLM to independently invent accounting arithmetic without supervision. By having Dart calculate the numbers deterministically and using the local LLM strictly for natural-language narrative variation, answers are guaranteed to be mathematically 100% correct.

---

## 4. UI/UX Workflow
- When reviewing a completed question, a button labeled **"⚡ Mutate Problem (New Numbers)"** is displayed.
- The UI triggers a 1.5–3s local synthesis animation.
- A new variation replaces the problem stem with refreshed figures, and the MCQ choices recalculate accordingly.
- Tracks whether the user still gets the problem right when numbers change.

---

## 5. Engineering Constraints & Edge Cases
- **Statutory Boundaries:** Variable mutation scripts must obey statutory limits (e.g., Philippine tax rates must stick to 0%, 20%, 25%, 2% MCIT, 1% temporary MCIT periods; VAT remains 12%).
- **Cache Management:** Mutated questions are saved with a `parentQuestionId` reference and marked as `isSynthetic: true` so users can reset or purge synthesized questions to reclaim storage.

