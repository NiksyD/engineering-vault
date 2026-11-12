---
tags: [alliance, mock-defense, pages]
---

# P8 · User Pages (Admin only)

Index: [[P0 - Page Map and How to Read These]]

Controller: `UserController` (class-level `[Authorize(Roles = "Admin")]`) · Service: `UserService` · Views: `User/{Index,Form,Approvals}.cshtml` · Models: `UserModel`, `UserViewModel`

---

## 1. Users list: `GET /User/Index?search=&role=`
- `GetUsers(search, role)`: search matches **username, name or student number** (case-insensitive); optional role filter; ordered by role then name; mapped with AutoMapper (password never copied).
- **View:** buttons **Account approvals** → `User/Approvals` and **New user** → `User/Create`; toolbar with search and role dropdown (auto-submit); table: name + email, username, student no., course · year, role badge, status badge (**Pending approval**, Active or Inactive), and row actions **Edit** → `User/Edit/{id}` and **Deactivate/Reactivate** (POST with confirm). On phones the columns fold into the name cell.

## 2. Create user: `GET|POST /User/Create`
- `Form.cshtml` (shared with Edit): First/Middle/Last name, Email, Username, Password (with the password checklist), **Role** dropdown (Admin/Officer/Student), Student no., Year (1–6), Course dropdown, **Active** checkbox.
- **POST:** password is required for new users; `UserModel.Validate` and model validation run; `CreateUser(model, actor)`:
  - duplicate username → `UserExists`; duplicate student number → `StudentNumberExists` (placed on the matching field by `AddServiceError`);
  - `IsApproved = true` automatically (admin-created accounts need no approval), `ApprovedBy` = the admin, password encrypted, audit fields set.
- The Admin is the only way to create **Officers** and other **Admins**; self-registration can only produce Students.

## 3. Edit user: `GET|POST /User/Edit/{id}`
- **GET:** `GetUser(id)` with the password blanked; the password box says "Leave blank to keep the current one".
- **POST → `UpdateUser`:** username uniqueness is re-checked only if it changed; student number uniqueness excludes this user; AutoMapper updates fields (it **ignores** Id, Password, Name, approval fields and CreatedTime); **a blank password keeps the existing encrypted password**, otherwise the new one is encrypted; `UpdatedBy` = admin.

## 4. Deactivate / reactivate: `POST /User/ToggleActive/{id}`
- **An admin cannot deactivate themselves** (`id == CurrentUser.AccountId` → error toast).
- Flips `IsActive`. Login then returns `Inactive` ("account inactive"). **Caveat:** an already signed-in user keeps their session until the cookie expires (120 min) because the cookie claims aren't re-checked ([[05 - Code Review - Strengths, Risks, Limitations]] item 7).

## 5. Approvals: `GET /User/Approvals`
- `GetPendingUsers()`: users with `IsApproved == false`, oldest request first.
- **View:** explanation ("can't sign in until approved; check each request against student records"); **Approve all (n)** button (POST with confirm); a table with **checkboxes**, name, student no., course · year, email, username, requested time; a toolbar with "*n* selected", **Approve selected** and **Reject selected** (both disabled until something is ticked; Reject asks "the accounts will be deleted"). A **select-all** checkbox selects only the rows on the current page; its state (checked / indeterminate) and the count update as you tick, page, or filter (listens to `pager:render`).

## 6. Approve / Approve all / Reject: `POST`
| Endpoint | Behavior |
|---|---|
| `Approve(int[] ids)` | at least one id (`NoUsersSelected` otherwise); only users still unapproved are affected; sets `IsApproved`, `ApprovedBy` (admin username), `ApprovedTime`, `UpdatedBy/Time`; toast "n users approved" |
| `ApproveAll` | same, for every pending user |
| `Reject(int[] ids)` | **deletes** the selected *pending* users only; approved accounts can never be deleted through this endpoint |

- Both the tick list and the confirmation are convenience; the service ignores any id that isn't pending, so a forged request can't delete an approved user.
- **Say it:** "Approval protects the school's records: a stranger can request an account, but nothing works until an admin has checked the student number against the registrar."

## Account lifecycle summary
```
Register (public) ──► Pending (IsApproved=false) ──Approve──► Active ──Deactivate──► Inactive ──Reactivate──► Active
                          └──Reject──► deleted
Admin Create ─────────────────────────► Active (already approved)
```
