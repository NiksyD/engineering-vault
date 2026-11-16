---
title: "AngieBarato v2 - M3 Local Data & Sync Plan"
category: Implementation Plan
doc-status: Draft
priority: P0
created: 2026-11-16
updated: 2026-11-16
tags:
  - angiebarato
  - plan
  - offline
  - sync
---

# AngieBarato v2 - M3 Local Data & Sync Plan

Turns Milestone 3 of [[AngieBarato v2 - Master Build Tracker]] into build steps. The behavior rules are in [[AngieBarato 02 - Offline Data & Sync]]. This note is about how to build it and what to decide first. Nothing here is built yet.

## 1. What M3 must prove

**Done when:** with the network cut, a test creates a sale, an adjustment, and a product, restarts the app, reconnects, and all three appear in Supabase exactly once. Running sync twice changes nothing. A forced conflict shows on the Sync screen.

## 2. Findings that shape the plan

1. **SQLite is built into Electron 44.** Electron 44 runs Node 24.22, which includes `node:sqlite` (SQLite 3.53). Checked on this machine. This avoids native modules (`better-sqlite3`) that must be rebuilt for each Electron version and each operating system, which is the most common cause of broken installers for offline apps. It also runs under plain Node, so the sync engine can be tested without Electron.
2. **Drizzle has no `node:sqlite` driver.** It has `better-sqlite3`, `libsql` and a callback-based `sqlite-proxy`. The sync engine works generically over many tables, so plain SQL with small typed repositories is simpler than an ORM here. Numbered `.sql` migration files, the same style as `supabase/migrations`.
3. **`server_seq` can commit out of order** (noted in M1). A pull must re-read a window below its cursor. Rows are keyed by uuid, so re-reading is harmless.
4. **Attribution problem.** Posting functions take the actor from `auth.uid()`. If cashier A sells offline, signs out, and cashier B signs in, a push made under B would record B as the cashier. See decision D18.
5. **The local file holds business data unencrypted.** `node:sqlite` has no encryption. See decision D17.

## 3. Decisions to settle before building

