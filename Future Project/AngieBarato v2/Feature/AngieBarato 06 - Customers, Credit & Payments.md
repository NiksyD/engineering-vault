---
title: "AngieBarato 06 - Customers, Credit & Payments"
category: Feature Spec
doc-status: Draft
priority: P1
milestone: M7
created: 2026-11-16
updated: 2026-11-16
tags:
  - angiebarato
  - feature
  - customers
  - credit
---

# AngieBarato 06 - Customers, Credit & Payments

Part of [[AngieBarato v2 - Overview & Roadmap]]. Built in Milestone 7 of [[AngieBarato v2 - Master Build Tracker]]. Fixes F8 in [[AngieBarato v2 - Existing System Analysis]].

## Purpose

Let trusted customers buy on credit, collect what they owe in parts, and always be able to show how a balance was reached.

## The idea

In v1, a customer has `current_balance` that is raised and lowered by arithmetic, and a collection overwrites a sale's `amount_paid`. In v2, the balance is the sum of a **customer ledger**. Each credit sale, collection, and correction is its own row.

## Tables

**`customers`**: `id`, `name`, `phone`, `email`, `address`, `notes`, `credit_limit_centavos`, `is_active`, `created_at`, `updated_at`, `deleted_at`. There is no balance column. The balance is calculated from the ledger and cached in a view for display.

**`customer_ledger`** (append only)

| Column | Meaning |
| :--- | :--- |
| `customer_id`, `branch_id` | whose, where |
| `kind` | `invoice` (credit sale), `payment`, `return_credit`, `adjustment`, `opening` |
| `amount_centavos` | positive increases what the customer owes, negative reduces it |
| `ref_table`, `ref_id` | the sale or collection |
| `due_date` | for invoices |
| `actor_id`, `device_id`, `created_at` | who and where |

**`collections`**: a payment received from a customer: `id`, `customer_id`, `amount`, `method`, `reference`, `received_by`, `shift_id`, and `collection_allocations` (`collection_id`, `sale_id`, `amount`) saying which invoices it pays.

## How it works

1. A credit sale in the POS adds an `invoice` row for the unpaid part of the sale.
2. A manager or cashier with `customers.collect` opens the customer, presses Collect, enters the amount and method, and sees the open invoices.
3. By default the amount is applied to the oldest invoice first. The user can choose a different allocation.
4. The collection adds a negative `payment` row, and a receipt prints.
5. The collection belongs to the open shift, so it appears in the drawer count if paid in cash.

## Rules

- **Credit limit** is checked in the service and again in `post_sale`. The check uses the ledger sum plus the new sale.
- **Offline credit** is allowed within the last known limit minus a safety margin (D4). Two registers can still exceed it together. The server adds an `over_credit_limit` flag instead of rejecting.
- **An over-limit sale** needs `sales.credit_override` and a manager PIN. The approval id is saved on the sale.
- **No row is edited or deleted.** A mistaken collection is reversed with a new row that links to the original, with a reason and approval.
- **Overpayment** becomes a credit balance (negative balance), shown clearly, and can be used on the next credit sale.
- **Statement:** all rows for a period, with a running balance. It can be printed or exported.
- **Aging:** buckets of 0 to 30, 31 to 60, 61 to 90, and over 90 days, from each invoice's due date.
- **Walk-in customers** (no record) can only pay in full. Credit needs a customer record.

## Screens

See [[AngieBarato v2 - Astryx UI Map]]: Searchable Table (customers), Order Detail (customer statement), Dialog (collect).

- Customers list with balance, limit, and an over-limit badge.
- Customer detail: contact info, ledger with running balance, open invoices, Collect button.
- Receivables report with aging buckets.

## Done when

- A customer buys 1,000 on credit, pays 400 on one day and 600 on another, and the statement shows 3 rows with a balance of zero.
- The balance always equals the sum of ledger rows, tested with random data.
- An over-limit sale cannot complete without approval, and the approval is visible on the sale.
- Reversing a collection leaves both rows in the ledger.
