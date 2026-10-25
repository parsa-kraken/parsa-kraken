#!/usr/bin/env python3
"""
Generate 5 green-themed GitHub profile section SVGs for Parsa Taheri.

Sections:
  1. TECHNOLOGY UNIVERSE     — skill matrix with progress bars
  2. SYSTEM ARCHITECTURE     — layered architecture diagram
  3. CAREER TRAJECTORY       — work experience timeline
  4. EDUCATION & KNOWLEDGE   — academic + language skills
  5. CONTACT NETWORK         — contact info card grid

Style: dark navy background (#0b1220) with hacker green (#16a34a, #059669, #22c55e)
       and red accents (#dc2626, #f87171) — matches the existing profile palette.
Size:  1180 x 660 (matches existing profile SVG width).
"""
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape

# Resolve paths relative to the project root (parent of this scripts/ folder).
# This way the script works regardless of where the project is checked out.
ROOT = Path(__file__).resolve().parent.parent
SECTIONS = ROOT / "sections"
SECTIONS.mkdir(exist_ok=True)


def esc(s):
    """XML-escape text content (& < >)."""
    return xml_escape(str(s))

# Palette --------------------------------------------------------------
BG_DARK        = "#0b1220"   # near-black navy
BG_PANEL       = "#0f172a"   # slate 900
BG_PANEL_SOFT  = "#111c33"   # darker than slate
BORDER_GREEN   = "#16a34a"
BORDER_FADED   = "rgba(34,197,94,0.30)"
GREEN           = "#22c55e"
GREEN_BRIGHT   = "#4ade80"
GREEN_DARK     = "#059669"
RED             = "#f87171"
RED_BRIGHT     = "#ef4444"
TEXT_PRIMARY   = "#e2e8f0"   # slate 200
TEXT_SECOND    = "#94a3b8"   # slate 400
TEXT_DIM        = "#64748b"   # slate 500
AMBER           = "#fbbf24"
BLUE_SOFT       = "#60a5fa"

# Common fonts
FONT_MONO = "'JetBrains Mono','Courier New',Consolas,monospace"
FONT_SANS = "'Inter','Segoe UI',Roboto,Helvetica,Arial,sans-serif"

W = 1180
H = 660


# ====================================================================
#  shared helpers
# ====================================================================
def svg_open(w=W, h=H):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
        f'font-family="{FONT_SANS}">\n'
    )


def svg_close():
    return "</svg>\n"


def defs_common():
    """Shared defs: gradients, filters, patterns, animations."""
    return f'''<defs>
  <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" stop-color="#0b1220"/>
    <stop offset="50%" stop-color="#0a1322"/>
    <stop offset="100%" stop-color="#0d1a30"/>
  </linearGradient>
  <radialGradient id="bgGlow" cx="50%" cy="0%" r="80%">
    <stop offset="0%" stop-color="{GREEN_DARK}" stop-opacity="0.18"/>
    <stop offset="60%" stop-color="{GREEN_DARK}" stop-opacity="0.04"/>
    <stop offset="100%" stop-color="#000000" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="barFill" x1="0%" y1="0%" x2="100%" y2="0%">
    <stop offset="0%" stop-color="{GREEN_DARK}"/>
    <stop offset="50%" stop-color="{GREEN}"/>
    <stop offset="100%" stop-color="{GREEN_BRIGHT}"/>
  </linearGradient>
  <linearGradient id="barFillRed" x1="0%" y1="0%" x2="100%" y2="0%">
    <stop offset="0%" stop-color="{RED_BRIGHT}"/>
    <stop offset="100%" stop-color="{RED}"/>
  </linearGradient>
  <linearGradient id="borderGlow" x1="0%" y1="0%" x2="100%" y2="0%">
    <stop offset="0%" stop-color="{BORDER_GREEN}" stop-opacity="0.9"/>
    <stop offset="50%" stop-color="{GREEN_BRIGHT}" stop-opacity="0.4"/>
    <stop offset="100%" stop-color="{BORDER_GREEN}" stop-opacity="0.9"/>
  </linearGradient>
  <pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse">
    <path d="M 32 0 L 0 0 0 32" fill="none" stroke="{GREEN}" stroke-width="0.4" stroke-opacity="0.06"/>
  </pattern>
  <pattern id="scanlines" width="4" height="4" patternUnits="userSpaceOnUse">
    <rect width="4" height="1" fill="{GREEN}" opacity="0.025"/>
  </pattern>
  <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
    <feGaussianBlur stdDeviation="3" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <filter id="softGlow" x="-50%" y="-50%" width="200%" height="200%">
    <feGaussianBlur stdDeviation="6" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <style>
    text {{ font-family: {FONT_SANS}; }}
    .mono {{ font-family: {FONT_MONO}; }}
    .h1 {{ font-size: 26px; font-weight: 700; fill: {GREEN_BRIGHT}; letter-spacing: 2px; }}
    .h2 {{ font-size: 18px; font-weight: 600; fill: {TEXT_PRIMARY}; letter-spacing: 1px; }}
    .h3 {{ font-size: 14px; font-weight: 600; fill: {GREEN_BRIGHT}; letter-spacing: 0.5px; }}
    .lbl {{ font-size: 11px; fill: {TEXT_DIM}; letter-spacing: 1.5px; text-transform: uppercase; }}
    .val {{ font-size: 14px; fill: {TEXT_PRIMARY}; }}
    .key {{ font-size: 13px; fill: {GREEN_BRIGHT}; font-weight: 600; }}
    .pct {{ font-size: 11px; fill: {TEXT_SECOND}; font-family: {FONT_MONO}; }}
    .meta {{ font-size: 11px; fill: {TEXT_DIM}; font-family: {FONT_MONO}; }}
    .arrow {{ fill: none; stroke: {GREEN}; stroke-width: 1.5; }}
  </style>
</defs>
'''