| # | Question | Recommendation |
| :-: | :--- | :--- |
| D17 ✅ | Encrypt the local database file? | **Decided: no file encryption in M3. Rely on operating-system disk encryption** (BitLocker, LUKS, FileVault) and write that into the install guide. File mode `0600`. The real secrets (session, PIN hashes) already live in `safeStorage`. SQLCipher needs a native module and brings back the rebuild problem. Revisit if the owner needs it. |
| D18 ✅ | Who is recorded when a sale is pushed after the cashier signed out? | **Decided: one cashier per branch, so only the simple rule:** block sign-out while offline with unsynced documents. (Original idea, if two cashiers ever share a register: keep each user's session until their documents are pushed.) The outbox row stores the user id, the sync engine pushes it with that user's saved session, and the session is deleted once the user's queue is empty. Correct attribution, and the audit log stays honest. **Step one:** block sign-out while that user has unsynced documents and the app is offline, with a clear message. Build the per-user sessions as a later step in M3d. |
| D19 ✅ | Product edits offline? | **Decided: yes, as a generic "upsert row" in the outbox**, because the engine needs that mechanism for shifts and stock counts anyway. Catalog screens themselves come in M4. |
| D20 ✅ | SQLite access layer | **Decided: `node:sqlite` with plain SQL and numbered migrations.** No ORM, no native module. |

## 4. Architecture

```
Renderer ── typed IPC ── services (main process)
                          │  write: one SQLite transaction = data change + outbox row
                          ▼
                    local.db  (node:sqlite, WAL)
                    ├─ synced tables (same columns as Postgres)
                    ├─ sync_outbox     pending documents
                    ├─ sync_conflicts  rejected documents (visible, never dropped)
                    ├─ sync_state      cursor per table, last sync time
                    └─ device          branch, register code, device id, invoice counter
                          ▲   ▼
                    SyncEngine ── transport ── Supabase (PostgREST + post_* functions)
```

- **Transport is an interface.** Tests give the engine a fake transport and a real one pointed at the local Supabase stack.
- **One writer.** Only the main process opens the file. The renderer never touches it.
- **WAL mode**, `synchronous = FULL` for sales (a power cut must not lose a completed sale), `foreign_keys = ON`.
- **Money and time** match Postgres: integer centavos, ISO timestamps in UTC.

## 5. Sync rules

**Push** (outbox → server), in order, one worker:
- Documents that have a posting function (`sale`, `void`, `return`, `adjustment`, `collection`, `goods_receipt`, transfer send and receive, stock count approval) go to that function. Its document id is the idempotency key.
- Plain rows (shifts, stock counts and lines, products, barcodes, branch prices) go as an upsert by id through the normal API under row level security.
- A network error retries with backoff (1 s up to 5 min). A **business rejection** (an error response) moves the row to `sync_conflicts` with the message and unblocks the queue. Nothing is dropped.
- An outbox row that depends on another (a sale on a shift that did not sync) waits for it.

**Pull** (server → device), per table, newest first by `server_seq`:
- `select … where server_seq > (cursor − 1000) order by server_seq limit 500`, repeat until a short page.
- Only the device's branch tables are requested, so RLS and the filter agree.
- Upsert by id locally. Soft-deleted rows arrive with `deleted_at` and are kept as tombstones.
- **A local row with a pending outbox change is not overwritten** by a pull. The pending change wins until it is pushed.

**First sync (bootstrap):** a new device pulls everything for its branch before the app lets anyone sell. Progress is shown. It can be resumed.

**Triggers:** app start, every 30 s while online, on reconnect, and a few seconds after a local write.

**Connectivity** is the result of the last real request, not `navigator.onLine`. No hardcoded fallback address (this was a v1 flaw).

## 6. Build steps

| Step | Result | Done when |
| :-: | :--- | :--- |
| **M3a** | Local database foundation | `node:sqlite` opens `local.db` in WAL mode; numbered migrations run on start with a backup first; the synced tables exist locally; Vitest is set up and tests the migration runner (this also completes tracker item 0.7). |
| **M3b** | Device registration and numbering | First-run screen picks a branch and register and records the device in `devices`. Invoice numbers `BR1-R1-000123` come from a local counter and never repeat or skip, across restarts and crashes. |
| **M3c** | Pull and bootstrap | A new device ends up with the branch's catalog, customers, balances and settings. A second pull changes nothing. Cursor overlap tested with rows committed out of order. |
| **M3d** | Outbox and push | The three done-when documents (sale, adjustment, product) sync exactly once. Duplicate, lost-response and crash cases pass. Conflicts land in `sync_conflicts`. |
| **M3e** | Sync UI and chaos tests | Status dot, a Sync screen (pending, failed, conflicts, retry), the offline banner wired to real state, and the chaos suite: kill mid-sync, drop after the server commits, two devices selling the last unit. |

Each step ends with tests passing, the tracker updated, and a commit.

## 7. Risks

| Risk | Plan |
| :--- | :--- |
| `node:sqlite` is marked experimental or release-candidate in some Node 24 builds. | Wrap it behind one small `Database` interface (about six methods). Swapping to `better-sqlite3` later changes one file. |
| Local schema drifts from Postgres. | A test compares the column list of every synced table against the generated Supabase types. |
| A device clock is wrong. | The server never uses a device clock to decide what is new (`server_seq` does). Flag `late_sync` on very old documents. |
| A large first sync is slow on weak internet. | Page size 500, resumable, progress shown. Ask the owner for a typical catalog size. |
| Corrupt database file. | WAL, backup before each migration and nightly, and the outbox is the thing to protect first. A "restore from backup" path in M10. |

## 8. Owner answers (2026-11-16)

- **Size:** thousands of products. At a few hundred bytes each that is a few megabytes, so the first sync is quick even on a weak connection.
- **Customers:** most sales are walk-in, so **walk-in is the default** (D22): a sale has no customer record, only an optional name. The cashier may pick a saved customer, which is required for credit. Only saved customers are synced, and all of them are pulled (customers are not tied to a branch).
- **Cashiers:** one per branch, so D18 stays simple.
- **Hosting:** the production server will be a self-hosted Supabase in a homelab (D21). Storage is a disk, not a plan. See the hosting notes in [[AngieBarato v2 - Open Decisions]]. The design is unaffected, but the sync target is the owner's server and its uptime, backups and network become part of the pilot checklist (M10).
- **Disk encryption:** unknown. Add to the install guide as a requirement to check.

## 9. Questions for the owner (remaining)

- [x] Products and customers per branch: thousands of products, mostly walk-in customers.
- [x] Cashiers per register: one.
- [ ] Is the disk encrypted on the register computers, or can it be? (D17.)
- [ ] Will branches reach the homelab over a VPN (WireGuard or Tailscale) or through a public HTTPS address? (D21.)
