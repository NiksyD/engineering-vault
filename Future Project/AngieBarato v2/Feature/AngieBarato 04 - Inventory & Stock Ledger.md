---
title: "AngieBarato 04 - Inventory & Stock Ledger"
category: Feature Spec
doc-status: Draft
priority: P0
milestone: M5
created: 2026-11-16
updated: 2026-11-16
tags:
  - angiebarato
  - feature
  - inventory
---

# AngieBarato 04 - Inventory & Stock Ledger

Part of [[AngieBarato v2 - Overview & Roadmap]]. Built in Milestone 5 of [[AngieBarato v2 - Master Build Tracker]]. Fixes F7 and F10 in [[AngieBarato v2 - Existing System Analysis]].

## Purpose

Know how many of each item every branch holds, why the number changed, and what it cost.

## The idea

In v1, `branch_inventory.current_stock` is a number that each action adds to or subtracts from. In v2, stock is a **ledger**: a list of movements that never changes. On-hand is the sum of the movements. The cached `stock_balances` row is a speed-up that is always rebuilt from the ledger when in doubt.

## Tables

**`stock_movements`** (append only)

| Column | Meaning |
| :--- | :--- |
| `id`, `branch_id`, `product_id` | which item, where |
| `qty` | signed quantity (positive in, negative out) |
| `unit_cost_centavos` | cost of this movement |
| `reason` | `sale`, `sale_return`, `void`, `receipt`, `transfer_out`, `transfer_in`, `adjustment`, `count_variance`, `opening` |
| `ref_table`, `ref_id` | the document that caused it |
| `actor_id`, `device_id`, `created_at` | who and where |

**`stock_balances`**: `branch_id`, `product_id`, `on_hand`, `avg_cost_centavos`, `last_movement_at`. Updated in the same transaction as the movement.

**`stock_counts` and `stock_count_lines`**: `branch_id`, `status`, and per line `counted_qty`, `system_qty` at count time, `variance`.

## How stock moves

| Event | Movement |
| :--- | :--- |
| Sale | `-qty` per item, cost snapshot saved on the sale item |
| Return to stock | `+qty` |
| Void | `+qty`, reverses the sale's movements |
| Goods receipt | `+qty` at the received cost, updates average cost |
| Transfer sent | `-qty` at the source branch |
| Transfer received | `+qty` at the destination at the source's average cost |
| Adjustment | signed, with a reason code |
| Count variance | signed, posted when a count is approved |

## Cost

- **Moving average per branch.** When goods arrive: `new_avg = (old_on_hand * old_avg + qty * unit_cost) / (old_on_hand + qty)`, rounded to a centavo, with the rule tested (F10).
- A transfer carries the source branch's average cost to the destination.
- A sale item stores the branch's average cost at the time of the sale. Profit reports use that stored value.
- If on-hand is zero or negative when goods arrive, the average becomes the new unit cost.

## Rules

- **Only the ledger writer** (`services/stock`) changes `stock_balances`. No other code touches it.
- **Negative stock is allowed and flagged** by default (D3). A branch can turn on "strict stock" to stop sales at zero.
- **Adjustments need a reason code.** Above a value threshold, they need manager approval. Losses and damage show in their own report.
- **A stock count freezes the system quantity at the time counting starts**, so sales during counting are not counted twice. On approval, the variance is posted as movements.
- **Reconciliation:** a job compares each `stock_balances.on_hand` with the ledger sum and lists every difference. It must always be empty.
- **Non-stock items** (`track_inventory = false`, for example a service) never create movements.

## Screens

See [[AngieBarato v2 - Astryx UI Map]]: Grouped Table (stock on hand), Searchable Table (movements), Inline Wizard (stock count), Dialog (adjustment).

- Stock on hand by branch with low-stock, out-of-stock, and negative badges.
- Movement history per product, with the document each came from.
- Adjustment dialog with product picker, quantity, reason, and approval when needed.
- Stock count: pick scope (all, category, or aisle list), count by scan or entry, review variances, submit, approve.
- A stock valuation report: on-hand times average cost, by branch and category.

## Done when

- A test applies 1,000 random movements across 3 branches and on-hand equals the ledger sum for every product.
- Receiving 10 at cost 100 on top of 10 at cost 80 gives an average of 90.
- A stock count with 3 variances posts 3 movements only after approval, and the audit log links to the count.
- The reconciliation job returns an empty list on the pilot database after a week.
