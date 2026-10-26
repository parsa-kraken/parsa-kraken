# Final profile setup

This project is personalized for **Parsa Taheri** and is ready to push to GitHub.

## What's in this repository

| Path | Purpose |
|------|---------|
| `profile.json` | Single source of truth for ALL profile data (basic info, skills, career, education, contacts). |
| `profile.jpg` | Source portrait photo (converted to ASCII art on build). |
| `templates/light.template.svg`<br>`templates/dark.template.svg` | The main profile card template (left=ASCII portrait, right=SYSTEM.INFO text rows). |
| `light.svg`<br>`dark.svg` | Generated main profile cards (consumed by README). |
| `sections/01-tech-universe.svg` | Green panel: skill matrix with progress bars. |
| `sections/02-system-architecture.svg` | Green panel: layered architecture diagram. |
| `sections/03-career-trajectory.svg` | Green panel: work experience timeline. |
| `sections/04-education-knowledge.svg` | Green panel: education + languages + mastery badges. |
| `sections/05-contact-network.svg` | Green panel: contact info grid. |
| `dist/github-snake.svg`<br>`dist/github-snake-dark.svg` | **Live** GitHub contribution snake — auto-generated daily by the GitHub Action. |
| `.github/workflows/jet-heatmap.yml` | GitHub Action that regenerates the snake SVGs daily. |
| `README.md`<br>`README.template.md` | Profile README (final + template). |
| `build_profile.py` | Generates `light.svg`, `dark.svg`, `README.md` from `profile.json` + templates. |
| `scripts/build_sections.py` | Generates all 5 `sections/*.svg` panels from the data inside the script. |
| `scripts/fix_alignment.py` | Patches the SYSTEM.INFO rows in `light/dark.svg` + templates so all values left-align to the same x-column. Run after every `build_profile.py` rebuild. |

## Build workflow

```bash
# 1. Install Python deps (only needed once)
pip install -r requirements.txt

# 2. Regenerate the main profile cards + README
python build_profile.py

# 3. Fix the SYSTEM.INFO row alignment in the freshly-generated SVGs
python scripts/fix_alignment.py

# 4. Regenerate the 5 green section SVGs
python scripts/build_sections.py
```

After any edit to `profile.json` (or to the section data inside `scripts/build_sections.py`), re-run steps 2–4.

## Design decisions

### Palette
- The original purple/indigo accents were converted to hacker green.
- The old blue/cyan accents were converted to red.
- The 5 new green sections use a dark navy background (`#0b1220`) with green/red accents to match.

### Row alignment in SYSTEM.INFO
- The original template relied on hand-tuned dot filler counts per row, which left the value column at different x-positions per row (the user reported "7 out of 11 don't start on the same column").
- The patched layout uses explicit `x` attributes on every `<tspan>`:
  - prefix `. ` at x=520
  - red key at x=540
  - dots filler `: ............... ` at x=720 (fixed width)
  - value at x=870 (always the same column)
- The patch is applied by `scripts/fix_alignment.py` and is re-runnable.

### Contribution chart
- The old `dist/github-jet.svg` was a manually-drawn fake: an animated jet flying over randomly-colored squares that looked like a contribution heatmap but were not real data. It has been removed.
- The README now embeds the **real** contribution snake at `dist/github-snake.svg` (and `-dark.svg`), which is regenerated daily by `Platane/snk` via `.github/workflows/jet-heatmap.yml`.
- The README also pulls live stats from `github-readme-stats.vercel.app` so the numbers are always real.

### Green sections
- The 5 green panels (`sections/01..05`) are inspired by the shinobi-coder profile layout (technology universe + system architecture style), customized with Parsa Taheri's CV data.
- All data is in `profile.json`; the display-friendly shortened strings live in `scripts/build_sections.py` because the SVG layout has tight horizontal space constraints.

## Privacy
- Phone numbers, birth date, marital status, and military-service details from the source CV are intentionally NOT published in any of the SVG panels. They remain only in the source CV.

## Public profile note
- After pushing to GitHub, visit the **Actions** tab and run the "Sync live contribution snake" workflow once manually. It will then update daily on its own.
