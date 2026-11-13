#!/usr/bin/env python3
"""
Generate 6 CYBERPUNK minimal GitHub profile section SVGs for Parsa Taheri.

Palette (owner-specified):
  deep black     #111119
  violet         #8B35FF
  neon pink      #D500F9
  electric blue  #00D9FF
  neon yellow    #FFE500

Design language - "neon grid minimal":
  - deep-black canvas (#111119) with a whisper-quiet grid and two slow
    breathing radial glows (violet / electric blue)
  - thin 1px accent strokes, glass panels, minimal corner brackets
  - monospace micro-labels with wide letter-spacing, big bold sans titles
  - one accent colour per panel/card, rotating through the palette
  - neon yellow reserved for the single most important value of a section
  - restrained SMIL animation: pulsing dots, dash-drift lines, growing
    progress bars, one rotating dashed ring per panel

Sections:
  01 TECHNOLOGY UNIVERSE    - 4 stack panels (frontend / backend / AI / cloud)
  02 AI-NATIVE ENGINEERING  - hero + LLM / vision cards + architecture strips
  03 CAREER TRAJECTORY      - horizontal timeline, 4 role cards
  04 EDUCATION & KNOWLEDGE  - 3 degree cards + languages + mastery badges
  05 CONTACT NETWORK        - 6 endpoint cards
  06 LIVE GITHUB STATS      - particle network + live stat panel

Size: 1664x936. Regenerate via: python scripts/build_sections.py
"""
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape
import random

ROOT = Path(__file__).resolve().parent.parent
SECTIONS = ROOT / "sections"
SECTIONS.mkdir(exist_ok=True)

# ============================================================================
# CYBERPUNK DESIGN TOKENS
# ============================================================================
BG_0   = "#111119"   # deep black base
BG_1   = "#0C0C14"   # darker vignette
BG_2   = "#16161F"   # lifted tint
PANEL_TOP = "#1C1C29"
PANEL_BOT = "#13131C"
VIOLET = "#8B35FF"
PINK   = "#D500F9"
BLUE   = "#00D9FF"
YELLOW = "#FFE500"
TXT    = "#F2F2FA"   # primary text
TXT_2  = "#A9A9C4"   # secondary text
TXT_3  = "#63637F"   # dim text
LINE_DARK = "#26263A"  # hairline separators

SANS = "Arial, Helvetica, sans-serif"
MONO = "ui-monospace, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"

W, H = 1664, 936


def esc(s):
    """XML-escape text content (& < >)."""
    return xml_escape(str(s))


# ============================================================================
# SHARED DEFS
# ============================================================================
def defs_common():
    return f'''<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{BG_2}"/>
    <stop offset=".5" stop-color="{BG_0}"/>
    <stop offset="1" stop-color="{BG_1}"/>
  </linearGradient>
  <linearGradient id="panel" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{PANEL_TOP}" stop-opacity=".92"/>
    <stop offset="1" stop-color="{PANEL_BOT}" stop-opacity=".96"/>
  </linearGradient>
  <linearGradient id="panelV" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#221833" stop-opacity=".94"/>
    <stop offset="1" stop-color="{PANEL_BOT}" stop-opacity=".97"/>
  </linearGradient>
  <linearGradient id="panelB" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#12202B" stop-opacity=".94"/>
    <stop offset="1" stop-color="{PANEL_BOT}" stop-opacity=".97"/>
  </linearGradient>
  <linearGradient id="panelP" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#251331" stop-opacity=".94"/>
    <stop offset="1" stop-color="{PANEL_BOT}" stop-opacity=".97"/>
  </linearGradient>
  <linearGradient id="panelY" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#262313" stop-opacity=".94"/>
    <stop offset="1" stop-color="{PANEL_BOT}" stop-opacity=".97"/>
  </linearGradient>

  <radialGradient id="glowV" cx="50%" cy="50%" r="50%">
    <stop offset="0" stop-color="{VIOLET}" stop-opacity=".16"/>
    <stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="glowB" cx="50%" cy="50%" r="50%">
    <stop offset="0" stop-color="{BLUE}" stop-opacity=".13"/>
    <stop offset="1" stop-color="{BLUE}" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="glowP" cx="50%" cy="50%" r="50%">
    <stop offset="0" stop-color="{PINK}" stop-opacity=".15"/>
    <stop offset="1" stop-color="{PINK}" stop-opacity="0"/>
  </radialGradient>

  <pattern id="grid" width="44" height="44" patternUnits="userSpaceOnUse">
    <path d="M44 0H0V44" fill="none" stroke="#7A6AFF" stroke-opacity=".05"/>
    <circle cx="0" cy="0" r="1" fill="{BLUE}" opacity=".14"/>
  </pattern>

  <filter id="glow" x="-100%" y="-100%" width="300%" height="300%">
    <feGaussianBlur stdDeviation="4" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <filter id="tinyGlow" x="-100%" y="-100%" width="300%" height="300%">
    <feGaussianBlur stdDeviation="1.8"/>
  </filter>
  <filter id="softGlow" x="-100%" y="-100%" width="300%" height="300%">
    <feGaussianBlur stdDeviation="18"/>
  </filter>
</defs>
'''


def svg_open(w=W, h=H):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" preserveAspectRatio="xMidYMid meet">\n'
    )


def svg_close():
    return "</svg>\n"


def background(glow_a="glowV", glow_b="glowB"):
    """Minimal deep-black canvas: gradient + quiet grid + two breathing glows."""
    return f'''<rect width="{W}" height="{H}" fill="url(#bg)"/>
<rect width="{W}" height="{H}" fill="url(#grid)">
  <animateTransform attributeName="transform" type="translate"
    values="0 0;44 44;0 0" dur="22s" repeatCount="indefinite"/>
</rect>
<ellipse cx="{W*0.30:.0f}" cy="210" rx="520" ry="280" fill="url(#{glow_a})" filter="url(#softGlow)">
  <animate attributeName="opacity" values=".65;1;.65" dur="9s" repeatCount="indefinite"/>
</ellipse>
<ellipse cx="{W*0.72:.0f}" cy="760" rx="480" ry="260" fill="url(#{glow_b})" filter="url(#softGlow)">
  <animate attributeName="opacity" values=".5;.85;.5" dur="11s" repeatCount="indefinite"/>
</ellipse>
<g fill="{BLUE}" filter="url(#tinyGlow)">
  <circle cx="240" cy="150" r="1.6" opacity=".5"><animate attributeName="cy" values="150;132;150" dur="6s" repeatCount="indefinite"/></circle>
  <circle cx="1420" cy="180" r="1.4" opacity=".4"><animate attributeName="cy" values="180;196;180" dur="7s" repeatCount="indefinite"/></circle>
  <circle cx="480" cy="820" r="1.5" opacity=".35"><animate attributeName="cy" values="820;806;820" dur="8s" repeatCount="indefinite"/></circle>
  <circle cx="1180" cy="840" r="1.3" opacity=".4"><animate attributeName="cy" values="840;856;840" dur="6.5s" repeatCount="indefinite"/></circle>
</g>
'''


def header_block(num, title, subtitle, accent):
    """Minimal centered header: mono kicker, big title, dim sub, animated underline."""
    return f'''<g font-family="{SANS}" text-anchor="middle">
  <text x="{W//2}" y="70" fill="{accent}" font-family="{MONO}" font-size="12" letter-spacing="5" opacity=".9">
    {esc(num)} // {esc(subtitle.split('/')[0].strip() if '/' in subtitle else "SYSTEM")}
    <animate attributeName="opacity" values=".6;1;.6" dur="4s" repeatCount="indefinite"/>
  </text>
  <text x="{W//2}" y="116" fill="{TXT}" font-size="44" font-weight="800" letter-spacing="1">{esc(title)}</text>
  <text x="{W//2}" y="150" fill="{TXT_3}" font-family="{MONO}" font-size="12" letter-spacing="3">{esc(subtitle)}</text>
  <rect x="662" y="172" width="340" height="1.5" fill="{accent}" opacity=".55">
    <animate attributeName="width" values="240;420;240" dur="5s" repeatCount="indefinite"/>
    <animate attributeName="x" values="712;622;712" dur="5s" repeatCount="indefinite"/>
  </rect>
</g>
'''


def ticks(w, h, color, length=12, op=.5):
    """One minimal path with 4 corner brackets - the cyberpunk panel signature."""
    d = (f"M0 {length} V0 H{length} "
         f"M{w-length} 0 H{w} V{length} "
         f"M{w} {h-length} V{h} H{w-length} "
         f"M{length} {h} H0 V{h-length}")
    return (f'<path d="{d}" fill="none" stroke="{color}" stroke-width="1.5" '
            f'stroke-opacity="{op}"/>')


def footer_block(text, accent=BLUE):
    # mono 11px + letter-spacing 3  ->  ~9.6px per char, half-width ~4.8/char
    half = int(len(str(text)) * 5.2) + 24
    return f'''<g font-family="{MONO}" font-size="11" fill="{TXT_3}" letter-spacing="3" opacity=".85" text-anchor="middle">
  <circle cx="{W//2 - half}" cy="{H-24}" r="2" fill="{accent}"/>
  <text x="{W//2}" y="{H-20}">{esc(text)}</text>
  <circle cx="{W//2 + half}" cy="{H-24}" r="2" fill="{accent}"/>
</g>
'''


def progress_bar(x, y, w, pct, color, delay=0.0, h=4):
    """Minimal thin progress bar that grows once, keeps a faint track."""
    fill_w = int(w * pct / 100)
    return f'''<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h/2:.1f}" fill="{LINE_DARK}"/>
<rect x="{x}" y="{y}" width="0" height="{h}" rx="{h/2:.1f}" fill="{color}" filter="url(#tinyGlow)">
  <animate attributeName="width" from="0" to="{fill_w}" dur="1.6s" begin="{delay}s" fill="freeze" calcMode="spline" keySplines="0.25 0.1 0.25 1"/>
</rect>
'''


def pulsing_dot(cx, cy, color, r=5, dur=1.8, begin=0.0):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{color}" filter="url(#tinyGlow)">'
            f'<animate attributeName="r" values="{max(r-2,2)};{r+2};{max(r-2,2)}" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values=".45;1;.45" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/></circle>')


