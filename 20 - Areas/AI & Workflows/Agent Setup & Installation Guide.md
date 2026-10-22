---
title: "Workstation AI Agent Setup Guide"
tags:
  - setup
  - workstation
  - ai-tools
  - devops
---

# 💻 Workstation AI Agent Setup Guide

> Use this one-stop checklist whenever setting up a new computer, work laptop, or internship machine.

---

## 🚀 1. Essential Global Skills & Plugins

Run these terminal commands to set up the core AI tools:

### A. Superpowers (Methodology, TDD & Planning)
```bash
agy plugin install https://github.com/obra/superpowers
```

### B. Ponytail (Pragmatic Minimalist & Anti-Bloat)
```bash
mkdir -p ~/.gemini/config/skills/ponytail && \
curl -s https://raw.githubusercontent.com/DietrichGebert/ponytail/main/skills/ponytail/SKILL.md > ~/.gemini/config/skills/ponytail/SKILL.md
```

---

## 📚 2. Installed Skills Catalog

| Skill | Purpose | Activation Command |
|---|---|---|
| **[[Superpowers - Engineering Methodology\|Superpowers]]** | Structured planning, TDD tests, specs, subagent execution | `agy` automatically loads or invoke `/superpowers` |
| **[[Ponytail - Pragmatic Minimalist\|Ponytail]]** | "Lazy senior dev" mode — minimal working diffs, zero bloat | `/ponytail` or say `"be lazy"` |

---

## 🗂️ 3. Restoring Your Knowledge, Tools & Rules

- **Obsidian Vault**: Clone or sync this `ObsidianVault` repository to `~/Documents/ObsidianVault`.
- **Activate Standup Tool**:
  ```bash
  mkdir -p ~/.local/bin && \
  chmod +x ~/Documents/ObsidianVault/00\ -\ Meta/Scripts/standup.py && \
  ln -sf ~/Documents/ObsidianVault/00\ -\ Meta/Scripts/standup.py ~/.local/bin/standup
  ```
- **Global Rules Bridge (Optional)**: If you want Antigravity to always read your core rules file:
  ```bash
  ln -s ~/Documents/ObsidianVault/20\ -\ Areas/Agent-Rules.md ~/.gemini/config/rules/obsidian-agent-rules.md
  ```
