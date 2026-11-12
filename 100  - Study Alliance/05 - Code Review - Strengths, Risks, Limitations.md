---
tags: [alliance, mock-defense, code-review]
---

# 05 · Code Review: Strengths, Risks, Limitations

Back to [[00 - Index]] · Previous: [[04 - Data Model]] · Next: [[06 - Defense Q&A Cheat Sheet]]

This is a self-review done by reading the source (not by running the app or the tests; the repo has no test project). Items marked **verified in code** I confirmed by reading the cited file. Know the weak points before the panel finds them, and prepare the honest answer plus the fix.

## Strengths (say these proudly)

1. **Clean layering.** Controllers are thin; every rule lives in a service; repositories only touch the DB. Easy to explain and to test.
2. **Defense in depth on authorization:** global login filter → role attribute → organization-scope check in the service. An officer can't act on another org even by crafting a URL.
3. **Server-side enforcement of the state machine** (`AllowedTransitions`), not just hiding buttons.
4. **Database-level integrity** (unique indexes on registration per student/event, attendance per registration, registration code, username, student number, member per org).
5. **Over-posting protection:** AutoMapper ignores `Status`, `Id`, role/approval fields; `AddUser` forces `Role = Student` and `IsApproved = false`.
6. **CSRF protection** on all state-changing POSTs that matter, including the AJAX check-in (token copied from the form).
7. **Good UX for the hardest moment (the door):** JSON check-in with no reload, 3-second duplicate-scan debounce, typed-code fallback, result card, live counters.
8. **Central error handling** (`ServiceExceptionFilter`): rule violations become friendly messages, AJAX gets JSON with 400/403.
9. **Open-redirect protection:** `Url.IsLocalUrl` on `returnUrl` (Login, Cancel).
10. **Efficient queries:** projections and counts computed in SQL, bulk absentee insert, one query for the check-in lookup.
11. **Readable codes:** 10 characters, ambiguous characters removed, `RandomNumberGenerator`.
12. **Deployment thought-through:** environment-variable overrides, hosted SQL script generator, dev-only account switcher returning 404 in production.

## Risks and weaknesses (be ready to admit and fix)

