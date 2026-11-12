---
tags: [alliance, mock-defense, architecture]
---

# 01 · System Flow and Architecture

Back to [[00 - Index]] · Next: [[02 - Endpoint Map (GET and POST)]]

## 1. Solution layout (4 projects)

| Project | Contains | Rule |
|---|---|---|
| `ASI.Basecode.WebApp` | Controllers, Razor views, `wwwroot` (CSS/JS), `Startup*.cs`, auth classes, `ServiceExceptionFilter`, `ControllerBase<T>` | **Thin.** Receive request → call a service → choose the response. |
| `ASI.Basecode.Services` | Services (business rules), service/view models, `PasswordManager`, `QrCodeManager`, `SessionManager`, projections | **All logic lives here.** Throws exceptions on rule violations. |
| `ASI.Basecode.Data` | EF Core models, `AsiBasecodeDBContext`, repositories, `UnitOfWork` | **Only reads/writes the database.** No business rules. |
| `ASI.Basecode.Resources` | `Const`, `Enums`, `Courses`, `.resx` message files | Shared text and constants. No logic. |

Dependency direction: `WebApp → Services → Data`, and all three reference `Resources`.

## 2. Technology stack

- ASP.NET Core MVC with Razor views, .NET 9, server-rendered (no SPA).
- Entity Framework Core + SQL Server (LocalDB in dev). `UseSnakeCaseNamingConvention()` maps `EventRegistration` → `event_registrations`, etc.
- AutoMapper (`Startup.AutoMapper.cs`) for view model ↔ entity mapping.
- CsvHelper for CSV export; ZXing for server-side QR SVG; `html5-qrcode` in the browser for scanning.
- Front end: custom `pass.css`, jQuery + jQuery Validation, Font Awesome, toastr.

## 3. The path of one request

Example: officer scans a QR at the check-in desk.

```
Browser (Views/Attendance/Index.cshtml, html5-qrcode)
  │  fetch POST /Attendance/CheckIn   (eventId, code, anti-forgery token, X-Requested-With)
  ▼
ASP.NET pipeline: HTTPS redirect → static files → session → routing → authentication → authorization
  │  global AuthorizeFilter("RequireAuthenticatedUser") + [Authorize(Roles="Admin,Officer")] on the class
  │  [ValidateAntiForgeryToken] on the action
  ▼
AttendanceController.CheckIn(eventId, code)          ← WebApp/Controllers
  │  CurrentUser  (built from the auth cookie claims)
  ▼
AttendanceService.CheckIn(...)                       ← Services/Services
  │  FindEvent → EnsureCanManageOrganization → EnsureAttendanceAllowed → lookup → late rule
  ▼
Repositories (EventRegistrationRepository, AttendanceRepository)   ← Data/Repositories
  │  AddAttendance/UpdateAttendance → UnitOfWork.SaveChanges()
  ▼
SQL Server
  ▲
Controller returns Json(result) → browser shows green/red result card and updates the table row
```

