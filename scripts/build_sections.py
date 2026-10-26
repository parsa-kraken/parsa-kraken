#!/usr/bin/env python3
"""
Generate 5 green-themed GitHub profile section SVGs for Parsa Taheri.

Sections (reskinned to match shinobi-coder's actual UI style):
  1. TECHNOLOGY UNIVERSE     — 4 vertical panels with animated nodes + tech badges
  2. SYSTEM ARCHITECTURE     — hero banner + AI pipe + AI cards (with AI/ML pipeline)
  3. CAREER TRAJECTORY       — 4 timeline cards
  4. EDUCATION & KNOWLEDGE  — 3 education cards + languages + mastery badges
  5. CONTACT NETWORK         — 6 contact cards (website replaces status)
  6. UNIFIED STATS           — particle.js-style unified stats panel

Visual language (extracted from shinobi-coder SVGs):
  - Deep forest green gradient background (#020b07 → #061812 → #02100a)
  - Animated grid pattern (small 12px + large 42px) drifting diagonally
  - Ambient radial halos with soft glow filter
  - Top centered title: large bold sans-serif (Arial) with subtle opacity pulse
  - Subtitle: small monospace with letter-spacing, dim green
  - Animated neon underline rect that grows/shrinks
  - Floating particles with tiny glow filter
  - Panel cards: 4-22px rounded, glassmorphism fill, green stroke, top accent bar
  - Status indicators: pulsing dots with tiny glow filter
  - Tech badges: 62x62 rounded squares with double-stroke detail

Size: 1664x936 (matches shinobi-coder's reference dimensions).
"""
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape
import json

# Resolve paths relative to the project root (parent of this scripts/ folder).
ROOT = Path(__file__).resolve().parent.parent
SECTIONS = ROOT / "sections"
SECTIONS.mkdir(exist_ok=True)


def esc(s):
    """XML-escape text content (& < >)."""
    return xml_escape(str(s))


# ============================================================================
# SHINOBI-STYLE DESIGN TOKENS
# ============================================================================
# Color palette extracted directly from shinobi-coder's SVGs
BG_DEEP        = "#020b07"   # near-black green
BG_MID         = "#061812"   # dark forest
BG_LIGHT       = "#02100a"
PANEL_FILL_TOP = "#102a1d"   # panel gradient top (96% opacity)
PANEL_FILL_BOT = "#06150e"   # panel gradient bottom
NEON_GREEN    = "#25ff78"    # main neon accent
NEON_BRIGHT   = "#8affb4"    # bright variant
NEON_DEEP     = "#39ff82"    # deep variant
HALO_COLOR    = "#1dff6b"
TEXT_PRIMARY  = "#edfff4"    # near-white green-tinted
TEXT_HEADER   = "#dffff0"    # primary header
TEXT_SECOND   = "#75ad8c"    # secondary text
TEXT_DIM      = "#68ad83"    # dim text
TEXT_MUTED    = "#8aaaa1"
LABEL_GREEN   = "#65ff9b"    # numbered label color
ACCENT_GREEN  = "#6cff9d"
BORDER_GREEN  = "#4bff8a"
BORDER_FADED  = "rgba(75,255,138,0.30)"

# Tech badge colors per group (variety)
GROUP_COLORS = [
    NEON_BRIGHT,   # Frontend
    "#7dffaa",     # Backend
    NEON_DEEP,     # Data
    "#9affba",     # Cloud
    NEON_GREEN,    # AI
    "#baffd0",     # DevOps
    "#d8ffe5",     # Leadership
    "#75ff9f",     # Process
]

W = 1664
H = 936


# ============================================================================
# SHARED DEFS (matches shinobi's exact gradient/filter/pattern setup)
# ============================================================================
def defs_shinobi():
    """Shinobi's exact defs block — gradients, filters, patterns, badges."""
    return f'''<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{BG_DEEP}"/>
    <stop offset=".48" stop-color="{BG_MID}"/>
    <stop offset="1" stop-color="{BG_LIGHT}"/>
  </linearGradient>
  <linearGradient id="panel" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{PANEL_FILL_TOP}" stop-opacity=".96"/>
    <stop offset="1" stop-color="{PANEL_FILL_BOT}" stop-opacity=".97"/>
  </linearGradient>
  <linearGradient id="neon" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{NEON_GREEN}" stop-opacity="0"/>
    <stop offset=".5" stop-color="{NEON_BRIGHT}"/>
    <stop offset="1" stop-color="{NEON_GREEN}" stop-opacity="0"/>
  </linearGradient>
  <linearGradient id="greenText" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{NEON_BRIGHT}"/>
    <stop offset=".5" stop-color="{NEON_DEEP}"/>
    <stop offset="1" stop-color="{NEON_BRIGHT}"/>
  </linearGradient>
  <radialGradient id="halo">
    <stop offset="0" stop-color="{NEON_DEEP}" stop-opacity=".28"/>
    <stop offset=".45" stop-color="{HALO_COLOR}" stop-opacity=".08"/>
    <stop offset="1" stop-color="{HALO_COLOR}" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="orb">
    <stop offset="0" stop-color="{NEON_DEEP}" stop-opacity=".55"/>
    <stop offset="1" stop-color="{HALO_COLOR}" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="hero" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#06150e" stop-opacity=".95"/>
    <stop offset=".5" stop-color="#0a2218" stop-opacity=".85"/>
    <stop offset="1" stop-color="#06150e" stop-opacity=".95"/>
  </linearGradient>
  <linearGradient id="scan" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{NEON_GREEN}" stop-opacity="0"/>
    <stop offset=".5" stop-color="{NEON_BRIGHT}"/>
    <stop offset="1" stop-color="{NEON_GREEN}" stop-opacity="0"/>
  </linearGradient>

  <!-- 3D Brain gradient (top-light to bottom-dark for hemisphere shading) -->
  <radialGradient id="brainGrad" cx="40%" cy="30%" r="80%">
    <stop offset="0" stop-color="#baffd0" stop-opacity=".95"/>
    <stop offset=".4" stop-color="{NEON_BRIGHT}" stop-opacity=".75"/>
    <stop offset=".75" stop-color="{NEON_GREEN}" stop-opacity=".55"/>
    <stop offset="1" stop-color="#072914" stop-opacity=".85"/>
  </radialGradient>
  <!-- 3D Eye sclera gradient (top-light to bottom-dark) -->
  <linearGradient id="eyeScleraGrad" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#1a3a25" stop-opacity=".95"/>
    <stop offset=".5" stop-color="#0c2117" stop-opacity=".9"/>
    <stop offset="1" stop-color="#06150e" stop-opacity=".95"/>
  </linearGradient>
  <!-- 3D Iris gradient (dark center, bright ring, dark edge) -->
  <radialGradient id="irisGrad" cx="50%" cy="50%" r="50%">
    <stop offset="0" stop-color="#020b07"/>
    <stop offset=".3" stop-color="#0a2218" stop-opacity=".9"/>
    <stop offset=".6" stop-color="{NEON_GREEN}" stop-opacity=".7"/>
    <stop offset=".85" stop-color="{NEON_BRIGHT}" stop-opacity=".9"/>
    <stop offset="1" stop-color="{NEON_DEEP}"/>
  </radialGradient>
  <!-- Eye glow accent (scanning ray gradient) -->
  <linearGradient id="eyeRay" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{NEON_BRIGHT}" stop-opacity="0"/>
    <stop offset=".5" stop-color="{NEON_BRIGHT}" stop-opacity=".8"/>
    <stop offset="1" stop-color="{NEON_BRIGHT}" stop-opacity="0"/>
  </linearGradient>
  <pattern id="grid" width="42" height="42" patternUnits="userSpaceOnUse">
    <path d="M42 0H0V42" fill="none" stroke="#6aff9c" stroke-opacity=".055"/>
    <circle cx="0" cy="0" r="1" fill="{NEON_BRIGHT}" opacity=".18"/>
  </pattern>
  <pattern id="smallGrid" width="12" height="12" patternUnits="userSpaceOnUse">
    <path d="M12 0H0V12" fill="none" stroke="#7bffa9" stroke-opacity=".022"/>
  </pattern>
  <filter id="glow" x="-100%" y="-100%" width="300%" height="300%">
    <feGaussianBlur stdDeviation="5" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <filter id="softGlow" x="-100%" y="-100%" width="300%" height="300%">
    <feGaussianBlur stdDeviation="16"/>
  </filter>
  <filter id="tinyGlow" x="-100%" y="-100%" width="300%" height="300%">
    <feGaussianBlur stdDeviation="2"/>
  </filter>

  <!-- Tech badge (shinobi style) -->
  <g id="badge">
    <rect x="-31" y="-31" width="62" height="62" rx="15"
          fill="#0c2117" stroke="{NEON_GREEN}" stroke-opacity=".28"/>
    <rect x="-27" y="-27" width="54" height="54" rx="12"
          fill="none" stroke="{NEON_BRIGHT}" stroke-opacity=".08"/>
    <circle r="21" fill="none" stroke="#52ff91" stroke-opacity=".11"/>
  </g>

  <!-- Pulsing status dot -->
  <g id="status">
    <circle r="4" fill="#73ffa5" filter="url(#tinyGlow)">
      <animate attributeName="r" values="2.5;5;2.5" dur="1.7s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values=".35;1;.35" dur="1.7s" repeatCount="indefinite"/>
    </circle>
  </g>

  <!-- Corner decorations -->
  <g id="cornerTL">
    <path d="M0 30 V0 H30" fill="none" stroke="{NEON_GREEN}" stroke-width="1.5" stroke-opacity=".5"/>
  </g>
  <g id="cornerTR">
    <path d="M0 30 V0 H-30" fill="none" stroke="{NEON_GREEN}" stroke-width="1.5" stroke-opacity=".5"/>
  </g>
  <g id="cornerBL">
    <path d="M0 -30 V0 H30" fill="none" stroke="{NEON_GREEN}" stroke-width="1.5" stroke-opacity=".5"/>
  </g>
  <g id="cornerBR">
    <path d="M0 -30 V0 H-30" fill="none" stroke="{NEON_GREEN}" stroke-width="1.5" stroke-opacity=".5"/>
  </g>
</defs>
'''


def svg_open(w=W, h=H):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" preserveAspectRatio="xMidYMid meet">\n'
    )


def svg_close():
    return "</svg>\n"


