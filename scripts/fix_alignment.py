#!/usr/bin/env python3
"""
Fix the text alignment in parsa-kraken profile SVGs.

The original SYSTEM.INFO panel uses 'flow' tspan layout where each tspan
follows the previous one's natural width. Because the dot filler counts
are hand-tuned per row and don't perfectly compensate for the variable
key length, the value column ends up at different x positions per row.

This script rewrites each row to use explicit x positions on every tspan
so that:
  - the leading '. '           is at x = 520
  - the red key                is at x = 540
  - the dots filler ': ... '   is at x = 720
  - the value (white/black)    is at x = 870  -> ALWAYS ALIGNED

Works on:
  - templates/light.template.svg
  - templates/dark.template.svg
  - light.svg  (after substitution)
  - dark.svg   (after substitution)
"""
from pathlib import Path
import re
import json

# Resolve paths relative to the project root (parent of this scripts/ folder).
ROOT = Path(__file__).resolve().parent.parent
TEMPLATES = ROOT / "templates"
DARK_FILL = "#dbeafe"   # dark theme value text fill
LIGHT_FILL = "#1E293B"   # light theme value text fill

# x columns (px). The system info panel starts at x=508 and is 655 wide
COL_PREFIX = 520
COL_KEY = 540
COL_DOTS = 720
COL_VALUE = 870

# y positions for each row (lc0..lc21). lc0 at y=42, step=22
def y_of(idx):
    return 42 + idx * 22

# Separator (the long dashed line for header / section breaks)
SEPARATOR_LIGHT = " -——————————————————————————————————————————-—-"
SEPARATOR_DARK = SEPARATOR_LIGHT  # same length

# A row's worth of dots between the colon and the value.
# Width budget: from x=720 (COL_DOTS) to x=870 (COL_VALUE) = 150px.
# At 15px monospace, ~9px per char -> ~16 chars fit comfortably.
DOTS = ": ............... "


def build_row(clip_id, idx, kind, theme_fill, payload=None):
    """Build a single <g clip-path="url(#clip_id)">... row.

    `kind` is one of:
      - 'head'        : terminal_id header (red header + dashed separator)
      - 'separator_h' : a section separator header (e.g. '- Contact' + dashes)
      - 'spacer'      : empty row with just '. '
      - 'kv_simple'   : row with single key + value  (key is plain string)
      - 'kv_compound' : row with 'Core.Lang' / 'Grid.Mail' style compound key
      - 'note'        : row with just '. ' prefix and a value (no key)
    """
    y = y_of(idx)
    g_open = f'<g clip-path="url(#{clip_id})"><text x="520" y="0" fill="{theme_fill}">'
    g_close = '</text></g>'

    if kind == 'head':
        # payload is the terminal_id (or {{TERMINAL_ID}})
        text = payload[0] if isinstance(payload, tuple) else payload
        return (
            g_open
            + f'<tspan x="{COL_PREFIX}" y="{y}" class="head">{text}</tspan>'
            + f'<tspan x="{COL_DOTS}" y="{y}" class="cc">{SEPARATOR_LIGHT}</tspan>'
            + g_close
        )

    if kind == 'separator_h':
        # payload is the accent header text e.g. '- Contact'
        text = payload[0] if isinstance(payload, tuple) else payload
        return (
            g_open
            + f'<tspan x="{COL_PREFIX}" y="{y}" class="accent">{text}</tspan>'
            + f'<tspan x="{COL_DOTS}" y="{y}" class="cc">{SEPARATOR_LIGHT}</tspan>'
            + g_close
        )

    if kind == 'spacer':
        return (
            g_open
            + f'<tspan x="{COL_PREFIX}" y="{y}" class="cc">. </tspan>'
            + g_close
        )

    if kind == 'note':
        # '. ' prefix + value only (no key, no dots)
        text = payload[0] if isinstance(payload, tuple) else payload
        return (
            g_open
            + f'<tspan x="{COL_PREFIX}" y="{y}" class="cc">. </tspan>'
            + f'<tspan x="{COL_VALUE}" y="{y}" class="value">{text}</tspan>'
            + g_close
        )

    if kind == 'kv_simple':
        key, value = payload
        return (
            g_open
            + f'<tspan x="{COL_PREFIX}" y="{y}" class="cc">. </tspan>'
            + f'<tspan x="{COL_KEY}" y="{y}" class="key">{key}</tspan>'
            + f'<tspan x="{COL_DOTS}" y="{y}" class="cc">{DOTS}</tspan>'
            + f'<tspan x="{COL_VALUE}" y="{y}" class="value">{value}</tspan>'
            + g_close
        )

    if kind == 'kv_compound':
        # payload is (prefix_word, sub_word, value) e.g. ('Core', 'Lang', 'C# | Python')
        prefix_word, sub_word, value = payload
        # Core . Lang : ........... value
        # We put 'Core' at COL_KEY, '.' inline, 'Lang' at COL_KEY+50
        # The compound keys never go above ~9 chars, so COL_DOTS=720 stays safe
        return (
            g_open
            + f'<tspan x="{COL_PREFIX}" y="{y}" class="cc">. </tspan>'
            + f'<tspan x="{COL_KEY}" y="{y}" class="key">{prefix_word}</tspan>'
            + f'<tspan x="{COL_KEY + 50}" y="{y}" class="cc">.</tspan>'
            + f'<tspan x="{COL_KEY + 65}" y="{y}" class="key">{sub_word}</tspan>'
            + f'<tspan x="{COL_DOTS}" y="{y}" class="cc">{DOTS}</tspan>'
            + f'<tspan x="{COL_VALUE}" y="{y}" class="value">{value}</tspan>'
            + g_close
        )

    raise ValueError(f"Unknown kind: {kind}")