# ============================================================================
# SECTION 1 - TECHNOLOGY UNIVERSE  (accent rotation: B / V / P / Y)
# ============================================================================
TECH_PANELS = [
    {
        "num":  "01",
        "kind": "INTERFACE",
        "title": "FRONTEND",
        "sub":  "Experience / Components / Interaction",
        "color": BLUE,
        "panel": "panelB",
        "tags":  [
            ("React",      "atom"),
            ("Next.js",    "triangle"),
            ("TypeScript", "square"),
            ("Vue.js 3",   "vshape"),
            ("Tailwind",   "wave"),
            ("Three.js",   "cube"),
            ("Sass",       "brace"),
        ],
        "items": ["React", "Next.js", "TypeScript", "Vue.js 3", "Tailwind", "Three.js"],
        "status_text": "COMPONENTS ONLINE",
        "pct":   85,
    },
    {
        "num":  "02",
        "kind": "LOGIC",
        "title": "BACKEND",
        "sub":  "APIs / Services / Distributed Systems",
        "color": VIOLET,
        "panel": "panelV",
        "tags":  [
            ("Node.js",       "hex"),
            ("Python",        "snake"),
            ("Django",        "gshape"),
            ("Go",            "go"),
            ("REST API",      "link"),
            ("Microservices", "nodes"),
        ],
        "items": ["Node.js", "Python", "Django", "Go", "REST APIs", "Microservices"],
        "status_text": "SERVICES SYNCHRONIZED",
        "pct":   90,
    },
    {
        "num":  "03",
        "kind": "INTELLIGENCE",
        "title": "AI / ML",
        "sub":  "Vision / Learning / Inference",
        "color": PINK,
        "panel": "panelP",
        "tags":  [
            ("OpenCV",     "eye"),
            ("PyTorch",    "torch"),
            ("TensorFlow", "tf"),
            ("ML",         "brain"),
            ("Deep Learn", "layers"),
            ("LangChain",  "chain"),
        ],
        "items": ["OpenCV", "PyTorch", "TensorFlow", "Machine Learning", "Deep Learning", "LangChain"],
        "status_text": "MODELS TRAINED",
        "pct":   95,
    },
    {
        "num":  "04",
        "kind": "INFRASTRUCTURE",
        "title": "CLOUD",
        "sub":  "Scale / Containers / Automation",
        "color": YELLOW,
        "panel": "panelY",
        "tags":  [
            ("AWS",        "cloud"),
            ("Azure",      "triangle"),
            ("GCP",        "cloud"),
            ("Docker",     "box"),
            ("Kubernetes", "wheel"),
            ("Nginx",      "gate"),
        ],
        "items": ["Docker", "Kubernetes", "Nginx", "AWS", "Azure", "GCP", "CI/CD"],
        "status_text": "CLUSTERS OPERATIONAL",
        "pct":   88,
    },
]


def _tech_icon(shape: str, color: str, size: int = 22):
    """Small geometric tech icon centered at (0,0), fits ~size x size box."""
    s = size
    if shape == "atom":
        return (f'<g fill="none" stroke="{color}" stroke-width="1.4">'
                f'<ellipse rx="{s*0.45}" ry="{s*0.18}"/>'
                f'<ellipse rx="{s*0.45}" ry="{s*0.18}" transform="rotate(60)"/>'
                f'<ellipse rx="{s*0.45}" ry="{s*0.18}" transform="rotate(-60)"/>'
                f'<circle r="{s*0.08}" fill="{color}" stroke="none"/></g>')
    if shape == "triangle":
        return (f'<path d="M0 -{s*0.42} L{s*0.38} {s*0.32} L-{s*0.38} {s*0.32} Z" '
                f'fill="{color}" fill-opacity=".18" stroke="{color}" stroke-width="1.2"/>')
    if shape == "square":
        return (f'<rect x="-{s*0.36}" y="-{s*0.36}" width="{s*0.72}" height="{s*0.72}" rx="3" '
                f'fill="{color}" fill-opacity=".18" stroke="{color}" stroke-width="1.2"/>')
    if shape == "vshape":
        return (f'<path d="M-{s*0.42} -{s*0.28} L0 {s*0.32} L{s*0.42} -{s*0.28} '
                f'M-{s*0.18} -{s*0.28} L0 -{s*0.06} L{s*0.18} -{s*0.28}" fill="none" '
                f'stroke="{color}" stroke-width="1.6" stroke-linejoin="round"/>')
    if shape == "wave":
        return (f'<g fill="none" stroke="{color}" stroke-width="1.6" stroke-linecap="round">'
                f'<path d="M-{s*0.4} -{s*0.05} Q-{s*0.2} -{s*0.25} 0 -{s*0.05} T{s*0.4} -{s*0.05}"/>'
                f'<path d="M-{s*0.4} {s*0.18} Q-{s*0.2} -{s*0.02} 0 {s*0.18} T{s*0.4} {s*0.18}"/></g>')
    if shape == "cube":
        return (f'<g fill="none" stroke="{color}" stroke-width="1.4">'
                f'<path d="M0 -{s*0.42} L{s*0.36} -{s*0.18} L0 0 L-{s*0.36} -{s*0.18} Z" fill="{color}" fill-opacity=".35"/>'
                f'<path d="M0 0 L{s*0.36} -{s*0.18} L{s*0.36} {s*0.18} L0 {s*0.42} Z" fill="{color}" fill-opacity=".2"/>'
                f'<path d="M0 0 L-{s*0.36} -{s*0.18} L-{s*0.36} {s*0.18} L0 {s*0.42} Z" fill="{color}" fill-opacity=".1"/></g>')
    if shape == "brace":
        return (f'<path d="M-{s*0.18} -{s*0.42} Q-{s*0.32} -{s*0.42} -{s*0.32} -{s*0.2} '
                f'Q-{s*0.32} 0 -{s*0.4} 0 Q-{s*0.32} 0 -{s*0.32} {s*0.2} '
                f'Q-{s*0.32} {s*0.42} -{s*0.18} {s*0.42}" fill="none" stroke="{color}" '
                f'stroke-width="1.6" stroke-linecap="round"/>')
    if shape == "hex":
        return (f'<path d="M0 -{s*0.42} L{s*0.36} -{s*0.21} L{s*0.36} {s*0.21} L0 {s*0.42} '
                f'L-{s*0.36} {s*0.21} L-{s*0.36} -{s*0.21} Z" fill="{color}" fill-opacity=".18" '
                f'stroke="{color}" stroke-width="1.4"/>')
    if shape == "snake":
        return (f'<g fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round">'
                f'<path d="M-{s*0.32} -{s*0.28} Q{s*0.32} -{s*0.28} {s*0.32} 0 '
                f'Q{s*0.32} {s*0.28} -{s*0.32} {s*0.28}"/>'
                f'<circle cx="-{s*0.32}" cy="-{s*0.28}" r="1.5" fill="{color}"/>'
                f'<circle cx="{s*0.32}" cy="{s*0.28}" r="1.5" fill="{color}"/></g>')
    if shape == "gshape":
        return (f'<g fill="none" stroke="{color}" stroke-width="1.6">'
                f'<path d="M-{s*0.18} -{s*0.42} L-{s*0.18} {s*0.42} '
                f'M-{s*0.18} -{s*0.05} Q{s*0.32} -{s*0.05} {s*0.32} -{s*0.28} '
                f'M-{s*0.18} {s*0.05} Q{s*0.32} {s*0.05} {s*0.32} {s*0.28}"/></g>')
    if shape == "go":
        return (f'<g fill="none" stroke="{color}" stroke-width="1.8">'
                f'<path d="M-{s*0.05} -{s*0.32} A{s*0.32} {s*0.32} 0 1 1 -{s*0.05} {s*0.32} '
                f'L{s*0.32} {s*0.32} M-{s*0.05} {s*0.1} L{s*0.18} {s*0.1}"/></g>')
    if shape == "link":
        return (f'<g fill="none" stroke="{color}" stroke-width="1.6" stroke-linecap="round">'
                f'<path d="M-{s*0.32} 0 A{s*0.18} {s*0.18} 0 0 1 -{s*0.05} -{s*0.18} '
                f'L{s*0.05} -{s*0.18} A{s*0.18} {s*0.18} 0 0 1 {s*0.32} 0"/>'
                f'<path d="M{s*0.32} 0 A{s*0.18} {s*0.18} 0 0 1 {s*0.05} {s*0.18} '
                f'L-{s*0.05} {s*0.18} A{s*0.18} {s*0.18} 0 0 1 -{s*0.32} 0"/>'
                f'<line x1="-{s*0.32}" y1="0" x2="{s*0.32}" y2="0" stroke-dasharray="2 3" stroke-opacity=".5"/></g>')
    if shape == "nodes":
        return (f'<g fill="{color}">'
                f'<circle cx="-{s*0.32}" cy="-{s*0.18}" r="2.5"/>'
                f'<circle cx="{s*0.32}" cy="-{s*0.18}" r="2.5"/>'
                f'<circle cx="0" cy="{s*0.18}" r="2.5"/>'
                f'<line x1="-{s*0.32}" y1="-{s*0.18}" x2="0" y2="{s*0.18}" stroke="{color}" stroke-width="1.2"/>'
                f'<line x1="{s*0.32}" y1="-{s*0.18}" x2="0" y2="{s*0.18}" stroke="{color}" stroke-width="1.2"/></g>')
    if shape == "eye":
        return (f'<g fill="none" stroke="{color}" stroke-width="1.4">'
                f'<path d="M-{s*0.42} 0 Q0 -{s*0.28} {s*0.42} 0 Q0 {s*0.28} -{s*0.42} 0 Z"/>'
                f'<circle r="{s*0.1}" fill="{color}" stroke="none"/></g>')
    if shape == "torch":
        return (f'<g fill="{color}">'
                f'<path d="M0 -{s*0.42} Q{s*0.22} -{s*0.15} {s*0.18} {s*0.05} '
                f'Q{s*0.12} {s*0.28} 0 {s*0.42} Q-{s*0.12} {s*0.28} -{s*0.18} {s*0.05} '
                f'Q-{s*0.22} -{s*0.15} 0 -{s*0.42} Z" fill-opacity=".3" stroke="{color}" stroke-width="1.2"/>'
                f'<path d="M0 -{s*0.18} Q{s*0.1} -{s*0.05} {s*0.08} {s*0.1} '
                f'Q0 {s*0.2} -{s*0.08} {s*0.1} Q-{s*0.1} -{s*0.05} 0 -{s*0.18} Z" fill-opacity=".7"/></g>')
    if shape == "tf":
        return (f'<g fill="none" stroke="{color}" stroke-width="1.6" stroke-linejoin="round">'
                f'<path d="M0 -{s*0.42} L-{s*0.32} -{s*0.05} L-{s*0.32} {s*0.42} '
                f'M0 -{s*0.42} L{s*0.32} -{s*0.05} L{s*0.32} {s*0.42} '
                f'M-{s*0.32} -{s*0.05} L{s*0.32} -{s*0.05}"/></g>')
    if shape == "brain":
        return (f'<g fill="none" stroke="{color}" stroke-width="1.4">'
                f'<path d="M-{s*0.05} -{s*0.32} Q-{s*0.32} -{s*0.32} -{s*0.32} -{s*0.05} '
                f'Q-{s*0.4} {s*0.1} -{s*0.25} {s*0.3} Q-{s*0.18} {s*0.42} -{s*0.05} {s*0.32} Z" fill="{color}" fill-opacity=".18"/>'
                f'<path d="M{s*0.05} -{s*0.32} Q{s*0.32} -{s*0.32} {s*0.32} -{s*0.05} '
                f'Q{s*0.4} {s*0.1} {s*0.25} {s*0.3} Q{s*0.18} {s*0.42} {s*0.05} {s*0.32} Z" fill="{color}" fill-opacity=".18"/>'
                f'<line x1="0" y1="-{s*0.32}" x2="0" y2="{s*0.32}" stroke-dasharray="2 2"/></g>')
    if shape == "layers":
        return (f'<g fill="{color}" fill-opacity=".35" stroke="{color}" stroke-width="1">'
                f'<rect x="-{s*0.36}" y="-{s*0.4}" width="{s*0.72}" height="{s*0.12}" rx="1.5"/>'
                f'<rect x="-{s*0.28}" y="-{s*0.22}" width="{s*0.56}" height="{s*0.12}" rx="1.5"/>'
                f'<rect x="-{s*0.2}" y="-{s*0.04}" width="{s*0.4}" height="{s*0.12}" rx="1.5"/>'
                f'<rect x="-{s*0.12}" y="{s*0.14}" width="{s*0.24}" height="{s*0.12}" rx="1.5"/></g>')
    if shape == "chain":
        return (f'<g fill="none" stroke="{color}" stroke-width="1.5">'
                f'<ellipse cx="-{s*0.18}" cy="-{s*0.18}" rx="{s*0.16}" ry="{s*0.1}" transform="rotate(-45 -{s*0.18} -{s*0.18})"/>'
                f'<ellipse cx="{s*0.18}" cy="{s*0.18}" rx="{s*0.16}" ry="{s*0.1}" transform="rotate(-45 {s*0.18} {s*0.18})"/></g>')
    if shape == "cloud":
        return (f'<g fill="{color}" fill-opacity=".16" stroke="{color}" stroke-width="1.3">'
                f'<path d="M-{s*0.32} {s*0.05} Q-{s*0.42} {s*0.05} -{s*0.42} -{s*0.1} '
                f'Q-{s*0.42} -{s*0.3} -{s*0.22} -{s*0.3} Q-{s*0.12} -{s*0.4} {s*0.05} -{s*0.4} '
                f'Q{s*0.25} -{s*0.4} {s*0.32} -{s*0.2} Q{s*0.42} -{s*0.2} {s*0.42} -{s*0.05} '
                f'Q{s*0.42} {s*0.15} {s*0.22} {s*0.15} L-{s*0.22} {s*0.15} '
                f'Q-{s*0.32} {s*0.15} -{s*0.32} {s*0.05} Z"/></g>')
    if shape == "box":
        return (f'<g fill="none" stroke="{color}" stroke-width="1.4">'
                f'<rect x="-{s*0.34}" y="-{s*0.18}" width="{s*0.68}" height="{s*0.36}" rx="2"/>'
                f'<line x1="0" y1="-{s*0.18}" x2="0" y2="{s*0.18}"/>'
                f'<line x1="-{s*0.18}" y1="-{s*0.18}" x2="-{s*0.18}" y2="-{s*0.28}"/>'
                f'<line x1="0" y1="-{s*0.28}" x2="0" y2="-{s*0.18}"/>'
                f'<line x1="{s*0.18}" y1="-{s*0.18}" x2="{s*0.18}" y2="-{s*0.28}"/></g>')
    if shape == "wheel":
        return (f'<g fill="none" stroke="{color}" stroke-width="1.3">'
                f'<circle r="{s*0.34}"/>'
                f'<circle r="{s*0.1}" fill="{color}" fill-opacity=".4"/>'
                f'<line x1="0" y1="-{s*0.34}" x2="0" y2="-{s*0.1}"/>'
                f'<line x1="0" y1="{s*0.34}" x2="0" y2="{s*0.1}"/>'
                f'<line x1="-{s*0.34}" y1="0" x2="-{s*0.1}" y2="0"/>'
                f'<line x1="{s*0.34}" y1="0" x2="{s*0.1}" y2="0"/>'
                f'<line x1="-{s*0.24}" y1="-{s*0.24}" x2="-{s*0.07}" y2="-{s*0.07}"/>'
                f'<line x1="{s*0.24}" y1="{s*0.24}" x2="{s*0.07}" y2="{s*0.07}"/>'
                f'<line x1="-{s*0.24}" y1="{s*0.24}" x2="-{s*0.07}" y2="{s*0.07}"/>'
                f'<line x1="{s*0.24}" y1="-{s*0.24}" x2="{s*0.07}" y2="-{s*0.07}"/></g>')
    if shape == "gate":
        return (f'<g fill="none" stroke="{color}" stroke-width="1.4">'
                f'<path d="M0 -{s*0.36} L{s*0.32} -{s*0.18} L{s*0.32} {s*0.32} '
                f'L-{s*0.32} {s*0.32} L-{s*0.32} -{s*0.18} Z" fill="{color}" fill-opacity=".16"/>'
                f'<line x1="-{s*0.16}" y1="0" x2="{s*0.16}" y2="0"/>'
                f'<line x1="0" y1="-{s*0.05}" x2="0" y2="{s*0.32}"/></g>')
    return f'<circle r="3" fill="{color}"/>'