def background_shinobi():
    """Shinobi's exact background block: bg gradient + animated grids + halo."""
    return f'''<rect width="{W}" height="{H}" fill="url(#bg)"/>
<rect width="{W}" height="{H}" fill="url(#grid)">
  <animateTransform attributeName="transform" type="translate"
    values="0 0;42 42;0 0" dur="16s" repeatCount="indefinite"/>
</rect>
<rect width="{W}" height="{H}" fill="url(#smallGrid)" opacity=".6">
  <animateTransform attributeName="transform" type="translate"
    values="0 0;-12 12;0 0" dur="9s" repeatCount="indefinite"/>
</rect>
<ellipse cx="{W//2}" cy="270" rx="540" ry="300" fill="url(#halo)" filter="url(#softGlow)">
  <animate attributeName="rx" values="460;600;480;570;460" dur="9s" repeatCount="indefinite"/>
  <animate attributeName="ry" values="250;340;270;320;250" dur="9s" repeatCount="indefinite"/>
  <animate attributeName="opacity" values=".55;.9;.48;.8;.55" dur="9s" repeatCount="indefinite"/>
</ellipse>
'''


def header_block(title, subtitle, title_y=84, sub_y=123, underline_y=146):
    """Shinobi-style centered header with pulsing title, dim sub, animated neon underline."""
    return f'''<g font-family="Arial, Helvetica, sans-serif" text-anchor="middle">
  <text x="{W//2}" y="{title_y}" fill="{TEXT_HEADER}" font-size="48" font-weight="700" letter-spacing="1">
    {esc(title)}
    <animate attributeName="opacity" values=".84;1;.84" dur="4s" repeatCount="indefinite"/>
  </text>
  <text x="{W//2}" y="{sub_y}" fill="{ACCENT_GREEN}" font-size="15" letter-spacing="4" opacity=".72">
    {esc(subtitle)}
  </text>
  <rect x="575" y="{underline_y}" width="514" height="1.5" fill="url(#neon)">
    <animate attributeName="width" values="350;620;350" dur="5s" repeatCount="indefinite"/>
    <animate attributeName="x" values="657;522;657" dur="5s" repeatCount="indefinite"/>
  </rect>
</g>
<!-- Floating header particles -->
<g fill="{NEON_BRIGHT}" filter="url(#tinyGlow)">
  <circle cx="270" cy="90" r="2"><animate attributeName="cy" values="90;72;90" dur="3s" repeatCount="indefinite"/></circle>
  <circle cx="1390" cy="105" r="1.5"><animate attributeName="cy" values="105;128;105" dur="4s" repeatCount="indefinite"/></circle>
  <circle cx="460" cy="142" r="1.3"><animate attributeName="cx" values="460;485;460" dur="3.5s" repeatCount="indefinite"/></circle>
  <circle cx="1190" cy="135" r="1.7"><animate attributeName="cx" values="1190;1165;1190" dur="4.2s" repeatCount="indefinite"/></circle>
</g>
'''


def corners_block():
    """Shinobi-style corner brackets at the 4 corners of the SVG canvas."""
    return f'''<use href="#cornerTL" transform="translate(20,20)"/>
<use href="#cornerTR" transform="translate({W-20},20)"/>
<use href="#cornerBL" transform="translate(20,{H-20})"/>
<use href="#cornerBR" transform="translate({W-20},{H-20})"/>
'''


def footer_block(text="// systems connected // continuous delivery //"):
    """Shinobi-style centered footer with dot prefix/suffix."""
    return f'''<g font-family="monospace" font-size="11" fill="{ACCENT_GREEN}" letter-spacing="3" opacity=".7" text-anchor="middle">
  <circle cx="{W//2 - 240}" cy="{H-22}" r="2" fill="{ACCENT_GREEN}"/>
  <text x="{W//2}" y="{H-18}">{esc(text)}</text>
  <circle cx="{W//2 + 240}" cy="{H-22}" r="2" fill="{ACCENT_GREEN}"/>
</g>
'''


# ============================================================================
# SECTION 1 — TECHNOLOGY UNIVERSE
# (4 vertical panels: Frontend, Backend, AI/ML, Cloud — each with tech badges,
#  animated node network, status indicator, progress bar)
# ============================================================================
TECH_PANELS = [
    {
        "num":  "01",
        "kind": "INTERFACE",
        "title": "FRONTEND",
        "sub":  "Experience • Components • Interaction",
        "color": NEON_BRIGHT,
        "tags":  ["RE", "N", "TS", "V", "NG", "TW", "SCSS"],
        "items": ["React", "Next.js", "TypeScript", "Vue.js 3", "Tailwind", "Three.js"],
        "status_text": "COMPONENTS ONLINE",
        "pct":   85,
    },
    {
        "num":  "02",
        "kind": "LOGIC",
        "title": "BACKEND",
        "sub":  "APIs • Services • Distributed Systems",
        "color": "#7dffaa",
        "tags":  ["JS", "PY", "DJ", "FL", "API", "μSVC"],
        "items": ["Node.js", "Python", "Django", "FastAPI", "REST APIs", "GraphQL"],
        "status_text": "SERVICES SYNCHRONIZED",
        "pct":   90,
    },
    {
        "num":  "03",
        "kind": "INTELLIGENCE",
        "title": "AI / ML",
        "sub":  "Vision • Learning • Inference",
        "color": NEON_GREEN,
        "tags":  ["CV", "ML", "DL", "PT", "TF", "HF", "LC"],
        "items": ["OpenCV", "PyTorch", "TensorFlow", "Machine Learning", "Deep Learning", "LangChain"],
        "status_text": "MODELS TRAINED",
        "pct":   95,
    },
    {
        "num":  "04",
        "kind": "INFRASTRUCTURE",
        "title": "CLOUD",
        "sub":  "Scale • Containers • Automation",
        "color": "#9affba",
        "tags":  ["AWS", "AZ", "GCP", "DK", "K8S", "NGX"],
        "items": ["Docker", "Kubernetes", "Nginx", "AWS", "Azure", "GCP", "CI/CD"],
        "status_text": "CLUSTERS OPERATIONAL",
        "pct":   88,
    },
]


def section_tech_universe():
    out = [svg_open()]
    out.append(defs_shinobi())
    out.append(background_shinobi())
    out.append(header_block("TECHNOLOGY UNIVERSE",
                            "ENGINEERING STACK / SYSTEMS / INFRASTRUCTURE / INTELLIGENCE"))
    out.append(corners_block())

    # 4 panels — calculate x positions (4 panels, 350 wide, gap 24, total 1432 + margins 116 each side = 1664)
    panel_w = 350
    panel_h = 650
    panel_y = 190
    gap = (W - 80 - 4 * panel_w) // 3  # ~24px gap
    panel_xs = [40 + i * (panel_w + gap) for i in range(4)]

    out.append(f'<g font-family="Arial, Helvetica, sans-serif">')
    for i, p in enumerate(TECH_PANELS):
        x = panel_xs[i]
        c = p["color"]

        # Outer glow rect
        out.append(f'<g transform="translate({x} {panel_y})">')
        out.append(f'<rect width="{panel_w}" height="{panel_h}" rx="22" fill="{NEON_GREEN}" opacity=".035" filter="url(#softGlow)"/>')
        # Inner panel with gradient
        out.append(f'<rect x="4" y="4" width="{panel_w-8}" height="{panel_h-8}" rx="20" fill="url(#panel)" stroke="{BORDER_GREEN}" stroke-opacity=".30"/>')
        # Top accent bar
        out.append(f'<rect x="4" y="4" width="{panel_w-8}" height="6" rx="3" fill="{c}" opacity=".5">')
        out.append(f'<animate attributeName="opacity" values=".25;.8;.25" dur="3.5s" begin="{i*0.4}s" repeatCount="indefinite"/></rect>')

        # Number + kind label
        out.append(f'<text x="28" y="46" fill="{LABEL_GREEN}" font-size="12" letter-spacing="3">{p["num"]} / {p["kind"]}</text>')
        # Title
        out.append(f'<text x="28" y="88" fill="{TEXT_PRIMARY}" font-size="31" font-weight="700">{p["title"]}</text>')
        # Subtitle
        out.append(f'<text x="28" y="115" fill="{TEXT_SECOND}" font-size="12">{esc(p["sub"])}</text>')

        # Animated node network (top right of panel)
        out.append(f'<g transform="translate({panel_w-76} 73)" fill="none" stroke="{c}">')
        out.append(f'<circle r="39" stroke-opacity=".14" stroke-dasharray="3 8">')
        out.append(f'<animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="8s" repeatCount="indefinite"/></circle>')
        out.append(f'<circle r="25" stroke-opacity=".25">')
        out.append(f'<animate attributeName="r" values="21;29;21" dur="2.4s" begin="{i*0.3}s" repeatCount="indefinite"/></circle>')
        out.append(f'<path d="M-17 0H17M0-17V17" stroke-opacity=".28"/>')
        out.append(f'<circle r="4" fill="{NEON_BRIGHT}" stroke="none">')
        out.append(f'<animate attributeName="r" values="2;6;2" dur="1.5s" begin="{i*0.2}s" repeatCount="indefinite"/></circle>')
        out.append('</g>')

        # Tech badges (grid of small rounded squares)
        badge_y_start = 180
        badge_size = 50
        badge_gap = 14
        # 3 cols x 3 rows max
        per_row = 3
        for j, tag in enumerate(p["tags"][:9]):
            col = j % per_row
            row = j // per_row
            bx = 28 + col * (badge_size + badge_gap)
            by = badge_y_start + row * (badge_size + badge_gap)
            out.append(f'<g transform="translate({bx + badge_size//2} {by + badge_size//2})">')
            out.append(f'<rect x="-{badge_size//2}" y="-{badge_size//2}" width="{badge_size}" height="{badge_size}" rx="12" '
                       f'fill="#0c2117" stroke="{c}" stroke-opacity=".28"/>')
            out.append(f'<text text-anchor="middle" y="5" fill="{c}" font-family="monospace" font-size="11" font-weight="700">{esc(tag)}</text>')
            out.append('</g>')

        # Divider
        out.append(f'<line x1="28" y1="{badge_y_start + 3*(badge_size+badge_gap) - 6}" x2="{panel_w-28}" y2="{badge_y_start + 3*(badge_size+badge_gap) - 6}" stroke="{c}" stroke-width="0.5" stroke-opacity=".2"/>')

        # List section
        list_y = badge_y_start + 3*(badge_size+badge_gap) + 10
        out.append(f'<text x="28" y="{list_y}" fill="{c}" font-size="10" letter-spacing="1.5" font-family="monospace" opacity=".8">CORE TOOLCHAIN</text>')
        list_y += 22
        for k, item in enumerate(p["items"]):
            col = k % 2
            row = k // 2
            ix = 28 + col * (panel_w - 56) // 2
            iy = list_y + row * 22
            out.append(f'<text x="{ix}" y="{iy}" fill="{TEXT_PRIMARY}" font-size="12">{esc(item)}</text>')

        # Status footer
        sf_y = panel_h - 80
        out.append(f'<line x1="28" y1="{sf_y}" x2="{panel_w-28}" y2="{sf_y}" stroke="{c}" stroke-width="0.5" stroke-opacity=".15"/>')
        out.append(f'<text x="28" y="{sf_y+20}" fill="{TEXT_SECOND}" font-size="10" letter-spacing="1" font-family="monospace">STATUS</text>')
        out.append(f'<text x="28" y="{sf_y+38}" fill="{TEXT_PRIMARY}" font-size="13" font-weight="600" letter-spacing="0.5">{esc(p["status_text"])}</text>')
        # Status dot (pulsing)
        out.append(f'<circle cx="{panel_w-32}" cy="{sf_y+33}" r="5" fill="{c}" filter="url(#tinyGlow)">')
        out.append(f'<animate attributeName="r" values="3;6;3" dur="1.7s" repeatCount="indefinite"/>')
        out.append(f'<animate attributeName="opacity" values=".5;1;.5" dur="1.7s" repeatCount="indefinite"/></circle>')
        # Progress bar
        out.append(f'<rect x="28" y="{sf_y+50}" width="{panel_w-56}" height="4" rx="2" fill="rgba(255,255,255,0.08)"/>')
        fill_w = int((panel_w - 56) * p["pct"] / 100)
        out.append(f'<rect x="28" y="{sf_y+50}" width="0" height="4" rx="2" fill="{c}" filter="url(#glow)">')
        out.append(f'<animate attributeName="width" from="0" to="{fill_w}" dur="1.6s" begin="{0.4 + i*0.2}s" fill="freeze" calcMode="spline" keySplines="0.25 0.1 0.25 1"/></rect>')

        out.append('</g>')  # close panel group

    out.append('</g>')  # close outer group

    out.append(footer_block("PARSA @ KRAKEN // 4 DOMAINS // ENGINEERING STACK ONLINE"))
    out.append(svg_close())
    return ''.join(out)


