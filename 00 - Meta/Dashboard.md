---
tags:
  - dashboard
---

# Engineering Workspace

### Active Sprint Tickets

```dataview
TABLE status AS "Status", project AS "Project", priority AS "Priority", dateformat(file.mtime, "yyyy-MM-dd HH:mm") AS "Updated"
FROM "10 - Projects"
WHERE status != "done" AND status != "archived" AND !contains(file.path, "Templates")
SORT choice(status = "in-progress", 1, choice(status = "code-review", 2, choice(status = "todo", 3, 4))) asc, file.mtime desc
```

---

### In Review & QA

```dataview
TABLE status AS "Status", project AS "Project", dateformat(file.mtime, "yyyy-MM-dd HH:mm") AS "Updated"
FROM "10 - Projects"
WHERE (status = "code-review" OR status = "merged" OR status = "in-qa-testing" OR status = "ready-for-testing") AND !contains(file.path, "Templates")
SORT file.mtime desc
```

---

### Recent Logs

```dataview
TABLE dateformat(file.mtime, "yyyy-MM-dd HH:mm") AS "Last Modified"
FROM "90 - Daily"
SORT file.name desc
LIMIT 5
```

---

### Navigation & Reference

- [[00 - Meta/Templates/Ticket Template|Ticket Template]]
- [[00 - Meta/Vault Architecture & Directory Guide|Vault Architecture Guide]]
- [[20 - Areas/AI & Workflows/Agent Setup & Installation Guide|AI Agent Setup & Skills]]
- [[30 - Resources/CodeGraphs|Codebase Knowledge Graphs]]
