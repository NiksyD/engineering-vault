---
title: "Jira Workflow & Enterprise Integration Guide"
tags:
  - guide
  - jira
  - enterprise
  - workflow
  - standup
---

# 🏢 Jira Workflow & Enterprise Integration Guide

> Practical strategy for bridging corporate Jira boards with your local Obsidian vault and autonomous AI agent workflow.

---

## 1. The Enterprise Reality: Why NOT to build a full Jira API bot today

Before your first day at a company, **do not write an automatic Jira API sync script**. Here is why:

1. **Enterprise SSO & Firewalls**: 95% of software companies lock Jira behind Okta, Azure AD, Google Workspace SSO, or a corporate VPN. Personal API tokens are frequently disabled or restricted by corporate IT.
2. **Corporate IP & Compliance Risk**: Your `ObsidianVault` is version-controlled to your personal GitHub (`NiksyD/engineering-vault`). If a script automatically pipes proprietary company tickets, client names, or internal architecture into notes that get pushed to personal GitHub, it violates corporate security and data protection agreements.
3. **Changing Workflows**: Every engineering team customizes Jira statuses differently (`Ready for Dev`, `In Review`, `PO Review`, `Blocked`, `UAT`). Building an API integration beforehand leads to wasted effort.

---

## 2. The "Golden Thread" Pattern (Industry Best Practice)

You do **not** need an API bot to have a seamless Jira workflow. Senior engineers use the **Golden Thread** convention:

```text
Jira Ticket Key (e.g. UCJ-104 or PAY-402)
       │
       ├── Obsidian Note:  `10 - Projects/<Project>/Tickets/<KEY>-<slug>.md`
       ├── Git Branch:     `git checkout -b feat/<KEY>-<slug>`
       ├── Commit Message: `feat(<KEY>): implement sorting logic`
       └── Pull Request:   `[<KEY>] Implement sorting logic`
```

### Why this works everywhere:
- **Jira Smart Commits**: When your Git branch or commit contains the ticket key (`PAY-402`), Jira **automatically** links your branches, commits, and GitHub/GitLab PRs directly to the Jira card on the team's sprint board!
- **Zero API tokens required**: Git and GitHub handle the integration on the company server.
- **5-Second Vault Ingestion**:
  1. Open the Jira ticket.
  2. Copy the description / acceptance criteria.
  3. In Obsidian: Create `10 - Projects/<Project>/Tickets/<KEY>.md` from the Ticket Template.
  4. Run `/grill-me` or `/ponytail` with your agent.

---

## 3. Future Implementation: Official Jira CLI (`jira-cli`)

If your future employer provides developer access to Jira API tokens, use the official open-source Atlassian CLI rather than complex custom code:

### Installation
```bash
# Via Go or GitHub release (ankitpokhrel/jira-cli)
go install github.com/ankitpokhrel/jira-cli/cmd/jira@latest
```

### Onboarding Configuration (Run once on work laptop)
```bash
jira init
# Follow prompts: Server URL (e.g. company.atlassian.net), Email, and Corporate API Token
```

### High-Leverage CLI Commands
```bash
# View all tickets assigned to you in the current sprint
jira sprint list --current

# Fetch ticket details directly into an Obsidian note
jira issue view UCJ-104 --plain > "10 - Projects/UCJobs/Tickets/UCJ-104.md"

# Move ticket status directly from your terminal when opening a PR
jira issue move UCJ-104 "In Review"
```

---

## 4. Daily Standup Sync (`standup`)

To eliminate the manual chore of remembering what you did yesterday for morning standup meetings or Slack updates, use the installed `standup` CLI tool:

### Quick Commands
```bash
# Generate today's standup and sync it into 90 - Daily/YYYY-MM-DD.md
standup

# For Monday standups (looks back 3 days across Friday + weekend)
standup --days 3

# Display summary in terminal only without modifying files (ready to copy into Slack/Teams)
standup --print-only
```

### What It Does:
1. Scans your active repositories under `~/Documents/` for non-merge commits authored by you.
2. Filters out automated vault backups and internal tooling noise.
3. Queries `10 - Projects/` for tickets currently marked `status: in-progress`.
4. Writes a clean Markdown summary into today's daily log:
   - `- **Yesterday**`: Grouped by repository with commit messages and short hashes.
   - `- **Today**`: Active tickets currently in progress.
   - `- **Blockers**`: Defaults to `None`.