# ============================================================================
# SECTION 2 — SYSTEM ARCHITECTURE
# (Hero banner + AI pipe + 2 AI cards with neural network icons)
# ============================================================================
def _3d_brain_icon():
    """3D brain icon for the LLM / Generative Intelligence card.

    Two organic hemispheres with curved sulci (grooves), shaded with a
    radial gradient for spherical 3D depth. Highlight at top-left to
    simulate light source. Pulsing neural nodes scattered across the
    surface. Slight wobble animation for "thinking" feel.
    """
    return f'''<g transform="scale(1.05)">
  <!-- Subtle brain pulse (entire brain breathes) -->
  <g>
    <animateTransform attributeName="transform" type="scale"
      values="1;1.04;1" dur="3.5s" repeatCount="indefinite"
      calcMode="spline" keySplines="0.4 0 0.6 1; 0.4 0 0.6 1" keyTimes="0;0.5;1"/>

    <!-- LEFT HEMISPHERE: organic blob shape -->
    <path d="M -2,-32
             C -22,-38 -36,-25 -38,-8
             C -44,4 -38,18 -28,28
             C -22,38 -10,42 -2,38
             L -2,-32 Z"
          fill="url(#brainGrad)"
          stroke="{NEON_GREEN}" stroke-width="1.4" stroke-opacity=".7"
          filter="url(#glow)"/>

    <!-- RIGHT HEMISPHERE: mirror of left -->
    <path d="M 2,-32
             C 22,-38 36,-25 38,-8
             C 44,4 38,18 28,28
             C 22,38 10,42 2,38
             L 2,-32 Z"
          fill="url(#brainGrad)"
          stroke="{NEON_GREEN}" stroke-width="1.4" stroke-opacity=".7"
          filter="url(#glow)"/>

    <!-- Central fissure (the line separating the two hemispheres) -->
    <path d="M 0,-32 Q -2,-5 0,5 Q 2,20 0,38"
          fill="none" stroke="{NEON_GREEN}" stroke-width="1.2" stroke-opacity=".55"/>

    <!-- SULCI (curved grooves) on LEFT hemisphere -->
    <g fill="none" stroke="{NEON_GREEN}" stroke-width="0.9" stroke-opacity=".5">
      <path d="M -22,-22 Q -14,-15 -8,-5 Q -5,5 -10,15"/>
      <path d="M -28,-12 Q -18,-8 -12,2 Q -8,12 -14,22"/>
      <path d="M -32,2 Q -22,8 -16,18 Q -12,28 -8,32"/>
      <path d="M -15,-28 Q -10,-18 -5,-10 Q 0,-2 -2,8"/>
    </g>

    <!-- SULCI on RIGHT hemisphere (mirror) -->
    <g fill="none" stroke="{NEON_GREEN}" stroke-width="0.9" stroke-opacity=".5">
      <path d="M 22,-22 Q 14,-15 8,-5 Q 5,5 10,15"/>
      <path d="M 28,-12 Q 18,-8 12,2 Q 8,12 14,22"/>
      <path d="M 32,2 Q 22,8 16,18 Q 12,28 8,32"/>
      <path d="M 15,-28 Q 10,-18 5,-10 Q 0,-2 2,8"/>
    </g>

    <!-- 3D highlight (top-left, simulating light source) -->
    <ellipse cx="-18" cy="-22" rx="10" ry="6"
             fill="{NEON_BRIGHT}" opacity=".4" filter="url(#tinyGlow)"/>
    <ellipse cx="18" cy="-22" rx="10" ry="6"
             fill="{NEON_BRIGHT}" opacity=".4" filter="url(#tinyGlow)"/>

    <!-- Neural nodes scattered on brain surface (pulsing) -->
    <g fill="#baffd0" filter="url(#tinyGlow)">
      <circle cx="-15" cy="-20" r="2.5">
        <animate attributeName="opacity" values=".4;1;.4" dur="1.5s" repeatCount="indefinite"/>
      </circle>
      <circle cx="-25" cy="-5" r="2.5">
        <animate attributeName="opacity" values=".4;1;.4" dur="1.5s" begin="0.3s" repeatCount="indefinite"/>
      </circle>
      <circle cx="-20" cy="15" r="2.5">
        <animate attributeName="opacity" values=".4;1;.4" dur="1.5s" begin="0.6s" repeatCount="indefinite"/>
      </circle>
      <circle cx="-8" cy="25" r="2.5">
        <animate attributeName="opacity" values=".4;1;.4" dur="1.5s" begin="0.9s" repeatCount="indefinite"/>
      </circle>
      <circle cx="15" cy="-20" r="2.5">
        <animate attributeName="opacity" values=".4;1;.4" dur="1.5s" begin="0.15s" repeatCount="indefinite"/>
      </circle>
      <circle cx="25" cy="-5" r="2.5">
        <animate attributeName="opacity" values=".4;1;.4" dur="1.5s" begin="0.45s" repeatCount="indefinite"/>
      </circle>
      <circle cx="20" cy="15" r="2.5">
        <animate attributeName="opacity" values=".4;1;.4" dur="1.5s" begin="0.75s" repeatCount="indefinite"/>
      </circle>
      <circle cx="8" cy="25" r="2.5">
        <animate attributeName="opacity" values=".4;1;.4" dur="1.5s" begin="1.05s" repeatCount="indefinite"/>
      </circle>
    </g>

    <!-- Synaptic connections (faint) -->
    <g fill="none" stroke="#baffd0" stroke-width="0.6" stroke-opacity=".35">
      <path d="M -15,-20 L -25,-5 L -20,15 L -8,25 L 8,25 L 20,15 L 25,-5 L 15,-20 Z"/>
      <path d="M -15,-20 L 15,-20 M -25,-5 L 25,-5 M -20,15 L 20,15"/>
    </g>

    <!-- Brain stem (small protrusion at bottom) -->
    <path d="M -5,38 Q -3,46 0,48 Q 3,46 5,38"
          fill="url(#brainGrad)" stroke="{NEON_GREEN}" stroke-width="1" stroke-opacity=".6"/>
  </g>
</g>
'''


