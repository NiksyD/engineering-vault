---
tags: [alliance, mock-defense, demo, student-side]
---

# 08 · Niko's Part: Student Side Demo Trace

Back to [[00 - Index]]

**Script:** login with the newly approved account → browse events (show the course restriction example) → register on a live event (explain overlap prevention and auto-waitlist) → My Events → QR ticket.

> Based on the repo **after pulling main** (commits `0660d91` course eligibility, `3dfb544` schedule conflicts, plus a registration transaction). Notes 01–07 and P1–P8 were written before this pull, so where they differ (for example "known limitation: race on the last seat", or "no course restriction"), **this note is correct**.

Files are under `ASIBasecodeCsharp/`.

## Before the demo (setup checklist)
1. Register a new student at `/Account/Register`. Log in once to show the **pending approval** message.
2. Sign in as `admin` → `User/Approvals` → approve that student.
3. Pick a student whose course is **NOT** in the restricted event's list (seed data: event 3, the Hackathon, allows only BS Computer Science (AI-Focused Elective), BS Information Technology, BS IT - Software Engineering, BS Computer Engineering; event 4 allows only BS Computer Engineering). Use that student to show the restriction.
4. Have two **Open** events with overlapping times, and one Open event that is **full** (capacity reached) to show the waitlist. Check start times are in the future and the deadline hasn't passed.

## Step 1: Login with the approved account
- `WebApp/Controllers/AccountController.cs` → `Login` (POST) → `Services/Services/UserService.cs` → `AuthenticateUser`.
- Order: password match → `IsApproved` (else Pending) → `IsActive` (else Inactive) → success. Then `SignInManager.SignInAsync` (claims in a JWT cookie) → redirect to `Home/Index`.
- **Say:** "Self-registered accounts start with `IsApproved = false`. They can't sign in until an admin approves."

## Step 2: Browse events + course restriction
- `EventController.Index` → `EventService.GetPublishedEvents(user, search, upcomingOnly)`:
  - drafts excluded, **events of deactivated organizations hidden from students**, upcoming only by default;
  - `ViewerCourse(currentUser)` reads **the student's course from the database** and passes it to `EventProjection.ToViewModel(accountId, viewerCourse)`, so each card knows whether *this student* is eligible.
- View `Shared/_PassRack.cshtml`: each card shows **"For {EligibilityText}"** (e.g. "College of Computer Studies, BS Computer Engineering" or "All students"). If registration is open but the student is not eligible, the footer says **"Not open to your course"**.
- Data: table `event_allowed_courses (event_id, course)`, unique per pair. **No rows = open to all students.** Model: `Data/Models/Event.cs` `AllowedCourses`; the officer sets it on the event form (`RestrictToCourses` + `AllowedCourses` in `EventViewModel`; `EventService.AllowedCoursesOf`).
- Open the restricted event → `Views/Event/Details.cshtml`: "This event is only open to students of: … Your course isn't on the list", and the **Register button is disabled**.
- **The real enforcement is on the server**, not the disabled button: `RegistrationService.EnsureCourseAllowed` loads the allowed courses; if the list is non-empty and the student's course (read from the DB, never from the form) isn't in it → `InvalidDataException(NotEligibleForEvent)`.
- **Say:** "The button is disabled for convenience; the service enforces it, so a forged POST is still refused."
- Rule to remember: **changing the allowed list later doesn't remove already-registered students**; only new registrations are checked (comment in `EventService.UpdateEvent`).

## Step 3: Register on a live event
Live = status **Open**, before the registration deadline, before the start time.

1. Click **Register** on `Event/Details` → `POST /Registration/Register` (`RegistrationController.Register`; Student role only; CSRF token).
2. `RegistrationService.Register(eventId, user)`:
   - **Transaction + row lock:** `BEGIN TRANSACTION` (ReadCommitted), then `SELECT id FROM events WITH (UPDLOCK, HOLDLOCK) WHERE id = @eventId`. Two students registering for the same event are processed **one after the other**, so the last seat can't be double-booked. On a deadlock/timeout/duplicate double-click it clears the tracker and throws `RegistrationBusy` (friendly message).
   - then `RegisterLocked`, whose steps are numbered in the code comments:

