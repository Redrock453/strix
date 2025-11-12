#!/bin/bash
# Z.AI Setup Script for Strix
# Automatically configures Strix to use Z.AI API

set -e

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🦉 Strix + Z.AI Configuration"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check if .env exists
if [ -f .env ]; then
    echo "⚠️  .env file already exists!"
    read -p "Overwrite with Z.AI configuration? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ Setup cancelled"
        exit 1
    fi
fi

# Check for Z.AI API key in environment
if [ -n "$ZAI_API_KEY" ]; then
    echo "✅ Found ZAI_API_KEY in environment"
    API_KEY="$ZAI_API_KEY"
elif [ -n "$ANTHROPIC_AUTH_TOKEN" ]; then
    echo "✅ Found ANTHROPIC_AUTH_TOKEN in environment"
    API_KEY="$ANTHROPIC_AUTH_TOKEN"
else
    echo "🔑 Z.AI API Key required"
    echo ""
    echo "Get your API key from: https://z.ai/manage-apikey/apikey-list"
    echo ""
    read -p "Enter your Z.AI API key: " API_KEY
    
    if [ -z "$API_KEY" ]; then
        echo "❌ API key cannot be empty"
        exit 1
    fi
fi

# Create .env file
cat > .env << EOF
# Z.AI API Configuration
ZAI_API_KEY=${API_KEY}
ANTHROPIC_BASE_URL=https://api.z.ai/api/anthropic
ANTHROPIC_API_KEY=${API_KEY}
LLM_API_KEY=${API_KEY}
STRIX_LLM=anthropic/claude-sonnet-4-20250514
STRIX_SANDBOX_MODE=false
API_TIMEOUT_MS=3000000
EOF

echo "✅ .env file created"

# Export variables for current session
export ZAI_API_KEY="$API_KEY"
export ANTHROPIC_BASE_URL="https://api.z.ai/api/anthropic"
export ANTHROPIC_API_KEY="$API_KEY"
export LLM_API_KEY="$API_KEY"
export STRIX_LLM="anthropic/claude-sonnet-4-20250514"

echo "✅ Environment variables exported"

# Add to .bashrc for persistence (optional)
read -p "Add to ~/.bashrc for automatic loading? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # Check if already in bashrc
    if ! grep -q "Z.AI Configuration for Strix" ~/.bashrc; then
        cat >> ~/.bashrc << 'EOF'

# Z.AI Configuration for Strix
export ZAI_API_KEY="${ZAI_API_KEY}"
export ANTHROPIC_BASE_URL="https://api.z.ai/api/anthropic"
export ANTHROPIC_API_KEY="${ZAI_API_KEY}"
export LLM_API_KEY="${ZAI_API_KEY}"
export STRIX_LLM="anthropic/claude-sonnet-4-20250514"
EOF
        echo "✅ Added to ~/.bashrc"
    else
        echo "ℹ️  Already in ~/.bashrc"
    fi
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Z.AI Configuration Complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📚 Configuration:"
echo "   Model: Claude Sonnet 4 (via Z.AI)"
echo "   Base URL: https://api.z.ai/api/anthropic"
echo "   Timeout: 50 minutes"
echo ""
echo "🚀 Ready to run Strix!"
echo ""
echo "Examples:"
echo "  poetry run strix --target ./my-app"
echo "  poetry run strix --target https://github.com/user/repo"
echo "  poetry run strix -n --target https://example.com"
echo ""
echo "📖 Documentation: docs/ZAI_INTEGRATION.md"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