def _3d_eye_icon():
    """3D eye icon for the Vision / Perceptual Intelligence card.

    Almond-shaped eye with a 3D iris (radial gradient: dark center to
    bright ring) and pupil. Highlight on pupil simulates cornea reflection.
    Animated scanning rays sweep around the iris to suggest active vision.
    Subtle eye-blink animation: the eye lid scales vertically every few
    seconds to look alive.
    """
    return f'''<g transform="scale(1.15)">

  <!-- Eye wobble + blink group -->
  <g>
    <animateTransform attributeName="transform" type="scale"
      values="1 1; 1 0.96; 1 1" dur="3.8s" repeatCount="indefinite"
      calcMode="spline" keySplines="0.4 0 0.6 1; 0.4 0 0.6 1" keyTimes="0;0.5;1"/>

    <!-- EYE OUTLINE (almond shape) — the sclera (white of eye) -->
    <path d="M -42,0
             C -28,-24 -12,-28 0,-28
             C 12,-28 28,-24 42,0
             C 28,24 12,28 0,28
             C -12,28 -28,24 -42,0 Z"
          fill="url(#eyeScleraGrad)"
          stroke="{NEON_GREEN}" stroke-width="1.6" stroke-opacity=".7"
          filter="url(#glow)"/>

    <!-- Sclera highlight (top arc, simulating spherical curvature) -->
    <path d="M -28,-12 Q 0,-22 28,-12"
          fill="none" stroke="{NEON_BRIGHT}" stroke-width="1" stroke-opacity=".45"
          filter="url(#tinyGlow)"/>
    <!-- Sclera shadow (bottom arc, depth) -->
    <path d="M -28,12 Q 0,22 28,12"
          fill="none" stroke="{NEON_GREEN}" stroke-width="0.8" stroke-opacity=".3"/>

    <!-- IRIS (3D sphere look — radial gradient) -->
    <circle r="20"
            fill="url(#irisGrad)"
            stroke="{NEON_GREEN}" stroke-width="1.2" stroke-opacity=".85"
            filter="url(#glow)"/>
    <!-- Iris ring (bright outer edge for "glowing eye" effect) -->
    <circle r="20" fill="none" stroke="{NEON_BRIGHT}" stroke-width="0.6" stroke-opacity=".6"/>

    <!-- Iris radial pattern (fibers) -->
    <g stroke="{NEON_BRIGHT}" stroke-width="0.5" stroke-opacity=".55" fill="none">
      <line x1="0" y1="-17" x2="0" y2="-13"/>
      <line x1="0" y1="17" x2="0" y2="13"/>
      <line x1="-17" y1="0" x2="-13" y2="0"/>
      <line x1="17" y1="0" x2="13" y2="0"/>
      <line x1="-12" y1="-12" x2="-9" y2="-9"/>
      <line x1="12" y1="-12" x2="9" y2="-9"/>
      <line x1="-12" y1="12" x2="-9" y2="9"/>
      <line x1="12" y1="12" x2="9" y2="9"/>
      <line x1="-15" y1="-8" x2="-12" y2="-6"/>
      <line x1="15" y1="-8" x2="12" y2="-6"/>
      <line x1="-15" y1="8" x2="-12" y2="6"/>
      <line x1="15" y1="8" x2="12" y2="6"/>
    </g>

    <!-- PUPIL (dark center) -->
    <circle r="8" fill="#020b07" stroke="{NEON_BRIGHT}" stroke-width="1"/>
    <!-- Pupil highlight (cornea reflection — 3D light source) -->
    <circle cx="-3" cy="-3" r="3.5" fill="{NEON_BRIGHT}" opacity=".85"
            filter="url(#tinyGlow)"/>
    <circle cx="3" cy="3" r="1.5" fill="{NEON_BRIGHT}" opacity=".5"/>

    <!-- Scanning rays around iris (animated, suggesting active vision) -->
    <g stroke="{NEON_BRIGHT}" stroke-width="1" stroke-opacity=".6" fill="none" filter="url(#tinyGlow)">
      <line x1="0" y1="-26" x2="0" y2="-32">
        <animate attributeName="opacity" values="0.2;1;0.2" dur="2s" repeatCount="indefinite"/>
      </line>
      <line x1="-22" y1="-22" x2="-28" y2="-28">
        <animate attributeName="opacity" values="0.2;1;0.2" dur="2s" begin="0.25s" repeatCount="indefinite"/>
      </line>
      <line x1="22" y1="-22" x2="28" y2="-28">
        <animate attributeName="opacity" values="0.2;1;0.2" dur="2s" begin="0.5s" repeatCount="indefinite"/>
      </line>
      <line x1="-30" y1="0" x2="-36" y2="0">
        <animate attributeName="opacity" values="0.2;1;0.2" dur="2s" begin="0.75s" repeatCount="indefinite"/>
      </line>
      <line x1="30" y1="0" x2="36" y2="0">
        <animate attributeName="opacity" values="0.2;1;0.2" dur="2s" begin="1s" repeatCount="indefinite"/>
      </line>
      <line x1="-22" y1="22" x2="-28" y2="28">
        <animate attributeName="opacity" values="0.2;1;0.2" dur="2s" begin="1.25s" repeatCount="indefinite"/>
      </line>
      <line x1="22" y1="22" x2="28" y2="28">
        <animate attributeName="opacity" values="0.2;1;0.2" dur="2s" begin="1.5s" repeatCount="indefinite"/>
      </line>
      <line x1="0" y1="26" x2="0" y2="32">
        <animate attributeName="opacity" values="0.2;1;0.2" dur="2s" begin="1.75s" repeatCount="indefinite"/>
      </line>
    </g>

    <!-- Sweep scan-line rotating around the iris (like a LiDAR scan) -->
    <g>
      <animateTransform attributeName="transform" type="rotate"
        from="0" to="360" dur="6s" repeatCount="indefinite"/>
      <line x1="0" y1="0" x2="0" y2="-26" stroke="{NEON_BRIGHT}" stroke-width="0.8"
            stroke-opacity=".7" filter="url(#tinyGlow)"/>
      <circle cx="0" cy="-26" r="2" fill="{NEON_BRIGHT}" filter="url(#tinyGlow)"/>
    </g>

  </g>
</g>
'''


