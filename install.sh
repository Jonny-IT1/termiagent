#!/usr/bin/env bash
# 🚀 TermiAgent One-Liner Installer (Linux / macOS)
set -e

echo "📦 Installing TermiAgent via uv..."

if ! command -v uv &> /dev/null; then
    echo "Installing uv package manager..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$PATH"
fi

uv tool install termiagent --from . || uv pip install -e .

echo ""
echo "🎉 TermiAgent installation complete!"
echo "Run 'termiagent' in any terminal to start chatting with your codebase."