def background(title_label, frame_color=BORDER_GREEN):
    """Common background + header bar."""
    return f'''<rect width="{W}" height="{H}" fill="url(#bgGrad)"/>
<rect width="{W}" height="{H}" fill="url(#grid)"/>
<rect width="{W}" height="{H}" fill="url(#scanlines)"/>
<rect width="{W}" height="{H}" fill="url(#bgGlow)"/>

<!-- Header bar -->
<g>
  <rect x="20" y="20" width="{W-40}" height="56" rx="8" fill="{BG_PANEL}" stroke="{frame_color}" stroke-width="1" stroke-opacity="0.5"/>
  <circle cx="42" cy="48" r="6" fill="{RED_BRIGHT}"/>
  <circle cx="62" cy="48" r="6" fill="{AMBER}"/>
  <circle cx="82" cy="48" r="6" fill="{GREEN_BRIGHT}">
    <animate attributeName="opacity" values="1;0.5;1" dur="2.4s" repeatCount="indefinite"/>
  </circle>
  <text x="105" y="46" class="mono" font-size="11" fill="{TEXT_DIM}" letter-spacing="2">{esc(title_label)}</text>
  <text x="105" y="62" class="h1" font-size="22">// {esc(title_label)}</text>
  <text x="{W-32}" y="55" text-anchor="end" class="meta">parsa@kraken ~ % ./section.sh --live</text>
</g>

<!-- Frame -->
<rect x="3" y="3" width="{W-6}" height="{H-6}" rx="14" fill="none" stroke="{frame_color}" stroke-width="1.5" stroke-opacity="0.55">
  <animate attributeName="stroke-opacity" values="0.4;0.75;0.4" dur="3.4s" repeatCount="indefinite"/>
</rect>
'''


# ====================================================================
#  SECTION 1 — TECHNOLOGY UNIVERSE
# ====================================================================
SKILL_GROUPS = [
    {
        "title": "ARCHITECTURE & ENGINEERING",
        "color": GREEN_BRIGHT,
        "skills": [
            ("Clean Architecture", 100),
            ("Design Patterns",     100),
            ("Object-Oriented Prog.", 100),
            ("SOLID Principles",    100),
            ("Code Review & Quality", 100),
            ("Microservices",        80),
        ],
    },
    {
        "title": "LANGUAGES & FRAMEWORKS",
        "color": GREEN_BRIGHT,
        "skills": [
            ("C#",        100),
            ("JavaScript", 100),
            ("Python",     80),
            ("Node.js",    80),
            ("TypeScript", 80),
            ("C++",        70),
        ],
    },
    {
        "title": "FRONTEND",
        "color": GREEN_BRIGHT,
        "skills": [
            ("HTML5 / CSS3", 100),
            ("React.js",    100),
            ("Vue.js 3",    100),
            ("Next.js",      80),
            ("Tailwind CSS", 80),
            ("Three.js",     60),
        ],
    },
    {
        "title": "BACKEND & API",
        "color": GREEN_BRIGHT,
        "skills": [
            ("RESTful API",  100),
            ("GraphQL",       80),
            ("Django / FastAPI", 80),
            ("Database Design",  80),
        ],
    },
    {
        "title": "DATABASE & STORAGE",
        "color": GREEN_BRIGHT,
        "skills": [
            ("PostgreSQL", 100),
            ("SQL Server", 100),
            ("MySQL",      100),
            ("MongoDB",     80),
            ("Redis",       80),
        ],
    },
    {
        "title": "DEVOPS & INFRA",
        "color": GREEN_BRIGHT,
        "skills": [
            ("Docker",        100),
            ("Linux Admin",   100),
            ("Nginx",          80),
            ("Kubernetes",     80),
            ("CI/CD Pipelines",60),
            ("AWS / Azure / GCP", 80),
        ],
    },
    {
        "title": "SECURITY",
        "color": RED,
        "skills": [
            ("OWASP Top 10",                60),
            ("Web App Security",            60),
            ("Network Fundamentals", 60),
            ("Burp Suite",                  40),
            ("Nmap",                        60),
            ("Linux Security",              60),
        ],
    },
    {
        "title": "LEADERSHIP & PROCESS",
        "color": AMBER,
        "skills": [
            ("Agile / Scrum",                  100),
            ("Project Planning",  100),
            ("Team Mentoring",                 100),
            ("Technical Decision",      100),
            ("SDLC",                           100),
            ("Tech Leadership",    100),
        ],
    },
]


