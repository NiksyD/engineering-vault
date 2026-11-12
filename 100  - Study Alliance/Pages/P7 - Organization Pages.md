---
tags: [alliance, mock-defense, pages]
---

# P7 · Organization Pages (Admin only)

Index: [[P0 - Page Map and How to Read These]]

Controller: `OrganizationController` (class-level `[Authorize(Roles = "Admin")]`) · Service: `OrganizationService` · Views: `Organization/{Index,Form,Members}.cshtml`

**Why this matters:** organization membership is what gives an Officer their scope ([[01 - System Flow and Architecture#Three layers of authorization]]). To make someone a working officer an Admin must (1) set the user's **Role = Officer** ([[P8 - User Pages]]) **and** (2) **add them as a member** of the organization here. A Student added as a member still can't manage events, because `CanManageOrganization` requires the Officer role.

---

## 1. List: `GET /Organization/Index?search=`
- `GetOrganizations(search)`: filter by name or acronym (case-insensitive), ordered by name, with `MemberCount` and `EventCount` computed in SQL.
- **View:** **New organization** button; search box; table: organization (name link → Members, acronym, description), adviser, member count, event count, Active/Inactive badge, and row actions **Members** → `Organization/Members/{id}`, **Edit** → `Organization/Edit/{id}`, **Delete** (trash; shown only when `EventCount == 0`, with confirm "its member list is removed too").

## 2. Create / Edit: `GET|POST /Organization/Create`, `GET|POST /Organization/Edit/{id}`
- **View `Form.cshtml`:** Name (required), Acronym, Adviser, Description, **Active** checkbox ("officers can create events for it"); button text switches between create and save.
- **POST** → model validation → `CreateOrganization` / `UpdateOrganization`:
  - `EnsureNameAvailable`: the name must be unique (case-insensitive, ignoring the record itself on edit) → `OrganizationExists`, shown at the top of the form;
  - audit fields (`CreatedBy`, `UpdatedBy`, times) are set.
- Success → toast and back to the list.
- **Effect of Inactive:** `GetManagedOrganizationOptions` only offers *active* organizations, so officers can't create new events for an inactive one (existing events remain).

## 3. Delete: `POST /Organization/Delete/{id}`
- Service refuses if the organization **has any events** (`OrganizationHasEvents`); the database also blocks it (`DeleteBehavior.Restrict`). Otherwise deletes the organization and, by cascade, its membership rows.

## 4. Members page: `GET /Organization/Members/{id}`
- `GetMembers(id)` returns the organization, its members (name, username/student number, **role badge**, position, joined date, ordered by name) and `AvailableUsers` (active and approved users who are **not already members**).
- **View:** left card **Add a member** (user dropdown, optional Position, max 50 chars); right table of members.

## 5. Member actions (all POST + CSRF, redirect back to the Members page)
| Endpoint | Rule |
|---|---|
| `AddMember(organizationId, memberId, position)` | organization must exist, user must exist, not already a member (`AlreadyMember`; unique index also guards it); blank position becomes **"Member"** |
| `UpdateMember(id, organizationId, position)` | updates the position text (blank → "Member") |
| `RemoveMember(id)` | deletes the membership; the officer immediately loses scope over that organization for **new requests** (but see the session note in [[05 - Code Review - Strengths, Risks, Limitations]] item 7: role claims in the cookie stay until it expires) |

- **Say it:** "Organization membership, not the role alone, defines what an officer can touch. Remove the membership and the officer can no longer manage that organization's events, because every service call re-reads the memberships from the database."
