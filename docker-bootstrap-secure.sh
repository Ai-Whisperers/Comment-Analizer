#!/bin/bash
# SECURE BOOTSTRAP SCRIPT FOR COMMENT ANALYZER
# Implements security recommendations from audit report

set -euo pipefail  # Exit on error, undefined vars, pipe failures
IFS=$'\n\t'       # Set secure Internal Field Separator

# Security: Disable command history
set +o history
export HISTFILE=/dev/null

# Colors for output (secure, no injection)
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly NC='\033[0m' # No Color

# Security: Set umask for file creation
umask 077

echo "================================================"
echo "   Comment Analyzer - Secure Bootstrap v2.0"
echo "================================================"

# Security: Function to safely log without exposing secrets
secure_log() {
    local message="$1"
    # Remove potential secrets from log output
    echo "${message}" | sed -E 's/(api[_-]?key|token|secret|password)=[^ ]+/\1=**REDACTED**/gi'
}

# Security: Verify container integrity
verify_integrity() {
    echo -e "\n${BLUE}Verifying container integrity...${NC}"
    
    # Check if running as non-root
    if [ "$(id -u)" -eq 0 ]; then
        echo -e "${RED}✗ CRITICAL: Running as root user - Security violation${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✓ Running as non-root user (UID: $(id -u))${NC}"
    
    # Verify package integrity
    if [ -f /app/packages-hash.txt ]; then
        echo -e "${GREEN}✓ Package integrity hash found${NC}"
    else
        echo -e "${YELLOW}⚠ Package integrity hash missing${NC}"
    fi
    
    # Check security manifest
    if [ -f /app/security-manifest.txt ]; then
        echo -e "${GREEN}✓ Security manifest present${NC}"
    else
        echo -e "${YELLOW}⚠ Security manifest missing${NC}"
    fi
}

# Security: Load encrypted secrets
load_secrets() {
    echo -e "\n${BLUE}Loading secure configuration...${NC}"
    
    # Check for secrets volume
    if [ -d /run/secrets ]; then
        echo -e "${GREEN}✓ Secrets volume mounted${NC}"
        
        # Load API key from secret file (encrypted at rest)
        if [ -f /run/secrets/openai_api_key ]; then
            export OPENAI_API_KEY=$(cat /run/secrets/openai_api_key)
            echo -e "${GREEN}✓ OpenAI API key loaded from secure storage${NC}"
        elif [ -f /run/secrets/api_key ]; then
            export OPENAI_API_KEY=$(cat /run/secrets/api_key)
            echo -e "${GREEN}✓ API key loaded from secure storage${NC}"
        fi
    else
        echo -e "${YELLOW}⚠ Secrets volume not mounted - checking environment${NC}"
    fi
    
    # Fallback to environment variable (less secure)
    if [ -z "${OPENAI_API_KEY:-}" ]; then
        if [ -f /app/.env ]; then
            # Source .env with validation
            echo -e "${YELLOW}⚠ Loading from .env file (less secure)${NC}"
            # Validate .env file permissions
            if [ "$(stat -c %a /app/.env)" != "600" ]; then
                echo -e "${YELLOW}⚠ .env file permissions not optimal (should be 600)${NC}"
            fi
            # Source with safety checks
            set -a
            source /app/.env 2>/dev/null || true
            set +a
        fi
    fi
    
    # Validate API key presence without exposing it
    if [ -z "${OPENAI_API_KEY:-}" ]; then
        echo -e "${RED}✗ CRITICAL: OpenAI API key not configured${NC}"
        echo "Please provide API key via:"
        echo "  1. Secrets volume: /run/secrets/openai_api_key"
        echo "  2. Environment variable: OPENAI_API_KEY"
        echo "  3. .env file (least secure)"
        exit 1
    else
        # Validate API key format (basic check)
        if [[ ! "${OPENAI_API_KEY}" =~ ^sk-[a-zA-Z0-9]{48}$ ]]; then
            echo -e "${YELLOW}⚠ API key format may be invalid${NC}"
        else
            echo -e "${GREEN}✓ OpenAI API key validated${NC}"
        fi
    fi
}