If the service throws `InvalidDataException`, `KeyNotFoundException` or `UnauthorizedAccessException`, [[#6. Error handling|ServiceExceptionFilter]] converts it into JSON (AJAX) or a toast + redirect (normal request).

## 4. Startup and the middleware pipeline

Files: `Program.cs`, `Startup.cs`, `Startup.Auth.cs`, `Startup.DI.cs`, `Startup.AutoMapper.cs`, `Startup.Logger.cs`.

`Program.cs`:
1. `WebApplication.CreateBuilder(...)` loads `appsettings.json`, `appsettings.{Env}.json`, then environment variables (so a host can override the connection string and secret key).
2. `new StartupConfigurer(configuration)` → sets `PathManager`, builds the signing key, calls `PasswordManager.SetUp(...)`.
3. `ConfigureServices` registers: memory cache, `AsiBasecodeDBContext` (SQL Server, 120 s command timeout, snake-case), MVC + Razor runtime compilation, session, AutoMapper, DI services, authorization.
4. `ConfigureApp` pipeline order: `UseExceptionHandler("/Home/Error")` + `UseHsts` (non-Development) → logger → `UseHttpsRedirection` → `UseStatusCodePagesWithReExecute("/Home/Status?code=…")` → `UseStaticFiles` → localization → `UseSession` → `UseRouting` → `UseAuthentication` → `UseAuthorization`.
5. Default route: `{controller=Account}/{action=Login}/{id?}` (the app opens on the login page).

### Dependency injection (`Startup.DI.cs`)
All **Scoped** (one instance per HTTP request): `IUnitOfWork`, the 7 services (`IUserService`, `IAccessService`, `IOrganizationService`, `IEventService`, `IRegistrationService`, `IAttendanceService`, `IReportService`), the 5 repositories, `SignInManager`, `TokenProvider`.
Singletons: `IHttpContextAccessor`, `IActionContextAccessor`, `TokenProviderOptionsFactory`, `TokenValidationParametersFactory`, AutoMapper's `IMapper`.

Because `UnitOfWork` is scoped and wraps one `DbContext`, every repository in a request shares the same context.

## 5. Authentication and authorization

### Sign-in
1. `AccountController.Login` (POST) → `UserService.AuthenticateUser(userId, password)`.
2. The submitted password is encrypted with `PasswordManager.EncryptPassword` and compared to the stored value (see [[05 - Code Review - Strengths, Risks, Limitations]] for why this matters).
3. Result enum `LoginResult`: `Success`, `Failed`, `Inactive`, `Pending` (not yet approved). Each maps to its own message.
4. On success `SignInManager.SignInAsync(user)` builds claims (`NameIdentifier`=username, `Name`, `Role`, `UserId`, `UserName`, `AccountId`=numeric PK) and signs in with the cookie scheme `ASI_Basecode`.
5. The cookie's ticket is a **signed JWT** (`CustomJwtDataFormat` implements `ISecureDataFormat<AuthenticationTicket>`; HMAC-SHA256 with `TokenAuthentication:SecretKey`; expiry `ExpirationMinutes` = 120; `AllowRefresh = false`).
6. The session also stores `UserName` and `Role` (display only).
7. A local `returnUrl` is honored only if `Url.IsLocalUrl(returnUrl)` (open-redirect protection).

### How each request knows who you are
`ControllerBase<T>.CurrentUser` rebuilds a `CurrentUserModel { AccountId, UserId, Role }` from the claims. Controllers pass it to services, and services do the permission checks.

### Three layers of authorization
1. **Global:** `AuthorizeFilter("RequireAuthenticatedUser")` is added to every MVC action. Everything requires login unless marked `[AllowAnonymous]` (Login, Register, Error, Status, SignOutUser, SwitchAccount).
2. **Role attributes:** `[Authorize(Roles = Const.RolesManagers)]` (`"Admin,Officer"`), `Const.RoleAdmin`, `Const.RoleStudent`.
3. **Scope check inside services:** `AccessService.EnsureCanManageOrganization(orgId, user)`: Admin always passes; Officer passes only if a row exists in `organization_members` for (org, user); otherwise `UnauthorizedAccessException`. This is what stops Officer A from touching Officer B's organization even though both hold the "Officer" role.

Wrong role → redirected to `/Account/AccessDenied`. Not logged in → `/Account/Login?ReturnUrl=…`.

### Account lifecycle
`Register` (public) creates a **Student** with `IsApproved = false` → the student cannot sign in (`Pending`) until an Admin approves in `User/Approvals`. Admin-created users (`User/Create`) are approved immediately. `ToggleActive` deactivates/reactivates; an admin cannot deactivate themselves.

## 6. Error handling

`ServiceExceptionFilter` (registered globally in `Startup.Auth.cs`) handles only three exception types thrown by services:

| Exception | Meaning | AJAX response | Normal response |
|---|---|---|---|
| `InvalidDataException` | A business rule failed (registration closed, already registered…) | JSON `{success:false,message}` HTTP 400 | Toast + redirect back (Referer) or `/Home/Index` |
| `KeyNotFoundException` | Record not found / hidden draft | JSON HTTP 400 | same |
| `UnauthorizedAccessException` | Officer outside their organization | JSON HTTP 403 | same |

Anything else → `UseExceptionHandler("/Home/Error")` (500 page; logged in `HomeController.Error`). 404 and other empty status codes → `/Home/Status`.

Form pages (`Create`/`Edit`) catch `InvalidDataException` themselves and show it as a validation message so the user keeps what they typed. `AddServiceError` maps known messages to the right field (`UserId`, `StudentNumber`, `Course`).

## 7. Flash messages
`NotifySuccess` / `NotifyError` write to `TempData["SuccessMessage"]` / `["ErrorMessage"]`; the layout renders them as toastr toasts on the next page (Post-Redirect-Get pattern). Waitlist uses `TempData["WarningMessage"]`.

## 8. Repository + Unit of Work pattern
- `BaseRepository` holds the `IUnitOfWork` and exposes `Context`, `GetDbSet<T>()`.
- Repositories return `IQueryable<T>` (e.g. `GetRegistrations()`), so services compose queries (`Where`, `Include`, `Select`) and EF translates it to one SQL statement.
- Each Add/Update/Delete calls `UnitOfWork.SaveChanges()` immediately, so **every repository write is its own commit**. There is no multi-step transaction (see the race-condition note in [[05 - Code Review - Strengths, Risks, Limitations]]).

## 9. Projections
`EventProjection.ToViewModel(accountId)` and `RegistrationProjection.ToViewModel` are expression trees reused by many services. They compute seats left, counts, "my registration" and `CanCancel` in SQL instead of loading whole entities.

## 10. Roles → what each can reach

| Area | Student | Officer | Admin |
|---|---|---|---|
| Dashboard (`Home/Index`) | own upcoming/attended | managed orgs' stats | all stats + pending approvals |
| Browse events / details | ✔ (no drafts) | ✔ (sees own drafts) | ✔ |
| Register / cancel / ticket / My events | ✔ | cancel/ticket for own org's registrations | same as officer for any org |
| Create/edit/delete/status events | ✘ | own orgs only | all |
| Attendance desk (scan, check-out, override) | ✘ | own orgs only | all |
| Reports + CSV | ✘ | own orgs only | all |
| Organizations + members | ✘ | ✘ | ✔ |
| Users + approvals | ✘ | ✘ | ✔ |