def section_tech_universe():
    out = [svg_open()]
    out.append(defs_common())
    out.append(background("glowB", "glowV"))
    out.append(header_block("01", "TECHNOLOGY UNIVERSE",
                            "ENGINEERING STACK / SYSTEMS / INFRASTRUCTURE / INTELLIGENCE", BLUE))

    panel_w, panel_h, panel_y = 350, 650, 210
    gap = (W - 80 - 4 * panel_w) // 3
    panel_xs = [40 + i * (panel_w + gap) for i in range(4)]

    out.append(f'<g font-family="{SANS}">')
    for i, p in enumerate(TECH_PANELS):
        x = panel_xs[i]
        c = p["color"]
        out.append(f'<g transform="translate({x} {panel_y})">')
        # glass panel + accent hairline + corner brackets
        out.append(f'<rect width="{panel_w}" height="{panel_h}" rx="16" fill="url(#{p["panel"]})" '
                   f'stroke="{c}" stroke-opacity=".28"/>')
        out.append(f'<rect x="1" y="1" width="{panel_w-2}" height="{panel_h-2}" rx="15" fill="none" '
                   f'stroke="{TXT}" stroke-opacity=".05"/>')
        out.append(ticks(panel_w - 2, panel_h - 2, c, 12, .55))
        out.append(f'<rect x="24" y="30" width="26" height="2" fill="{c}"/>')

        # number + kind
        out.append(f'<text x="24" y="58" fill="{c}" font-family="{MONO}" font-size="12" '
                   f'letter-spacing="3" font-weight="600">{p["num"]} / {p["kind"]}</text>')
        # title + sub
        out.append(f'<text x="24" y="102" fill="{TXT}" font-size="34" font-weight="800">{p["title"]}</text>')
        out.append(f'<text x="24" y="128" fill="{TXT_2}" font-size="13">{esc(p["sub"])}</text>')

        # one rotating dashed ring, top-right
        out.append(f'<g transform="translate({panel_w-56} 76)" fill="none" stroke="{c}">')
        out.append(f'<circle r="30" stroke-opacity=".22" stroke-dasharray="4 10">')
        out.append(f'<animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="14s" repeatCount="indefinite"/></circle>')
        out.append(f'<circle r="4" fill="{c}" stroke="none" filter="url(#tinyGlow)">'
                   f'<animate attributeName="opacity" values=".4;1;.4" dur="2.2s" repeatCount="indefinite"/></circle>')
        out.append('</g>')

        # tech badge chips (2-col, icon + name)
        badge_y_start = 170
        badge_w, badge_h = 142, 38
        badge_gap_x, badge_gap_y = 12, 10
        per_row = 2
        for j, tag in enumerate(p["tags"][:7]):
            display_name, icon_shape = tag
            col, row = j % per_row, j // per_row
            bx = 24 + col * (badge_w + badge_gap_x)
            by = badge_y_start + row * (badge_h + badge_gap_y)
            out.append(f'<g transform="translate({bx} {by})">')
            out.append(f'<rect width="{badge_w}" height="{badge_h}" rx="8" fill="{BG_0}" fill-opacity=".55" '
                       f'stroke="{c}" stroke-opacity=".30"/>')
            out.append(f'<g transform="translate(20 {badge_h//2})">{_tech_icon(icon_shape, c, 20)}</g>')
            out.append(f'<line x1="38" y1="7" x2="38" y2="{badge_h-7}" stroke="{c}" stroke-opacity=".22" stroke-width="0.8"/>')
            out.append(f'<text x="46" y="{badge_h//2 + 4}" fill="{TXT}" font-size="13" font-weight="600">{esc(display_name)}</text>')
            out.append('</g>')

        # divider + core toolchain
        divider_y = badge_y_start + 4 * (badge_h + badge_gap_y) - 4
        out.append(f'<line x1="24" y1="{divider_y}" x2="{panel_w-24}" y2="{divider_y}" stroke="{LINE_DARK}" stroke-width="1"/>')
        list_y = divider_y + 26
        out.append(f'<text x="24" y="{list_y}" fill="{c}" font-family="{MONO}" font-size="11" '
                   f'letter-spacing="2.5" opacity=".95">CORE TOOLCHAIN</text>')
        list_y += 26
        for k, item in enumerate(p["items"]):
            col, row = k % 2, k // 2
            ix = 24 + col * (panel_w - 48) // 2
            iy = list_y + row * 25
            out.append(f'<circle cx="{ix+4}" cy="{iy-4}" r="2.5" fill="{c}" opacity=".8"/>')
            out.append(f'<text x="{ix+14}" y="{iy}" fill="{TXT_2}" font-size="13">{esc(item)}</text>')

        # status footer
        sf_y = panel_h - 78
        out.append(f'<line x1="24" y1="{sf_y}" x2="{panel_w-24}" y2="{sf_y}" stroke="{LINE_DARK}" stroke-width="1"/>')
        out.append(f'<text x="24" y="{sf_y+22}" fill="{TXT_3}" font-family="{MONO}" font-size="10" letter-spacing="2">STATUS</text>')
        out.append(f'<text x="24" y="{sf_y+42}" fill="{TXT}" font-size="14" font-weight="700" letter-spacing="0.5">{esc(p["status_text"])}</text>')
        out.append(pulsing_dot(panel_w - 30, sf_y + 37, c, 5, 1.8, i * 0.2))
        out.append(progress_bar(24, sf_y + 52, panel_w - 48, p["pct"], c, 0.4 + i * 0.2))

        out.append('</g>')

    out.append('</g>')
    out.append(footer_block("PARSA @ KRAKEN // 4 DOMAINS // ENGINEERING STACK ONLINE", BLUE))
    out.append(svg_close())
    return ''.join(out)