def section_tech_universe():
    """Skill matrix with progress bars in 2 columns."""
    out = [svg_open()]
    out.append(defs_common())
    out.append(background("TECHNOLOGY UNIVERSE"))

    # Subtitle
    out.append(f'<text x="32" y="108" class="mono" font-size="11" fill="{TEXT_DIM}" letter-spacing="2">// SKILL MATRIX  //  GROUPS: {len(SKILL_GROUPS)}  //  LAST_SYNC: 1404/01</text>')

    # 2-column layout: 4 groups per column (last column gets the overflow)
    col_w = (W - 80) // 2
    col_x = [40, 40 + col_w + 0]
    start_y = 130
    group_h = 120

    out.append(f'<g transform="translate(0,{start_y})">')
    for i, grp in enumerate(SKILL_GROUPS):
        col = 0 if i < 4 else 1
        row = i % 4
        x = col_x[col]
        y = row * group_h

        # Group panel
        out.append(f'<g transform="translate({x},{y})">')
        out.append(f'<rect x="0" y="0" width="{col_w-20}" height="{group_h-10}" rx="6" fill="{BG_PANEL_SOFT}" stroke="{grp["color"]}" stroke-width="0.7" stroke-opacity="0.4"/>')
        # Group title
        out.append(f'<text x="14" y="22" class="h3" fill="{grp["color"]}">{esc(grp["title"])}</text>')
        out.append(f'<line x1="14" y1="30" x2="{col_w-34}" y2="30" stroke="{grp["color"]}" stroke-width="0.6" stroke-opacity="0.35"/>')

        # Skills
        skill_y = 44
        bar_x = 195            # give names 181px (was 151) for safer fit
        bar_w = col_w - 20 - bar_x - 32  # leave 32px for the % label
        for skill_name, pct in grp["skills"]:
            # Bar background (drawn FIRST so text is on top)
            out.append(f'<rect x="{bar_x}" y="{skill_y}" width="{bar_w}" height="6" rx="3" fill="{BG_DARK}" stroke="{BORDER_FADED}" stroke-width="0.5"/>')
            # Bar fill
            fill_w = int(bar_w * pct / 100)
            # Animate width on render
            out.append(
                f'<rect x="{bar_x}" y="{skill_y}" width="0" height="6" rx="3" fill="url(#barFill)" '
                f'filter="url(#glow)">'
                f'<animate attributeName="width" from="0" to="{fill_w}" dur="1.2s" begin="{0.4 + i*0.15}s" fill="freeze" '
                f'calcMode="spline" keySplines="0.25 0.1 0.25 1"/></rect>'
            )
            # Pct label
            pct_color = GREEN_BRIGHT if pct >= 80 else (AMBER if pct >= 60 else RED)
            out.append(f'<text x="{bar_x + bar_w + 8}" y="{skill_y+8}" class="pct" fill="{pct_color}">{esc(pct)}%</text>')
            # Name (drawn LAST — on top of bars, so always readable)
            out.append(f'<text x="14" y="{skill_y+8}" class="val" font-size="11" fill="{TEXT_PRIMARY}">{esc(skill_name)}</text>')
            skill_y += 16
        out.append('</g>')
    out.append('</g>')

    out.append(svg_close())
    return ''.join(out)


# ====================================================================
#  SECTION 2 — SYSTEM ARCHITECTURE
# ====================================================================
ARCH_LAYERS = [
    {
        "name":  "PRESENTATION LAYER",
        "color": GREEN_BRIGHT,
        "items": ["React.js", "Vue.js 3", "Next.js", "TypeScript", "Tailwind CSS", "Three.js"],
    },
    {
        "name":  "API GATEWAY",
        "color": GREEN_BRIGHT,
        "items": ["RESTful API", "GraphQL", "JWT Auth", "Rate Limiting"],
    },
    {
        "name":  "BUSINESS LOGIC",
        "color": GREEN_BRIGHT,
        "items": ["Node.js", "Python (Django/FastAPI)", "C# (.NET)", "Microservices"],
    },
    {
        "name":  "DATA & STORAGE",
        "color": GREEN_BRIGHT,
        "items": ["PostgreSQL", "MongoDB", "Redis Cache", "MySQL"],
    },
    {
        "name":  "INFRASTRUCTURE",
        "color": GREEN_BRIGHT,
        "items": ["Docker", "Kubernetes", "Nginx Reverse Proxy", "AWS / Azure / GCP"],
    },
    {
        "name":  "SECURITY (CROSS-CUTTING)",
        "color": RED,
        "items": ["OWASP Top 10", "Web App Security", "Linux Security", "Burp Suite", "Nmap"],
    },
]


