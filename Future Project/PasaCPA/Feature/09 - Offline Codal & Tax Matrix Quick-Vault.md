---
title: Offline Codal & Tax Matrix Quick-Vault
category: Reviewer Reference & Tooling
doc-status: Planned
priority: P1
created: 2026-10-28
target_subjects:
  - TAX
  - RFBT
  - AUD
  - FAR
  - AFAR
  - MAS
---

# Offline Codal & Tax Matrix Quick-Vault

## 1. Overview & Problem Statement
CPALE examinees constantly lose study momentum when reviewing offline in transit because they need to verify statutory thresholds, tax percentages, or corporate voting quorums. Flipping through 800-page physical codals or opening bloated PDF viewers wastes time.

The **Offline Codal & Tax Matrix Quick-Vault** is a lightweight, instant-search reference library pre-cached inside the app. It provides instant lookup for Philippine tax schedules, statutory thresholds, and standard directories with zero network latency.

---

## 2. Core Reference Matrices Included

### A. Corporate Income Tax Matrix (CREATE Act / RA 11534)
- **Domestic MSME:** $20\%$ RCIT (Total Assets $\le ₱100\text{M}$ excluding land AND Net Taxable Income $\le ₱5\text{M}$).
- **Standard Domestic / Resident Foreign:** $25\%$ RCIT.
- **Minimum Corporate Income Tax (MCIT):** $2\%$ of Gross Income (1% temporary window July 1, 2020 – June 30, 2023).
- **Improperly Accumulated Earnings Tax (IAET):** Repealed under CREATE.

### B. Graduated Individual Income Tax Brackets (TRAIN Act / RA 10963)
- Revised 2023 onwards graduated tax brackets ($0\%$ up to $₱250\text{k}$; graduating to $35\%$ for $> ₱8\text{M}$).
- **Optional 8% Gross Income Tax:** Criteria, qualification tests, and $₱250\text{k}$ deduction eligibility for pure business/professional income.

### C. Withholding Tax & De Minimis Schedules
- **Expanded Withholding Tax (EWT):** Quick-lookup rates for professional fees ($5\%/10\%$ individuals, $10\%/15\%$ corporate), rentals ($5\%$), contractor fees ($2\%$).
- **Final Withholding Tax (FWT):** Bank interest, dividends, royalties, capital gains tax on real property ($6\%$) and shares of stock ($15\%$).
- **De Minimis Ceilings:** Monetized leave credits, medical allowances, rice subsidy ($₱2,000/\text{mo}$), and the statutory $₱90,000$ 13th month & other benefits threshold.

### D. Ease of Paying Taxes (EOPT Act / RA 11976) Matrix
- Taxpayer classification brackets: Micro ($< ₱3\text{M}$), Small ($₱3\text{M} - ₱20\text{M}$), Medium ($₱20\text{M} - ₱1\text{B}$), Large ($\ge ₱1\text{B}$).
- Invoicing and accrual basis rules, filing venue flexibilities, and reduced penalties for micro/small taxpayers.

### E. Revised Corporation Code (RCCP / RA 11232) Voting Thresholds
- **Majority of BOD + 2/3 Outstanding Capital Stock (OCS):** Amendment of AOI, merger/consolidation, sale of substantially all corporate assets, increase/decrease of capital stock.
- **Majority of Quorum of BOD:** Regular corporate resolutions.
- **Appraisal Right Triggers & Deadlines:** 30-day demand window, fair valuation mechanics.

### F. PFRS / PAS and PSA Standards Directory
- Searchable index linking every standard number to its official title and core accounting scope (e.g., *PAS 12: Income Taxes*, *PFRS 9: Financial Instruments*, *PFRS 16: Leases*, *PSA 700: Forming an Opinion*).

---

## 3. UX & Ergonomics
- **Global Quick-Search:** Instant full-text fuzzy search (e.g., typing `"MSME"` or `"Rice subsidy"` returns the exact statutory excerpt in $< 50\text{ms}$).
- **Split-Screen In-Exam Dock:** During practice drills, examinees can slide open the Quick-Vault without exiting the problem screen.
- **Copy to Calculator:** Tap any statutory percentage or threshold to copy it directly into the calculator register.

---

## 4. Technical Architecture & Database Schema
```dart
class QuickReferenceEntry {
  int id;
  String category;        // "TAX_TABLE", "RCCP_VOTING", "PFRS_STANDARDS", "EOPT"
  String title;           // e.g., "CREATE Corporate MSME Ceiling"
  String statutoryCitation; // "RA 11534, Sec. 27(A)"
  String summaryMarkdown; // Concise tabular summary
  List<String> searchKeywords; // ["msme", "20%", "rcit", "100m", "5m"]
  DateTime lastStatutoryUpdate;
}
```

---

## 5. Engineering Constraints
- Pre-compiled SQLite FTS5 (Full-Text Search) table to ensure instant searching across thousands of legal clauses on low-end hardware.
- Delta-sync compatible: when the BIR issues new Revenue Regulations, only updated table records are patched via Supabase deltas.

