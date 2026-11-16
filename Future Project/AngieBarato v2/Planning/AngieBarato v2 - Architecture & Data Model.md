---
title: "AngieBarato v2 - Architecture & Data Model"
category: Architecture
doc-status: Draft
priority: P0
created: 2026-11-16
updated: 2026-11-16
tags:
  - angiebarato
  - architecture
  - data-model
---

# AngieBarato v2 - Architecture & Data Model

Part of [[AngieBarato v2 - Overview & Roadmap]]. Flaw numbers (F1, F2, ...) refer to [[AngieBarato v2 - Existing System Analysis]]. Open choices are in [[AngieBarato v2 - Open Decisions]].

---

## 1. Stack

| Layer | Choice | Why |
| :--- | :--- | :--- |
| Desktop shell | Electron 44, electron-vite 6 | Best hardware support (printers, scanners, USB). Already scaffolded in `angiebaratov2`. |
| UI | React 19, TypeScript, Vite 8 | No server rendering is needed in a desktop app. |
| Design system | Astryx (`@astryxdesign/core`, neutral theme) | Ships prebuilt CSS, so no StyleX build plugin is needed. See [[AngieBarato v2 - Astryx UI Map]]. |
| Routing | TanStack Router | Typed routes and route guards. |
| Server state in UI | TanStack Query over IPC | Caching and invalidation for local reads. |
| UI state | Zustand | Cart, current shift, sync status. |
| Forms | React Hook Form + Zod | Same Zod schemas validate in the UI, in the main process, and on the server. |
| Local database | SQLite via `better-sqlite3` + Drizzle (sqlite dialect) | One file per device. Fast, transactional. |
| Cloud database | Supabase Postgres | Auth, storage, and the shared source of truth. |
| Server logic | Postgres functions (posting) + one Supabase Edge Function (Hono) for admin tasks | See D6. No separate API server to host. |
| Money | Integer centavos | See D2. |
| Testing | Vitest (unit), pgTAP or SQL tests (RLS), Playwright for Electron (end to end) | |
| Release | electron-builder, `electron-updater`, GitHub Actions | `.deb` and AppImage for Linux, NSIS for Windows. |

## 2. Process layout

```
┌────────────────────────── Electron ───────────────────────────┐
│ Renderer (React + Astryx)                                     │
│   screens, forms, cart state                                  │
│        │  typed IPC (contextBridge, no Node access)           │
│ Preload  ▼                                                    │
│ Main process                                                  │
│   ├─ services/    sales, stock, customers... (business rules) │
│   ├─ db/          SQLite + Drizzle + migrations               │
│   ├─ sync/        outbox push, change pull, conflict records  │
│   ├─ security/    password and PIN hashing, safeStorage keys  │
│   └─ hardware/    receipt printer, cash drawer, scanner       │
└───────────────────────────────┬───────────────────────────────┘
                                │ HTTPS, only when online
                        Supabase (Postgres + Auth + Edge Function)
```

**Rules**
- The renderer never talks to Supabase directly and never touches SQLite. It only calls typed IPC methods. This keeps the service-role key and all rules out of the web layer.
- All business rules live in `services/` in the main process, built on a shared pure module (`src/shared/`) that contains money, tax, discount, and rounding. The same module is imported by the Edge Function so the server recomputes with identical code (F1, F12).
- Electron: `contextIsolation` on, `nodeIntegration` off, sandbox on in production, a strict Content Security Policy, and every IPC input validated with Zod.

## 3. Folder layout of `angiebaratov2`

```
src/
  main/        index.ts, window.ts, ipc/ (one file per feature), services/, db/, sync/, security/, hardware/
  preload/     index.ts, index.d.ts  (the typed API surface)
  shared/      money.ts, pricing.ts, tax.ts, schemas/ (zod), permissions.ts, errors.ts
  renderer/src/
    app/       providers.tsx, router.tsx, layouts/
    features/  catalog/ inventory/ pos/ customers/ procurement/ reports/ admin/ auth/
    components/ shared Astryx-based pieces (MoneyText, SyncStatus, ConfirmDialog...)
    lib/       ipc client, hooks
supabase/
  migrations/  SQL, one file per change
  functions/   admin (Hono)
  tests/       RLS and posting-function tests
```

A feature folder holds its screens, hooks, and IPC calls. A feature may import from `components/` and `shared/`, never from another feature. This addresses F13 and F14: no screen reaches into another screen's code, and no file mixes unrelated rules.

## 4. Data model

All keys are UUIDv7 created on the device, so offline creation never collides. Every synced table has `created_at`, `updated_at`, `deleted_at`, and a server-assigned `server_seq` used by the sync cursor. Money columns are `bigint` centavos. Quantities are `numeric(12,3)` so items sold by weight work.

### 4.1 Access
| Table | Key columns |
| :--- | :--- |
| `profiles` | `id` (= auth user id), `full_name`, `role_id`, `branch_id` (home), `is_active` |
| `profile_pins` | `profile_id`, `pin_hash`, `failed_attempts`, `locked_until`. Not readable through the Data API. |
| `roles` | `id`, `name`, `description` |
| `permissions` | `code` (for example `sales.void`), `module`, `description` |
| `role_permissions` | `role_id`, `permission_code` |
| `devices` | `id`, `branch_id`, `register_code`, `name`, `last_seen_at`, `is_active` |
| `approvals` | `id`, `type`, `requested_by`, `approved_by`, `reason`, `ref_table`, `ref_id`, `device_id`, `created_at` |
| `audit_logs` | `id`, `actor_id`, `branch_id`, `device_id`, `action`, `resource`, `resource_id`, `before`, `after`, `created_at` |

