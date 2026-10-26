#!/bin/sh
# Copies the ronson. brand agents into ~/.claude/agents so every project can use them.
#   sh brand/install-agents.sh            (from a clone)
#   curl -fsSL https://lironson.github.io/brand/install-agents.sh | sh
set -eu

dest="${HOME}/.claude/agents"
base="https://raw.githubusercontent.com/lironson/lironson.github.io/main/.claude/agents"
here="$(cd "$(dirname "$0")" 2>/dev/null && pwd || true)"

mkdir -p "$dest"
for a in brand-guardian brand-designer brand-apply; do
  src="${here}/../.claude/agents/${a}.md"
  if [ -n "$here" ] && [ -f "$src" ]; then
    cp "$src" "$dest/${a}.md"
  else
    curl -fsSL "${base}/${a}.md" -o "$dest/${a}.md"
  fi
  echo "installed ${a}"
done
