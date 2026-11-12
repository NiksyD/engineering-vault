---
tags: [alliance, mock-defense, pages]
---

# P1 · Account Pages

Index: [[P0 - Page Map and How to Read These]] · Related: [[01 - System Flow and Architecture#5. Authentication and authorization]]

Controller: `WebApp/Controllers/AccountController.cs` · Views: `Views/Account/*` · Service: `UserService`

---

## 1. Sign in page: `GET /Account/Login`
- **Who:** anyone (`[AllowAnonymous]`). This is also the **default route** (`/` redirects here).
- **Action:** stores the `ReturnUrl` query value in `TempData["returnUrl"]`, **clears the session** (`SessionManager.Clear`), sets a new `SessionId`, returns the view.
- **View (`Login.cshtml`, layout `_AuthLayout`):** "ID card" with Username + Password fields, a **Sign in** button, and a footer link **Create an account** → `Account/Register`. The form posts to `Account/Login`; client validation is off (`novalidate`), the server validates.

## 2. Sign in submit: `POST /Account/Login`
- **Action `Login(LoginViewModel, returnUrl)`:**
  1. `ModelState` invalid (username or password empty) → redisplay.
  2. `UserService.AuthenticateUser(userId, password, ref user)`:
     - encrypts the typed password (`PasswordManager.EncryptPassword`) and finds a user with that username **and** password;
     - none → `LoginResult.Failed`; found but `!IsApproved` → `Pending`; found but `!IsActive` → `Inactive`; else `Success`.
  3. Success → `SignInManager.SignInAsync(user)` (claims + JWT-in-cookie, 120 min), session gets `UserName` and `Role`, then redirect to a **local** `returnUrl` (`Url.IsLocalUrl`) or `Home/Index`.
  4. Failure → error toast: "account pending approval" / "account inactive" / generic "invalid login", and the form is shown again.
- **Rules:** the generic message for a wrong username *or* password avoids revealing which usernames exist. The Pending/Inactive messages do reveal the account exists, but only after the correct password.
- **Say it:** "Login result is an enum, so each failure has its own message and the controller never needs to know why."
- **Gap to know:** no anti-forgery validation attribute and no lockout ([[05 - Code Review - Strengths, Risks, Limitations]] items 3, 8).

## 3. Registration page: `GET /Account/Register`
- **Who:** anyone. Shows the student sign-up form (`Register.cshtml`): First/Middle (optional)/Last name, Student no., Course (dropdown from `Courses.All`), Year (1–6), School email, Username, Password (with the live **password checklist**), Confirm password.
- `data-live-required` on the form adds red `*` markers that clear as fields are completed.

## 4. Registration submit: `POST /Account/Register`
- **Action `Register(UserViewModel)`:** `ModelState` check → `UserService.AddUser(model)` →
  - duplicate username → `UserExists` (shown on the Username field);
  - duplicate student number → `StudentNumberExists` (on the Student no. field);
  - invalid course (not in the list) → `InvalidCourse`;
  - success: role forced to **Student**, `IsActive = true`, **`IsApproved = false`**, password encrypted, audit fields set.
- On success: toast "pending approval" and redirect to Login. The student **cannot sign in until an Admin approves** ([[P8 - User Pages]] approvals).
- Unexpected exceptions are logged with `HandleExceptionLog` and shown as a generic server error.
- **Say it:** "Role and approval are decided on the server. The form model has no Role field, so a user can't promote themselves."

## 5. Access denied: `GET /Account/AccessDenied`
- Shown automatically when a signed-in user opens a page their role can't access (configured as `AccessDeniedPath`). Static message with a way back.

## 6. Sign out: `GET /Account/SignOutUser`
- `SignInManager.SignOutAsync` removes the auth cookie, redirects to Login. Linked from the account menu in `_Layout.cshtml` (desktop and mobile). It is a GET (see review note 4).

## 7. Dev account switcher: `POST /Account/SwitchAccount`
- Only works when `ASPNETCORE_ENVIRONMENT=Development`; otherwise `NotFound()`. `AccountSwitcherViewComponent` renders the button (bottom-right, listing active+approved users); selecting one signs out, signs in as that user (no password), and redirects to Home. Has CSRF validation.
- **Say it:** "It exists so I can demo all three roles quickly; it disappears in production."