# ============================================================================
# SECTION 2 - AI-NATIVE ENGINEERING  (accent: violet, pink support)
# ============================================================================
def _defs_ai():
    """Extra gradients for the 3D brain + eye icons (violet/pink/blue)."""
    return f'''<defs>
  <radialGradient id="brainGrad" cx="40%" cy="30%" r="80%">
    <stop offset="0" stop-color="#E4D4FF" stop-opacity=".95"/>
    <stop offset=".4" stop-color="#B98AFF" stop-opacity=".8"/>
    <stop offset=".75" stop-color="{VIOLET}" stop-opacity=".6"/>
    <stop offset="1" stop-color="#221040" stop-opacity=".85"/>
  </radialGradient>
  <linearGradient id="eyeScleraGrad" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#1C2733" stop-opacity=".95"/>
    <stop offset=".5" stop-color="#12161F" stop-opacity=".9"/>
    <stop offset="1" stop-color="{BG_1}" stop-opacity=".95"/>
  </linearGradient>
  <radialGradient id="irisGrad" cx="50%" cy="50%" r="50%">
    <stop offset="0" stop-color="{BG_0}"/>
    <stop offset=".3" stop-color="#122030" stop-opacity=".9"/>
    <stop offset=".6" stop-color="{BLUE}" stop-opacity=".65"/>
    <stop offset=".85" stop-color="#7DEFFF" stop-opacity=".85"/>
    <stop offset="1" stop-color="{BLUE}"/>
  </radialGradient>
  <linearGradient id="eyeRay" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{BLUE}" stop-opacity="0"/>
    <stop offset=".5" stop-color="{BLUE}" stop-opacity=".75"/>
    <stop offset="1" stop-color="{BLUE}" stop-opacity="0"/>
  </linearGradient>
  <linearGradient id="heroV" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#1B1430" stop-opacity=".9"/>
    <stop offset=".5" stop-color="#221638" stop-opacity=".85"/>
    <stop offset="1" stop-color="#181226" stop-opacity=".9"/>
  </linearGradient>
  <linearGradient id="titleV" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#B98AFF"/>
    <stop offset=".5" stop-color="{TXT}"/>
    <stop offset="1" stop-color="#9B6CFF"/>
  </linearGradient>
</defs>
'''


def _3d_brain_icon():
    """3D brain with slow Y-axis spin (scaleX fake perspective), violet."""
    return f'''<g>
  <animateTransform attributeName="transform" type="scale"
    values="1 1;0.45 1;-1 1;-0.45 1;-1 1;-0.45 1;1 1;0.45 1;1 1"
    keyTimes="0;0.125;0.25;0.375;0.5;0.625;0.75;0.875;1"
    dur="14s" repeatCount="indefinite"/>
  <g transform="scale(1.05)">
    <path d="M -2,-32 C -22,-38 -36,-25 -38,-8 C -44,4 -38,18 -28,28 C -22,38 -10,42 -2,38 L -2,-32 Z"
          fill="url(#brainGrad)" stroke="{VIOLET}" stroke-width="1.4" stroke-opacity=".7" filter="url(#glow)"/>
    <path d="M 2,-32 C 22,-38 36,-25 38,-8 C 44,4 38,18 28,28 C 22,38 10,42 2,38 L 2,-32 Z"
          fill="url(#brainGrad)" stroke="{VIOLET}" stroke-width="1.4" stroke-opacity=".7" filter="url(#glow)"/>
    <path d="M 0,-32 Q -2,-5 0,5 Q 2,20 0,38" fill="none" stroke="{PINK}" stroke-width="1.2" stroke-opacity=".55"/>
    <g fill="none" stroke="{VIOLET}" stroke-width="0.9" stroke-opacity=".55">
      <path d="M -22,-22 Q -14,-15 -8,-5 Q -5,5 -10,15"/>
      <path d="M -28,-12 Q -18,-8 -12,2 Q -8,12 -14,22"/>
      <path d="M -32,2 Q -22,8 -16,18 Q -12,28 -8,32"/>
      <path d="M -15,-28 Q -10,-18 -5,-10 Q 0,-2 -2,8"/>
    </g>
    <g fill="none" stroke="{VIOLET}" stroke-width="0.9" stroke-opacity=".55">
      <path d="M 22,-22 Q 14,-15 8,-5 Q 5,5 10,15"/>
      <path d="M 28,-12 Q 18,-8 12,2 Q 8,12 14,22"/>
      <path d="M 32,2 Q 22,8 16,18 Q 12,28 8,32"/>
      <path d="M 15,-28 Q 10,-18 5,-10 Q 0,-2 2,8"/>
    </g>
    <ellipse cx="-18" cy="-22" rx="10" ry="6" fill="#E4D4FF" opacity=".35" filter="url(#tinyGlow)"/>
    <ellipse cx="18" cy="-22" rx="10" ry="6" fill="#E4D4FF" opacity=".35" filter="url(#tinyGlow)"/>
    <g fill="#D9C7FF" filter="url(#tinyGlow)">
      <circle cx="-15" cy="-20" r="2.5"><animate attributeName="opacity" values=".4;1;.4" dur="1.5s" repeatCount="indefinite"/></circle>
      <circle cx="-25" cy="-5" r="2"><animate attributeName="opacity" values="1;.3;1" dur="1.9s" repeatCount="indefinite"/></circle>
      <circle cx="-9" cy="12" r="2"><animate attributeName="opacity" values=".5;1;.5" dur="1.3s" begin=".4s" repeatCount="indefinite"/></circle>
      <circle cx="15" cy="-20" r="2.5"><animate attributeName="opacity" values=".4;1;.4" dur="1.7s" begin=".2s" repeatCount="indefinite"/></circle>
      <circle cx="25" cy="-5" r="2"><animate attributeName="opacity" values="1;.3;1" dur="2.1s" begin=".6s" repeatCount="indefinite"/></circle>
      <circle cx="9" cy="12" r="2"><animate attributeName="opacity" values=".5;1;.5" dur="1.5s" begin=".8s" repeatCount="indefinite"/></circle>
      <circle cx="0" cy="30" r="2"><animate attributeName="opacity" values=".4;1;.4" dur="1.6s" begin="1s" repeatCount="indefinite"/></circle>
    </g>
  </g>
</g>'''


def _3d_eye_icon():
    """3D scanning eye, electric-blue iris with pink ray sweep."""
    return f'''<g>
  <g transform="scale(1.08)">
    <path d="M -46,0 Q 0,-34 46,0 Q 0,34 -46,0 Z"
          fill="url(#eyeScleraGrad)" stroke="{BLUE}" stroke-width="1.4" stroke-opacity=".6" filter="url(#glow)"/>
    <path d="M -46,0 Q 0,-34 46,0 Q 0,34 -46,0 Z" fill="none" stroke="{PINK}" stroke-width="0.8" stroke-opacity=".28"/>
    <circle r="17" fill="url(#irisGrad)" filter="url(#glow)"/>
    <circle r="17" fill="none" stroke="{BLUE}" stroke-opacity=".55"/>
    <circle r="6.5" fill="{BG_1}"/>
    <circle cx="-4" cy="-6" r="2.2" fill="#EAFBFF" opacity=".85" filter="url(#tinyGlow)"/>
    <rect x="-46" y="-9" width="92" height="18" fill="url(#eyeRay)" opacity=".5">
      <animate attributeName="y" values="-9;9;-9" dur="4.2s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="0;.55;0" dur="4.2s" repeatCount="indefinite"/>
    </rect>
    <g fill="none" stroke="{BLUE}" stroke-opacity=".5">
      <path d="M -58,-12 Q -46,-8 -46,0" >
        <animate attributeName="stroke-opacity" values=".1;.6;.1" dur="2.4s" repeatCount="indefinite"/></path>
      <path d="M 58,-12 Q 46,-8 46,0">
        <animate attributeName="stroke-opacity" values=".6;.1;.6" dur="2.4s" repeatCount="indefinite"/></path>
    </g>
    <g fill="#7DEFFF" filter="url(#tinyGlow)">
      <circle cx="-34" cy="-9" r="1.8"><animate attributeName="opacity" values=".3;1;.3" dur="2s" repeatCount="indefinite"/></circle>
      <circle cx="34" cy="-9" r="1.8"><animate attributeName="opacity" values="1;.3;1" dur="2.3s" repeatCount="indefinite"/></circle>
      <circle cx="0" cy="22" r="1.5"><animate attributeName="opacity" values=".4;1;.4" dur="1.8s" begin=".5s" repeatCount="indefinite"/></circle>
    </g>
  </g>
</g>'''


