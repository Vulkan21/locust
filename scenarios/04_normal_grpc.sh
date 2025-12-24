set -e

RESULTS_DIR=${1:-"results/test"}
TEST_NAME="04_normal_grpc"
GRPC_HOST=${GRPC_TARGET:-"localhost:50051"}

echo "========================================="
echo "Normal Load - gRPC"
echo "========================================="
echo "Host: $GRPC_HOST"
echo "Users: 50, Spawn rate: 5/s, Duration: 10min"
echo ""

locust -f locustfile_grpc_simple.py \
    --host=$GRPC_HOST \
    --users 50 \
    --spawn-rate 5 \
    --run-time 3m \
    --headless \
    --html "$RESULTS_DIR/${TEST_NAME}.html" \
    --csv "$RESULTS_DIR/${TEST_NAME}"

echo ""
echo "✓ Test complete! Results saved to:"
echo "  - $RESULTS_DIR/${TEST_NAME}.html"
echo "  - $RESULTS_DIR/${TEST_NAME}_stats.csv"



