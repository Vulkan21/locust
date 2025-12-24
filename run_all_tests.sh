set -e

echo "================================"
echo "Load Testing Suite for REST vs gRPC"
echo "================================"
echo ""

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' 

RESULTS_DIR="results/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$RESULTS_DIR"

echo -e "${BLUE}Results will be saved to: $RESULTS_DIR${NC}"
echo ""

run_test() {
    local test_name=$1
    local script=$2
    
    echo -e "${YELLOW}========================================${NC}"
    echo -e "${YELLOW}Running: $test_name${NC}"
    echo -e "${YELLOW}========================================${NC}"
    
    bash "$script" "$RESULTS_DIR"
    
    echo -e "${GREEN}✓ Completed: $test_name${NC}"
    echo ""
    sleep 3
}


echo -e "${BLUE}Starting test suite...${NC}"
echo ""

run_test "1. Sanity Check - REST API" "./scenarios/01_sanity_rest.sh"
run_test "2. Sanity Check - gRPC" "./scenarios/02_sanity_grpc.sh"
run_test "3. Normal Load - REST API" "./scenarios/03_normal_rest.sh"
run_test "4. Normal Load - gRPC" "./scenarios/04_normal_grpc.sh"
run_test "5. Stress Test - REST API" "./scenarios/05_stress_rest.sh"
run_test "6. Stress Test - gRPC" "./scenarios/06_stress_grpc.sh"
run_test "7. Stability Test - REST API" "./scenarios/07_stability_rest.sh"
run_test "8. Stability Test - gRPC" "./scenarios/08_stability_grpc.sh"

echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}All tests completed!${NC}"
echo -e "${GREEN}================================${NC}"
echo ""
echo "Results saved in: $RESULTS_DIR"
echo ""
echo "Summary of tests:"
ls -lh "$RESULTS_DIR"/*.html 2>/dev/null || echo "No HTML reports found"
echo ""
echo "Total test duration: ~30 minutes"


