---
title: "AngieBarato v2 - Master Build Tracker"
category: Project Management & Execution Tracker
doc-status: Active
priority: P0
created: 2026-11-16
updated: 2026-11-16
tags:
  - angiebarato
  - roadmap
  - todo
  - engineering-tracker
---

# AngieBarato v2 - Master Build Tracker

> **For AI agents and developers:** read this tracker at the start of every task and update it at the end. Check a box only after `npm run typecheck`, `npm run lint`, and the tests all pass. If a task turns out to be wrong or unneeded, strike it through and say why. Do not delete it.

**Related notes**
- [[AngieBarato v2 - Overview & Roadmap]]
- [[AngieBarato v2 - Existing System Analysis]]
- [[AngieBarato v2 - Architecture & Data Model]]
- [[AngieBarato v2 - Open Decisions]]
- [[AngieBarato v2 - Astryx UI Map]]

**How to read a milestone**
- **Done when** is the test for the whole milestone. If it is not true, the milestone is not finished, whatever the boxes say.
- **Skills** names the Claude skills (from the niksyskills library) that apply. Load them before starting the work.
- **Fixes** lists the v1 flaws from [[AngieBarato v2 - Existing System Analysis]] that the milestone removes.
- Milestones are in build order. Do not start one before the previous one's **Done when** is true.

---

## Milestone 0: Foundation

*Specs: [[AngieBarato v2 - Architecture & Data Model]] sections 1 to 3*
*Skills: `environment-setup-guide`, `architecture-decision-records`, `lint-and-validate`, `typescript-expert`, `github-actions-templates`*
*Fixes: F13, F19*

**Done when:** a change pushed to the main branch is type-checked, linted, tested, and built, and the app window shows an Astryx screen.

- [x] **0.1 Scaffold** the project with electron-vite (React + TypeScript) in `angiebaratov2`.
- [x] **0.2 Astryx wired in.** Packages installed, `neutral` theme added (`src/renderer/src/astryx-themes.ts`), reset and base CSS imported, root wrapped in `<Theme>`. A test `Button` renders in the Electron window (confirmed by screenshot 2026-11-16).
- [x] **0.3 Dev script.** `npm run dev` passes `--no-sandbox` for local development on Ubuntu. `dev:sandbox` keeps the original. Do not ship with the sandbox off.
- [ ] **0.4 Project metadata.** Real app name, `appId`, author, description, and window title ("AngieBarato") in `package.json`, `electron-builder.yml`, and the main process.
- [x] **0.5 Remove template leftovers** (`Versions.tsx`, logo assets, `base.css`, the `ping` IPC example). Done during M2.
- [ ] **0.6 Project rules.**
  - [ ] Write `AGENTS.md` (short, always loaded) and `docs/standards/coding-standard.md`. `CLAUDE.md` imports `AGENTS.md`.
  - [ ] Add lint rules that block raw HTML elements, inline `style`, `console.log`, and `any`.
  - [ ] Create `docs/adr/` and record A1 to A5 from [[AngieBarato v2 - Open Decisions]].
- [ ] **0.7 Tooling.** (Vitest and the `check` script are done, see M3a.) Vitest, Prettier, `typecheck`, `lint`, `test`, `check` scripts, and a CI workflow. Decide whether `angiebaratov2` is its own git repository.
- [ ] **0.8 Install the skills** from the list in this note. Fix the install URL on the skills site first (it points to localhost).
- [ ] **0.9 Create the folder layout** from the architecture note, section 3, with a lint rule that stops one feature from importing another.

---

## Milestone 1: Database and security

*Specs: [[AngieBarato v2 - Architecture & Data Model]] sections 4 to 7*
*Skills: `supabase`, `supabase-postgres-best-practices`, `database-design`, `api-security-best-practices`, `threat-modeling-expert`*
*Fixes: F2, F3, F12, F18*

**Done when:** a fresh Supabase project can be built from the migrations alone, and the test suite proves that a cashier of branch A cannot read or write branch B data, cannot write ledger tables directly, and cannot call a posting function without its permission.

- [x] **1.1 Settle blocking decisions** in [[AngieBarato v2 - Open Decisions]].
  - [x] D1 one business, several branches (2026-11-16).
  - [x] D2 money as integer centavos (confirmed 2026-11-16).
  - [x] D6 server shape: Postgres functions plus one Edge Function (confirmed 2026-11-16).
  - [ ] D5 tax included or added, and receipt format. **Still open (ask the accountant).** The schema has setting `tax.prices_include_tax` (default `true`) and `post_sale` reads it. The server does not yet recompute tax.