| Step | Check | Failure |
|---|---|---|
| 1 | event exists and isn't Draft | not found |
| 2 | organization is active | `OrganizationInactive` |
| 3 | status Open, `now <= RegistrationDeadline`, `now < StartTime` (`AppClock.Now` = **Philippine time**) | `RegistrationClosed` |
| 4 | **capacity:** count `Registered`; `Capacity > 0 && count >= Capacity` → **Waitlisted**, else Registered (0 = unlimited) | (no failure; sets the status) |
| 5 | already registered (not cancelled) | `AlreadyRegistered` |
| 6 | **course allowed** (`EnsureCourseAllowed`) | `NotEligibleForEvent` |
| 7 | **no overlapping event** (`ScheduleConflicts.Overlapping`) | `ScheduleConflict` ("…clashes with {title} on {time}") |
| 8 | save: reuse the old cancelled row, or insert a new one with `GenerateUniqueCode()` | |

   - **Overlap rule** (`Services/Services/ScheduleConflicts.cs`): two events overlap when `other.Start < this.End && other.End > this.Start`. **Back-to-back doesn't overlap** (one ends at 3:00, the next starts at 3:00). It counts the student's **Registered *and* Waitlisted** registrations; **cancelled registrations and cancelled events are ignored**.
   - The Details page warns **before** clicking: `EventService.GetEvent` fills `ConflictingEventTitle`, and the view says "This event happens at the same time as X, which you're already registered for. Cancel that registration first", with the button disabled. The server check in step 7 is the real guard.
   - **Overlap is also checked at the door:** `AttendanceService.CheckIn` and `SetStatus` call `ScheduleConflicts.CheckedInElsewhere`. If the student was already checked in to an overlapping event (e.g. they registered before the rule existed, or an event was rescheduled), they can't be recorded Present twice.
3. Controller: **Waitlisted** → warning toast; **Registered** → success toast; redirect to `Event/Details`.

**Auto-waitlist explanation (say it):**
"When an event is full I'm not rejected; my registration is saved as *Waitlisted* with my `RegisteredTime`. When someone cancels, `PromoteWaitlisted` promotes the oldest waitlisted students into the freed seats (and it also runs when an officer raises the capacity). So the waitlist is first-come, first-served and automatic."

- `Cancel` → `RegistrationService.Cancel`: only owner or the organization's manager; `CanCancel` (not cancelled, no attendance, Open/Closed event, before start); marks Cancelled; if it was a Registered seat → `PromoteWaitlisted`.
- **Demo tip:** register for the full event → show the waitlist badge/warning → (as officer or with another student) cancel one registered seat → show the waitlisted student became Registered.

## Step 4: My Events → QR ticket
- `RegistrationController.MyEvents` (Student only) → `RegistrationService.GetMyRegistrations(accountId)`. The view splits **current passes** (cards) from **attendance history** (table).
- Click **Show pass** → `GET /Registration/Ticket/{id}` → `GetTicket`: owner or org manager only. **Only if the status is Registered**, it generates `QrCodeManager.GenerateSvg(RegistrationCode)` (ZXing, inline SVG). A waitlisted/cancelled pass shows "no check-in code yet".
- The QR contains **only the 10-character code** (alphabet without 0/O/1/I). At the door `AttendanceService.CheckIn` looks it up **within the event being scanned**.
- **Say:** "The ticket never contains personal data. If the scanner fails, the officer can type the code or the student number."

## What to say if asked "what happens if…"
| Question | Answer |
|---|---|
| Two students click the last seat at once? | The event row is locked inside a transaction; the second is processed after and gets **Waitlisted**. |
| Student modifies the form to bypass the course rule? | They can't: the course is read from the database and the rule is checked in the service. |
| Registers for two events at the same time? | Blocked at step 7 (also warned on the Details page). Back-to-back is allowed. |
| Registered for a clashing event, then both are open? | Cancelling the first frees the second. Waitlisted counts as a registration for overlap purposes. |
| Cancelled, then wants back in? | Allowed while Open: the old row is reused (one row per student per event), status recalculated (may be Waitlisted). |
| Event is cancelled? | Overlap ignores cancelled events; the pass history shows "Event cancelled". |

## Quick file list to have open while presenting
`Controllers/AccountController.cs` · `Services/Services/UserService.cs` (AuthenticateUser) · `Services/Services/EventService.cs` (GetPublishedEvents, GetEvent) · `Services/Services/EventProjection.cs` · `Views/Shared/_PassRack.cshtml` · `Views/Event/Details.cshtml` · `Controllers/RegistrationController.cs` · `Services/Services/RegistrationService.cs` (Register, RegisterLocked, EnsureCourseAllowed, PromoteWaitlisted) · `Services/Services/ScheduleConflicts.cs` · `Views/Registration/MyEvents.cshtml`, `Ticket.cshtml` · `Services/Manager/QrCodeManager.cs`
(All paths relative to `ASI.Basecode.WebApp/` or `ASI.Basecode.Services/`.)
