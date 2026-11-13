#!/usr/bin/env python3
"""
Re-style the Platane/snk contribution snake with the "commit log" board design
(the same visual style as Sushmitadasari's assets/contribution-snake.svg),
while keeping the original snake's MOVEMENT ALGORITHM:

  * the exact route waypoints parsed from the snk keyframes (same path, same
    cell-by-cell speed, same seamless loop)
  * by default the loop is TRAVERSED IN REVERSE (--keep-direction disables
    this): the raw snk solver eats the small commits first and the biggest
    ones last, so playing the very same loop backwards makes the snake go for
    the BIG commits first and the small ones at the end - exactly the
    behaviour the profile owner asked to keep

Everything visual comes from the friend's board design, re-themed to the
owner's cyberpunk palette (deep black #111119 / violet #8B35FF /
neon pink #D500F9 / electric blue #00D9FF / neon yellow #FFE500):
1200x410 deep-black board, serif headline, 4 stat blocks (CONTRIBUTIONS,
ACTIVE DAYS, LONGEST STREAK, BUSIEST DAY), month + weekday labels,
15px rounded cells with a pop-in wave, a 9-segment violet->pink snake with
a glowing electric-blue head and eyes, longest-streak marker (neon yellow),
footer + Less/More legend.

Usage:
  python scripts/build_snake.py --input dist/raw/github-snake.svg \
      --login parsa-kraken --out dist/github-snake.svg --out-dark dist/github-snake-dark.svg \
      [--counts data/contributions-snapshot.json | --fetch] [--window-end 2026-10-25]

If the input SVG is already restyled (no snk keyframes found) the script
exits without touching anything, so it is safe to re-run.
"""
import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path
from urllib import request as urlreq

# ----------------------------------------------------------------------------
# Board design tokens - CYBERPUNK minimal theme
#   deep black #111119 / violet #8B35FF / neon pink #D500F9 /
#   electric blue #00D9FF / neon yellow #FFE500
# (board layout kept from Sushmitadasari's commit-log design,
#  colours re-themed to the cyberpunk palette)
# ----------------------------------------------------------------------------
W, H = 1200, 410
CELL, GAP = 15, 4
STEP = CELL + GAP
GRID_X, GRID_Y = 118, 182
# heat ramp: empty -> deep violet -> violet -> neon pink -> electric blue (peak)
LEVELS = ["#1E1E2C", "#3D2870", "#8B35FF", "#D500F9", "#00D9FF"]
HEAD_COLOR, TRAIL_A, TRAIL_B, TAIL_COLOR = "#00D9FF", "#8B35FF", "#5B2AA6", "#D500F9"
TEXT_MAIN, TEXT_PINK, TEXT_DIM = "#F2F2FA", "#B98AFF", "#8A8AA8"
TEXT_BLUE, TEXT_YELLOW = "#00D9FF", "#FFE500"
EYE_COLOR = "#0C0C14"
SNAKE_BEGIN = 2.4  # seconds before the snake starts (lets cells pop in first)
SEGMENTS = 9
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def fmt_date(d):
    return f"{d.day} {MONTHS[d.month - 1]} {d.year}"