- [ ] **1.2 Create the Supabase project** (development) and link the CLI. *The owner created a new project. Linking needs `npx supabase login` and `npx supabase link --project-ref <ref>`, which only the owner can run. Migrations are tested against a local Supabase stack, not yet pushed to the hosted project.*
- [x] **1.3 Identity tables** (`20261116100733_identity.sql`): `profiles`, `profile_branches`, `profile_pins`, `roles`, `permissions`, `role_permissions`, `branches`, `devices`. Seeded 23 permissions and the Admin, Manager and Cashier roles.
- [x] **1.4 Catalog tables** (`..._catalog.sql`): `categories` (max 3 levels), `products`, `product_barcodes`, `branch_products`, `price_changes` (filled by triggers).
- [x] **1.5 Ledger tables** (`..._inventory.sql`): `stock_movements` (append only), `stock_balances` (changed only by a trigger, moving-average cost), `stock_counts`, `stock_count_lines`, and the `stock_balance_drift` view.
- [x] **1.6 Sales tables** (`..._sales.sql`): `customers`, `shifts`, `sales`, `sale_items`, `sale_payments`, `sale_returns`, `sale_return_items`, `receipt_prints`. *`held_carts` is not in Postgres: held carts stay on the device only.*
- [x] **1.7 Customer and procurement tables** (`..._customers_procurement.sql`): `customer_ledger`, `collections`, `collection_allocations`, `suppliers`, `purchase_orders` and items, `goods_receipts` and items, `supplier_payments`, `transfers` and items, plus state-machine triggers.
- [x] **1.8 System tables** (`..._system.sql`): typed `settings` (with defaults), `approvals`, `audit_logs`, and an audit trigger on 19 admin and catalog tables. *`sequences` is not in Postgres: invoice counters live on the device.*
- [x] **1.9 Sync support:** a global `server_seq` sequence stamped by trigger, `updated_at` triggers, and soft-delete columns on mutable tables. *Sequence values can commit out of order, so the pull in M3 must re-read an overlap window below its cursor.*
- [x] **1.10 RLS on every table.** Ledger and transaction tables have no write grant. Admin, catalog, draft-document tables have permission-based write policies.
- [x] **1.11 Private helper functions** (`..._security_rls.sql`): `private.is_active_user()`, `has_permission(code)`, `has_any_permission(...)`, `can_access_branch(id)`. In a non-exposed schema, with empty `search_path`.
- [x] **1.12 Posting functions** (`..._posting_functions.sql`): `post_sale`, `post_void`, `post_return`, `post_stock_adjustment`, `post_collection`, `post_goods_receipt`, `post_transfer_send`, `post_transfer_receive`, `post_stock_count_approval`. Each is a private `SECURITY DEFINER` implementation with a public `SECURITY INVOKER` wrapper, idempotent on its document id, and writes its audit row in the same transaction.
- [x] **1.13 Tests:** 78 pgTAP checks pass (`npm run db:test`): `01_security.test.sql` (27) and `02_posting.test.sql` (51). The Supabase advisor (`npm run db:advisors`) reports no warnings. Its only notice is that `profile_pins` has RLS on and no policy, which is intended.
- [x] **1.14 Types** generated to `src/shared/database.types.ts` (`npm run db:types`). Re-run after each migration.

**Not done in M1 (carry forward)**
- [ ] Push the migrations to the hosted project (needs `login` and `link`) and run the advisors there.
- [ ] Server-side tax recompute (waits for D5). Today the server recomputes subtotal, discount and total, and flags differences.
- [ ] `post_shift_*` functions. Shifts are written directly under RLS for now, and a closed shift is immutable by trigger.
- [ ] PIN set and verify functions, and how an offline device gets approver hashes (M2).
- [ ] Reports that depend on per-role cost visibility: a cashier can read `unit_cost_centavos` on their branch's sale items today. Decide in M2 whether to hide cost.
- [ ] Timezone default is `Asia/Manila` (assumed from the peso and GCash). Confirm.

---

## Milestone 2: App shell, accounts, and roles

*Specs: [[AngieBarato 01 - Access, Profiles & Audit]]*
*Skills: `auth-implementation-patterns`, `frontend-security-coder`, `react-patterns`, `ui-states`*
*Fixes: F2, F4, F16*

**Done when:** an admin, a manager, and a cashier each sign in, see only the screens their role allows, and a cashier typing a restricted route is stopped. A manager approval by PIN works and is recorded.

