---
tags: [alliance, mock-defense, code]
---

# 03 · Major Flows Code Walkthrough

Back to [[00 - Index]] · Previous: [[02 - Endpoint Map (GET and POST)]] · Next: [[04 - Data Model]]

For each flow: **where it is**, **what it does step by step**, and **the line you say out loud in the defense**.

---

## A. Check a student in (the core feature)

- Controller: `WebApp/Controllers/AttendanceController.cs` → `CheckIn(int eventId, string code)` (`[HttpPost]`, `[ValidateAntiForgeryToken]`, returns `Json(...)`)
- Service: `Services/Services/AttendanceService.cs` → `CheckIn(...)`
- Browser: `Views/Attendance/Index.cshtml` → `checkIn(code)`, `showResult(data)`, `updateRow(data)`, plus `Html5QrcodeScanner`

Service steps:
1. `FindEvent(eventId)` (throws `KeyNotFoundException` if missing).
2. `EnsureCanManageOrganization(ev.OrganizationId, currentUser)` → officer must belong to that organization.
3. `EnsureAttendanceAllowed(ev)` → only `Open` or `Closed` events.
4. `input = code.Trim()`, `code = input.ToUpperInvariant()`.
5. **One query** for a registration where `EventId == eventId && (RegistrationCode == code || Student.StudentNumber == input)`, with `Include(Student)` and `Include(Attendance)`.
6. No match → `Fail("Invalid registration code")`. Registration not `Registered` (cancelled/waitlisted) → "registration not active".
7. Already has `CheckInTime` → "already checked in", returns the **original** status/time. No double check-in.
8. **Late rule:** `now > ev.StartTime.AddMinutes(ev.LateAfterMinutes)` → `Late`, else `Present`.
9. No attendance row → `AddAttendance`; existing row (e.g. earlier marked Absent) → update it. `RecordedBy` stores the officer.
10. Returns `CheckInResultModel { Success, Message, StudentName, StudentNumber, Status, Time, RegistrationId }`.

Browser side:
- `html5-qrcode` opens the camera (10 fps, 220×220 box) and calls `checkIn(decodedText)`.
- The scanner fires many times a second, so `checkIn` ignores the **same code within 3 seconds** and ignores calls while a request is `busy`.
- Posts form data (including the anti-forgery token) with `fetch`, header `X-Requested-With: XMLHttpRequest`.
- Result card turns green (`ok`) or red (`fail`); the attendee row's status tag and the Present/Late/Pending counters update **without reloading**.

**Say it:** "A code from another event can't be used because the query filters `r.EventId == eventId`. JSON is returned instead of a page so the officer can scan the next student immediately."

---

## B. Register for an event with automatic waitlist

- Controller: `RegistrationController.Register(int eventId)` (`[Authorize(Roles = Student)]`, POST, CSRF)
- Service: `RegistrationService.Register(eventId, currentUser)`

Steps:
1. Load the event where `Status != Draft`, otherwise `KeyNotFoundException`.
2. Registration is allowed only if `Status == Open` **and** `now <= RegistrationDeadline` **and** `now < StartTime`; otherwise `InvalidDataException(RegistrationClosed)`.
3. Count current `Registered` seats. `Capacity > 0 && registered >= Capacity` → status **Waitlisted**; else **Registered**. `Capacity == 0` means unlimited.
4. Find an existing row for (event, student):
   - active (Registered/Waitlisted) → "already registered";
   - `Cancelled` → **reuse the row** (reset status/time, clear `CancelledTime`) because the DB allows one row per student per event (unique index `EventId + StudentId`).
5. Otherwise insert a new registration with `GenerateUniqueCode()`.
6. Controller shows a **warning** toast if waitlisted, a **success** toast if registered, and redirects to the event page (Post-Redirect-Get).

`GenerateUniqueCode()`: 10 characters from `ABCDEFGHJKLMNPQRSTUVWXYZ23456789` (no `0/O/1/I`, easy to read aloud), generated with `RandomNumberGenerator` (cryptographically secure), re-rolled until no collision.

**Say it:** "Waitlist order is fair because `RegisteredTime` is stored and promotion takes the oldest first."
**Known limitation:** counting and saving are separate steps, so two students clicking for the very last seat at the same instant could both get in. Fix: a DB transaction with a row lock or serializable isolation.

---

## C. Cancel and waitlist promotion

- `RegistrationService.Cancel(registrationId, currentUser)`:
  1. Load the registration via `RegistrationProjection`.
  2. `EnsureOwnerOrManager` → the student who owns it, or an Admin/Officer who manages the event's organization.
  3. `registration.CanCancel` must be true (`RegistrationViewModel`): not already cancelled, **no attendance recorded**, event is `Open` or `Closed`, and `now < StartTime` (no cancelling once the event has started).
  4. Set `Status = Cancelled`, `CancelledTime = now`, save.
  5. If it **was `Registered`**, call `PromoteWaitlisted(eventId)`.
- `PromoteWaitlisted(eventId)`: only for `Open`/`Closed` events; takes waitlisted rows ordered by `RegisteredTime`; `freeSlots = Capacity - registeredCount` (or everyone if unlimited); flips the first `freeSlots` to `Registered`.
- It is also called from `EventService.UpdateEvent`, so **raising capacity** promotes waitlisted students automatically.

