---
tags: [alliance, mock-defense, pages]
---

# P0 · Page Map and How to Read the Page Notes

Back to [[00 - Index]]

Each page note answers, for every page/action: **who can open it → which controller action → which service method → which data query → what the view shows and which buttons lead where → edge cases → what to say in the defense.**

## Page notes

| Note | Pages / actions covered |
|---|---|
| [[P1 - Account Pages]] | Login, Register, AccessDenied, Sign out, dev Switch account |
| [[P2 - Home Pages]] | `/Home/Index` dashboard (student vs officer/admin), Error, Status |
| [[P3 - Event Pages]] | `/Event/Index`, `/Event/Details`, `/Event/Manage`, Create/Edit form, Delete, ChangeStatus |
| [[P4 - Registration Pages]] | `/Registration/MyEvents`, Register, Cancel, `/Registration/Ticket` |
| [[P5 - Attendance Pages]] | `/Attendance/Index` check-in desk, CheckIn, CheckOut, SetStatus |
| [[P6 - Report Pages]] | `/Report/Index`, `/Report/Event`, CSV exports |
| [[P7 - Organization Pages]] | Organizations list, form, members, add/update/remove member |
| [[P8 - User Pages]] | Users list, create/edit, approvals, toggle active |

## Template used in each section

```
URL · verb · who may open it
Controller action  →  Service method  →  Data query
View: what is displayed, every button/link and where it goes
Rules / edge cases
Say it in the defense
```

## Navigation map (who links where)

```
Login ──► Home/Index ─┬─(student)─► Event/Details ► Registration/Ticket ► (print)
   ▲                  │             Registration/MyEvents ► Ticket / Cancel
   │                  │             Event/Index (browse) ► Event/Details ► Register / Cancel
Register ► Login      │
(pending approval)    └─(officer/admin)► Event/Create ► Event/Details
                                         Event/Manage ► Details / Edit / Report / Delete / Check in
                                         Event/Details ► Attendance/Index ► CheckIn · CheckOut · SetStatus
                                                       ► Report/Event ► ExportEvent (CSV)
                                         Report/Index ► Report/Event · ExportSummary (CSV)
                      (admin only)  ──► Organization/Index ► Members ► Add / Update / Remove
                                        User/Index ► Create / Edit / ToggleActive ► Approvals
```

## Role → pages quick table

| Page | Student | Officer | Admin |
|---|---|---|---|
| Home/Index | ✔ (own passes) | ✔ (own orgs) | ✔ (all) |
| Event/Index, Event/Details | ✔ | ✔ | ✔ |
| Event/Manage, Create, Edit | ✘ | ✔ (own orgs) | ✔ |
| Registration/MyEvents | ✔ only | ✘ (403 → AccessDenied) | ✘ |
| Registration/Ticket, Cancel | owner | org manager | any org |
| Attendance/*, Report/* | ✘ | own orgs | all |
| Organization/*, User/* | ✘ | ✘ | ✔ |

**Defense line:** "A hidden button is never the security. Every page re-checks the role and the organization on the server."
