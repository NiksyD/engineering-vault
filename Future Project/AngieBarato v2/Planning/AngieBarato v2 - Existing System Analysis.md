---
title: "AngieBarato v2 - Existing System Analysis"
category: Analysis
doc-status: Active
priority: P0
created: 2026-11-16
updated: 2026-11-16
tags:
  - angiebarato
  - analysis
  - v1-review
---

# AngieBarato v2 - Existing System Analysis

A review of v1 (`angiebarato/` web app, `angiebarato-api/` API, `angiebarato-mob/` mobile app). It lists how the business flow works today and every flaw v2 must fix. Part of [[AngieBarato v2 - Overview & Roadmap]].

**How this was done.** The knowledge graph in `angiebarato/graphify-out` (built 2026-10-27 at commit `1dc0b771`: 1,375 nodes, 64 communities) shows the shape of the code. About half of its communities are npm package metadata, so it is a weak guide to the business flow. The flow and the flaws below come from reading the routes, the schema, and the POS code directly. File references are given so each claim can be checked.

---

## 1. Structure of v1

| Part | What it is |
| :--- | :--- |
| `angiebarato/` | Next.js 16 web app, wrapped in Electron. The Electron `main.js` starts a Next.js server inside the desktop app. |
| `angiebarato-api/` | A second Next.js project used only as a REST API (about 40 routes), with Drizzle on Supabase Postgres. Deployed separately. |
| `angiebarato-mob/` | An Expo mobile app. |
| Database | Supabase Postgres, 19 tables, serial integer keys, plus `supabase/migrations` for row-level security. |

**What the graph does show.** The most connected nodes are `cn()` (218 edges), `Button()` (114), `authenticatedFetch()` (92), `Input()` (80), and `DashboardHeader()` (64). That means the UI is held together by shared styling helpers and one fetch wrapper. The `authenticatedFetch` community has cohesion 0.07, which means pages call the API in many different ways with no shared data layer. Every one of about 25 screens has its own hand-written service file.

## 2. The business flow in v1

**Procure to stock**
1. A supplier is created. A purchase order is made (`draft`, `sent`, `received`, `cancelled`).
2. Marking it `received` adds stock to `branch_inventory` and recomputes a moving-average cost on the product.

**Stock movement**
- Transfers go `send`, then `receive`. A shortfall on receive becomes a `loss` adjustment against the source branch, created by `'system'`.
- Adjustments (`damage`, `loss`, `correction`, `returned`) add or subtract from `current_stock`.

**Sell**
1. The cashier builds a cart in the POS. Totals, discount, and tax are computed in the browser.
2. The browser posts the sale. The server inserts the sale and items, reduces stock, and raises the customer balance for credit sales.
3. If the internet is down, the sale goes into a local-storage queue and is posted later.

**Collect**
- A receivable payment sets `amount_paid` on the sale to a new total and moves the customer balance by the difference.

**Report and audit**
- Reports read the sales table directly. An audit log row is written after most actions.

## 3. Flaws

Severity: **Critical** = money or security is wrong today. **High** = data becomes wrong over time. **Medium** = limits the business or slows the team.

### Critical

**F1. The server trusts totals and prices from the browser.**
`angiebarato-api/app/api/sales/route.ts` stores `subtotal`, `discount_amount`, `tax_amount`, `total_amount`, `unit_price`, and `payment_status` exactly as sent. It never reads the product price or recomputes anything. Anyone who can call the API can sell any item for any price.
*v2:* the server recomputes every sale from the product price table, and the shared pricing module is the only place math happens. See [[AngieBarato 05 - POS & Checkout]].

**F2. Most API routes have no permission check.**
`middleware.ts` only checks roles for `/api/admin/*` and non-GET `/api/settings`. A cashier, or any signed-in user, can create adjustments, receive purchase orders, cancel transfers, and read every branch's sales. Some routes never read the session at all (`inventory/adjustments` and `inventory/transfers/receive` do not look up the user; `created_by` is `'system'` or client-supplied). The middleware does require a valid login for every `/api` call, so this is about missing permission and branch checks, not anonymous access.
*v2:* every action checks a named permission, in the database and in the app. See [[AngieBarato 01 - Access, Profiles & Audit]].

**F3. Row-level security policies are open.**
`002_branches_inventory_rls_policies.sql` uses `USING (true)` on `branches` and `branch_inventory`, so the policies do not limit rows by branch or role. A later file is named `007_allow_public_branches.sql` (not reviewed line by line). Because the app ships the Supabase anon key, a signed-in user can talk to the database directly and skip the API checks. **To confirm before relying on it:** read all of migrations `001` to `014` and test with a cashier session.
*v2:* RLS is on every table with real predicates (branch, role), and is tested. See [[AngieBarato v2 - Architecture & Data Model]].

**F4. Weak PIN design.**
`utils/pin.ts` uses PBKDF2 with 1,000 iterations. `users/verify-pin` loads every active user with a PIN and returns the first manager whose PIN matches, so two managers with the same PIN are indistinguishable, and there is no rate limit and no lockout. The result is not tied to the action it approves, so an override cannot be proven later.
*v2:* a PIN approval is scoped to one action, one approver, and one document, with lockout and a stronger hash. See [[AngieBarato 01 - Access, Profiles & Audit]].

**F5. Invoice numbers can collide.**
`{prefix}{YYYYMMDD}-{random 4 digits}`. With 9,000 values per day, a busy day will hit a duplicate. The column is unique, so the insert fails with a 500. For an offline sale that is already complete, the failure leaves it stuck in the queue.
*v2:* a per-register, gap-free sequence. See [[AngieBarato 02 - Offline Data & Sync]].