def section_system_architecture():
    out = [svg_open()]
    out.append(defs_shinobi())
    out.append(background_shinobi())
    out.append(corners_block())

    # Hero banner
    out.append(f'''<g clip-path="url(#heroClipTemp)">
  <rect x="30" y="28" width="{W-60}" height="170" rx="24" fill="url(#hero)"/>
  <!-- diagonal energy -->
  <path d="M-100 195L470 20 M160 205L730 20 M450 205L1020 20
           M740 205L1310 20 M1030 205L1600 20 M1320 205L1890 20"
        stroke="{NEON_BRIGHT}" stroke-opacity=".09" stroke-width="2">
    <animateTransform attributeName="transform" type="translate"
      values="0 0;90 0;0 0" dur="8s" repeatCount="indefinite"/>
  </path>
  <!-- neural network decoration in hero -->
  <g fill="none" stroke="#72ffa3" stroke-opacity=".16" stroke-width="1.4">
    <path d="M1180 82L1260 52L1340 95L1420 60L1510 110L1580 70"/>
    <path d="M1210 150L1280 112L1360 142L1440 102L1530 150"/>
    <path d="M1260 52L1280 112M1340 95L1360 142M1420 60L1440 102M1510 110L1530 150"/>
  </g>
  <g>
    <circle cx="1180" cy="82" r="5" fill="{NEON_BRIGHT}"/>
    <circle cx="1260" cy="52" r="5" fill="{NEON_BRIGHT}"/>
    <circle cx="1340" cy="95" r="5" fill="{NEON_BRIGHT}"/>
    <circle cx="1420" cy="60" r="5" fill="{NEON_BRIGHT}"/>
    <circle cx="1510" cy="110" r="5" fill="{NEON_BRIGHT}"/>
    <circle cx="1580" cy="70" r="5" fill="{NEON_BRIGHT}"/>
    <circle cx="1210" cy="150" r="4" fill="{NEON_BRIGHT}"/>
    <circle cx="1280" cy="112" r="4" fill="{NEON_BRIGHT}"/>
    <circle cx="1360" cy="142" r="4" fill="{NEON_BRIGHT}"/>
    <circle cx="1440" cy="102" r="4" fill="{NEON_BRIGHT}"/>
    <circle cx="1530" cy="150" r="4" fill="{NEON_BRIGHT}"/>
    <animate attributeName="opacity" values=".25;1;.25" dur="3s" repeatCount="indefinite"/>
  </g>
  <circle cx="1370" cy="100" r="125" fill="none"
          stroke="#54ff91" stroke-opacity=".08" stroke-width="1"
          stroke-dasharray="4 12">
    <animateTransform attributeName="transform" type="rotate"
      from="0 1370 100" to="360 1370 100" dur="14s" repeatCount="indefinite"/>
  </circle>
</g>
<rect x="30" y="28" width="{W-60}" height="170" rx="24"
      fill="none" stroke="#63ff9a" stroke-opacity=".32"/>
<text x="{W//2}" y="125" text-anchor="middle"
      font-family="Arial, Helvetica, sans-serif"
      font-size="58" font-weight="800" letter-spacing="2"
      fill="url(#greenText)">
  AI-NATIVE ENGINEERING
  <animate attributeName="opacity" values=".82;1;.82" dur="4s" repeatCount="indefinite"/>
</text>
<text x="{W//2}" y="157" text-anchor="middle"
      font-family="monospace" font-size="11" letter-spacing="4"
      fill="{ACCENT_GREEN}" opacity=".7">
  INTELLIGENCE / RETRIEVAL / AUTOMATION / CONTEXT
</text>
<rect x="600" y="177" width="464" height="2" fill="url(#scan)" filter="url(#glow)">
  <animate attributeName="width" values="320;520;320" dur="5s" repeatCount="indefinite"/>
  <animate attributeName="x" values="672;572;672" dur="5s" repeatCount="indefinite"/>
</rect>
''')

    # AI System Core pipe
    out.append(f'''<g font-family="monospace">
  <text x="{W//2}" y="242" text-anchor="middle" fill="{NEON_GREEN}" font-size="10" letter-spacing="3">AI SYSTEM CORE</text>
  <path d="M650 270H1014" stroke="{NEON_GREEN}" stroke-opacity=".16" stroke-width="2"/>
  <path d="M650 270H1014" stroke="{NEON_BRIGHT}" stroke-opacity=".6" stroke-width="1.5" stroke-dasharray="2 14">
    <animate attributeName="stroke-dashoffset" values="0;-64" dur="1.4s" repeatCount="indefinite"/>
  </path>
  <circle cx="650" cy="270" r="5" fill="#baffd0" filter="url(#glow)">
    <animate attributeName="r" values="3;9;3" dur="1.4s" repeatCount="indefinite"/>
  </circle>
  <circle cx="1014" cy="270" r="5" fill="#baffd0" filter="url(#glow)">
    <animate attributeName="r" values="3;9;3" dur="1.7s" repeatCount="indefinite"/>
  </circle>
</g>
''')

    # Two AI cards (LLM APPLICATIONS, VISION & ML)
    ai_cards = [
        {
            "num":  "01",
            "kind": "GENERATIVE INTELLIGENCE",
            "title": "LLM APPLICATIONS",
            "sub":  "MODELS / PROMPTS / AGENTS / CONTEXT",
            "items": ["LangChain", "RAG Pipelines", "Vector DBs", "Prompt Engineering", "Fine-tuning", "Function Calling"],
            "pct":  95,
        },
        {
            "num":  "02",
            "kind": "PERCEPTUAL INTELLIGENCE",
            "title": "VISION & ML",
            "sub":  "IMAGES / VIDEO / PATTERNS / INFERENCE",
            "items": ["Image Processing", "Machine Vision", "OpenCV", "PyTorch", "TensorFlow", "Real-time Inference"],
            "pct":  95,
        },
    ]

    card_xs = [180, 880]
    card_w = 624
    card_h = 444
    card_y = 292

    out.append('<g font-family="Arial, Helvetica, sans-serif">')
    for i, c in enumerate(ai_cards):
        x = card_xs[i]
        # Outer glow
        out.append(f'<g transform="translate({x} {card_y})">')
        out.append(f'<rect x="-8" y="-8" width="{card_w+16}" height="{card_h+16}" rx="28" fill="{NEON_GREEN}" opacity=".04" filter="url(#softGlow)"/>')
        out.append(f'<rect width="{card_w}" height="{card_h}" rx="24" fill="url(#panel)" stroke="{BORDER_GREEN}" stroke-opacity=".34"/>')
        out.append(f'<rect width="{card_w}" height="5" rx="2" fill="{NEON_GREEN}">')
        out.append(f'<animate attributeName="opacity" values=".25;1;.25" dur="3.2s" begin="{i*0.6}s" repeatCount="indefinite"/></rect>')
        # Number/kind label
        out.append(f'<text x="30" y="40" fill="{LABEL_GREEN}" font-family="monospace" font-size="10" letter-spacing="3">{c["num"]} / {c["kind"]}</text>')

        # Brain/neural icon (decorative)
        icon_x = card_w // 2
        out.append(f'<g transform="translate({icon_x} 105)">')
        out.append(f'<circle r="74" fill="url(#orb)" opacity=".28">')
        out.append(f'<animate attributeName="r" values="55;82;55" dur="4s" begin="{i*0.5}s" repeatCount="indefinite"/></circle>')
        out.append(f'<circle r="61" fill="none" stroke="{NEON_GREEN}" stroke-opacity=".13" stroke-dasharray="3 10">')
        out.append(f'<animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="9s" repeatCount="indefinite"/></circle>')

        # ICON: pick a distinct 3D shape per card.
        #   Card 0 (LLM APPLICATIONS)    -> 3D BRAIN (organic, generative)
        #   Card 1 (VISION & ML)         -> 3D EYE   (perceptual, vision)
        if i == 0:
            out.append(_3d_brain_icon())
        else:
            out.append(_3d_eye_icon())
        out.append('</g>')

        # Title + sub
        out.append(f'<text x="30" y="215" fill="{TEXT_PRIMARY}" font-size="30" font-weight="700">{esc(c["title"])}</text>')
        out.append(f'<text x="30" y="242" fill="{TEXT_SECOND}" font-family="monospace" font-size="10" letter-spacing="1.5">{esc(c["sub"])}</text>')

        # Items as 2-column grid
        items_y = 280
        for k, item in enumerate(c["items"]):
            col = k % 3
            row = k // 3
            ix = 30 + col * (card_w - 60) // 3
            iy = items_y + row * 32
            out.append(f'<g transform="translate({ix} {iy})">')
            out.append(f'<rect x="0" y="0" width="{(card_w - 60)//3 - 6}" height="22" rx="11" fill="#0c2117" stroke="{NEON_GREEN}" stroke-opacity=".28"/>')
            out.append(f'<circle cx="14" cy="11" r="3" fill="{NEON_BRIGHT}"/>')
            out.append(f'<text x="24" y="15" fill="{TEXT_PRIMARY}" font-size="11">{esc(item)}</text>')
            out.append('</g>')

        # Status footer
        sf_y = card_h - 40
        out.append(f'<line x1="30" y1="{sf_y-10}" x2="{card_w-30}" y2="{sf_y-10}" stroke="{NEON_GREEN}" stroke-width="0.5" stroke-opacity=".15"/>')
        out.append(f'<text x="30" y="{sf_y+10}" fill="{TEXT_SECOND}" font-family="monospace" font-size="10" letter-spacing="1">DEPLOYMENT</text>')
        out.append(f'<text x="30" y="{sf_y+28}" fill="{TEXT_PRIMARY}" font-size="13" font-weight="600">INFERENCE ONLINE</text>')
        out.append(f'<circle cx="{card_w-32}" cy="{sf_y+23}" r="5" fill="{NEON_BRIGHT}" filter="url(#tinyGlow)">')
        out.append(f'<animate attributeName="r" values="3;6;3" dur="1.7s" repeatCount="indefinite"/></circle>')
        out.append(f'<rect x="30" y="{sf_y+38}" width="{card_w-60}" height="4" rx="2" fill="rgba(255,255,255,0.08)"/>')
        fill_w = int((card_w - 60) * c["pct"] / 100)
        out.append(f'<rect x="30" y="{sf_y+38}" width="0" height="4" rx="2" fill="{NEON_GREEN}" filter="url(#glow)">')
        out.append(f'<animate attributeName="width" from="0" to="{fill_w}" dur="1.8s" begin="{0.4 + i*0.3}s" fill="freeze"/></rect>')
        out.append('</g>')

    out.append('</g>')

    # Bottom row: 4 architectural layer strips
    layer_y = 770
    layer_h = 60
    layer_gap = 12
    arch_layers = [
        ("PRESENTATION",  ["React.js", "Vue.js 3", "Next.js", "TypeScript", "Tailwind CSS"]),
        ("API GATEWAY",    ["RESTful API", "GraphQL", "JWT Auth", "Rate Limiting"]),
        ("BUSINESS LOGIC", ["Node.js", "Python (Django/FastAPI)", "C# (.NET)", "Microservices"]),
        ("AI / ML",        ["PyTorch", "TensorFlow", "OpenCV", "LangChain"]),
        ("INFRASTRUCTURE", ["Docker", "Kubernetes", "Nginx", "AWS / Azure / GCP"]),
    ]
    for i, (name, items) in enumerate(arch_layers):
        y = layer_y + i * 0  # All on one row
    # Actually lay them out in a single row, 5 strips
    strip_w = (W - 80 - 4 * 12) // 5
    for i, (name, items) in enumerate(arch_layers):
        x = 40 + i * (strip_w + 12)
        y = layer_y
        out.append(f'<g transform="translate({x} {y})">')
        out.append(f'<rect width="{strip_w}" height="{layer_h}" rx="10" fill="url(#panel)" stroke="{BORDER_GREEN}" stroke-opacity=".25"/>')
        out.append(f'<rect width="4" height="{layer_h}" rx="2" fill="{NEON_GREEN}"/>')
        out.append(f'<text x="14" y="20" fill="{LABEL_GREEN}" font-family="monospace" font-size="9" letter-spacing="2">{name}</text>')
        # Items as small badges inline
        bx = 14
        for item in items[:3]:
            tw = len(item) * 6 + 14
            out.append(f'<g transform="translate({bx} 30)">')
            out.append(f'<rect width="{tw}" height="20" rx="10" fill="#0c2117" stroke="{NEON_GREEN}" stroke-opacity=".22"/>')
            out.append(f'<text x="{tw//2}" y="14" text-anchor="middle" fill="{TEXT_PRIMARY}" font-size="9">{esc(item)}</text>')
            out.append('</g>')
            bx += tw + 6
        out.append('</g>')

    out.append(footer_block("AI-NATIVE ARCHITECTURE // LAYERED // OBSERVABLE // RESILIENT"))
    out.append(svg_close())
    return ''.join(out)


# ============================================================================
# SECTION 3 — CAREER TRAJECTORY
# ============================================================================
CAREER = [
    {
        "start": 1398, "end": 1399,
        "role": "Game Developer",
        "company": "Golad Game & Animation Studio",
        "location": "Kermanshah",
        "tag": "GAME_DEV",
        "bullets": [
            "C# / C++ gameplay programming",
            "Unreal Engine & Unity 3D engines",
            "3D Max modeling & character design"
        ]
    },
    {
        "start": 1399, "end": 1401,
        "role": "Web Designer & SEO Engineer",
        "company": "Koosha Rayan Co.",
        "location": "Ilam",
        "tag": "WEB_SEO",
        "bullets": [
            "HTML5 / CSS3 / JS / Vue.js 3",
            "WordPress + WooCommerce customization",
            "UI optimization & technical SEO"
        ]
    },
    {
        "start": 1401, "end": None,
        "role": "Programming Instructor",
        "company": "Computer Technical-Vocational School",
        "location": "Kermanshah",
        "tag": "TEACHING",
        "bullets": [
            "Frontend / Backend / Database",
            "Python · Node.js · MySQL · Linux",
            "Algorithms, data structures, OOP"
        ]
    },
    {
        "start": 1404, "end": None,
        "role": "Technical Manager",
        "company": "sup",
        "location": "Kermanshah",
        "tag": "TECH_LEAD",
        "bullets": [
            "Team leadership & technical planning",
            "Software architecture & code reviews",
            "Product lifecycle & mentorship"
        ]
    },
]