def build_system_info_block(theme_fill, is_template):
    """Build the full 22-row SYSTEM.INFO block (lc0..lc21).

    If is_template=True, placeholders like {{NAME}} are used.
    If is_template=False, real values from profile.json are substituted.
    """
    if is_template:
        P = lambda k: "{{" + k + "}}"
        rows = [
            (0,  'lc0',  'head',         ('{{TERMINAL_ID}}',)),
            (1,  'lc1',  'kv_simple',    ('Subject',    P('NAME'))),
            (2,  'lc2',  'kv_simple',    ('Role',       P('ROLE'))),
            (3,  'lc3',  'kv_simple',    ('Origin',     P('ORIGIN'))),
            (4,  'lc4',  'kv_simple',    ('Education',  P('EDUCATION'))),
            (5,  'lc5',  'kv_simple',    ('Current',    P('CURRENT'))),
            (6,  'lc6',  'kv_simple',    ('Focus',      P('FOCUS'))),
            (7,  'lc7',  'kv_simple',    ('Experience', P('EXPERIENCE'))),
            (8,  'lc8',  'kv_compound',  ('Core', 'Lang',      P('LANGUAGES'))),
            (9,  'lc9',  'kv_compound',  ('Core', 'Frontend',  P('FRONTEND'))),
            (10, 'lc10', 'kv_compound',  ('Core', 'Backend',   P('BACKEND'))),
            (11, 'lc11', 'kv_compound',  ('Core', 'Database',  P('DATABASE'))),
            (12, 'lc12', 'kv_compound',  ('Core', 'Infra',     P('INFRA'))),
            (13, 'lc13', 'spacer',       ()),
            (14, 'lc14', 'separator_h',  ('- Contact',)),
            (15, 'lc15', 'kv_compound',  ('Grid', 'Mail',     P('EMAIL'))),
            (16, 'lc16', 'kv_compound',  ('Grid', 'Telegram',  P('TELEGRAM'))),
            (17, 'lc17', 'kv_compound',  ('Grid', 'LinkedIn',  P('LINKEDIN'))),
            (18, 'lc18', 'kv_compound',  ('Grid', 'Github',    P('GITHUB_USERNAME'))),
            (19, 'lc19', 'spacer',       ()),
            (20, 'lc20', 'separator_h',  ('- Live Stats',)),
            (21, 'lc21', 'note',         ('Live GitHub stats below \u2193',)),
        ]
    else:
        data = json.loads((ROOT / "profile.json").read_text(encoding="utf-8"))
        rows = [
            (0,  'lc0',  'head',         (data['terminal_id'],)),
            (1,  'lc1',  'kv_simple',    ('Subject',    data['name'])),
            (2,  'lc2',  'kv_simple',    ('Role',       data['role'])),
            (3,  'lc3',  'kv_simple',    ('Origin',     data['origin'])),
            (4,  'lc4',  'kv_simple',    ('Education',  data['education'])),
            (5,  'lc5',  'kv_simple',    ('Current',    data['current'])),
            (6,  'lc6',  'kv_simple',    ('Focus',      data['focus'])),
            (7,  'lc7',  'kv_simple',    ('Experience', data['experience'])),
            (8,  'lc8',  'kv_compound',  ('Core', 'Lang',      data['languages'])),
            (9,  'lc9',  'kv_compound',  ('Core', 'Frontend',  data['frontend'])),
            (10, 'lc10', 'kv_compound',  ('Core', 'Backend',   data['backend'])),
            (11, 'lc11', 'kv_compound',  ('Core', 'Database',  data['database'])),
            (12, 'lc12', 'kv_compound',  ('Core', 'Infra',     data['infra'])),
            (13, 'lc13', 'spacer',       ()),
            (14, 'lc14', 'separator_h',  ('- Contact',)),
            (15, 'lc15', 'kv_compound',  ('Grid', 'Mail',      data['email'])),
            (16, 'lc16', 'kv_compound',  ('Grid', 'Telegram',  data['telegram'])),
            (17, 'lc17', 'kv_compound',  ('Grid', 'LinkedIn',  data['linkedin'])),
            (18, 'lc18', 'kv_compound',  ('Grid', 'Github',    data['github_username'])),
            (19, 'lc19', 'spacer',       ()),
            (20, 'lc20', 'separator_h',  ('- Live Stats',)),
            (21, 'lc21', 'note',         ('Live GitHub stats below \u2193',)),
        ]

    parts = []
    for idx, clip_id, kind, payload in rows:
        parts.append(build_row(clip_id, idx, kind, theme_fill, payload))
    return "".join(parts)


