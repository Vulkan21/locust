set -e

RESULTS_DIR=${1:-"results/test"}
TEST_NAME="01_sanity_rest"
REST_HOST=${REST_BASE_URL:-"http://localhost:8000"}

echo "========================================="
echo "Sanity Check - REST API"
echo "========================================="
echo "Host: $REST_HOST"
echo "Users: 5, Spawn rate: 1/s, Duration: 2min"
echo ""

locust -f locustfile_rest_simple.py \
    --host=$REST_HOST \
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



