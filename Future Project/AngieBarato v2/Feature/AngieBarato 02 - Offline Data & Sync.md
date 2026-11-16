---
title: "AngieBarato 02 - Offline Data & Sync"
category: Feature Spec
doc-status: Draft
priority: P0
milestone: M3
created: 2026-11-16
updated: 2026-11-16
tags:
  - angiebarato
  - feature
  - offline
  - sync
---

# AngieBarato 02 - Offline Data & Sync

Part of [[AngieBarato v2 - Overview & Roadmap]]. Built in Milestone 3 of [[AngieBarato v2 - Master Build Tracker]]. Fixes F5, F6, F15 in [[AngieBarato v2 - Existing System Analysis]].

## Purpose

The shop keeps selling when the internet is down, and nothing is lost or counted twice when it comes back.

## Principles

1. **The app reads and writes only the local SQLite database.** The network is not in the path of a sale.
2. **A completed sale is a fact.** The server never rejects an offline sale because of stock or a price difference. It records the sale and raises a flag for a person to review.
3. **Every write is repeatable.** Sending the same document twice has the same result as sending it once.
4. **Nothing disappears silently.** What the server cannot accept becomes a visible conflict.

## How it works

**Write path**
1. A service changes the data and inserts a `sync_outbox` row in one SQLite transaction.
2. The sync worker takes outbox rows in order and calls the matching Postgres posting function with the document id as the idempotency key.
3. On success the outbox row is marked done. On a network error it is retried with backoff. On a business rejection it becomes a `sync_conflicts` row.

**Read path**
1. The device keeps a cursor per table, stored as the highest `server_seq` it has seen.
2. It asks for rows with a higher `server_seq`, limited to its own branches, in pages.
3. Deleted rows arrive as rows with `deleted_at` set.
4. A new device runs a first sync (bootstrap) before it can be used.

`server_seq` comes from a database sequence, not a clock. Device clocks can be wrong, so `updated_at` is never used to decide what is new.

## Document identity and numbering

- Every row has a UUIDv7 created on the device.
- Each register has a code (for example `BR1-R2`). Invoice numbers come from a local counter in `sequences`: `BR1-R2-000123`. Numbers are unique per register and have no gaps. A voided sale keeps its number (F5).
- A device cannot be used until it is registered to a branch and register in `devices`.

## Conflict rules

| Data | Rule |
| :--- | :--- |
| Sales, payments, returns, ledger rows | Append only. They cannot conflict. |
| Stock | Derived from the ledger. Two devices selling the same item both succeed. Negative stock is flagged (D3). |
| Customer balance | Derived from the customer ledger. Over-limit is flagged (D4). |
| Catalog (products, prices, categories) | Last write wins by server time. The overwritten value is kept in `price_changes` or the audit log. |
| Settings | Last write wins. Branch settings override global settings. |
| A document in the wrong state (for example a void of an already voided sale) | Rejected into `sync_conflicts` with the reason. |

## Flags the server may add on sync

`stock_negative`, `price_mismatch`, `total_mismatch`, `over_credit_limit`, `offline_approval`, `late_sync` (older than 48 hours). Flags show on the "needs review" list in Reports and do not block anything.

## Sync screen and status

- **Status dot** in the top bar: synced, syncing, offline, needs attention.
- **Sync screen:** counts of pending, failed, and conflicts. Each conflict shows the document, the reason, and the actions that make sense (retry, accept with a note, cancel with approval).
- A **Banner** appears after a configurable time offline, so a manager knows the branch is running on local data only.

## Safety

- SQLite runs in WAL mode. The file is backed up before each migration and nightly (M10).
- The app asks for confirmation before it can be closed while the outbox has pending rows.
- The Supabase URL comes from configuration. There is no hardcoded fallback address (F6).
- Realtime is off by default. Pull runs on a timer and on reconnect (D14).

## Done when

- **Cut-the-network test:** offline, create a sale, an adjustment, and a product. Restart. Reconnect. Each appears in Supabase once.
- **Duplicate test:** send the same sale twice. One sale exists.
- **Lost response test:** kill the connection after the server commits, then retry. One sale exists.
- **Two devices offline test:** both sell the last unit. Both sales sync. One `stock_negative` flag exists.
- **Crash test:** kill the app during sync. The next start finishes without duplicates.
- Fixing a conflict from the Sync screen updates the outbox and the status dot.
