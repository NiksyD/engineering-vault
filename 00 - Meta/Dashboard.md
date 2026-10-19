---
tags:
  - dashboard
---

# 🚀 Engineering Mission Control

> *"Ship fast, stay organized, document decisions."*

---

## ⚡ Active Tickets & Features

```dataview
TABLE status AS "Status", project AS "Project", priority AS "Priority", file.mtime AS "Updated"
FROM "10 - Projects"
WHERE status != "done" AND file.name != "Templates"
SORT file.mtime desc
```

---

## 📅 Recent Daily Logs

```dataview
TABLE file.mtime AS "Last Touched"
FROM "90 - Daily"
SORT file.name desc
LIMIT 5
```

---

## 🔗 Quick Links
- [[00 - Meta/Templates/Ticket Template|New Ticket Template]]
- [[20 - Areas/Frontend|Frontend Guidelines]]
- [[20 - Areas/Backend|Backend Guidelines]]
- [[30 - Resources/CodeGraphs|Codebase Knowledge Graphs]]
