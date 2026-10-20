---
name: ucjobs-standards-implement
description: Implement features, bug fixes, or UI changes strictly according to UCJobs design, React 19, Next.js 16, and Vitest standards.
---

# Implement to UCJobs Standards

Treat the user's request as the implementation specification. Deliver the requested behavior completely while keeping existing functionality, responsive behavior, accessibility, and visual styling intact.

## Definition of Done

An implementation in \`ucjobs-web\` is complete only when all of the following are true:

1. **Exact changed-file set identified**: Only edit files directly related to the task. Unrelated cleanups or formatting of other files are strictly forbidden.
2. **Architecture & Stack Compliance**:
   - **Framework**: Next.js 16 App Router & React 19 standards.
   - **State**: Zustand for global state (\`zustand\`), React local state for UI state.
   - **Styling**: Tailwind CSS v4, Lucide icons (\`lucide-react\`).
   - **UI Standards**: Respect existing \`web-design-guidelines\` and \`components/ui\` design tokens.
3. **Type & Lint Checks**:
   - Run \`npm run type-check\` (\`tsc --noEmit\`) — zero TypeScript errors allowed.
   - Run \`npm run lint\` (\`eslint\`) — zero ESLint errors introduced.
4. **Test Verification**:
   - New logic, utilities, or complex form behaviors have unit/integration tests added using Vitest (\`npm run test:ci\`).
5. **Report & Receipts**:
   - Show the exact command outputs proving that tests and type-checks passed.
   - Never stage (\`git add\`) or commit automatically without user confirmation.
