#!/bin/bash
# 🚀 Start Day Protocol
# Usage: ./scripts/start_day.sh

# 1. Health Check
echo "🩺 Running System Health Check..."
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
"$DIR/healthcheck.sh"

# 2. Sync Hint
echo ""
echo "🔄 To Sync Tasks:"
echo "   Run: opencode run 'Sync Taiga and Super Productivity'"

echo ""
echo "✅ Ready to Build."
