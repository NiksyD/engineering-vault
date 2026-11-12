---
tags: [alliance, mock-defense, pages]
---

# P2 · Home Pages

Index: [[P0 - Page Map and How to Read These]]

Controller: `HomeController` · Service: `ReportService.GetDashboard` · View: `Views/Home/Index.cshtml` · Model: `DashboardModel`

---

## 1. Dashboard: `GET /Home/Index`
- **Who:** any signed-in user. After login everyone lands here.
- **Action:** `_reportService.GetDashboard(CurrentUser, UserName)` → one `DashboardModel`; the **view branches on `Model.Role`**.

### A. Student dashboard
**Service logic** (`Role.Student` branch):
| Field | Query |
|---|---|
| `MyUpcoming` | my registrations where status ≠ Cancelled, `Event.EndTime >= now`, event ≠ Cancelled, ordered by start (projected to `RegistrationViewModel`) |
| `MyUpcomingCount` | count of `MyUpcoming` |
| `MyAttendedCount` | my registrations that have an attendance row whose status ≠ Absent (Present or Late) |
| `OpenEventCount` | events `Status == Open`, `RegistrationDeadline >= now`, `StartTime > now` |
| `UpcomingEvents` | the same open events, ordered by start, projected with my registration info |

**View sections:**
1. **Header:** "Hi, {first name}" and today's date. (No "New event" button for students.)
2. **Your next pass:** the first upcoming registration with status *Registered* shown as a pass card with date/time/venue, a **Show pass at the door** button → `Registration/Ticket/{id}` and the registration code. If none: empty-state "No pass yet".
3. **Your registrations:** summary line (`n upcoming · n attended · n open for registration`), link **All passes** → `Registration/MyEvents`, and a table (5 per page) with event link → `Event/Details`, when, a status badge (Registered/Waitlisted) and a **Pass** button (only if Registered).
4. **Open for registration:** `_PassRack` cards (6 per page) of open events, link **Browse all events** → `Event/Index`.

### B. Officer / Admin dashboard
**Service logic:**
- `organizationIds = GetManagedOrganizationIds(user)` (Admin: all; Officer: their memberships).
- `OrganizationCount`, `PendingApprovals` (Admin only), `StudentCount` (Admin: active approved students; Officer: distinct members of their organizations), `ActiveEventCount` (Open or Closed), `TotalRegistrations` (Registered status), `OverallAttendanceRate` = attended ÷ recorded, rounded to 1 decimal where *recorded* = registrations that have an attendance row and *attended* = those not Absent.
- `UpcomingEvents`: events of managed organizations with `EndTime >= now`, not Cancelled, not Completed, ordered by start; all flagged `CanManage`.

**View sections:**
1. **Header:** "Hi, {name}" and a **New event** button → `Event/Create`.
2. **Pending approvals notice (Admin, if > 0):** "n new accounts waiting" with a link → `User/Approvals`.
3. **"Door" card:** the first upcoming event that is **Open or Closed**: org, registration state badge, title (→ `Event/Details`), counts (doors open time, registered/capacity, checked in, not yet in) and buttons **Open the check-in desk** → `Attendance/Index?eventId=` and **Event details**. If none: "No door to run yet".
4. **Coming up:** table (5 per page): title, org · venue, when, registered/capacity, status badge, **Check in** button when Open/Closed. Link **All your events** → `Event/Manage`.

**Rules / edge cases**
- An officer with no organization membership sees zeros and empty states (and can't create events: [[P3 - Event Pages]] form notice).
- `OverallAttendanceRate` is *attended ÷ recorded*, while the report pages use *(present + late) ÷ registered*. Both are correct for their definition but give **different percentages** when some students have no attendance row yet. Know which is which if asked.

**Say it:** "One controller action and one service method serve three dashboards; the model carries the role and the view picks the layout. All numbers are computed in SQL."

---

## 2. Error page: `GET /Home/Error`
- `[AllowAnonymous]`; reached through `UseExceptionHandler("/Home/Error")` outside Development. Logs the original exception (`IExceptionHandlerPathFeature`), sets HTTP 500, shows `Error.cshtml` with a request ID.

## 3. Status page: `GET /Home/Status?code=404`
- `[AllowAnonymous]`; reached through `UseStatusCodePagesWithReExecute`. Sets the response status to `code` and shows a friendly "page not found" style page (`Status.cshtml`). This is why a mistyped URL doesn't show a raw browser error.