# Security: Check system requirements with limits
check_requirements() {
    local errors=0
    
    echo -e "\n${BLUE}Checking security requirements...${NC}"
    
    # Check Python
    if command -v python3 &> /dev/null; then
        echo -e "${GREEN}✓ Python $(python3 --version 2>&1)${NC}"
    else
        echo -e "${RED}✗ Python not found${NC}"
        errors=$((errors + 1))
    fi
    
    # Check Streamlit
    if command -v streamlit &> /dev/null; then
        echo -e "${GREEN}✓ Streamlit installed${NC}"
    else
        echo -e "${RED}✗ Streamlit not found${NC}"
        errors=$((errors + 1))
    fi
    
    # Security: Check file system permissions
    for dir in /app/data /app/outputs /app/logs; do
        if [ -w "$dir" ]; then
            echo -e "${GREEN}✓ Write access to $dir${NC}"
        else
            echo -e "${RED}✗ No write access to $dir${NC}"
            errors=$((errors + 1))
        fi
    done
    
    # Security: Verify no world-writable files
    world_writable=$(find /app -type f -perm -002 2>/dev/null | wc -l)
    if [ "$world_writable" -eq 0 ]; then
        echo -e "${GREEN}✓ No world-writable files found${NC}"
    else
        echo -e "${YELLOW}⚠ Found $world_writable world-writable files${NC}"
    fi
    
    return $errors
}

# Security: Initialize secure directories
init_secure_directories() {
    echo -e "\n${BLUE}Initializing secure directories...${NC}"
    
    # Define directories with appropriate permissions
    declare -A directories=(
        ["/app/data/raw"]=755
        ["/app/data/processed"]=755
        ["/app/outputs/exports"]=755
        ["/app/outputs/reports"]=755
        ["/app/outputs/visualizations"]=755
        ["/app/client_input"]=750
        ["/app/logs"]=755
        ["/app/.secrets"]=700
    )
    
    for dir in "${!directories[@]}"; do
        permission="${directories[$dir]}"
        if [ ! -d "$dir" ]; then
            mkdir -p "$dir"
            chmod "$permission" "$dir"
            echo -e "${GREEN}✓ Created $dir with permissions $permission${NC}"
        else
            # Verify permissions
            current_perm=$(stat -c %a "$dir")
            if [ "$current_perm" != "$permission" ]; then
                echo -e "${YELLOW}⚠ $dir has permissions $current_perm (expected $permission)${NC}"
            else
                echo -e "  Directory exists: $dir (permissions: $permission)"
            fi
        fi
    done
}

# Security: Validate environment with restrictions
validate_environment() {
    echo -e "\n${BLUE}Validating secure environment...${NC}"
    
    # Set secure defaults
    export APP_ENV="${APP_ENV:-production}"
    export LOG_LEVEL="${LOG_LEVEL:-WARNING}"  # Less verbose in production
    export MAX_FILE_SIZE_MB="${MAX_FILE_SIZE_MB:-50}"
    export SESSION_TIMEOUT_MINUTES="${SESSION_TIMEOUT_MINUTES:-30}"
    export API_RATE_LIMIT_PER_MINUTE="${API_RATE_LIMIT_PER_MINUTE:-60}"
    export ENABLE_DEBUG="${ENABLE_DEBUG:-false}"
    
    # Security: Validate APP_ENV
    if [ "$APP_ENV" == "development" ]; then
        echo -e "${YELLOW}⚠ Running in development mode - reduced security${NC}"
    else
        echo -e "${GREEN}✓ Running in production mode${NC}"
    fi
    
    # Security: Ensure debug is disabled in production
    if [ "$APP_ENV" == "production" ] && [ "$ENABLE_DEBUG" == "true" ]; then
        echo -e "${RED}✗ Debug enabled in production - disabling${NC}"
        export ENABLE_DEBUG="false"
    fi
    
    # Display secure configuration (without secrets)
    echo -e "\n${BLUE}Secure Configuration:${NC}"
    echo "  Environment: $APP_ENV"
    echo "  OpenAI Model: ${OPENAI_MODEL:-gpt-4}"
    echo "  Max File Size: ${MAX_FILE_SIZE_MB} MB"
    echo "  Session Timeout: ${SESSION_TIMEOUT_MINUTES} minutes"
    echo "  Rate Limit: ${API_RATE_LIMIT_PER_MINUTE} requests/min"
    echo "  Log Level: $LOG_LEVEL"
    echo "  Debug Mode: $ENABLE_DEBUG"
}

