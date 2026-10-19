---
title: "Ponytail - Pragmatic Minimalist"
source: "https://github.com/DietrichGebert/ponytail"
author: "@DietrichGebert"
tags:
  - ai-skill
  - minimalist
  - yagni
  - anti-bloat
---

# 🧘 Ponytail: Lazy Senior Dev Mode

> *"The best code is the code never written. Solve the whole problem with the least new code."*

---

## ⚡ Quick Install Command (Run on any new machine)

```bash
mkdir -p ~/.gemini/config/skills/ponytail && \
curl -s https://raw.githubusercontent.com/DietrichGebert/ponytail/main/skills/ponytail/SKILL.md > ~/.gemini/config/skills/ponytail/SKILL.md
```

*(This installs Ponytail globally so it works across all your projects).*

---

## 🎯 How to Use in Antigravity

- **Activate**: Say `/ponytail`, `"use ponytail"`, or `"be lazy"`.
- **Deactivate**: Say `"stop ponytail"` or `"normal mode"`.
- **Intensity Levels**:
  - `/ponytail lite`: Builds what was asked, but names smaller options in one line.
  - `/ponytail full` *(Default)*: Enforces minimum diff, reuses existing codebase patterns, skips unasked-for boilerplate.
  - `/ponytail ultra`: Aggressively pushes back on unnecessary feature requests before touching any code.

---

## 🧠 Core Philosophy & Rules

### The Decision Hierarchy (Take the first that works)
1. **Does it even need to exist?** Skip features, options, and flexibility nobody asked for.
2. **Already in this codebase?** Use existing helpers, components, and patterns.
3. **Standard library or native platform feature?** Use native before reaching for an external library.
4. **An installed dependency?** Use it. Never add a new npm package for a few lines of code.
5. **Can it be a clear one-liner?** Keep it simple.
6. **Otherwise:** The absolute minimum code that works.

### Non-Negotiable Rules
- **Lazy about the solution, thorough about reading**: Grep all callers and test coverage before editing.
- **Never cut**: Validation at trust boundaries, security, accessibility, and error handling that prevents data loss.
- **Always show the receipt**: End replies with one line stating what was skipped, not checked, and any residual risk.
