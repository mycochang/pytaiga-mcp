# Taiga MCP Bridge

## Project Overview

The Taiga MCP Bridge (`mcp-taiga-bridge`) is an integration layer that connects the [Taiga](https://taiga.io/) project management platform with the Model Context Protocol (MCP). It enables AI agents to perform comprehensive project management tasks programmatically, maintaining contextual awareness of the project state.

**Key Features:**
*   **CRUD Operations:** Full support for Projects, Epics, User Stories, Tasks, Issues, and Sprints (Milestones).
*   **Transport Modes:** Supports both `stdio` (for CLI/local agents) and `sse` (Server-Sent Events) for web-based clients.
*   **Authentication:** Auto-authentication via environment variables or manual session management via MCP tools.
*   **Security:** Credential protection in logs and allowlist-based parameter validation.
*   **Context Management:** Configurable response verbosity (`minimal`, `standard`, `full`) to optimize token usage.

**Architecture:**
*   **Server:** Built with `mcp.server.fastmcp.FastMCP`.
*   **Client:** Uses `pytaigaclient` to interact with the Taiga API.
*   **Config:** Pydantic-based configuration handling environment variables (`.env`).

## Building and Running

The project uses [uv](https://github.com/astral-sh/uv) for fast Python package management.

### Installation

**Prerequisites:** Python 3.10+ and `uv`.

```bash
# Basic installation
./install.sh

# Development installation (includes test dependencies)
./install.sh --dev

# Manual installation via uv
uv pip install -e .
```

### Running the Server

**Standard Mode (stdio):**
```bash
./run.sh
# OR
uv run python src/server.py
```

**SSE Mode:**
```bash
./run.sh --sse
# OR
uv run python src/server.py --sse
```

### Configuration

Create a `.env` file in the project root:
```env
TAIGA_API_URL=https://api.taiga.io/api/v1/
TAIGA_USERNAME=your_username
TAIGA_PASSWORD=your_password
TAIGA_TRANSPORT=stdio
LOG_LEVEL=INFO
```

## Testing

The project uses `pytest` for testing.

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test types (markers defined in pyproject.toml)
pytest -m unit
pytest -m integration
```

### Debugging

Use the provided inspection script:
```bash
./inspect.sh
```

## Development Conventions

*   **Language:** Python 3.10+
*   **Linting:** `ruff` (configuration in `pyproject.toml`).
*   **Type Hinting:** `mypy` is used for type checking.
*   **Commit Messages:** Clear and descriptive messages.
*   **Testing:** New features must include tests.
    *   **Unit Tests:** `tests/test_server.py`
    *   **Integration Tests:** `tests/test_integration.py`
*   **Logging:** Use the configured logger (`logger = logging.getLogger(__name__)`). Ensure no credentials are logged.

## Known Issues / Environment Context

*   **Corrupted Projects:** Project IDs **9** ("Cybersecurity and Network Infrastructure") and **11** ("Arbor Insight ERP & Wiki") are corrupted stubs. They trigger `500 DataError` (invalid JSON) on write operations.
    *   **Action:** Treat these as read-only or ignore them until further notice.
    *   **Fix:** A Taiga Issue (#9) has been filed in "Project FOSS" to track this.
