#!/usr/bin/env python3
"""Render all section SVGs (and snake) to PNG previews via Playwright/Chromium."""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "preview"
OUT.mkdir(exist_ok=True)

TARGETS = [
    ("sections/01-tech-universe.svg", 1664, 936),
    ("sections/02-ai-native-engineering.svg", 1664, 936),
    ("sections/03-career-trajectory.svg", 1664, 936),
    ("sections/04-education-knowledge.svg", 1664, 936),
    ("sections/05-contact-network.svg", 1664, 936),
    ("sections/06-live-github-stats.svg", 1664, 936),
]

def main():
    names = sys.argv[1:]
    with sync_playwright() as p:
        b = p.chromium.launch()
        for rel, w, h in TARGETS:
            stem = Path(rel).stem
            if names and stem not in names and not any(n in stem for n in names):
                continue
            pg = b.new_page(viewport={"width": w, "height": h})
            pg.goto("file://" + str((ROOT / rel).resolve()))
            pg.wait_for_timeout(2500)
            pg.screenshot(path=str(OUT / f"{stem}.png"), clip={"x": 0, "y": 0, "width": w, "height": h})
            pg.close()
            print("rendered", stem)
        b.close()

if __name__ == "__main__":
    main()
