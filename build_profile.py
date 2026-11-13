#!/usr/bin/env python3
from pathlib import Path
from html import escape
import json
import sys

ROOT = Path(__file__).resolve().parent
PROFILE_PATH = ROOT / "profile.json"
PHOTO_CANDIDATES = [ROOT / "profile.jpg", ROOT / "profile.jpeg", ROOT / "profile.png", ROOT / "profile.webp"]
PORTRAIT_TXT = ROOT / "portrait.txt"
TEMPLATE_DIR = ROOT / "templates"

ASCII_WIDTH = 92
ASCII_HEIGHT = 53
START_X = 30
START_Y = 79.98
END_Y = 472.47
CHARSET = " .:-=+*#%@"

FIELDS = {
    "TERMINAL_ID": "terminal_id",
    "NAME": "name",
    "ROLE": "role",
    "ORIGIN": "origin",
    "EDUCATION": "education",
    "CURRENT": "current",
    "FOCUS": "focus",
    "EXPERIENCE": "experience",
    "LANGUAGES": "languages",
    "FRONTEND": "frontend",
    "BACKEND": "backend",
    "DATABASE": "database",
    "INFRA": "infra",
    "EMAIL": "email",
    "TELEGRAM": "telegram",
    "LINKEDIN": "linkedin",
    "GITHUB_USERNAME": "github_username",
}


def load_profile():
    data = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
    missing = [v for v in FIELDS.values() if v not in data]
    if missing:
        raise SystemExit("Missing profile.json fields: " + ", ".join(missing))
    return data


def photo_to_ascii(photo_path: Path):
    try:
        from PIL import Image, ImageEnhance, ImageOps
    except ImportError:
        raise SystemExit(
            "Pillow is required to convert profile.jpg. Run: pip install -r requirements.txt"
        )

    img = Image.open(photo_path)
    img = ImageOps.exif_transpose(img).convert("L")

    # Crop to the same visual proportions as the existing portrait panel.
    target_ratio = ASCII_WIDTH / (ASCII_HEIGHT * 1.95)
    w, h = img.size
    current_ratio = w / h
    if current_ratio > target_ratio:
        new_w = int(h * target_ratio)
        left = max(0, (w - new_w) // 2)
        img = img.crop((left, 0, left + new_w, h))
    else:
        new_h = int(w / target_ratio)
        top = max(0, (h - new_h) // 2)
        img = img.crop((0, top, w, top + new_h))

    # Normalize portrait contrast so facial features survive the ASCII conversion.
    img = ImageOps.autocontrast(img, cutoff=1)
    img = ImageEnhance.Contrast(img).enhance(1.55)
    img = ImageEnhance.Sharpness(img).enhance(1.25)
    img = img.resize((ASCII_WIDTH, ASCII_HEIGHT))

    pixels = list(img.getdata())
    chars = []
    scale = (len(CHARSET) - 1) / 255
    for row in range(ASCII_HEIGHT):
        line = "".join(CHARSET[round(pixels[row * ASCII_WIDTH + col] * scale)] for col in range(ASCII_WIDTH))
        chars.append(line)
    return chars


def load_portrait_lines():
    for p in PHOTO_CANDIDATES:
        if p.exists():
            print(f"Using photo: {p.name}")
            return photo_to_ascii(p)

    if not PORTRAIT_TXT.exists():
        raise SystemExit("Add profile.jpg/profile.png, or provide portrait.txt")

    lines = PORTRAIT_TXT.read_text(encoding="utf-8", errors="ignore").splitlines()
    lines = [(line[:ASCII_WIDTH]).ljust(ASCII_WIDTH) for line in lines[:ASCII_HEIGHT]]
    while len(lines) < ASCII_HEIGHT:
        lines.append(" " * ASCII_WIDTH)
    print("No profile photo found; using portrait.txt fallback")
    return lines


def portrait_tspans(lines):
    if ASCII_HEIGHT == 1:
        ys = [START_Y]
    else:
        step = (END_Y - START_Y) / (ASCII_HEIGHT - 1)
        ys = [START_Y + i * step for i in range(ASCII_HEIGHT)]
    out = []
    for y, line in zip(ys, lines):
        out.append(f'<tspan x="{START_X}" y="{y:.2f}" xml:space="preserve">{escape(line)}</tspan>')
    return "\n".join(out)


def render_svg(theme, data, portrait):
    src = TEMPLATE_DIR / f"{theme}.template.svg"
    text = src.read_text(encoding="utf-8")
    text = text.replace("{{PORTRAIT_TSPANS}}", portrait)
    for placeholder, key in FIELDS.items():
        text = text.replace("{{" + placeholder + "}}", escape(str(data[key])))
    out = ROOT / f"{theme}.svg"
    out.write_text(text, encoding="utf-8")
    print(f"Wrote {out.name}")


def render_readme(data):
    src = ROOT / "README.template.md"
    if not src.exists():
        return
    text = src.read_text(encoding="utf-8")
    text = text.replace("{{GITHUB_USERNAME}}", str(data["github_username"]))
    (ROOT / "README.md").write_text(text, encoding="utf-8")
    print("Wrote README.md")


def main():
    data = load_profile()
    lines = load_portrait_lines()
    tspans = portrait_tspans(lines)
    render_svg("light", data, tspans)
    render_svg("dark", data, tspans)
    render_readme(data)
    print("Profile build complete.")


if __name__ == "__main__":
    main()