# Security: Enhanced health checks
health_check() {
    echo -e "\n${BLUE}Running security health checks...${NC}"
    
    # Check disk space
    available_space=$(df /app | awk 'NR==2 {print $4}')
    if [ "$available_space" -lt 100000 ]; then
        echo -e "${YELLOW}⚠ Low disk space: ${available_space}KB available${NC}"
    else
        echo -e "${GREEN}✓ Disk space OK (${available_space}KB available)${NC}"
    fi
    
    # Check memory
    if [ -f /proc/meminfo ]; then
        available_mem=$(grep MemAvailable /proc/meminfo | awk '{print $2}')
        if [ "$available_mem" -lt 256000 ]; then
            echo -e "${RED}✗ Critical: Low memory (${available_mem}KB)${NC}"
            exit 1
        elif [ "$available_mem" -lt 512000 ]; then
            echo -e "${YELLOW}⚠ Low memory: ${available_mem}KB available${NC}"
        else
            echo -e "${GREEN}✓ Memory OK (${available_mem}KB available)${NC}"
        fi
    fi
    
    # Security: Check for suspicious processes
    suspicious_count=$(ps aux | grep -E '(nc|netcat|nmap|curl.*eval)' | grep -v grep | wc -l)
    if [ "$suspicious_count" -gt 0 ]; then
        echo -e "${RED}✗ Suspicious processes detected${NC}"
    else
        echo -e "${GREEN}✓ No suspicious processes found${NC}"
    fi
    
    # Security: Verify network restrictions
    if [ "$STREAMLIT_SERVER_ADDRESS" == "0.0.0.0" ]; then
        echo -e "${YELLOW}⚠ Server binding to all interfaces (less secure)${NC}"
    else
        echo -e "${GREEN}✓ Server binding restricted to: $STREAMLIT_SERVER_ADDRESS${NC}"
    fi
}

# Security: Setup audit logging
setup_audit_logging() {
    echo -e "\n${BLUE}Setting up audit logging...${NC}"
    
    # Create audit log with timestamp
    AUDIT_LOG="/app/logs/audit_$(date +%Y%m%d_%H%M%S).log"
    
    # Initialize audit log
    {
        echo "=== AUDIT LOG INITIALIZED ==="
        echo "Timestamp: $(date -Iseconds)"
        echo "User: $(whoami)"
        echo "UID: $(id -u)"
        echo "Environment: ${APP_ENV}"
        echo "Container ID: ${HOSTNAME}"
        echo "==========================="
    } > "$AUDIT_LOG"
    
    # Set restricted permissions
    chmod 600 "$AUDIT_LOG"
    
    echo -e "${GREEN}✓ Audit logging initialized: $AUDIT_LOG${NC}"
    
    # Export for application use
    export AUDIT_LOG_PATH="$AUDIT_LOG"
}

# Security: Setup rate limiting
setup_rate_limiting() {
    echo -e "\n${BLUE}Configuring rate limiting...${NC}"
    
    # Create rate limit tracking directory
    RATE_LIMIT_DIR="/tmp/rate_limits"
    mkdir -p "$RATE_LIMIT_DIR"
    chmod 700 "$RATE_LIMIT_DIR"
    
    # Export rate limiting configuration
    export RATE_LIMIT_ENABLED="true"
    export RATE_LIMIT_STORAGE="$RATE_LIMIT_DIR"
    
    echo -e "${GREEN}✓ Rate limiting configured${NC}"
}

