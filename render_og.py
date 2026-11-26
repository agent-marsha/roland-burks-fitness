#!/usr/bin/env python3
"""Render og-card.html (same folder) to og-image.png at exactly 1200x630."""
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image

HERE = Path(__file__).resolve().parent
SRC = HERE / "og-card.html"
OUT = HERE / "og-image.png"

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1200, "height": 630}, device_scale_factor=1)
    page.goto(SRC.as_uri())
    page.wait_for_load_state("networkidle")
    page.evaluate("document.fonts.ready.then(() => true)")
    page.screenshot(path=str(OUT), clip={"x": 0, "y": 0, "width": 1200, "height": 630})
    browser.close()

size = Image.open(OUT).size
assert size == (1200, 630), f"bad size {size}"
print(f"{OUT} {size}")