def section_ai_native_engineering():
    out = [svg_open()]
    out.append(defs_common())
    out.append(_defs_ai())
    out.append(background("glowV", "glowP"))

    # ---------------------------------------------------------- hero banner
    out.append(f'''<g>
  <rect x="30" y="28" width="{W-60}" height="170" rx="16" fill="url(#heroV)" stroke="{VIOLET}" stroke-opacity=".35"/>
  {ticks(W-60, 170, VIOLET, 12, .5)}
  <path d="M-100 195L470 20 M160 205L730 20 M450 205L1020 20
           M740 205L1310 20 M1030 205L1600 20 M1320 205L1890 20"
        stroke="{VIOLET}" stroke-opacity=".08" stroke-width="1.5">
    <animateTransform attributeName="transform" type="translate" values="0 0;90 0;0 0" dur="10s" repeatCount="indefinite"/>
  </path>
  <g stroke-opacity=".9">
    <g fill="none" stroke="{PINK}" stroke-opacity=".35" stroke-width="1.2">
      <path d="M1180 82L1260 52L1340 95L1420 60L1510 110L1580 70"/>
      <path d="M1210 150L1280 112L1360 142L1440 102L1530 150"/>
      <path d="M1260 52L1280 112M1340 95L1360 142M1420 60L1440 102M1510 110L1530 150"/>
    </g>
    <g fill="{PINK}" filter="url(#tinyGlow)">
      <circle cx="1180" cy="82" r="4"><animate attributeName="opacity" values=".3;1;.3" dur="2.1s" repeatCount="indefinite"/></circle>
      <circle cx="1260" cy="52" r="4"><animate attributeName="opacity" values="1;.3;1" dur="1.8s" repeatCount="indefinite"/></circle>
      <circle cx="1340" cy="95" r="4"><animate attributeName="opacity" values=".4;1;.4" dur="2.4s" repeatCount="indefinite"/></circle>
      <circle cx="1420" cy="60" r="4"><animate attributeName="opacity" values=".5;1;.5" dur="1.6s" begin=".3s" repeatCount="indefinite"/></circle>
      <circle cx="1510" cy="110" r="4"><animate attributeName="opacity" values=".3;1;.3" dur="2s" begin=".5s" repeatCount="indefinite"/></circle>
      <circle cx="1580" cy="70" r="4"><animate attributeName="opacity" values="1;.4;1" dur="1.9s" begin=".2s" repeatCount="indefinite"/></circle>
    </g>
    <g fill="{BLUE}" filter="url(#tinyGlow)">
      <circle cx="1210" cy="150" r="3"><animate attributeName="opacity" values=".4;1;.4" dur="2.2s" repeatCount="indefinite"/></circle>
      <circle cx="1280" cy="112" r="3"><animate attributeName="opacity" values="1;.3;1" dur="1.7s" begin=".4s" repeatCount="indefinite"/></circle>
      <circle cx="1360" cy="142" r="3"><animate attributeName="opacity" values=".4;1;.4" dur="2s" begin=".8s" repeatCount="indefinite"/></circle>
      <circle cx="1440" cy="102" r="3"><animate attributeName="opacity" values=".5;1;.5" dur="1.8s" begin=".1s" repeatCount="indefinite"/></circle>
      <circle cx="1530" cy="150" r="3"><animate attributeName="opacity" values=".4;1;.4" dur="2.3s" begin=".6s" repeatCount="indefinite"/></circle>
    </g>
  </g>
  <circle cx="1370" cy="100" r="125" fill="none" stroke="{VIOLET}" stroke-opacity=".18" stroke-width="1" stroke-dasharray="4 12">
    <animateTransform attributeName="transform" type="rotate" from="0 1370 100" to="360 1370 100" dur="18s" repeatCount="indefinite"/>
  </circle>
</g>
<text x="{W//2}" y="118" text-anchor="middle" font-family="{SANS}" font-size="54" font-weight="800" letter-spacing="2" fill="url(#titleV)">
  AI-NATIVE ENGINEERING
  <animate attributeName="opacity" values=".85;1;.85" dur="4s" repeatCount="indefinite"/>
</text>
<text x="{W//2}" y="152" text-anchor="middle" font-family="{MONO}" font-size="12" letter-spacing="4" fill="{TXT_3}">
  INTELLIGENCE / RETRIEVAL / AUTOMATION / CONTEXT
</text>
<rect x="662" y="172" width="340" height="1.5" fill="{VIOLET}" opacity=".5">
  <animate attributeName="width" values="240;420;240" dur="5s" repeatCount="indefinite"/>
  <animate attributeName="x" values="712;622;712" dur="5s" repeatCount="indefinite"/>
</rect>
''')

    # ------------------------------------------------------ AI system core pipe
    out.append(f'''<g font-family="{MONO}">
  <text x="{W//2}" y="240" text-anchor="middle" fill="{VIOLET}" font-size="10" letter-spacing="3">AI SYSTEM CORE</text>
  <path d="M650 266H1014" stroke="{VIOLET}" stroke-opacity=".22" stroke-width="2"/>
  <path d="M650 266H1014" stroke="{PINK}" stroke-opacity=".7" stroke-width="1.5" stroke-dasharray="2 14">
    <animate attributeName="stroke-dashoffset" values="0;-64" dur="1.4s" repeatCount="indefinite"/>
  </path>
  <circle cx="650" cy="266" r="5" fill="{PINK}" filter="url(#glow)">
    <animate attributeName="r" values="3;8;3" dur="1.4s" repeatCount="indefinite"/>
  </circle>
  <circle cx="1014" cy="266" r="5" fill="{BLUE}" filter="url(#glow)">
    <animate attributeName="r" values="3;8;3" dur="1.7s" repeatCount="indefinite"/>
  </circle>
</g>
''')

    # ------------------------------------------------------------- two AI cards
    ai_cards = [
        {
            "num":  "01",
            "kind": "GENERATIVE INTELLIGENCE",
            "title": "LLM APPLICATIONS",
            "sub":  "MODELS / PROMPTS / AGENTS / CONTEXT",
            "items": ["LangChain", "RAG Pipelines", "Vector DBs", "Prompt Engineering", "Fine-tuning", "Function Calling"],
            "pct":  95,
            "color": VIOLET,
            "panel": "panelV",
        },
        {
            "num":  "02",
            "kind": "PERCEPTUAL INTELLIGENCE",
            "title": "VISION & ML",
            "sub":  "IMAGES / VIDEO / PATTERNS / INFERENCE",
            "items": ["Image Processing", "Machine Vision", "OpenCV", "PyTorch", "TensorFlow", "Real-time Inference"],
            "pct":  95,
            "color": BLUE,
            "panel": "panelB",
        },
    ]

    card_xs, card_w, card_h, card_y = [180, 880], 624, 444, 292
    out.append(f'<g font-family="{SANS}">')
    for i, c in enumerate(ai_cards):
        x, acc = card_xs[i], c["color"]
        out.append(f'<g transform="translate({x} {card_y})">')
        out.append(f'<rect width="{card_w}" height="{card_h}" rx="16" fill="url(#{c["panel"]})" '
                   f'stroke="{acc}" stroke-opacity=".30"/>')
        out.append(ticks(card_w - 2, card_h - 2, acc, 12, .5))
        out.append(f'<rect x="28" y="26" width="26" height="2" fill="{acc}"/>')
        out.append(f'<text x="28" y="52" fill="{acc}" font-family="{MONO}" font-size="11" letter-spacing="3">{c["num"]} / {c["kind"]}</text>')

        icon_x = card_w // 2
        out.append(f'<g transform="translate({icon_x} 122)">')
        out.append(f'<circle r="74" fill="url(#{"glowV" if i == 0 else "glowB"})" opacity=".6">')
        out.append(f'<animate attributeName="r" values="58;84;58" dur="4.5s" begin="{i*0.5}s" repeatCount="indefinite"/></circle>')
        out.append(f'<circle r="61" fill="none" stroke="{acc}" stroke-opacity=".22" stroke-dasharray="3 10">')
        out.append(f'<animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="12s" repeatCount="indefinite"/></circle>')
        out.append(_3d_brain_icon() if i == 0 else _3d_eye_icon())
        out.append('</g>')

        out.append(f'<text x="28" y="228" fill="{TXT}" font-size="28" font-weight="800">{esc(c["title"])}</text>')
        out.append(f'<text x="28" y="252" fill="{TXT_3}" font-family="{MONO}" font-size="10" letter-spacing="1.5">{esc(c["sub"])}</text>')

        items_y = 288
        col_w = (card_w - 60) // 3
        for k, item in enumerate(c["items"]):
            col, row = k % 3, k // 3
            ix = 28 + col * col_w
            iy = items_y + row * 30
            out.append(f'<g transform="translate({ix} {iy})">')
            out.append(f'<rect width="{col_w-8}" height="22" rx="6" fill="{BG_0}" fill-opacity=".55" stroke="{acc}" stroke-opacity=".26"/>')
            out.append(f'<circle cx="13" cy="11" r="2.5" fill="{acc}"/>')
            out.append(f'<text x="22" y="15" fill="{TXT_2}" font-size="11">{esc(item)}</text>')
            out.append('</g>')

        sf_y = card_h - 40
        out.append(f'<line x1="28" y1="{sf_y-10}" x2="{card_w-28}" y2="{sf_y-10}" stroke="{LINE_DARK}" stroke-width="1"/>')
        out.append(f'<text x="28" y="{sf_y+10}" fill="{TXT_3}" font-family="{MONO}" font-size="10" letter-spacing="2">DEPLOYMENT</text>')
        out.append(f'<text x="28" y="{sf_y+28}" fill="{TXT}" font-size="13" font-weight="700">INFERENCE ONLINE</text>')
        out.append(pulsing_dot(card_w - 32, sf_y + 23, acc, 5, 1.7, i * 0.3))
        out.append(progress_bar(28, sf_y + 38, card_w - 56, c["pct"], acc, 0.4 + i * 0.3))
        out.append('</g>')

    out.append('</g>')

    # ------------------------------------------------------ architecture strips
    arch_layers = [
        ("PRESENTATION",  ["React.js", "Vue.js 3", "Next.js"], BLUE),
        ("API GATEWAY",   ["RESTful API", "GraphQL", "JWT Auth"], VIOLET),
        ("BUSINESS LOGIC", ["Node.js", "Django/FastAPI", "C# (.NET)"], PINK),
        ("AI / ML",       ["PyTorch", "TensorFlow", "LangChain"], YELLOW),
        ("INFRASTRUCTURE", ["Docker", "Kubernetes", "Nginx"], BLUE),
    ]
    layer_y, layer_h = 774, 58
    strip_w = (W - 80 - 4 * 12) // 5
    for i, (name, items, acc) in enumerate(arch_layers):
        x = 40 + i * (strip_w + 12)
        out.append(f'<g transform="translate({x} {layer_y})">')
        out.append(f'<rect width="{strip_w}" height="{layer_h}" rx="10" fill="url(#panel)" stroke="{acc}" stroke-opacity=".3"/>')
        out.append(f'<rect width="3" height="{layer_h}" rx="1.5" fill="{acc}" opacity=".85"/>')
        out.append(f'<text x="16" y="21" fill="{acc}" font-family="{MONO}" font-size="9.5" letter-spacing="2">{name}</text>')
        bx = 16
        for item in items[:3]:
            tw = len(item) * 6.2 + 16
            out.append(f'<g transform="translate({bx:.0f} 30)">')
            out.append(f'<rect width="{tw:.0f}" height="20" rx="6" fill="{BG_0}" fill-opacity=".5" stroke="{acc}" stroke-opacity=".24"/>')
            out.append(f'<text x="{tw/2:.0f}" y="14" text-anchor="middle" fill="{TXT_2}" font-size="9">{esc(item)}</text>')
            out.append('</g>')
            bx += tw + 7
        out.append('</g>')

    out.append(footer_block("AI-NATIVE ARCHITECTURE // LAYERED // OBSERVABLE // RESILIENT", VIOLET))
    out.append(svg_close())
    return ''.join(out)


