#!/usr/bin/env python3
"""
Reorder the GitHub contribution snake's animation so it eats BRIGHT
cells first, then DIM cells.

The Platane/snk action generates an SVG where each contribution cell has
its own @keyframes rule defining WHEN in the timeline that cell briefly
flashes its contribution color. By default, the order follows the snake's
path (TSP-style), which means bright and dim cells are interleaved.

This script post-processes the generated SVG so that:
  - Cells with the highest contribution level (var(--c4) = darkest green)
    animate at LOW timeline percentages (early)
  - Cells with the lowest contribution level (var(--c1) = lightest green)
    animate at HIGH timeline percentages (late)
  - Empty cells (var(--ce)) keep their default fill (no animation)

The visual effect: as the snake's 26.7s animation plays, the brightest
squares light up first, then progressively dimmer ones — matching the
"eat bright first, then dim" behavior the user requested.

Usage:
  python scripts/reorder_snake.py dist/github-snake.svg
  python scripts/reorder_snake.py dist/github-snake-dark.svg

The script is idempotent: running it twice produces the same output.
"""
from pathlib import Path
import re
import sys


# snk color tokens (defined in the SVG's <style> as CSS vars)
# We use the variable NAMES, not hex values, to stay theme-agnostic.
LEVEL_VARS = ["c4", "c3", "c2", "c1"]  # high → low contribution
EMPTY_VAR = "ce"                         # empty (no contribution)

# Pattern matches a single @keyframes rule, e.g.:
#   @keyframes c0{96.99%{fill:var(--c4)}97.01%,100%{fill:var(--ce)}}
# snk's keyframes contain NESTED braces (one level), so we need a regex
# that handles one level of nesting: outer {...} contains inner {...} pairs.
KEYFRAME_RE = re.compile(
    r'@keyframes\s+(c[a-z0-9]+)\s*\{(?:[^{}]|\{[^{}]*\})*\}',
    re.IGNORECASE,
)

# Pattern matches a single cell class rule, e.g.:
#   .c.c0{fill:var(--c4);animation-name:c0}
# Note: snk uses var(--cN) with double dashes inside the parens.
CELLCLASS_RE = re.compile(
    r'\.c\.c([a-z0-9]+)\{fill:var\(--(c[1-4])\);animation-name:c\1\}',
    re.IGNORECASE,
)

# Pattern matches the global .c rule's animation duration
ANIM_DUR_RE = re.compile(r'\.c\{[^}]*animation:\s*none\s+(\d+)ms', re.IGNORECASE)


def parse_cells(svg_text):
    """Return list of (cell_id, level_var) tuples, e.g. [('c0','c4'), ...]."""
    cells = []
    for m in CELLCLASS_RE.finditer(svg_text):
        cell_id = m.group(1)          # e.g. '0', '1', 'a', etc.
        level_var = m.group(2).lower()  # 'c1', 'c2', 'c3', 'c4'
        cells.append((cell_id, level_var))
    return cells


def reorder_svg(svg_text):
    """Reorder snake animation timings so bright cells animate first."""
    # 1. Parse all animated cells with their contribution level
    cells = parse_cells(svg_text)
    if not cells:
        return svg_text  # nothing to do

    # 2. Sort by level (level 4 = brightest = first; level 1 = dimmest = last)
    def level_key(cell):
        _, lv = cell
        try:
            return -int(lv[1])  # negative so higher level sorts first
        except (IndexError, ValueError):
            return 0
    sorted_cells = sorted(cells, key=level_key)

    # 3. Distribute timing evenly across the timeline
    # Each cell gets a small "flash" window. We space them so the last cell
    # ends at ~99% (just before the animation loops).
    n = len(sorted_cells)
    if n == 0:
        return svg_text
    # Per-cell window duration (in % of timeline)
    # Bright cells get slightly longer flash windows so they're more prominent
    window = 0.4  # % each cell stays "on"
    gap = (99.0 - n * window) / max(1, n - 1)  # gap between cells

    new_keyframes = []
    new_cellclasses = []
    for i, (cell_id, level_var) in enumerate(sorted_cells):
        # When the cell's flash starts (in %)
        start_pct = i * gap + i * window
        end_pct = start_pct + window
        # Build the new @keyframes rule
        new_keyframes.append(
            f'@keyframes c{cell_id}{{{start_pct:.3f}%{{fill:var(--{level_var})}}'
            f'{end_pct:.3f}%,100%{{fill:var(--{EMPTY_VAR})}}}}'
        )
        # Build the new cell class rule (level + animation-name)
        new_cellclasses.append(
            f'.c.c{cell_id}{{fill:var(--{level_var});animation-name:c{cell_id}}}'
        )

    # 4. Replace old keyframes block (in <style>)
    # The original SVG has all @keyframes as one big concatenated block in the
    # CSS, e.g.:
    #   .c.c0{...}.c.c1{...}...@keyframes c0{...}@keyframes c1{...}...
    # We replace each @keyframes individually.
    new_text = svg_text
    # Build a map from cell_id (numeric/alpha) to its new keyframe text
    # We need to also handle the cell class rule changes (linking the new
    # animation-name to the new keyframe).
    # Since the cell IDs are reused, the simplest approach is:
    #   - Remove all existing @keyframes rules
    #   - Remove all .c.cN rules
    #   - Inject the new ones in their place
    # We do this by replacing the entire CSS block content.

    # Find the <style> block
    style_open = new_text.find('<style')
    style_close = new_text.find('</style>')
    if style_open == -1 or style_close == -1:
        # No <style> block — fall back to per-rule replacement
        for kf_match in KEYFRAME_RE.finditer(svg_text):
            pass
        return svg_text

    # Extract existing CSS
    css_start = new_text.find('>', style_open) + 1
    css_end = style_close
    css = new_text[css_start:css_end]

    # Remove all existing @keyframes cN{...} rules
    css = KEYFRAME_RE.sub('', css)
    # Remove all .c.cN{...} rules (snk uses var(--cN) with double-dash)
    css = re.sub(
        r'\.c\.c[a-z0-9]+\{fill:var\(--c[1-4]\);animation-name:c[a-z0-9]+\}',
        '',
        css,
    )

    # Append the new keyframes + cell classes at the end of the CSS
    css += '\n' + '\n'.join(new_cellclasses) + '\n' + '\n'.join(new_keyframes) + '\n'

    # Rebuild the SVG text with the new CSS
    new_text = new_text[:css_start] + css + new_text[css_end:]
    return new_text


def main():
    if len(sys.argv) < 2:
        print("Usage: reorder_snake.py <path-to-snake.svg> [<path2> ...]")
        sys.exit(1)
    for arg in sys.argv[1:]:
        path = Path(arg)
        if not path.exists():
            print(f"  {path}: NOT FOUND, skipping")
            continue
        original = path.read_text(encoding="utf-8")
        new = reorder_svg(original)
        if new == original:
            print(f"  {path.name}: no changes (no animated cells found)")
        else:
            path.write_text(new, encoding="utf-8")
            print(f"  {path.name}: reordered snake animation (bright → dim)")


if __name__ == "__main__":
    main()
