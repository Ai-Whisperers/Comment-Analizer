#!/bin/bash
# Architecture Map Git Hooks Installer
# Purpose: Set up automatic map updates on git events

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HOOKS_DIR="${PROJECT_ROOT}/.git/hooks"
SCRIPTS_DIR="${PROJECT_ROOT}/scripts"

echo "🔧 INSTALLING ARCHITECTURE MAP GIT HOOKS"
echo "=========================================="
echo "Project root: ${PROJECT_ROOT}"
echo "Hooks directory: ${HOOKS_DIR}"

# Verify git repository
if [ ! -d "${PROJECT_ROOT}/.git" ]; then
    echo "❌ Error: Not a git repository"
    exit 1
fi

# Verify scripts exist
if [ ! -f "${SCRIPTS_DIR}/update_architecture_map.py" ]; then
    echo "❌ Error: update_architecture_map.py not found"
    exit 1
fi

if [ ! -f "${SCRIPTS_DIR}/cleanup_old_architecture_docs.py" ]; then
    echo "❌ Error: cleanup_old_architecture_docs.py not found"
    exit 1
fi

# Make scripts executable
echo "📝 Making scripts executable..."
chmod +x "${SCRIPTS_DIR}/update_architecture_map.py"
chmod +x "${SCRIPTS_DIR}/cleanup_old_architecture_docs.py"

# Install post-commit hook (map updates)
echo "🔄 Installing post-commit hook..."
cat > "${HOOKS_DIR}/post-commit" << 'EOF'
#!/bin/bash
# Auto-update architecture map after commits
# Triggered: After successful commit
# Purpose: Keep map synchronized with code changes

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)/scripts"

# Only update map if source files changed
CHANGED_FILES=$(git diff --name-only HEAD~1 HEAD)

# Check if any architecture-relevant files changed
if echo "$CHANGED_FILES" | grep -qE "(^src/|^pages/|^streamlit_app\.py|^static/)" ; then
    echo "🤖 Architecture files changed, updating map..."
    
    # Run map update (non-interactive)
    python3 "${SCRIPT_DIR}/update_architecture_map.py" --execute
    
    if [ $? -eq 0 ]; then
        echo "✅ Architecture map updated successfully"
    else
        echo "⚠️ Architecture map update failed (non-fatal)"
    fi
else
    echo "ℹ️ No architecture files changed, skipping map update"
fi
EOF

# Install pre-push hook (validation & cleanup)
echo "🚀 Installing pre-push hook..."
cat > "${HOOKS_DIR}/pre-push" << 'EOF'
#!/bin/bash
# Validate architecture before push
# Triggered: Before git push
# Purpose: Ensure map accuracy and clean up old docs

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)/scripts"

echo "🔍 Pre-push validation: Architecture map"

# Check if useful architecture map exists
MAP_FILE="${SCRIPT_DIR}/../local-reports/useful_architecture_map.md"
if [ ! -f "$MAP_FILE" ]; then
    echo "❌ Error: useful_architecture_map.md not found"
    echo "💡 Run: python3 scripts/update_architecture_map.py --execute"
    exit 1
fi

# Validate map is not empty
if [ ! -s "$MAP_FILE" ]; then
    echo "❌ Error: Architecture map is empty"
    exit 1
fi

# Check for old graph documentation (prevent confusion)
OLD_GRAPH_FILES=(
    "docs/arquitectura/00_Master_Graph_Navigation.md"
    "docs/arquitectura/Hierarchical_Graph_System_Design.md"
    "docs/arquitectura/Interactive_Graph_Explorer.md"
    "docs/arquitectura/Complete_Vertex_Inventory.md"
    "docs/arquitectura/subgraphs/"
)

OLD_FILES_EXIST=false
for file in "${OLD_GRAPH_FILES[@]}"; do
    if [ -e "${SCRIPT_DIR}/../${file}" ]; then
        echo "⚠️ Warning: Old graph documentation exists: $file"
        OLD_FILES_EXIST=true
    fi
done

if [ "$OLD_FILES_EXIST" = true ]; then
    echo "🧹 Old documentation detected. Run cleanup:"
    echo "   python3 scripts/cleanup_old_architecture_docs.py --execute"
    echo ""
    echo "❓ Push anyway? [y/N]"
    read -r response
    case "$response" in 
        [yY][eE][sS]|[yY])
            echo "✅ Continuing with push..."
            ;;
        *)
            echo "❌ Push cancelled. Clean up old docs first."
            exit 1
            ;;
    esac
fi

echo "✅ Pre-push validation passed"
EOF

# Make hooks executable
chmod +x "${HOOKS_DIR}/post-commit"
chmod +x "${HOOKS_DIR}/pre-push"

# Create hook management script
echo "🔧 Creating hook management script..."
cat > "${SCRIPTS_DIR}/manage_hooks.sh" << 'EOF'
#!/bin/bash
# Git Hooks Management Script

HOOKS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/.git/hooks"

case "$1" in
    status)
        echo "📊 Git Hooks Status:"
        echo "==================="
        for hook in post-commit pre-push; do
            if [ -x "${HOOKS_DIR}/${hook}" ]; then
                echo "✅ ${hook}: Active"
            else
                echo "❌ ${hook}: Inactive"
            fi
        done
        ;;
    disable)
        echo "🔇 Disabling architecture hooks..."
        mv "${HOOKS_DIR}/post-commit" "${HOOKS_DIR}/post-commit.disabled" 2>/dev/null || true
        mv "${HOOKS_DIR}/pre-push" "${HOOKS_DIR}/pre-push.disabled" 2>/dev/null || true
        echo "✅ Hooks disabled"
        ;;
    enable)
        echo "🔊 Enabling architecture hooks..."
        mv "${HOOKS_DIR}/post-commit.disabled" "${HOOKS_DIR}/post-commit" 2>/dev/null || true
        mv "${HOOKS_DIR}/pre-push.disabled" "${HOOKS_DIR}/pre-push" 2>/dev/null || true
        chmod +x "${HOOKS_DIR}/post-commit" "${HOOKS_DIR}/pre-push" 2>/dev/null || true
        echo "✅ Hooks enabled"
        ;;
    test)
        echo "🧪 Testing hooks..."
        echo "Testing map update..."
        python3 "$(dirname "$0")/update_architecture_map.py" --dry-run
        echo "✅ Test complete"
        ;;
    *)
        echo "Usage: $0 {status|enable|disable|test}"
        echo ""
        echo "Commands:"
        echo "  status  - Show hook status"
        echo "  enable  - Enable architecture hooks"
        echo "  disable - Disable architecture hooks" 
        echo "  test    - Test hook functionality"
        exit 1
        ;;
esac
EOF

chmod +x "${SCRIPTS_DIR}/manage_hooks.sh"

# Summary
echo ""
echo "✅ INSTALLATION COMPLETE"
echo "========================"
echo "Installed hooks:"
echo "  📝 post-commit  → Auto-update architecture map"  
echo "  🚀 pre-push     → Validate map & check for old docs"
echo ""
echo "Management:"
echo "  📊 Status:  scripts/manage_hooks.sh status"
echo "  🔇 Disable: scripts/manage_hooks.sh disable"
echo "  🔊 Enable:  scripts/manage_hooks.sh enable"
echo "  🧪 Test:    scripts/manage_hooks.sh test"
echo ""
echo "🎯 Your architecture map will now stay synchronized automatically!"
echo "🤖 Zero tokens required for maintenance!"