- [x] **2.1 Main-process security base:** `contextIsolation` on, `nodeIntegration` off, `sandbox` on, a CSP, all permission requests denied, navigation and new windows blocked. IPC calls check the sender, validate input with Zod, and never leak internal errors.
- [x] **2.2 Typed IPC bridge:** the preload script exposes one object, `window.api.auth`, typed from `src/shared/types.ts`. It requires only `electron`, so it runs sandboxed.
- [x] **2.3 Sign in, sign out, session resume:** the Supabase session and an offline copy of the profile are stored encrypted with Electron `safeStorage`. If the system cannot encrypt, nothing is written to disk. *A device resumes offline for up to 14 days (D16). The very first sign-in on a device needs the internet, because no password is stored locally.*
- [x] **2.4 Router and guards:** TanStack Router with hash history. Signed-out users go to sign-in. Each protected route checks its permission and redirects to a "no access" page. `PermissionGate` and `useCan` hide controls.
- [x] **2.5 App shell:** the Astryx `AppShell` and `SideNav`, with menu items hidden by permission, an offline banner, and a sign-out item. Menu items for later milestones are guarded placeholders.
- [x] **2.5a Admin bootstrap:** `npm run admin:create -- --email ...` creates the first Admin (hidden password prompt, secret key read only from `.env`).
- [x] **2.5b Offline font:** the neutral theme loaded Figtree from Google Fonts at runtime. It is now bundled with `@fontsource/figtree`, and the generated `astryx-themes.ts` was removed so nothing re-imports the remote font.
- **Verified:** 15 checks of the sign-in rules and 14 end-to-end checks driving the real Electron window against the local database (admin and cashier menus, blocked admin route, wrong password, sign-out, reload keeps the session). Scripts are in `tests/checks/`. They are manual for now and become Vitest and Playwright tests in M0.7.
- [x] **2.5d Change my password:** Account page. Needs the current password, 12+ characters, and must differ. The check uses a throwaway client so the saved session is not touched.
- [ ] **2.5c Put the publishable key in `.env`** (`MAIN_VITE_SUPABASE_PUBLISHABLE_KEY`) and run `npm run admin:create` against the hosted project. *Owner action.*
- [x] **2.6 Users and roles screens** (Astryx Table, Dialog, Selector, MultiSelector, CheckboxInput):
  - Users: list with search, add (one-time temporary password), edit, turn off and on, reset password. Emails come from the `admin-users` Edge Function.
  - Roles: list, create, edit permissions grouped by module. An all-access role shows "its list cannot be edited". A user cannot tick a permission they do not hold.
  - **Edge Function** `supabase/functions/admin-users` (Hono, Deno): checks the caller itself (`verify_jwt` is off in `config.toml`), uses the secret key only for Auth user changes, and writes profile rows as the caller so the audit log names the real person.
  - **Privilege guards** (`20261116113234_privilege_guards.sql`): nobody can use user or role management to raise their own access. Only an admin can create or change an admin, nobody can change their own role or switch themselves off, a role editor can grant only permissions they hold, built-in roles cannot be deleted, and the last active admin cannot be removed.
  - **Verified:** 91 database tests (13 new), 21 Edge Function checks, 28 end-to-end checks in the real window (`tests/checks/`). Lint and typecheck are clean.
  - **Owner actions to put this on the hosted project:** `npx supabase db push --remote` (the new migration), then `npx supabase functions deploy admin-users`.
  - Known limits: a temporary password has no forced change on first login (Supabase Auth has no such flag), so an in-app "change my password" screen is still needed. Turning a user off blocks their data at once (row level security) but a signed-in session keeps a valid access token for up to one hour.
- [x] **2.7 PIN and approvals** (`20261116115612_pin_and_approvals.sql`):
  - **Online:** `verify_approval_pin` checks the PIN on the server (bcrypt via pgcrypto), counts wrong tries (the count is saved, because a wrong PIN returns a result and does not raise), locks for 15 minutes after 5, and writes a **verified** approval row. No hash leaves the server.
  - **Offline:** `get_approver_verifiers` gives the main process the bcrypt hashes of one branch's approvers, kept only in the encrypted store and wiped on sign-out. The page never receives a hash. The check uses `bcryptjs`, with its own 5-try lock. These approvals are **unverified** and flagged `offline_approval` on sync. The owner can switch this off (`approvals.offline_enabled`).
  - **Claimed approvals are no longer trusted:** `post_sale` flags any approval the server did not verify (`unverified_approval`, or `offline_approval` when offline). Approvals gained a `verified` column.
  - **Rules:** PINs are 4 to 6 digits and must not be simple (1234, 1111, repeated pairs). Setting a PIN needs the account password again. Admins can clear a PIN. PINs and hashes never appear in the audit log or in anything returned to the page.
  - **UI:** Account page (PIN card for approvers), a reusable `ApprovalDialog` (used by the POS in M6; a development-only page exercises it), and "Clear approval PIN" in the Users menu.
  - **Verified:** 121 database tests (30 new for PINs), 19 PIN service checks, 20 end-to-end checks in the real window. Lint, typecheck and the Supabase advisor are clean.
  - **Honest limit:** a 4 to 6 digit PIN has at most a million values, so anyone who gets a hash can recover it quickly. Offline approval accepts that risk for D4.
