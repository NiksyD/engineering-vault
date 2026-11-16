---
title: "AngieBarato v2 - Astryx UI Map"
category: Frontend Design
doc-status: Draft
priority: P1
created: 2026-11-16
updated: 2026-11-16
tags:
  - angiebarato
  - frontend
  - astryx
---

# AngieBarato v2 - Astryx UI Map

Which Astryx template and components each screen starts from. Part of [[AngieBarato v2 - Overview & Roadmap]].

Source lists: [components](https://astryx.atmeta.com/components) and [templates](https://astryx.atmeta.com/templates). Names below match those pages (checked 2026-11-16).

**How to use this note**
- Start every screen from a template with `npx @astryxdesign/cli template <name>`, then adapt it. Templates are content-only, so wrap them in the app shell.
- Look up a component's real props before using it: `npx @astryxdesign/cli component <Name>`. Example: `Button` requires a `label` prop, which a plain `<Button>text</Button>` does not provide.
- Use Astryx components only. No raw HTML elements and no inline `style` for layout, once the lint rule is added (same rule as Anneal).
- The app already follows the system's light or dark mode. A fixed theme or a toggle is an open item (see [[AngieBarato v2 - Master Build Tracker]], M2).

## 1. App shell

| Need | Use |
| :--- | :--- |
| Overall frame | Template **Side Nav** (collapsible, resizable left rail) with the `AppShell`, `SideNav`, and `TopNav` components. |
| Navigation groups | `SideNav` sections: Sell, Inventory, Procurement, Customers, Reports, Admin. Items are hidden by permission. |
| Quick find | `Command Palette` for jump to screen, product, customer. Shortcut hints with `Kbd`. |
| Branch and register switch | `Selector` in the top bar. |
| Sync and connection status | `Status Dot` plus `Badge` in the top bar, and a `Banner` when offline or when conflicts need review. |
| Notifications | `Toast`. |

## 2. Screen map

| Screen | Starting point | Components |
| :--- | :--- | :--- |
| **Sign in** | Template **Login Card** (or **Login Split**) | `Field`, `Text Input`, `Button`, `Banner` for errors |
| **PIN unlock / approval** | None. A short custom dialog. | `Dialog`, `Number Input` or four `Text Input` cells, `Banner` |
| **POS (sell screen)** | None. Compose from `Layout` + `Grid`. | Left: `Typeahead` for search and scan, `Grid` of `Clickable Card` product tiles, category `Tab List`. Right: cart as `Table`, `Number Input` for qty, `Metadata List` for totals, big `Button` for Pay. `Kbd` for shortcuts. `Empty State` for an empty cart. |
| **Payment** | Template **Checkout Form** (for the summary that updates live) inside a `Dialog` | `Segmented Control` for method, `Number Input` for tendered, `Metadata List` for change due, `Field` per payment line |
| **Held carts** | `Drawer` | `List`, `Timestamp`, `Button` |
| **Shift open and close** | Template **Dialog Wizard** | `Stepper`, `Number Input` (cash count by denomination), `Metadata List` (expected vs counted) |
| **Receipt** | None. A print layout. | `Text`, `Divider`, thermal printer output |
| **Products list** | Template **Filterable Table** | `Table`, `Power Search`, `Table Selection Toolbar`, resizable detail pane |
| **Product detail / edit** | Template **Product Detail** for viewing, **Two-column Form** for editing | `Thumbnail`, `Form Layout`, `Field`, `Text Input`, `Number Input`, `Switch`, `Tokenizer` for barcodes, `File Input` for image |
| **Categories** | Template **Tree Table** | `Tree List` |
| **Branches, registers** | Template **Searchable Table** + `Dialog` form | `Table`, `Form Layout` |
| **Stock on hand** | Template **Grouped Table** (group by branch or category) | `Table`, `Badge` for low stock, `Status Dot` |
| **Stock movements (ledger)** | Template **Searchable Table** | `Date Range Input`, `Selector` for reason |
| **Adjustments** | `Dialog` form | `Complex Selector` for product, `Number Input`, `Selector` for reason, approval dialog if needed |
| **Stock count** | Template **Inline Wizard** | `Number Input` per line, variance `Badge` |
| **Customers list** | Template **Searchable Table** | `Table`, `Badge` for over-limit |
| **Customer detail and statement** | Template **Order Detail** (record, totals, timeline) | `Metadata List`, `Table`, `Timestamp`, `Button` for Collect |
| **Collect payment** | `Dialog` | `Number Input`, `Segmented Control`, `Table` of open invoices |
| **Sales history** | Template **Filterable Table** | `Date Range Input`, `Power Search`, `Pagination` |
| **Sale detail** | Template **Order Detail** | `Table`, `Metadata List`, `Timestamp`, Return and Void buttons |
| **Return and void** | Template **Dialog Wizard** | `Table` with selection, `Text Area` for reason, approval step |
| **Suppliers** | Template **Searchable Table** + `Dialog` form | |
| **Purchase order create** | Template **Form Wizard** (supplier, items, review) | `Stepper`, `Typeahead`, `Table`, `Number Input` |
| **Purchase order detail and receive** | Template **Order Detail** | `Table` with per-line received qty, `Badge` for status |
| **Transfers** | Template **Inbox Table** or **Filterable Table** | `Table`, status `Badge`, `Dialog Wizard` to create, receive screen with variance |
| **Dashboard** | Template **Data Dashboard** (tiles, sparklines, period compare) | `Card`, `Skeleton`, `Date Range Input` |
| **Reports** | Template **Analytics Dashboard** or **Searchable Table** | `Table`, `Date Range Input`, `Selector`, export `Button` |
| **Audit log** | Template **Searchable Table** | `Table`, `Power Search`, `Code Block` for before and after |
| **Users and roles** | Template **Settings Panels** and **Searchable Table** | `Table`, `Checkbox Input` grid for permissions, `Dialog` |
| **Settings** | Template **Settings Panels** | `Switch`, `Text Input`, `Selector`, `Form Layout` |
| **Sync and conflicts** | Template **Grouped Table** | `Table`, `Banner`, `Button` for retry and resolve |
| **Label printing** | `Dialog` | `Number Input`, barcode preview (`jsbarcode`) |

## 3. States every screen must design

Use the same set on every screen so the app feels consistent. This follows the `ui-states` skill.

| State | Component |
| :--- | :--- |
| First use, no data | `Empty State` with one clear action |
| Loading | `Skeleton` for tables and cards, `Spinner` only inside buttons |
| Error | `Banner` with a retry action |
| Offline | Global `Banner` plus a `Status Dot`. Screens keep working. |
| Needs review (conflict) | `Badge` on the row and a count on the sync item in the nav |
| No permission | The item is hidden. A direct route shows an `Empty State` with the reason. |

## 4. Shared pieces to build once

These go in `src/renderer/src/components/` and are used by every feature.

- `MoneyText`: formats centavos for display. The only place money is formatted.
- `SyncStatus`: dot, label, and pending count.
- `PermissionGate`: hides children without a permission.
- `ApprovalDialog`: asks for a manager and PIN, returns an approval id. Used by discounts, voids, refunds, and credit overrides.
- `ProductPicker`: typeahead with barcode scan support.
- `ConfirmDialog`: one place for destructive confirmations.
- `DataTable` wrapper: columns, empty state, loading state, and pagination on top of Astryx `Table`.

## 5. Open UI items

- [ ] Choose the theme: follow the system, fixed dark, or a user toggle.
- [ ] Confirm that the POS screen works at the smallest register display (for example 1366 by 768) and with touch.
- [ ] Decide on charts. See D8 in [[AngieBarato v2 - Open Decisions]].
- [ ] Run the `wcag-accessibility-audit` skill on the POS and on the payment dialog before the pilot.
