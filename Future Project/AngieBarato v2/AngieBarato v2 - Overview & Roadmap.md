---
title: "AngieBarato v2 - Overview & Roadmap"
category: Product Overview
doc-status: Active
priority: P0
created: 2026-11-16
updated: 2026-11-16
tags:
  - angiebarato
  - roadmap
  - overview
---

# AngieBarato v2 - Overview & Roadmap

AngieBarato v2 is a desktop point-of-sale and inventory system for a small retail business with one or more branches. It is a rebuild of the v1 web app. v2 keeps working when the internet is down, and it treats stock and money as records that can be audited, not numbers that get overwritten.

This note is the entry point. Read it first, then follow the links.

**Planning notes**
- [[AngieBarato v2 - Master Build Tracker]]: the milestone checklist. Update it at the start and end of every task.
- [[AngieBarato v2 - Existing System Analysis]]: how v1 works today, and the flaws v2 must fix. Each flaw has a number (F1, F2, ...) that other notes refer to.
- [[AngieBarato v2 - Architecture & Data Model]]: stack, process layout, tables, state machines, security rules.
- [[AngieBarato v2 - Open Decisions]]: choices that are not settled yet, each with a recommendation.
- [[AngieBarato v2 - Astryx UI Map]]: which Astryx template and components to use for each screen.

**Feature specs**
- [[AngieBarato 01 - Access, Profiles & Audit]]
- [[AngieBarato 02 - Offline Data & Sync]]
- [[AngieBarato 03 - Catalog & Pricing]]
- [[AngieBarato 04 - Inventory & Stock Ledger]]
- [[AngieBarato 05 - POS & Checkout]]
- [[AngieBarato 06 - Customers, Credit & Payments]]
- [[AngieBarato 07 - Procurement & Transfers]]
- [[AngieBarato 08 - Reports & Dashboards]]

---

## 1. The problem

| Pain point | What v1 does today | Flaw |
| :--- | :--- | :--- |
| The shop cannot stop selling when the internet drops. | A browser-based offline queue in local storage. | F5, F6 |
| Sale totals, prices, and discounts come from the browser. | The server stores whatever the browser sends. | F1 |
| Any signed-in user can call most of the API. | Only admin and settings routes check permissions. | F2, F3 |
| Stock is one number that gets overwritten. | `current_stock` is changed by `+` and `-`, with no history and no limit. | F7 |
| Credit, payments, and returns are thin. | One payment method per sale, no returns, no voids, payments overwrite each other. | F8, F9 |

Details and file references are in [[AngieBarato v2 - Existing System Analysis]].

## 2. Who it is for

| Role | Uses the app to |
| :--- | :--- |
| **Cashier** | Sell, take payment, print receipts, hold a cart, count the drawer at shift end. |
| **Manager** | Approve overrides (discount, void, refund, credit over limit), adjust stock, receive deliveries, see branch reports. |
| **Admin / owner** | Manage branches, users, roles, prices, suppliers, and see all reports and the audit log. |

## 3. What makes v2 different

1. **Offline first.** Every screen reads and writes a local SQLite database. The internet is only used to sync, in the background.
2. **A sale is a fact once the customer has left.** Offline sales are accepted and flagged on sync (for example, stock went negative). They are never rejected.
3. **Stock and money are ledgers.** Stock on hand is the sum of movements. A customer balance is the sum of invoices minus payments. Nothing is overwritten.
4. **One set of rules, enforced in three places.** Row-level security in the database, permission checks in the actions, and hidden buttons in the UI.
5. **The price is computed in one shared module.** The same code runs in the app and on the server, in whole centavos, so totals always match.

## 4. The core flow

```
Supplier ──> Purchase order ──> Receive ──┐
                                          ├──> Stock ledger ──> Stock on hand
Transfer (branch to branch) ──────────────┤
Adjustment / count ───────────────────────┤
Sale / return / void ─────────────────────┘
                          │
Sale ──> Payment(s) ──> Shift totals ──> Reports
  └──> Credit sale ──> Customer ledger ──> Collection
```

