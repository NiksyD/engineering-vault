---
tags: [alliance, mock-defense, study-guide]
project: Student Org Event Registration and Attendance System
stack: ASP.NET Core MVC · Razor · .NET 9 · EF Core · SQL Server
---

# Mock Defense Study Guide: Student Org Events

**Repo:** `Alliance_Dynamo/Dynamo/ASIBasecodeCsharp` (built on the ASI Bridge/JumpStart C# BaseCode)
**One-line pitch:** Student organizations publish events, students register (auto-waitlist when full), officers take attendance by scanning each student's QR ticket, and admins read reports.

## Read in this order

1. [[01 - System Flow and Architecture]] — layers, request lifecycle, auth, roles, dependency injection
2. [[02 - Endpoint Map (GET and POST)]] — every route, verb, role, and what it calls
3. [[03 - Major Flows Code Walkthrough]] — the code panelists will ask about (check-in, register/waitlist, lifecycle, login, approvals)
4. [[04 - Data Model]] — tables, relationships, constraints, enums
5. [[05 - Code Review - Strengths, Risks, Limitations]] — honest self-review so you are not surprised
6. [[06 - Defense Q&A Cheat Sheet]] — likely questions with short answers
7. [[07 - Front End, Views and Helpers]] — Razor views, site.js (pagination, confirm, validation helpers), small helpers, seed SQL

> **Updated after pulling main:** course eligibility, overlap prevention and a locked registration transaction now exist. See [[08 - Niko Student Demo Trace]]. Older notes (01–07, P1–P8) predate this pull; where they say "no course restriction" or "race on the last seat", they are outdated.

8. [[08 - Niko Student Demo Trace]] — student-side demo flow and how to trace the code

## Page-by-page notes (every page, its buttons, its service and query)

Start at [[P0 - Page Map and How to Read These]], then: [[P1 - Account Pages]] · [[P2 - Home Pages]] · [[P3 - Event Pages]] · [[P4 - Registration Pages]] · [[P5 - Attendance Pages]] · [[P6 - Report Pages]] · [[P7 - Organization Pages]] · [[P8 - User Pages]]

Companion file: `ASIBasecodeCsharp/.docs/Study-Guide-Functions-and-Code.pdf` (58 pages, function-by-function with line numbers; its line numbers can drift as the code changes, so confirm against the source).

## 60-second summary (memorize this)

- **3 roles:** Admin (everything), Officer (only organizations they are a member of), Student (browse, register, ticket).
- **Layers:** WebApp (controllers + Razor views) → Services (all business rules) → Data (EF Core repositories) → SQL Server. A fourth project, Resources, holds constants, enums and message text.
- **Event lifecycle:** `Draft → Open → Closed → Completed`, or `Cancelled`. Students never see drafts.
- **Registration:** Only while the event is Open, before the deadline, before the start. If `Capacity > 0` and full, the student is **Waitlisted**. A cancellation promotes the oldest waitlisted student automatically.
- **Check-in:** Officer scans the QR (or types the 10-character code or student number). The browser POSTs via fetch to `Attendance/CheckIn`, which returns JSON. Late is `now > StartTime + LateAfterMinutes`.
- **Completing an event** marks every registered student with no attendance row as **Absent**.
- **Security model:** global login requirement + `[Authorize(Roles=…)]` + service-level `EnsureCanManageOrganization` (so officer scope is enforced even if the controller attribute is satisfied) + `[ValidateAntiForgeryToken]` on state-changing POSTs.
- **Business-rule errors** are exceptions thrown by services; `ServiceExceptionFilter` turns them into a toast (or JSON for AJAX) instead of an error page.

## Demo accounts (from the README)

| Username | Password | Role |
|---|---|---|
| `admin` | `Admin@123` | Admin |
| `msantos` | `Officer@123` | Officer (President, Computer Science Society) |
| `jreyes` | `Officer@123` | Officer (Governor, Engineering Student Council) |
| `student1` … `student6` | `Student@123` | Student |

In the `Development` environment a "Switch account" button signs you in as any active user without a password (returns 404 elsewhere).

## Demo script idea (5 minutes)

1. Sign in as `student1` → browse events → register → see QR ticket (`Registration/Ticket`).
2. Fill an event to capacity with other students → show the waitlist → cancel one → show the automatic promotion.
3. Sign in as `msantos` → open the event's attendance desk → scan/type the code → show the Present/Late result card.
4. Mark the event **Completed** → no-shows become Absent → open the Report → export CSV.
5. Sign in as `admin` → approve a self-registered student (`User/Approvals`).
