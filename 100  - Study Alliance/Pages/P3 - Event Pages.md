---
tags: [alliance, mock-defense, pages]
---

# P3 · Event Pages

Index: [[P0 - Page Map and How to Read These]] · Lifecycle theory: [[03 - Major Flows Code Walkthrough#D. Event lifecycle]]

Controller: `EventController` · Service: `EventService` · Views: `Views/Event/{Index,Details,Manage,Form}.cshtml` + `Shared/_PassRack.cshtml` · Model: `EventViewModel`

---

## 1. Browse events: `GET /Event/Index?search=&showPast=`
- **Who:** any signed-in user (students' main catalog).
- **Action → service:** `GetPublishedEvents(CurrentUser, search, upcomingOnly: !showPast)`.
- **Query logic:**
  1. `Search`: case-insensitive match on **title, venue, organization name, organization acronym**.
  2. **Drafts are always excluded** (`Status != Draft`).
  3. Upcoming only (default): `EndTime >= now` **and** not Cancelled. "Include past events" shows everything non-draft, including cancelled.
  4. Ordered by start time; projected with counts and *my* registration (`EventProjection.ToViewModel(accountId)`); `CanManage` is set for events whose organization the user manages.
- **View:** search box + "Include past events" checkbox (auto-submits on change; both are GET so results are bookmarkable), then `_PassRack`:
  - each **pass card** = org band, title link → `Event/Details`, date, time, venue, **seat meter** (10 segments, filled proportionally; "n going" if unlimited), and a footer: *Your pass + badge* if I'm registered/waitlisted, else "Register by …" (plus a **Waitlist** badge when `SlotsLeft == 0`), else "Registration closed".
  - cards are paged client-side (9 per page).
- **Say it:** "The browse page never shows drafts, and the card footer tells the student their standing at a glance."

---

## 2. Event details: `GET /Event/Details/{id}`
- **Who:** any signed-in user. Action calls `GetEvent(id, CurrentUser)` and, if the user can manage it, `GetAllowedStatusChanges(status)` into `ViewBag.StatusChanges`.
- **Service rules:** missing → `KeyNotFoundException`. **A Draft is "not found" for anyone who can't manage it** (so students can't guess the URL). `CanManage` = Admin, or Officer who is a member of the event's organization.
- **View:** two columns.
  - **Left "ID card":** organization, title, status badge, starts/ends, venue, register-by deadline, seats (`n of capacity taken · x left`, "Open seating" if unlimited, waitlist count), *Late after n min* (managers only), description.
  - **Right, student panel "Your pass"** (only for the Student role):
    - already registered/waitlisted → badge; waitlisted users see "you move up automatically"; Registered users get **Show my pass** → `Registration/Ticket/{id}`; **Cancel registration** form → `POST Registration/Cancel` (with `returnUrl` back to this page and a confirm dialog) shown only while the event is Open/Closed and before the start time;
    - not registered and `IsRegistrationOpen` → **Register for this event** (or **Join the waitlist** when no seats are left) → `POST Registration/Register`;
    - otherwise "Registration is closed".
  - **Right, manager panel "Run this event"** (when `CanManage`): **Open the check-in desk** (only when Open/Closed) → `Attendance/Index`; **Attendance report** → `Report/Event`; **Edit details** (hidden for Completed/Cancelled) → `Event/Edit`; and **Change status** buttons built from `AllowedTransitions`. Labels: Draft→Open = "Publish and open registration", Closed→Open = "Reopen registration", Open→Closed = "Close registration", "Mark completed", "Cancel event". Each has a **confirm dialog** (Completed warns that no-shows become Absent; Cancelled warns it's permanent).
- **Edge cases:** a student who can't register sees why; an officer of another organization sees the page but **not** the manager panel.
- **Say it:** "Only the transitions the state machine allows are rendered, but the server re-validates in `ChangeStatus` anyway."

---

## 3. Manage events: `GET /Event/Manage?search=&status=`
- **Who:** `[Authorize(Roles = "Admin,Officer")]`.
- **Service:** `GetManagedEvents`: events whose `OrganizationId` is in `GetManagedOrganizationIds(user)`, optional search, optional **status filter**, ordered by **newest start first**; every row flagged `CanManage`.
- **View:** header with **New event** → `Event/Create`; toolbar (search + status dropdown that auto-submits); table columns: Event (link, org · venue), When, Registered/capacity, Waitlist, Attended, Status badge, and row actions:
  - **Check in** (if Open or Closed) → `Attendance/Index`;
  - **Edit** pencil (hidden for Completed/Cancelled) → `Event/Edit`;
  - **Report** chart icon → `Report/Event`;
  - **Delete** trash (form POST with confirm) shown when `RegisteredCount == 0 && WaitlistedCount == 0`.
- **Known mismatch to be ready for:** the service refuses to delete an event that has **any** registration row, *including cancelled ones*. The button only checks Registered and Waitlisted counts, so for an event whose only registrations are cancelled the button appears and the click shows the "event has registrations" message. Safe (server wins), just slightly confusing UX.
- **Say it:** "Officers only ever see their own organizations' events here, because the query is filtered by their memberships."

---

## 4. Create event: `GET /Event/Create` and `POST /Event/Create`
- **GET:** `LoadOrganizations()` fills a dropdown from `GetManagedOrganizationOptions` (only *active* organizations the user manages); returns `Form.cshtml` with a blank `EventViewModel` (defaults: start in 7 days at 9:00, end 12:00, deadline 6 days ahead at 17:00, capacity 50, late after 15).
- **View (`Form.cshtml`, shared with Edit):** fields Organization, Venue, Title, Description, Starts/Ends/Register-by (`datetime-local`), Seats (hint: 0 = open seating; overflow joins the waitlist), Late after (minutes). If the user belongs to no active organization a notice says to ask an administrator. Submit button text: "Create draft".
- **POST:** model validation (`[Required]`, `[StringLength]`, `[Range]`, plus `IValidatableObject`: **end after start** and **deadline not after start**) → `EventService.CreateEvent`:
  - `EnsureCanManageOrganization(model.OrganizationId)` (an officer can't create an event for someone else's organization by editing the dropdown value);
  - AutoMapper maps the fields; **Status forced to Draft**; created/updated by & time set.
  - Redirect to `Event/Details/{newId}` with a success toast.

## 5. Edit event: `GET /Event/Edit/{id}` and `POST /Event/Edit`
- **GET:** `GetEvent`; if not `CanManage` the action throws `UnauthorizedAccessException` (→ toast). Same form, button "Save changes".
- **POST → `UpdateEvent`:**
  1. `FindEvent` (with registrations); scope check for the event's **current** organization **and** the **new** organization in the form;
  2. if `Capacity > 0` and `Capacity < registered count` → `CapacityBelowRegistered` (shown in the validation summary so the user keeps their input);
  3. AutoMapper updates the entity (**Status is ignored**, so editing can't change the lifecycle);
  4. `PromoteWaitlisted(eventId)`: if capacity went up, waitlisted students move into the new seats.
- **Gap to know:** the Edit button is hidden for Completed/Cancelled events, but `UpdateEvent` has **no status check**, so a hand-typed `GET/POST /Event/Edit/{id}` still edits a completed event. Fix: reject edits when the status is terminal.

## 6. Delete event: `POST /Event/Delete/{id}`
- `[Authorize(Roles="Admin,Officer")]` + CSRF. `DeleteEvent`: scope check; **refuses if the event has any registrations**; otherwise deletes. Redirects to Manage with a success toast.

## 7. Change status: `POST /Event/ChangeStatus` (`id`, `status`)
- `ChangeStatus`: scope check; `AllowedTransitions[current]` must contain the new status, else `InvalidStatusChange`; saves; **if `Completed` → `MarkAbsentees`**. Toast text differs for Completed ("absentees marked").
- Transitions: Draft→Open/Cancelled · Open→Closed/Completed/Cancelled · Closed→Open/Completed/Cancelled · Completed and Cancelled are final.
- **Side effects to remember:**
  - Draft→Open is what makes the event **visible to students** and starts registrations.
  - Closed stops *new registrations* (registration requires `Open`), but attendance is still allowed while Closed.
  - Reopening (Closed→Open) does not auto-promote anyone; promotion happens on cancellation or capacity change.
  - Cancelling an event keeps registrations (students keep their record, the event is hidden from "upcoming" lists).
