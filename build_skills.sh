#!/bin/bash
# Rebuilds the .skill packages from the source directories
# Usage: ./build_skills.sh

SKILL_CREATOR_PATH="/home/arborinisght/.nvm/versions/node/v24.11.0/lib/node_modules/@google/gemini-cli/node_modules/@google/gemini-cli-core/dist/src/skills/builtin/skill-creator/scripts/package_skill.cjs"

echo "Building git-safe-workflow..."
node "$SKILL_CREATOR_PATH" skills/git-safe-workflow skills

echo "Building taiga-manager..."
node "$SKILL_CREATOR_PATH" skills/taiga-manager skills

echo "Done! .skill files are in skills/ (and ignored by git)"
