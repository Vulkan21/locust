set -e

RESULTS_DIR=${1:-"results/test"}
TEST_NAME="06_stress_grpc"
GRPC_HOST=${GRPC_TARGET:-"localhost:50051"}

echo "========================================="
echo "Stress Test - gRPC"
echo "========================================="
echo "Host: $GRPC_HOST"
echo "Users: 200, Spawn rate: 20/s, Duration: 15min"
echo ""

locust -f locustfile_grpc_simple.py \
    --host=$GRPC_HOST \
    --users 200 \
    --spawn-rate 10 \
    --run-time 5m \
    --headless \
    --html "$RESULTS_DIR/${TEST_NAME}.html" \
    --csv "$RESULTS_DIR/${TEST_NAME}"

echo ""
echo "✓ Test complete! Results saved to:"
echo "  - $RESULTS_DIR/${TEST_NAME}.html"
echo "  - $RESULTS_DIR/${TEST_NAME}_stats.csv"



