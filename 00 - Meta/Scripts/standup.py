#!/usr/bin/env python3
"""
Standup Generator & Obsidian Daily Log Sync
Extracts recent git commits across active workspaces and syncs them into Obsidian's 90 - Daily log.
"""

import os
import sys
import argparse
import subprocess
import datetime
import re
from pathlib import Path

# Dynamically resolve vault location from script location (00 - Meta/Scripts/standup.py -> ObsidianVault)
VAULT_DIR = Path(__file__).resolve().parents[2]
if not (VAULT_DIR / "90 - Daily").exists():
    VAULT_DIR = Path.home() / "Documents/ObsidianVault"

DAILY_DIR = VAULT_DIR / "90 - Daily"
PROJECTS_DIR = VAULT_DIR / "10 - Projects"
DOCS_DIR = VAULT_DIR.parent

# Ignore commits matching these substrings
IGNORED_COMMIT_PATTERNS = [
    "vault backup:",
    "Merge branch",
    "Merge pull request",
    "first commit",
    "Initial commit"
]

def find_git_repos(base_dir: Path, max_depth: int = 3):
    """Find git repositories in base_dir up to max_depth."""
    repos = []
    for root, dirs, files in os.walk(base_dir):
        depth = len(Path(root).relative_to(base_dir).parts)
        if depth > max_depth:
            dirs.clear()
            continue
        if ".git" in dirs:
            repos.append(Path(root))
            dirs.remove(".git")  # don't recurse into .git
    return sorted(repos)

def get_recent_commits(repo_path: Path, days: int, author: str = None):
    """Get commits from a repository in the last N days."""
    cmd = [
        "git", "-C", str(repo_path), "log",
        f"--since={days}.days",
        "--pretty=format:%h|%an|%s",
        "--no-merges"
    ]
    if author:
        cmd.append(f"--author={author}")
    
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        raw_lines = res.stdout.strip().split("\n")
        commits = []
        for line in raw_lines:
            if not line:
                continue
            parts = line.split("|", 2)
            if len(parts) == 3:
                commit_hash, commit_author, subject = parts
                # Filter out automated or noisy commits
                if any(pat.lower() in subject.lower() for pat in IGNORED_COMMIT_PATTERNS):
                    continue
                commits.append((commit_hash, subject.strip()))
        return commits
    except Exception:
        return []

def get_active_tickets():
    """Scan 10 - Projects for notes with status: in-progress."""
    active = []
    if not PROJECTS_DIR.exists():
        return active
    for root, _, files in os.walk(PROJECTS_DIR):
        for f in files:
            if f.endswith(".md"):
                p = Path(root) / f
                try:
                    content = p.read_text(encoding="utf-8")
                    if re.search(r"^status:\s*in-progress\b", content, re.MULTILINE):
                        title_match = re.search(r"^title:\s*[\"']?(.*?)[\"']?$", content, re.MULTILINE)
                        title = title_match.group(1) if title_match else p.stem
                        project_match = re.search(r"^project:\s*[\"']?(.*?)[\"']?$", content, re.MULTILINE)
                        proj = project_match.group(1) if project_match else ""
                        active.append((p.stem, title, proj))
                except Exception:
                    pass
    return active

def generate_standup_text(repo_commits, active_tickets):
    """Generate Markdown standup summary."""
    yesterday_lines = []
    if repo_commits:
        for repo_name, commits in repo_commits.items():
            yesterday_lines.append(f"  - **{repo_name}**:")
            for chash, msg in commits:
                yesterday_lines.append(f"    - {msg} (`{chash}`)")
    else:
        yesterday_lines.append("  - (No commits found in lookback window)")

    today_lines = []
    if active_tickets:
        for stem, title, proj in active_tickets:
            proj_str = f"[{proj}] " if proj else ""
            today_lines.append(f"  - Continue {proj_str}[[{stem}|{title}]]")
    else:
        today_lines.append("  - Review backlog and plan next task")

    blocker_lines = ["  - None"]

    output = []
    output.append("- **Yesterday**:")
    output.extend(yesterday_lines)
    output.append("- **Today**:")
    output.extend(today_lines)
    output.append("- **Blockers**:")
    output.extend(blocker_lines)

    return "\n".join(output)

def update_daily_file(daily_file: Path, date_str: str, standup_body: str):
    """Update or create the 90 - Daily/YYYY-MM-DD.md note."""
    if not daily_file.exists():
        content = f"""---
date: "{date_str}"
tags:
  - daily
---

# Daily Log: {date_str}

### Objectives
- [ ] 

---

### Standup Notes
{standup_body}

---

### Scratchpad
- 
"""
        daily_file.write_text(content, encoding="utf-8")
        return True, "Created new daily log"
    
    # If file exists, update only the ### Standup Notes section
    content = daily_file.read_text(encoding="utf-8")
    section_pattern = r"(### Standup Notes\n)(.*?)(?=\n---\n|\Z)"
    new_section = f"\\1{standup_body}\n"
    
    if re.search(section_pattern, content, re.DOTALL):
        updated_content = re.sub(section_pattern, new_section, content, flags=re.DOTALL)
        daily_file.write_text(updated_content, encoding="utf-8")
        return True, "Updated existing Standup Notes section"
    else:
        # If Standup Notes header is missing, append it before Scratchpad or at bottom
        if "### Scratchpad" in content:
            updated_content = content.replace("### Scratchpad", f"### Standup Notes\n{standup_body}\n\n---\n\n### Scratchpad")
        else:
            updated_content = content + f"\n\n### Standup Notes\n{standup_body}\n"
        daily_file.write_text(updated_content, encoding="utf-8")
        return True, "Appended Standup Notes to daily log"

def main():
    parser = argparse.ArgumentParser(description="Git-to-Daily Standup Sync")
    today = datetime.date.today()
    # If today is Monday (weekday 0), default lookback is 3 days to cover Friday-Sunday
    default_days = 3 if today.weekday() == 0 else 1

    # Detect default git author dynamically on any machine
    detected_author = None
    try:
        author_proc = subprocess.run(["git", "config", "user.name"], capture_output=True, text=True)
        detected_author = author_proc.stdout.strip() or "NiksyD"
    except Exception:
        detected_author = "NiksyD"

    parser.add_argument("--days", type=int, default=default_days, help=f"Lookback days (default: {default_days})")
    parser.add_argument("--date", type=str, default=today.isoformat(), help="Target daily note date YYYY-MM-DD")
    parser.add_argument("--print-only", action="store_true", help="Print report to terminal without editing file")
    parser.add_argument("--author", type=str, default=detected_author, help=f"Git author filter (default: {detected_author})")
    args = parser.parse_args()

    # Discover git repos
    repos = find_git_repos(DOCS_DIR)
    repo_commits = {}
    for r in repos:
        commits = get_recent_commits(r, days=args.days, author=args.author)
        if commits:
            repo_commits[r.name] = commits

    active_tickets = get_active_tickets()
    standup_text = generate_standup_text(repo_commits, active_tickets)

    # Terminal output
    print(f"\n\033[1;36m=== Standup Report ({args.date} | Past {args.days}d) ===\033[0m")
    print(standup_text)
    print("\033[1;36m" + "="*45 + "\033[0m\n")

    if not args.print_only:
        DAILY_DIR.mkdir(parents=True, exist_ok=True)
        target_file = DAILY_DIR / f"{args.date}.md"
        success, msg = update_daily_file(target_file, args.date, standup_text)
        print(f"\033[1;32m✓ {msg} -> {target_file}\033[0m")

if __name__ == "__main__":
    main()