def section_system_architecture():
    """Layered architecture diagram."""
    out = [svg_open()]
    out.append(defs_common())
    out.append(background("SYSTEM ARCHITECTURE"))

    out.append(f'<text x="32" y="108" class="mono" font-size="11" fill="{TEXT_DIM}" letter-spacing="2">// LAYERED ARCHITECTURE  //  6 LAYERS  //  END-TO-END FLOW</text>')

    # Layout: vertical stack of layer cards with arrows between them
    layers_y_start = 130
    layer_h = 64
    layer_gap = 14
    layer_x = 60
    layer_w = W - 2 * layer_x - 220  # leave space on right for the legend/labels

    out.append(f'<g transform="translate(0,{layers_y_start})">')
    for i, layer in enumerate(ARCH_LAYERS):
        y = i * (layer_h + layer_gap)
        c = layer["color"]

        # Layer card
        out.append(f'<g transform="translate({layer_x},{y})">')
        out.append(f'<rect x="0" y="0" width="{layer_w}" height="{layer_h}" rx="8" '
                   f'fill="{BG_PANEL_SOFT}" stroke="{c}" stroke-width="1" stroke-opacity="0.55" '
                   f'filter="url(#glow)"/>')

        # Left accent strip
        out.append(f'<rect x="0" y="0" width="6" height="{layer_h}" rx="3" fill="{c}" opacity="0.85"/>')

        # Layer name
        out.append(f'<text x="20" y="22" class="h3" fill="{c}" letter-spacing="2">{esc(layer["name"])}</text>')
        out.append(f'<text x="20" y="42" class="meta" fill="{TEXT_DIM}">// L{i+1}</text>')

        # Items as inline badges
        bx = 100
        by = 36
        for item in layer["items"]:
            text_w = len(item) * 7 + 16
            out.append(f'<g transform="translate({bx},{by})">')
            out.append(f'<rect x="0" y="0" width="{text_w}" height="22" rx="11" '
                       f'fill="{BG_DARK}" stroke="{c}" stroke-width="0.7" stroke-opacity="0.5"/>')
            out.append(f'<text x="{text_w//2}" y="15" text-anchor="middle" class="val" font-size="11" fill="{TEXT_PRIMARY}">{esc(item)}</text>')
            out.append('</g>')
            bx += text_w + 8

        # Right-side layer label
        out.append(f'<text x="{layer_w + 18}" y="32" class="mono" font-size="11" fill="{TEXT_SECOND}" letter-spacing="2">{esc(layer["name"].split()[0])}</text>')
        out.append(f'<text x="{layer_w + 18}" y="48" class="meta" fill="{TEXT_DIM}">// LAYER_{i+1}</text>')
        out.append('</g>')

        # Down arrow to next layer
        if i < len(ARCH_LAYERS) - 1:
            ax = layer_x + 30
            ay = y + layer_h
            out.append(
                f'<g transform="translate({ax},{ay})">'
                f'<line x1="0" y1="0" x2="0" y2="{layer_gap}" class="arrow"/>'
                f'<path d="M -4 {layer_gap-4} L 0 {layer_gap} L 4 {layer_gap-4}" fill="none" stroke="{GREEN}" stroke-width="1.5"/>'
                f'</g>'
            )
    out.append('</g>')

    # Right-side legend / annotations
    legend_x = W - 200
    out.append(f'<g transform="translate({legend_x},140)">')
    out.append(f'<rect x="0" y="0" width="180" height="380" rx="8" fill="{BG_PANEL_SOFT}" stroke="{BORDER_GREEN}" stroke-width="0.7" stroke-opacity="0.4"/>')
    out.append(f'<text x="14" y="24" class="h3" fill="{GREEN_BRIGHT}">// LEGEND</text>')
    out.append(f'<line x1="14" y1="32" x2="166" y2="32" stroke="{BORDER_GREEN}" stroke-width="0.5" stroke-opacity="0.4"/>')

    legend_rows = [
        ("green",  GREEN_BRIGHT, "Application / Data"),
        ("red",    RED,           "Security layer"),
        ("amber",  AMBER,         "Leadership / Process"),
        ("glow",   GREEN_BRIGHT,  "Live service"),
    ]
    ly = 52
    for label, color, desc in legend_rows:
        out.append(f'<circle cx="22" cy="{ly}" r="5" fill="{color}"><animate attributeName="opacity" values="1;0.5;1" dur="2s" repeatCount="indefinite"/></circle>')
        out.append(f'<text x="38" y="{ly+4}" class="val" font-size="11">{desc}</text>')
        ly += 22

    # Stats block
    ly += 16
    out.append(f'<line x1="14" y1="{ly-6}" x2="166" y2="{ly-6}" stroke="{BORDER_GREEN}" stroke-width="0.5" stroke-opacity="0.4"/>')
    out.append(f'<text x="14" y="{ly+12}" class="h3" fill="{GREEN_BRIGHT}">// FLOW</text>')
    ly += 24
    out.append(f'<text x="14" y="{ly}" class="meta">REQUEST ↓</text>')
    ly += 18
    out.append(f'<text x="14" y="{ly}" class="meta">VALIDATE ↓</text>')
    ly += 18
    out.append(f'<text x="14" y="{ly}" class="meta">PROCESS ↓</text>')
    ly += 18
    out.append(f'<text x="14" y="{ly}" class="meta">PERSIST ↓</text>')
    ly += 18
    out.append(f'<text x="14" y="{ly}" class="meta">RESPONSE ↑</text>')
    out.append('</g>')

    # Bottom callout
    out.append(f'<text x="{W//2}" y="{H-22}" text-anchor="middle" class="meta" fill="{TEXT_DIM}">// engineered for resilience · observable · horizontally scalable //</text>')

    out.append(svg_close())
    return ''.join(out)


# ====================================================================
#  SECTION 3 — CAREER TRAJECTORY
# ====================================================================
CAREER = [
    {
        "start": 1398,
        "end":   1399,
        "role":  "Game Developer",
        "company": "Golad Game & Animation Studio",
        "location": "Kermanshah",
        "tag":   "GAME_DEV",
        "color": GREEN_BRIGHT,
        "bullets": [
            "C# / C++ gameplay programming",
            "Unreal Engine & Unity 3D engines",
            "3D Max modeling & character design",
        ],
    },
    {
        "start": 1399,
        "end":   1401,
        "role":  "Web Designer & SEO Engineer",
        "company": "Koosha Rayan Co.",
        "location": "Ilam",
        "tag":   "WEB_SEO",
        "color": GREEN_BRIGHT,
        "bullets": [
            "HTML5 / CSS3 / JS / Vue.js 3",
            "WordPress + WooCommerce customization",
            "UI optimization & technical SEO",
        ],
    },
    {
        "start": 1401,
        "end":   None,  # present
        "role":  "Programming Instructor",
        "company": "Computer Technical-Vocational School",
        "location": "Kermanshah",
        "tag":   "TEACHING",
        "color": AMBER,
        "bullets": [
            "Frontend / Backend / Database",
            "Python · Node.js · MySQL · Linux",
            "Algorithms, data structures, OOP",
        ],
    },
    {
        "start": 1404,
        "end":   None,  # present
        "role":  "Technical Manager",
        "company": "Danesh Bonyan Negar Hooshmand",
        "location": "Kermanshah",
        "tag":   "TECH_LEAD",
        "color": RED,
        "bullets": [
            "Team leadership & technical planning",
            "Software architecture & code reviews",
            "Product lifecycle & mentorship",
        ],
    },
]