def section_career_trajectory():
    out = [svg_open()]
    out.append(defs_shinobi())
    out.append(background_shinobi())
    out.append(header_block("CAREER TRAJECTORY",
                            "TIMELINE / 4 ROLES / 6+ YEARS / ACTIVE: 2"))
    out.append(corners_block())

    # Horizontal timeline
    timeline_y = 470
    timeline_x_start = 80
    timeline_x_end = W - 80

    # Timeline base line with gradient
    out.append(f'<line x1="{timeline_x_start}" y1="{timeline_y}" x2="{timeline_x_end}" y2="{timeline_y}" '
               f'stroke="{NEON_GREEN}" stroke-width="2" stroke-opacity=".55" filter="url(#glow)"/>')
    # Animated traveling pulse on timeline
    out.append(f'<circle cx="{timeline_x_start}" cy="{timeline_y}" r="6" fill="{NEON_BRIGHT}" filter="url(#glow)">')
    out.append(f'<animate attributeName="cx" values="{timeline_x_start};{timeline_x_end};{timeline_x_start}" dur="12s" repeatCount="indefinite"/>')
    out.append(f'<animate attributeName="opacity" values="0;1;1;1;0" keyTimes="0;0.05;0.5;0.95;1" dur="12s" repeatCount="indefinite"/></circle>')

    # Year markers
    year_marks = [1398, 1399, 1401, 1404, "now"]
    for i, y in enumerate(year_marks):
        x = timeline_x_start + int((timeline_x_end - timeline_x_start) * i / (len(year_marks) - 1))
        out.append(f'<line x1="{x}" y1="{timeline_y - 8}" x2="{x}" y2="{timeline_y + 8}" stroke="{NEON_GREEN}" stroke-width="1"/>')
        out.append(f'<text x="{x}" y="{timeline_y + 28}" text-anchor="middle" font-family="monospace" font-size="11" fill="{TEXT_SECOND}">{y}</text>')

    # 4 career cards (alternating above/below timeline)
    card_w = 360
    card_h = 280
    positions = [
        (timeline_x_start + 80,  timeline_y - card_h - 50, 0),  # above
        (timeline_x_start + 320, timeline_y + 50, 1),  # below
        (timeline_x_start + 720, timeline_y - card_h - 50, 0),  # above
        (timeline_x_start + 1080, timeline_y + 50, 1),  # below
    ]
    for i, (job, (card_x, card_y, _)) in enumerate(zip(CAREER, positions)):
        c = NEON_BRIGHT if i % 2 == 0 else NEON_GREEN
        period = f"{job['start']}" + (f" – {job['end']}" if job['end'] else " – now")
        # Connector
        connector_y_start = card_y + card_h if card_y < timeline_y else card_y
        connector_y_end = timeline_y
        out.append(f'<line x1="{card_x + card_w//2}" y1="{connector_y_start}" x2="{card_x + card_w//2}" y2="{connector_y_end}" '
                   f'stroke="{c}" stroke-width="1" stroke-opacity=".7"/>')
        # Card
        out.append(f'<g transform="translate({card_x} {card_y})">')
        out.append(f'<rect x="-4" y="-4" width="{card_w+8}" height="{card_h+8}" rx="22" fill="{c}" opacity=".04" filter="url(#softGlow)"/>')
        out.append(f'<rect width="{card_w}" height="{card_h}" rx="18" fill="url(#panel)" stroke="{c}" stroke-opacity=".34"/>')
        out.append(f'<rect width="{card_w}" height="5" rx="2" fill="{c}">')
        out.append(f'<animate attributeName="opacity" values=".25;1;.25" dur="3.2s" begin="{i*0.4}s" repeatCount="indefinite"/></rect>')

        # Period chip + tag
        out.append(f'<g transform="translate(20 18)">')
        out.append(f'<rect width="130" height="22" rx="11" fill="#0c2117" stroke="{c}" stroke-opacity=".5"/>')
        out.append(f'<text x="65" y="15" text-anchor="middle" font-family="monospace" font-size="11" fill="{c}">{period}</text>')
        out.append('</g>')
        out.append(f'<g transform="translate({card_w - 88} 18)">')
        out.append(f'<rect width="68" height="22" rx="11" fill="#0c2117" stroke="{c}" stroke-opacity=".5"/>')
        out.append(f'<text x="34" y="15" text-anchor="middle" font-family="monospace" font-size="10" fill="{c}">{esc(job["tag"])}</text>')
        out.append('</g>')

        # Role + company + location
        out.append(f'<text x="20" y="68" fill="{TEXT_PRIMARY}" font-size="22" font-weight="700">{esc(job["role"])}</text>')
        out.append(f'<text x="20" y="92" fill="{TEXT_SECOND}" font-size="13">{esc(job["company"])}</text>')
        out.append(f'<text x="20" y="110" font-family="monospace" font-size="11" fill="{TEXT_DIM}">[ {esc(job["location"])} ]</text>')

        # Divider
        out.append(f'<line x1="20" y1="124" x2="{card_w-20}" y2="124" stroke="{c}" stroke-width="0.5" stroke-opacity=".3"/>')

        # Bullets
        by = 148
        for b in job["bullets"]:
            out.append(f'<circle cx="28" cy="{by-3}" r="3" fill="{c}" filter="url(#tinyGlow)"/>')
            truncated = b if len(b) < 42 else b[:40] + "…"
            out.append(f'<text x="40" y="{by}" fill="{TEXT_PRIMARY}" font-size="12">{esc(truncated)}</text>')
            by += 22

        # Footer accent
        out.append(f'<line x1="20" y1="{card_h-20}" x2="{card_w-20}" y2="{card_h-20}" stroke="{c}" stroke-width="0.5" stroke-opacity=".15"/>')
        out.append(f'<circle cx="{card_w - 30}" cy="{card_h - 10}" r="4" fill="{c}" filter="url(#tinyGlow)">')
        out.append(f'<animate attributeName="opacity" values=".5;1;.5" dur="1.7s" repeatCount="indefinite"/></circle>')

        out.append('</g>')  # close card

        # Milestone dot on timeline
        cx = card_x + card_w // 2
        out.append(f'<circle cx="{cx}" cy="{timeline_y}" r="9" fill="{c}" stroke="{BG_DEEP}" stroke-width="2" filter="url(#glow)"/>')
        out.append(f'<circle cx="{cx}" cy="{timeline_y}" r="4" fill="{BG_DEEP}"/>')

    out.append(footer_block("TRAJECTORY // GAME → WEB → EDUCATION → LEADERSHIP // STILL BUILDING"))
    out.append(svg_close())
    return ''.join(out)


# ============================================================================
# SECTION 4 — EDUCATION & KNOWLEDGE
# ============================================================================
EDUCATION = [
    {
        "degree":   "M.Sc. Artificial Intelligence",
        "field":    "Artificial Intelligence",
        "school":   "Islamic Azad University, Hamedan",
        "city":     "Hamedan",
        "period":   "1404 – present",
        "gpa":      "In progress",
        "color":    NEON_BRIGHT,
        "status":   "Current Student",
    },
    {
        "degree":   "Bachelor of Computer Engineering",
        "field":    "Software",
        "school":   "Islamic Azad University, Kermanshah",
        "city":     "Kermanshah",
        "period":   "1402 – 1404",
        "gpa":      "18.5",
        "color":    NEON_GREEN,
        "status":   "Completed",
    },
    {
        "degree":   "Associate Degree in Computer Engineering",
        "field":    "Software",
        "school":   "Ilam National Skills University",
        "city":     "Ilam",
        "period":   "1400 – 1402",
        "gpa":      "17.70",
        "color":    "#9affba",
        "status":   "Completed",
    },
]

LANGUAGES = [
    ("English",  [("Reading", 4), ("Writing", 4), ("Speaking", 3), ("Listening", 4)], NEON_BRIGHT),
]


def section_education_knowledge():
    out = [svg_open()]
    out.append(defs_shinobi())
    out.append(background_shinobi())
    out.append(header_block("EDUCATION & KNOWLEDGE",
                            "ACADEMIC RECORD / LANGUAGES / CONTINUOUS LEARNING"))
    out.append(corners_block())

    # Left column: 3 education cards (vertical stack)
    card_x = 50
    card_y_start = 220
    card_w = 800
    card_h = 200
    card_gap = 16

    out.append(f'<text x="{card_x}" y="195" fill="{LABEL_GREEN}" font-family="monospace" font-size="11" letter-spacing="3">// ACADEMIC RECORD</text>')

    for i, edu in enumerate(EDUCATION):
        cy = card_y_start + i * (card_h + card_gap)
        c = edu["color"]

        out.append(f'<g transform="translate({card_x} {cy})">')
        out.append(f'<rect x="-4" y="-4" width="{card_w+8}" height="{card_h+8}" rx="22" fill="{c}" opacity=".04" filter="url(#softGlow)"/>')
        out.append(f'<rect width="{card_w}" height="{card_h}" rx="18" fill="url(#panel)" stroke="{c}" stroke-opacity=".34"/>')
        out.append(f'<rect width="6" height="{card_h}" rx="3" fill="{c}" opacity=".85"/>')
        out.append(f'<rect width="{card_w}" height="5" rx="2" fill="{c}">')
        out.append(f'<animate attributeName="opacity" values=".25;1;.25" dur="3.2s" begin="{i*0.4}s" repeatCount="indefinite"/></rect>')

        # Period + status chips (top right)
        out.append(f'<g transform="translate(20 18)">')
        out.append(f'<rect width="150" height="22" rx="11" fill="#0c2117" stroke="{c}" stroke-opacity=".5"/>')
        out.append(f'<text x="75" y="15" text-anchor="middle" font-family="monospace" font-size="11" fill="{c}">{esc(edu["period"])}</text>')
        out.append('</g>')
        out.append(f'<g transform="translate({card_w - 130} 18)">')
        out.append(f'<rect width="110" height="22" rx="11" fill="{c}" opacity=".18"/>')
        out.append(f'<text x="55" y="15" text-anchor="middle" font-family="monospace" font-size="10" fill="{c}">{esc(edu["status"])}</text>')
        out.append('</g>')

        # Degree + field + school
        out.append(f'<text x="20" y="68" fill="{TEXT_PRIMARY}" font-size="22" font-weight="700">{esc(edu["degree"])}</text>')
        out.append(f'<text x="20" y="92" fill="{c}" font-family="monospace" font-size="11">// Field: <tspan fill="{TEXT_PRIMARY}">{esc(edu["field"])}</tspan></text>')
        out.append(f'<text x="20" y="112" fill="{TEXT_SECOND}" font-size="13">{esc(edu["school"])}</text>')
        out.append(f'<text x="20" y="130" font-family="monospace" font-size="11" fill="{TEXT_DIM}">[ {esc(edu["city"])} ]</text>')

        # GPA chip
        if edu["gpa"] != "In progress":
            out.append(f'<g transform="translate({card_w - 130} {card_h - 50})">')
            out.append(f'<rect width="110" height="30" rx="15" fill="{c}" opacity=".15"/>')
            out.append(f'<text x="55" y="20" text-anchor="middle" font-family="monospace" font-size="12" fill="{c}">GPA {esc(edu["gpa"])}</text>')
            out.append('</g>')
        else:
            out.append(f'<g transform="translate({card_w - 170} {card_h - 50})">')
            out.append(f'<rect width="150" height="30" rx="15" fill="{c}" opacity=".15"/>')
            out.append(f'<circle cx="20" cy="15" r="4" fill="{c}"><animate attributeName="opacity" values=".5;1;.5" dur="1.7s" repeatCount="indefinite"/></circle>')
            out.append(f'<text x="85" y="20" text-anchor="middle" font-family="monospace" font-size="11" fill="{c}">CURRENTLY STUDYING</text>')
            out.append('</g>')

        # Bottom meta
        out.append(f'<line x1="20" y1="{card_h-12}" x2="{card_w-20}" y2="{card_h-12}" stroke="{c}" stroke-width="0.4" stroke-opacity=".2"/>')

        out.append('</g>')

    # Right column: Languages + Mastery badges
    right_x = 900
    right_w = 720
    out.append(f'<text x="{right_x}" y="195" fill="{LABEL_GREEN}" font-family="monospace" font-size="11" letter-spacing="3">// LANGUAGES</text>')

    # Language cards
    lang_y = 220
    for lang_name, skills, color in LANGUAGES:
        out.append(f'<g transform="translate({right_x} {lang_y})">')
        out.append(f'<rect x="-4" y="-4" width="{right_w+8}" height="108" rx="22" fill="{color}" opacity=".04" filter="url(#softGlow)"/>')
        out.append(f'<rect width="{right_w}" height="100" rx="18" fill="url(#panel)" stroke="{color}" stroke-opacity=".34"/>')
        out.append(f'<rect width="6" height="100" rx="3" fill="{color}" opacity=".85"/>')
        out.append(f'<text x="20" y="36" fill="{TEXT_PRIMARY}" font-size="20" font-weight="700">{esc(lang_name)}</text>')
        # Skill dots
        bx = 160
        bw = 130
        for skill_name, level in skills:
            out.append(f'<text x="{bx}" y="32" font-family="monospace" font-size="10" fill="{TEXT_DIM}" letter-spacing="1.5">{esc(skill_name)}</text>')
            # 5 dots, filled up to `level`
            for k in range(5):
                dx = bx + k * 14
                dy = 44
                if k < level:
                    out.append(f'<circle cx="{dx}" cy="{dy}" r="5" fill="{color}" filter="url(#tinyGlow)">')
                    out.append(f'<animate attributeName="r" values="4;6;4" dur="1.7s" begin="{k*0.2}s" repeatCount="indefinite"/></circle>')
                else:
                    out.append(f'<circle cx="{dx}" cy="{dy}" r="5" fill="{BG_DEEP}" stroke="{color}" stroke-width="0.8" stroke-opacity=".4"/>')
            bx += bw
        out.append(f'<text x="20" y="80" font-family="monospace" font-size="10" fill="{TEXT_DIM}" letter-spacing="1">// CEFR-equiv: B2</text>')
        out.append('</g>')
        lang_y += 130

    # Mastery badges grid
    out.append(f'<text x="{right_x}" y="{lang_y+15}" fill="{LABEL_GREEN}" font-family="monospace" font-size="11" letter-spacing="3">// MASTERY BADGES</text>')

    badges = [
        ("Clean Arch",      100, NEON_BRIGHT),
        ("RESTful API",     100, NEON_GREEN),
        ("React.js",        100, NEON_BRIGHT),
        ("PostgreSQL",      100, NEON_GREEN),
        ("Docker",          100, NEON_BRIGHT),
        ("Linux Admin",     100, NEON_GREEN),
        ("Machine Learning", 95, "#baffd0"),
        ("Tech Lead",       100, "#d8ffe5"),
    ]
    badge_w = 170
    badge_h = 30
    per_row = 4
    by = lang_y + 30
    for i, (name, pct, color) in enumerate(badges):
        col = i % per_row
        row = i // per_row
        x = right_x + col * (badge_w + 8)
        y = by + row * (badge_h + 8)
        out.append(f'<g transform="translate({x} {y})">')
        out.append(f'<rect width="{badge_w}" height="{badge_h}" rx="15" fill="#0c2117" stroke="{color}" stroke-opacity=".55"/>')
        out.append(f'<circle cx="16" cy="{badge_h//2}" r="4" fill="{color}" filter="url(#tinyGlow)">')
        out.append(f'<animate attributeName="opacity" values="1;0.4;1" dur="2s" begin="{i*0.2}s" repeatCount="indefinite"/></circle>')
        out.append(f'<text x="28" y="{badge_h//2 + 4}" fill="{TEXT_PRIMARY}" font-size="11">{esc(name)}</text>')
        out.append(f'<text x="{badge_w-8}" y="{badge_h//2 + 4}" text-anchor="end" font-family="monospace" font-size="10" fill="{color}">{pct}%</text>')
        out.append('</g>')

    out.append(footer_block("LEARNING IS CONTINUOUS // THE ARCHITECT NEVER STOPS REFINING THE CRAFT"))
    out.append(svg_close())
    return ''.join(out)


