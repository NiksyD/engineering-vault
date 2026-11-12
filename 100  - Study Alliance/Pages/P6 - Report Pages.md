---
tags: [alliance, mock-defense, pages]
---

# P6 · Report Pages

Index: [[P0 - Page Map and How to Read These]]

Controller: `ReportController` (class-level `[Authorize(Roles = "Admin,Officer")]`) · Service: `ReportService` · Views: `Report/Index.cshtml`, `Report/Event.cshtml`

---

## 1. Reports summary: `GET /Report/Index?organizationId=`
- **Action:** fills `ViewBag.Organizations` (`GetManagedOrganizationOptions`) for the filter and calls `GetEventSummaries(user, organizationId)`.
- **Service logic:** events in the user's managed organizations, **excluding drafts**, optionally filtered to one organization, newest first. Each row (`EventReportItemModel`) counts, in SQL:
  - `Registered` = registrations with status Registered;
  - `Present`, `Late`, `Absent` = registered students whose attendance has that status;
  - `AttendanceRate` = `(Present + Late) × 100 ÷ Registered` rounded to 1 decimal (0 if none registered).
- **View:** header with **Export CSV** → `Report/ExportSummary?organizationId=`; four stat tiles computed in the view (Events, Registrations, Attended, **Turnout %** = total attended ÷ total registered); an organization dropdown that auto-submits; a table (Event link → `Report/Event`, Date, Status badge, Registered, Present, Late, Absent, **Turnout bar**).
- **Note:** students with no attendance row yet count as neither Present, Late nor Absent, but they are in the *Registered* denominator, so a running event shows a lower turnout until check-in is finished or the event is Completed (which turns the rest into Absent).
- **Say it:** "Officers only see reports for their own organizations; the filter list and the data both come from the same managed-organization IDs."

## 2. One event report: `GET /Report/Event/{id}`
- Uses the **same** `GetAttendanceSheet` as the check-in desk (so the same scope check applies) but renders a read-only, print-friendly page.
- **View:** back link "All reports"; **Print** button (`window.print()`) and **Export CSV** → `Report/ExportEvent/{id}`; stat tiles (Status, Registered, Present, Late, Absent, Turnout = `(Present + Late) ÷ Attendees.Count`); the **attendance record** table (#, student + number, course · year, registered time, status, in, out, remarks) and the **waitlist** list if there is one.

## 3. CSV exports
| Endpoint | Content | Service |
|---|---|---|
| `GET /Report/ExportEvent/{id}` | one row per attendee: student number, name, course, year level, registration code, registered time, attendance ("Not yet recorded" if none), check-in, check-out, remarks. File name `attendance_{id}_{yyyyMMdd_HHmm}.csv` | `ExportEventCsv` (reuses `GetAttendanceSheet`, so scope is enforced) |
| `GET /Report/ExportSummary?organizationId=` | one row per event: event, organization, date, status, registered, present, late, absent, attendance rate %. File name `event_summary_{timestamp}.csv` | `ExportSummaryCsv` (reuses `GetEventSummaries`) |

- Both return `File(content, "text/csv", fileName)`. Written with **CsvHelper**, UTF-8 **with BOM** so Excel shows accented names correctly.
- They are `GET` (read-only, no state change), so no anti-forgery token is needed.