def section_career_trajectory():
    out = [svg_open()]
    out.append(defs_common())
    out.append(background("CAREER TRAJECTORY"))

    out.append(f'<text x="32" y="108" class="mono" font-size="11" fill="{TEXT_DIM}" letter-spacing="2">// TIMELINE  //  4 ROLES  //  6+ YEARS  //  ACTIVE: 2</text>')

    # Horizontal timeline
    timeline_y = 380
    timeline_x_start = 60
    timeline_x_end = W - 60
    timeline_w = timeline_x_end - timeline_x_start

    # Timeline base line
    out.append(f'<line x1="{timeline_x_start}" y1="{timeline_y}" x2="{timeline_x_end}" y2="{timeline_y}" stroke="{BORDER_GREEN}" stroke-width="2" stroke-opacity="0.55"/>')
    # Pulsing progress dot at the right end
    out.append(f'<circle cx="{timeline_x_end}" cy="{timeline_y}" r="6" fill="{GREEN_BRIGHT}" filter="url(#glow)">')
    out.append(f'<animate attributeName="opacity" values="1;0.4;1" dur="1.6s" repeatCount="indefinite"/></circle>')

    # Year ticks
    years = [1398, 1399, 1401, 1404, "now"]
    for i, y in enumerate(years):
        x = timeline_x_start + int(timeline_w * i / (len(years) - 1))
        out.append(f'<line x1="{x}" y1="{timeline_y-6}" x2="{x}" y2="{timeline_y+6}" stroke="{GREEN}" stroke-width="1"/>')
        out.append(f'<text x="{x}" y="{timeline_y+24}" text-anchor="middle" class="meta">{y}</text>')

    # 4 career cards (alternating above/below timeline)
    card_w = 250
    card_h = 200
    for i, job in enumerate(CAREER):
        # Card x position along timeline
        # Place at year fraction
        if i < 3:
            tx = timeline_x_start + int(timeline_w * i / 3)
        else:
            tx = timeline_x_end - 30
        above = (i % 2 == 0)
        card_x = tx - card_w // 2
        card_y = timeline_y - card_h - 30 if above else timeline_y + 50
        # Clamp
        card_x = max(timeline_x_start, min(card_x, timeline_x_end - card_w))

        c = job["color"]

        # Connector line from card to timeline
        connector_y_start = card_y + card_h if above else card_y
        connector_y_end   = timeline_y
        out.append(f'<line x1="{tx}" y1="{connector_y_start}" x2="{tx}" y2="{connector_y_end}" '
                   f'stroke="{c}" stroke-width="1" stroke-opacity="0.7"/>')

        # Card
        out.append(f'<g transform="translate({card_x},{card_y})">')
        out.append(f'<rect x="0" y="0" width="{card_w}" height="{card_h}" rx="8" '
                   f'fill="{BG_PANEL_SOFT}" stroke="{c}" stroke-width="1" stroke-opacity="0.6" '
                   f'filter="url(#glow)"/>')
        # Accent strip
        out.append(f'<rect x="0" y="0" width="6" height="{card_h}" rx="3" fill="{c}" opacity="0.85"/>')
        # Period
        period_str = f"{job['start']}" + (f" – {job['end']}" if job['end'] else " – now")
        out.append(f'<text x="20" y="22" class="meta" fill="{c}">{esc(period_str)}</text>')
        # Tag chip
        out.append(f'<g transform="translate({card_w - 80}, 12)">')
        out.append(f'<rect x="0" y="0" width="64" height="18" rx="9" fill="{BG_DARK}" stroke="{c}" stroke-width="0.7" stroke-opacity="0.5"/>')
        out.append(f'<text x="32" y="13" text-anchor="middle" class="meta" fill="{c}">{esc(job["tag"])}</text>')
        out.append('</g>')
        # Role
        out.append(f'<text x="20" y="50" class="h2" font-size="16" fill="{TEXT_PRIMARY}">{esc(job["role"])}</text>')
        # Company
        out.append(f'<text x="20" y="70" class="val" font-size="12" fill="{TEXT_SECOND}">{esc(job["company"])}</text>')
        # Location
        out.append(f'<text x="20" y="86" class="meta">[ {esc(job["location"])} ]</text>')
        # Separator
        out.append(f'<line x1="20" y1="96" x2="{card_w-20}" y2="96" stroke="{c}" stroke-width="0.4" stroke-opacity="0.3"/>')
        # Bullets
        by = 112
        for b in job["bullets"]:
            out.append(f'<circle cx="26" cy="{by - 3}" r="2" fill="{c}"/>')
            # Wrap text — keep under card width
            truncated = b if len(b) < 38 else b[:36] + "…"
            out.append(f'<text x="36" y="{by}" class="val" font-size="11" fill="{TEXT_PRIMARY}">{esc(truncated)}</text>')
            by += 18
        out.append('</g>')

        # Milestone dot on timeline
        out.append(f'<circle cx="{tx}" cy="{timeline_y}" r="7" fill="{c}" stroke="#0b1220" stroke-width="2" filter="url(#glow)"/>')
        out.append(f'<circle cx="{tx}" cy="{timeline_y}" r="3" fill="{BG_DARK}"/>')

    # Bottom legend / footer
    out.append(f'<text x="{W//2}" y="{H-22}" text-anchor="middle" class="meta" fill="{TEXT_DIM}">// trajectory · game → web → education → leadership · still building //</text>')

    out.append(svg_close())
    return ''.join(out)


