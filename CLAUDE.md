# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

GitHub **profile README** repo (`Mpradeep-dev/Mpradeep-dev`). The repo name matches the
username, so `README.md` renders on the user's GitHub profile page. There is no application,
no build, no tests, no package manager — the only "deliverables" are `README.md` and the
GitHub Actions workflow.

## Structure

- `README.md` — the profile page. Pure Markdown + inline HTML (`<p align>`, `<img>`,
  `<picture>`). Visuals come from external services rendered via image URLs:
  - `capsule-render.vercel.app` — animated waving header banner
  - `img.shields.io` / `img.icons8.com` / `devicon` / `simple-icons` / `vectorlogo.zone` — tech-stack badges & icons
  - `komarev.com/ghpvc` — profile view counter
  - `github-readme-streak-stats.herokuapp.com` — contribution streak card
  - `cultofthepartyparrot.com` — party-parrot GIF strip
- `.github/workflows/blank.yml` — daily cron that regenerates the contribution snake animation.

## Contribution snake animation (the one piece of automation)

`.github/workflows/blank.yml` runs daily (`cron: "0 0 * * *"`) and on manual dispatch:
1. `platane/snk@v3` generates light + dark snake SVGs into `dist/`.
2. `crazy-max/ghaction-github-pages@v4` force-pushes `dist/` to the **`output`** branch.

The `<picture>` block near the bottom of `README.md` references those SVGs from the `output`
branch (`.../Mpradeep-dev/output/github-contribution-grid-snake.svg`). Key coupling to respect:

- The token env var is `GITHUB_TOKEN: ${{ secrets.GITHUBTOKEN }}` — the secret name is
  `GITHUBTOKEN` (no underscore), not the default `GITHUB_TOKEN`. Don't "correct" it without
  confirming the repo secret name.
- The job needs `permissions: contents: write` to push the `output` branch — keep it.
- The `github_user_name` in the workflow and the SVG URLs in `README.md` must both stay
  `Mpradeep-dev`. Changing one without the other breaks the rendered snake.

## Working in this repo

- Editing `README.md` is the main task. Match the existing pattern: centered `<p align>`
  blocks, sectioned by `## emoji Title` headings separated by `---`, icons as `<img height="45">`.
- To preview, push to a branch and view on GitHub — most image services only render on
  github.com, not in a local Markdown preview.
- Identity/links that recur and must stay consistent: GitHub `Mpradeep-dev`, profile-views
  username `mpradeep2005`, LinkedIn `in/mpradeep-dev`, email `pradeepmurugesan.dev@gmail.com`.
