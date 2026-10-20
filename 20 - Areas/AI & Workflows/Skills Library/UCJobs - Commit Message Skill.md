---
name: ucjobs-commit-message
description: Generate one clean Conventional Commit message and non-technical bullet summary from current UCJobs changes without staging, committing, or pushing.
---

# Generate a UCJobs Commit Message

Review the current change set and produce one recommended Conventional Commit message matching UCJobs repository standards. This skill is advisory only: never run \`git add\`, \`git commit\`, or \`git push\` automatically.

## Workflow

1. Inspect \`git status\` and the relevant diff in the application repository.
2. Identify the primary user-visible or architectural purpose of the change.
3. Choose the most accurate Conventional Commit type:
   - \`feat\`: adds a user-facing capability (e.g. candidate filters, application status tracker).
   - \`fix\`: corrects broken or unexpected behavior.
   - \`chore\`: maintenance, configuration, dependencies, or tooling.
   - \`refactor\`: changes internal structure without changing behavior.
   - \`docs\`: documentation-only changes.
   - \`test\`: test-only changes (Vitest / Testing Library).
   - \`style\`: formatting or presentation-only changes.
   - \`perf\`: improves performance without changing intended behavior.
   - \`ci\`: continuous-integration / build changes.
4. Write a concise subject in imperative mood, lowercase type, omit trailing period.
5. Summarize the outcome in short, non-technical bullet points describing benefits to users or developers.
6. If the change set contains unrelated work, warn that changes should be split before committing.

## Required Output

Return exactly this structure:

\`\`\`text
<type>: <short imperative subject>

- <plain-language outcome or user benefit>
- <plain-language secondary outcome>
\`\`\`