# ====================================================================
#  SECTION 4 — EDUCATION & KNOWLEDGE
# ====================================================================
EDUCATION = [
    {
        "degree":   "Bachelor of Computer Engineering",
        "field":    "Software",
        "school":   "Islamic Azad University, Kermanshah",
        "city":     "Kermanshah",
        "period":   "1402 – 1404",
        "gpa":      "18.5",
        "color":    GREEN_BRIGHT,
    },
    {
        "degree":   "Associate Degree in Computer Engineering",
        "field":    "Software",
        "school":   "Ilam National Skills University",
        "city":     "Ilam",
        "period":   "1400 – 1402",
        "gpa":      "17.70",
        "color":    GREEN_BRIGHT,
    },
]

LANGUAGES = [
    ("English",  [("Reading", 4), ("Writing", 4), ("Speaking", 3), ("Listening", 4)], GREEN_BRIGHT),
    ("French",  [("Reading", 2), ("Writing", 2), ("Speaking", 1), ("Listening", 2)], AMBER),
]


def section_education_knowledge():
    out = [svg_open()]
    out.append(defs_common())
    out.append(background("EDUCATION & KNOWLEDGE"))

    out.append(f'<text x="32" y="108" class="mono" font-size="11" fill="{TEXT_DIM}" letter-spacing="2">// ACADEMIC BACKGROUND  //  LANGUAGES  //  CONTINUOUS LEARNING</text>')

    # Left column: Education cards
    out.append(f'<text x="40" y="148" class="h3" fill="{GREEN_BRIGHT}">// ACADEMIC RECORD</text>')

    card_x = 40
    card_y_start = 160
    card_w = 520
    card_h = 200

    for i, edu in enumerate(EDUCATION):
        cy = card_y_start + i * (card_h + 24)
        c = edu["color"]
        out.append(f'<g transform="translate({card_x},{cy})">')
        out.append(f'<rect x="0" y="0" width="{card_w}" height="{card_h}" rx="10" '
                   f'fill="{BG_PANEL_SOFT}" stroke="{c}" stroke-width="1" stroke-opacity="0.55" '
                   f'filter="url(#glow)"/>')
        out.append(f'<rect x="0" y="0" width="6" height="{card_h}" rx="3" fill="{c}" opacity="0.85"/>')

        # Period chip
        out.append(f'<g transform="translate(20, 18)">')
        out.append(f'<rect x="0" y="0" width="130" height="22" rx="11" fill="{BG_DARK}" stroke="{c}" stroke-width="0.6" stroke-opacity="0.5"/>')
        out.append(f'<text x="65" y="15" text-anchor="middle" class="meta" fill="{c}">{esc(edu["period"])}</text>')
        out.append('</g>')

        # GPA chip
        out.append(f'<g transform="translate({card_w - 110}, 18)">')
        out.append(f'<rect x="0" y="0" width="90" height="22" rx="11" fill="{c}" opacity="0.18"/>')
        out.append(f'<text x="45" y="15" text-anchor="middle" class="mono" font-size="11" fill="{c}">GPA {esc(edu["gpa"])}</text>')
        out.append('</g>')

        # Degree
        out.append(f'<text x="20" y="62" class="h2" font-size="16" fill="{TEXT_PRIMARY}">{esc(edu["degree"])}</text>')
        out.append(f'<text x="20" y="84" class="key" font-size="12">// Field: <tspan fill="{TEXT_PRIMARY}">{esc(edu["field"])}</tspan></text>')
        out.append(f'<text x="20" y="106" class="val" font-size="12" fill="{TEXT_SECOND}">{esc(edu["school"])}</text>')
        out.append(f'<text x="20" y="124" class="meta">[ {esc(edu["city"])} ]</text>')

        # Decorative book icon / progress at bottom
        out.append(f'<line x1="20" y1="{card_h-30}" x2="{card_w-20}" y2="{card_h-30}" stroke="{c}" stroke-width="0.4" stroke-opacity="0.3"/>')
        out.append(f'<text x="20" y="{card_h-12}" class="meta">// CREDENTIAL_VERIFIED · GRADE_A · ACADEMIC_TRANSCRIPT_ON_FILE</text>')

        out.append('</g>')

    # Right column: Languages + skills badges
    right_x = 590
    out.append(f'<text x="{right_x}" y="148" class="h3" fill="{GREEN_BRIGHT}">// LANGUAGES</text>')

    lang_y = 160
    for lang_name, skills, color in LANGUAGES:
        out.append(f'<g transform="translate({right_x},{lang_y})">')
        out.append(f'<rect x="0" y="0" width="550" height="100" rx="10" '
                   f'fill="{BG_PANEL_SOFT}" stroke="{color}" stroke-width="0.8" stroke-opacity="0.4"/>')
        # Lang name
        out.append(f'<text x="20" y="32" class="h2" font-size="18" fill="{color}">{esc(lang_name)}</text>')
        # 4 sub-skills as small bars
        bx = 130
        bw = 90
        for skill_name, level in skills:
            out.append(f'<text x="{bx}" y="32" class="meta" fill="{TEXT_DIM}">{esc(skill_name)}</text>')
            # 5 dots, filled up to `level`
            for k in range(5):
                dx = bx + k * 12
                dy = 42
                if k < level:
                    out.append(f'<circle cx="{dx}" cy="{dy}" r="4" fill="{color}" filter="url(#glow)"/>')
                else:
                    out.append(f'<circle cx="{dx}" cy="{dy}" r="4" fill="{BG_DARK}" stroke="{color}" stroke-width="0.6" stroke-opacity="0.4"/>')
            bx += bw
        # Bottom row meta
        out.append(f'<text x="20" y="80" class="meta">// CEFR-equiv: { "B2" if esc(lang_name) == "English" else "A1-A2" }</text>')
        out.append('</g>')
        lang_y += 120

    # Bottom: skills mastery badges
    out.append(f'<text x="{right_x}" y="{lang_y+12}" class="h3" fill="{GREEN_BRIGHT}">// MASTERY BADGES</text>')

    badges = [
        ("Clean Arch",     100, GREEN_BRIGHT),
        ("RESTful API",    100, GREEN_BRIGHT),
        ("React.js",       100, GREEN_BRIGHT),
        ("PostgreSQL",     100, GREEN_BRIGHT),
        ("Docker",         100, GREEN_BRIGHT),
        ("Linux Admin",    100, GREEN_BRIGHT),
        ("Agile / Scrum",  100, AMBER),
        ("Tech Lead",      100, RED),
    ]
    bx = right_x
    by = lang_y + 26
    badge_w = 145
    badge_h = 28
    per_row = 4
    for i, (name, pct, color) in enumerate(badges):
        col = i % per_row
        row = i // per_row
        x = bx + col * (badge_w + 8)
        y = by + row * (badge_h + 8)
        out.append(f'<g transform="translate({x},{y})">')
        out.append(f'<rect x="0" y="0" width="{badge_w}" height="{badge_h}" rx="14" '
                   f'fill="{BG_DARK}" stroke="{color}" stroke-width="0.7" stroke-opacity="0.6"/>')
        out.append(f'<circle cx="14" cy="{badge_h//2}" r="4" fill="{color}"><animate attributeName="opacity" values="1;0.4;1" dur="2s" begin="{i*0.2}s" repeatCount="indefinite"/></circle>')
        out.append(f'<text x="26" y="{badge_h//2 + 4}" class="val" font-size="11">{esc(name)}</text>')
        out.append(f'<text x="{badge_w-8}" y="{badge_h//2 + 4}" text-anchor="end" class="meta" fill="{color}">{pct}%</text>')
        out.append('</g>')

    # Bottom callout
    out.append(f'<text x="{W//2}" y="{H-22}" text-anchor="middle" class="meta" fill="{TEXT_DIM}">// learning is continuous · the architect never stops refining the craft //</text>')

    out.append(svg_close())
    return ''.join(out)