| # | Finding | Where | Why it matters | Fix to propose |
|---|---|---|---|---|
| 1 | **Passwords are encrypted (reversible), not hashed.** AES, key = first 16 bytes of the app secret, **fixed all-zero IV**, so identical passwords produce identical ciphertext. Anyone with the secret key can decrypt every password. | `Services/Manager/PasswordManager.cs` (verified in code) | Standard is a slow salted hash (PBKDF2/bcrypt/Argon2 via `PasswordHasher<T>`). | Replace with `PasswordHasher`; migrate on next login. Note: this class comes from the provided ASI base code, and the demo SQL is keyed to it. |
| 2 | **Secret key committed in `appsettings.json`** (`AsiBasecode_keySecret@$13376934212`). | `WebApp/appsettings.json` (verified) | It signs the login cookie *and* is the password encryption key. Mitigated: README/hosted script require overriding it via env var in production, and production secrets are git-ignored. | User secrets in dev; env var / vault in prod; rotate. |
| 3 | **Login and Register POSTs have no `[ValidateAntiForgeryToken]`.** | `AccountController.cs` `Login` and `Register` POST (verified: attributes absent) | Login-CSRF (forcing a victim into the attacker's account) is low severity but a classic checklist item. All other POSTs are protected. | Add the attribute (the forms already use tag helpers, which emit the token), or a global `AutoValidateAntiforgeryTokenAttribute` filter. |
| 4 | **Sign-out is a GET** (`SignOutUser`), anonymous, no CSRF. | `AccountController.cs`; links in `_Layout.cshtml` | A malicious page can log users out (nuisance). | Make it POST + token. |
| 5 | **Race condition on the last seat.** Count of registered seats and the insert are separate commits. | `RegistrationService.Register` | Two simultaneous requests can both pass `registered < capacity` and exceed capacity. | Wrap in a transaction with serializable isolation/`UPDLOCK`, or re-check after insert. |
| 6 | **No transaction across multi-step operations.** Every repository call commits on its own (`UnitOfWork.SaveChanges()` inside each Add/Update). E.g. `Cancel` saves the cancellation, then promotes the waitlist in separate saves; `ChangeStatus` saves the status, then marks absentees separately. | `Data/Repositories/*`, services | A crash between steps leaves a half-applied state (e.g. event Completed but no Absent rows). | Make the unit of work explicit and commit once per use case. |
| 7 | **Deactivating a user doesn't end their session.** Auth is cookie/JWT-claims only (120 min); I found no per-request check of `IsActive`/`IsApproved` or role. | `Authentication/*`, `ToggleActive` (searched, none found) | A deactivated or demoted user keeps access until the cookie expires. | Validate against the DB in a `OnValidatePrincipal` hook, or shorten expiry. |
| 8 | **Login has no brute-force protection** (no lockout/rate limit/CAPTCHA). | `AccountController.Login`, `UserService.AuthenticateUser` | Unlimited password guessing. | Lockout counter or rate-limiting middleware. |
| 9 | **Cookie `SecurePolicy = SameAsRequest`.** | `Startup.Auth.cs` (verified) | Over plain HTTP the cookie isn't `Secure`. Mitigated by `UseHttpsRedirection` + HSTS outside Development. | `Always` in production. |
| 10 | **Check-in by student number** accepts any registered student's number, and student numbers aren't secret. | `AttendanceService.CheckIn` | By design (manual fallback when the camera fails), and only officers of that org can do it. It's a policy trade-off, not a bug. | Mention it as intentional; log who recorded it (`RecordedBy` already does). |
| 11 | **Reject deletes the user row permanently** (no audit trail of the rejection). | `UserService.RejectUsers` | Lost history; can't tell "rejected" from "never existed". | Soft-delete or a `RejectedBy/Time` field. |
| 12 | **Time handling uses server local time** (`DateTime.Now`), no time zone. | everywhere | Wrong if the server isn't in the school's time zone (hosted servers often are UTC). | Store UTC and convert, or fix the host time zone. |
| 13 | **Case-insensitive search via `ToLower().Contains`** can't use indexes. | `EventService.Search`, `UserService.GetUsers` | Fine at student-org scale; slow at large scale. | Full-text search or collation-based comparison. |
| 14 | **Unused/legacy template code remains:** `ControllerBase` exposes `ClientId`, `ClientSystemId`, `Supervisor`…, Japanese comments (`認証OK`), `SessionManager`, `SetupRoot` path `C:\setup\...`. | `Mvc/ControllerBase.cs`, `AccountController.cs`, `appsettings.json` | Looks unfinished; `ClientId` would throw if called (no such claim). | Remove dead members. Explain: inherited from the ASI base code. |
| 15 | **No automated tests** in the solution (no test project in `ASI.Basecode.sln`). | repo | Rules like the late threshold, waitlist promotion and transitions are easy to unit-test. | xUnit tests for the services with an in-memory/SQLite DB. |
| 16 | **Debug-level EF logging** is enabled in `appsettings.json` (`Microsoft.EntityFrameworkCore: Debug`). | `appsettings.json` | Logs SQL (and parameters) in production. | `Warning` level in production config. |

## Limitations (scope, not defects)

- Single campus: no multi-tenant, no email/SMS notifications, no password reset (an admin edits the user), no email verification of the student.
- QR camera scanning only works over **HTTPS or localhost** (browser rule). Typing the code always works.
- No offline mode: check-in needs a server connection (the page shows a red "couldn't reach the server" card).
- Waitlist is automatic only; there is no manual reorder.
- Event times have no recurrence; capacity `0` means unlimited.
- Reports are tables + CSV; there are no charts.

## Quick "is it good?" verdict
A well-structured teaching-grade MVC app with strong domain rules and access control. The weaknesses are in the **credential-handling and concurrency edges** (items 1–8), most inherited from the base template or caused by committing each repository call separately. All have small, well-understood fixes. Lead with the strengths, then volunteer items 1, 3, 5, 6 with their fixes before the panel does.
