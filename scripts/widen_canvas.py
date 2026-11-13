#!/usr/bin/env python3
"""
Extend the profile SVG canvas from 1180 → 1280 px wide.

Why: the value column at x=870 has only 307px of horizontal room before the
right panel border. Because `.value` uses a monospace font (Courier New 14px),
long values like "Architecture | Backend | Cloud | Security" (40 chars ≈ 336px
in monospace) were getting visually clipped at the right panel edge.

Widening the SVG to 1280 px gives the right panel an extra 100 px of width,
so the value column now has ~407 px — enough for the longest values without
losing the hacker/monospace aesthetic.

Patches all four files:
  templates/light.template.svg
  templates/dark.template.svg
  light.svg   (also re-run after build_profile.py)
  dark.svg    (also re-run after build_profile.py)
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
FILES = [
    ROOT / "templates" / "light.template.svg",
    ROOT / "templates" / "dark.template.svg",
    ROOT / "light.svg",
    ROOT / "dark.svg",
]

OLD_W = "1180"
NEW_W = "1280"
DELTA = 100  # NEW_W - OLD_W

# Substitutions to apply.
# Each tuple is (regex, replacement). We use regex so the same pattern catches
# all instances across the file.
SUBSTITUTIONS = [
    # SVG root: width="1180" and viewBox="0 0 1180 610"
    (re.compile(r'(<svg\b[^>]*\bwidth=")1180(")'), rf'\g<1>{NEW_W}\g<2>'),
    (re.compile(r'(<svg\b[^>]*\bviewBox="0 0 )1180( 610")'), rf'\g<1>{NEW_W}\g<2>'),
    # First two full-width background rects (after defs)
    (re.compile(r'(<rect width=")1180(" height="610" rx="18")'), rf'\g<1>{NEW_W}\g<2>'),
    # Titlebar background: x="3" y="3" width="1174"  -> 1274
    (re.compile(r'(<rect x="3" y="3" width=")1174(" height="34" rx="16")'), rf'\g<1>{DELTA + 1174}\g<2>'),
    # Centered title text: x="590" -> x="640"
    (re.compile(r'(<text x=")590(" y="25" text-anchor="middle")'), rf'\g<1>{590 + DELTA//2}\g<2>'),
    # SCANNING indicator circle: cx="1122" -> cx="1222"
    (re.compile(r'(<circle cx=")1122(" cy="20")'), rf'\g<1>{1122 + DELTA}\g<2>'),
    # SCANNING text: x="1132" -> x="1232"
    (re.compile(r'(<text x=")1132(" y="24" class="scan-label")'), rf'\g<1>{1132 + DELTA}\g<2>'),
    # Right panel: width="655" (and now width="669" from earlier patch) -> 755/769
    # We allow either value
    (re.compile(r'(<rect x="508" y="10" width=")(655|669)(" height="500")'),
     rf'\g<1>{655 + DELTA}\g<3>'),
    # Reveal mask: width="1180"
    (re.compile(r'(<mask id="revealMask"[^>]*width=")1180(" height="620")'), rf'\g<1>{NEW_W}\g<2>'),
    (re.compile(r'(<rect x="0" y="0" width=")1180(" height="0" fill="#fff">)'), rf'\g<1>{NEW_W}\g<2>'),
    # Animated height rect: to="560"  (already 560, leave alone)
    # Scan line rect (with -70 y and translate anim): width="1180"
    (re.compile(r'(<rect x="0" y="-70" width=")1180(" height="70")'), rf'\g<1>{NEW_W}\g<2>'),

    # Clip-path animation target width: 690 -> 780  (was clipping long values)
    (re.compile(r'to="690"'), 'to="780"'),
    # Outer frame: x="3" y="3" width="1174" height="604" rx="16" -> 1274
    (re.compile(r'(<rect x="3" y="3" width=")1174(" height="604" rx="16")'),
     rf'\g<1>{DELTA + 1174}\g<2>'),
]


def patch_file(path: Path):
    text = path.read_text(encoding="utf-8")
    original = text
    counts = []
    for pat, repl in SUBSTITUTIONS:
        new_text, n = pat.subn(repl, text)
        counts.append(n)
        text = new_text
    if text == original:
        print(f"  {path.name}: NO CHANGES (already patched?)")
    else:
        path.write_text(text, encoding="utf-8")
        # Show first non-zero substitution count for sanity
        nz = next((c for c in counts if c > 0), 0)
        print(f"  {path.name}: patched ({sum(counts)} substitutions)")


def main():
    print(f"Widening profile SVG canvas from {OLD_W} → {NEW_W}px...")
    for f in FILES:
        if not f.exists():
            print(f"  {f}: MISSING — skipped")
            continue
        patch_file(f)
    print("Done. The right panel is now ~100px wider, giving the value column more room.")


if __name__ == "__main__":
    main()
