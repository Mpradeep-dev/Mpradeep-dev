# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

GitHub **profile README** repo (`Mpradeep-dev/Mpradeep-dev`). The repo name matches the
username, so `README.md` renders on the user's GitHub profile page. There is no application,
no build, no tests, no package manager — the only "deliverables" are `README.md` and the
GitHub Actions workflow.

## Structure

- `README.md` — the profile page. Markdown + inline HTML (`<p align>`, `<img>`, `<picture>`,
  one `<table>`). Restrained dark-tech layout: hand-designed SVG header, one teal accent
  (`#34d3c1` dark / `#0d9488` light) locked across the page, uniform `flat-square` chips on
  a single `#0d1117` background (brand colour lives only in the logo glyph).
- `assets/header-dark.svg`, `assets/header-light.svg` — hand-authored header banner
  (name, eyebrow, accent rule, aperture motif). Referenced by relative path via `<picture>`
  with `prefers-color-scheme`. Static SVG only — no `<script>`, no SMIL animation (GitHub
  strips both). **All text is outlined to `<path>` (no `<text>`, no font dependency)** so it
  renders identically on every machine. To re-edit the wording, regenerate from
  `scratchpad/text2path.py` + `build_svg.py` (fontTools + local Segoe UI: `segoeuib.ttf`
  bold for the name, `seguisb.ttf` semibold for the eyebrow, `segoeui.ttf` for the sub),
  then re-run the well-formed-XML + BoundsPen checks.
- External image services still used, kept on the locked palette (`bg 0d1117`,
  `accent 34d3c1`, `text 8b98a5`, `title 34d3c1`, `border 1b2430` — never `tokyonight`):
  - `img.shields.io` — tech-stack + contact chips (`style=flat-square`)
  - `github-readme-stats.vercel.app` — stats card, top-langs, and the "Featured projects" pins
  - `streak-stats.demolab.com` — contribution streak (current domain; the old
    `github-readme-streak-stats.herokuapp.com` is deprecated)
  - `github-readme-activity-graph.vercel.app` — contribution activity graph
  - `raw.githubusercontent.com/.../output/*.svg` — the contribution snake (see below)
  - `images.credly.com` / `learn.microsoft.com` — real credential badge art in the table
- Deliberately removed (AI/template tells): `capsule-render` waving banners, `komarev`
  view counter, `for-the-badge` rainbow badge wall, emoji-per-heading. Do not reintroduce.
  Third-party widgets are recoloured to the locked palette, not left on their stock themes.
- `.github/workflows/blank.yml` — daily cron that regenerates the contribution snake animation.

## Contribution snake animation (the one piece of automation)

`.github/workflows/blank.yml` runs daily (`cron: "0 0 * * *"`) and on manual dispatch:
1. `platane/snk@v3` generates light + dark snake SVGs into `dist/`.
2. `crazy-max/ghaction-github-pages@v4` force-pushes `dist/` to the **`output`** branch.

The `<picture>` block at the end of the "Activity" section references those SVGs from the
`output` branch (`.../Mpradeep-dev/output/github-contribution-grid-snake.svg`). Key coupling:

- The token env var is `GITHUB_TOKEN: ${{ secrets.GITHUBTOKEN }}` — the secret name is
  `GITHUBTOKEN` (no underscore), not the default `GITHUB_TOKEN`. Don't "correct" it without
  confirming the repo secret name.
- The job needs `permissions: contents: write` to push the `output` branch — keep it.
- The `github_user_name` in the workflow and the SVG URLs in `README.md` must both stay
  `Mpradeep-dev`. Changing one without the other breaks the rendered snake.

## Working in this repo

- Editing `README.md` is the main task. Match the current pattern: `## Title` headings with
  no emoji, centered `<p align>` blocks for the header/links/widgets, left-aligned prose for
  "What I build", uniform `flat-square` chips grouped under bold labels. Section order:
  header, links, What I build, Stack, Featured projects, Activity, Verified badges, footer.
- To preview, push to a branch and view on GitHub — `shields.io` and the snake SVG only
  render on github.com, not in a local Markdown preview. The `assets/*.svg` header does
  render locally.
- When editing `assets/*.svg`: keep the light and dark files in visual lockstep (same
  geometry, swapped palette), keep them static, and keep both accent hexes as the only
  non-neutral colour.
- Identity/links that recur and must stay consistent: GitHub `Mpradeep-dev`, LinkedIn
  `in/mpradeep-dev`, email `pradeepmurugesan.dev@gmail.com`, portfolio `pradeepmurugesan.dev`.
