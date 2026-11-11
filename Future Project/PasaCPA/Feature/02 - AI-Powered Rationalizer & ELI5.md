---
title: AI-Powered Rationalizer & ELI5
category: Local AI
doc-status: Planned
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

# AI-Powered Rationalizer & ELI5

## 1. Overview & Problem Statement
Traditional reviewer answer keys provide static, one-sentence explanations (e.g., *"The answer is A because of Sec. 27(A)"*). When an examinee selects a wrong option (e.g., Option B: ₱1,050,000 using 25% RCIT), they are left wondering what calculation trap they fell into.

The **AI-Powered Rationalizer** uses an on-device Small Language Model (Gemini Nano via AICore or quantized Gemma 2B via MediaPipe) to evaluate the examinee's exact incorrect choice in real time, explaining the trap and demonstrating the correct formula derivation—100% offline.

---

## 2. Advanced CPALE Features

### A. Cascading Error Intelligence (Grouped Caselets)
In multi-item accounting problems (e.g., Item 18: Gross Profit $\rightarrow$ Item 19: Ending Inventory):
- If the examinee got Item 18 wrong, standard answer keys mark Item 19 wrong without explanation.
- The **AI Rationalizer checks for cascading premise errors**:
  - *"Your Item 19 calculation is mathematically consistent with your corrupted Year 1 Gross Profit from Item 18. If your initial ₱450,000 had been correct, your answer of ₱1,200,000 would hold. Here is how the correct Year 1 base changes the downstream balance..."*
  - This prevents students from losing confidence in a valid downstream method when the flaw was purely an upstream arithmetic slip.

### B. Distractor Trap Recognition
- Specifically targets classic review center "traps" (e.g., forgetting to add back non-deductible expenses, using gross instead of net sales for MCIT, or misapplying the de minimis 90k threshold).

---

## 3. User Experience & Interface
- **Trigger:** An "⚡ Ask On-Device AI" button in Practice Mode, or within the post-exam diagnostic review.
- **Dual-View Tabs:**
  1. **Step-by-Step Derivation:** Formal mathematical and statutory proof (e.g., Step 1: MSME qualification test $\rightarrow$ Step 2: RCIT calculation $\rightarrow$ Step 3: MCIT comparison).
  2. **Simplified Breakdown (ELI5):** High-level conversational explanation highlighting the rule of thumb and why common pitfalls occur.
- **Latency & Streaming:** Token streaming output so text begins rendering within 200–500ms of tapping the button.

---

## 4. Technical Pipeline & Prompt Architecture

```
[ Question Context + Accounting Ledger + Caselet History ]
                           │
                           ▼
[ Examinee Choice (e.g., "B") + Correct Key ("A") ]
                           │
                           ▼
[ On-Device Prompt Assembler (Local Dart/Kotlin) ]
                           │
                           ▼
[ Local LLM: Gemini Nano (AICore) / Gemma 2B (MediaPipe) ]
                           │
                           ▼
[ Markdown Formatted Rationale Streamed to UI ]
```

### System Prompt Template
```markdown
You are a top-performing Philippine CPA Reviewer and Board Exam Coach. 
Analyze the following accounting question and evaluate why the student failed:

[CASE CONTEXT]: {casePrompt}
[FINANCIAL DATA]: {tableDataJson}
[QUESTION]: {questionText}
[CORRECT ANSWER]: Option {correctOptionLetter}: {correctOptionText}
[STUDENT SELECTED]: Option {studentOptionLetter}: {studentOptionText}
[PREVIOUS CASELET STEP RESULT]: {previousStepContext}

TASK:
1. Explain the specific calculation or conceptual mistake that leads to Option {studentOptionLetter} (identify the distractor trap).
2. If this is a grouped caselet, check if the student's answer was logically consistent with an error made in the preceding sub-question.
3. Provide a clear, step-by-step legal or mathematical proof showing why Option {correctOptionLetter} is the sole correct answer under current Philippine accounting/tax standards.
4. Keep the tone concise, authoritative, and encouraging. Use standard accounting formatting (₱ symbols, underline final figures).
```

---

## 5. Engineering Constraints & Performance Budget
- **Model Quantization:** INT4 or INT8 quantized models (e.g., Gemma 2B / 1.2B) to stay under 1.5GB RAM usage.
- **Device Fallback Matrix:**
  - *Tier 1 (Flagship / AICore available):* Direct system inference via Android AICore (Gemini Nano). 0MB app storage footprint.
  - *Tier 2 (Mid-range / No AICore):* Bundled/downloaded MediaPipe Gemma 2B task file stored in internal app cache.
  - *Tier 3 (Low RAM < 4GB):* Display pre-compiled static author rationales with a note that local AI synthesis is disabled.
- **Cache Local Syntheses:** Save the markdown result to the local database so reopening the question never incurs a second inference run.
