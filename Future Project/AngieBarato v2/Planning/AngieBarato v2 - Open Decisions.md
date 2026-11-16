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
| D13 | PIN rules                                                                                          | **4 to 6 digits, argon2id or scrypt, 5 failures lock the PIN for 15 minutes, PIN works only on enrolled devices.**                                                                                                                 | M2     |
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
