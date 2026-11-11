---
title: "<% tp.file.title %>"
status: <% await tp.system.suggester(["todo","in-progress","code-review","merged","in-qa-testing","done"], ["todo","in-progress","code-review","merged","in-qa-testing","done"], false, "Status") %>
priority: medium
created: <% tp.file.creation_date("YYYY-MM-DD HH:mm") %>
tags:
  - ticket
  - dev
# Status options: todo | in-progress | code-review | merged | in-qa-testing | done
---

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
