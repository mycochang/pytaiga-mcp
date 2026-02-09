---
name: git-safe-workflow
description: Enforces safety checks before code modifications - git status/fetch/pull, implication analysis, and prerequisite verification. Use when planning code changes.
---

# Git Safe Workflow

This skill enforces a disciplined, safety-first workflow for software engineering tasks. It requires checking the environment state and analyzing implications *before* making changes.

## Workflow

Follow these steps in order before modifying code.

### 1. Environment Assessment (The "O" in OODA)

Before planning fixes, you must understand the current state of the repository.

1.  **Check Local Status:**
    ```bash
    git status
    ```
    - Are there uncommitted changes?
    - Are you on the correct branch?

2.  **Check Remote Status:**
    ```bash
    git fetch --all
    git branch -vv
    ```
    - Are you behind `origin`?
    - Are there upstream changes that might conflict?
    - **Rule:** If behind, pull (rebase preferred) before starting work, unless specifically debugging a detached state.

### 2. Implication Analysis (The "O" in OODA)

Before writing code, pause and analyze:

1.  **Dependencies:** Does this change affect other files? (Use `grep` or `search_file_content` to find usages).
2.  **Conflicts:** Does the `git fetch` reveal recent changes to the same files?
3.  **Prerequisites:** Do existing tests pass? Is the build currently broken?
    - *If the build is already broken, fix that first or acknowledge it.*

### 3. Execution (The "D" and "A" in OODA)

Only after the above are satisfied:

1.  **Plan:** State your plan clearly.
2.  **Act:** Create/Modify files.
3.  **Verify:** Run tests (`pytest`, `npm test`, etc.).

## Best Practices

- **Never code in the dark:** Always know if `origin/main` has moved.
- **Respect the branch:** Don't push directly to protected branches (like `master` or `main`) if you are a guest. Create a feature branch.
- **Atomic Commits:** Keep fixes focused.