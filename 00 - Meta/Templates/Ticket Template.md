<%*
const statuses = ["todo", "in-progress", "code-review", "merged", "in-qa-testing", "done"];
const status = await tp.system.suggester(statuses, statuses, false, "Status");
tR += `---
title: "${tp.file.title}"
status: ${status ?? "todo"}
priority: medium
created: ${tp.file.creation_date("YYYY-MM-DD HH:mm")}
tags:
  - ticket
  - dev
---`;
%>

# <% tp.file.title %>

## Problem & Context
> Concise description of the issue or requirement.

### Acceptance Criteria
- [ ] 

---

## Technical Architecture
- Target Module: 
- Affected Files: 
- Dependencies: 

---

## Implementation Plan
1. 
2. 
3. 

---

## Verification
- [ ] Type check passes (`npm run type-check`)
- [ ] Linter passes (`npm run lint`)
- [ ] Tests pass (`npm run test:ci`)