# ============================================================================
# SECTION 5 — CONTACT NETWORK
# ============================================================================
CONTACTS = [
    {"key": "EMAIL",    "value": "mrparsataheri1@gmail.com", "color": NEON_BRIGHT, "icon": "envelope"},
    {"key": "TELEGRAM", "value": "@p2002t",                  "color": NEON_GREEN, "icon": "send"},
    {"key": "LINKEDIN", "value": "parsa-taheri-781b90355",    "color": NEON_BRIGHT, "icon": "linkedin"},
    {"key": "GITHUB",   "value": "parsa-kraken",              "color": NEON_GREEN, "icon": "github"},
    {"key": "LOCATION", "value": "Tehran, Iran",            "color": "#9affba", "icon": "pin"},
    {"key": "WEBSITE",  "value": "parsataheri.com",          "color": "#baffd0", "icon": "globe"},
]


def _icon_path(name, color):
    if name == "envelope":
        return (f'<rect x="2" y="6" width="20" height="13" rx="2" fill="none" stroke="{color}" stroke-width="1.4"/>'
                f'<path d="M 2 8 L 12 14 L 22 8" fill="none" stroke="{color}" stroke-width="1.4"/>')
    if name == "send":
        return (f'<path d="M 3 12 L 22 3 L 13 22 L 11 14 Z" fill="none" stroke="{color}" stroke-width="1.4" stroke-linejoin="round"/>'
                f'<line x1="11" y1="14" x2="22" y2="3" stroke="{color}" stroke-width="1.4"/>')
    if name == "linkedin":
        return (f'<rect x="2" y="2" width="20" height="20" rx="3" fill="none" stroke="{color}" stroke-width="1.4"/>'
                f'<line x1="7" y1="7" x2="7" y2="17" stroke="{color}" stroke-width="1.6"/>'
                f'<circle cx="7" cy="5" r="1.2" fill="{color}"/>'
                f'<path d="M 11 17 L 11 9 M 11 13 C 12 10 16 9 17 13 L 17 17" fill="none" stroke="{color}" stroke-width="1.6" stroke-linejoin="round"/>')
    if name == "github":
        return (f'<path d="M 12 2 C 6.5 2 2 6.5 2 12 C 2 16.5 5 20.4 9 21.8 C 9.5 21.9 9.7 21.5 9.7 21.2 L 9.7 19.5 C 7 20.1 6.4 18.3 6.4 18.3 C 6 17.2 5.4 16.9 5.4 16.9 C 4.6 16.4 5.5 16.4 5.5 16.4 C 6.5 16.5 7 17.4 7 17.4 C 7.8 18.9 9.2 18.5 9.7 18.2 C 9.8 17.6 10 17.2 10.3 17 C 8.1 16.7 5.8 15.8 5.8 11.9 C 5.8 10.8 6.2 9.9 6.9 9.2 C 6.8 9 6.4 7.9 7 6.4 C 7 6.4 7.9 6.1 9.7 7.4 C 10.5 7.2 11.3 7.1 12 7.1 C 12.7 7.1 13.5 7.2 14.3 7.4 C 16.1 6.1 17 6.4 17 6.4 C 17.6 7.9 17.2 9 17.1 9.2 C 17.8 9.9 18.2 10.8 18.2 11.9 C 18.2 15.8 15.9 16.7 13.7 17 C 14 17.3 14.3 17.8 14.3 18.6 L 14.3 21.2 C 14.3 21.5 14.5 21.9 15 21.8 C 19 20.4 22 16.5 22 12 C 22 6.5 17.5 2 12 2 Z" fill="{color}" fill-opacity="0.9"/>')
    if name == "pin":
        return (f'<path d="M 12 2 C 7.5 2 4 5.5 4 10 C 4 16 12 22 12 22 C 12 22 20 16 20 10 C 20 5.5 16.5 2 12 2 Z" fill="none" stroke="{color}" stroke-width="1.4"/>'
                f'<circle cx="12" cy="10" r="3" fill="none" stroke="{color}" stroke-width="1.4"/>')
    if name == "globe":
        return (f'<circle cx="12" cy="12" r="10" fill="none" stroke="{color}" stroke-width="1.4"/>'
                f'<path d="M 2 12 L 22 12" stroke="{color}" stroke-width="1.4"/>'
                f'<path d="M 12 2 C 15 5 15 19 12 22 C 9 19 9 5 12 2 Z" fill="none" stroke="{color}" stroke-width="1.4"/>')
    return ''


def section_contact_network():
    out = [svg_open()]
    out.append(defs_shinobi())
    out.append(background_shinobi())
    out.append(header_block("CONTACT NETWORK",
                            "6 ENDPOINTS / OPEN FOR COLLABORATION / RESPONSE_TIME: <24h"))
    out.append(corners_block())

    # 3x2 grid of contact cards
    card_w = 480
    card_h = 280
    gap = 24
    grid_w = 3 * card_w + 2 * gap  # 1488
    grid_x = (W - grid_w) // 2  # center
    grid_y = 200

    for i, c in enumerate(CONTACTS):
        col = i % 3
        row = i // 3
        x = grid_x + col * (card_w + gap)
        y = grid_y + row * (card_h + gap)
        color = c["color"]

        out.append(f'<g transform="translate({x} {y})">')
        # Outer glow
        out.append(f'<rect x="-4" y="-4" width="{card_w+8}" height="{card_h+8}" rx="22" fill="{color}" opacity=".04" filter="url(#softGlow)"/>')
        # Main panel
        out.append(f'<rect width="{card_w}" height="{card_h}" rx="18" fill="url(#panel)" stroke="{color}" stroke-opacity=".34"/>')
        # Top accent bar
        out.append(f'<rect width="{card_w}" height="5" rx="2" fill="{color}">')
        out.append(f'<animate attributeName="opacity" values=".25;1;.25" dur="3.2s" begin="{i*0.4}s" repeatCount="indefinite"/></rect>')

        # Top label
        out.append(f'<text x="20" y="36" font-family="monospace" font-size="11" letter-spacing="3" fill="{color}">// {esc(c["key"])}</text>')
        # Status dot top-right
        out.append(f'<circle cx="{card_w-24}" cy="28" r="5" fill="{color}" filter="url(#tinyGlow)">')
        out.append(f'<animate attributeName="r" values="3;6;3" dur="1.7s" begin="{i*0.2}s" repeatCount="indefinite"/></circle>')

        # Icon (centered)
        icon_y = 70
        out.append(f'<g transform="translate({card_w//2 - 12} {icon_y})">')
        out.append(_icon_path(c["icon"], color))
        out.append('</g>')

        # Decorative node network below icon
        out.append(f'<g transform="translate({card_w//2} 130)" fill="none" stroke="{color}">')
        out.append(f'<circle r="32" stroke-opacity=".14" stroke-dasharray="3 8">')
        out.append(f'<animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="8s" repeatCount="indefinite"/></circle>')
        out.append(f'<circle r="20" stroke-opacity=".25">')
        out.append(f'<animate attributeName="r" values="17;23;17" dur="2.4s" begin="{i*0.3}s" repeatCount="indefinite"/></circle>')
        out.append('</g>')

        # Value (centered)
        out.append(f'<text x="{card_w//2}" y="200" text-anchor="middle" fill="{TEXT_PRIMARY}" font-size="20" font-weight="700">{esc(c["value"])}</text>')

        # Bottom meta
        meta_text = {
            "EMAIL":    "// PGP available on request",
            "TELEGRAM": "// fastest response channel",
            "LINKEDIN": "// professional network",
            "GITHUB":   "// primary code hub",
            "LOCATION": "// UTC+3:30 · IRST",
            "WEBSITE":  "// personal portfolio · live",
        }.get(c["key"], "// open")
        out.append(f'<line x1="20" y1="{card_h-30}" x2="{card_w-20}" y2="{card_h-30}" stroke="{color}" stroke-width="0.4" stroke-opacity=".3"/>')
        out.append(f'<text x="{card_w//2}" y="{card_h-12}" text-anchor="middle" font-family="monospace" font-size="10" fill="{TEXT_DIM}" letter-spacing="1">{esc(meta_text)}</text>')

        out.append('</g>')

    out.append(footer_block("REACH OUT // LET US ENGINEER SOMETHING WORTH SHIPPING TOGETHER"))
    out.append(svg_close())
    return ''.join(out)