# ----------------------------------------------------------------------------
# 1) Parse the snk SVG: grid cells, levels, eat percentages, head route
# ----------------------------------------------------------------------------
def parse_snk(svg_text):
    kf = {}
    for ch in re.split(r"@keyframes ", svg_text)[1:]:
        name = ch.split("{", 1)[0]
        end = ch.find("}}")
        if end == -1:
            continue
        kf[name] = ch[ch.find("{") + 1:end]

    cells = {}
    for m in re.finditer(r'<rect class="c( c[\w]+)?" x="(-?\d+)" y="(-?\d+)" rx="2" ry="2"/>', svg_text):
        cls, x, y = m.group(1), int(m.group(2)), int(m.group(3))
        col, row = (x - 2) // 16, (y - 2) // 16
        if cls:  # this cell gets eaten: level + percentage of the loop
            body = kf.get(cls.strip(), "")
            fm = re.match(r"([\d.]+)%\{fill:var\(--c(\d)\)\}", body)
            if not fm:
                raise SystemExit("Unexpected snk keyframe for " + cls)
            cells[(col, row)] = {"eat": float(fm.group(1)), "level": int(fm.group(2))}
        else:
            cells[(col, row)] = {"eat": None, "level": 0}

    route = []
    body = kf.get("s0", "")
    for pcts, tx, ty in re.findall(r"([\d.,%]+)\{transform:translate\((-?\d+)px,(-?\d+)px\)\}", body):
        for p in pcts.split(","):
            route.append([float(p.rstrip("%")), int(tx) // 16, int(ty) // 16])
    route.sort(key=lambda w: w[0])
    if not cells or not route:
        raise SystemExit("Input does not look like a Platane/snk SVG - nothing to do.")
    return cells, route


# ----------------------------------------------------------------------------
# 2) Contribution counts (real, public calendar - same source as the friend's)
# ----------------------------------------------------------------------------
def parse_calendar_html(html):
    tds = re.findall(r'data-date="(\d{4}-\d{2}-\d{2})"[^>]*id="(contribution-day-component-[\d-]+)"[^>]*data-level="(\d)"', html)
    tips = dict(re.findall(r'<tool-tip[^>]*for="(contribution-day-component-[\d-]+)"[^>]*>([^<]+)</tool-tip>', html))
    out = {}
    for date, tid, _lvl in tds:
        t = tips.get(tid, "")
        m = re.match(r"(\d+)\s+contributions?", t)
        out[date] = int(m.group(1)) if m else 0
    return out


def fetch_counts(login):
    today = dt.date.today()
    counts = {}
    for year in (today.year, today.year - 1):
        url = f"https://github.com/users/{login}/contributions?from={year}-01-01&to={year}-12-31"
        try:
            req = urlreq.Request(url, headers={"User-Agent": "Mozilla/5.0 (snake-restyler)"})
            with urlreq.urlopen(req, timeout=25) as r:
                counts.update(parse_calendar_html(r.read().decode("utf-8", "ignore")))
        except Exception as e:  # noqa: BLE001 - graceful degradation
            print(f"warn: could not fetch {year} calendar: {e}")
    print(f"fetched {len(counts)} days of real contribution counts")
    return counts or None


# ----------------------------------------------------------------------------
# 3) Build the friend-style board from the parsed snake
# ----------------------------------------------------------------------------
def build_board(cells, route, login, window_end, counts, loop_dur, first_date=None):
    cols = sorted(set(c for c, _ in cells))
    rows = sorted(set(r for _, r in cells))
    n_cols, n_rows = max(cols) + 1, max(rows) + 1

    # Window: `n_cols` Sunday-based weeks; window_end is the snapshot date and
    # its week is the last (partial) column of the grid.
    we = dt.date.fromisoformat(window_end)
    last_week_start = we - dt.timedelta(days=(we.weekday() + 1) % 7)  # back to Sunday
    start = last_week_start - dt.timedelta(weeks=n_cols - 1)
    end = last_week_start + dt.timedelta(days=6)  # Saturday closing the window
    days = [start + dt.timedelta(days=i) for i in range(n_cols * 7)]

    # level per day comes from the parsed grid (the snake's own world);
    # counts come from the real calendar, zeroed where the snapshot grid is 0
    # row of the week is Sunday-based (row 0 = Sunday, like GitHub's calendar)
    def cell_key(d):
        return ((d - start).days // 7, (d.weekday() + 1) % 7)

    # When does the head touch each cell on the (possibly reversed) loop?
    # A cell is eaten the FIRST time the head reaches it. Sampling at
    # quarter-cell steps captures mid-segment crossings and waypoint stops;
    # positions snapped only when near a cell centre (axis-aligned moves).
    visits = {}
    for (p1, c1, r1), (p2, c2, r2) in zip(route, route[1:]):
        steps = abs(c2 - c1) + abs(r2 - r1)
        if steps == 0:
            continue
        n = max(steps * 4, 1)
        for k in range(n + 1):
            t = p1 + (p2 - p1) * k / n
            col = c1 + (c2 - c1) * k / n
            row = r1 + (r2 - r1) * k / n
            if abs(col - round(col)) < 0.3 and abs(row - round(row)) < 0.3:
                key = (int(round(col)), int(round(row)))
                if key not in visits or t < visits[key]:
                    visits[key] = t

    def grid_level(d):
        cell = cells.get(cell_key(d))
        return cell["level"] if cell else 0

    def grid_eat(d):
        """Loop percentage when the head eats this cell, or None."""
        cell = cells.get(cell_key(d))
        if not cell or cell["eat"] is None:
            return None
        return visits.get(cell_key(d))

    def day_count(d):
        if grid_level(d) == 0:
            return 0
        if counts and d.isoformat() in counts:
            return counts[d.isoformat()]
        return None  # unknown (no counts provided)

    total = sum(c for c in (day_count(d) for d in days) if c)
    active_days = [d for d in days if grid_level(d) > 0]
    # longest streak of consecutive active days
    best_run, run, best_end = 0, 0, None
    for d in days:
        if grid_level(d) > 0:
            run += 1
            if run > best_run:
                best_run, best_end = run, d
        else:
            run = 0
    best_start = best_end - dt.timedelta(days=best_run - 1) if best_end else None
    counted = [d for d in days if (day_count(d) or 0) > 0]
    peak = max(counted, key=lambda d: day_count(d)) if counted else None

    # ---------------------------------------------------------------- cells --
    def center(col, row):
        return (GRID_X + col * STEP + CELL / 2, GRID_Y + row * STEP + CELL / 2)

    cells_svg = []
    for d in days:
        col, row = (d - start).days // 7, (d.weekday() + 1) % 7
        lvl = grid_level(d)
        x, y = GRID_X + col * STEP, GRID_Y + row * STEP
        delay = 0.3 + (col + row * 1.6) * 0.018
        glow = ' filter="url(#hm-glow)"' if lvl == 4 else ""
        color = LEVELS[min(lvl, 4)]
        eat = ""
        if grid_eat(d) is not None:
            eat_frac = min(max(grid_eat(d) / 100.0, 0.0001), 0.9999)
            eat = (f'<animate attributeName="fill" values="{color};{LEVELS[0]}" '
                   f'keyTimes="0;{eat_frac:.4f}" calcMode="discrete" '
                   f'dur="{loop_dur:.2f}s" begin="{SNAKE_BEGIN}s" repeatCount="indefinite"/>')
        c = day_count(d)
        title = (f"{c} contribution{'' if c == 1 else 's'} \u00b7 {fmt_date(d)}"
                 if c is not None else fmt_date(d))
        cells_svg.append(
            f'<rect class="hm-c" style="animation-delay:{delay:.3f}s" x="{x}" y="{y}" '
            f'width="{CELL}" height="{CELL}" rx="3.5" fill="{color}"{glow}>'
            f"<title>{esc(title)}</title>{eat}</rect>"
        )
    cells_svg = "\n    ".join(cells_svg)

    # ---------------------------------------------------------------- route --
    pts = [(center(c, r)[0], center(c, r)[1]) for _p, c, r in route]
    key_times = [p / 100.0 for p, _c, _r in route]
    if key_times[-1] < 1.0:  # hold the final position until the loop restarts
        pts.append(pts[-1])
        key_times.append(1.0)
    # guard: strictly increasing keyTimes
    for i in range(1, len(key_times)):
        if key_times[i] <= key_times[i - 1]:
            key_times[i] = key_times[i - 1] + 1e-4
    # cumulative length -> keyPoints
    cum, total_len = [0.0], 0.0
    for i in range(1, len(pts)):
        total_len += abs(pts[i][0] - pts[i - 1][0]) + abs(pts[i][1] - pts[i - 1][1])
        cum.append(total_len)
    key_points = [round(c / total_len, 6) for c in cum]
    key_points[0], key_points[-1] = 0.0, 1.0
    kt = ";".join(f"{t:.4f}" for t in key_times)
    kp = ";".join(f"{v:.6f}" for v in key_points)
    path_d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)

    # per-cell seconds (for the 1-cell-per-segment trail delay)
    moves = []
    for i in range(1, len(route)):
        dp = route[i][0] - route[i - 1][0]
        dc = abs(route[i][1] - route[i - 1][1]) + abs(route[i][2] - route[i - 1][2])
        if dc and dp > 0:
            moves.append(dp / dc)
    per_cell_pct = sorted(moves)[len(moves) // 2] if moves else 0.375
    per_cell_sec = loop_dur * per_cell_pct / 100.0

    # ---------------------------------------------------------------- snake --
    segs = []
    for k in range(SEGMENTS):
        seg = SEGMENTS - 1 - k  # draw tail first so the head sits on top
        size = CELL - seg * 0.9
        fill = HEAD_COLOR if seg == 0 else TRAIL_A if seg < 3 else TRAIL_B if seg < 6 else TAIL_COLOR
        op = 1 - seg * 0.06
        glow = ' filter="url(#hm-glow)"' if seg == 0 else ""
        begin = SNAKE_BEGIN + seg * per_cell_sec
        eyes = (f'<circle cx="{size / 2 - 4:.1f}" cy="-2.5" r="1.3" fill="{EYE_COLOR}"/>'
                f'<circle cx="{size / 2 - 4:.1f}" cy="2.5" r="1.3" fill="{EYE_COLOR}"/>') if seg == 0 else ""
        segs.append(
            f'<g opacity="0"{glow}>'
            f'<animateMotion path="{path_d}" rotate="auto" dur="{loop_dur:.2f}s" '
            f'begin="{begin:.3f}s" repeatCount="indefinite" calcMode="linear" '
            f'keyPoints="{kp}" keyTimes="{kt}"/>'
            f'<animate attributeName="opacity" values="{op:.2f};{op:.2f}" '
            f'keyTimes="0;1" calcMode="discrete" dur="{loop_dur:.2f}s" '
            f'begin="{begin:.3f}s" repeatCount="indefinite"/>'
            f'<rect x="{-size / 2:.1f}" y="{-size / 2:.1f}" width="{size:.1f}" '
            f'height="{size:.1f}" rx="{size / 2.6:.1f}" fill="{fill}"/>{eyes}</g>'
        )
    snake_svg = "\n    ".join(segs)

    # ---------------------------------------------------------------- labels --
    labels, last_month = [], -1
    for d in days:
        m = d.month - 1
        if m == last_month:
            continue
        last_month = m
        labels.append({"col": (d - start).days // 7, "text": MONTHS[m]})
    if len(labels) > 1 and labels[1]["col"] - labels[0]["col"] < 3:
        labels = labels[1:]
    month_svg = "".join(
        f'<text x="{GRID_X + lb["col"] * STEP}" y="{GRID_Y - 12}">{lb["text"]}</text>'
        for lb in labels
    )
    day_labels = "".join(
        f'<text x="{GRID_X - 12}" y="{GRID_Y + r * STEP + 11}">{name}</text>'
        for r, name in ((1, "Mon"), (3, "Wed"), (5, "Fri"))
    )

    # -------------------------------------------------------------- streak ---
    streak_svg = ""
    if best_run > 1 and best_start is not None:
        sx = GRID_X + ((best_start - start).days // 7) * STEP + CELL / 2  # streak start column
        label_x = min(sx, W - 430)
        streak_svg = (
            f'<g class="hm-fade" style="animation-delay:2.6s">\n'
            f'    <path d="M{sx:.0f} {GRID_Y + 7 * STEP - 2} V {GRID_Y + 7 * STEP + 10}" '
            f'stroke="{TEXT_YELLOW}" stroke-opacity=".75"/>\n'
            f'    <text class="hm-mono" x="{label_x:.0f}" y="{GRID_Y + 7 * STEP + 24}" '
            f'font-size="10.5" letter-spacing="1.6" fill="{TEXT_YELLOW}">'
            f'LONGEST STREAK \u00b7 {best_run} DAYS \u00b7 {fmt_date(best_start).upper()} '
            f'\u2013 {fmt_date(best_end).upper()}</text>\n  </g>'
        )

    # ---------------------------------------------------------------- stats --
    date_range = f"{MONTHS[start.month - 1]} {start.year} \u2013 {MONTHS[end.month - 1]} {end.year}"
    stats = [
        ("CONTRIBUTIONS", f"{total:,}" if total else "\u2014", date_range),
        ("ACTIVE DAYS", str(len(active_days)), f"of {len(days)} days"),
        ("LONGEST STREAK", str(best_run) if best_run else "0", "consecutive days"),
        ("BUSIEST DAY", f"{day_count(peak)}" if peak else "\u2014",
         fmt_date(peak) if peak else "no data"),
    ]
    stats_svg = []
    for i, (label, value, sub) in enumerate(stats):
        x = 610 + i * 150
        stats_svg.append(
            f'<g transform="translate({x} 58)">\n'
            f'      <text class="hm-mono" font-size="10" letter-spacing="1.8" fill="{TEXT_PINK}">{label}</text>\n'
            f'      <text class="hm-serif" y="44" font-size="36" font-weight="300" fill="{TEXT_MAIN}">{esc(value)}</text>\n'
            f'      <text class="hm-mono" y="64" font-size="9.5" fill="{TEXT_DIM}">{esc(sub)}</text>\n'
            f'    </g>'
        )
    stats_svg = "\n    ".join(stats_svg)

    # --------------------------------------------------------------- legend --
    legend_x = W - 56 - 5 * 18 - 70
    legend = "".join(
        f'<rect x="{legend_x + 36 + i * 18}" y="372" width="12" height="12" rx="3" fill="{c}"/>'
        for i, c in enumerate(LEVELS)
    )

    snapshot = fmt_date(we)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="hm-title hm-desc">
  <title id="hm-title">GitHub contributions for @{esc(login)}</title>
  <desc id="hm-desc">{total} contributions from {fmt_date(start)} to {fmt_date(end)}: {len(active_days)} active days, longest streak {best_run} days{", busiest day " + str(day_count(peak)) + " contributions on " + fmt_date(peak) if peak else ""}. Source: public GitHub contribution calendar, snapshot {snapshot}.</desc>
  <defs>
    <linearGradient id="hm-bg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#1B1B28"/><stop offset="1" stop-color="#111119"/>
    </linearGradient>
    <radialGradient id="hm-light" cx="88%" cy="0%" r="70%">
      <stop offset="0" stop-color="#8B35FF" stop-opacity=".30"/><stop offset=".55" stop-color="#D500F9" stop-opacity=".10"/><stop offset="1" stop-color="#8B35FF" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="hm-light2" cx="0%" cy="100%" r="60%">
      <stop offset="0" stop-color="#00D9FF" stop-opacity=".14"/><stop offset="1" stop-color="#00D9FF" stop-opacity="0"/>
    </radialGradient>
    <filter id="hm-glow" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="2.4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
  <style>
    .hm-serif {{ font-family: Georgia, "Iowan Old Style", "Palatino Linotype", "Times New Roman", serif; }}
    .hm-mono {{ font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, "Liberation Mono", monospace; }}
    .hm-c {{ transform-box: fill-box; transform-origin: center; animation: hm-in .8s cubic-bezier(.34,1.56,.64,1) both; }}
    .hm-fade {{ animation: hm-fade 1.2s ease both; }}
    @keyframes hm-in {{ from {{ opacity: 0; transform: scale(.2); }} to {{ opacity: 1; transform: none; }} }}
    @keyframes hm-fade {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
    @media (prefers-reduced-motion: reduce) {{ .hm-c, .hm-fade {{ animation: none; }} .hm-motion {{ display: none; }} }}
  </style>

  <rect width="{W}" height="{H}" rx="20" fill="url(#hm-bg)"/>
  <rect width="{W}" height="{H}" rx="20" fill="url(#hm-light)"/>
  <rect width="{W}" height="{H}" rx="20" fill="url(#hm-light2)"/>
  <rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="19.5" fill="none" stroke="#8B35FF" stroke-opacity=".28"/>
  <rect x="5.5" y="5.5" width="{W - 11}" height="{H - 11}" rx="15" fill="none" stroke="#00D9FF" stroke-opacity=".10"/>

  <g class="hm-fade">
    <text class="hm-mono" x="56" y="68" font-size="11" letter-spacing="2.6" fill="{TEXT_BLUE}">COMMIT LOG \u00b7 REAL GITHUB ACTIVITY</text>
    <text class="hm-serif" x="54" y="110" font-size="27" font-weight="300" fill="{TEXT_MAIN}">A year of building, <tspan font-style="italic" fill="{TRAIL_A}">one square</tspan> at a time.</text>
    {stats_svg}
  </g>

  <g class="hm-mono" font-size="10.5" fill="{TEXT_DIM}">{month_svg}</g>
  <g class="hm-mono" font-size="10" fill="{TEXT_DIM}" text-anchor="end">
    {day_labels}
  </g>

  <g>
    {cells_svg}
  </g>

  <g class="hm-motion">
    {snake_svg}
  </g>

  {streak_svg}

  <g class="hm-fade">
    <text class="hm-mono" x="56" y="382" font-size="10.5" fill="{TEXT_DIM}">Source: public GitHub contribution calendar for @{esc(login)} \u00b7 snapshot {snapshot} \u00b7 refreshed daily</text>
    <text class="hm-mono" x="{legend_x}" y="382" font-size="10.5" fill="{TEXT_DIM}">Less</text>
    {legend}
    <text class="hm-mono" x="{legend_x + 36 + 5 * 18 + 4}" y="382" font-size="10.5" fill="{TEXT_DIM}">More</text>
  </g>
</svg>
'''
    return svg, {"total": total, "active": len(active_days), "streak": best_run,
                 "peak": (str(day_count(peak)), fmt_date(peak)) if peak else None,
                 "window": (str(start), str(end)), "per_cell_sec": round(per_cell_sec, 4)}


# ----------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default="dist/github-snake.svg")
    ap.add_argument("--login", default="parsa-kraken")
    ap.add_argument("--out", default="dist/github-snake.svg")
    ap.add_argument("--out-dark", default="dist/github-snake-dark.svg")
    ap.add_argument("--counts")
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--window-end", default=None,
                    help="last day of the grid window, e.g. 2026-10-25 (default: auto from input mtime)")
    ap.add_argument("--loop", type=float, default=26.7, help="loop duration seconds")
    ap.add_argument("--keep-direction", action="store_true",
                    help="keep the raw snk direction (small commits eaten first)")
    ap.add_argument("--preview-out")
    args = ap.parse_args()

    src = Path(args.input)
    text = src.read_text(encoding="utf-8")
    if "@keyframes s0" not in text:
        print("Input is already restyled (no snk keyframes) - leaving it untouched.")
        return

    cells, route = parse_snk(text)
    if not args.keep_direction:
        # play the very same loop backwards -> biggest commits get eaten first
        route = [(100.0 - p, c, r) for p, c, r in reversed(route)]
        route = [(0.0, route[0][1], route[0][2])] + route  # hold the entry cell at t=0
        print("route reversed: the snake now eats the biggest commits first")
    print(f"parsed: {len(cells)} cells, route of {len(route)} waypoints")

    counts = None
    if args.counts:
        counts = {d["date"]: d.get("count", 0) for d in json.load(open(args.counts))["days"]}
        print(f"counts from {args.counts}: {len(counts)} days")
    elif args.fetch:
        counts = fetch_counts(args.login)

    # window end: keep the snake's own snapshot date (mtime of the raw snk file)
    if args.window_end:
        window_end = args.window_end
    else:
        window_end = dt.date.fromtimestamp(src.stat().st_mtime).isoformat()
        print(f"window end auto = {window_end}")

    svg, info = build_board(cells, route, args.login, window_end, counts, args.loop)
    print("board:", json.dumps(info, ensure_ascii=False))

    for out in (args.out, args.out_dark):
        Path(out).parent.mkdir(parents=True, exist_ok=True)
        Path(out).write_text(svg, encoding="utf-8")
        print("wrote", out)

    # keep the raw snk SVG so re-runs are possible
    raw_dir = Path(args.out).parent / "raw"
    raw_dir.mkdir(exist_ok=True)
    (raw_dir / src.name).write_text(text, encoding="utf-8")
    print("raw snk svg archived to", raw_dir / src.name)

    if args.preview_out:
        psvg = re.sub(r'<g class="hm-motion">\s*', '<g class="hm-motion">\n    ', svg)
        # freeze the snake at points along the route for a static preview
        centers = []
        for p, c, r in route:
            centers.append((GRID_X + c * STEP + CELL / 2, GRID_Y + r * STEP + CELL / 2))
        idx = [int(len(centers) * f) for f in (0.25, 0.23, 0.21, 0.19, 0.17, 0.15, 0.13, 0.11, 0.09)]

        def freeze(m):
            i = freeze.i
            freeze.i += 1
            x, y = centers[idx[i]]
            return f'<g opacity="1" transform="translate({x:.1f} {y:.1f})">'
        freeze.i = 0
        psvg = re.sub(r'<g opacity="0">', freeze, psvg)
        psvg = re.sub(r'<animateMotion\b[^>]*/>', "", psvg)
        psvg = re.sub(r'<animateMotion\b[^>]*>.*?</animateMotion>', "", psvg, flags=re.S)
        psvg = re.sub(r'<animate\b[^>]*/>', "", psvg)
        psvg = re.sub(r'<animate\b[^>]*>.*?</animate>', "", psvg, flags=re.S)
        Path(args.preview_out).write_text(psvg, encoding="utf-8")
        print("wrote preview", args.preview_out)


if __name__ == "__main__":
    main()
