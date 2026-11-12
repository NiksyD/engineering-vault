---
tags: [alliance, mock-defense, pages]
---

# P4 · Registration Pages

Index: [[P0 - Page Map and How to Read These]] · Theory: [[03 - Major Flows Code Walkthrough#B. Register for an event with automatic waitlist]]

Controller: `RegistrationController` · Service: `RegistrationService` · Views: `Registration/MyEvents.cshtml`, `Registration/Ticket.cshtml` · Model: `RegistrationViewModel`

---

## 1. My passes: `GET /Registration/MyEvents`
- **Who:** `[Authorize(Roles = "Student")]` only. An Officer or Admin opening it is redirected to **Access Denied** (they have no registrations page; officers manage events instead).
- **Service:** `GetMyRegistrations(accountId)`: all of the student's registrations, newest event first, projected through `RegistrationProjection` (event title, organization, venue, times, event status, code, status, attendance status, check-in/out times, remarks).
- **View logic** (split happens in the view):
  - **current** = status ≠ Cancelled **and** event end ≥ now **and** event not Cancelled, ordered by start;
  - **history** = everything else.
- **Current passes** are cards: org, title (→ `Event/Details`), date/time/venue, buttons:
  - **Show pass** (only if status *Registered*) → `Registration/Ticket/{id}`;
  - **Cancel** (only if `CanCancel`) → `POST Registration/Cancel` with a confirm dialog;
  - footer: "Valid pass" or "On the waitlist" and a badge (the **attendance** status if one exists, otherwise the registration status).
- **Attendance history** table: event, date, registration badge (shows "Event cancelled" when the event was cancelled), attendance badge (or "Not recorded"), and check-in/out times. This is where a student sees Present/Late/Absent after an event.
- **Say it:** "Students see their standing and their attendance in one place."

## 2. Register: `POST /Registration/Register` (`eventId`)
- `[Authorize(Roles="Student")]` + CSRF. Triggered by the button on `Event/Details`. Logic: [[03 - Major Flows Code Walkthrough#B. Register for an event with automatic waitlist]] (checks event is not Draft, is Open, before deadline and start; counts seats; Waitlisted vs Registered; reuse of a cancelled row; new unique code).
- Controller: **Waitlisted** → warning toast; **Registered** → success toast; both redirect back to `Event/Details/{eventId}`.
- Errors (registration closed, already registered, event not found) come from the service as exceptions and are shown as an error toast by `ServiceExceptionFilter` on the page the user came from.

## 3. Cancel: `POST /Registration/Cancel` (`id`, `returnUrl`)
- **Who:** any signed-in user, but the service allows only the **owner** or a **manager of the event's organization** (`EnsureOwnerOrManager`).
- **Rules:** `CanCancel` = not already cancelled, **no attendance recorded**, event is **Open or Closed**, and **before the start time**. Otherwise `CannotCancelRegistration`.
- **Effects:** status → Cancelled, `CancelledTime` set; if it was a *Registered* seat, `PromoteWaitlisted(eventId)` moves the oldest waitlisted student in. Cancelling a *waitlisted* registration frees nothing.
- **Redirect:** to `returnUrl` only if `Url.IsLocalUrl` (the Details page passes it); from My Passes there is no returnUrl, so it goes to `MyEvents`.
- **Say it:** "Cancellation and promotion happen in the same request, so a freed seat is filled immediately in registration order."

## 4. Ticket (event pass): `GET /Registration/Ticket/{id}`
- **Who:** signed-in; the owner or a manager of that event's organization (`EnsureOwnerOrManager`), otherwise 403 toast. This also lets an officer open a student's pass from the desk if needed.
- **Service `GetTicket`:** loads the registration; **only if status is Registered** generates `QrCodeSvg = QrCodeManager.GenerateSvg(RegistrationCode)` (ZXing, inline SVG, 240 px).
- **View:** a lanyard + ID card: organization, event title, student **initials avatar** (`BadgeHelper.Initials`), name, student number, date, time, venue; then the **QR code** and the readable **10-character code** ("if the scanner struggles, read this code to the officer"). A waitlisted or cancelled pass shows "This pass is waitlisted/cancelled, so it has no check-in code yet." The footer shows the attendance status once recorded, otherwise the registration status. **Print pass** button calls `window.print()`; screen-only elements carry `no-print`.
- **Security point:** the QR contains only the random code, nothing personal. An officer's check-in query additionally requires the code to belong to the event being scanned.
