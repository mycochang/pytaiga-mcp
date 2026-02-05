# Agent Knowledge Base & Guide for PyTaiga MCP

This repository implements a Model Context Protocol (MCP) server for Taiga.
**Agents reading this:** Use this guide to *Orient* yourself within the Taiga domain and *Decide* on correct actions.

## 1. Domain Model (Observe)

Understand the hierarchy and relationships of the Taiga system before acting.

*   **Project**: The root container. All work items belong to a project.
    *   **User Story**: A feature/requirement. Can be assigned to a **Milestone** (Sprint).
        *   **Task**: A unit of work derived from a User Story.
    *   **Epic**: A large body of work that groups User Stories.
    *   **Issue**: A defect or bug. **Critical:** Unlike other items, Issues depend on strictly defined metadata (Priority, Severity, Type, Status).
    *   **Wiki**: Documentation pages.

**Key Rule:** All operations use numeric `IDs`, not names or slugs (unless creating a new project).

## 2. Critical Workflows & Dependencies (Orient)

### The "Issue" Workflow (Strict Requirement)
Creating an Issue is **not** a single step. You cannot "guess" IDs for priorities or statuses.
1.  **List Project**: Get the Project ID.
2.  **Fetch Metadata**: You **MUST** fetch these lists first:
    *   `get_issue_priorities(project_id)`
    *   `get_issue_statuses(project_id)`
    *   `get_issue_types(project_id)`
    *   `get_issue_severities(project_id)`
3.  **Create Issue**: Use the IDs obtained from step 2.

### The Standard OODA Loop for Agents

1.  **Observe**: Gather context. Example: User asks "Add a login feature".
2.  **Orient**: Map to Domain Model. Login = User Story. Project ID needed.
3.  **Decide**:
    *   **Weigh Options**: Should this be one story or an Epic? Is the context clear?
    *   **Uncertainty Check**: If requirements are vague, **ASK** the user.
    *   **Plan**: If the task is complex (e.g., "Setup the whole project"), **PROPOSE** a plan *before* acting.
    *   **Coaching Constraint**: For User Stories, **ALWAYS** ask coaching questions to ensure quality:
        *   "Who is this for?" (Persona)
        *   "What is the benefit?" (Value)
        *   "How do we know it's done?" (Acceptance Criteria)
4.  **Act**: Execute the agreed plan.
    *   **User Story Template**: Ensure descriptions follow: *"As a [Role], I want [Feature] so that [Benefit]."*

### Naming Conventions
*   **Priorities**: Use `/priorities` endpoint (internal implementation detail: fixed in server).
*   **Severities**: Use `/severities` endpoint.

## 3. Agile Philosophy & Strategic Context (Why)

As an Agile Coach and Agent, you must understand **WHY** work is being done. We follow the OKR/KPI framework to link execution to strategy.

### OKRs (Objectives and Key Results)
*   **Purpose:** Set ambitious, strategic goals. The "North Star".
*   **Structure:** *"I will [Objective] as measured by [Key Results]."*
*   **Mapping to Taiga:**
    *   **Objective** → **Epic**: A high-level, often cross-cutting goal (e.g., "Harmonize MCP Fleet").
    *   **Key Result** → **User Story**: A measurable step or deliverable that proves the objective was met (e.g., "Verify PyTaiga MCP Phase 3").

### KPIs (Key Performance Indicators)
*   **Purpose:** Monitor health and performance of ongoing processes. The "Pulse Check".
*   **Examples:** Velocity, Lead Time, Bug Count.
*   **Usage:** Use these to flag risks during the "Decide" phase. If velocity is low, propose simpler stories.

### The "Golden Thread" Rule
Every **Task** must support a **User Story**.
Every **User Story** must support an **Epic** (Objective).
If you cannot trace a Task to a Strategic Objective, **ASK** the user for context before acting.

## 4. Reference Implementation (Act)

If you are unsure how to sequence tools for a complex task (e.g., "Manage an Epic lifecycle"), **read the code** in `verify_tools.py`.

*   **File:** `verify_tools.py`
*   **Purpose:** This script contains the *canonical* sequence of operations for every supported resource. It is the "Gold Standard" for how to use this MCP server.
*   **Action:** If asked to verify the system, run `.venv/bin/python verify_tools.py`.

## 5. Development Commands

### Environment Setup
- **Package Manager:** `uv` is used.
- **Install Dependencies:** `./install.sh` (or `uv sync` if available).
- **Virtual Env:** Activates from `.venv/bin/activate`.

### Testing
- **Run Verification Skill:** `.venv/bin/python verify_tools.py` (Best way to test "does it work?")
- **Run Unit Tests:** `./run_unit_tests.sh` or `pytest`
- **Run Integration Tests:** `./run_integration_tests.sh` (requires active Taiga instance)

### Linting & Formatting
- **Linter:** `ruff` is configured in `pyproject.toml`.
- **Command:** `ruff check .`

## 6. Code Style & Conventions

*   **Source:** `src/` (Server: `src/server.py`, Config: `src/config.py`).
*   **Typing:** Mandatory type hints.
*   **Error Handling:** Catch `TaigaException`. Log errors before raising.
*   **MCP Tools:** Use `@mcp.tool`. Use `_get_session_id`. Support `verbosity`.

## 7. Available Tools Reference

Refer to `src/server.py` for the definitive list.

