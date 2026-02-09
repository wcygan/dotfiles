#!/usr/bin/env bash
#
# capture-screenshots.sh - Automated screenshot capture with bot protection handling
#
# Usage: ./capture-screenshots.sh <URL> [output-dir]

set -euo pipefail

URL="${1:-}"
OUTPUT_DIR="${2:-design-research-output}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

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

# Check if UV is available
if ! command -v uv &> /dev/null; then
    echo "❌ Error: uv not found. Please install from https://docs.astral.sh/uv/"
    echo "   Quick install: curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# STRATEGY 1: Standard Playwright (fast, no stealth)
echo "🔄 Strategy 1: Standard Playwright CLI"

# Check if Playwright CLI is available
if command -v npx &> /dev/null; then
    echo "📸 Full page screenshot..."
    npx playwright screenshot \
        --full-page \
        "$URL" \
        "$OUTPUT_DIR/full-page.png" 2>/dev/null || echo "⚠️  Standard capture failed"
else
    echo "⚠️  Playwright CLI not available, skipping standard capture"
fi

# Detect if we got blocked using improved detection
echo ""
echo "🔍 Checking for bot protection..."

BLOCKED=false
if [ -f "$OUTPUT_DIR/full-page.png" ]; then
    # Use detect-block.py with OCR for improved detection
    if uv run "$SCRIPT_DIR/detect-block.py" "$OUTPUT_DIR/full-page.png" 2>/dev/null; then
        echo "✅ No bot protection detected"
        BLOCKED=false
    else
        echo "⚠️  Bot protection detected"
        BLOCKED=true
        # Show what was detected
        uv run "$SCRIPT_DIR/detect-block.py" "$OUTPUT_DIR/full-page.png" 2>/dev/null | grep -E '(reasons|blocked)' || true
    fi
else
    BLOCKED=true
    echo "⚠️  No screenshot captured (may be blocked)"
fi

# STRATEGY 2: Camoufox Stealth Mode (if blocked)
if [ "$BLOCKED" = true ]; then
    echo ""
    echo "🔄 Strategy 2: Camoufox stealth mode (Firefox-based anti-detect)"
    echo ""

    if [ -f "$SCRIPT_DIR/capture-stealth.py" ]; then
        # UV automatically handles dependencies via inline metadata
        uv run "$SCRIPT_DIR/capture-stealth.py" "$URL" "$OUTPUT_DIR"
        STEALTH_EXIT=$?

        if [ $STEALTH_EXIT -eq 0 ]; then
            echo ""
            echo "✅ Camoufox stealth mode successful!"
        else
            echo ""
            echo "❌ Camoufox stealth mode also blocked"
            echo ""
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            echo "⚠️  MANUAL FALLBACK REQUIRED"
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            echo ""
            echo "The site has strong bot protection that blocked:"
            echo "  1. Standard Playwright CLI"
            echo "  2. Camoufox anti-detect browser (0% detection score normally)"
            echo ""
            echo "This indicates aggressive bot protection (likely CAPTCHA required)."
            echo ""
            echo "To continue design research, use manual browser capture:"
            echo ""
            echo "1. Open $URL in your browser"
            echo "2. Complete any CAPTCHA challenges"
            echo "3. Open DevTools (F12 or Cmd+Option+I)"
            echo "4. Run the extraction scripts from MANUAL-FALLBACK.md"
            echo "5. Take manual screenshots at different viewports"
            echo ""
            echo "See design-research/MANUAL-FALLBACK.md for complete instructions."
            echo ""
            exit 1
        fi
    else
        echo "❌ Stealth script not found: $SCRIPT_DIR/capture-stealth.py"
        echo "   Cannot proceed with anti-bot evasion"
        exit 1
    fi
fi

echo ""
echo "✅ Screenshots saved to: $OUTPUT_DIR/"
echo ""
echo "Files created:"
ls -lh "$OUTPUT_DIR"/*.png 2>/dev/null || echo "  (no screenshots captured)"
