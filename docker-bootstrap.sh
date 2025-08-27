#!/bin/bash
# Bootstrap script for Comment Analyzer Docker container
# This script handles initialization and startup contracts

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "================================================"
echo "   Comment Analyzer - Docker Bootstrap v1.0"
echo "================================================"

# Function to check critical requirements
check_requirements() {
    local errors=0
    
    echo -e "\n${YELLOW}Checking requirements...${NC}"
    
    # Check for OpenAI API Key
    if [ -z "$OPENAI_API_KEY" ]; then
        if [ -f /app/.env ]; then
            source /app/.env
        fi
    fi
    
    if [ -z "$OPENAI_API_KEY" ]; then
        echo -e "${RED}✗ CRITICAL: OPENAI_API_KEY not set${NC}"
        echo "  Please set via environment variable or .env file"
        errors=$((errors + 1))
    else
        echo -e "${GREEN}✓ OpenAI API Key configured${NC}"
    fi
    
    # Check Python installation
    if command -v python &> /dev/null; then
        echo -e "${GREEN}✓ Python $(python --version 2>&1)${NC}"
    else
        echo -e "${RED}✗ Python not found${NC}"
        errors=$((errors + 1))
    fi
    
    # Check Streamlit installation
    if command -v streamlit &> /dev/null; then
        echo -e "${GREEN}✓ Streamlit installed${NC}"
    else
        echo -e "${RED}✗ Streamlit not found${NC}"
        errors=$((errors + 1))
    fi
    
    return $errors
}

# Function to initialize directories
init_directories() {
    echo -e "\n${YELLOW}Initializing directories...${NC}"
    
    directories=(
        "/app/data/raw"
        "/app/data/processed"
        "/app/outputs/exports"
        "/app/outputs/reports"
        "/app/outputs/visualizations"
        "/app/client_input"
        "/app/logs"
    )
    
    for dir in "${directories[@]}"; do
        if [ ! -d "$dir" ]; then
            mkdir -p "$dir"
            echo -e "${GREEN}✓ Created $dir${NC}"
        else
            echo -e "  Directory exists: $dir"
        fi
    done
}

# Function to validate environment
validate_environment() {
    echo -e "\n${YELLOW}Validating environment...${NC}"
    
    # Check APP_ENV
    if [ -z "$APP_ENV" ]; then
        export APP_ENV="production"
        echo -e "  APP_ENV not set, defaulting to: production"
    else
        echo -e "  APP_ENV: $APP_ENV"
    fi
    
    # Display configuration
    echo -e "\n${YELLOW}Configuration:${NC}"
    echo "  OpenAI Model: ${OPENAI_MODEL:-gpt-4}"
    echo "  Max Tokens: ${OPENAI_MAX_TOKENS:-4000}"
    echo "  Max File Size: ${MAX_FILE_SIZE_MB:-50} MB"
    echo "  Log Level: ${LOG_LEVEL:-INFO}"
}

# Function to run health checks
health_check() {
    echo -e "\n${YELLOW}Running health checks...${NC}"
    
    # Check disk space
    available_space=$(df /app | awk 'NR==2 {print $4}')
    if [ "$available_space" -lt 100000 ]; then
        echo -e "${YELLOW}⚠ Low disk space: ${available_space}KB available${NC}"
    else
        echo -e "${GREEN}✓ Disk space OK${NC}"
    fi
    
    # Check memory
    if [ -f /proc/meminfo ]; then
        available_mem=$(grep MemAvailable /proc/meminfo | awk '{print $2}')
        if [ "$available_mem" -lt 512000 ]; then
            echo -e "${YELLOW}⚠ Low memory: ${available_mem}KB available${NC}"
        else
            echo -e "${GREEN}✓ Memory OK${NC}"
        fi
    fi
}

# Main bootstrap sequence
main() {
    echo -e "\n${YELLOW}Starting bootstrap sequence...${NC}"
    
    # Check requirements
    check_requirements
    if [ $? -ne 0 ]; then
        echo -e "\n${RED}Bootstrap failed: Missing critical requirements${NC}"
        exit 1
    fi
    
    # Initialize directories
    init_directories
    
    # Validate environment
    validate_environment
    
    # Run health checks
    health_check
    
    echo -e "\n${GREEN}================================================${NC}"
    echo -e "${GREEN}   Bootstrap completed successfully!${NC}"
    echo -e "${GREEN}================================================${NC}"
    
    # Start the application
    echo -e "\n${YELLOW}Starting Streamlit application...${NC}"
    echo "Access the application at: http://localhost:8501"
    echo "================================================"
    
    # Execute streamlit with proper configuration
    exec streamlit run /app/src/main.py \
        --server.port=8501 \
        --server.address=0.0.0.0 \
        --server.headless=true \
        --browser.gatherUsageStats=false \
        --theme.base="dark" \
        --theme.primaryColor="#4ea4ff" \
        --theme.backgroundColor="#0f1419" \
        --theme.secondaryBackgroundColor="#18202a" \
        --theme.textColor="#e6edf3"
}

# Handle signals for graceful shutdown
trap 'echo -e "\n${YELLOW}Shutting down...${NC}"; exit 0' SIGINT SIGTERM

# Run main bootstrap
main "$@"