# ============================================================================
# SECTION 3 - CAREER TRAJECTORY  (accent: neon pink timeline)
# ============================================================================
CAREER = [
    {
        "start": 2019, "end": 2020,
        "role": "Game Developer",
        "company": "Golad Game & Animation Studio",
        "location": "Kermanshah",
        "tag": "GAME_DEV",
        "color": BLUE, "panel": "panelB",
        "bullets": [
            "C# / C++ gameplay programming",
            "Unreal Engine & Unity 3D engines",
            "3D Max modeling & character design"
        ]
    },
    {
        "start": 2020, "end": 2022,
        "role": "Web Designer & SEO Engineer",
        "company": "Koosha Rayan Co.",
        "location": "Ilam",
        "tag": "WEB_SEO",
        "color": VIOLET, "panel": "panelV",
        "bullets": [
            "HTML5 / CSS3 / JS / Vue.js 3",
            "WordPress + WooCommerce customization",
            "UI optimization & technical SEO"
        ]
    },
    {
        "start": 2022, "end": None,
        "role": "Programming Instructor",
        "company": "Computer Technical-Vocational School",
        "location": "Kermanshah",
        "tag": "TEACHING",
        "color": PINK, "panel": "panelP",
        "bullets": [
            "Frontend / Backend / Database",
            "Python / Node.js / MySQL / Linux",
            "Algorithms, data structures, OOP"
        ]
    },
    {
        "start": 2025, "end": None,
        "role": "Technical Manager",
        "company": "sup",
        "location": "Kermanshah",
        "tag": "TECH_LEAD",
        "color": YELLOW, "panel": "panelY",
        "bullets": [
            "Team leadership & technical planning",
            "Software architecture & code reviews",
            "Product lifecycle & mentorship"
        ]
    },
]


def section_career_trajectory():
    out = [svg_open()]
    out.append(defs_common())
    out.append(background("glowP", "glowV"))
    out.append(header_block("03", "CAREER TRAJECTORY",
                            "TIMELINE / 4 ROLES / 6+ YEARS / ACTIVE: 2", PINK))

    timeline_y = 530
    tl_x1, tl_x2 = 80, W - 80

    # base line + travelling dash pulse (pink core)
    out.append(f'<line x1="{tl_x1}" y1="{timeline_y}" x2="{tl_x2}" y2="{timeline_y}" stroke="{PINK}" stroke-opacity=".28" stroke-width="2"/>')
    out.append(f'<line x1="{tl_x1}" y1="{timeline_y}" x2="{tl_x2}" y2="{timeline_y}" stroke="{PINK}" stroke-width="1.6" stroke-dasharray="6 18" filter="url(#tinyGlow)">'
               f'<animate attributeName="stroke-dashoffset" values="0;-192" dur="6s" repeatCount="indefinite"/></line>')

    # year markers
    year_marks = [2019, 2020, 2022, 2025, "now"]
    for i, y in enumerate(year_marks):
        x = tl_x1 + int((tl_x2 - tl_x1) * i / (len(year_marks) - 1))
        out.append(f'<line x1="{x}" y1="{timeline_y-9}" x2="{x}" y2="{timeline_y+9}" stroke="{PINK}" stroke-width="1.5" stroke-opacity=".75"/>')
        col = YELLOW if y == "now" else TXT_2
        out.append(f'<text x="{x}" y="{timeline_y+30}" text-anchor="middle" font-family="{MONO}" font-size="13" font-weight="700" fill="{col}">{y}</text>')

    # 4 career cards alternating above/below
    card_w, card_h = 360, 280
    positions = [
        (tl_x1 + 60,  timeline_y - card_h - 52),
        (tl_x1 + 310, timeline_y + 52),
        (tl_x1 + 700, timeline_y - card_h - 52),
        (tl_x1 + 1050, timeline_y + 52),
    ]
    for i, job in enumerate(CAREER):
        card_x, card_y = positions[i]
        c = job["color"]
        period = f"{job['start']}" + (f" - {job['end']}" if job['end'] else " - now")

        connector_y_start = card_y + card_h if card_y < timeline_y else card_y
        out.append(f'<line x1="{card_x + card_w//2}" y1="{connector_y_start}" x2="{card_x + card_w//2}" y2="{timeline_y}" '
                   f'stroke="{c}" stroke-width="1.2" stroke-opacity=".55" stroke-dasharray="3 5"/>')

        out.append(f'<g transform="translate({card_x} {card_y})">')
        out.append(f'<rect width="{card_w}" height="{card_h}" rx="14" fill="url(#{job["panel"]})" stroke="{c}" stroke-opacity=".32"/>')
        out.append(ticks(card_w - 2, card_h - 2, c, 11, .5))

        # period chip + tag
        out.append(f'<rect x="20" y="18" width="138" height="26" rx="7" fill="{BG_0}" fill-opacity=".6" stroke="{c}" stroke-opacity=".5"/>')
        out.append(f'<text x="89" y="35" text-anchor="middle" font-family="{MONO}" font-size="12" font-weight="700" fill="{c}">{period}</text>')
        out.append(f'<rect x="{card_w-96}" y="18" width="76" height="26" rx="7" fill="{BG_0}" fill-opacity=".6" stroke="{c}" stroke-opacity=".5"/>')
        out.append(f'<text x="{card_w-58}" y="35" text-anchor="middle" font-family="{MONO}" font-size="11" font-weight="700" fill="{c}">{esc(job["tag"])}</text>')

        # role + company + location
        out.append(f'<text x="20" y="78" fill="{TXT}" font-size="21" font-weight="800">{esc(job["role"])}</text>')
        out.append(f'<text x="20" y="102" fill="{TXT_2}" font-size="13">{esc(job["company"])}</text>')
        out.append(f'<text x="20" y="121" font-family="{MONO}" font-size="11" fill="{TXT_3}">[ {esc(job["location"])} ]</text>')

        out.append(f'<line x1="20" y1="136" x2="{card_w-20}" y2="136" stroke="{LINE_DARK}" stroke-width="1"/>')

        by = 162
        for b in job["bullets"]:
            out.append(f'<circle cx="29" cy="{by-4}" r="2.5" fill="{c}"/>')
            truncated = b if len(b) < 42 else b[:40] + "..."
            out.append(f'<text x="42" y="{by}" fill="{TXT_2}" font-size="12.5">{esc(truncated)}</text>')
            by += 24

        out.append(f'<line x1="20" y1="{card_h-20}" x2="{card_w-20}" y2="{card_h-20}" stroke="{LINE_DARK}" stroke-width="0.8"/>')
        out.append(pulsing_dot(card_w - 28, card_h - 10, c, 4, 2.2, i * 0.3))
        out.append('</g>')

        # milestone dot on timeline
        cx = card_x + card_w // 2
        out.append(f'<circle cx="{cx}" cy="{timeline_y}" r="9" fill="{BG_0}" stroke="{c}" stroke-width="2"/>')
        out.append(f'<circle cx="{cx}" cy="{timeline_y}" r="3" fill="{c}" filter="url(#tinyGlow)"/>')

    out.append(footer_block("4 ROLES // 6+ YEARS // BUILDING - TEACHING - LEADING", PINK))
    out.append(svg_close())
    return ''.join(out)


# ============================================================================
# SECTION 4 - EDUCATION & KNOWLEDGE  (accent: electric blue)
# ============================================================================
EDUCATION = [
    {
        "degree": "M.Sc. Artificial Intelligence",
        "field":  "Artificial Intelligence",
        "school": "Islamic Azad University, Hamedan",
        "city":   "Hamedan",
        "period": "1404 - present",
        "gpa":    "In progress",
        "color":  VIOLET, "panel": "panelV",
        "status": "Current Student",
    },
    {
        "degree": "Bachelor of Computer Engineering",
        "field":  "Software",
        "school": "Islamic Azad University, Kermanshah",
        "city":   "Kermanshah",
        "period": "1402 - 1404",
        "gpa":    "18.5",
        "color":  BLUE, "panel": "panelB",
        "status": "Completed",
    },
    {
        "degree": "Associate Degree in Computer Engineering",
        "field":  "Software",
        "school": "Ilam National Skills University",
        "city":   "Ilam",
        "period": "1400 - 1402",
        "gpa":    "17.70",
        "color":  PINK, "panel": "panelP",
        "status": "Completed",
    },
]

LANGUAGES = [
    ("English", [("Reading", 4), ("Writing", 4), ("Speaking", 3), ("Listening", 4)], BLUE),
]

BADGES = [
    ("Clean Arch",       100, BLUE),
    ("RESTful API",      100, VIOLET),
    ("React.js",         100, PINK),
    ("PostgreSQL",       100, YELLOW),
    ("Docker",           100, BLUE),
    ("Linux Admin",      100, VIOLET),
    ("Machine Learning",  95, PINK),
    ("Tech Lead",        100, YELLOW),
]