- [x] **2.8 Audit viewer** (`/admin/audit`, needs `admin.audit`):
  - Filters for what, action, who (searchable) and a date range; newest first; "Load more" paging (50 at a time); a drawer with the before and after values. Plain-language names (Changed, Settings, Sale posted) from `src/shared/audit.ts`, with the raw value shown for anything not listed yet.
  - **Paging:** keyed on time and id together. A transaction stamps all its rows with the same time, so a time-only cursor skips or repeats rows. A test pages through 120 rows that share one timestamp and gets all 125, none repeated or missing.
  - **Cursor safety:** the cursor is placed inside a database filter string, so the IPC schema accepts only an ISO timestamp and a uuid. Filter syntax in either value is rejected (tested).
  - Dates use the computer's time zone (a day is midnight to midnight there). Branch time zones come with the reports in M9.
  - The code blocks have no copy button: the page has no clipboard permission, and a broken button is worse than none.
  - **Verified:** 17 service checks, 22 end-to-end checks (run twice, plus once on a freshly reset database). Lint, typecheck, Prettier and the advisor are clean.
  - **Test note:** the Astryx dropdown triggers sit at a different depth in each Selector, and keyboard or coordinate clicks did not reach them. The test finds the nearest expandable button from the listbox and clicks it.
- [x] **2.9 Typed settings screen** (`/admin/settings`, needs `admin.settings`):
  - Five cards, each saved on its own with Save and Undo: Company and receipt, Tax, Discounts and credit, Stock, Manager approvals. Text, numbers with units, switches, and money shown in pesos but stored as centavos.
  - `src/shared/settings.ts` is the one list of settings, used by the screen, the main-process check and the tests. A migration (`settings_validation`) makes the database refuse out-of-range values too (tax 0 to 100, PIN tries 3 to 10, whole numbers where needed), so a bad value is refused even if the app is bypassed.
  - The offline PIN lock numbers (5 tries, 15 minutes) are not on the screen: the offline check uses fixed values, so showing them would let the two disagree.
  - Every change is audited with the admin as the actor and the old value.
  - **Still open:** `tax.prices_include_tax` is shown with a note to ask the accountant (D5). Branch-level overrides are not on the screen yet (the database supports them).
  - **Verified:** 135 database tests (14 new), 17 service checks, 29 end-to-end checks (repeatable, run three times in a row). Lint, typecheck, Prettier and the advisor are clean.
  - **Bug found and fixed while testing:** the card was re-created after a save, which hid the "Saved." message and would have discarded anything typed before the refresh finished. The cache is now updated at once and the card is kept.