Every arrow that moves stock writes a ledger row. Every arrow that moves money writes a payment row. Each row has a user, a device, a branch, and a time.

## 5. Scope of the first release

**In scope**
- Login with email and password, plus a PIN for quick unlock and approvals.
- Branches, registers (devices), users, roles, permissions.
- Products, barcodes, categories, per-branch price and reorder point.
- POS: scan, search, cart, hold, discounts, split payment, credit sale, receipt print, returns, voids, shifts.
- Stock ledger, adjustments, stock counts.
- Customers with credit limit, statement, and collections.
- Suppliers, purchase orders with partial receiving, branch transfers.
- Reports: daily sales, product performance, stock valuation, receivables, shift report.
- Audit log viewer.
- Background sync with a visible status.
- Installers and auto-update for Windows and Linux.

**Out of scope for the first release**
- Product variants (size, color).
- Multi-company (several businesses in one install). Decided out of scope (D1).
- Online store, loyalty points, e-wallet integrations.
- Full accounting (general ledger, tax filing). v2 exports data for the accountant.
- A mobile app. See D10.

## 6. Milestones

Details and checklists are in [[AngieBarato v2 - Master Build Tracker]].

| # | Milestone | Result |
| :-: | :--- | :--- |
| M0 | Foundation | The Electron app builds, themes with Astryx, and has the project rules written down. |
| M1 | Database and security | The v2 Supabase schema, row-level security, and tests exist. |
| M2 | App shell, accounts, roles | A user signs in and sees the screens their role allows. |
| M3 | Local data and sync | The app reads and writes SQLite and syncs with Supabase, tested with the network cut. |
| M4 | Catalog | Products, barcodes, categories, and branches are managed. |
| M5 | Inventory ledger | Stock is a ledger, with adjustments and stock counts. |
| M6 | POS and checkout | A cashier completes a sale offline, prints a receipt, and closes a shift. |
| M7 | Customers and credit | Credit sales, collections, and statements work. |
| M8 | Procurement and transfers | Deliveries and branch transfers move stock correctly. |
| M9 | Reports and audit | Managers see reports. Every sensitive action is in the audit log. |
| M10 | Migration and pilot | v1 data is imported and one branch runs on v2 for a real week. |

M3 comes before the feature milestones on purpose. Every feature after it is built on the local database, so building it first avoids rewriting each screen later.

## 7. Assumptions to check with the owner

These are guesses. Each one changes the design if it is wrong.

- [ ] How many registers does each branch have, and can two work offline at the same time?
- [ ] Epson thermal printer chosen (D9). Which model? Is there a cash drawer and a scanner?
- [ ] Must receipts follow a government format with numbered, gap-free invoices? Ask the accountant.
- [ ] Are prices entered with tax included or tax added on top?
- [x] Are credit sales allowed while offline? Yes (D4).
- [x] One business, several branches (D1).
- [x] v1 data to carry over: products, branches, users. No customer balances (D11).
- [ ] How long can a branch realistically be offline: minutes, or days?

## 8. What carries over from v1

| Carries over | Notes |
| :--- | :--- |
| Products and branches | Re-keyed with UUIDs, columns cleaned up. See [[AngieBarato 03 - Catalog & Pricing]]. |
| The module layout idea | Features grouped by business area (catalog, inventory, sales, procurement). Rebuilt with clear boundaries. |
| Roles and permissions model | Kept, with checks added on every action. |
| Barcode label printing | Reused through `jsbarcode`. |

| Does not carry over | Reason |
| :--- | :--- |
| The separate Next.js API project | Replaced by Postgres functions and a small Edge Function. See [[AngieBarato v2 - Architecture & Data Model]]. |
| shadcn and Radix components | Replaced by Astryx. |
| The localStorage offline queue | Replaced by SQLite and an outbox. |
| Client-computed totals | Replaced by the shared pricing module. |
| The mobile app (`angiebarato-mob`) | Parked. See D10. |