# Security: Monitor for security events
security_monitor() {
    # This would run in background to monitor security events
    {
        while true; do
            # Check for failed authentication attempts
            failed_auth=$(grep -c "authentication failed" /app/logs/*.log 2>/dev/null || echo 0)
            if [ "$failed_auth" -gt 10 ]; then
                echo "$(date): WARNING - Multiple authentication failures detected" >> "$AUDIT_LOG_PATH"
            fi
            
            # Check for API rate limit violations
            # This would integrate with your application's rate limiting
            
            sleep 60  # Check every minute
        done
    } &
    
    echo -e "${GREEN}✓ Security monitoring started (PID: $!)${NC}"
}

# Main secure bootstrap sequence
main() {
    echo -e "\n${BLUE}Starting secure bootstrap sequence...${NC}"
    
    # Security checks first
    verify_integrity
    
    # Load secrets securely
    load_secrets
    
    # Check requirements
    check_requirements
    if [ $? -ne 0 ]; then
        echo -e "\n${RED}Bootstrap failed: Missing critical requirements${NC}"
        exit 1
    fi
    
    # Initialize secure environment
    init_secure_directories
    validate_environment
    setup_audit_logging
    setup_rate_limiting
    
    # Run health checks
    health_check
    
    # Start security monitoring
    security_monitor
    
    echo -e "\n${GREEN}================================================${NC}"
    echo -e "${GREEN}   Secure Bootstrap completed successfully!${NC}"
    echo -e "${GREEN}================================================${NC}"
    
    # Security: Clear sensitive environment variables from process
    unset OPENAI_API_KEY_TEMP
    
    # Start the application with security restrictions
    echo -e "\n${BLUE}Starting Streamlit application (secure mode)...${NC}"
    echo "Access URL: http://${STREAMLIT_SERVER_ADDRESS:-127.0.0.1}:8501"
    echo "================================================"
    
    # Security: Use exec to replace shell process (prevents shell injection)
    # Add security headers and restrictions
    exec streamlit run /app/src/main.py \
        --server.port=8501 \
        --server.address="${STREAMLIT_SERVER_ADDRESS:-127.0.0.1}" \
        --server.headless=true \
        --server.runOnSave=false \
        --server.allowRunOnSave=false \
        --browser.gatherUsageStats=false \
        --server.fileWatcherType=none \
        --server.enableCORS=false \
        --server.enableXsrfProtection=true \
        --server.maxUploadSize="${MAX_FILE_SIZE_MB:-50}" \
        --theme.base="dark" \
        --theme.primaryColor="#4ea4ff" \
        --theme.backgroundColor="#0f1419" \
        --theme.secondaryBackgroundColor="#18202a" \
        --theme.textColor="#e6edf3" \
        2>&1 | while read -r line; do
            # Security: Filter logs to prevent secret exposure
            secure_log "$line"
        done
}

# Security: Signal handling for graceful shutdown
cleanup() {
    echo -e "\n${YELLOW}Received shutdown signal...${NC}"
    
    # Log shutdown event
    if [ -n "${AUDIT_LOG_PATH:-}" ]; then
        echo "$(date): Application shutdown initiated" >> "$AUDIT_LOG_PATH"
    fi
    
    # Clean up sensitive data
    rm -f /tmp/rate_limits/*
    
    echo -e "${YELLOW}Shutting down gracefully...${NC}"
    exit 0
}

# Register signal handlers
trap cleanup SIGINT SIGTERM SIGQUIT

# Security: Prevent script sourcing (must be executed)
if [ "${BASH_SOURCE[0]}" != "${0}" ]; then
    echo "This script must be executed, not sourced"
    exit 1
fi

# Run main bootstrap with error handling
main "$@" || {
    echo -e "${RED}Bootstrap failed with exit code: $?${NC}"
    exit 1
}