# ============================================================================
# SECTION 6 — UNIFIED STATS (particle.js-style)
# (Single unified panel with particle network background + central stat cards)
# ============================================================================
def section_unified_stats():
    out = [svg_open()]
    out.append(defs_shinobi())
    out.append(background_shinobi())
    out.append(corners_block())

    # Particle network background (lots of floating connected dots)
    import random
    random.seed(42)  # deterministic for reproducible build
    particles = []
    # Generate ~40 particles with depth (z) for parallax illusion
    for _ in range(40):
        x = random.randint(80, W - 80)
        y = random.randint(80, H - 80)
        z = random.choice([1, 2, 3])  # depth layer
        particles.append((x, y, z))

    # Draw connecting lines between nearby particles (parallax effect)
    out.append('<g stroke="#5cff95" stroke-opacity=".08" stroke-width="1">')
    for i, (x1, y1, z1) in enumerate(particles):
        for j, (x2, y2, z2) in enumerate(particles):
            if i >= j:
                continue
            dist = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
            if dist < 200:
                out.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/>')
    out.append('</g>')

    # Draw particles (size by z, with glow filter)
    out.append('<g fill="#8affb4" filter="url(#tinyGlow)">')
    for i, (x, y, z) in enumerate(particles):
        r = z * 1.2 + 1.5
        out.append(f'<circle cx="{x}" cy="{y}" r="{r}" opacity=".7">')
        # Animate y position for parallax drift
        drift = 12 + z * 4
        dur = 6 + z * 2
        out.append(f'<animate attributeName="cy" values="{y};{y-drift};{y+drift//2};{y}" dur="{dur}s" begin="{i*0.1}s" repeatCount="indefinite"/>')
        out.append(f'<animate attributeName="opacity" values=".4;1;.4" dur="{dur/2}s" begin="{i*0.15}s" repeatCount="indefinite"/></circle>')
    out.append('</g>')

    # Big central hero panel (glassmorphism)
    hero_w = 900
    hero_h = 380
    hero_x = (W - hero_w) // 2
    hero_y = (H - hero_h) // 2

    out.append(f'<g transform="translate({hero_x} {hero_y})">')
    # Outer glow
    out.append(f'<rect x="-8" y="-8" width="{hero_w+16}" height="{hero_h+16}" rx="32" fill="{NEON_GREEN}" opacity=".06" filter="url(#softGlow)"/>')
    # Main panel
    out.append(f'<rect width="{hero_w}" height="{hero_h}" rx="28" fill="url(#panel)" stroke="{BORDER_GREEN}" stroke-opacity=".45"/>')
    # Top accent
    out.append(f'<rect width="{hero_w}" height="6" rx="3" fill="{NEON_GREEN}">')
    out.append(f'<animate attributeName="opacity" values=".4;1;.4" dur="3s" repeatCount="indefinite"/></rect>')

    # Title
    out.append(f'<text x="{hero_w//2}" y="60" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="800" letter-spacing="3" fill="url(#greenText)">')
    out.append(f'LIVE GITHUB STATS')
    out.append(f'<animate attributeName="opacity" values=".85;1;.85" dur="4s" repeatCount="indefinite"/></text>')
    out.append(f'<text x="{hero_w//2}" y="86" text-anchor="middle" font-family="monospace" font-size="11" letter-spacing="4" fill="{ACCENT_GREEN}" opacity=".72">')
    out.append(f'REPOSITORIES / STARS / FOLLOWERS / CONTRIBUTIONS')
    out.append('</text>')
    # Animated scan line under title
    out.append(f'<rect x="200" y="100" width="{hero_w-400}" height="1.5" fill="url(#scan)" filter="url(#glow)">')
    out.append(f'<animate attributeName="width" values="200;{hero_w-300};200" dur="5s" repeatCount="indefinite"/>')
    out.append(f'<animate attributeName="x" values="350;150;350" dur="5s" repeatCount="indefinite"/></rect>')

    # 4 stat cells (3 across the top + 1 wide bottom)
    # Stats are LIVE because README pulls them from github-readme-stats / streak-stats at runtime
    # via <img> tags AROUND this SVG. The SVG itself shows decorative stat cards with
    # PLACEHOLDER for the live number (the actual numbers come from the live badges below).

    # Top row: 3 stat cards
    top_y = 130
    top_h = 110
    top_w = (hero_w - 80) // 3
    stats_top = [
        ("REPOSITORIES", "PARS-KRAKEN", "LIVE PULL", NEON_BRIGHT),
        ("STARS",         "EARNED",     "REAL-TIME",  NEON_GREEN),
        ("FOLLOWERS",     "NETWORK",    "GROWING",    "#9affba"),
    ]
    for i, (label, sub, status, color) in enumerate(stats_top):
        sx = 30 + i * (top_w + 10)
        out.append(f'<g transform="translate({sx} {top_y})">')
        out.append(f'<rect width="{top_w}" height="{top_h}" rx="14" fill="#0c2117" stroke="{color}" stroke-opacity=".45"/>')
        out.append(f'<rect width="{top_w}" height="3" rx="1.5" fill="{color}">')
        out.append(f'<animate attributeName="opacity" values=".25;1;.25" dur="2.5s" begin="{i*0.3}s" repeatCount="indefinite"/></rect>')
        out.append(f'<text x="{top_w//2}" y="35" text-anchor="middle" font-family="monospace" font-size="11" letter-spacing="2.5" fill="{color}">{esc(label)}</text>')
        # Number — live badge reference note
        out.append(f'<text x="{top_w//2}" y="68" text-anchor="middle" font-family="Arial" font-size="24" font-weight="800" fill="{TEXT_PRIMARY}">{esc(sub)}</text>')
        out.append(f'<text x="{top_w//2}" y="90" text-anchor="middle" font-family="monospace" font-size="9" letter-spacing="1" fill="{TEXT_DIM}">{esc(status)}</text>')
        # Pulsing status dot
        out.append(f'<circle cx="{top_w-16}" cy="16" r="4" fill="{color}" filter="url(#tinyGlow)">')
        out.append(f'<animate attributeName="r" values="3;5;3" dur="1.7s" begin="{i*0.2}s" repeatCount="indefinite"/></circle>')
        out.append('</g>')

    # Bottom wide stat: "Total Repositories" — the headline number from live API
    bot_y = 260
    bot_h = 100
    out.append(f'<g transform="translate(30 {bot_y})">')
    out.append(f'<rect width="{hero_w-60}" height="{bot_h}" rx="14" fill="#0c2117" stroke="{NEON_GREEN}" stroke-opacity=".55"/>')
    out.append(f'<rect width="{hero_w-60}" height="4" rx="2" fill="{NEON_GREEN}">')
    out.append(f'<animate attributeName="opacity" values=".3;1;.3" dur="2.2s" repeatCount="indefinite"/></rect>')
    out.append(f'<text x="30" y="36" font-family="monospace" font-size="11" letter-spacing="3" fill="{LABEL_GREEN}">// TOTAL REPOSITORIES</text>')
    out.append(f'<text x="30" y="74" font-family="Arial" font-size="34" font-weight="800" fill="url(#greenText)">')
    out.append('ALL PUBLIC + PRIVATE REPOS')
    out.append('</text>')
    # Note about live pull
    out.append(f'<text x="{hero_w-90}" y="36" text-anchor="end" font-family="monospace" font-size="10" letter-spacing="1.5" fill="{TEXT_DIM}">LIVE FROM GITHUB API</text>')
    # Pulsing live dot
    out.append(f'<circle cx="{hero_w-78}" cy="74" r="6" fill="{NEON_BRIGHT}" filter="url(#glow)">')
    out.append(f'<animate attributeName="r" values="5;9;5" dur="1.4s" repeatCount="indefinite"/>')
    out.append(f'<animate attributeName="opacity" values=".7;1;.7" dur="1.4s" repeatCount="indefinite"/></circle>')
    out.append('</g>')

    out.append('</g>')  # close hero panel

    out.append(footer_block("LIVE DATA // SYNCED FROM GITHUB API // REFRESH EVERY LOAD"))
    out.append(svg_close())
    return ''.join(out)


# ============================================================================
# MAIN — write all 6 sections
# ============================================================================
def main():
    sections = [
        ("01-tech-universe.svg",      section_tech_universe()),
        ("02-system-architecture.svg", section_system_architecture()),
        ("03-career-trajectory.svg",  section_career_trajectory()),
        ("04-education-knowledge.svg", section_education_knowledge()),
        ("05-contact-network.svg",    section_contact_network()),
        ("06-unified-stats.svg",      section_unified_stats()),
    ]
    for fname, content in sections:
        path = SECTIONS / fname
        path.write_text(content, encoding="utf-8")
        print(f"  wrote {path.name}  ({len(content)} bytes)")


if __name__ == "__main__":
    main()
