#!/bin/bash
# MCP Health Check Script
# Verifies that all required MCP servers are configured and enabled.

echo "🔍 Checking MCP Server Configuration..."

# 1. Check OpenCode Config
CONFIG_FILE="$HOME/.config/opencode/opencode.json"
if [ -f "$CONFIG_FILE" ]; then
    echo "✅ OpenCode config found: $CONFIG_FILE"
    
    # Check for specific servers
    grep -q "super-productivity" "$CONFIG_FILE" && echo "  - super-productivity: Configured" || echo "  ❌ super-productivity: MISSING"
    grep -q "taiga" "$CONFIG_FILE" && echo "  - taiga: Configured" || echo "  ❌ taiga: MISSING"
    grep -q "github" "$CONFIG_FILE" && echo "  - github: Configured" || echo "  ❌ github: MISSING"
    grep -q "brave-search" "$CONFIG_FILE" && echo "  - brave-search: Configured" || echo "  ❌ brave-search: MISSING"
else
    echo "❌ OpenCode config NOT found!"
fi

echo ""
echo "🔍 Checking Dependencies..."
# 2. Check Docker (for GitHub)
if command -v docker &> /dev/null; then
    echo "✅ Docker is installed (Required for GitHub MCP)"
    if docker ps &> /dev/null; then
        echo "  - Docker Daemon is running"
    else
        echo "  ❌ Docker Daemon is NOT running"
    fi
else
    echo "❌ Docker is NOT installed"
fi

# 3. Check UV (for Python servers)
if command -v uv &> /dev/null; then
    echo "✅ uv is installed"
else
    echo "❌ uv is NOT installed"
fi

echo ""
echo "🔍 Current Status (via OpenCode CLI)..."
# 4. Run OpenCode List
if command -v opencode &> /dev/null; then
    opencode mcp list
else
    echo "⚠️ 'opencode' CLI not found in PATH. Cannot verify live connection status."
fi

echo ""
echo "📋 To apply changes: Restart OpenCode or run 'Reload MCP Servers'"
