#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "pytesseract>=0.3.10",
#   "pillow>=10.0.0",
# ]
# ///
"""Detect if a page is blocked by anti-bot systems."""

import sys
import json
from pathlib import Path

try:
    from PIL import Image
    import pytesseract
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False


def detect_block(screenshot_path: str, html_content: str = "") -> dict:
    """Detect bot protection from screenshot and HTML analysis."""
    indicators = {
        "cloudflare": False,
        "captcha": False,
        "empty": False,
        "corrupted": False,
        "reasons": []
    }

    # Check screenshot file size
    screenshot = Path(screenshot_path)
    if screenshot.exists():
        size = screenshot.stat().st_size

        # Small files are likely block pages
        if size < 50_000:  # < 50KB likely a block page
            indicators["empty"] = True
            indicators["reasons"].append(f"Screenshot unusually small ({size} bytes < 50KB)")

        # Large files (>400KB) may indicate corruption or complex block pages
        elif size > 400_000:
            indicators["corrupted"] = True
            indicators["reasons"].append(f"Screenshot unusually large ({size} bytes > 400KB) - may be corrupted")

        # Try to detect corruption by attempting to open the image
        try:
            img = Image.open(screenshot_path)
            img.verify()
        except Exception as e:
            indicators["corrupted"] = True
            indicators["reasons"].append(f"Image validation failed: {str(e)}")

        # OCR text extraction if available
        if OCR_AVAILABLE and size < 500_000:  # Don't OCR huge files
            try:
                img = Image.open(screenshot_path)
                text = pytesseract.image_to_string(img).lower()

                # Check for block page keywords in screenshot
                block_keywords = [
                    "sorry, you have been blocked",
                    "you have been blocked",
                    "access denied",
                    "blocked",
                    "cloudflare",
                    "ray id",
                    "checking your browser",
                    "just a moment",
                    "security check",
                    "captcha"
                ]

                found_keywords = [kw for kw in block_keywords if kw in text]
                if found_keywords:
                    indicators["cloudflare"] = "cloudflare" in text or "ray id" in text
                    indicators["captcha"] = "captcha" in text
                    indicators["reasons"].append(f"Block keywords found in screenshot: {', '.join(found_keywords)}")

            except Exception as e:
                # OCR failed, but don't mark as blocked
                pass

    # Check HTML content
    if html_content:
        lower_content = html_content.lower()

        # Cloudflare indicators
        cloudflare_keywords = [
            "checking your browser",
            "just a moment",
            "challenge-platform",
            "ray id",
            "you have been blocked",
            "sorry, you have been blocked",
            "access denied",
            "cloudflare"
        ]
        if any(phrase in lower_content for phrase in cloudflare_keywords):
            indicators["cloudflare"] = True
            found = [kw for kw in cloudflare_keywords if kw in lower_content]
            indicators["reasons"].append(f"Cloudflare keywords in HTML: {', '.join(found[:3])}")

        # CAPTCHA indicators
        if any(captcha in lower_content for captcha in ["captcha", "recaptcha", "hcaptcha"]):
            indicators["captcha"] = True
            indicators["reasons"].append("CAPTCHA detected in HTML")

        # Very minimal content
        if len(html_content) < 2000:
            indicators["empty"] = True
            indicators["reasons"].append(f"HTML content unusually small ({len(html_content)} chars)")

    is_blocked = indicators["cloudflare"] or indicators["captcha"] or indicators["empty"] or indicators["corrupted"]

    return {
        "blocked": is_blocked,
        **indicators
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: uv run detect-block.py <screenshot-path> [html-path]", file=sys.stderr)
        sys.exit(1)

    screenshot_path = sys.argv[1]
    html_path = sys.argv[2] if len(sys.argv) > 2 else None

    html = ""
    if html_path:
        html = Path(html_path).read_text()

    result = detect_block(screenshot_path, html)
    print(json.dumps(result, indent=2))
    sys.exit(1 if result["blocked"] else 0)
