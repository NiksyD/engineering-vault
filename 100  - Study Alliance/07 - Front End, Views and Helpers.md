---
tags: [alliance, mock-defense, frontend]
---

# 07 · Front End, Views and Helpers

Back to [[00 - Index]] · Related: [[03 - Major Flows Code Walkthrough]]

The earlier notes cover the server side. This one covers the Razor views, the JavaScript, and the small helpers the PDF calls "minor functions". Panelists often ask "how does the page know X?"

## 1. Views map (`ASI.Basecode.WebApp/Views`)

| Folder | View | Used by | Notes |
|---|---|---|---|
| Account | `Login`, `Register`, `AccessDenied` | `AccountController` | Use `_AuthLayout`. Register has the live required-field markers and the password checklist. |
| Home | `Index` (dashboard, 173 lines), `Status` (404/other) | `HomeController` | `Index` renders a different layout per role from `DashboardModel`. |
| Event | `Index` (browse), `Details`, `Manage`, `Form` (create + edit share one form) | `EventController` | `Details` shows different panels: student "Your pass" (register / waitlisted / cancel / show pass) vs manager panel (check-in desk, report, edit, status buttons). |
| Registration | `MyEvents`, `Ticket` | `RegistrationController` | `Ticket` shows the QR SVG and a **Print pass** button (`window.print()`, `no-print` class hides the chrome). |
| Attendance | `Index` (258 lines, scanner + table) | `AttendanceController` | The only view with substantial page script (see [[03 - Major Flows Code Walkthrough]] flow A). |
| Report | `Index`, `Event` | `ReportController` | Print-friendly tables + CSV links. |
| Organization | `Index`, `Form`, `Members` | `OrganizationController` | Admin only. |
| User | `Index`, `Form`, `Approvals` | `UserController` | Admin only. |
| Shared | `_Layout`, `_AuthLayout`, `_Scripts`, `_PassRack`, `_Lanyard`, `_Mark`, `_Empty`, `Error`, `Components/AccountSwitcher/Default` | everywhere | Partial views and layout pieces. |

`_ViewStart.cshtml` sets the default layout; `_ViewImports.cshtml` enables tag helpers.

## 2. Role-aware UI (`_Layout.cshtml`)
Lines 8–10 compute `isAdmin`, `isManager` (Admin or Officer) and `isStudent` from `User.IsInRole(...)` and show only the matching navigation (students: events, my passes; managers: manage events, reports; admin: also organizations, users, approvals). **The menu is only a convenience. The real protection is the server-side `[Authorize]` and service checks**, so typing a hidden URL still gets refused.

