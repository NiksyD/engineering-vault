---
title: "AngieBarato 07 - Procurement & Transfers"
category: Feature Spec
doc-status: Draft
priority: P1
milestone: M8
created: 2026-11-16
updated: 2026-11-16
tags:
  - angiebarato
  - feature
  - procurement
  - transfers
---

# AngieBarato 07 - Procurement & Transfers

Part of [[AngieBarato v2 - Overview & Roadmap]]. Built in Milestone 8 of [[AngieBarato v2 - Master Build Tracker]]. Fixes F10 and F11 in [[AngieBarato v2 - Existing System Analysis]].

## Purpose

Order from suppliers, receive deliveries in parts, pay for them, and move stock between branches, with every step recorded in the stock ledger.

## Purchase orders

**Flow:** `draft` → `ordered` → `partially_received` → `received`. A `draft` or `ordered` order can be `cancelled`.

1. A user with `procurement.manage` creates a draft: supplier, branch, expected date, and items with quantity and unit cost.
2. The order is marked `ordered` (and printed or exported for the supplier). It can no longer be edited, except by cancelling.
3. When a delivery arrives, a **goods receipt** is created against the order: for each item, the quantity actually received, plus a note.
4. Posting the receipt adds `receipt` movements to the ledger, updates the branch's average cost (see [[AngieBarato 04 - Inventory & Stock Ledger]]), and updates the order to `partially_received` or `received`.

**Rules**
- Several receipts can exist for one order. Received quantity cannot exceed ordered quantity unless the user has `procurement.over_receive` and a reason is given.
- **A received order cannot be cancelled** (F11). A mistake is corrected by a return-to-supplier adjustment.
- Unit cost on a receipt may differ from the order. Both are stored, and the difference shows on the receipt.
- A supplier payment is recorded against a received order, with a method, a reference, and a date. The order shows unpaid, partly paid, or paid.

**Tables:** `suppliers`, `purchase_orders`, `purchase_order_items`, `goods_receipts`, `goods_receipt_items`, `supplier_payments`.

## Transfers

**Flow:** `draft` → `in_transit` → `received` (or `received_with_variance`). A `draft` can be `cancelled`.

1. A user with `inventory.transfer` creates a transfer from branch A to branch B with items and quantities.
2. **Send:** stock leaves A. One `transfer_out` movement per item, at A's average cost. The transfer is now `in_transit`.
3. **Receive** at B: the user enters the received quantity per item. One `transfer_in` movement per item, at the cost A sent.
4. If a received quantity is lower than sent, the transfer ends as `received_with_variance`. The shortfall needs manager approval and becomes a loss adjustment linked to the transfer, created by the real user, not by `'system'` (F11).
5. A transfer can be received only by a user of the destination branch.

**Rules**
- Stock in transit is shown as its own number, not counted in either branch.
- A sent transfer cannot be cancelled. If the goods come back, it is received at the source branch as a return transfer.
- Received quantity cannot exceed sent quantity.

**Tables:** `transfers` (`from_branch_id`, `to_branch_id`, `status`, `sent_by`, `sent_at`, `received_by`, `received_at`), `transfer_items` (`product_id`, `qty_sent`, `qty_received`, `unit_cost`).

## Suppliers

`suppliers`: name, contact person, phone, email, address, tax id, payment terms, notes, `is_active`. A supplier with orders cannot be deleted. It is deactivated.

## State machine tests

Every disallowed move is a test that must fail with a clear message: for example `received` to `cancelled`, `in_transit` to `draft`, receiving a cancelled order, and receiving a transfer twice.

## Offline behavior

Purchase orders and transfers work offline. A transfer's send and receive happen on two different devices, so the receiving device sees an `in_transit` transfer only after sync. Until then it cannot be received. The screen explains this.

## Screens

See [[AngieBarato v2 - Astryx UI Map]]: Form Wizard (new order), Order Detail (order and receipt), Inbox Table or Filterable Table (transfers), Dialog Wizard (receive).

## Done when

- An order for 100 units is received as 60, then 40. After each receipt the on-hand and the average cost are correct, and the order status follows.
- A transfer of 10 where 8 arrive creates the variance with the receiver's name and a manager approval.
- Each disallowed transition is rejected in the service and by a database check.
