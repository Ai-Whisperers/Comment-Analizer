#!/bin/bash
# Security validation script for Comment Analyzer
# Run before deployment to validate security configuration

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo "=========================================="
echo "   Security Configuration Validator"
echo "=========================================="

ERRORS=0
WARNINGS=0

# Function to check security item
check_security() {
    local description="$1"
    local command="$2"
    local expected="$3"
    
    echo -n "Checking: $description... "
    
    result=$(eval "$command" 2>/dev/null || echo "FAILED")
    
    if [[ "$result" == "$expected" ]] || [[ "$result" =~ $expected ]]; then
        echo -e "${GREEN}✓${NC}"
        return 0
    elif [[ "$result" == "FAILED" ]]; then
        echo -e "${RED}✗ (Failed to execute)${NC}"
        ((ERRORS++))
        return 1
    else
        echo -e "${YELLOW}⚠ (Got: $result, Expected: $expected)${NC}"
        ((WARNINGS++))
        return 1
    fi
}

echo -e "\n${BLUE}1. File Security Checks${NC}"
echo "------------------------"

# Check .env file permissions
if [ -f .env ]; then
    check_security ".env permissions" "stat -c %a .env" "600"
else
    echo -e ".env file: ${YELLOW}Not found (OK if using secrets)${NC}"
fi

# Check for sensitive data in code
echo -n "Checking for hardcoded secrets... "
if grep -r "sk-[a-zA-Z0-9]\{48\}" src/ 2>/dev/null; then
    echo -e "${RED}✗ Found potential API keys in source${NC}"
    ((ERRORS++))
else
    echo -e "${GREEN}✓${NC}"
fi

# Check Dockerfile security
echo -n "Checking Dockerfile for USER directive... "
if grep -q "USER appuser" Dockerfile.secure; then
    echo -e "${GREEN}✓${NC}"
else
    echo -e "${RED}✗ Missing non-root user${NC}"
    ((ERRORS++))
fi

echo -e "\n${BLUE}2. Dependencies Security${NC}"
echo "------------------------"

# Check for known vulnerabilities
echo -n "Scanning requirements.txt for vulnerabilities... "
if command -v safety &> /dev/null; then
    vulnerabilities=$(safety check --json 2>/dev/null | grep -c '"vulnerability"' || echo "0")
    if [ "$vulnerabilities" -eq "0" ]; then
        echo -e "${GREEN}✓ No known vulnerabilities${NC}"
    else
        echo -e "${RED}✗ Found $vulnerabilities vulnerabilities${NC}"
        ((ERRORS++))
    fi
else
    echo -e "${YELLOW}⚠ Safety not installed${NC}"
    ((WARNINGS++))
fi

echo -e "\n${BLUE}3. Docker Security${NC}"
echo "------------------"

# Check Docker daemon security
echo -n "Checking Docker daemon configuration... "
if docker info 2>/dev/null | grep -q "Security Options"; then
    echo -e "${GREEN}✓${NC}"
else
    echo -e "${YELLOW}⚠ Cannot verify Docker security options${NC}"
    ((WARNINGS++))
fi

# Check for secrets directory
echo -n "Checking secrets directory... "
if [ -d secrets ]; then
    check_security "secrets directory permissions" "stat -c %a secrets" "700"
else
    echo -e "${YELLOW}⚠ secrets directory not found${NC}"
    ((WARNINGS++))
fi

echo -e "\n${BLUE}4. Configuration Security${NC}"
echo "-------------------------"

# Check for secure configuration in docker-compose
echo -n "Checking docker-compose security settings... "
if [ -f docker-compose.secure.yml ]; then
    security_features=0
    
    grep -q "read_only: true" docker-compose.secure.yml && ((security_features++))
    grep -q "no-new-privileges:true" docker-compose.secure.yml && ((security_features++))
    grep -q "cap_drop:" docker-compose.secure.yml && ((security_features++))
    grep -q "user: \"1000:1000\"" docker-compose.secure.yml && ((security_features++))
    
    if [ "$security_features" -ge 3 ]; then
        echo -e "${GREEN}✓ ($security_features/4 security features enabled)${NC}"
    else
        echo -e "${YELLOW}⚠ Only $security_features/4 security features enabled${NC}"
        ((WARNINGS++))
    fi
else
    echo -e "${RED}✗ docker-compose.secure.yml not found${NC}"
    ((ERRORS++))
fi

echo -e "\n${BLUE}5. Runtime Security${NC}"
echo "-------------------"

# Check for audit logging setup
echo -n "Checking audit logging configuration... "
if grep -q "setup_audit_logging" docker-bootstrap-secure.sh 2>/dev/null; then
    echo -e "${GREEN}✓${NC}"
else
    echo -e "${RED}✗ Audit logging not configured${NC}"
    ((ERRORS++))
fi

# Check for rate limiting
echo -n "Checking rate limiting configuration... "
if grep -q "setup_rate_limiting" docker-bootstrap-secure.sh 2>/dev/null; then
    echo -e "${GREEN}✓${NC}"
else
    echo -e "${YELLOW}⚠ Rate limiting not configured${NC}"
    ((WARNINGS++))
fi

echo -e "\n${BLUE}6. Network Security${NC}"
echo "-------------------"

# Check for localhost binding
echo -n "Checking network binding configuration... "
if grep -q "127.0.0.1:8501:8501" docker-compose.secure.yml 2>/dev/null; then
    echo -e "${GREEN}✓ Bound to localhost only${NC}"
else
    echo -e "${YELLOW}⚠ Check network binding configuration${NC}"
    ((WARNINGS++))
fi

echo -e "\n${BLUE}7. Compliance Checks${NC}"
echo "--------------------"

# Check for security documentation
echo -n "Checking for security documentation... "
if [ -f "local-reports/bootstrap-contracts-audit-report.md" ]; then
    echo -e "${GREEN}✓ Audit report found${NC}"
else
    echo -e "${YELLOW}⚠ Security audit report not found${NC}"
    ((WARNINGS++))
fi

# Summary
echo "=========================================="
echo -e "${BLUE}Security Check Summary${NC}"
echo "=========================================="

if [ "$ERRORS" -eq 0 ] && [ "$WARNINGS" -eq 0 ]; then
    echo -e "${GREEN}✓ All security checks passed!${NC}"
    echo "The application is ready for secure deployment."
    exit 0
elif [ "$ERRORS" -eq 0 ]; then
    echo -e "${YELLOW}⚠ Passed with $WARNINGS warnings${NC}"
    echo "Review warnings before production deployment."
    exit 0
else
    echo -e "${RED}✗ Failed with $ERRORS errors and $WARNINGS warnings${NC}"
    echo "Address critical issues before deployment."
    exit 1
fi