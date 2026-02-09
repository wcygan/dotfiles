#!/usr/bin/env bash
#
# capture-screenshots.sh - Automated screenshot capture for design research
#
# Usage: ./capture-screenshots.sh <URL> [output-dir]

set -euo pipefail

URL="${1:-}"
OUTPUT_DIR="${2:-design-research-output}"

if [[ -z "$URL" ]]; then
    echo "Error: URL required"
    echo "Usage: $0 <URL> [output-dir]"
    exit 1
fi

# Create output directory
mkdir -p "$OUTPUT_DIR"

echo "📸 Capturing screenshots for: $URL"
echo "📁 Output directory: $OUTPUT_DIR"
echo ""

# Check if Playwright is available
if ! command -v npx &> /dev/null; then
    echo "❌ Error: npx not found. Please install Node.js"
    exit 1
fi

# Check if playwright is installed
if ! npx playwright --version &> /dev/null; then
    echo "⚠️  Playwright not found. Installing..."
    npm install -D playwright
    npx playwright install chromium
fi

echo "📸 Full page screenshot..."
npx playwright screenshot \
    --full-page \
    "$URL" \
    "$OUTPUT_DIR/full-page.png"

echo "📸 Viewport screenshot (1920x1080)..."
npx playwright screenshot \
    --viewport-size=1920,1080 \
    "$URL" \
    "$OUTPUT_DIR/viewport.png"

echo "📸 Mobile screenshot (iPhone 12)..."
npx playwright screenshot \
    --viewport-size=390,844 \
    "$URL" \
    "$OUTPUT_DIR/mobile.png"

echo "📸 Tablet screenshot (iPad Pro)..."
npx playwright screenshot \
    --viewport-size=1024,1366 \
    "$URL" \
    "$OUTPUT_DIR/tablet.png"

echo "📸 Dark mode screenshot..."
npx playwright screenshot \
    --color-scheme=dark \
    "$URL" \
    "$OUTPUT_DIR/dark-mode.png" \
    || echo "⚠️  Dark mode screenshot may not be available"

echo ""
echo "✅ Screenshots saved to: $OUTPUT_DIR/"
echo ""
echo "Files created:"
ls -lh "$OUTPUT_DIR"/*.png