## 3. Shared pieces
- **`_Scripts.cshtml`:** loads jQuery, validation and toastr, then reads `TempData["SuccessMessage"]`, `["WarningMessage"]` and `["ErrorMessage"]` (serialized with `Json.Serialize`, so quotes can't break out of the script) and shows toasts. This is how every `NotifySuccess(...)` becomes a popup.
- **`_PassRack.cshtml`:** the card layout for event "passes" (events list, dashboards). Cards use `data-` attributes the pager reads.
- **`BadgeHelper` (`WebApp/Helpers`):** `Badge(status)` renders `<span class="tag tag-{status}">` (CSS colors per status such as Present, Late, Open, Waitlisted), HTML-encoded. `Initials("Ana Cruz")` → `"AC"` for the avatar slot. A null/empty status shows "Pending".
- **`AccountSwitcherViewComponent`:** renders the dev-only account switcher; returns empty content unless `IsDevelopment()`.

## 4. JavaScript (`wwwroot/js/site.js`, 240 lines)
| Feature | How it's triggered | What it does |
|---|---|---|
| **Confirm before destructive actions** | `<form data-confirm="Are you sure?">` | A single `submit` listener calls `window.confirm`; cancel stops the submit. Used on Cancel registration, Delete, Change status. |
| **Menu closers** | click listeners | Close the mobile account menu and the dev switcher when you tap outside. |
| **Pagination for every table and card rack** | automatic; `data-page-size` (tables 10, racks 9) | Client-side paging with page numbers (`1 … 4 5 6 … 12`), page-size menu (10/25/50 for tables). Rows hidden by a filter carry `data-filtered-out`; `el.pager.render()` re-renders and fires a `pager:render` event. |
| **Required-field markers** | `<form data-live-required>` | Adds a red `*` to labels of every `data-val-required` field and updates as fields are filled. |
| **Password checklist** | `<input data-password-rules>` | Live checklist for the 8+ chars / upper / lower / digit / special rule. Mirrors server `Const.PasswordPattern`. |

Important point: **client-side validation is a convenience; the server re-validates everything** (`ModelState`, `IValidatableObject`, service rules).

Pagination is purely client-side: the server sends the whole list. Fine for a campus app; for big data you'd page in SQL.

## 5. Attendance page script (recap)
`checkIn`, `showResult`, `updateRow`, `Html5QrcodeScanner` setup, and a `MutationObserver` that relabels the library's buttons. Details in [[03 - Major Flows Code Walkthrough]] (flow A).

## 6. Small server helpers (the PDF's "minor functions")
| Helper | Where | What it does |
|---|---|---|
| `CurrentUser` | `Mvc/ControllerBase.cs` | Builds `CurrentUserModel` from claims (`AccountId`, `UserId`, `Role`). |
| `FindEvent`, `FindUser`, `FindOrganization`, `FindMembership`, `FindRegistration` | services | Load or throw `KeyNotFoundException` (becomes "not found" message). |
| `EnsureAttendanceAllowed` | `AttendanceService` | Only Open/Closed events allow attendance. |
| `Fail(message)` | `AttendanceService` | Builds a failed `CheckInResultModel`. |
| `EventProjection.ToViewModel(accountId)` / `RegistrationProjection.ToViewModel` | `Services/Services` | Shared SQL projections (counts, "my registration"). |
| Computed props | view models | `EventViewModel.SlotsLeft`, `IsUnlimited`, `IsRegistrationOpen`; `RegistrationViewModel.CanCancel` (not cancelled, no attendance, Open/Closed event, before start); `EventReportItemModel.AttendanceRate`. |
| `GetManagedOrganizationOptions`, `LoadOrganizations` | `OrganizationService`, `EventController` | Dropdown of organizations the user may manage. |
| `GetActiveUser` | `UserService` | User must be active **and** approved (used by the dev switcher). |
| `Courses.All` / `IsValid` | `Resources/Constants/Courses.cs` | Fixed list of 17 programs (BS Computer Science, BS Nursing, …) used by the dropdown and validated server-side (`UserViewModel.Validate`). |
| `Const.PasswordPattern`, `UsernamePattern` | `Resources/Constants/Const.cs` | One regex shared by server and client validation. |
| `Messages/*.resx` | `Resources/Messages` | All user-facing text (`Errors`, `Common`, `Screen`) so wording changes in one place. |
| `SessionManager` | `Services/Manager` | Thin wrapper over the session (`Clear` on the login page). Session only stores display values. |
| `HandleExceptionLog` | `ControllerBase` | Writes a formatted error log (controller, action, request, stack trace). Used by `Register` for unexpected errors. |
| Logging | `Startup.Logger.cs` | File + console logging; level from `appsettings.json`. |

## 7. Security details specific to the views
- Razor encodes output by default (`@Model.Title` is HTML-encoded); `BadgeHelper` encodes manually with `WebUtility.HtmlEncode`. The one `Html.Raw` I saw is for toast messages passed through `Json.Serialize`.
- Forms use tag helpers (`asp-controller`, `asp-action`, `method="post"`), which add the anti-forgery token automatically, even on Login/Register (the server just doesn't validate it there; see [[05 - Code Review - Strengths, Risks, Limitations]] item 3).
- The ticket QR contains only the registration code, never personal data.

## 8. Database script (`Database/student_event_db.sql`, 415 lines)
- Creates `student_event_db`, the six tables and their unique indexes, then seeds organizations, members, events at different lifecycle stages, registrations (including waitlisted/cancelled) and some attendance, so every screen has data.
- Re-running resets everything to demo data.
- `build_hosted_script.ps1` produces the hosted version with a fresh secret key (details in [[04 - Data Model]]).

## Still not covered in these notes (read these yourself if you have time)
- Exact CSS (`wwwroot/css/pass.css`) and the design rationale: `DESIGN.md` (19 KB) and `PRODUCT.md` in the repo root explain the visual system and users. Read `PRODUCT.md` (short): it states the product principles panelists may quote ("the door is the hardest moment").
- The full text of every view and the remaining PDF pages (pagination internals, 4.9–4.14) if you want line-by-line detail.
