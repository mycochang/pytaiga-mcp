---
name: taiga-manager
description: Intelligent orchestration of Taiga project management. Handles daily standups, sprint planning, health checks, and backlog hygiene using OODA loops. Adapts to project context via memory or dynamic discovery.
---

# Taiga Manager

This skill transforms individual Taiga tool calls into cohesive, intelligent workflows. It implements the OODA loop (Observe-Orient-Decide-Act) for project management and abstracts specific project details to remain adaptable.

## Core Principle: Dynamic Context
Do not assume Project IDs or names. Always **Orient** first by:
1.  Checking active context (Memory/Config).
2.  Listing available projects.
3.  Asking the user if ambiguous.

## Workflows

### 1. The Daily Standup (Status Report)
**Trigger:** "What's the status?", "Daily standup", "Show me active work"

1.  **Observe:**
    *   `list_projects(verbosity="minimal")`
    *   Identify the target project. *Strategy: If multiple exist, ask "Which project?" or check memory for `active_project_id`.*
2.  **Orient:**
    *   `list_milestones(project_id)` -> Find the *active* sprint (check start/finish dates against today).
    *   `list_user_stories(project_id, filters={"status__is_closed": False})` -> Get in-flight items.
3.  **Decide:**
    *   **Blockers:** Filter for `is_blocked=True`.
    *   **Risks:** Identify high-priority items not yet in progress.
4.  **Act:**
    *   Report: "Active Sprint: [Name]. Blocked Items: [List]. Attention Needed: [List]."

### 2. The Doctor (Health Check)
**Trigger:** "Check project health", "Why is Taiga failing?", "Verify integrity"

1.  **Observe:**
    *   `list_projects(verbosity="standard")`
    *   *Consult Memory:* Check if any projects are flagged as `corrupted` or `read_only` in agent memory.
2.  **Act (Safety Protocol):**
    *   Iterate through projects.
    *   **Skip Known Bad Projects:** If memory indicates a project ID is corrupted (e.g., custom attribute JSON errors), skip write operations for it.
    *   **Verify Read:** `get_project(id)` for each.
    *   **Verify Write (Dry Run):** Check if metadata (like `userstory_custom_attributes`) is accessible.
3.  **Report:**
    *   "Healthy Projects: [List]"
    *   "Issues Found: [List with IDs and error details]"

### 3. Sprint Planning (Backlog Refinement)
**Trigger:** "Plan the next sprint", "Refine backlog"

1.  **Orient:**
    *   Get the project ID (ask or infer).
    *   `list_user_stories(project_id, filters={"milestone": None, "status__is_closed": False})` (The Backlog).
2.  **Decide:**
    *   **Hygiene Check:** Identify stories missing **Points**, **Tags**, or **Acceptance Criteria**.
    *   *Heuristic:* A story without points cannot be planned.
3.  **Act (Coaching):**
    *   Present unrefined stories: "These X items need estimation."
    *   If user estimates, use `update_user_story` to set points.
    *   *Standard:* Use the project's specific Point IDs (fetch `get_project` to map "3 points" -> `point_id`).

### 4. The Golden Thread (Strategic Alignment)
**Trigger:** "Create a task for...", "Add a feature"

1.  **Orient:**
    *   **Hierarchy Check:** Task -> Story -> Epic.
2.  **Decide:**
    *   If the request is a "Task" (e.g., "Fix the login button"), look for a parent User Story.
    *   If no parent exists, **PROPOSE** creating the User Story first.
    *   *Anti-Pattern:* Do not create "Orphan Tasks" (Tasks without User Stories) unless the project explicitly supports it (Kanban mode).
3.  **Act:**
    *   `create_user_story` (Use `update_project` with `.edit()`/PATCH semantics if updating metadata).
    *   `create_task` linked to that story.

## Known Constraints (Memory Injection)

*   **Corrupted Projects:** If you encounter 500 errors on specific projects (e.g., JSON syntax errors), **Save this fact to memory** (`save_memory`).
    *   *Fact Format:* "Taiga Project ID [ID] has corrupted custom attributes. Treat as Read-Only."
*   **API Quirks:**
    *   **Updates:** Always use partial updates (PATCH/edit) for Projects.
    *   **Issues:** Creating Issues requires strict metadata IDs (Priority, Severity, Status, Type). Fetch these lists before creating.
