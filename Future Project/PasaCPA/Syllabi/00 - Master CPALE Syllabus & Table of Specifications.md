---
title: "Master CPALE Syllabus & Table of Specifications"
category: CPALE Master Reference
doc-status: Official (PRC BOA Res. No. 2022-30)
effective_date: October 2022 Examination to Present
total_subjects: 6
total_items: 450 (5 x 70 MCQs + 1 x 100 MCQs)
total_exam_hours: 18.0 (3 hours per subject)
created: 2026-10-31
tags:
  - cpale
  - syllabus
  - table-of-specifications
  - boa
---

# Master CPALE Syllabus & Table of Specifications (TOS)
**Professional Regulatory Board of Accountancy (PRC BOA) Resolution No. 2022-30**  
*Effective Beginning the October 2022 Licensure Examination for Certified Public Accountants (LECPA)*

> [!IMPORTANT] Core Board Rules & Standards Policy
> 1. **Passing Requirements:** A candidate must obtain a **General Weighted Average (GWA) of at least 75%**, with **no grade lower than 60%** in any given subject.
> 2. **Conditioned Status:** A candidate who obtains a GWA of at least 75% but fails in not more than two (2) subjects (scores below 60%) shall be deemed *Conditioned*. The candidate must re-examine in the conditioned subjects within two (2) years and obtain a grade of at least 75% in each.
> 3. **Refresher Course Rule:** Any candidate who fails in two (2) complete examinations shall be disqualified from taking another examination unless they submit evidence of completion of at least twenty-four (24) units of refresher courses in an accredited school.
> 4. **Superseding Rule:** New laws, standards, and other issuances which are effective as of the date of the examination shall supersede related topics listed in the syllabi and will be included in the examination unless there is an advisory from the Board of Accountancy to the contrary.

## 1. Official 3-Day Board Exam Timetable & Subject Breakdown
| Day & Time Slot | Subject Code | Subject Title | Questions | Time per Item | Dedicated Syllabus Note |
| :--- | :---: | :--- | :---: | :---: | :--- |
| **Day 1: 8:00 AM - 11:00 AM** | `MS` | Management Services | 70 MCQs | ~2.57 min | [[03 - Management Services (MS) Syllabus\|MS Syllabus & Checklist]] |
| **Day 1: 1:00 PM - 4:00 PM** | `AUD` | Auditing | 70 MCQs | ~2.57 min | [[04 - Auditing (AUD) Syllabus\|AUD Syllabus & Checklist]] |
| **Day 2: 8:00 AM - 11:00 AM** | `TAX` | Taxation | 70 MCQs | ~2.57 min | [[06 - Taxation (TAX) Syllabus\|TAX Syllabus & Checklist]] |
| **Day 2: 1:00 PM - 4:00 PM** | `RFBT` | Regulatory Framework for Business Transactions | **100 MCQs** | **~1.80 min** | [[05 - Regulatory Framework for Business Transactions (RFBT) Syllabus\|RFBT Syllabus & Checklist]] |
| **Day 3: 8:00 AM - 11:00 AM** | `FAR` | Financial Accounting and Reporting | 70 MCQs | ~2.57 min | [[01 - Financial Accounting and Reporting (FAR) Syllabus\|FAR Syllabus & Checklist]] |
| **Day 3: 1:00 PM - 4:00 PM** | `AFAR` | Advanced Financial Accounting and Reporting | 70 MCQs | ~2.57 min | [[02 - Advanced Financial Accounting and Reporting (AFAR) Syllabus\|AFAR Syllabus & Checklist]] |
| **TOTAL** | — | **6 Subjects Across 3 Days** | **450 MCQs** | — | **1,122 Syllabus Line Items** |

## 2. Table of Specifications (TOS) Cognitive Weighting
The PRC Board of Accountancy structures questions according to three cognitive taxonomy tiers:

| Cognitive Tier | Description & Examination Focus | Approximate Weight | Board Strategy & Triage |
| :--- | :--- | :---: | :--- |
| **Level 1: Remembering & Understanding** | Basic recall of legal provisions, statutory thresholds, standard definitions, accounting concepts, and ethical rules. | **30% – 35%** | Answer in <45 seconds. High recall efficiency banks time for calculation-heavy sections. |
| **Level 2: Applying & Analyzing** | Routine computational problems, journal entry determination, financial ratio calculations, standard tax returns, and standard cost variances. | **45% – 50%** | Standard 2-minute cadence. Rely on pure Dart deterministic math and Casio JW-200SC memory registers. |
| **Level 3: Evaluating & Creating** | Multi-step monster caselets, consolidated elimination worksheets, complex tax planning scenarios, and forensic audit investigations. | **15% – 20%** | Time trap alert. Triage to end of exam session; eliminate obvious distractors and solve systematically. |

## 3. PasaCPA Architecture Alignment
How these 6 official syllabi are wired into the local-first PasaCPA engine:

- **Drift SQLite Tagging:** Every question in `ExamQuestion` is tagged with `syllabusTopicId` (e.g. `FAR.8.2.1` for Leases, `TAX.3.2.1` for Corporate Income Tax), enabling granular performance tracking.
- **FSRS Flashcard Decks:** Flashcards are automatically generated from syllabus leaf topics tagged with legal bases and accounting definitions.
- **Casio JW-200SC Engine:** The pure Dart offline calculator replicates the official exam calculator with Grand Total (GT) and K-Constant division for rapid discounting.
- **3-Day Board Gauntlet Simulator:** Simulates the actual 3-day timetable with automatic BOA grading rules (GWA calculation, conditioned flag, passing curve).

## 4. Subject Syllabus Direct Links
- [[01 - Financial Accounting and Reporting (FAR) Syllabus]] (Annex A — 70 MCQs, 9 Major Sections, 157 Items)
- [[02 - Advanced Financial Accounting and Reporting (AFAR) Syllabus]] (Annex B — 70 MCQs, 14 Major Sections, 168 Items)
- [[03 - Management Services (MS) Syllabus]] (Annex C — 70 MCQs, 3 Major Sections, 106 Items)
- [[04 - Auditing (AUD) Syllabus]] (Annex D — 70 MCQs, 2 Major Sections, 158 Items)
- [[05 - Regulatory Framework for Business Transactions (RFBT) Syllabus]] (Annex E — 100 MCQs, 8 Major Sections, 427 Items)
- [[06 - Taxation (TAX) Syllabus]] (Annex F — 70 MCQs, 9 Major Sections, 106 Items)
