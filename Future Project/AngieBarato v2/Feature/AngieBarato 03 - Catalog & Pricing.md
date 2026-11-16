---
title: "AngieBarato 03 - Catalog & Pricing"
category: Feature Spec
doc-status: Draft
priority: P0
milestone: M1, M4
created: 2026-11-16
updated: 2026-11-16
tags:
  - angiebarato
  - feature
  - catalog
---

# AngieBarato 03 - Catalog & Pricing

Part of [[AngieBarato v2 - Overview & Roadmap]]. Built in Milestone 4 of [[AngieBarato v2 - Master Build Tracker]]. Fixes F12 and part of F10 in [[AngieBarato v2 - Existing System Analysis]].

## Purpose

One clean list of what the business sells, with prices that are the same on every device, and a history of every price change.

## What changes from v1 `products` and `branches`

### Products

| v1 column | v2 |
| :--- | :--- |
| `id serial` | `id uuid` (v7). A `legacy_id` column keeps the old integer for the import. |
| `product_name` | `name` |
| `category` (legacy text) | **Dropped.** Only `category_id` remains. |
| `price numeric` | `price_centavos bigint`. The default selling price. |
| `last_cost`, `cogs` | **Replaced.** Cost lives per branch in `stock_balances.avg_cost_centavos`. The product keeps one `standard_cost_centavos` used only as a starting guess. |
| `stock_threshold` | **Dropped.** The reorder point is per branch (`branch_products.reorder_point`). |
| `status text` | `is_active boolean` |
| `sku` | `sku`, unique when set |
| `barcode` | **Moved** to `product_barcodes` (a product can have many) |
| `image_url` | `image_path` (storage path, cached on the device) |
| (missing) | `unit` (pcs, kg, box), `is_taxable`, `track_inventory`, `brand`, `description`, `deleted_at`, `updated_at` |

### Branches

| v1 column | v2 |
| :--- | :--- |
| `id serial` | `id uuid` |
| `branch_name` | `name` |
| (missing) | `code` (unique, used in invoice numbers, for example `BR1`), `address`, `phone`, `tax_id`, `timezone`, `is_active`, `deleted_at` |
| `location`, `status` | `address` and `is_active` |

New table `devices` (register) belongs to a branch. See [[AngieBarato 01 - Access, Profiles & Audit]].

## Tables

- `categories`: `id`, `name`, `parent_id`, `sort_order`, `is_active`. Three levels at most.
- `products`, `product_barcodes` (`product_id`, `barcode` unique, `is_primary`, `pack_qty` default 1).
- `branch_products`: `branch_id`, `product_id`, `price_override_centavos` (nullable), `reorder_point`, `is_available`.
- `price_changes`: `product_id`, `branch_id` (nullable), `old`, `new`, `changed_by`, `reason`, `changed_at`.

## Pricing rules

- **Money is integer centavos.** The shared module `src/shared/money.ts` is the only place that converts to display text. `MoneyText` is the only component that shows it (F12).
- **Effective price** = branch override if set, otherwise the product price. Computed by `shared/pricing.ts`.
- **Tax:** a product is taxable or not. The business setting says whether prices include tax (D5). The module computes tax per line and rounds once, with the rule written in a comment and covered by tests.
- **Discounts** are line or cart level, a fixed amount or a percent, limited by role (for example a cashier up to 5 percent, more needs approval).
- **Changing a price** needs `catalog.price`, writes `price_changes`, and writes an audit row. It does not change past sales, because sale items snapshot price and cost.

## Screens

See [[AngieBarato v2 - Astryx UI Map]]: Filterable Table, Product Detail, Two-column Form, Tree Table.

- Products list with search by name, SKU, or barcode, and filters for category, active, and low stock.
- Product form with barcodes as a token input and an image upload.
- Bulk price change with a preview.
- CSV import and export with a preview and an error list.
- Barcode label printing.

## Rules

- A barcode is unique across the whole catalog, including inactive products.
- A product with stock history cannot be deleted. It is deactivated.
- A deactivated product stays visible in history and reports and is hidden in the POS.
- Names are trimmed, and duplicate active names show a warning, not an error.

## Done when

- An admin creates a product with two barcodes and a branch price. A second device shows it after sync, offline-capable.
- Scanning either barcode in the POS finds the product.
- A price change shows in the price history with the user and reason.
- The v1 import (M10) creates the same number of active products and branches, with a report of anything skipped.
