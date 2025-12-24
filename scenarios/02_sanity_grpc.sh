set -e

RESULTS_DIR=${1:-"results/test"}
TEST_NAME="02_sanity_grpc"
GRPC_HOST=${GRPC_TARGET:-"localhost:50051"}

echo "========================================="
echo "Sanity Check - gRPC"
echo "========================================="
echo "Host: $GRPC_HOST"
echo "Users: 5, Spawn rate: 1/s, Duration: 2min"
echo ""

locust -f locustfile_grpc_simple.py \
    --host=$GRPC_HOST \
    --users 5 \
    --spawn-rate 1 \
    --run-time 2m \
    --headless \
    --html "$RESULTS_DIR/${TEST_NAME}.html" \
    --csv "$RESULTS_DIR/${TEST_NAME}"

echo ""
echo "✓ Test complete! Results saved to:"
echo "  - $RESULTS_DIR/${TEST_NAME}.html"
echo "  - $RESULTS_DIR/${TEST_NAME}_stats.csv"



