set -e

RESULTS_DIR=${1:-"results/test"}
TEST_NAME="05_stress_rest"
REST_HOST=${REST_BASE_URL:-"http://localhost:8000"}

echo "========================================="
echo "Stress Test - REST API"
echo "========================================="
echo "Host: $REST_HOST"
echo "Users: 200, Spawn rate: 20/s, Duration: 15min"
echo ""

locust -f locustfile_rest_simple.py \
    --host=$REST_HOST \
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



