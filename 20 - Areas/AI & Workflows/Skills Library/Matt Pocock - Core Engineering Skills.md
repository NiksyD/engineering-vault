---
title: "Matt Pocock Skills (Grill-Me, Diagnosing Bugs, To-Tickets)"
source: "https://github.com/mattpocock/skills"
author: "@mattpocock (Matt Pocock / AI Hero)"
tags:
  - ai-skill
  - engineering
  - debugging
  - specs
---

# 🎓 Matt Pocock: Core Intern-to-Senior Skills

> Pragmatic, high-discipline engineering skills that force AI agents to interview you, diagnose bugs surgically, and break specs into bite-sized tickets.

---

## ⚡ Quick Install Command (Run on any new machine)

```bash
mkdir -p ~/.gemini/config/skills/grill-me ~/.gemini/config/skills/diagnosing-bugs ~/.gemini/config/skills/to-tickets && \
curl -s https://raw.githubusercontent.com/mattpocock/skills/main/skills/engineering/grill-with-docs/SKILL.md > ~/.gemini/config/skills/grill-me/SKILL.md && \
curl -s https://raw.githubusercontent.com/mattpocock/skills/main/skills/engineering/diagnosing-bugs/SKILL.md > ~/.gemini/config/skills/diagnosing-bugs/SKILL.md && \
curl -s https://raw.githubusercontent.com/mattpocock/skills/main/skills/engineering/to-tickets/SKILL.md > ~/.gemini/config/skills/to-tickets/SKILL.md
```

---

## 🎯 How to Use Each Skill

### 1. `/grill-me` — The Requirement Interviewer
- **When to use**: Whenever you get a new ticket or feature request, before writing any code.
- **Trigger**: Say `/grill-me` or `"grill me on this feature"`.
- **What it does**: Conducts an intense Socratic interview to uncover missing edge cases, architectural trade-offs, and implicit assumptions.

### 2. `/diagnosing-bugs` — Surgical Debugging
- **When to use**: Whenever an error throws, a test fails, or something acts unexpectedly.
- **Trigger**: Say `/diagnosing-bugs`, `"diagnose this bug"`, or `"debug this"`.
- **What it does**: 
  1. Builds a tight pass/fail reproduction feedback loop.
  2. Isolates the exact line/root cause.
  3. Recommends the minimal single-file fix (no reckless shotgun editing).

### 3. `/to-tickets` — Automated Ticket Generator
- **When to use**: After discussing a feature or drafting a spec.
- **Trigger**: Say `/to-tickets`.
- **What it does**: Breaks down the discussion into vertical slice tickets with blocking dependencies, ready to paste into `10 - Projects/Tickets/`.
