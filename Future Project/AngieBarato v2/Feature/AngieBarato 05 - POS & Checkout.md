---
title: "AngieBarato 05 - POS & Checkout"
category: Feature Spec
doc-status: Draft
priority: P0
milestone: M6
created: 2026-11-16
updated: 2026-11-16
tags:
  - angiebarato
  - feature
  - pos
---

# AngieBarato 05 - POS & Checkout

Part of [[AngieBarato v2 - Overview & Roadmap]]. Built in Milestone 6 of [[AngieBarato v2 - Master Build Tracker]]. Fixes F1, F4, F5, F9 in [[AngieBarato v2 - Existing System Analysis]].

## Purpose

Sell fast, with correct totals, with or without internet, and leave a record a manager can trust at the end of the day.

## How it works

**Cashier**
1. Signs in and opens a shift with an opening cash float.
2. Scans or searches items. The cart updates. Quantity changes with the keyboard.
3. Applies a discount if allowed. A larger one asks a manager for a PIN.
4. Presses Pay. Chooses cash, card, GCash, credit, or a mix. Enters the amount tendered. The change due is shown.
5. Completes the sale. The receipt prints. The cart clears.
6. At the end of the day, counts the drawer. The app shows expected versus counted and asks for a reason if they differ.

**Other flows:** hold a cart and resume it, look up a past sale, reprint a receipt, void a sale from the same shift, refund items from an older sale.

## Completing a sale (one transaction)

All of this happens in a single SQLite transaction in the main process, so it is all-or-nothing:

1. Recompute every line and the total with `shared/pricing.ts`, from the cached product prices. Browser values are never trusted (F1).
2. Assign the invoice number from the register's sequence (F5).
3. Insert `sales`, `sale_items` (with price and branch cost snapshots), and `sale_payments`.
4. Insert one `stock_movements` row per tracked item and update `stock_balances`.
5. For a credit sale, insert a `customer_ledger` invoice row.
6. Insert the approval references, the audit row, and the outbox row.
7. Send the receipt to the printer after the transaction commits.

When synced, `post_sale` on the server runs the same calculation, stores the sale, and adds flags if anything differs (see [[AngieBarato 02 - Offline Data & Sync]]).

## Tables

`shifts`, `sales`, `sale_items`, `sale_payments`, `sale_returns`, `sale_return_items`, `held_carts`, `receipt_prints`. Columns are in [[AngieBarato v2 - Architecture & Data Model]].

| Table | Notes |
| :--- | :--- |
| `shifts` | `device_id`, `opened_by`, `opened_at`, `opening_float`, `closed_at`, `counted_cash`, `expected_cash`, `variance`, `variance_reason` |
| `sales` | `invoice_number`, `shift_id`, `customer_id`, `subtotal`, `discount`, `tax`, `total`, `amount_paid`, `status`, `sale_day` (in the branch time zone), `flags`, `approval_ids` |
| `sale_items` | `product_id`, `name`, `qty`, `unit_price`, `unit_cost`, `discount`, `tax`, `line_total` |
| `sale_payments` | `method`, `amount`, `reference` (for card or GCash), `tendered`, `change` |

## Rules

- **One pricing module.** `shared/pricing.ts` is the only code that does sale math. The UI shows what it returns.
- **Split payments:** the payment lines must add up to the total, or the remainder becomes credit for a named customer. Cash change is only given from cash.
- **Credit sale:** needs a customer. The local balance and credit limit are checked. Over the limit needs `sales.credit_override` and a manager PIN, and the approval id is stored on the sale (F8, F4).
- **Discount limits** come from the role. A discount beyond it needs approval. Every approval is recorded.
- **Void:** only a sale from the same open shift, with approval, and it reverses stock and any customer ledger row. The invoice number stays and the sale shows `voided`.
- **Refund or return:** from any completed sale, with item selection, a reason, a restock choice (back to stock or damaged), and a refund method. Needs `sales.refund` and approval.
- **Strict stock** (optional per branch): block a sale if on-hand is too low. Otherwise the sale proceeds and the item is flagged (D3).
- **Held carts** are saved locally. They do not touch stock.
- **Receipts:** prints company info, branch, invoice number, cashier, items, discounts, tax, payments, change, and a footer from settings. A reprint is marked "COPY" and logged in `receipt_prints`.
- **A sale is never edited.** Corrections are voids or returns.

## Keyboard and hardware

- A keyboard-wedge barcode scanner works with no setup. A scan in the search field adds the item.
- Shortcuts: `F2` search, `F4` pay, `F6` hold, `Esc` cancel dialog. Shown with `Kbd`.
- ESC/POS thermal printing over USB or network and a cash drawer kick through the printer (D9). Print failure never blocks the sale. The receipt can be reprinted.

## Screens

See [[AngieBarato v2 - Astryx UI Map]]: a custom POS layout, Checkout Form inside a Dialog, Dialog Wizard for shift close and returns, Order Detail for a sale.

## Done when

- Offline test: open shift, scan 5 items, pay half cash and half GCash, print, sync, and the server total equals the device total.
- A sale with a tampered browser price still totals correctly, because the main process recomputes it.
- Voiding and refunding both need a manager PIN and appear in the audit log with the approver.
- Closing a shift with a cash difference requires a reason, and the shift report shows it.
- The keyboard alone can complete a sale.
