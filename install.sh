#!/bin/bash
# Yatori USDC Request Skill Installer
# Usage: curl -sSL https://yatori.io/agents/yatori-usdc-request-skill/install.sh | bash

set -e

SKILL_NAME="skill-yatori-usdc-request"
SKILL_DIR="$HOME/.openclaw/skills/$SKILL_NAME"
BASE_URL="https://yatori.io/agents/yatori-usdc-request-skill"

echo "📦 Installing Yatori USDC Request Skill..."
echo ""

# Create skill directory
mkdir -p "$SKILL_DIR"

# Download skill files
echo "⬇️  Downloading skill files..."
curl -sSL "$BASE_URL/skill.py" -o "$SKILL_DIR/skill.py"
curl -sSL "$BASE_URL/SKILL.md" -o "$SKILL_DIR/SKILL.md"

# Create __init__.py
cat > "$SKILL_DIR/__init__.py" << 'EOF'
"""Yatori USDC Request Skill"""
from .skill import create_payment_link, create_payment_link_with_tracking

__version__ = "1.0.0"
__all__ = ["create_payment_link", "create_payment_link_with_tracking"]
EOF

echo "✅ Yatori USDC Request Skill installed!"
echo ""
echo "📍 Location: $SKILL_DIR"
echo ""
echo "🚀 Quick Start:"
echo "   from skill import create_payment_link"
echo "   link = create_payment_link(recipient='ADDRESS', amount=5.0)"
echo ""
echo "📚 Documentation: $SKILL_DIR/SKILL.md"
