# Final profile setup

This project is already personalized for **Parsa Taheri**.

## Editable data
- `profile.json` contains the profile/resume summary and social identifiers.
- `profile.jpg` is the source portrait.
- `templates/light.template.svg` and `templates/dark.template.svg` contain the layout and hacker palette.

## Rebuild after any change
```bash
pip install -r requirements.txt
python build_profile.py
```

The build regenerates `light.svg`, `dark.svg`, and `README.md`.

## Current palette logic
- The old purple/indigo accents were converted to hacker green.
- The old blue/cyan accents were converted to red.
- Neutral text/background colors and the original green/accent colors were left unchanged.

## Resume summary used
The card intentionally keeps only GitHub-relevant information: role, current work, education, focus areas, major stack, and public professional/social contacts. Personal details such as birth date, marital status, military status, and phone numbers are intentionally omitted from the public GitHub card.

## GitHub Actions
The heatmap workflow is installed at `.github/workflows/jet-heatmap.yml`. On the first push, run it manually once from the GitHub **Actions** tab. After that, it updates daily.

## Public profile note
Phone numbers, birth date, marital status and military-status details from the CV are not published in the card. They are unnecessary for a public GitHub profile and remain only in the source CV you provided.
