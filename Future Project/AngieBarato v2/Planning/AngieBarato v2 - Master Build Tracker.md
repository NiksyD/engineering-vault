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
  - **Conflicts:** `resolveConflict` supports retry, accept (keep the server's version) and cancel. Accept and cancel free anything that was waiting on it. (The screen for this was built in M3e, see 3.9.)
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
- [x] **3.7 Connectivity (M3e, done):** the connection state ('unknown', 'online', 'offline') comes from the real result of the last sync round, not from a separate ping. It drives the menu dot and the offline banner.
- [x] **3.8 Invoice and document numbers (done in M3d):** gap-free per register, assigned in the same transaction as the sale. Proven again by the chaos suite (see 3.10).
- [x] **3.9 Sync UI (M3e, done):** `/sync` screen, menu entry with a status dot (All synced, Syncing, N waiting, Offline, N need attention), and an offline banner.
  - **Screen:** documents waiting (in words: "Sale BR1-R1-000007, 2 items · ₱1,234.56") and documents the server refused, each with Retry, Keep server version, or Cancel it.
  - **Rules:** deciding needs `approvals.give`; keep and cancel need a written reason; the decision is stored with who made it and why (local migration 0007).
  - **Tests:** 214 unit tests; `app-syncscreen-e2e.check.mjs` (35 checks in the real window). Sabotage-checked: removing the permission or the reason rule fails the tests.
  - **Not covered by an automatic test:** the offline banner in the real window (the app's network cannot be cut from the test). The state logic behind it is unit tested.
- [x] **3.10 Chaos tests (M3e, done):** `tests/checks/sync-chaos.check.mts`, 24 checks with real SIGKILL of separate processes.
  - **Selling:** killed 8 times mid-sale. Every sale the cashier saw confirmed was in the database, invoice numbers 1..N with no gaps or repeats, every sale queued, stock exact, integrity check ok.
  - **Sending:** killed 8 times mid-send. Every sale on the server exactly once, stock reduced once per sale.
  - **Long offline:** 500 sales sent in one go (about 10 s), no conflict, still gap-free.
  - **First download:** killed 6 times, then resumed. Every product arrived, all 15 tables marked done.
  - **Already covered earlier (sync-push check):** a duplicate request, a lost reply after the server committed, two registers selling the last unit.
  - **Limit:** SIGKILL tests a crash of the app, not a power cut. The database uses synchronous FULL, but a real power-cut test needs a VM or hardware.

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
- [x] **4.2 Categories (done):** `/categories`, needs `catalog.manage`. Tree of up to three levels: add, edit, move, add subcategory, turn off or on. Nothing is deleted.
  - **Works from this computer's own data**, so it works offline and other registers see changes after sync. A computer that is not set up as a register (or has not finished its first download) is asked to set up first.
  - **Rules checked locally, with clear messages** (`src/main/local/categories.ts`): name required; no repeat name in the same place; no fourth level (counting what hangs below when moving); no loops; cannot turn off a category that still has active subcategories; cannot turn on or add under a turned-off parent. The database enforces the three-level limit and the permission as well (a cashier's category is refused by the server and becomes a conflict).
  - **A queue bug found and fixed (also affected products from M3d):** an edit that replaces an older waiting edit kept the old place in the queue. Create product A, then category B, then move A into B: A went to the server before B existed and was refused. Now an edit is only merged into an older one when nothing newer is waiting. A test fails without the fix, and so does the real-server check.
  - **Verified:** 244 unit tests (30 new; depth and loop rules sabotage-checked); `catalog-sync.check.mts` against the real server (9 checks: offline order, move after creation, second register sees the tree, rename and turn-off travel, cashier refused, fourth level refused); `app-categories-e2e.check.mjs` in the real window (37 checks); full regression green (pull 25, push 32, chaos 24).
  - **Not built:** manual ordering (categories sort by name), delete (by design).
- [x] **4.3 Products (done, images left out on purpose):** `/catalog` (menu: Products), needs `catalog.manage`.
  - **List:** search by name, code or barcode (a scanner works: it types digits and Enter), filter by category (includes subcategories, or "No category") and Active, Turned off or All, 25 per page, total shown. Read from this computer's own data, so it works offline. Tried with about 29,000 products in the local database: opens and searches instantly.
  - **Form:** name, code (SKU), brand, category, unit, selling price, cost, taxable, track stock, description. Prices are typed in pesos and become whole centavos with no floating point (`parsePesos`, 6 tests). A bad amount is explained.
  - **Rules (checked locally with clear messages):** name required; a code (SKU) cannot repeat; a category must exist and be on (a product may stay in one that was turned off later); the same name as another active product is a **warning**, not an error; nothing is deleted, only turned off (an edit never turns a product back on).
  - **Price permission:** creating a product needs `catalog.manage`. Changing the price or cost of an existing product also needs `catalog.price` (the screen locks those fields, the service refuses, and the server's own rule is the final gate).
  - **Images:** the product has an `image_path` column and it is kept on every edit, but there is no upload. Decision: add small optional thumbnails with the sell screen (M6) only if wanted; it needs Supabase Storage on the self-hosted server.
  - **Not built yet:** branch price override and reorder point (4.5), price history screen (4.6), CSV (4.7), labels (4.8).
- [x] **4.4 Barcodes (done with 4.3):** several per product, one **main**, each with how many units it stands for (a pack barcode can mean 12). Added by typing or scanning and pressing Enter; remove; make main.
  - **Unique across the whole catalog, including turned-off products:** a clash names the owning product. A removed barcode is freed for another product; removed and re-added is the same row. Removing marks the row deleted and queues that (nothing is lost).
  - **Barcodes a scanner cannot send** (spaces, odd characters) are refused. Exactly one main barcode is always kept.
  - **Two registers adding the same barcode offline:** the first to send wins; the second is refused by the server and shows on the Sync screen as a conflict with the reason. The product itself still arrives.
  - **A sync bug found and fixed:** in that situation the register's next download crashed on its own unique rule (the server's row clashed with its own refused one), which would have stopped every later download. A pull now hides the local row that holds a barcode or code the server's row owns (the refused document stays in the Sync screen). Three unit tests fail without the fix, and so does the real-server check.
  - **Verified:** 292 unit tests (49 new; five key rules sabotage-checked); `catalog-products.check.mts` on the real server (15 checks: category and barcodes in order, found by either barcode on a second register, same barcode on two registers, removal and re-use, turn off, cashier refused); `app-products-e2e.check.mjs` in the real window (59 checks: scanner-style entry, bad price, duplicate barcode, same-name warning, edit, filters, paging with 30 products, turn off and on, reaching the server, reload).
- [x] **4.5 Branch pricing (done):** the product form has an "At this branch (BR1)" section: the branch's own price (empty = use the selling price), a reorder point, and "Sold at this branch". Works offline, syncs like the rest.
  - **One rule for the price a customer pays:** `effectivePriceCentavos` (`src/shared/pricing.ts`): branch price if set, else the default; a branch price of 0 is a real price. The product list already uses it ("₱45.00", with "Default ₱50.00" beneath, and a "Not sold here" marker); the sell screen (M6) will reuse it.
  - **Permission:** setting or changing a branch price needs `catalog.price`; the reorder point and availability need only `catalog.manage`. **Gap closed in the database** (migration `20261116180000_branch_price_insert_guard`): the existing trigger only watched UPDATE, so someone with `catalog.manage` alone could set a branch price by creating the row. 9 new database tests (160 in all); with the guard removed, the clerk test fails, on the real server too.
  - **Which branch:** a register holds only its own branch's data, so a computer sets the price for its own branch. Other branches set theirs from their own computers. Decision open: an online-only admin view to set every branch from one place.
  - **Not yet used:** the reorder point and availability are stored and synced; stock alerts (M5) and the sell screen (M6) will use them.
- [x] **4.6 Price history (done):** "Price history" in a product's row menu shows what changed (selling price, cost, or price at a branch), from and to ("default price" when a branch price is cleared), who, and when, newest first.
  - **Written by the server's own triggers** whenever a price or cost moves, so it cannot be skipped or edited. Changing only the reorder point or availability adds nothing.
  - **Needs the internet** (read from the server, like the Audit log): the history is not downloaded to registers. A name that cannot be read shows as "Another user".
  - **Limits:** the spec's "reason" is not recorded, because the triggers cannot know why a price changed; adding one needs a database change and a form field. A price set when a product is created is not a change.
  - **Verified:** 323 unit tests; `catalog-branch-prices.check.mts` on the real server (16 checks: branch row reaches the server and a second register, history with names and branches, clearing a price, a clerk can set a reorder point but not a price); `app-branchprice-e2e.check.mjs` in the real window (41 checks, including letters refused in the price and reorder fields). Full regression green: 160 database tests, five real-window suites (41, 63, 37, 35, 30), six real-server checks.
  - **A miss caught by the real-window test:** my first edit to the form silently did not apply and nothing but the real window could notice. The real-server and unit checks do not go through the form.
- [x] **4.7 Import and export (done):** Products page, menu "Import and export": Import from a CSV file, Export all products, Download a blank template.
  - **Import = choose, preview, confirm.** The preview runs every row through the SAME save code as a person's edit, inside a transaction it then rolls back, so it says exactly what the import will do (including rows that clash with each other) and saves nothing. Counts: new, updated, unchanged, with problems; the new categories; ignored columns; each problem with its row number as a spreadsheet numbers it (header = row 1) and a plain reason. "Import N products, skip M" saves the good rows together; a bad row is undone alone.
  - **Matching:** the `Id` column first (exports carry it), then the code, then any barcode. Without the Id, a re-imported export would have **duplicated every product with no code and no barcode** (found by the real-server check, not by the first unit tests). A blank Id is a new product. A column missing from the file leaves existing values alone; a blank price on an existing product keeps its price. Categories come from a path ("Food > Grain") and are created if missing (three levels at most, none turned off).
  - **Reading files:** quotes, commas and line breaks inside cells, a byte-order mark, comma or semicolon or tab separators (Excel varies by country), `12,50` as ₱12.50 (a decimal comma, never ₱1,250), UTF-8 only (a Latin-1 file is refused with "save as CSV UTF-8"), at most 10 MB and 20,000 rows. Text a spreadsheet would run as a formula is neutralised on export and restored on import.
  - **Permissions:** needs `catalog.manage`; a row that changes a price or cost needs `catalog.price` (otherwise that row is a problem, the rest go ahead).
  - **A speed problem found and fixed:** saving got slower with every queued row (0.8 s, 2.2 s, 3.6 s per thousand) because merging a repeated edit scanned every waiting document. Each queued row edit now carries an indexed `merge_key` (local migration `0008`); a thousand saves now take 0.13 to 0.31 s. The download's "is an edit still waiting" check uses it too, with a fallback for edits queued before the migration. 5,000 products import in about 4 s on this machine (an earlier note here said 1.5 s, which was wrong).
  - **A preview bug found and fixed:** a row that made a category and then failed was undone, but the preview still listed the category. A test now covers it.
  - **Known limit:** the queue sends one document at a time (about 18 ms each): 400 products reach the server in 14 s, so 5,000 products would take about 3 minutes in the background. Batching the sends would make it much faster; not built.
  - **Test hook:** a script cannot click an operating system file dialog, so a development build (never a packaged one) reads two environment variables, `ANGIEBARATO_TEST_IMPORT_FILE` and `ANGIEBARATO_TEST_SAVE_DIR`, in place of the dialogs.
  - **Verified:** 393 unit tests; `catalog-import.check.mts` on the real server (17 checks: categories, pack barcodes and branch values reach the server and a second register, re-import is "unchanged", export then import gives the same catalog, 400 products synced); `app-import-e2e.check.mjs` in the real window (49 checks, including quoted commas, a bad row, Excel-style semicolon and decimal-comma files, a non-UTF-8 file, a file with no Price column, and the exported file importing back with nothing changed). Key rules sabotage-checked.
- [x] **4.8 Label printing (done, printer still undecided):** "Print labels…" in a product's row menu. Prints on whatever printer the computer has, so it works with any printer you buy later.
  - **How:** the page prints itself with a print-only sheet of labels (a hidden sheet in the page, `@page` set to the label size, one label per page, no margin). No printer driver, no extra permission. The system print dialog opens and the person chooses the printer.
  - **Dialog:** label size (Small 40 x 25, Medium 50 x 30, Large 60 x 40, Wide 100 x 50 mm, or a custom width and height, 20 to 200 mm), copies (1 to 500), show the price, show the code, and a live preview of one label. Choices are remembered on this computer (not synced), saved when a person prints.
  - **Label:** name (shortened with an ellipsis if long), the barcode with its number under it, the code, and the price. **Barcode:** the product's main barcode. A valid EAN-13 is drawn as EAN-13; anything else (including a 13-digit number with a wrong check digit, which the library refuses) as Code 128. No barcode, or one a printed barcode cannot hold, gives a warning and a label with name and price only.
  - **Library:** `jsbarcode` 3.12.3 (pinned).
  - **Verified:** 10 unit tests (format choice, sizes, copies, text fitting; the check-digit rule is sabotage-checked); `app-labels-e2e.check.mjs` in the real window (45 checks). Because a script cannot answer the system print dialog, the test stubs `window.print`, then switches the page to print media (which applies the real print stylesheet) and measures: only the label sheet is shown, N labels each on its own page, each 50 x 30 mm (also 60 x 40 and a custom 70 x 35), the page size declared to the printer. Found by looking at the print screenshot: a long code ran into the price (now truncated).
  - **NOT verified:** a real print on a real printer. How a particular label printer paginates, scales or feeds the paper has not been tested, and this Electron build has no PDF export over its test interface. Test with the actual printer once you have one, and with a few labels first.
  - **Not built:** printing labels for several products at once, a label template editor, and the receipt printer (D9, Epson thermal) which is part of M6.

---

## Milestone 5: Inventory ledger

*Specs: [[AngieBarato 04 - Inventory & Stock Ledger]]*
*Skills: `database-design`, `test-driven-development`, `ui-states`*
*Fixes: F7, F10*

**Done when:** every stock change is a ledger row, on-hand equals the ledger sum in a test of 1,000 random movements, and a stock count with variances posts adjustments after manager approval.

- [x] **5.1 Ledger writer (done):** `src/main/local/ledger.ts`, `postMovement` is the only way stock changes on a register. It writes the ledger row and the cached balance in one transaction, refuses a zero movement, and does the same arithmetic as the server's trigger. Sales and adjustments both go through it.
  - **Verified:** 1,000 random movements across 3 branches leave on-hand equal to the ledger sum for every product (unit test, deterministic seed). Against the real server: 450 random movements, including fractions and negative stock, give identical on-hand AND average cost on the register and the server, and the server's own `stock_balance_drift` view is empty (`inventory-ledger.check.mts`). Key rules sabotage-checked (one equivalent mutation noted: at exactly zero stock the blend formula gives the new cost anyway).
- [x] **5.2 Stock on hand (done):** Inventory in the menu, needs `inventory.view`, read from this computer's own data so it works offline. Tiles for stock value, low, out of stock and negative; search by name, code or barcode; filter by category and by status; badges Negative, Out of stock, Low, In stock; value is on hand times the branch average cost (or the product's own cost before costed stock arrives); nothing counts for zero or negative stock.
  - **Shows this register's branch only** (the register holds only its branch's balances). A view of every branch for the owner would be online-only and is not built.
  - **Note for the pilot:** before the first stock count, every tracked product reads Out of stock. Load opening stock with a stock count (5.5) or adjustments.
- [x] **5.3 Stock history (done):** "Stock history" in the menu and "Stock history" in a product's row menu. Filters: reason, date range, one product. Shows when, product, change, reason (with the invoice number for a sale, and the note), cost, who. Newest first, "Load more".
  - **Needs the internet:** the register does not download movements, only balances, so this reads the server (like price history and the Audit log). A movement made by the system shows "System".
- [x] **5.4 Adjustments (done):** "Adjust stock…" in a stock row's menu, needs `inventory.adjust`. Take stock out or add, a reason that fits the direction (damaged, lost, expired and returned to supplier only remove; found only adds; correction and other either), quantity (letters refused as you type), a note, and a live "new total". Works offline and syncs.
  - **Approval:** above the approval limit (setting `adjustment.approval_threshold_centavos`, default ₱1,000, a branch value wins, read from the downloaded settings) a manager must approve, unless the person can give approvals themselves. The register asks for the PIN; the approval travels with the adjustment. The server checks it again.
  - **A real gap found and fixed:** the approval dialog told a stock clerk "You do not have permission", because only people who can sell could list the approvers. Found by looking at the real-window screenshot, not by any unit or server check. Anyone who sells or adjusts, counts or transfers stock may now ask a manager (migration `20261117100000_approval_requesters`, 11 new database tests, a shared list on the register).
  - **Verified:** 12 more unit tests per rule (boundary of the limit, direction, permissions; five rules sabotage-checked); `inventory-adjust.check.mts` on the real server (23 checks: one adjustment reaches the server once, a lost reply is not subtracted twice, two registers adjusting at once, the server refuses a large adjustment that bypasses the register's check, a manager's approval is accepted); `app-stock-e2e.check.mjs` in the real window (88 checks, including a wrong PIN refused and a verified approval on the server).
- [x] **5.5 Stock counts (done):** "Stock counts" in the menu (needs `inventory.count` or `inventory.count_approve`). Start a count (named, for example "Aisle 1"), scan or type a product, enter how many, repeat; remove a line; submit for approval; a manager approves (the differences become stock movements) or sends it back for a recount; cancel. A counter sees "Waiting for a manager" and no approve button. Works offline and syncs.
  - **How it avoids losing a sale:** each line records what the register held when that product was counted, and the variance is a change added to whatever the stock is at approval. A sale made after counting is kept (counted 8, one sold after, approved: 7, not 8). Tested.
  - **One unfinished count per product:** each register enforces it for the counts it knows about, and **the database enforces it too** (trigger), because two registers counting offline cannot see each other and approving both would post the same difference twice. The second register's line is refused and shows as a visible conflict.
  - **Why status changes are a posting function:** a register sends rows as an upsert, and Postgres checks the INSERT rule (status must be `open`) even when the row exists, so a count could never be sent as `submitted`. `post_stock_count_status` (migration `20261119100000`) does it, is idempotent by state, and refuses an empty count. Counts and their lines are now **downloaded** to registers (17 tables, was 15); an upgraded computer briefly shows "downloading" once.
  - **A download cannot undo a decision still waiting to be sent:** while a submit or approval is queued, the server's older status does not overwrite the local one (otherwise an approved count could flip back and be approved twice). Tested.
  - **Verified:** 26 database tests for counts (197 in all); 22 unit tests on the count rules with seven deliberate breakages caught; 8 more service tests (a counter cannot approve, an approver cannot count); `inventory-counts.check.mts` on the real server, 28 checks twice (offline count sent in order; a counter bypassing the register refused by the server; approval posts exactly the differences; a lost reply does not post twice; send back, recount, resubmit; two registers on the same product; cancel); `app-counts-e2e.check.mjs` in the real window, 71 checks.
  - **Known limit:** a register that stays offline a long time and then sends a count line for a product another count has since finished would carry a stale "system" quantity, and its variance would be applied on top. The register's own "last downloaded" time is the only warning. Not guarded.
  - **Not built:** counting by category or aisle list as a scope (the description is free text and a count only covers what is scanned), a printable count sheet.
- [x] **5.6 Cost method (done with 5.1):** moving average per branch in `stock_balances`, identical on the register and the server (450 random movements). A sale item snapshots the branch cost at sale time (already in the sale writer).
- [x] **5.7 Reconciliation (done):** "Check the stock" on Stock on hand asks the server to compare every balance of this branch with the sum of its ledger (the server's `stock_balance_drift` view) and shows "All N stock numbers match the history" or each difference with both numbers. Needs the internet and `inventory.view`.
  - **Verified:** unit tests (two deliberate breakages caught); in the real window the test corrupts one server balance to 13, the check names the product with 13 against 8, and after the balance is put back it is clean again. It also found nothing in 450 random movements and in every other run.
  - **Not built:** a scheduled job. This is a button; running it on a timer and alerting someone is for the pilot (M10).

---

## Milestone 6: POS and checkout

*Specs: [[AngieBarato 05 - POS & Checkout]]*
*Skills: `react-patterns`, `ui-states`, `accessibility-compliance-accessibility-audit` (or the existing `wcag-accessibility-audit`), `e2e-testing-patterns`*
*Fixes: F1, F4, F5, F9*

**Done when:** with the network off, a cashier opens a shift, scans and sells items with a split cash and GCash payment, prints a receipt, voids one sale and refunds another with manager approval, closes the shift with a cash count, and every sale syncs once on reconnect with the server totals matching.

- [x] **6.1 Shared pricing module (done):** `priceSale` in `src/shared/pricing.ts` is the only code that does sale math, and the register now prices every sale from its own catalog and settings. **This closes F1:** `recordSale` no longer accepts a price, tax or cost from its caller; it takes the product, the quantity and any discount, and works out the rest (`quoteSale` does the same for the sell screen, so what the cashier sees is what is saved).
  - **Rules:** exact integer arithmetic (BigInt), so a half centavo rounds the same on every computer and matches Postgres (halves up). A line is quantity (up to three decimals) times price. Line discount: a fixed amount or a percentage (two decimals), never more than the line. Cart discount: on what is left after line discounts, shared across the lines in proportion by the largest-remainder method (shares add up exactly; a tie goes to the earlier line; a free line gets none). Tax is worked out per line on what the customer pays after both discounts, rounded once, and only on taxable items. **Both tax modes are supported** (price includes tax, or tax added on top) because D5 is still open; the register reads the rate and the mode from the downloaded settings (a branch value beats the business-wide one).
  - **The price** is this branch's own price if it has one, else the default (`effectivePriceCentavos`). A turned-off product, or one this branch does not sell, cannot be sold. A rule of selling comes out as a `SaleRuleError` with a readable message.
  - **Verified:** 27 pricing tests (golden cases, rounding halves up for tax included and added, allocation and tie-breaking, refusing nonsense), including 3,000 random carts checked two ways (the totals identity, and an independently written fractions calculation) with six deliberate breakages caught; 9 more sale writer tests, six more breakages caught; `pos-pricing.check.mts` on the real server: 150 random sales in three tax configurations (included 12%, added 12%, added 7.5%) with discounts, branch prices and non-taxable items: every subtotal, discount, tax, total and line total identical on the register and the server, no price or total mismatch flagged, no stock drift. The earlier push and chaos checks pass with register-priced sales.
  - **Still to do on the server (6.9):** `post_sale` checks the price against the catalog and that the totals are consistent, but it still **takes the tax amount from the device**. A tampered tax would not be flagged yet.
- [x] **6.2 Shifts (done):** a cashier opens a shift with the cash in the drawer and closes it with a count. The register works out the expected cash itself (float plus cash taken on sales that were not voided; card and GCash are not in the drawer), and the close screen is a **blind count**: the expected amount is shown only after a count is typed. A difference needs a written reason, on the screen, in the register, and on the server. Works with no internet. Screen: Sell > Shift, with recent shifts and their reasons.
  - Server: migration `20261120100000_shift_close` adds `post_shift_close` (a shift could not be sent as closed by upsert, because the insert rule demands "open", same as stock counts) and one open shift per register. Only the cashier who opened it, or a manager, may close it. Closing twice is a no-op; a closed shift cannot be edited.
  - Sync: the close is queued after the shift's sales, and a pull cannot reopen a shift whose close is still waiting.
  - Tests: 15 database tests (`10_shifts`), 25 shift unit tests (8 mutations caught), 5 service tests, 3 pull tests, real-server `pos-shifts` 21/21 (offline day, close 5.00 short, sent once, server numbers match, forged and duplicate shifts refused), real-window `app-shift-e2e` 46/46.
  - **Not yet:** the server does not recompute the expected cash (needs refunds and customer payments from 6.8 and M8), and the sell screen does not yet refuse a sale when no shift is open (6.3/6.6).
  - Hosted project needs `20261120100000_shift_close` pushed too.
- [x] **6.3 Sell screen (done, without payment):** Sell > Point of sale. Scan or type a barcode, code or name; a whole barcode adds its item straight away (a pack barcode adds its pack quantity), a name shows a short list. Quantities are typed (letters ignored, three decimals), the same product scanned twice adds to its line, a line over the stock on the shelf is flagged but not blocked. Prices come from the register's catalog and branch prices through `quoteCart` (so what the cashier sees is what 6.1 will save). Needs an open shift, else it offers to open one.
  - **Discounts:** per line and for the whole sale, as a percent or an amount. Any discount needs `sales.discount`. A cashier may give up to `discount.cashier_max_percent` (5 by default) of the subtotal, line and cart discounts together; above it the screen asks for a manager PIN. The manager's approval covers that discount or a smaller one, and asks again if the discount grows. A manager is never held to the limit.
  - A sale in progress is cleared when anyone signs in or out, and survives moving between screens.
  - Tests: 16 sell unit tests (7 mutations caught), 5 service tests, 11 cart tests, real-window `app-pos-e2e` 72/72 (scan, pack, search, quantity, stock warning, discounts as a manager, cashier asking a manager with a wrong then right PIN, approval covering a smaller but not a bigger discount, sign-out clearing the sale).
  - **Not yet:** "Take payment" is a disabled button (6.5/6.6), and the approval id is not yet carried into the saved sale (done with 6.6). Search shows at most 12 products.
- [x] **6.4 Hold and resume (done):** on the sell screen, **Hold** puts the sale aside under an optional name (for example the customer's) and empties the screen for the next customer; **On hold (n)** lists the waiting sales (name, item count, who held it, when) with Resume and Delete (asks first).
  - A held sale lives only on this register (local migration `0010_held_carts`): it touches no stock, queues nothing for the server, and keeps no prices, only the products, quantities and discounts. It is priced again when resumed, so a price change while it waited is respected, and a product turned off or no longer sold here is left out with a message naming it.
  - Any cashier at the same register can resume a held sale (it shows who held it). It is given back once and forgotten, so it cannot be resumed twice. Resuming needs an empty screen. A manager approval does not travel with it: a discount over the limit is asked for again.
  - Limit: 20 held sales per register. Resetting the computer's register setup wipes them (a pre-reset backup is taken first).
  - Tests: 14 held unit tests (7 mutations caught), 4 service tests, cart test; `app-pos-e2e` now 113/113 (hold, resume, repriced, delete with confirm, a product turned off while waiting, a second cashier resuming).
- [x] **6.5 Payment and 6.6 Complete sale (done):** **Take payment** opens one dialog: cash received (with Exact and bill buttons), card, GCash, any mix, with the change shown live. Complete sale saves everything in one local transaction and queues it. Only cash, card and GCash (decision: no other methods); both tax modes are supported and shown on the screen (tax included or added), pending the accountant (D5).
  - **The register works out the payments itself** (`settle` in `src/shared/payment.ts`, shared by the screen and the register, 5,000 random cases): card and GCash pay exactly what is given and cannot exceed the total; cash pays the rest and anything more is change. `recordSale` now refuses a payment, change or tendered amount that does not add up, so a caller cannot invent them.
  - **Needs an open shift** (the sale is tied to it). A discount over the limit needs a manager approval to come with the sale.
  - **Credit:** the unpaid rest goes on a saved customer's account (search by name or phone). Checked against the customer's limit; with no internet only the limit minus `credit.offline_margin_percent` (10 by default) may be used (D4). Over the limit needs `sales.credit_override` or a manager PIN, and the approval is saved with the sale.
  - **Defect found and fixed:** the server counts a manager approval as verified only if it is tied to the sale it was given for, but the approval was asked for before the sale had an id, so every approved sale would have been flagged `unverified_approval`. The sale now gets its id when it starts, the approval is tied to it, and the real-server test confirms no flag.
  - Tests: 12 payment tests (6 mutations caught), 9 credit tests (6 caught), 7 new sale-writer payment tests, 29 service tests (9 mutations caught); `app-pay-e2e` 87/87 (cash and change, split cash+GCash with reference, card slip, mistakes refused, exact, cancel, credit, cashier over the limit asking a manager with a wrong then right PIN, server totals, ledger, approvals tied to the sale, no flags, no stock drift). Full regression green (212 database tests, 669 unit tests, every real-window and real-server check).
  - **Not yet:** the receipt (6.7), customers cannot be created yet (screen is M8; credit uses customers already downloaded), no credit due date, and the server's tax re-check was added in 6.9.
- [x] **6.7 Receipt:** preview, print, reprint marked COPY with a log entry. *(done 2026-11-19)*
  - Server: `post_receipt_print` (idempotent, only someone who may sell at the sale's branch), 8 pgTAP tests. Needs pushing to the hosted project: `20261121100000_receipt_prints`.
  - Register: `src/main/local/receipts.ts` builds the receipt from the saved sale (names and prices as sold) plus company name, address, tax ID and footer from settings; the local `receipt_prints` table (migration 0011) is the log and each print is queued for the server after its sale.
  - Screen: a Receipt button on "Sale complete" opens a preview (58 or 80 mm paper, remembered per computer). Print goes through the system print window, so any installed printer works (D9 still open). The first print is the original; every later one says `*** COPY ***`. Looking at the receipt is not a print. Both tax modes are worded (`Includes 12% tax` or `Tax (12%)`).
  - A print never touches the sale: if printing or logging fails the sale is saved and the receipt can be printed again.
  - **Not yet:** raw ESC/POS and the cash drawer kick (need the printer model, D9), printing on its own right after the sale, finding an older sale to reprint (done in 6.8, the Sales screen), and the cashier's name on a receipt printed by someone else (names of other users are not on the register).
  - Cancelling the print window still counts as a print (the browser cannot tell).
- [x] **6.8 Returns and voids** with approval, restock choice, and refund method. *(done 2026-11-19; also the Sales screen, which was not a listed step)*
  - **Sales screen** (`/pos/sales`, under Sell): this shift, today or every sale this computer has, newest first; search by invoice number or customer. Open a sale to see what was sold, how it was paid, what was returned, its receipt (so a receipt that was forgotten can be printed again as a COPY), and to void it or take items back. Reads only this computer's data, so it works offline.
  - **Void:** a sale of the shift that is open now, not already voided, nothing returned from it. The reason is required. The stock it took goes back, an unpaid (credit) part comes off the customer's account, and the sale stays on record as voided.
  - **Return:** any completed sale, any shift, whole or part. Quantities per line (up to what is left), each line back on the shelf or damaged (no stock), a reason, and the refund as cash, card, GCash or store credit (store credit needs a customer on the sale). Needs an open shift. The refund is the line total times the share returned, rounded the same way as the server (BigInt). A cash refund comes out of the expected drawer cash at shift close; the shift screen shows it.
  - **Approval:** someone who holds `sales.void` / `sales.refund` does it alone; a cashier gets the manager PIN dialog after the form is filled in. The approval is tied to the sale (void) or to the return (the id is made when the dialog opens).
  - **Server (migration `20261122100000_void_return_approvals`):** `post_void` and `post_return` used to demand the permission from whoever *sent* them, so a cashier's sync would have been refused even with a manager's PIN. They now accept a cashier who carries the approval of a manager who holds the permission and may give approvals; an approval the server did not verify is recorded and flagged on the sale (`unverified_approval`, or `offline_approval`). Both also take the `ledger_id` the register used, so the customer ledger row that comes back down is the same row and not a second one counted twice. 19 new database tests.
  - **Sync:** the register now downloads `sale_returns` and `sale_return_items` (migration 0012 locally), and a sale whose void or return is still waiting to be sent is protected from being put back by an older server row.
  - Tests: 17 void/return tests (4 mutations caught), 4 service tests, 4 pull-protection tests (mutation caught), `app-sales-e2e` 78/78 (list, search, reprint, return as manager by cash, void as manager, damaged store credit, cashier with wrong then right PIN for a void and a return, then the server and the computer agree: statuses, 3 returns worth ₱1,500.00, verified approvals tied to the void and the return, no flags, the customer account nets to nothing and is not counted twice, stock 99 on both, no drift).
  - **Not yet:** a refund slip (the receipt of a voided sale says VOIDED; a return has no paper of its own), a void is not refused by the server when its shift has closed in the meantime (the register enforces it), refunding cash on a credit sale does not reduce what the customer owes (the manager picks store credit for that), collections against a sale are not checked on the register (the customer payments screen is M8), and the server does not yet review flagged sales (6.9).
  - Needs pushing to the hosted project: `20261122100000_void_return_approvals` (with the four already waiting and `20261121100000_receipt_prints`).
- [x] **6.9 Server recompute:** `post_sale` recomputes totals and flags mismatches (D3, D4). Flags show on a review screen. *(done 2026-11-19)*
  - **Tax re-check** (migration `20261123100000_sale_tax_check`): the server works the tax out again line by line from the catalog (taxable products only, after each line's share of the cart discount, tax taken out of the price or added on top). It flags `tax_mismatch` when the register's tax differs by more than a centavo per line, or when its lines do not add up to its tax. The register now sends the tax rate and the mode it used (`tax_rate_percent`, `prices_include_tax`); the server flags `tax_setting_mismatch` when they differ from the settings now (this branch's own value first). A setting changed while a register was offline looks the same as a register that lies, so a person decides. Old queued sales without those fields are checked against the settings now. A flag never refuses a sale.
  - **Tolerance:** the server's cart-discount shares skip the register's "leftover centavo" step, so each line may differ by a centavo. A tampering of one or two centavos on a many-line sale is therefore not caught; larger ones are.
  - **Review** (migration `20261123100100_sale_reviews`): `sale_reviews` (append-only, keeps the flags that were reviewed and an optional note), view `sales_needing_review` (flagged sales whose flags a review does not cover, so a sale flagged again later returns), `review_sale` (needs `approvals.give` at the sale's branch, idempotent, audited as `SALE_REVIEWED`).
  - **Screen:** Admin → **Flagged sales** (`/admin/review`, for `approvals.give`): lists what the server flagged with the flags in words, and each sale opens to what the server noticed, what to check, and Mark as reviewed with a note. Needs the internet (it reads the server, and so shows every register of the manager's branches). Flag wording is in `src/shared/saleFlags.ts`.
  - Tests: 15 tax database tests (2 mutations caught) and 12 review database tests (266 in all), `pos-pricing` 16/16 (the register's tax equals the server's re-check on 150 random carts in both modes at 12% and 7.5%, no flag), `sale-review` 15/15 against the real server, `app-review-e2e` 17/17 in the real window, a payload unit test (mutation caught), flag wording tests.
  - **Not yet:** a count of unreviewed sales on the home screen or menu, filtering the list by branch or flag, and unflagged-but-suspicious patterns (many voids by one cashier) which belong to reports (M10). The server still does not recompute the expected cash of a shift.
  - Needs pushing to the hosted project: `20261123100000_sale_tax_check` and `20261123100100_sale_reviews` (with the five already waiting).
- [x] **6.10 Keyboard flow** and touch targets. Run the accessibility audit. *(done 2026-11-19; also a date filter on the Sales screen)*
  - **Keys on the sell screen:** `F2` goes to the search box, `F4` takes payment (when there is a quote and nothing waits for a manager), `F6` puts the sale on hold, `Esc` closes any window. The keys do nothing while a window is open, so a shortcut never acts behind one. They are shown with the design system's `Kbd` under the search box and on the Hold button; the pay button shows plain `F4` in its own colour (the key-cap look has white text, which cannot be read on the light primary button; axe found this). Buttons carry `aria-keyshortcuts`.
  - **Cursor placement:** the payment, hold and discount windows put the cursor in their first box when they open, and "New sale" is focused on the Sale complete screen, so Enter finishes a sale and starts the next one with the cursor back in the search box. A full sale (scan, pay, change, next sale) and holding a sale are done in the test with no mouse.
  - **Touch targets:** every button on the sell screen and in the payment window is at least 44 by 44 pixels (`touch.ts`); the design system's largest button is 36. The test measures them.
  - **Accessibility audit:** axe-core (dev dependency) at WCAG 2.0/2.1/2.2 A and AA over the sell screen (empty and with an item), payment, hold, sales, one sale, shift and flagged sales, in dark and light. It found two things, both fixed: the page had no `lang` (serious), and the white F4 key cap on the light button (contrast 1.11, serious). Now no violation of any kind.
  - **Sales screen date filter:** Show → Choose dates, with a date range picker (either end may be left open), filtered by the branch's own sale day.
  - Tests: `app-keys-e2e` 60/60, date range unit test (mutation caught), `app-sales-e2e` 83/83.
  - **Not yet:** an automatic audit does not catch everything (reading order, screen-reader wording, a cashier who cannot see colour): a person with a screen reader should try the sell screen once. The other screens (inventory, products, admin) were not audited. Shortcuts for the Sales and Shift screens, and Enter to pick the first search result, are not built. The window's close button and the sidebar controls are the design system's own size (28 to 32 pixels).
- [x] **6.11 End-to-end test** of the done-when scenario (2026-11-19). `tests/checks/app-day-e2e.check.mjs` cuts the connection with a switchable proxy (`flaky-proxy.mjs`): a cashier works a whole shift offline (split cash and GCash, receipt, a void and a return approved with a manager PIN, shift close), then one sync, then the server and register totals match. 54 checks. It uses the same real-window method as the other suites, not Playwright.

---

## Milestone 7: Customers and credit

*Specs: [[AngieBarato 06 - Customers, Credit & Payments]]*
*Skills: `database-design`, `test-driven-development`*
*Fixes: F8*

**Done when:** a customer buys on credit, makes two partial collections on different days, and the statement shows each invoice and payment, with the balance equal to the ledger sum. An over-limit sale needs approval and the approval is on the sale.

- [x] **7.1 Customers** (2026-11-20). Customers screen: anyone who sells or collects can look (name, phone, what they owe, limit, over-limit mark, search); `customers.manage` adds, edits and turns off. Offline, rules checked on the register (name, phone 7+ digits and not shared, a customer who owes cannot be turned off). `app-customers-e2e` 57. Not yet: paging.
- [x] **7.2 Customer ledger** (2026-11-20). A collection's ledger row takes the id the register chose (migration `collection_ledger_id`), so nothing is counted twice. New `post_customer_adjustment` (migration `customer_adjustment`): a manager's opening balance (once per customer) or a correction up or down, with a reason, audited. Pgtap 15 and 16.
- [x] **7.3 Collections** (2026-11-20). Collect on the Customers screen: oldest invoices first, or choose the invoices; cash, card or GCash; cash counts in the shift's drawer; cannot pay more than owed. `app-collect-e2e` 55. Not yet: invoices of another branch are not listed (that part goes on the account), no screen to reverse a collection, no printed slip.
- [x] **7.4 Statement** (2026-11-20). Every line with its running balance, a chosen period with the balance brought forward, and a printable A4 sheet. Not yet: tried on a real printer.
- [x] **7.5 Receivables** (2026-11-20). Decided: credit sales are due 30 days after the sale (setting `credit.term_days`, migration `credit_terms`). Buckets: not due, 1-30, 31-60, 61-90, over 90; payments use the oldest debt first; an opening balance is due the day it was entered; store credit shown apart. `app-receivables-e2e` 39. Not yet: export, an "as of" date.
- [x] **7.6 Credit rules (D4)** (2026-11-20). Built in M6 and checked again: the limit, the lower limit with no internet (margin setting), a manager's PIN for an over-limit sale, and the server flagging `over_credit_limit` when no verified approval comes with it. Covered by `app-pay-e2e` and the M7 done-when test.
- [x] **7.7 Done-when test** (2026-11-20). `tests/checks/app-credit-e2e.check.mjs` (43 checks): credit up to the limit, two partial payments (cash, then GCash), the statement lines and balances equal the ledger sum, an over-limit sale approved with a PIN and the verified approval tied to that sale on the server, register and server agree. The window cannot move the clock, so the two payments are taken one after the other here; the unit tests cover payments on different days.

---

## Milestone 8: Procurement and transfers

*Specs: [[AngieBarato 07 - Procurement & Transfers]]*
*Skills: `form-cro`, `ui-states`, `test-driven-development`*
*Fixes: F10, F11*

**Done when:** a purchase order is received in two partial deliveries, stock and branch cost update correctly after each, and a transfer with a shortage records the variance without inventing a "system" user.

- [x] **8.1 Suppliers** (2026-11-20). Suppliers screen (Stock menu): anyone who manages or receives deliveries can look; `procurement.manage` adds, edits and turns off. Offline, kept on the computer (local table, downloaded, sent as an upsert). Rules: name required and not shared (any capitals), phone 7+ digits, valid email. Search finds name, contact, phone (also by its digits) and email; the same digit search was added to customers and the register's customer search. `app-suppliers-e2e` 36. Not yet: a supplier detail page (it comes with purchase orders in 8.2), paging.
- [x] **8.2 Purchase orders** (2026-11-20). Purchase orders screen (Stock menu) and an order page: pick a supplier, find products by name/code/barcode (cost starts at the product's usual cost), quantities to 3 decimals, running total; save a draft, edit it while it is a draft, send it to the supplier (then read-only), print it on A4, cancel a draft or a sent order. Numbers like `PO-BR1-R1-000001`. Offline, downloaded for the branch. New server function `post_order_status` (migration `order_status`): an upsert is checked as a new draft, so sending/cancelling goes through a posting function, with the pull protected so an older server status cannot put it back. `app-orders-e2e` 59, 14 unit tests (one covers every allowed and refused move of the state machine; the database refuses the same moves), pgTAP 18. One page instead of a wizard. Not yet: receiving (8.3), a supplier detail page showing their orders, paging.
- [x] **8.3 Goods receipts** (2026-11-20). Receive goods on a sent or partly received order: what arrived per line (starts at what is still to come), the cost confirmed per line (starts at the ordered cost), a note per line, the supplier's invoice number and a delivery note. Stock goes up at once at that cost and the branch average cost blends; the order becomes partly received, then received when every line is in, and then has no Receive or Cancel button. More than ordered needs `procurement.over_receive` (Admin has it, Manager does not). The order page lists every delivery. Offline; the server's existing `post_goods_receipt` does the posting (no new migration); downloads cannot put an older status or received quantity back while a delivery waits to be sent. `app-receiving-e2e` 70, 14 unit tests (mutations caught). **Delivery draft:** what is typed in Receive goods is saved on the computer as it goes (never synced, never touches stock), so a closed window or power cut does not lose a half-counted delivery; the order says "A delivery was started on this computer" and the button becomes Continue delivery; **Start over** puts every line back to what is still to come at the ordered cost and clears the draft; recording the delivery deletes it. Not yet: a draft cannot be continued on another computer. Not yet: correcting a delivery entered wrongly (the receipt is a document that is never edited), a supplier invoice matched against the order.
- [x] **8.4 Supplier payments** (2026-11-20). **Pay supplier** on an order that has received goods (needs `procurement.manage`): amount (starts at what is owed), how paid (cash, bank transfer, GCash, cheque, other) and a reference. What is owed = the goods received so far at the cost on each delivery, less earlier payments; a payment can never be more than that, and not on an order with nothing received. The order shows goods received, paid, still owed and each payment; the order list has an Owed to supplier column. New server function `post_supplier_payment` (migration `supplier_payments`) works out what is owed itself, so two computers cannot pay the same debt twice (the second is held as needing attention with the reason), and writes the audit log. Offline. `app-supplierpay-e2e` 37, 6 unit tests (mutation caught), pgTAP 19. Not yet: a supplier-level payables overview and aging, paying one payment across several orders, a way to correct a wrong payment, cash payments taken from the shift's drawer.
- [x] **8.5 Transfers** (2026-11-20). Transfers screen (Stock menu): what leaves this branch and what is on its way here. Draft a transfer (destination branch, note, products this branch holds with their quantity), cancel a draft, send it: the stock leaves this branch at once at its average cost (the cost the other branch brings it in at). The other branch downloads it, counts what really arrived per line and receives it; a shortage is recorded on the transfer as received with a shortage and needs a manager (the person receiving if they may approve, otherwise a PIN approval tied to the transfer). Both ends work offline; received by the real person, no made-up system user. Numbers like `TR-BR1-R1-000001`. New sync scope `either` (transfers are downloaded by both branches), new server function `post_transfer_status` (migration `transfer_status`) because an upsert cannot cancel. `app-transfers-e2e` 68 (one computer set up as branch A, then B, then A), 15 unit tests (mutations caught), pgTAP 20. Not yet: a printed transfer slip, a transfer cannot be fixed after sending (the receiver records what arrived), unit cost of an old transfer is not shown to a branch that is not part of it.
- [x] **8.6 State machine tests** (2026-11-20). `supabase/tests/database/21_state_machines.test.sql` tries every pair of statuses on a purchase order and on a transfer against the database and checks that exactly the allowed moves succeed and nothing leaves received or cancelled; the register has the same table (`PO_TRANSITIONS`, `TRANSFER_TRANSITIONS`) with unit tests for every pair.

**Milestone 8 is built.** Not yet in M8: a supplier detail page, payables overview with aging, correcting a delivery or a payment entered wrongly, a printed transfer slip.

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