# Regex that matches the entire block from <g clip-path="url(#lc0)"> to the
# closing </g> of <g clip-path="url(#lc21)">. The original SVGs put all 22
# clip-path groups on a single line, so we can capture them all at once.
ROW_BLOCK_RE = re.compile(
    r'<g clip-path="url\(#lc0\)"><text.*?</text></g>'
    r'.*?'
    r'<g clip-path="url\(#lc21\)"><text.*?</text></g>',
    re.DOTALL,
)


def patch_svg(svg_path, theme_fill, is_template):
    text = svg_path.read_text(encoding="utf-8")
    new_block = build_system_info_block(theme_fill, is_template)
    new_text, n = ROW_BLOCK_RE.subn(new_block, text, count=1)
    if n == 0:
        raise RuntimeError(f"Row block not found in {svg_path}")
    svg_path.write_text(new_text, encoding="utf-8")
    print(f"  Patched {svg_path.name}  ({len(new_block)} chars of row content)")


def main():
    print("Aligning SYSTEM.INFO rows...")
    patch_svg(TEMPLATES / "light.template.svg", LIGHT_FILL, is_template=True)
    patch_svg(TEMPLATES / "dark.template.svg",  DARK_FILL,  is_template=True)
    patch_svg(ROOT / "light.svg", LIGHT_FILL, is_template=False)
    patch_svg(ROOT / "dark.svg",  DARK_FILL,  is_template=False)
    print("Done. All values now start at x=870 -> perfectly aligned.")


if __name__ == "__main__":
    main()
