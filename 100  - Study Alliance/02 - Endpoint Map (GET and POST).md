---
tags: [alliance, mock-defense, endpoints]
---

# 02 · Endpoint Map (GET and POST)

Back to [[00 - Index]] · Previous: [[01 - System Flow and Architecture]] · Next: [[03 - Major Flows Code Walkthrough]]

**Routing:** conventional route `{controller=Account}/{action=Login}/{id?}`, so `GET /Event/Details/5` binds `id=5`; other parameters come from the query string or form (e.g. `/Attendance/Index?eventId=5`).
**Every action requires login** (global filter) unless marked *Anonymous*. "Managers" = Admin + Officer. "Scope" = the service also checks officer membership in the event's organization.
**Every state-changing POST has `[ValidateAntiForgeryToken]`**, except Login and Register (see [[05 - Code Review - Strengths, Risks, Limitations]]).

Source: `ASI.Basecode.WebApp/Controllers/*.cs`

## AccountController (sign-in, registration)

| Verb | URL | Access | Does | Calls |
|---|---|---|---|---|
| GET | `/Account/Login` | Anonymous | Show login page, clear session, store returnUrl | `SessionManager.Clear` |
| POST | `/Account/Login` | Anonymous | Authenticate; sign in; redirect to returnUrl or Home | `UserService.AuthenticateUser`, `SignInManager.SignInAsync` |
| GET | `/Account/Register` | Anonymous | Student self-registration form | — |
| POST | `/Account/Register` | Anonymous | Create Student, `IsApproved=false`, redirect to login with "pending approval" | `UserService.AddUser` |
| GET | `/Account/AccessDenied` | Any signed-in | "You can't open this page" | — |
| POST | `/Account/SwitchAccount` | Anonymous + CSRF | **Development only** (404 otherwise): sign in as any active user | `UserService.GetActiveUser` |
| GET | `/Account/SignOutUser` | Anonymous | Sign out, back to login | `SignInManager.SignOutAsync` |

## HomeController

| Verb | URL | Access | Does |
|---|---|---|---|
| GET | `/Home/Index` | Any signed-in | Role-specific dashboard → `ReportService.GetDashboard` |
| GET | `/Home/Error` | Anonymous | Friendly 500 page; logs the exception |
| GET | `/Home/Status?code=404` | Anonymous | Friendly 404/other status page |

## EventController

| Verb | URL | Access | Does | Service method |
|---|---|---|---|---|
| GET | `/Event/Index?search=&showPast=` | Any signed-in | Browse published events (upcoming by default) | `GetPublishedEvents` |
| GET | `/Event/Details/{id}` | Any signed-in | Event page; drafts hidden unless you manage the org | `GetEvent` |
| GET | `/Event/Manage?search=&status=` | Managers | Events of orgs you manage | `GetManagedEvents` |
| GET | `/Event/Create` | Managers | Blank form | `GetManagedOrganizationOptions` |
| POST | `/Event/Create` | Managers + CSRF + Scope | Create as **Draft** | `CreateEvent` |
| GET | `/Event/Edit/{id}` | Managers + Scope | Prefilled form | `GetEvent` |
| POST | `/Event/Edit` | Managers + CSRF + Scope | Update; blocks capacity below registered count; promotes waitlist | `UpdateEvent` |
| POST | `/Event/Delete/{id}` | Managers + CSRF + Scope | Delete only if no registrations | `DeleteEvent` |
| POST | `/Event/ChangeStatus` (`id`, `status`) | Managers + CSRF + Scope | Lifecycle transition; `Completed` marks absentees | `ChangeStatus` |

## RegistrationController

| Verb | URL | Access | Does | Service method |
|---|---|---|---|---|
| GET | `/Registration/MyEvents` | **Student** | My registrations/passes/history | `GetMyRegistrations` |
| POST | `/Registration/Register` (`eventId`) | **Student** + CSRF | Register or auto-waitlist | `Register` |
| POST | `/Registration/Cancel` (`id`, `returnUrl`) | Signed-in + CSRF; owner or org manager | Cancel; promote waitlist | `Cancel` |
| GET | `/Registration/Ticket/{id}` | Signed-in; owner or org manager | Printable ticket with QR (only when Registered) | `GetTicket` |

## AttendanceController (class-level `[Authorize(Roles="Admin,Officer")]`)

| Verb | URL | Does | Service method |
|---|---|---|---|
| GET | `/Attendance/Index?eventId=` | Check-in desk: scanner, counters, attendee + waitlist tables | `GetAttendanceSheet` |
| POST | `/Attendance/CheckIn` (`eventId`, `code`) | **Returns JSON** (AJAX). Code or student number → Present/Late | `CheckIn` |
| POST | `/Attendance/CheckOut` (`id`, `eventId`) | Record check-out time | `CheckOut` |
| POST | `/Attendance/SetStatus` (`id`, `eventId`, `status`, `remarks`) | Manual override Present/Late/Absent with remarks | `SetStatus` |

All four enforce organization scope in the service.

## ReportController (class-level `Admin,Officer`)

| Verb | URL | Does | Service method |
|---|---|---|---|
| GET | `/Report/Index?organizationId=` | Summary table per event (registered/present/late/absent/rate) | `GetEventSummaries` |
| GET | `/Report/Event/{id}` | Single event attendance sheet | `GetAttendanceSheet` |
| GET | `/Report/ExportEvent/{id}` | **CSV download** of one event | `ExportEventCsv` |
| GET | `/Report/ExportSummary?organizationId=` | **CSV download** of the summary | `ExportSummaryCsv` |

## OrganizationController (class-level `Admin` only)

| Verb | URL | Does |
|---|---|---|
| GET | `/Organization/Index?search=` | List with member/event counts |
| GET / POST | `/Organization/Create` | Create (unique name) |
| GET / POST | `/Organization/Edit/{id}` | Edit |
| POST | `/Organization/Delete/{id}` | Delete only if it has no events |
| GET | `/Organization/Members/{id}` | Members + users available to add |
| POST | `/Organization/AddMember` (`organizationId`, `memberId`, `position`) | Add member (this is what grants an officer scope) |
| POST | `/Organization/UpdateMember` (`id`, `organizationId`, `position`) | Change position |
| POST | `/Organization/RemoveMember` (`id`) | Remove member |

## UserController (class-level `Admin` only)

| Verb | URL | Does |
|---|---|---|
| GET | `/User/Index?search=&role=` | Users list with search and role filter |
| GET | `/User/Approvals` | Pending self-registrations |
| POST | `/User/Approve` (`ids[]`) | Approve selected |
| POST | `/User/ApproveAll` | Approve all pending |
| POST | `/User/Reject` (`ids[]`) | **Delete** pending requests (approved users are never deleted here) |
| GET / POST | `/User/Create` | Admin creates a user (auto-approved) |
| GET / POST | `/User/Edit/{id}` | Edit; blank password keeps the current one |
| POST | `/User/ToggleActive/{id}` | Deactivate/reactivate; cannot target yourself |

## Counts to remember
- 8 controllers, about 50 actions.
- Only **one** endpoint returns JSON: `POST /Attendance/CheckIn`.
- Only **two** return files: `GET /Report/ExportEvent` and `/Report/ExportSummary` (CSV).
- Everything else returns a Razor view or a redirect (Post-Redirect-Get).
- Public (no login): Login (GET/POST), Register (GET/POST), SignOutUser, Error, Status, SwitchAccount (dev only).