- [x] **2.10 Theme toggle:** System, Light or Dark, in an Appearance card on the Account page. Saved per computer (each register keeps its own choice; it is not part of a user's account) and applied through the Astryx `Theme` `mode`. Defaults to System. Verified in the real window: the text colors flip, and the choice survives a restart (11 checks, run twice).

---

## Milestone 3: Local data and sync

> **Plan:** [[AngieBarato v2 - M3 Local Data & Sync Plan]] (build steps M3a to M3e, decisions D17 to D20). Settle the decisions before starting M3a.

*Specs: [[AngieBarato 02 - Offline Data & Sync]]*
*Skills: `database-design`, `nodejs-best-practices`, `test-driven-development`, `systematic-debugging`*
*Fixes: F5, F6, F15*

**Done when:** with the network cut, a test creates a sale, an adjustment, and a product, restarts the app, then reconnects and all three appear in Supabase exactly once. Running the sync twice changes nothing. A forced conflict shows on the Sync screen.

- [x] **3.1 SQLite setup (M3a, done):** `src/main/local/`.
  - `node:sqlite` (built into Electron 44, no native module) behind a small `Db` interface, so the engine can be swapped by changing one file. WAL, `synchronous = FULL`, foreign keys, busy timeout, file mode 0600. Transactions nest as savepoints.
  - Numbered `.sql` migrations bundled into the app. Each runs in its own transaction with a checksum. The app refuses to start if an applied migration was edited, or if the database is newer than the app. A consistent backup (`VACUUM INTO`) is taken before migrating existing data, keeping the newest five.
  - Three migrations so far: local sync tables (`device`, `counters`, `sync_state`, `sync_outbox`, `sync_conflicts`), reference tables (branches, registers, catalog, customers, settings), and sales and stock (stock balances and movements, customer ledger, shifts, sales, items, payments, approvals).
  - **A test compares every mirrored table's columns with the generated Postgres types.** I checked that it fails when a column is renamed, and that the walk-in credit rule test fails when the rule is removed.
  - Vitest is set up (`npm test`, and `npm run check` runs typecheck, lint and tests): 44 tests. This completes the Vitest part of 0.7. CI and Prettier checks in a workflow are still open.
  - Verified in the real app: the file is created in the user data folder with 22 tables, WAL mode and owner-only permissions, and a second start applies nothing.
  - **Notes:** `node:sqlite` prints an "experimental" warning, though it is stable enough in Node 24 (that is why the `Db` interface exists). Quantities are stored as `real` (no exact decimal in SQLite) and must be rounded to 3 places when written and summed. The remaining tables (returns, collections, purchasing, transfers, stock counts) get their own migrations in the milestones that need them.
- [x] **3.2 Device registration and numbering (M3b, done):**
  - **Registration** (`/setup`, an admin who works in at least one branch): picks the branch and reserves the next free register code (R1, R2 ...) as a **new** `devices` row, then saves it in the local database. A computer never takes over an existing register, because two computers sharing a code would both issue the same invoice numbers. A reinstalled computer becomes the next register. The code is read fresh and retried if another computer takes it first (up to 5 times). If the local save fails after the server accepted, the server record is retired so no register is left unowned.
  - **Where it shows:** a banner on every screen until the computer is set up (with a Set up button for admins, "ask an admin" for others), a "This computer is register BR1 R1" line on Home, and a warning when the signed-in user does not work in the register's branch. The setup page refuses a second setup. Selling will be blocked on an unset computer or a foreign branch when the POS is built (M6). Admin screens work on any computer.
  - **Invoice numbers** (`BR1-R1-000123`, `src/main/local/counters.ts`): taken from a local counter **inside the same transaction as the sale**, so a failed sale gives its number back and nothing is skipped. A restart never repeats one. The counter can be raised (never lowered) when the server has seen higher numbers for this register, for example after restoring an old backup; that call is wired in M3c.
  - Migration `0004_device_details` adds the branch code and register name to the local device row (the branches table is only filled by the first sync).
  - **Verified:** 74 unit tests (30 new): number format and parsing, rollback and restart behavior, registration rules against a fake server (next free number, per-branch numbering, retry, give-up, replacement refused, cashier refused, wrong branch refused, retire on failed local save). Real window with a fresh data folder: 22 checks as an admin (banner, setup, server and local rows match, audit entry, restart, second setup refused, cashier of the branch, cashier of another branch) and 6 as a cashier on an unset computer. Earlier end-to-end suites still pass. `npm run check` is clean.
  - **Open:** a back-office computer (the owner's PC) also becomes a register if set up. Skipping setup is fine, since admin screens do not need it. A screen to retire registers comes with branches and registers in M4.
- [x] **3.3 and 3.4 Outbox and push (M3d, done):** `src/main/sync/outbox.ts`, `push.ts`, `src/main/local/documents.ts`.
  - **Writers** (`documents.ts`): `recordSale`, `recordStockAdjustment` and `saveProduct` each change the local database AND queue the document **in one transaction**. If anything fails, nothing is saved and the invoice number is not used up. These are what the POS and stock screens will call; they do no pricing and no permission checks (the server checks everything again). A sale needs the branch downloaded first.
  - **Queue:** documents with a posting function use the document id as the idempotency key. Plain row edits (a product) are upserts; repeated edits of the same row that have not been tried are collapsed into one.
  - **Sending** is strictly first-in, first-out, one at a time. Success means done. The server answering "duplicate" also means done, which is what makes a lost reply safe. A refusal moves the document to the **conflicts** list with the server's reason and the queue moves on. A temporary failure (no connection, 5xx, 408, 429) keeps it, retries after 2 s, 4 s, 8 s ... up to 5 minutes (spread by 20 percent), and stops the run. An expired sign-in or a server older than the app stops the run without blaming the document. A document is marked "sending" before the call, so one cut short by a crash is sent again, harmlessly.
  - **Order of edits:** a document waiting out a pause holds back everything behind it, so an older edit of a product can never overwrite a newer one. A document that depends on another waits for it, and is never sent if that one ended in conflict.
  - **Conflicts:** `resolveConflict` supports retry, accept (keep the server's version) and cancel. Accept and cancel free anything that was waiting on it. (The screen for this is M3e.)
  - **Reconnecting:** Sync now ignores the pause, and a successful read (proof the connection is back) retries waiting documents at once. Without this, pressing Sync now just after a long outage could do nothing for 5 minutes. The real-server run exposed it.
  - **Order of a round:** send first, then read, so the read already includes this computer's own changes.
  - **Screen:** the Data card shows "N documents are waiting to be sent" and a warning when the server did not accept some.
  - Local migration `0006` rebuilds the outbox with a `conflict` status (SQLite cannot change a CHECK). Reset now counts only pending and sending documents as waiting, and unresolved conflicts separately.
  - **Verified:** 197 unit tests (60+ for the queue and push, each key protection proved by breaking it). Against the real local server, **32 checks including the M3 done-when**: with the network cut a sale, an adjustment and a product are queued, survive a restart, and after reconnecting exist on the server exactly once; re-running sends nothing; a reply lost after the server committed is resent and recognised (one sale, stock reduced once); a document the server refuses becomes a conflict with its reason and does not hold up the next sale; two registers selling the last unit are both accepted, the stock goes to -1, one is flagged `stock_negative`, and their invoice numbers (R1, R2) do not collide. In the real window: 30 checks, including a bad document becoming a visible conflict and blocking Reset. Full regression from a reset database is green.
- [x] **3.4 Push:** done with 3.3, see above.
- [x] **3.5 and 3.6 Pull and first download (M3c, done):** `src/main/sync/`.
  - **Engine** (`pull.ts`): per table, rows with `server_seq` above the cursor, oldest first, 500 per page; each page and its cursor move are one transaction, so an interrupted download resumes where it stopped. A new computer is "downloaded" only when all 15 tables have finished.
  - **Out-of-order commits:** `server_seq` can commit out of order, so every pull restarts 1,000 numbers below its cursor. A test shows a late row is caught, and that it would be lost for good without the overlap.
  - **Never overwrites:** a row with an edit still waiting in the outbox (single or two-column key); a newer local copy with an older server copy; an identical re-read (so a second pull reports 0 changes). A column the server did not send keeps its local default; an unknown column is ignored.
  - **Scope:** branch tables (prices, stock levels, registers, sales and so on) only for this register's branch; shared tables (catalog, customers, settings) for everyone. Stock movements are not downloaded. Sales and similar history go back 90 days from the first download, and **that cutoff is remembered** (migration `0005_history_floor`), so the overlap can never bring older rows in. This was found by the real-server run, not by the unit tests.
  - **Invoice counter:** raised to the highest number the server has seen for this register, never lowered (covers restoring an old backup).
  - **Runs:** after sign-in, after register setup, on Sync now, and every 30 seconds, one at a time. Network trouble is a status message ("No connection. This computer will try again."), not an error.
  - **Screen:** a "Data on this computer" card on Home with a progress bar during the first download, counts, "updated 2 minutes ago", and Sync now.
  - **Measured on the local server:** 5,000 products plus the rest, 5,570 rows in 0.4 s; with over 10,000 products in the database, 11,121 rows in 0.7 s; a second pull with nothing new re-reads about 1,800 rows in 0.25 s.
  - **Verified:** 114 unit tests (27 for the engine against a fake server, each protection proved by breaking it), 25 checks against the real local server as a cashier (row level security, branch scoping, the cutoff, deletes, stock changes, counter), and 20 end-to-end checks in the real window run twice from fresh computers. Full regression from a reset database: 151 database tests, all end-to-end suites, advisor clean.
  - **A bug the checks caught:** two IPC handlers were never registered, because an edit silently did not apply and TypeScript cannot see a missing handler. A new test now fails if any channel lacks a handler or a preload entry.
- [x] **3.6 First sync (bootstrap):** done with 3.5, see above.
- [ ] **3.7 Connectivity** check against the app's own Supabase URL from configuration (no hardcoded fallback), plus the real result of the last request.
- [ ] **3.8 Invoice and document numbers** from `sequences` with the register code prefix, gap-free per register.
- [ ] **3.9 Sync UI:** `SyncStatus`, a Sync screen listing pending, failed, and conflicts, with retry and resolve actions.
- [ ] **3.10 Chaos tests:** kill the app mid-sync, duplicate a request, drop the connection after the server committed, and run two devices offline together.

---

## Milestone 4: Catalog

*Specs: [[AngieBarato 03 - Catalog & Pricing]]*
*Skills: `react-patterns`, `frontend-api-integration-patterns`, `ui-states`*
*Fixes: F12*

**Done when:** an admin can create, edit, deactivate, and price products with several barcodes, and a cashier on a second device sees them after sync, including while offline.

- [x] **4.1 Branches and registers screen (done early, because a computer cannot be set up without a branch):** `/admin/branches`, needs `admin.settings`.
  - Add a branch (code, name, address, phone, tax ID, time zone), edit, turn off or on. A register list per branch with rename, retire and bring back, and a marker for this computer.
  - **Rules enforced in the database** (`branch_and_register_rules` migration, 16 tests), so they hold however a change is made: a branch code is locked once any register exists (it is printed on invoices); a register's code and branch never change; a branch with an active register cannot be turned off; no new register for a turned-off branch; nothing is ever deleted.
  - **Reset this computer:** retires the register on the server first (needs the internet), takes a safety copy of the local database (`pre-reset-*.db`, newest five kept), then clears the local data and register setup so the computer can become a **new** register (R1 retired, the next one is R2). Refused while any document is unsynced or any conflict is unresolved, and it says how many.
  - Messages for admins with no branch now name the cause and offer an Add a branch button.
  - **Verified:** 151 database tests, 83 unit tests (8 new for reset), 59 end-to-end checks in the real window on a fresh computer and an empty database (run twice): no branch, add one, bad and repeated codes, set up, locked code, rename, turn-off refused, reset refused with an unsynced sale, reset after it synced, becomes R2, bring R1 back, audit entries.
  - **Note:** "Last seen" shows Never until sync (M3d) records it.
- [ ] **4.2 Categories** (tree, max 3 levels).
- [ ] **4.3 Products:** list, detail, create, edit, deactivate, image upload with local cache.
- [ ] **4.4 Barcodes:** several per product, unique across the catalog.
- [ ] **4.5 Branch pricing:** default price on the product, optional branch override, reorder point per branch.
- [ ] **4.6 Price history:** every price or cost change writes a `price_changes` row and an audit row.
- [ ] **4.7 Import and export** products by CSV with a preview and error list.
- [ ] **4.8 Label printing** with `jsbarcode`.

---

## Milestone 5: Inventory ledger

*Specs: [[AngieBarato 04 - Inventory & Stock Ledger]]*
*Skills: `database-design`, `test-driven-development`, `ui-states`*
*Fixes: F7, F10*

**Done when:** every stock change is a ledger row, on-hand equals the ledger sum in a test of 1,000 random movements, and a stock count with variances posts adjustments after manager approval.

- [ ] **5.1 Ledger writer** in the main process: the only way to change stock. `stock_balances` updates in the same transaction.
- [ ] **5.2 Stock on hand screen** by branch, with low-stock and negative-stock badges.
- [ ] **5.3 Movement history** screen with filters.
- [ ] **5.4 Adjustments** with reason codes and approval above a threshold.
- [ ] **5.5 Stock counts:** open, count (by scan or entry), submit, approve, post variances.
- [ ] **5.6 Cost method:** moving average per branch, kept in `stock_balances`. A sale item snapshots the branch cost at sale time.
- [ ] **5.7 Reconciliation job** that compares `stock_balances` with the ledger and reports differences.

---

## Milestone 6: POS and checkout

*Specs: [[AngieBarato 05 - POS & Checkout]]*
*Skills: `react-patterns`, `ui-states`, `accessibility-compliance-accessibility-audit` (or the existing `wcag-accessibility-audit`), `e2e-testing-patterns`*
*Fixes: F1, F4, F5, F9*

**Done when:** with the network off, a cashier opens a shift, scans and sells items with a split cash and GCash payment, prints a receipt, voids one sale and refunds another with manager approval, closes the shift with a cash count, and every sale syncs once on reconnect with the server totals matching.

- [ ] **6.1 Shared pricing module** (`src/shared/pricing.ts`): line totals, discounts, tax, rounding, in centavos. Heavy unit tests, including rounding edge cases.
- [ ] **6.2 Shifts:** open with a float, close with a cash count, expected vs counted, variance reason.
- [ ] **6.3 Sell screen:** scan, search, quantity, line and cart discounts (permission and approval limits), notes.
- [ ] **6.4 Hold and resume** carts.
- [ ] **6.5 Payment:** cash, card, GCash, credit, and split payment. Change due. Credit limit check against the local customer balance.
- [ ] **6.6 Complete sale:** one transaction that writes the sale, items, payments, stock ledger rows, customer ledger row, audit, and outbox.
- [ ] **6.7 Receipt:** preview, ESC/POS print, reprint with a log entry.
- [ ] **6.8 Returns and voids** with approval, restock choice, and refund method.
- [ ] **6.9 Server recompute:** `post_sale` recomputes totals and flags mismatches (D3, D4). Flags show on a review screen.
- [ ] **6.10 Keyboard flow** and touch targets. Run the accessibility audit.
- [ ] **6.11 End-to-end tests** of the done-when scenario with Playwright.

---

## Milestone 7: Customers and credit

*Specs: [[AngieBarato 06 - Customers, Credit & Payments]]*
*Skills: `database-design`, `test-driven-development`*
*Fixes: F8*

**Done when:** a customer buys on credit, makes two partial collections on different days, and the statement shows each invoice and payment, with the balance equal to the ledger sum. An over-limit sale needs approval and the approval is on the sale.

- [ ] **7.1 Customers** list, detail, create, edit, credit limit.
- [ ] **7.2 Customer ledger** posting for credit sales, collections, and adjustments (append only).
- [ ] **7.3 Collections:** allocate a payment to specific open invoices, oldest first by default.
- [ ] **7.4 Statement** screen and printable statement.
- [ ] **7.5 Receivables report** with aging buckets.
- [ ] **7.6 Credit rules** in the service and the posting function (D4).

---

## Milestone 8: Procurement and transfers

*Specs: [[AngieBarato 07 - Procurement & Transfers]]*
*Skills: `form-cro`, `ui-states`, `test-driven-development`*
*Fixes: F10, F11*

**Done when:** a purchase order is received in two partial deliveries, stock and branch cost update correctly after each, and a transfer with a shortage records the variance without inventing a "system" user.

- [ ] **8.1 Suppliers** list and detail.
- [ ] **8.2 Purchase orders:** create (Form Wizard), edit while draft, send, cancel.
- [ ] **8.3 Goods receipts:** receive part or all, with a note per line. Posts ledger rows and updates average cost.
- [ ] **8.4 Supplier payments** against received orders.
- [ ] **8.5 Transfers:** create, send (stock leaves the source), receive (stock enters the destination), variance handling with approval.
- [ ] **8.6 State machine tests** that reject every disallowed transition.

---

## Milestone 9: Reports and audit

*Specs: [[AngieBarato 08 - Reports & Dashboards]]*
*Skills: `performance-engineer`, `observability-and-instrumentation`*
*Fixes: F17, F18*

**Done when:** a manager sees the dashboard and reports for their branch within a second on a year of sample data, and day boundaries follow the branch's time zone.

- [ ] **9.1 Decide charts** (D8).
- [ ] **9.2 Dashboard** with today's sales, top products, low stock, open shifts, and sync health.
- [ ] **9.3 Reports:** daily sales, product performance, stock valuation, receivables aging, shift report, discount and void report, "needs review" flags.
- [ ] **9.4 Local report queries** on indexed `sale_day` columns (computed in the branch time zone when the sale is saved).
- [ ] **9.5 Export** to CSV and print.
- [ ] **9.6 Audit viewer** with filters and a before/after view.
- [ ] **9.7 Local logging** to a file in the user data folder, with a "send diagnostics" bundle.

---

## Milestone 10: Migration and pilot

*Specs: [[AngieBarato v2 - Open Decisions]] D11, D15*
*Skills: `deprecation-and-migration`, `deployment-procedures`, `ci-cd-and-automation`, `postmortem-writing`*
*Fixes: F19*

**Done when:** one branch runs a real trading week on v2, end of day totals match the owner's cash count, and there is a tested way to go back to v1.

- [ ] **10.1 Import script** for v1 products, branches, and users only (D11) into the v2 schema, with a dry run and a report. No customer balances and no sales history.
- [ ] **10.2 Opening stock:** a first stock count per branch. Customers start empty (D11).
- [ ] **10.3 Packaging:** `.deb`, AppImage, and Windows installer. Fix the Linux sandbox helper permissions for the `.deb`.
- [ ] **10.4 Auto-update** through GitHub Releases, with a signed update on Windows.
- [ ] **10.5 Backup:** a daily local SQLite backup and a restore screen.
- [ ] **10.6 Pilot checklist:** parallel run with v1 for three days, a rollback plan, and a daily review of the "needs review" list.
- [ ] **10.7 Training notes** for cashiers and managers (one page each).
- [ ] **10.8 Postmortem** after the pilot week.

---

## Risks

| Risk | Impact | Mitigation |
| :--- | :--- | :--- |
| Sync bugs lose or duplicate sales. | Wrong money. | Idempotency keys, outbox, chaos tests in M3. Fall back to PowerSync only if bugs persist (D7). |
| Two offline registers sell the last unit. | Negative stock. | Allowed and flagged (D3). Reviewed daily. |
| Credit over-limit while offline. | Bad debt. | Margin plus manager PIN (D4). Flag on sync. |
| Receipt format does not meet tax rules. | Compliance problem. | Ask the accountant before M6 (D5). |
| Astryx is new and Electron is not in its docs. | UI surprises. | The trial in M0 passed. Keep a list of gaps and use `astryx gap-report`. |
| SQLite file corruption or loss. | Lost unsynced sales. | WAL mode, nightly backup, sync as soon as online. |
| Scope growth. | Late pilot. | Variants, loyalty, and online store stay out of the first release. |
