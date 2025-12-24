set -e

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "========================================"
echo "Checking services availability"
echo "========================================"
echo ""

REST_URL="${REST_BASE_URL:-http://localhost:8000}"
GRPC_HOST="${GRPC_TARGET:-localhost:50051}"
GRPC_HOSTNAME=$(echo $GRPC_HOST | cut -d':' -f1)
GRPC_PORT=$(echo $GRPC_HOST | cut -d':' -f2)

echo -e "${YELLOW}1. Checking REST API...${NC}"
echo "   URL: $REST_URL"

if curl -f -s -o /dev/null "$REST_URL/terms" 2>/dev/null; then
    echo -e "   ${GREEN}✓ REST API is available${NC}"
    
    TERM_COUNT=$(curl -s "$REST_URL/terms" | jq '. | length' 2>/dev/null || echo "unknown")
    echo "   Terms count: $TERM_COUNT"
else
    echo -e "   ${RED}✗ REST API is NOT available${NC}"
    echo "   Please start the service:"
    echo "     cd /srv/REST_FastAPI"
    echo "     docker compose up -d"
    REST_FAILED=1
fi

echo ""

echo -e "${YELLOW}2. Checking gRPC Service...${NC}"
echo "   Target: $GRPC_HOST"

if command -v nc &> /dev/null; then
    if nc -z $GRPC_HOSTNAME $GRPC_PORT 2>/dev/null; then
        echo -e "   ${GREEN}✓ gRPC service port is open${NC}"
else
        echo -e "   ${RED}✗ gRPC service port is NOT open${NC}"
        echo "   Please start the service:"
        echo "     cd /srv/gRPC_Protobuf"
        echo "     docker compose up -d"
        GRPC_FAILED=1
    fi
else
    echo -e "   ${YELLOW}⚠ netcat (nc) not available, skipping port check${NC}"
    echo "   Install: apt-get install netcat"
fi

echo ""

echo -e "${YELLOW}3. Checking Docker containers...${NC}"

if command -v docker &> /dev/null; then
    REST_CONTAINER=$(docker ps --filter "name=fastapi" --format "{{.Names}}" | head -1)
    GRPC_CONTAINER=$(docker ps --filter "name=grpc" --format "{{.Names}}" | head -1)
    
    if [ ! -z "$REST_CONTAINER" ]; then
        echo -e "   ${GREEN}✓ REST container running: $REST_CONTAINER${NC}"
else
        echo -e "   ${YELLOW}⚠ No REST container found${NC}"
    fi
    
    if [ ! -z "$GRPC_CONTAINER" ]; then
        echo -e "   ${GREEN}✓ gRPC container running: $GRPC_CONTAINER${NC}"
else
        echo -e "   ${YELLOW}⚠ No gRPC container found${NC}"
    fi
else
    echo -e "   ${YELLOW}⚠ Docker not available${NC}"
fi

echo ""

echo "========================================"
if [ -z "$REST_FAILED" ] && [ -z "$GRPC_FAILED" ]; then
    echo -e "${GREEN}✓ All services are ready!${NC}"
    echo "You can now run Locust tests:"
    echo ""
    echo "  # Quick test REST"
    echo "  locust -f locustfile_rest.py --host=$REST_URL --users 5 --spawn-rate 1 --run-time 1m --headless"
    echo ""
    echo "  # Quick test gRPC"
    echo "  locust -f locustfile_grpc.py --host=$GRPC_HOST --users 5 --spawn-rate 1 --run-time 1m --headless"
    echo ""
    echo "  # Run all tests"
    echo "  ./run_tests.sh"
    echo "========================================"
    exit 0
else
    echo -e "${RED}✗ Some services are not available${NC}"
    echo "Please start the missing services"
    echo "========================================"
    exit 1
fi
