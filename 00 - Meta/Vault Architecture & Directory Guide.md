---
title: Vault Architecture & Directory Guide
tags:
  - meta
  - guide
  - architecture
---

# Vault Architecture & Directory Guide

> The engineering principles, directory responsibilities, and operational workflows governing this knowledge vault.

---

## 1. Directory Structure & Responsibilities

### `00 - Meta` — Workspace Control & Configuration
- **Purpose**: System-level configuration, templates, and entry points.
- **Contents**:
  - `Dashboard.md`: Pinned mission control displaying active tickets, recent logs, and key links.
  - `Templates/`: Standard templates for tickets, daily standups, and ADRs.
  - `System/`: Property seed notes to anchor status values in Obsidian's index.
  - Operational guides and setup documentation.

### `10 - Projects` — Active Work with Deadlines
- **Purpose**: Initiatives, sprint tickets, and features that have a concrete end state.
- **Rule of Thumb**: Once an item is finished, merged, or closed, it moves to `40 - Archive`.
- **Subdirectory Roles**:
  - `Tickets/`: Individual sprint-sized tasks (e.g., bug fixes, UI adjustments, isolated API endpoints). Stored here while in-progress and tracked on the dashboard.
  - `Features/`: Multi-ticket product specifications, PRDs, and high-level feature designs before they are broken down into bite-sized tickets.
  - `Spikes/`: Time-boxed technical research or proof-of-concept experiments to evaluate an architecture or library before committing to an implementation.

### `20 - Areas` — Long-Term Craft & Standards (No End Date)
- **Purpose**: Personal engineering standards, domain expertise, and playbooks that stay with you across your entire career.
- **Subdirectory Roles**:
  - `Frontend/`: Framework standards (React, Next.js), state management patterns, and UI/UX design tokens.
  - `Backend/`: API architecture, database design, authentication flows, and migration best practices.
  - `DevOps/`: Containerization recipes, CI/CD pipelines, and deployment workflows.
  - `AI & Workflows/`: Curated agent skills library, prompt engineering patterns, and tool setup guides.

### `30 - Resources` — Reference Material & External Assets
- **Purpose**: Technical assets and external knowledge that you reference while designing or building.
- **Subdirectory Roles**:
  - `Architecture/`: High-level system design diagrams, ERDs, sequence diagrams, and API contracts.
  - `Snippets/`: Reusable TypeScript utility types, complex SQL queries, and shell scripts.
  - `CodeGraphs/`: Dedicated home for Graphify codebase knowledge graph exports (connected via local symlinks).

### `40 - Archive` — Cold Storage
- **Purpose**: Completed, deprecated, or superseded materials kept for audit and historical reference.
- **Subdirectory Roles**:
  - `Completed Tickets/`: Shipped tickets moved out of `10 - Projects` to maintain a clean, distraction-free workspace.
  - `Deprecated Designs/`: Obsolete technical specifications and retired experiments.

### `90 - Daily` — Working Memory & Calendar Logs
- **Purpose**: Day-to-day operational logs generated automatically from the Calendar widget.
- **Format**: `YYYY-MM-DD.md` (e.g. `2026-10-20.md`).
- **Contents**: Standup thoughts, immediate blockers, temporary console dumps, and links to active tickets.

---

## 2. Standard Ticket Lifecycle

```text
[Receive Requirement / Jira Ticket]
                │
                ▼
1. Create note in `10 - Projects/<Project>/Tickets/<ID>.md` (from Ticket Template)
2. Ask AI to plan implementation using `/ponytail` or `/grill-me`
3. Execute and verify tests locally
4. Generate commit message with commit-message skill
5. Mark `status: done` and move note to `40 - Archive/Completed Tickets/`
```

---

## 3. Codebase Knowledge Graphs (`CodeGraphs/`)

`CodeGraphs/` connects your external codebase AST extraction (via Graphify) directly into Obsidian without bloating your Git vault repository.

### How Symlinks Connect Codebases to the Vault (Local Only)
Because `30 - Resources/CodeGraphs/` is ignored in `.gitignore`, symlinks are created per-machine on local disk:

```bash
# Connect any codebase's Graphify export to your vault:
ln -s /path/to/<project>/graphify-out/obsidian /path/to/ObsidianVault/30\ -\ Resources/CodeGraphs/<ProjectName>
```

### Updating a Codebase Graph
When code changes in a repository:
```bash
cd /path/to/<project>
graphify update .            # Fast incremental scan of changed code
graphify export obsidian     # Updates markdown nodes; instantly visible in Obsidian
```

---

## 4. Tooling & Plugin Map

| Plugin | Primary Function |
|---|---|
| **Dataview** | Drives dynamic tables in `Dashboard.md` by querying note metadata (`status`, `project`, `file.mtime`). |
| **Templater** | Injects dynamic dates and titles into notes from `00 - Meta/Templates/`. |
| **Calendar** | Visual monthly calendar in bottom-right pane; clicks generate daily notes in `90 - Daily/`. |
| **Git** | Automated version control; auto-commits and pushes to remote GitHub repository. |
| **Tasks** | Aggregates `- [ ]` markdown checkboxes across all project notes. |
| **Advanced Tables** | Automatically aligns and formats markdown table columns. |
| **Omnisearch** | High-performance search engine with fuzzy matching, text indexing, and PDF/file deep search. |
| **Recent Files** | Fast sidebar navigation tracking recently opened and edited notes for zero context-switching friction. |
| **Sort & Permute lines** | Text-manipulation utility to alphabetically sort, deduplicate, and reverse lines or list items. |
