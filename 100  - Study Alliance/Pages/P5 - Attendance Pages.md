---
tags: [alliance, mock-defense, pages]
---

# P5 · Attendance Pages (the check-in desk)

Index: [[P0 - Page Map and How to Read These]] · Theory + code: [[03 - Major Flows Code Walkthrough#A. Check a student in (the core feature)]]

Controller: `AttendanceController` (class-level `[Authorize(Roles = "Admin,Officer")]`) · Service: `AttendanceService` · View: `Views/Attendance/Index.cshtml` · Model: `AttendanceSheetModel`

---

## 1. Check-in desk: `GET /Attendance/Index?eventId=`
- **Service `GetAttendanceSheet(eventId, user)`:**
  1. load the event (projection) → `KeyNotFoundException` if missing;
  2. `EnsureCanManageOrganization` (officer outside the organization → 403);
  3. load registrations that are **not cancelled**, ordered by student name;
  4. **Attendees** = status Registered; **Waitlist** = status Waitlisted ordered by `RegisteredTime`;
  5. counters: Present, Late, Absent, **Pending** (attendance row missing).
- **View, top:** back link to the event, title "Check-in desk", organization · start · venue, and shortcut buttons **Report** → `Report/Event` and **CSV** → `Report/ExportEvent`.
- **Scan panel** (only when the event is **Open or Closed**, `canCheckIn`): the camera area (`html5-qrcode`), a typed entry form ("code or student no.", `autocapitalize=characters`, placeholder like `TT4K9QZP2A`) with a **Check in** button, and a **result "punch card"** that turns green or red. For other statuses the panel and scanner script are not rendered, and a notice says scanning is only available while Open or Closed but individual records can still be corrected.
- **Counters** (Registered, Present, Late, Not yet in) have ids `count-present`, `count-late`, `count-pending` so the script can update them live.
- **Attendees table:** filter box (client-side, name / number / code), columns Student (name, number · course), Code, Status badge, In/out times, and per-row **Record** controls:
  - a **status dropdown + remarks + Save** form → `POST Attendance/SetStatus`;
  - **Check out** button (only if checked in and not yet checked out, and the event is Open/Closed) → `POST Attendance/CheckOut`.
- **Waitlist panel** (if any): numbered list "name (number) · since time".

## 2. Check in: `POST /Attendance/CheckIn` (`eventId`, `code`) → **JSON**
- Called by `fetch` (not a form submit). Returns `CheckInResultModel { success, message, studentName, studentNumber, status, time, registrationId }`.
- **Order of checks:** event exists → officer scope → event Open/Closed → find registration by **code or student number within this event** → Registered? → already checked in? → compute Present/Late → insert or update attendance → return.
- **Browser side:**
  - scanner or typed entry → `checkIn(code)`; ignores empty, ignores while a request is in flight, ignores the same code within 3 s;
  - `showResult`: name, number, message + `Status · time`, card class `ok`/`fail`, punch animation;
  - `updateRow`: finds `tr[data-registration-id]`, swaps the status badge, writes the time, sets the dropdown to the new status, flashes the row, and bumps counters (+1 Present or Late, −1 Pending);
  - network failure → red "Couldn't reach the server" card; `finally` clears the field and refocuses it so the next student can be typed immediately.
- **Messages the officer can see:** success; "invalid registration code" (also for another event's code); "registration not active" (cancelled or waitlisted); "already checked in" (shows the original status and time); "attendance not allowed" (event is Draft/Completed/Cancelled → returned as JSON error 400 by the filter).
- **Why JSON:** the officer must scan the next student immediately; a full page reload would break the queue flow.

## 3. Check out: `POST /Attendance/CheckOut` (`id` = registration id, `eventId`)
- Service: find registration (with event and attendance) → scope check → event must be Open/Closed → **requires a check-in time** (`NotCheckedIn` otherwise) → sets `CheckOutTime`, `RecordedBy`, `RecordedTime`.
- Controller: success toast, redirect back to the desk. (Normal form post, so the page reloads.)

## 4. Override status: `POST /Attendance/SetStatus` (`id`, `eventId`, `status`, `remarks`)
- **Purpose:** corrections: marking someone Present who lost their pass, Late/Absent overrides, adding **remarks**.
- Rules: scope check; allowed for any event **except Draft and Cancelled** (so officers can still fix records after Completed); the registration must be **Registered**.
- Behavior:
  - no attendance row → creates one (check-in time = now unless status is Absent);
  - existing row → sets status and remarks (trimmed); **Absent clears check-in and check-out times**; Present/Late with no check-in time stamps now;
  - always records who (`RecordedBy`) and when.
- Redirects to the desk with a success toast.

## Defense points for this page
- "Scope is enforced in the service: an officer of Org A gets 403 on Org B's desk even with the right URL."
- "At most one attendance per registration, enforced by a unique index, so a duplicate scan can't create two records."
- "Typing the student number is a deliberate fallback when the camera or the student's phone fails; every record stores which officer entered it."
- "The camera needs HTTPS or localhost; the typed entry always works."
- **Known gap:** the late rule uses `DateTime.Now` on the server, so the server clock/time zone must match the venue ([[05 - Code Review - Strengths, Risks, Limitations]] item 12).
