# Engineering Vault

> Local-first second brain, AI agent orchestration hub, and sprint cockpit for software engineering.

---

## The Philosophy

> "The best code is the code never written. The best notes are the ones you actually use."

This repository is a structured, production-ready Obsidian engineering vault designed to bridge **human architectural thinking** with **autonomous AI coding agents** (Antigravity, Claude Code, Codex).

- **Zero Cloud Lock-In**: 100% plain-text Markdown (`.md`) backed up via Git.
- **AI-Agent Native**: Direct disk access for agents without proprietary cloud APIs or browser extensions.
- **Sprint Aligned**: Mirrors real Jira / Linear sprint boards (`todo` -> `in-progress` -> `code-review` -> `merged` -> `in-qa-testing` -> `done`).
- **Token Efficient**: Deep context lives in notes; only sharp, high-leverage instructions are passed to agents to eliminate context window bloat.

---

## Scaffolding & Architecture

Built on an adapted **Johnny.Decimal + PARA** taxonomy for high-velocity software engineering:

```text
ObsidianVault/
├── 00 - Meta/               # System configuration, templates, and mission control
│   ├── System/              # Property seed notes (sprint status definitions)
│   ├── Templates/           # Standard templates (Ticket Template, Daily Log Template)
│   ├── Dashboard.md         # Auto-updating Mission Control (Dataview SQL)
│   └── Vault Architecture Guide # Comprehensive system reference
│
├── 10 - Projects/           # Active initiatives with defined end goals
│   └── <ProjectName>/
│       ├── Tickets/         # Active sprint tickets with specs & plans
│       ├── Features/        # High-level PRDs & multi-ticket specs
│       └── Spikes/          # Time-boxed technical research & POCs
│
├── 20 - Areas/              # Lifelong engineering craft (No end date)
│   ├── Frontend/            # React 19, Next.js 16, UI/UX tokens, state patterns
│   ├── Backend/             # API design, Go Chi/Fiber, Supabase, RLS policies
│   ├── DevOps/              # Docker multi-stage builds, Render, Vercel pipelines
│   └── AI & Workflows/      # Curated agent skills library & setup guides
│
├── 30 - Resources/          # Reference assets & external knowledge
│   ├── Architecture/        # System diagrams, ERDs, sequence diagrams, contracts
│   ├── Snippets/            # Reusable TypeScript utility types, SQL triggers, scripts
│   └── CodeGraphs/          # Persistent Graphify codebase knowledge graph exports
│
├── 40 - Archive/            # Cold storage (keeps active workspace clean)
│   ├── Completed Tickets/   # Shipped & merged tickets moved here
│   └── Deprecated Designs/  # Retired specs & obsolete experiments
│
└── 90 - Daily/              # Working memory & scratchpad
    └── YYYY-MM-DD.md        # Standup logs auto-generated from Calendar clicks
```

---

## The Core Intern-to-Senior AI Skill Stack

Curated, high-leverage agent skills installed globally in `~/.gemini/config/skills/` and documented in `20 - Areas/AI & Workflows/`:

| Skill | Author / Source | Role in Workflow | Command |
|---|---|---|---|
| **[Ponytail](https://github.com/DietrichGebert/ponytail)** | Dietrich Gebert | Extreme minimalism, YAGNI, shortest clean diff, no unasked-for bloat | `/ponytail [lite\|full\|ultra]` |
| **[Superpowers](https://github.com/obra/superpowers)** | Jesse Vincent (@obra) | Complete SDLC methodology: Socratic interview, bite-sized plans, TDD | `/superpowers` |
| **Grill-Me** | Matt Pocock | Relentless requirement stress-testing before code is written | `/grill-me` |
| **Diagnosing-Bugs** | Matt Pocock | Tight reproduction loop & surgical root-cause isolation | `/diagnosing-bugs` |
| **To-Tickets** | Matt Pocock | Converts conversation specs into vertical-slice tickets for Obsidian | `/to-tickets` |
| **Commit-Message** | Internal Standard | Generates clean Conventional Commits without staging/pushing | `/<repo>-commit-message` |

---

## Daily Engineering Flow

```text
1. Morning Standup
   - Click today's date in Calendar widget -> Generates 90 - Daily/YYYY-MM-DD.md
   - Dashboard displays active sprint tickets, reviews, and quick links

2. New Ticket Assigned
   - Paste raw criteria into 10 - Projects/<Project>/Tickets/<ID>.md
   - Prompt AI: "Plan implementation using /grill-me and /ponytail"
   - AI writes step-by-step verified plan into ticket note

3. Execution & Verification
   - Prompt AI: "Execute Step 1 of @<ID>.md to <Project> standards"
   - Agent runs type-check (tsc --noEmit), linter (eslint), and tests (vitest)
   - Generate commit using /<project>-commit-message

4. Completion & Archiving
   - Set frontmatter: status: done (Instantly clears from Dashboard)
   - Move note to 40 - Archive/Completed Tickets/
```

---

## 2-Minute Workstation Setup

When cloning onto a new machine or work laptop:

### 1. Clone in One Line
```bash
git clone https://github.com/NiksyD/engineering-vault.git ~/Documents/ObsidianVault
```
*Open Obsidian -> "Open folder as vault" -> select `~/Documents/ObsidianVault`.*

### 2. Install Global AI Skills
```bash
# Superpowers
agy plugin install https://github.com/obra/superpowers

# Ponytail
mkdir -p ~/.gemini/config/skills/ponytail && \
curl -s https://raw.githubusercontent.com/DietrichGebert/ponytail/main/skills/ponytail/SKILL.md > ~/.gemini/config/skills/ponytail/SKILL.md

# Matt Pocock Core Skills
mkdir -p ~/.gemini/config/skills/grill-me ~/.gemini/config/skills/diagnosing-bugs ~/.gemini/config/skills/to-tickets && \
curl -s https://raw.githubusercontent.com/mattpocock/skills/main/skills/engineering/grill-with-docs/SKILL.md > ~/.gemini/config/skills/grill-me/SKILL.md && \
curl -s https://raw.githubusercontent.com/mattpocock/skills/main/skills/engineering/diagnosing-bugs/SKILL.md > ~/.gemini/config/skills/diagnosing-bugs/SKILL.md && \
curl -s https://raw.githubusercontent.com/mattpocock/skills/main/skills/engineering/to-tickets/SKILL.md > ~/.gemini/config/skills/to-tickets/SKILL.md
```

### 3. Activate Standup CLI Tool
Link the standup script to your terminal PATH:
```bash
mkdir -p ~/.local/bin && \
chmod +x ~/Documents/ObsidianVault/00\ -\ Meta/Scripts/standup.py && \
ln -sf ~/Documents/ObsidianVault/00\ -\ Meta/Scripts/standup.py ~/.local/bin/standup
```

---

## Installed Obsidian Plugins

- **Dataview**: SQL-like dynamic tables querying notes by `status`, `project`, and `file.mtime`.
- **Templater**: Dynamic variable injection (`<% tp.file.title %>`, dates) for rapid ticket creation.
- **Calendar**: Interactive monthly grid linked directly to `90 - Daily/`.
- **Obsidian Git**: Automated 15-minute background commits and syncs to GitHub.
- **Tasks**: Vault-wide checklist aggregation.
- **Advanced Tables**: Auto-formatting and keyboard navigation for markdown tables.

---

## License

[MIT](LICENSE). Built for high-leverage software engineering.
