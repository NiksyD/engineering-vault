---
title: "AngieBarato 08 - Reports & Dashboards"
category: Feature Spec
doc-status: Draft
priority: P1
milestone: M9
created: 2026-11-16
updated: 2026-11-16
tags:
  - angiebarato
  - feature
  - reports
---

# AngieBarato 08 - Reports & Dashboards

Part of [[AngieBarato v2 - Overview & Roadmap]]. Built in Milestone 9 of [[AngieBarato v2 - Master Build Tracker]]. Fixes F17 and F18 in [[AngieBarato v2 - Existing System Analysis]].

## Purpose

Give the manager and owner the answers they need each day, quickly, from the device's own data, even offline.

## Where the numbers come from

- Reports read the **local SQLite** data, so they work offline and are fast. An owner who needs all branches reads the cloud data through a **branch rollup** (the same queries run in Postgres through views with `security_invoker = true`).
- Each report states which data it covers and when it last synced.
- Every sale stores `sale_day`, the date in the branch's time zone, computed when the sale is saved. Reports group by that column and use an index, not a date cast (F17).
- Profit uses the cost snapshot stored on each sale item.

## Reports

| Report | Contents | Who |
| :--- | :--- | :--- |
| **Dashboard** | Today's sales and count, average sale, top 5 products, low-stock count, open shifts, receivables due, sync health | Manager, admin |
| **Daily sales** | Sales by hour, by payment method, discounts, voids, returns, net total | Manager |
| **Shift report (Z report)** | Opening float, sales by method, collections, refunds, expected cash, counted cash, variance | Cashier (own), manager |
| **Product performance** | Quantity, revenue, cost, margin, by product and category | Manager |
| **Stock valuation** | On-hand times average cost by branch and category | Manager, admin |
| **Low and negative stock** | Items at or below reorder point, items below zero | Manager |
| **Receivables aging** | Customer balances by age bucket | Manager |
| **Payables** | Received orders not yet paid, by supplier | Admin |
| **Discounts and voids** | Who gave which discounts, voids and refunds, and who approved | Manager |
| **Needs review** | Sync flags: negative stock, price mismatch, over credit limit, offline approval, late sync | Manager |
| **Audit log** | Filterable by user, action, resource, and date, with before and after values | Admin |

## Rules

- A report never changes data.
- Totals shown on screen equal the totals in the export, because both come from one query.
- Date range filters use the branch's time zone. The report says which one.
- Money is shown through `MoneyText`. Exports use plain numbers with two decimals.
- A cashier sees only their own shift. A manager sees their branches. An admin sees everything.
- Exports go to CSV, and a print layout exists for the shift report and the statement.

## Dashboard and charts

The Astryx dashboard templates (**Data Dashboard**, **Analytics Dashboard**) already include tiles, sparklines, and charts. Inspect them with `npx astryx template data-dashboard` before choosing a chart library (D8). Recharts is the fallback, since v1 already uses it.

## Logging and diagnostics

- The main process writes a rolling log file in the user data folder.
- A "Copy diagnostics" button bundles the app version, sync status, pending outbox count, and last errors, with no customer data, so support can help without a call.

## Screens

See [[AngieBarato v2 - Astryx UI Map]]: Data Dashboard, Analytics Dashboard, Searchable Table.

## Done when

- On a year of generated data (about 100,000 sales), the dashboard loads in under a second.
- The day boundary is correct for a sale made at 11:55 pm in the branch's time zone while the machine runs on UTC.
- The export total matches the screen total for each report.
- The "needs review" list shows every flag raised in the M3 chaos tests.
