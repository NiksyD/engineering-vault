---
title: "AngieBarato v2 - Open Decisions"
category: Decision Log
doc-status: Active
priority: P0
created: 2026-11-16
updated: 2026-11-16
tags:
  - angiebarato
  - decisions
---

# AngieBarato v2 - Open Decisions

Choices that are not settled. Each has a recommendation so work is not blocked. When one is decided, move it to "Decided" and write a short ADR in the repo. Part of [[AngieBarato v2 - Overview & Roadmap]].

## Decided

| # | Decision | Date |
| :-: | :--- | :--- |
| A1 | Desktop app with Electron, React 19, Vite (electron-vite). | 2026-11-16 |
| A2 | UI with Astryx only. No Tailwind. Template and component list in [[AngieBarato v2 - Astryx UI Map]]. | 2026-11-16 |
| A3 | The app must work offline and sync to Supabase when online. Local SQLite is the app's database. | 2026-11-16 |
| A4 | A new database. The v1 `products` and `branches` tables are kept, cleaned up, and re-keyed. | 2026-11-16 |
| A5 | A `profiles` table linked to Supabase Auth, replacing v1 `users`. | 2026-11-16 |
| D17 | Local database file is not encrypted by the app. Rely on operating-system disk encryption, documented in the install guide. File mode 0600. | 2026-11-16 |
| D18 | Each branch has one cashier, so per-user sessions are not built. Sign-out is blocked while the app is offline with unsynced documents, so a sale is never recorded under someone else. Revisit if two cashiers share a register. | 2026-11-16 |
| D19 | Product edits can be made offline, as a generic row upsert in the outbox. | 2026-11-16 |
| D20 | SQLite through `node:sqlite` (built into Electron 44) with plain SQL and numbered migrations. No ORM, no native module. | 2026-11-16 |
| D21 | **Production runs on a self-hosted Supabase in the owner's homelab**, not Supabase Cloud. See the hosting notes below. | 2026-11-16 |
| D22 | **Walk-in is the default customer.** A sale has no customer record unless the cashier picks one. The customer picker is optional and only needed for credit and statements. Credit requires a saved customer. | 2026-11-16 |
| D1 | One business with several branches. No `org_id` on tables. Multi-company is out of scope. | 2026-11-16 |
| D4 | Credit sales are allowed offline, up to the customer's last known limit minus a safety margin. Any over-limit sale needs a manager PIN. Two registers can still exceed a limit together, so the server flags it on sync instead of rejecting. | 2026-11-16 |
| D9 | Hardware: an Epson thermal receipt printer (model not chosen yet). Build to the ESC/POS command set, which Epson thermal printers use, and keep the printer behind one adapter so the model can change. Scanner: keyboard-wedge (types like a keyboard). Confirm the exact model and the cash drawer before M6. | 2026-11-16 |
| D11 | Import products, branches, and users only. No customer balances. Users are re-invited, not copied with passwords. Opening stock comes from a first stock count. Sales history stays in v1 as read-only. | 2026-11-16 |

## Open

Each row: the question, the options, the recommendation, and what it blocks.