*   **Project Management:** `list_projects`, `get_project`, `create_project`, `update_project`, `delete_project`.
*   **User Stories:** `list_user_stories`, `get_user_story`, `create_user_story`, `update_user_story`, `delete_user_story`.
*   **Tasks:** `list_tasks`, `create_task`...
*   **Issues:** `list_issues`, `create_issue` (Requires metadata!), `get_issue_priorities`...
*   **Epics:** `list_epics`, `create_epic`...
*   **Wiki:** `list_wiki_pages`...

## 8. Adaptation & Learning

*   **Goal:** Continually refine this guide based on usage.
*   **Target:** Review and adapt this `AGENTS.md` by EoW 09.02.2026 to better match user preferences.
*   **Feedback Loop:** If a planned action fails or the user corrects the agent, note the correction and consider if it requires a rule update here.

## 9. MCP Deployment Standards
Guidelines for configuring MCP servers to ensure cross-agent compatibility.

### 🛠️ OpenCode Interpreter
*   **Path:** `~/.config/opencode/opencode.json`
*   **Schema (FLAT):** Servers must be direct children of the `"mcp"` key.
*   **Example:**
    ```json
    {
      "mcp": {
        "my-server": {
          "type": "local",
          "command": ["uv", "run", "server.py"],
          "enabled": true
        }
      }
    }
    ```
*   **⚠️ WARNING:** Never nest under `mcp.servers`. This will cause an "Invalid input mcp.servers" error.

### 🛠️ Gemini CLI
*   **Path:** `~/.gemini/settings.json`
*   **Schema:** Servers are listed under the `"mcpServers"` key.
*   **Example:**
    ```json
    {
      "mcpServers": {
        "my-server": {
          "command": "uv",
          "args": ["run", "server.py"]
        }
      }
    }
    ```

### 📋 Setup SOP
1.  **Check existing config:** `opencode mcp list` or `cat <path>`.
2.  **Verify launch command:** Run the `command` + `args` in a terminal first.
3.  **Inject config:** Use a script or `replace` to merge the server config.
4.  **Confirm:** Run `opencode mcp list` to ensure status is `✓ connected`.

---

## 10. User Story Templates (Agile Standards)

### Option A: Standard Agile (Value Focus)
```markdown
**As a** <Role>
**I want** <Action/Goal>
**So that** <Benefit/Value>

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
```

### Option B: Jobs To Be Done (Context Focus)
*Best for complex workflows or situational triggers.*
```markdown
**When I** <Situation/Trigger>
**I want to** <Motivation/Job>
**So that I can** <Expected Outcome>

## Acceptance Criteria
- [ ] Criterion 1
```

**Title Rule:** User Story titles must be concise and action-oriented. **NEVER** use "As a..." in the title - that goes in the description.

---

## 11. Estimation Heuristics (Fibonacci Scale)

| Points | Complexity | AI Time Estimate |
|--------|------------|------------------|
| **1** | Trivial (typos, config) | ~10 mins |
| **2** | Simple (standard function/test) | ~30 mins |
| **3** | Moderate (component/integration) | ~1-2 hours |
| **5** | Solid Feature | Day (human) / Morning (AI) |
| **8** | Complex Feature | Significant logic |
| **13** | **AI Sweet Spot** | Large context, full module |
| **20** | Very Large | One "Deep Dive" session |
| **40** | Epic Size | Consider splitting |
| **100** | TOO BIG | Mandatory split |

**Philosophy:** Prioritize **low context switching** over small batches. A 13-20pt "Fat Story" in one coherent session is often more efficient than 10 tiny tasks.

### Role-Based Points (Granular Estimation)
Assign points per skill domain, not just total effort:
*   **Front/Back:** Hard Coding
*   **UX/Design:** Visuals & Flows
*   **Client:** Emotional Labor, Negotiation
*   **Ops:** Admin, Logistics, Data Processing

**API Syntax:** Use `update_user_story` with `kwargs`:
```python
"points": {"<Role_ID>": <Point_ID>}
```
*Role and Point IDs are project-specific. Query your Taiga instance or check local config.*

---

## 12. Taiga Visual Standard (Optional)

Use emojis in **User Story Titles** (prefix) for quick visual scanning:

| Category | Emoji | Meaning |
|----------|-------|---------|
| **Type** | ✨ | Feature (New Value) |
| | 🐛 | Bug (Broken Value) |
| | 🔧 | Chore/Debt (Enabling Work) |
| | 📚 | Docs/Research (Knowledge) |
| **Priority** | 🔥 | Urgent / Blocker |
| | 📅 | Deadline Driven |
| **Status** | 🚧 | WIP (In Progress) |
| | 🧪 | QA / Testing |
| | ✅ | Done / Verified |

---

## 13. Extended OODA Protocol

### 1. Observe (Input)
*   Read the user's prompt.
*   Identify core intent and constraints.

### 2. Orient (Context)
*   **Action:** Search files, check Taiga, grep codebase.
*   **Stop Rule:** If context is missing (file not found, ambiguous reference), **STOP immediately**.
    *   Do not hallucinate.
    *   Do not guess.
    *   Ask: "I cannot find [Context]. Did you mean [Alternative]?"

### 3. Decide (Plan)
*   Formulate strategy based on context.
*   Draft options (Option A vs B) when ambiguous.
*   For complex tasks, **PROPOSE** before acting.

### 4. Act (Execute)
*   Call the tools.
*   Verify the output.
*   Mark tasks complete.

---

## 14. Private Configuration

For project-specific IDs, client names, and internal mappings, check:
*   **Local file:** `.arbor_config.md` (gitignored)
*   **Memory MCP:** Query entities with type `CompanyContext`