# ====================================================================
#  SECTION 5 — CONTACT NETWORK
# ====================================================================
CONTACTS = [
    {"key": "EMAIL",    "value": "mrparsataheri1@gmail.com",   "color": GREEN_BRIGHT, "icon": "envelope"},
    {"key": "TELEGRAM", "value": "@p2002t",                    "color": GREEN_BRIGHT, "icon": "send"},
    {"key": "LINKEDIN", "value": "parsa-taheri-781b90355",     "color": GREEN_BRIGHT, "icon": "linkedin"},
    {"key": "GITHUB",   "value": "parsa-kraken",               "color": GREEN_BRIGHT, "icon": "github"},
    {"key": "LOCATION", "value": "Tehran, Iran",              "color": AMBER,         "icon": "pin"},
    {"key": "STATUS",   "value": "Open to collaborations",    "color": RED,           "icon": "dot"},
]


def _icon_path(name, color):
    """Return SVG path string for a simple icon. 24x24 viewBox."""
    if name == "envelope":
        return (
            f'<rect x="2" y="6" width="20" height="13" rx="2" fill="none" stroke="{color}" stroke-width="1.4"/>'
            f'<path d="M 2 8 L 12 14 L 22 8" fill="none" stroke="{color}" stroke-width="1.4"/>'
        )
    if name == "send":
        return (
            f'<path d="M 3 12 L 22 3 L 13 22 L 11 14 Z" fill="none" stroke="{color}" stroke-width="1.4" stroke-linejoin="round"/>'
            f'<line x1="11" y1="14" x2="22" y2="3" stroke="{color}" stroke-width="1.4"/>'
        )
    if name == "linkedin":
        return (
            f'<rect x="2" y="2" width="20" height="20" rx="3" fill="none" stroke="{color}" stroke-width="1.4"/>'
            f'<line x1="7" y1="7" x2="7" y2="17" stroke="{color}" stroke-width="1.6"/>'
            f'<circle cx="7" cy="5" r="1.2" fill="{color}"/>'
            f'<path d="M 11 17 L 11 9 M 11 13 C 12 10 16 9 17 13 L 17 17" fill="none" stroke="{color}" stroke-width="1.6" stroke-linejoin="round"/>'
        )
    if name == "github":
        return (
            f'<path d="M 12 2 C 6.5 2 2 6.5 2 12 C 2 16.5 5 20.4 9 21.8 C 9.5 21.9 9.7 21.5 9.7 21.2 L 9.7 19.5 C 7 20.1 6.4 18.3 6.4 18.3 C 6 17.2 5.4 16.9 5.4 16.9 C 4.6 16.4 5.5 16.4 5.5 16.4 C 6.5 16.5 7 17.4 7 17.4 C 7.8 18.9 9.2 18.5 9.7 18.2 C 9.8 17.6 10 17.2 10.3 17 C 8.1 16.7 5.8 15.8 5.8 11.9 C 5.8 10.8 6.2 9.9 6.9 9.2 C 6.8 9 6.4 7.9 7 6.4 C 7 6.4 7.9 6.1 9.7 7.4 C 10.5 7.2 11.3 7.1 12 7.1 C 12.7 7.1 13.5 7.2 14.3 7.4 C 16.1 6.1 17 6.4 17 6.4 C 17.6 7.9 17.2 9 17.1 9.2 C 17.8 9.9 18.2 10.8 18.2 11.9 C 18.2 15.8 15.9 16.7 13.7 17 C 14 17.3 14.3 17.8 14.3 18.6 L 14.3 21.2 C 14.3 21.5 14.5 21.9 15 21.8 C 19 20.4 22 16.5 22 12 C 22 6.5 17.5 2 12 2 Z" fill="{color}" fill-opacity="0.9"/>'
        )
    if name == "pin":
        return (
            f'<path d="M 12 2 C 7.5 2 4 5.5 4 10 C 4 16 12 22 12 22 C 12 22 20 16 20 10 C 20 5.5 16.5 2 12 2 Z" fill="none" stroke="{color}" stroke-width="1.4"/>'
            f'<circle cx="12" cy="10" r="3" fill="none" stroke="{color}" stroke-width="1.4"/>'
        )
    if name == "dot":
        return (
            f'<circle cx="12" cy="12" r="6" fill="none" stroke="{color}" stroke-width="1.4"/>'
            f'<circle cx="12" cy="12" r="3" fill="{color}"><animate attributeName="opacity" values="1;0.3;1" dur="1.5s" repeatCount="indefinite"/></circle>'
        )
    return ''


