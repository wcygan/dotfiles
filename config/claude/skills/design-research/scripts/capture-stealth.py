#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "playwright",
#     "camoufox[geoip]>=0.4.4",
# ]
# ///
"""Stealth screenshot capture using Camoufox anti-detect browser."""

import sys
import time
import random
from pathlib import Path
from playwright.sync_api import sync_playwright
from camoufox.sync_api import Camoufox


def capture_with_stealth(url: str, output_dir: str, viewport: dict = None) -> dict:
    """Capture screenshot using Camoufox anti-detect browser."""
    if viewport is None:
        viewport = {"width": 1920, "height": 1080}

    full_page = viewport["width"] >= 1920

    print(f"🦊 Camoufox stealth mode: Capturing {url}")
    print(f"   Viewport: {viewport['width']}x{viewport['height']}")

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    try:
        # Launch Camoufox with anti-detect features
        with Camoufox(
            headless=True,
            humanize=True,  # Enable human-like behavior
            geoip=True,     # Use realistic geolocation
            os=("macos", "windows"),  # Randomize OS fingerprint
            # Firefox-based - fundamentally different from Chromium
        ) as browser:
            page = browser.new_page()

            # Set realistic viewport
            page.set_viewport_size(viewport)

            # Navigate with timeout
            page.goto(url, wait_until="networkidle", timeout=60000)

            # Human-like delay (1-3 seconds)
            delay = random.uniform(1.0, 3.0)
            print(f"⏱️  Waiting {delay:.1f}s (human-like delay)")
            time.sleep(delay)

            # Capture screenshot
            timestamp = int(time.time() * 1000)
            screenshot_path = output_path / f"stealth-{timestamp}.png"
            page.screenshot(path=str(screenshot_path), full_page=full_page)

            # Get HTML content for block detection
            html = page.content()

            print(f"✅ Screenshot saved: {screenshot_path}")

            return {
                "success": True,
                "screenshot_path": str(screenshot_path),
                "html": html,
                "url": url,
                "viewport": viewport
            }

    except Exception as error:
        print(f"❌ Error: {error}", file=sys.stderr)
        return {
            "success": False,
            "error": str(error),
            "url": url,
            "viewport": viewport
        }


def capture_all_viewports(url: str, output_dir: str) -> list[dict]:
    """Capture screenshots at multiple viewports."""
    viewports = [
        {"name": "desktop", "width": 1920, "height": 1080},
        {"name": "mobile", "width": 390, "height": 844},
        {"name": "tablet", "width": 1024, "height": 1366}
    ]

    results = []

    for vp in viewports:
        print(f"\n📱 Capturing {vp['name']} viewport ({vp['width']}x{vp['height']})")
        result = capture_with_stealth(url, output_dir, {"width": vp["width"], "height": vp["height"]})
        results.append({"viewport": vp["name"], **result})

    return results


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: uv run capture-stealth.py <URL> [output-dir]", file=sys.stderr)
        sys.exit(1)

    url = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "design-research-output"

    results = capture_all_viewports(url, output_dir)

    print("\n📊 Results:")
    for r in results:
        status = "✅" if r["success"] else "❌"
        print(f"  {r['viewport']}: {status}")

    all_success = all(r["success"] for r in results)
    sys.exit(0 if all_success else 1)
