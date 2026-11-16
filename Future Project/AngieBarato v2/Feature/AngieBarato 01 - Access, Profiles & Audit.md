---
title: "AngieBarato 01 - Access, Profiles & Audit"
category: Feature Spec
doc-status: Draft
priority: P0
milestone: M1, M2
created: 2026-11-16
updated: 2026-11-16
tags:
  - angiebarato
  - feature
  - security
---

# AngieBarato 01 - Access, Profiles & Audit

Part of [[AngieBarato v2 - Overview & Roadmap]]. Built in Milestones 1 and 2 of [[AngieBarato v2 - Master Build Tracker]]. Fixes F2, F3, F4, F16, F18 in [[AngieBarato v2 - Existing System Analysis]].

## Purpose

Decide who can do what, prove who did it, and let a manager approve a risky action in a way that cannot be faked later.

## How it works

**Sign in**
1. A user signs in with email and password through Supabase Auth. The session is stored with Electron `safeStorage`.
2. The app downloads the user's profile, role, permissions, and branches, and caches them.
3. Offline, the cached profile lets the user continue for up to 14 days since the last online check (D16). After that, an online sign-in is required.

**Quick unlock and approvals with a PIN**
- A PIN is a shortcut on a device that is already enrolled. It never replaces the password.
- A manager approval asks for the manager's name and PIN. A successful check creates one `approvals` row tied to one action and one document.

**Audit**
- Every sensitive action writes an `audit_logs` row in the same transaction as the change: who, which branch, which device, what, and before and after values.

## Tables

`profiles`, `profile_pins`, `roles`, `permissions`, `role_permissions`, `devices`, `approvals`, `audit_logs`. Columns are in [[AngieBarato v2 - Architecture & Data Model]].

- `profiles.id` equals the Supabase auth user id. The email stays in `auth.users` only.
- `profile_pins` is separate and is not readable through the Data API.
- Role and branch are never stored in `user_metadata`, because users can edit it.

## Roles and permissions

| Role | Starts with |
| :--- | :--- |
| Admin | Every permission. |
| Manager | Everything in their branches except user and role management. Can approve overrides. |
| Cashier | Sell, hold, take payment, reprint a receipt, open and close their own shift. |

Permission codes follow `module.action`:
`sales.create`, `sales.discount`, `sales.void`, `sales.refund`, `sales.credit_override`, `inventory.view`, `inventory.adjust`, `inventory.count`, `procurement.manage`, `procurement.receive`, `catalog.manage`, `catalog.price`, `customers.manage`, `customers.collect`, `reports.view`, `admin.users`, `admin.roles`, `admin.settings`, `admin.audit`.

An admin can edit roles and add custom ones. A permission change takes effect the next time the profile syncs, and it is checked from the table, not from a cached token.

## Rules

- **Three checks, one rule set:** row-level security in the database, `requirePermission` at the top of every service method, and hidden controls in the UI. Only the first two protect anything.
- **An approval is scoped.** It records the approver, the requester, the action type, the document, the reason, and the device. It cannot be reused for another action.
- **PIN policy:** 4 to 6 digits, argon2id or scrypt, five failures lock that PIN for 15 minutes, and a PIN works only on devices where the approver is enrolled (D13).
- **Approvals list the approver by name.** The old "match any manager's PIN" lookup is removed (F4).
- **Offline approvals** are checked against the cached hash, saved with an `offline` flag, and shown on the "needs review" screen after sync.
- **An inactive user** is rejected on the next sync, and the device removes the cached session.
- **Settings are typed.** Each setting has a type and a validation rule, and branch settings can override global ones (F16).
- **Audit rows cannot be edited or deleted** by anyone through the app.

## Screens

See [[AngieBarato v2 - Astryx UI Map]]: Login Card, Settings Panels, Searchable Table for users, roles, and audit.

## Done when

- A cashier cannot open an admin route, cannot call an admin service through IPC, and cannot read another branch's data through the database.
- A manager PIN approval creates a row that points to the sale it approved.
- Five wrong PINs lock the PIN.
- Every create, update, and delete of a sensitive record has an audit row with the same transaction id.
