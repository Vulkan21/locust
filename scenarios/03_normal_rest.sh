set -e

RESULTS_DIR=${1:-"results/test"}
TEST_NAME="03_normal_rest"
REST_HOST=${REST_BASE_URL:-"http://localhost:8000"}

echo "========================================="
echo "Normal Load - REST API"
echo "========================================="
echo "Host: $REST_HOST"
echo "Users: 50, Spawn rate: 5/s, Duration: 10min"
echo ""

locust -f locustfile_rest_simple.py \
    --host=$REST_HOST \
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



