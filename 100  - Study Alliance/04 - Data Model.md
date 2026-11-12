---
tags: [alliance, mock-defense, database]
---

# 04 · Data Model

Back to [[00 - Index]] · Previous: [[03 - Major Flows Code Walkthrough]] · Next: [[05 - Code Review - Strengths, Risks, Limitations]]

Files: `ASI.Basecode.Data/Models/*.cs`, `ASI.Basecode.Data/AsiBasecodeDbContext.cs`, schema + demo data in `Database/student_event_db.sql`. Table/column names are snake_case via `UseSnakeCaseNamingConvention()`. All `DateTime` columns are `datetime2`, and the app stores **local time** (`DateTime.Now`).

## ER diagram

```
users 1───< organization_members >───1 organizations
  │                                        │
  │ 1                                      │ 1
  ▼ *                                      ▼ *
event_registrations >───1 events ──────────┘
  │ 1
  ▼ 0..1
attendances
```

## Tables

| Table | Key columns | Constraints / notes |
|---|---|---|
| `users` | `id`, `user_id` (username), first/middle/last/`name`, `email`, `student_number`, `course`, `year_level`, `role`, `is_active`, `is_approved`, `approved_by/time`, `password`, audit cols | Unique `user_id` and unique `student_number`. `role` stored as a string (`Admin/Officer/Student`). |
| `organizations` | `id`, `name`, `acronym`, `description`, `adviser`, `is_active`, audit cols | Unique `name`. Cannot be deleted while it has events (FK `Restrict`). |
| `organization_members` | `id`, `organization_id`, `member_id`, `position`, `joined_time` | **Unique (organization_id, member_id).** Cascade delete from both sides. This table defines an officer's scope. |
| `events` | `id`, `organization_id`, `title`, `description`, `venue`, `start_time`, `end_time`, `registration_deadline`, `capacity`, `late_after_minutes`, `status`, audit cols | Index on `start_time`. `capacity = 0` means unlimited. `status` stored as string. |
| `event_registrations` | `id`, `event_id`, `student_id`, `registration_code`, `status`, `registered_time`, `cancelled_time` | **Unique (event_id, student_id)** and **unique `registration_code`**. Cascade from events and users. |
| `attendances` | `id`, `registration_id`, `check_in_time`, `check_out_time`, `status`, `remarks`, `recorded_by`, `recorded_time` | **Unique `registration_id`** (at most one attendance per registration, i.e. a one-to-one). Cascade from registration. |

## Enums (`Resources/Constants/Enums.cs`, stored as strings via `HasConversion<string>()`)

| Enum | Values |
|---|---|
| `Role` | Admin, Officer, Student |
| `EventStatus` | Draft, Open, Closed, Completed, Cancelled |
| `RegistrationStatus` | Registered, Waitlisted, Cancelled |
| `AttendanceStatus` | Present, Late, Absent |
| `LoginResult` | Success, Failed, Inactive, Pending |

## Why these constraints matter (defense talking points)

- **One registration per student per event** is enforced twice: the service checks it and the unique index guarantees it. That's why re-registering after a cancellation *reuses* the row.
- **One attendance per registration** is enforced by the unique index, so a double check-in cannot create duplicates even if the service check were bypassed.
- **Unique `registration_code`** + generation loop → a code identifies exactly one registration.
- **Cascade vs Restrict:** deleting an event cascades to its registrations and attendances (but the service refuses to delete an event that has registrations); deleting an organization with events is blocked at the database level (`Restrict`).
- **Waitlist** has no separate table: it is a status on `event_registrations`, ordered by `registered_time`.
- **Audit columns** (`created_by/time`, `updated_by/time`, `recorded_by/time`, `approved_by/time`) record who did what.

## Demo data / deployment
- `Database/student_event_db.sql` creates the database and seeds demo organizations, events and accounts; re-running resets everything.
- Hosted deployment: `Database/build_hosted_script.ps1` generates `student_event_db.hosted.sql` (no `CREATE DATABASE`/`USE`) and a **new random secret key**, re-encrypting the demo passwords for that key. Production settings come from environment variables: `ConnectionStrings__DefaultConnection`, `TokenAuthentication__SecretKey`, `ASPNETCORE_ENVIRONMENT=Production`.
- If `SecretKey` changes, every stored password stops working (the key is the AES key).

## Entity ↔ view model mapping
`Startup.AutoMapper.cs`: `UserViewModel→User`, `UserModel↔User` (ignores `Id`, `Password`, `Name`, approval fields), `OrganizationViewModel↔Organization`, `EventViewModel→Event` (**ignores `Id`, `Status`, `Organization`**). Those ignores are deliberate guard rails against over-posting (a client can't change status or ID by adding form fields).