---

## D. Event lifecycle

- `EventService.ChangeStatus(id, status, user)` and the static `AllowedTransitions` dictionary:

```
Draft     → Open, Cancelled
Open      → Closed, Completed, Cancelled
Closed    → Open, Completed, Cancelled
Completed → (none)
Cancelled → (none)
```

- Invalid jump → `InvalidDataException(InvalidStatusChange)`. The UI offers only `GetAllowedStatusChanges(current)`, so the server is the real guard and the UI is a convenience.
- On `Completed` → `AttendanceService.MarkAbsentees(eventId, actor)` bulk-inserts `Absent` attendance for every `Registered` student with **no** attendance row (`AddAttendances` is one batch).
- `CreateEvent`: always starts as **Draft**; sets `CreatedBy/UpdatedBy`; needs `EnsureCanManageOrganization(model.OrganizationId)`.
- `UpdateEvent`: checks scope for both the old and the new organization (stops moving an event into an org you don't manage); rejects `Capacity` below the registered count; AutoMapper ignores `Status`, so edits can never change the status.
- `DeleteEvent`: refused if **any** registration exists (`EventHasRegistrations`).
- `EventViewModel.Validate`: `EndTime > StartTime` and `RegistrationDeadline <= StartTime`.
- Students never see drafts: `GetPublishedEvents` filters them, `GetEvent` returns "not found" for a draft to anyone who can't manage it.

---

## E. Attendance override and check-out

- `SetStatus(registrationId, status, remarks, user)`: allowed unless the event is Draft/Cancelled; registration must be `Registered`. Setting **Absent** clears check-in/out times; setting Present/Late with no check-in time stamps `now`. `Remarks` is trimmed and saved.
- `CheckOut(registrationId, user)`: requires an existing `CheckInTime` (else `NotCheckedIn`); stores `CheckOutTime`.

---

## F. Sign-in and sessions

See [[01 - System Flow and Architecture#5. Authentication and authorization]].
Code: `AccountController.Login` → `UserService.AuthenticateUser` → `SignInManager.SignInAsync` → `CustomJwtDataFormat.Protect` → cookie.
`AuthenticateUser` order of checks: wrong credentials → `Failed`; `!IsApproved` → `Pending`; `!IsActive` → `Inactive`; else `Success`. A deliberately generic "invalid login" message is shown for wrong username *or* password (no user enumeration).

---

## G. Self-registration and admin approval

- `AccountController.Register` (POST) → model validation (`UserViewModel`): username regex (4–50 chars, letters/digits/`.`/`_`/`-`), required names/email/student number/course/year, **password policy** (8+, upper, lower, digit, special: `Const.PasswordPattern`), confirm-password match, course must be in the `Courses` list.
- `UserService.AddUser`: duplicate username → `UserExists`; duplicate student number → `StudentNumberExists`; forces **`Role = Student`**, `IsActive = true`, **`IsApproved = false`**; encrypts password.
- Because role is set server-side, a user can't self-register as an Admin by tampering with the form.
- Admin: `User/Approvals` → `Approve(ids)` / `ApproveAll` / `Reject(ids)`. Approve sets `IsApproved`, `ApprovedBy`, `ApprovedTime`. Reject **deletes** only unapproved rows.

---

## H. Reports and CSV

- `ReportService.GetEventSummaries(user, organizationId?)`: limited to `GetManagedOrganizationIds(user)` and non-draft events; computes Registered/Present/Late/Absent counts **inside the SQL query** (`e.Registrations.Count(...)`).
- `ExportEventCsv` reuses `GetAttendanceSheet` (so the same scope check applies) and `WriteCsv<T>` (CsvHelper, UTF-8 **with BOM** so Excel reads accents).
- `GetDashboard` builds three shapes: Student (my upcoming, attended count, open events), Officer/Admin (org count, student count, active events, total registrations, overall attendance rate = attended ÷ recorded, upcoming events; Admin also pending approvals).

---

## I. Organization scope (the officer rule)

`AccessService`:
- `CanManageOrganization(orgId, user)`: Admin → true; Officer → exists `OrganizationMember(OrganizationId, MemberId == user.AccountId)`; Student → false.
- `GetManagedOrganizationIds(user)`: Admin → all; Officer → their memberships; Student → empty list.
- Used by `EventService`, `AttendanceService`, `RegistrationService` (for managers acting on others' registrations) and `ReportService`.

**Say it:** "Roles say *what kind* of user you are; organization membership says *which data* you can touch. The second check lives in the service so no controller can forget it."

---

## J. Passwords and QR

- `PasswordManager.EncryptPassword`: AES with a 16-byte key taken from the first 16 bytes of `TokenAuthentication:SecretKey`, an all-zero IV, output Base64. Login encrypts the typed password and compares. It is **reversible encryption, not hashing** (see the review note).
- `QrCodeManager.GenerateSvg(content, size=240)`: ZXing writes an inline **SVG** (no `System.Drawing` dependency). The QR content is just the 10-character `RegistrationCode`; the ticket shows it only when the registration is `Registered`.