def section_contact_network():
    out = [svg_open()]
    out.append(defs_common())
    out.append(background("CONTACT NETWORK"))

    out.append(f'<text x="32" y="108" class="mono" font-size="11" fill="{TEXT_DIM}" letter-spacing="2">// 6 ENDPOINTS  //  OPEN FOR COLLABORATION  //  RESPONSE_TIME: &lt;24h</text>')

    # Grid 3x2 of contact cards
    card_w = 360
    card_h = 200
    gap = 16
    grid_x = (W - (3 * card_w + 2 * gap)) // 2  # center
    grid_y = 140

    for i, c in enumerate(CONTACTS):
        col = i % 3
        row = i // 3
        x = grid_x + col * (card_w + gap)
        y = grid_y + row * (card_h + gap)
        color = c["color"]

        out.append(f'<g transform="translate({x},{y})">')
        out.append(f'<rect x="0" y="0" width="{card_w}" height="{card_h}" rx="10" '
                   f'fill="{BG_PANEL_SOFT}" stroke="{color}" stroke-width="1" stroke-opacity="0.55" '
                   f'filter="url(#glow)"/>')
        # Accent corner
        out.append(f'<path d="M 0 0 L 60 0 L 0 60 Z" fill="{color}" opacity="0.12"/>')

        # Top row: key label + status dot
        out.append(f'<text x="20" y="30" class="meta" fill="{color}" letter-spacing="2">// {esc(c["key"])}</text>')
        out.append(f'<circle cx="{card_w-22}" cy="22" r="4" fill="{color}"><animate attributeName="opacity" values="1;0.4;1" dur="1.6s" begin="{i*0.2}s" repeatCount="indefinite"/></circle>')

        # Icon (centered in upper area)
        icon_y = 50
        out.append(f'<g transform="translate({card_w//2 - 12},{icon_y})">')
        out.append(_icon_path(c["icon"], color))
        out.append('</g>')

        # Value text (centered)
        out.append(f'<text x="{card_w//2}" y="150" text-anchor="middle" class="h2" font-size="16" fill="{TEXT_PRIMARY}">{esc(c["value"])}</text>')

        # Bottom meta
        out.append(f'<line x1="20" y1="{card_h-30}" x2="{card_w-20}" y2="{card_h-30}" stroke="{color}" stroke-width="0.4" stroke-opacity="0.3"/>')
        meta_text = {
            "EMAIL":    "// PGP available on request",
            "TELEGRAM": "// fastest response channel",
            "LINKEDIN": "// professional network",
            "GITHUB":   "// primary code hub",
            "LOCATION": "// UTC+3:30 · IRST",
            "STATUS":   "// actively building",
        }.get(c["key"], "// open")
        out.append(f'<text x="{card_w//2}" y="{card_h-12}" text-anchor="middle" class="meta" fill="{TEXT_DIM}">{meta_text}</text>')

        out.append('</g>')

    # Bottom callout
    out.append(f'<text x="{W//2}" y="{H-22}" text-anchor="middle" class="meta" fill="{TEXT_DIM}">// reach out · let us engineer something worth shipping together //</text>')

    out.append(svg_close())
    return ''.join(out)


# ====================================================================
#  Main — write all 5 sections
# ====================================================================
def main():
    sections = [
        ("01-tech-universe.svg",      section_tech_universe()),
        ("02-system-architecture.svg", section_system_architecture()),
        ("03-career-trajectory.svg",  section_career_trajectory()),
        ("04-education-knowledge.svg", section_education_knowledge()),
        ("05-contact-network.svg",    section_contact_network()),
    ]
    for fname, content in sections:
        path = SECTIONS / fname
        path.write_text(content, encoding="utf-8")
        print(f"  wrote {path.name}  ({len(content)} bytes)")


if __name__ == "__main__":
    main()