### 4.2 Catalog (see [[AngieBarato 03 - Catalog & Pricing]])
`branches`, `categories`, `products`, `product_barcodes`, `branch_products` (per-branch price override, reorder point, `is_available`), `price_changes`.

### 4.3 Inventory (see [[AngieBarato 04 - Inventory & Stock Ledger]])
`stock_movements` (the ledger), `stock_balances` (cached on-hand and average cost per branch and product), `stock_counts`, `stock_count_lines`.

### 4.4 Sales (see [[AngieBarato 05 - POS & Checkout]])
`shifts`, `sales`, `sale_items`, `sale_payments`, `sale_returns`, `sale_return_items`, `receipt_prints`. Held carts are device-only (SQLite) and are not stored in Postgres. A sale's approvals are rows in `approvals` that point back to it (`ref_table`, `ref_id`), not a column on the sale.

### 4.5 Customers (see [[AngieBarato 06 - Customers, Credit & Payments]])
`customers`, `customer_ledger` (invoice, payment, adjustment rows), `collections` (a payment that settles one or more invoices).

### 4.6 Procurement (see [[AngieBarato 07 - Procurement & Transfers]])
`suppliers`, `purchase_orders`, `purchase_order_items`, `goods_receipts`, `goods_receipt_items`, `supplier_payments`, `transfers`, `transfer_items`.

### 4.7 System
`settings` (typed: `key`, `type`, `value_json`, `scope` = global or branch), `sync_outbox`, `sync_conflicts`, `sequences` and `held_carts` exist **only in the device's SQLite** (invoice counters and held carts are per device).

## 5. State machines

Only these transitions are allowed. Anything else is rejected by the service and by a database check.

| Document | Flow |
| :--- | :--- |
| Shift | `open` → `closed` |
| Sale | `completed` → `voided` (same shift, needs approval) · `completed` → `partially_returned` → `returned` |
| Purchase order | `draft` → `ordered` → `partially_received` → `received` · `draft` or `ordered` → `cancelled` |
| Transfer | `draft` → `in_transit` → `received` · `draft` → `cancelled` · `in_transit` → `received_with_variance` |
| Stock count | `open` → `submitted` → `approved` (posts adjustments) |

A received purchase order cannot be cancelled. It can be corrected by a return-to-supplier adjustment (F11).

## 6. Invariants (tested)

1. `stock_balances.on_hand` equals the sum of `stock_movements.qty` for the same branch and product. A nightly check reports differences.
2. A sale's `total` equals the sum of its items, minus discount, plus tax, computed by the shared module. The server recomputes and stores a `flags` value if the device total differs.
3. The sum of `sale_payments` equals `amount_paid`. A credit sale has `amount_paid` less than `total`, and a matching `customer_ledger` row.
4. `customer_ledger` rows are never edited or deleted. A mistake is fixed with a reversing row.
5. Invoice numbers are unique per register and have no gaps.
6. Every row in `stock_movements`, `sale_payments`, and `customer_ledger` has `actor_id`, `branch_id`, and `device_id`.

## 7. Security model

**Three layers, same rule set**
1. **Database (RLS):** every table has RLS on. A user reads rows for branches they may access. Writes to ledger tables go only through posting functions, never directly.
2. **Service (main process):** every IPC method begins with `requirePermission('code')`. This protects offline use, where RLS is not in the path.
3. **UI:** buttons and routes are hidden when the user lacks the permission. This is for comfort only, never for safety.

**Specific rules**
- Roles and branch are read from `profiles` in policies. They are never taken from `user_metadata`.
- Posting functions are `SECURITY INVOKER` where possible. A function that must bypass RLS lives in a private schema, checks `auth.uid()` itself, and is not callable by `anon` (F2, F3).
- PIN: argon2id or scrypt, a lockout after 5 failures, scoped to one approval (F4). The PIN is a convenience on top of a signed-in device, not a login.
- Secrets: the service-role key never ships in the app. The Edge Function holds it. The app holds only the publishable key and the user's session, stored with Electron `safeStorage`.
- Pin package versions and commit the lockfile.

## 8. Sync summary

Full detail is in [[AngieBarato 02 - Offline Data & Sync]]. **Implementation status:** the Postgres side (tables, RLS, posting functions) is built and tested in `angiebaratov2/supabase/`. See M1 in [[AngieBarato v2 - Master Build Tracker]].

**Pull cursor caveat:** `server_seq` values can commit out of order. A device re-reads a small window below its cursor each pull. Rows are keyed by uuid, so this is harmless.

- **Writes:** a service writes to SQLite and an outbox row in one transaction. The sync engine sends outbox rows to the matching Postgres function with an idempotency key.
- **Reads:** the device keeps a cursor per table (`server_seq`). It pulls rows newer than the cursor for its own branch.
- **Conflicts:** ledger and sales rows never conflict (append only). Catalog rows use last write wins by server time. Anything the server cannot accept becomes a visible conflict record, never a silent drop.