### High

**F6. The offline queue can lose or duplicate sales.**
`lib/pos-offline-store.ts` keeps the queue in the browser's local storage. It sends an `offline_id`, but the server ignores it, so a request that succeeds but times out is sent again and creates a second sale. Clearing site data erases unsynced sales. The connectivity check pings a Supabase URL hardcoded as a fallback in the source. Failed sales stay in the list with an error and no way to fix them.
*v2:* a SQLite outbox with idempotency keys and a visible conflict screen. See [[AngieBarato 02 - Offline Data & Sync]].

**F7. Stock is a counter, can go negative silently, and has no history.**
Sales, adjustments, transfers, and receipts all do `current_stock = current_stock ± n`. There is no check that stock is available, and no way to rebuild the number if it is wrong. `purchase-orders/[id]/status` reads stock, then writes a new value, without a lock, so two receipts at once can lose one.
*v2:* an append-only stock ledger. On-hand is derived. See [[AngieBarato 04 - Inventory & Stock Ledger]].

**F8. Credit rules live only in the browser.**
The credit limit is checked in `checkout-dialog.tsx`. The "force credit sale" box is a client flag. The server never checks the limit and does not record who approved it. Collections (`sales/[id]/payment`) overwrite `amount_paid` with a new total, so there is no list of individual payments, no payment by cashier, and no way to reverse one.
*v2:* a payments table and a customer ledger, with server-side limit checks. See [[AngieBarato 06 - Customers, Credit & Payments]].

**F9. Missing retail basics.**
No returns, refunds, or voids. A sale has a single `payment_method`, so split payments (cash plus GCash) are impossible. No shifts, no opening float, no cash count, no end-of-day report. No held carts. No receipt reprint log.
*v2:* all of these. See [[AngieBarato 05 - POS & Checkout]].

**F10. Cost and profit are inconsistent.**
Moving-average cost is computed across all branches' stock and stored on the product. A sale snapshots `products.last_cost`, not the average. Transfers do not carry cost. Profit reports therefore mix two different cost ideas.
*v2:* one cost method, per branch, carried through transfers. See [[AngieBarato 04 - Inventory & Stock Ledger]].

**F11. Documents can move to any status.**
Purchase orders only block `received` to `received`. A received order can be set to `cancelled` with no stock reversal. Receiving is all-or-nothing, with no partial delivery. Transfer receive takes `received_by` from the request body.
*v2:* explicit state machines with allowed transitions. See [[AngieBarato 07 - Procurement & Transfers]].

**F12. Money is handled as JavaScript floats and numeric strings.**
`parseFloat`, `toFixed(2)`, and string columns appear throughout checkout and reports. Rounding differs between the browser total and the database sum.
*v2:* integer centavos everywhere. See [[AngieBarato 03 - Catalog & Pricing]].

### Medium

**F13. Three codebases for one product.** Web, API, and mobile are separate projects with duplicated types. A change to a table touches all three.
**F14. Giant components.** `checkout-dialog.tsx` is 980 lines and mixes tax math, credit rules, customer lookup, and printing. Payloads use `any`.
**F15. Realtime on every table** (migration `006`). It costs connections and widens what a client can subscribe to. Which screens actually use it was not checked.
**F16. Settings as free-text key and value.** `system_settings.value` is text. Nothing validates it, and types are lost.
**F17. Reports cast dates in SQL** (`created_at::date`), so indexes are not used, and the day boundary follows the server's time zone, not the branch's.
**F18. Audit log is fire-and-forget.** `logActivity` swallows its own errors and runs outside the transaction, so a sale can exist without its audit row, and the user can be `null`.
**F19. Heavy desktop packaging.** Electron starts a full Next.js server to show pages, and the build needs a 4 GB Node heap (`--max-old-space-size=4096`).

## 4. Summary table

| # | Flaw | Severity | Fixed in |
| :-: | :--- | :--- | :--- |
| F1 | Client-computed totals trusted | Critical | M6 |
| F2 | No permission checks on most routes | Critical | M1, M2 |
| F3 | Open RLS policies | Critical | M1 |
| F4 | Weak, unscoped PIN | Critical | M2, M6 |
| F5 | Random invoice numbers | Critical | M3, M6 |
| F6 | Offline queue loses or duplicates | High | M3 |
| F7 | Stock counter, no history | High | M5 |
| F8 | Credit and payments weak | High | M7 |
| F9 | No returns, split pay, shifts | High | M6 |
| F10 | Inconsistent cost | High | M5, M8 |
| F11 | Unrestricted status changes | High | M8 |
| F12 | Float money | High | M1 |
| F13 | Three codebases | Medium | M0 |
| F14 | Giant components | Medium | all |
| F15 | Realtime everywhere | Medium | M3 |
| F16 | Untyped settings | Medium | M2 |
| F17 | Date casts in reports | Medium | M9 |
| F18 | Audit outside the transaction | Medium | M1 |
| F19 | Heavy packaging | Medium | M0, M10 |

## 5. What v1 did well and v2 keeps

- The module folder layout (`catalog`, `inventory`, `sales`, `procurement`, `accounting`) matches how the business thinks. v2 uses the same grouping.
- Cost snapshots on sale items are the right idea. v2 keeps them, with a consistent cost source.
- The permission code convention (`inventory.view`, `sales.create`) is good and carries over.
- Cursor-based pagination on sales is the right approach for long lists.
- Barcode scan handling in the product grid and label printing both carry over as behavior.