|  #  | Question                                                                                           | Recommendation                                                                                                                                                                                                                     | Blocks |
| :-: | :------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----- |
| D2  | How to store money?                                                                                | **Integer centavos** (`bigint`) in both databases. No float rounding, and SQLite and Postgres match.                                                                                                                               | M1     |
| D3  | May stock go negative?                                                                             | **Yes, with a flag.** An offline sale is a fact. Block it only if a branch turns on "strict stock" in settings. Negative stock shows on a "needs review" report.                                                                   | M5, M6 |
| D5  | Tax included in price, or added on top? Do receipts need a government format and gap-free numbers? | **Ask the accountant before M6.** The design supports both: prices stored with a flag per setting. Per-register gap-free sequences already satisfy "no gaps" within a register.                                                    | M6     |
| D6  | Where does server logic run?                                                                       | **Postgres functions for posting** (atomic, close to the data) and **one Supabase Edge Function using Hono** for admin tasks that need the service-role key (create user, reset password, PIN verify). No separate server to host. | M1, M2 |
| D7  | Custom sync engine, or PowerSync?                                                                  | **Custom outbox and pull cursor.** Data is small, writes are mostly appends, and it avoids another paid service. Revisit PowerSync if sync bugs cost more than a sprint.                                                           | M3     |
| D8  | Charts: Astryx has no chart component in its component list.                                       | **Check the dashboard templates first** (`npx astryx template analytics-dashboard`). If they include chart code, reuse it. Otherwise use Recharts, which v1 already uses.                                                          | M9     |
| D10 | What happens to `angiebarato-mob`?                                                                 | **Park it.** Do not port it in v2. Revisit after the pilot.                                                                                                                                                                        | none   |
| D12 | Several registers per branch working offline together?                                             | **Support it from the start.** Per-register invoice sequences and a ledger-based stock model make it safe.                                                                                                                         | M3     |
| D13 | PIN rules | **Amended 2026-11-16.** 4 to 6 digits, not simple. **bcrypt (cost 12) through pgcrypto**, not argon2id or scrypt, because Postgres has no argon2 or scrypt and the same hash must verify offline in the app. 5 wrong tries lock the PIN for 15 minutes. The server checks online. Offline checks use hashes kept only in the app's main process, are marked unverified, and can be switched off in settings. | M2 |
| D14 | Supabase Realtime                                                                                  | **Off by default.** Sync by polling and on reconnect. Turn it on for one table only if a screen needs live updates.                                                                                                                | M3     |
| D15 | Where do installers live?                                                                          | **GitHub Releases** with `electron-updater`. v1 already publishes there.                                                                                                                                                           | M10    |
| D16 | Session length offline                                                                             | **A device stays usable offline for up to 14 days** since the last online check, then requires an online sign-in. Tune with the owner.                                                                                             | M2     |

## Questions for the owner

Answers to these settle D5, D12 and D16. D1, D4, D9 and D11 are decided above.

- [x] One business or several? One business, several branches (D1).
- [ ] How many registers per branch? Can the internet drop for hours?
- [x] Is credit sold to customers? Yes, including offline (D4). Still ask what happens when someone goes over the limit.
- [ ] Is the shop registered for tax, and does the accountant require a special receipt?
- [x] What printer? Probably an Epson thermal printer, model not chosen (D9). Drawer and scanner still to confirm.
- [x] Old data: products, branches, users only (D11).


## Hosting notes (D21)

The production database is a self-hosted Supabase (Docker) on the owner's own server, reached by every branch.

**What changes**
- **Storage is just disk.** There is no plan limit. More storage means a bigger disk or another volume. Nothing to buy from Supabase. Product images use the local storage volume by default, or an S3-compatible store (MinIO) if the disk is separate.
- **Backups become the owner's job.** There are none by default. Needed: a scheduled `pg_dump` (nightly) kept on a different disk and a copy off the machine, plus a restore test. A disk mirror (RAID or ZFS) protects against a dead drive but is not a backup.
- **The server is a single point of failure, which is why the app is offline-first.** Branches keep selling when it is down. A UPS and a monitored uptime check are worth having.
- **Security is the owner's too.** Strong secrets in `.env` (never the example ones), Postgres not exposed to the internet, and traffic from other branches over HTTPS through a reverse proxy (Caddy or Nginx) or, better, a private network (WireGuard or Tailscale) so the server is never public.
- **Upgrades are manual.** Pin the Supabase version, test an upgrade on a copy, and keep the migrations in this repo as the single source of schema.
- **Minimum hardware** per the Supabase docs: 4 GB RAM, 2 cores, 40 GB SSD. Recommended 8 GB, 4 cores, 80 GB or more SSD.

**What stays the same:** the schema, row level security, the posting functions and the app all work against any Supabase. The app already reads the secret key from `SUPABASE_SECRET_KEYS` or falls back to `SUPABASE_SERVICE_ROLE_KEY` in the Edge Function.

**To verify before the pilot (M10)**
- [ ] Which key format the chosen self-hosted version uses (the new publishable and secret keys, or the legacy anon and service-role JWTs) and that sign-in, `functions.invoke` and the admin script work with it.
- [ ] How Edge Functions are deployed self-hosted (files under `volumes/functions`, then restart the functions service), since `supabase functions deploy` is a cloud command.
- [ ] The admin script currently demands an `https` URL (or localhost). Allow a private network address if the owner uses a VPN with plain HTTP.
- [ ] A written restore drill: rebuild the server from a backup on a spare machine.
