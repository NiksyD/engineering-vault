---
title: UCJ-104 Credit Request Table
status: in-progress
project: UCJobs
priority: high
created: 2026-10-20 15:10
tags:
  - ticket
  - dev
  - table
  - sorting
---

# UCJ-104 Credit Request Table

## 📌 Problem / Requirement Description
Display an interactive Credit Request table for the Admin module with strict column sorting, format rules, and stable sort requirements.

---

## 📋 User Acceptance Criteria

### 1. Table Columns & Data Formatting
- [ ] **ID**: Sequential row number of each record currently displayed (for display purposes only; does NOT change when sorting). No angle-down sort icon.
- [ ] **User Name**: Formatted as \`First Name Last Name\`. Sortable.
- [ ] **Amount**: Credit amount requested by the user. Sortable.
- [ ] **Balance**: User's current credit balance excluding requested amount. Sortable.
- [ ] **Date Requested**: Formatted as \`Month (Shortened) Day, Year, Time\` (e.g. \`Oct 20, 2026, 3:10 PM\`). Sortable.
- [ ] **Status**: Displays one of three states:
  - \`Approved\`: Added to user balance by Admin.
  - \`Pending\`: Awaiting Admin approval or rejection.
  - \`Rejected\`: Declined by Admin, no credit added.
  - Sortable.
- [ ] **Action**: Displays both Approve and Reject action buttons/modal triggers.

### 2. Sorting Behavior & Rules
- [ ] **User Name**:
  - 1st click: \`A-Z\` (alphabetical)
  - 2nd click: \`Z-A\` (reverse alphabetical)
- [ ] **Amount & Balance**:
  - 1st click: Lowest to Highest (ascending)
  - 2nd click: Highest to Lowest (descending)
- [ ] **Date Requested**:
  - 1st click: Most Recent to Oldest (newest first)
  - 2nd click: Oldest to Most Recent
- [ ] **Status**:
  - 1st click: \`Pending -> Approved -> Rejected\`
  - 2nd click: \`Rejected -> Approved -> Pending\`
- [ ] **Stable Sort Requirement**:
  - If two or more records have the same value for the active sort column, maintain their original relative order (e.g. tie-breaker preserves original index).
- [ ] **Icon Indicator**:
  - Angle-down icon displayed on sortable column headers; omitted on the ID column.

---

## 🏗️ Architecture & Component Context
- **Target Repo**: \`ucjobs-web\`
- **Relevant Directory**: \`app/admin/credit-requests\` or \`components/credit-requests/\`
- **Tech Stack**: React 19, Next.js 16, Tailwind CSS v4, Lucide icons (\`ChevronDown\`, \`ChevronUp\`)

---

## 🧠 Claude / Antigravity Implementation Plan

### Step 1: Types & Sorting Utility (Stable Sort)
- Define TypeScript interfaces:
  \`\`\`ts
  export type CreditRequestStatus = "Pending" | "Approved" | "Rejected";

  export interface CreditRequestRecord {
    id: string; // unique entity id
    firstName: string;
    lastName: string;
    amount: number;
    balance: number;
    dateRequested: string; // ISO timestamp
    status: CreditRequestStatus;
  }
  \`\`\`
- Implement a custom \`sortCreditRequests(records, sortKey, sortDirection)\` function with index tie-breaker to ensure 100% stable sorting.
- Custom rank map for Status sorting:
  \`\`\`ts
  const STATUS_RANK_ASC = { Pending: 1, Approved: 2, Rejected: 3 };
  \`\`\`

### Step 2: Date & Currency Formatting Helpers
- Format date to \`MMM D, YYYY, h:mm A\` using native \`Intl.DateTimeFormat\`.
- Format amount/balance with proper currency localization.

### Step 3: Table Header & Row Component
- Render row index dynamically (\`index + 1\`) for the ID column so it remains strictly 1..N regardless of sort.
- Wire \`ChevronDown\` icon rotation / state toggle on clickable headers.
- Render Approve/Reject action handlers.

### Step 4: Verification & Tests
- Add a Vitest spec (\`credit-request-table.test.tsx\`) verifying:
  - Stable sort preserves original relative order on equal values (e.g. Juan Dela Cruz vs Antonio Luna).
  - ID column remains 1..N after sort.
  - Status follows \`Pending -> Approved -> Rejected\` order.

---

## 📝 Work Notes & Investigation Scratchpad
- 

---

## 🚀 Testing & Verification
- [ ] \`npm run type-check\` passes with zero errors
- [ ] \`npm run lint\` passes
- [ ] Vitest test suite passes for stable sorting
