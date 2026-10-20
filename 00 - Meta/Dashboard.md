---
tags:
  - dashboard
---

# Engineering Workspace

### Active Tickets & Tasks

```dataview
TABLE status AS "Status", project AS "Project", priority AS "Priority", dateformat(file.mtime, "yyyy-MM-dd HH:mm") AS "Updated"
FROM "10 - Projects"
WHERE status != "done" AND file.name != "Templates" AND !contains(file.path, "Templates")
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
- [[20 - Areas/AI & Workflows/Agent Setup & Installation Guide|AI Agent Setup & Skills]]
- [[20 - Areas/Frontend|Frontend Standards]]
- [[20 - Areas/Backend|Backend Architecture]]
- [[30 - Resources/CodeGraphs|Codebase Knowledge Graphs]]
