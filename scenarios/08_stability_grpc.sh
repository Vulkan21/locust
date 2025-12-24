set -e

RESULTS_DIR=${1:-"results/test"}
TEST_NAME="08_stability_grpc"
GRPC_HOST=${GRPC_TARGET:-"localhost:50051"}

echo "========================================="
echo "Stability Test - gRPC"
echo "========================================="
echo "Host: $GRPC_HOST"
echo "Users: 50, Spawn rate: 5/s, Duration: 30min"
echo "⚠ This is a long-running test (30 minutes)"
echo ""

locust -f locustfile_grpc_simple.py \
    --host=$GRPC_HOST \
    --users 100 \
    --spawn-rate 5 \
    --run-time 10m \
    --headless \
    --html "$RESULTS_DIR/${TEST_NAME}.html" \
    --csv "$RESULTS_DIR/${TEST_NAME}"

echo ""
echo "✓ Test complete! Results saved to:"
echo "  - $RESULTS_DIR/${TEST_NAME}.html"
echo "  - $RESULTS_DIR/${TEST_NAME}_stats.csv"



