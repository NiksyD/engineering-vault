---
tags: [alliance, mock-defense, qa]
---

# 06 · Defense Q&A Cheat Sheet

Back to [[00 - Index]] · See also [[05 - Code Review - Strengths, Risks, Limitations]]

## Architecture

**Q: Why four projects?**
Separation of concerns: WebApp (HTTP/UI), Services (rules), Data (persistence), Resources (shared constants/messages). Controllers stay thin; the rules are testable without HTTP. See [[01 - System Flow and Architecture]].

**Q: What is the Repository + Unit of Work for?**
Repositories hide EF Core behind interfaces and return `IQueryable`, so services compose queries. `UnitOfWork` wraps the one scoped `DbContext` shared by all repositories in a request. Honest note: each repository method calls `SaveChanges()`, so it behaves more like auto-commit than a true unit of work.

**Q: Why dependency injection? What lifetimes?**
Loose coupling (controllers depend on `IEventService`, not `EventService`). Services, repositories, `UnitOfWork` and `DbContext` are *scoped* (per request); `IMapper` and the HTTP accessor are singletons.

**Q: What's AutoMapper doing?**
Maps view models ↔ entities; configured to ignore `Id`, `Status`, role and approval fields to prevent over-posting.

**Q: Why return JSON for check-in but views elsewhere?**
Check-in needs instant feedback and the next scan right away; a page reload would break the queue flow. Everything else uses server-rendered Razor with Post-Redirect-Get.

## Security

**Q: How does authentication work?**
Cookie authentication whose ticket is a signed JWT (HMAC-SHA256, secret from config, 120-minute expiry). Claims hold username, role and numeric account ID.

**Q: How is authorization enforced?**
Three layers: global "must be signed in"; `[Authorize(Roles=…)]`; and `AccessService.EnsureCanManageOrganization` in the service for officer scope.

**Q: Can an officer open another organization's attendance page by changing the URL?**
No. `GetAttendanceSheet`/`CheckIn`/`SetStatus`/`CheckOut` call `EnsureCanManageOrganization`, which throws `UnauthorizedAccessException`; the filter shows a 403/toast.

**Q: Can a student register themselves as an Admin?**
No. `AddUser` hard-codes `Role = Student` and `IsApproved = false`; the form model has no role field.

**Q: How do you prevent CSRF?**
`[ValidateAntiForgeryToken]` on state-changing POSTs; the AJAX check-in sends the form's token. *(Gap to admit: Login/Register POSTs lack it.)*

**Q: How are passwords stored?**
AES-encrypted with the app secret (from the base template). *Be honest:* hashing with salt (PBKDF2/bcrypt) is the correct approach and is the first improvement I'd make.

**Q: What stops open redirects?** `Url.IsLocalUrl(returnUrl)`.

**Q: What is the "Switch account" button?** A dev-only convenience; the view component doesn't render and the endpoint returns 404 unless `ASPNETCORE_ENVIRONMENT=Development`.

## Business rules

**Q: When can a student register?** Event is `Open`, before the registration deadline and before the start time, and the student isn't already registered.

**Q: What happens when an event is full?** The student is `Waitlisted`. On a cancellation (or a capacity increase) the oldest waitlisted students (`RegisteredTime`) are promoted automatically.

**Q: How is "Late" decided?** `now > StartTime + LateAfterMinutes` (per-event setting, default 15), otherwise Present.

**Q: What if a student scans twice?** The service sees an existing check-in time and returns "already checked in" with the original time; the browser also ignores the same code for 3 seconds.

**Q: What happens to no-shows?** When the event is set to `Completed`, `MarkAbsentees` creates `Absent` attendance for registered students with no record. An officer can later override a status with remarks.

**Q: Can an event go backwards (Completed → Open)?** No. `AllowedTransitions` makes Completed/Cancelled terminal; `Closed → Open` is allowed to reopen registration.

**Q: Can you delete an event or organization?** An event only if it has no registrations; an organization only if it has no events.

**Q: Can a cancelled student register again?** Yes. The existing row is reused (one row per student per event) with a fresh status and time.

**Q: What does capacity 0 mean?** Unlimited (never waitlists).

## Data

**Q: How do you guarantee no duplicate attendance/registration?** Unique indexes: `(event_id, student_id)` on registrations and `registration_id` on attendances, in addition to service checks.

**Q: Where is the waitlist stored?** As `status = Waitlisted` on `event_registrations`; no separate table.

**Q: What does the QR contain?** Only the 10-character registration code. The server looks up the registration and verifies it belongs to the event being scanned.

**Q: Why are enums stored as strings?** Readable data and safe against reordering enum values (`HasConversion<string>()`).

## Improvements to volunteer
1. Password hashing instead of reversible encryption.
2. Anti-forgery on Login/Register, sign-out as POST.
3. Transaction (or locking) around register and cancel-with-promotion.
4. Validate active/role on each request (or short sessions) so deactivation takes effect immediately.
5. Login throttling/lockout.
6. Unit tests for the services (late threshold, waitlist promotion, status transitions, officer scope).
7. Email notifications for waitlist promotion; UTC time storage.

## Things to know cold (rapid fire)
- Default route: `Account/Login`.
- Roles: `Admin`, `Officer`, `Student`; managers constant = `"Admin,Officer"`.
- Cookie scheme name `ASI_Basecode`; session cookie name `asi.basecode`.
- Code alphabet excludes `0 O 1 I`; length 10.
- Password rule: 8+ chars with upper, lower, digit, special.
- Username rule: 4–50 chars, letters/digits/`.`/`_`/`-`.
- Only JSON endpoint: `POST /Attendance/CheckIn`. CSV endpoints: `ExportEvent`, `ExportSummary`.
- Tech: .NET 9, ASP.NET Core MVC, EF Core (SQL Server, snake_case), AutoMapper, CsvHelper, ZXing, html5-qrcode.
- Exceptions handled by the global filter: `InvalidDataException` (400), `KeyNotFoundException` (400), `UnauthorizedAccessException` (403).
