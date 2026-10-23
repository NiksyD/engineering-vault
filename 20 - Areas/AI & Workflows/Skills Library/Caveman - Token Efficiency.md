---
title: "Caveman - Token Efficiency & Terse Mode"
source: "https://github.com/JuliusBrussee/caveman"
author: "@JuliusBrussee"
tags:
  - ai-skill
  - token-saving
  - efficiency
  - concise
---

# 🪨 Caveman: Token-Saving & Terse Output

> *"why many token when few do trick. Code stay exact. Brain still big."*

---

## ⚡ Quick Install Command (Run on any new machine)

```bash
mkdir -p ~/.gemini/config/skills/caveman ~/.gemini/config/skills/ultracave && \
curl -s https://raw.githubusercontent.com/JuliusBrussee/caveman/main/skills/caveman/SKILL.md > ~/.gemini/config/skills/caveman/SKILL.md && \
curl -s https://raw.githubusercontent.com/JuliusBrussee/caveman/main/skills/ultracave/SKILL.md > ~/.gemini/config/skills/ultracave/SKILL.md
```

*(Installs Caveman and Ultracave globally in Antigravity as pure skills without invasive background proxy daemons).*

---

## 🎯 How to Use in Antigravity

- **Activate Caveman**: Say `/caveman`, `"caveman mode"`, or `"talk like caveman"`.
- **Activate Ultracave (Maximum Compression)**: Say `/ultracave` or `/caveman ultra`.
- **Check Status**: Say `/caveman status`.
- **Deactivate**: Say `"stop caveman"` or `"normal mode"`.

---

## 🧠 Core Philosophy & Rules

1. **Answer First**: Pattern is `[thing] [action] [reason]. [next step].` No greetings or recaps.
2. **Kill Ceremony**: No hedging, pleasantries, "Sure!", or "I'll now".
3. **Payload Verbatim**: Code, commands, paths, and error messages are untouched character-for-character.
4. **Articles Optional, Meaning Never**: Drop filler words, but *never* drop `not`, `never`, `no`, `only`, `except`. Units and numbers stay exact.
5. **One Idea Per Sentence**: Based on ASD-STE100 technical standard (20 words max, active voice).
6. **No Theater**: No "me think" or caricature behavior. If caveman phrasing isn't shorter, plain English wins.

### When Rules Break (Full Sentences Resume)
- Security warnings and irreversible actions (always confirmed in full sentences).
- Clarifying questions with selectable options.
- Content persisted outside chat (commits, PR descriptions, documentation).
