# Final profile setup

This project is personalized for **Parsa Taheri** and is ready to push to GitHub.

## What's in this repository

| Path | Purpose |
|------|---------|
| `profile.json` | Single source of truth for ALL profile data (basic info, skills, career, education, contacts). |
| `profile.jpg` | Source portrait photo (converted to ASCII art on build). |
| `templates/light.template.svg`<br>`templates/dark.template.svg` | The main profile card template (left=ASCII portrait, right=SYSTEM.INFO text rows). |
| `light.svg`<br>`dark.svg` | Generated main profile cards (consumed by README). |
| `sections/01-tech-universe.svg` | Cyberpunk panel: 4 stack panels (frontend / backend / AI / cloud) with tech badges. |
| `sections/02-ai-native-engineering.svg` | Cyberpunk panel: AI hero + LLM / vision cards + architecture strips. |
| `sections/03-career-trajectory.svg` | Cyberpunk panel: work experience timeline. |
| `sections/04-education-knowledge.svg` | Cyberpunk panel: education + languages + mastery badges. |
| `sections/05-contact-network.svg` | Cyberpunk panel: contact info grid. |
| `sections/06-live-github-stats.svg` | Cyberpunk panel: particle-network live stats panel. |
| `scripts/build_snake.py` | Re-styles the raw Platane/snk SVG into the cyberpunk "commit log" board (biggest commits eaten first) \u2192 `dist/github-snake*.svg`. |
| `dist/github-snake.svg`<br>`dist/github-snake-dark.svg` | **Live** GitHub contribution snake — auto-generated daily by the GitHub Action. |
| `.github/workflows/update-snake.yml` | GitHub Action that regenerates the snake SVGs daily. |
| `README.md`<br>`README.template.md` | Profile README (final + template). |
| `build_profile.py` | Generates `light.svg`, `dark.svg`, `README.md` from `profile.json` + templates. |
| `scripts/build_sections.py` | Generates all 6 `sections/*.svg` panels from the data inside the script. |
| `scripts/fix_alignment.py` | Patches the SYSTEM.INFO rows in `light/dark.svg` + templates so all values left-align to the same x-column. Run after every `build_profile.py` rebuild. |

## Build workflow

```bash
# 1. Install Python deps (only needed once)
pip install -r requirements.txt

# 2. Regenerate the main profile cards + README
python build_profile.py

# 3. Fix the SYSTEM.INFO row alignment in the freshly-generated SVGs
python scripts/fix_alignment.py

# 4. Regenerate the 6 cyberpunk section SVGs
python scripts/build_sections.py
```

After any edit to `profile.json` (or to the section data inside `scripts/build_sections.py`), re-run steps 2–4.

## Design decisions

### Palette (current)
- Sections + snake use the owner's cyberpunk palette:
  deep black `#111119`, violet `#8B35FF`, neon pink `#D500F9`,
  electric blue `#00D9FF`, neon yellow `#FFE500`.
- The Matrix terminal header keeps its retro-green look by design (owner's request).
- One accent colour per panel/card, rotating through the palette;
  neon yellow is reserved for the single most important value of a section.

### Row alignment in SYSTEM.INFO
- The original template relied on hand-tuned dot filler counts per row, which left the value column at different x-positions per row (the user reported "7 out of 11 don't start on the same column").
- The patched layout uses explicit `x` attributes on every `<tspan>`:
  - prefix `. ` at x=520
  - red key at x=540
  - dots filler `: ............... ` at x=720 (fixed width)
  - value at x=870 (always the same column)
- The patch is applied by `scripts/fix_alignment.py` and is re-runnable.

### Contribution snake
- The README embeds the **real** contribution snake at `dist/github-snake.svg` (and `-dark.svg`), regenerated daily by `Platane/snk` via `.github/workflows/update-snake.yml`.
- `scripts/build_snake.py` re-styles the raw snake into the cyberpunk commit-log board while keeping the exact snk movement route, played in reverse so the snake eats the BIGGEST commits first.
- The README also pulls live stats from shields.io + streak stats so the numbers are always real.

### Cyberpunk sections
- The 6 panels (`sections/01..06`) use a minimal cyberpunk UI: deep-black canvas, quiet grid,
  thin accent strokes, corner brackets, monospace micro-labels and restrained SMIL animation.
- All data is in `profile.json`; the display-friendly shortened strings live in `scripts/build_sections.py` because the SVG layout has tight horizontal space constraints.

## Privacy
- Phone numbers, birth date, marital status, and military-service details from the source CV are intentionally NOT published in any of the SVG panels. They remain only in the source CV.

## Public profile note
- After pushing to GitHub, visit the **Actions** tab and run the "Sync live contribution snake" workflow once manually. It will then update daily on its own.