def section_education_knowledge():
    out = [svg_open()]
    out.append(defs_common())
    out.append(background("glowB", "glowV"))
    out.append(header_block("04", "EDUCATION & KNOWLEDGE",
                            "ACADEMIC RECORD / LANGUAGES / CONTINUOUS LEARNING", BLUE))

    card_x, card_w, card_h, card_gap = 50, 800, 200, 16
    card_y_start = 210

    out.append(f'<text x="{card_x}" y="186" fill="{BLUE}" font-family="{MONO}" font-size="11" letter-spacing="3">// ACADEMIC RECORD</text>')

    for i, edu in enumerate(EDUCATION):
        cy = card_y_start + i * (card_h + card_gap)
        c = edu["color"]
        out.append(f'<g transform="translate({card_x} {cy})">')
        out.append(f'<rect width="{card_w}" height="{card_h}" rx="14" fill="url(#{edu["panel"]})" stroke="{c}" stroke-opacity=".30"/>')
        out.append(ticks(card_w - 2, card_h - 2, c, 11, .45))
        out.append(f'<rect x="0" y="14" width="2.5" height="{card_h-28}" fill="{c}" opacity=".8"/>')

        # period + status chips
        out.append(f'<rect x="22" y="18" width="148" height="24" rx="6" fill="{BG_0}" fill-opacity=".6" stroke="{c}" stroke-opacity=".45"/>')
        out.append(f'<text x="96" y="34" text-anchor="middle" font-family="{MONO}" font-size="11" fill="{c}">{esc(edu["period"])}</text>')
        st_col = YELLOW if edu["status"] == "Current Student" else c
        out.append(f'<rect x="{card_w-136}" y="18" width="116" height="24" rx="6" fill="{st_col}" fill-opacity=".10" stroke="{st_col}" stroke-opacity=".4"/>')
        out.append(f'<text x="{card_w-78}" y="34" text-anchor="middle" font-family="{MONO}" font-size="10" fill="{st_col}">{esc(edu["status"].upper())}</text>')
        if edu["status"] == "Current Student":
            out.append(pulsing_dot(card_w - 144, 30, YELLOW, 3.5, 1.6))

        # degree + field + school
        out.append(f'<text x="24" y="72" fill="{TXT}" font-size="21" font-weight="800">{esc(edu["degree"])}</text>')
        out.append(f'<text x="24" y="97" fill="{c}" font-family="{MONO}" font-size="11">// FIELD: <tspan fill="{TXT_2}">{esc(edu["field"].upper())}</tspan></text>')
        out.append(f'<text x="24" y="119" fill="{TXT_2}" font-size="13">{esc(edu["school"])}</text>')
        out.append(f'<text x="24" y="138" font-family="{MONO}" font-size="11" fill="{TXT_3}">[ {esc(edu["city"])} ]</text>')

        # GPA or "in progress"
        if edu["gpa"] != "In progress":
            out.append(f'<rect x="{card_w-130}" y="{card_h-56}" width="106" height="32" rx="8" fill="{c}" fill-opacity=".10" stroke="{c}" stroke-opacity=".45"/>')
            out.append(f'<text x="{card_w-77}" y="{card_h-35}" text-anchor="middle" font-family="{MONO}" font-size="13" fill="{c}">GPA {esc(edu["gpa"])}</text>')
        else:
            out.append(f'<rect x="{card_w-208}" y="{card_h-56}" width="184" height="32" rx="8" fill="{YELLOW}" fill-opacity=".08" stroke="{YELLOW}" stroke-opacity=".4"/>')
            out.append(f'<text x="{card_w-116}" y="{card_h-35}" text-anchor="middle" font-family="{MONO}" font-size="10.5" fill="{YELLOW}">CURRENTLY STUDYING</text>')

        out.append('</g>')

    # right column: languages + mastery badges
    right_x, right_w = 900, 714
    out.append(f'<text x="{right_x}" y="186" fill="{BLUE}" font-family="{MONO}" font-size="11" letter-spacing="3">// LANGUAGES</text>')

    lang_y = 210
    for lang_name, skills, color in LANGUAGES:
        out.append(f'<g transform="translate({right_x} {lang_y})">')
        out.append(f'<rect width="{right_w}" height="104" rx="14" fill="url(#panelB)" stroke="{color}" stroke-opacity=".30"/>')
        out.append(ticks(right_w - 2, 102, color, 11, .45))
        out.append(f'<text x="24" y="40" fill="{TXT}" font-size="19" font-weight="800">{esc(lang_name)}</text>')
        bx, bw = 160, 132
        for skill_name, level in skills:
            out.append(f'<text x="{bx}" y="34" font-family="{MONO}" font-size="9.5" fill="{TXT_3}" letter-spacing="1.5">{esc(skill_name.upper())}</text>')
            for k in range(5):
                dx, dy = bx + k * 14, 48
                if k < level:
                    out.append(f'<circle cx="{dx}" cy="{dy}" r="4.5" fill="{color}" filter="url(#tinyGlow)">'
                               f'<animate attributeName="opacity" values=".5;1;.5" dur="1.7s" begin="{k*0.15}s" repeatCount="indefinite"/></circle>')
                else:
                    out.append(f'<circle cx="{dx}" cy="{dy}" r="4" fill="none" stroke="{color}" stroke-width="0.9" stroke-opacity=".35"/>')
            bx += bw
        out.append(f'<text x="24" y="82" font-family="{MONO}" font-size="10" fill="{TXT_3}" letter-spacing="1">// CEFR-EQUIV: <tspan fill="{color}">B2</tspan></text>')
        out.append('</g>')

    badge_y = lang_y + 104 + 30
    out.append(f'<text x="{right_x}" y="{badge_y - 14}" fill="{BLUE}" font-family="{MONO}" font-size="11" letter-spacing="3">// MASTERY BADGES</text>')
    badge_w, badge_h, per_row = 172, 32, 4
    for i, (name, pct, color) in enumerate(BADGES):
        col, row = i % per_row, i // per_row
        x = right_x + col * (badge_w + 9)
        y = badge_y + row * (badge_h + 9)
        out.append(f'<g transform="translate({x} {y})">')
        out.append(f'<rect width="{badge_w}" height="{badge_h}" rx="8" fill="{BG_0}" fill-opacity=".55" stroke="{color}" stroke-opacity=".42"/>')
        out.append(pulsing_dot(16, badge_h // 2, color, 3.5, 2.0, i * 0.15))
        out.append(f'<text x="28" y="{badge_h//2 + 4}" fill="{TXT_2}" font-size="11">{esc(name)}</text>')
        out.append(f'<text x="{badge_w-8}" y="{badge_h//2 + 4}" text-anchor="end" font-family="{MONO}" font-size="10" fill="{color}">{pct}%</text>')
        out.append('</g>')

    out.append(footer_block("LEARNING IS CONTINUOUS // THE ARCHITECT NEVER STOPS REFINING THE CRAFT", BLUE))
    out.append(svg_close())
    return ''.join(out)


# ============================================================================
# SECTION 5 - CONTACT NETWORK  (accent rotation per endpoint)
# ============================================================================
CONTACTS = [
    {"key": "EMAIL",    "value": "mrparsataheri1@gmail.com", "color": BLUE,   "panel": "panelB", "icon": "envelope"},
    {"key": "TELEGRAM", "value": "@p2002t",                  "color": VIOLET, "panel": "panelV", "icon": "send"},
    {"key": "LINKEDIN", "value": "parsa-taheri-781b90355",   "color": PINK,   "panel": "panelP", "icon": "linkedin"},
    {"key": "GITHUB",   "value": "parsa-kraken",             "color": BLUE,   "panel": "panelB", "icon": "github"},
    {"key": "LOCATION", "value": "Tehran, Iran",             "color": YELLOW, "panel": "panelY", "icon": "pin"},
    {"key": "WEBSITE",  "value": "parsataheri.com",          "color": VIOLET, "panel": "panelV", "icon": "globe"},
]

CONTACT_META = {
    "EMAIL":    "// PGP available on request",
    "TELEGRAM": "// fastest response channel",
    "LINKEDIN": "// professional network",
    "GITHUB":   "// primary code hub",
    "LOCATION": "// UTC+3:30 / IRST",
    "WEBSITE":  "// personal portfolio / open",
}


def _icon_path(name, color):
    """Minimal line-style contact icon, 24x24 viewBox, centered at (12,12)."""
    hi = TXT
    if name == "envelope":
        return (f'<g fill="none" stroke="{color}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">'
                f'<rect x="2.5" y="5.5" width="19" height="13" rx="2.5" fill="{color}" fill-opacity=".14"/>'
                f'<path d="M 3 7 L 12 13.5 L 21 7"/>'
                f'<line x1="3" y1="6.5" x2="21" y2="6.5" stroke="{hi}" stroke-opacity=".5" stroke-width="0.8"/></g>')
    if name == "send":
        return (f'<g fill="none" stroke="{color}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">'
                f'<path d="M 3.5 11.5 L 21.5 3.5 L 13 21 L 11 13.5 Z" fill="{color}" fill-opacity=".14"/>'
                f'<line x1="11" y1="13.5" x2="21.5" y2="3.5" stroke="{hi}" stroke-opacity=".55" stroke-width="1"/></g>')
    if name == "linkedin":
        return (f'<g fill="none" stroke="{color}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">'
                f'<rect x="3" y="3" width="18" height="18" rx="3" fill="{color}" fill-opacity=".14"/>'
                f'<line x1="7.5" y1="10.5" x2="7.5" y2="17"/>'
                f'<circle cx="7.5" cy="7.4" r="1.1" fill="{color}" stroke="none"/>'
                f'<path d="M 11.5 17 L 11.5 10.5 M 11.5 13 C 12.4 10.8 16.5 10.4 16.5 13.4 L 16.5 17"/></g>')
    if name == "github":
        return (f'<g fill="none" stroke="{color}" stroke-width="1.5" stroke-linejoin="round">'
                f'<path d="M 12 2.5 C 6.5 2.5 2.5 6.6 2.5 11.9 C 2.5 16.2 5.3 19.9 9.2 21.2 C 9.7 21.3 9.9 21 9.9 20.7 L 9.9 18.9 C 7.2 19.5 6.6 17.8 6.6 17.8 C 6.2 16.7 5.6 16.4 5.6 16.4 C 4.8 15.9 5.7 15.9 5.7 15.9 C 6.6 16 7.1 16.9 7.1 16.9 C 7.9 18.3 9.3 17.9 9.8 17.6 C 9.9 17 10.1 16.6 10.4 16.3 C 8.2 16 5.9 15.2 5.9 11.5 C 5.9 10.5 6.3 9.6 6.9 9 C 6.8 8.7 6.4 7.8 7 6.4 C 7 6.4 7.9 6.1 9.7 7.3 C 10.5 7.1 11.3 7 12 7 C 12.7 7 13.5 7.1 14.3 7.3 C 16.1 6.1 17 6.4 17 6.4 C 17.6 7.8 17.2 8.7 17.1 9 C 17.7 9.6 18.1 10.5 18.1 11.5 C 18.1 15.2 15.8 16 13.6 16.3 C 14 16.7 14.2 17.3 14.2 18.2 L 14.2 20.7 C 14.2 21 14.4 21.3 14.9 21.2 C 18.8 19.9 21.5 16.2 21.5 11.9 C 21.5 6.6 17.5 2.5 12 2.5 Z" '
                f'fill="{color}" fill-opacity=".14"/></g>')
    if name == "pin":
        return (f'<g fill="none" stroke="{color}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">'
                f'<path d="M 12 2.5 C 7.9 2.5 4.5 5.8 4.5 9.9 C 4.5 15.4 12 21.5 12 21.5 C 12 21.5 19.5 15.4 19.5 9.9 C 19.5 5.8 16.1 2.5 12 2.5 Z" fill="{color}" fill-opacity=".14"/>'
                f'<circle cx="12" cy="9.9" r="2.6"/>'
                f'<circle cx="11" cy="8.8" r="0.9" fill="{hi}" stroke="none" opacity=".8"/></g>')
    if name == "globe":
        return (f'<g fill="none" stroke="{color}" stroke-width="1.4" stroke-linecap="round">'
                f'<circle cx="12" cy="12" r="9.5" fill="{color}" fill-opacity=".14"/>'
                f'<line x1="2.5" y1="12" x2="21.5" y2="12"/>'
                f'<path d="M 12 2.5 C 8.5 6 8.5 18 12 21.5 C 15.5 18 15.5 6 12 2.5 Z"/>'
                f'<path d="M 4.5 6.5 Q 12 9 19.5 6.5" stroke-opacity=".6"/>'
                f'<path d="M 4.5 17.5 Q 12 15 19.5 17.5" stroke-opacity=".6"/></g>')
    return ''


def section_contact_network():
    out = [svg_open()]
    out.append(defs_common())
    out.append(background("glowV", "glowB"))
    out.append(header_block("05", "CONTACT NETWORK",
                            "6 ENDPOINTS / OPEN FOR COLLABORATION / RESPONSE_TIME: <24H", VIOLET))

    card_w, card_h, gap = 480, 280, 24
    grid_w = 3 * card_w + 2 * gap
    grid_x = (W - grid_w) // 2
    grid_y = 210

    for i, c in enumerate(CONTACTS):
        col, row = i % 3, i // 3
        x = grid_x + col * (card_w + gap)
        y = grid_y + row * (card_h + gap)
        acc = c["color"]

        out.append(f'<g transform="translate({x} {y})">')
        out.append(f'<rect width="{card_w}" height="{card_h}" rx="14" fill="url(#{c["panel"]})" stroke="{acc}" stroke-opacity=".30"/>')
        out.append(ticks(card_w - 2, card_h - 2, acc, 11, .5))

        out.append(f'<text x="24" y="42" font-family="{MONO}" font-size="13" letter-spacing="3" font-weight="700" fill="{acc}">// {esc(c["key"])}</text>')
        out.append(pulsing_dot(card_w - 28, 36, acc, 5, 1.8, i * 0.2))

        # icon
        out.append(f'<g transform="translate({card_w//2 - 30} 76) scale(2.5)">')
        out.append(_icon_path(c["icon"], acc))
        out.append('</g>')

        # subtle orbit ring
        out.append(f'<g transform="translate({card_w//2} 148)" fill="none" stroke="{acc}">')
        out.append(f'<circle r="34" stroke-opacity=".20" stroke-dasharray="4 9">')
        out.append(f'<animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="12s" repeatCount="indefinite"/></circle>')
        out.append('</g>')

        out.append(f'<text x="{card_w//2}" y="206" text-anchor="middle" fill="{TXT}" font-size="22" font-weight="700">{esc(c["value"])}</text>')

        out.append(f'<line x1="24" y1="{card_h-34}" x2="{card_w-24}" y2="{card_h-34}" stroke="{LINE_DARK}" stroke-width="1"/>')
        out.append(f'<text x="{card_w//2}" y="{card_h-13}" text-anchor="middle" font-family="{MONO}" font-size="11.5" fill="{TXT_3}" letter-spacing="1.5">{esc(CONTACT_META[c["key"]])}</text>')

        out.append('</g>')

    out.append(footer_block("REACH OUT // LET US ENGINEER SOMETHING WORTH SHIPPING TOGETHER", VIOLET))
    out.append(svg_close())
    return ''.join(out)


# ============================================================================
# SECTION 6 - LIVE GITHUB STATS  (particle network, 4 accents)
# ============================================================================
def section_live_github_stats():
    out = [svg_open()]
    out.append(defs_common())
    out.append(background("glowB", "glowV"))

    # particle network (deterministic)
    random.seed(42)
    particles = []
    for _ in range(42):
        x = random.randint(70, W - 70)
        y = random.randint(70, H - 70)
        z = random.choice([1, 2, 3])
        particles.append((x, y, z))

    pcolors = [BLUE, VIOLET, PINK, BLUE, VIOLET]
    out.append('<g stroke="#6F5BFF" stroke-opacity=".07" stroke-width="1">')
    for i, (x1, y1, z1) in enumerate(particles):
        for j, (x2, y2, z2) in enumerate(particles):
            if i >= j:
                continue
            dist = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
            if dist < 190:
                out.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/>')
    out.append('</g>')

    out.append('<g filter="url(#tinyGlow)">')
    for i, (x, y, z) in enumerate(particles):
        r = z * 1.1 + 1.3
        pc = pcolors[i % len(pcolors)]
        drift = 10 + z * 4
        dur = 6 + z * 2
        out.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{pc}" opacity=".6">')
        out.append(f'<animate attributeName="cy" values="{y};{y-drift};{y+drift//2};{y}" dur="{dur}s" begin="{i*0.1}s" repeatCount="indefinite"/>')
        out.append(f'<animate attributeName="opacity" values=".3;.8;.3" dur="{dur/2:.1f}s" begin="{i*0.15}s" repeatCount="indefinite"/></circle>')
    out.append('</g>')

    # hero panel
    hero_w, hero_h = 900, 380
    hero_x, hero_y = (W - hero_w) // 2, (H - hero_h) // 2

    out.append(f'<g transform="translate({hero_x} {hero_y})" font-family="{SANS}">')
    out.append(f'<rect width="{hero_w}" height="{hero_h}" rx="18" fill="url(#panel)" stroke="{VIOLET}" stroke-opacity=".35"/>')
    out.append(ticks(hero_w - 2, hero_h - 2, VIOLET, 13, .55))

    out.append(f'<text x="{hero_w//2}" y="58" text-anchor="middle" font-family="{MONO}" font-size="11" letter-spacing="4" fill="{BLUE}" opacity=".9">06 // REAL-TIME TELEMETRY</text>')
    out.append(f'<text x="{hero_w//2}" y="100" text-anchor="middle" font-size="36" font-weight="800" letter-spacing="2" fill="{TXT}">LIVE GITHUB STATS</text>')
    out.append(f'<text x="{hero_w//2}" y="128" text-anchor="middle" font-family="{MONO}" font-size="11" letter-spacing="3.5" fill="{TXT_3}">REPOSITORIES / STARS / FOLLOWERS / CONTRIBUTIONS</text>')
    out.append(f'<rect x="290" y="146" width="320" height="1.5" fill="{PINK}" opacity=".5">')
    out.append(f'<animate attributeName="width" values="220;400;220" dur="5s" repeatCount="indefinite"/>')
    out.append(f'<animate attributeName="x" values="340;240;340" dur="5s" repeatCount="indefinite"/></rect>')

    # 3 top stat cells
    top_y, top_h, top_w = 172, 110, (hero_w - 80) // 3
    stats_top = [
        ("REPOSITORIES", "PARS-KRAKEN", "LIVE PULL",   BLUE),
        ("STARS",        "EARNED",      "REAL-TIME",   VIOLET),
        ("FOLLOWERS",    "NETWORK",     "GROWING",     PINK),
    ]
    for i, (label, sub, status, acc) in enumerate(stats_top):
        sx = 30 + i * (top_w + 10)
        out.append(f'<g transform="translate({sx} {top_y})">')
        out.append(f'<rect width="{top_w}" height="{top_h}" rx="10" fill="{BG_0}" fill-opacity=".55" stroke="{acc}" stroke-opacity=".4"/>')
        out.append(f'<rect x="14" y="14" width="22" height="2" fill="{acc}"/>')
        out.append(f'<text x="{top_w//2}" y="40" text-anchor="middle" font-family="{MONO}" font-size="10.5" letter-spacing="2.5" fill="{acc}">{esc(label)}</text>')
        out.append(f'<text x="{top_w//2}" y="72" text-anchor="middle" font-size="23" font-weight="800" fill="{TXT}">{esc(sub)}</text>')
        out.append(f'<text x="{top_w//2}" y="92" text-anchor="middle" font-family="{MONO}" font-size="9" letter-spacing="1.2" fill="{TXT_3}">{esc(status)}</text>')
        out.append(pulsing_dot(top_w - 16, 17, acc, 3.5, 1.7, i * 0.2))
        out.append('</g>')

    # bottom wide cell - yellow highlight
    bot_y, bot_h = 300, 62
    out.append(f'<g transform="translate(30 {bot_y})">')
    out.append(f'<rect width="{hero_w-60}" height="{bot_h}" rx="10" fill="{YELLOW}" fill-opacity=".05" stroke="{YELLOW}" stroke-opacity=".45"/>')
    out.append(f'<text x="26" y="26" font-family="{MONO}" font-size="10.5" letter-spacing="3" fill="{YELLOW}">// TOTAL REPOSITORIES</text>')
    out.append(f'<text x="26" y="50" font-size="26" font-weight="800" fill="{TXT}">ALL PUBLIC + PRIVATE REPOS</text>')
    out.append(f'<text x="{hero_w-92}" y="26" text-anchor="end" font-family="{MONO}" font-size="9.5" letter-spacing="1.5" fill="{TXT_3}">LIVE FROM GITHUB API</text>')
    out.append(pulsing_dot(hero_w - 80, 48, YELLOW, 5, 1.4))
    out.append('</g>')

    out.append('</g>')

    out.append(footer_block("LIVE DATA // SYNCED FROM GITHUB API // REFRESH EVERY LOAD", BLUE))
    out.append(svg_close())
    return ''.join(out)


# ============================================================================
# MAIN - write all 6 sections
# ============================================================================
def main():
    sections = [
        ("01-tech-universe.svg",         section_tech_universe()),
        ("02-ai-native-engineering.svg", section_ai_native_engineering()),
        ("03-career-trajectory.svg",     section_career_trajectory()),
        ("04-education-knowledge.svg",   section_education_knowledge()),
        ("05-contact-network.svg",       section_contact_network()),
        ("06-live-github-stats.svg",     section_live_github_stats()),
    ]
    # remove old-named outputs if present (02-system-architecture / 06-unified-stats)
    for old in ("02-system-architecture.svg", "06-unified-stats.svg"):
        p = SECTIONS / old
        if p.exists():
            p.unlink()
            print(f"  removed stale {old}")
    for fname, content in sections:
        path = SECTIONS / fname
        path.write_text(content, encoding="utf-8")
        print(f"  wrote {path.name}  ({len(content)} bytes)")


if __name__ == "__main__":
    main()
