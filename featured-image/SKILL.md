---
name: featured-image
description: Generate branded blog/social featured images by authoring an HTML "card" and rendering it to a PNG with headless Chromium ("HTML first, then to PNG"). Use when the user wants a featured image, hero/header image, OG or social card, or any branded post graphic for a content project. Handles one-time per-project brand setup (colors, fonts, dimensions), then composing and rendering per-post images. Triggers include "make a featured image", "create a blog header/social card", "og image", "render this to PNG for the post", or branded post graphics for a repo's blog.
---

# Featured Image

Author a 1280×720 HTML card, render it to a 2× PNG with headless Chromium. HTML-first gives full layout control and pixel-perfect brand fidelity; the PNG is the deliverable the user uploads.

## Workflow

1. **Locate the project's image directory.** Default `infographics/` at the repo root. Confirm or detect it.

2. **Check whether the project is configured.** Configured = the image dir contains `export.mjs`, `featured-image.json`, and a `brand-template.html`.
   - If **not** configured → follow `references/setup.md` to set it up. Do this once per project, then continue.

3. **Compose the post's card.** Copy `brand-template.html` to `<post-slug>-featured.html` in the image dir, then edit:
   - **Headline** — short, fits two lines.
   - **Subhead** — optional, one line.
   - **Visual** — one supporting graphic that illustrates the post's core idea. Replace the template's example visual.
   - Put the brand accent color on the **one** key phrase only.

4. **Render.** From the image dir: `node export.mjs <post-slug>-featured` → writes `<post-slug>-featured.png` at 2× (1280×720 → 2560×1440).

5. **Review and deliver.** Read the PNG to confirm fonts loaded and the layout reads cleanly; re-render after tweaks. Give the user the PNG path. If they'll upload it by hand, copy it to `~/Desktop`.

## Design

- Headline ≤ ~8 words, two lines max — the image is glanced at, not read.
- One accent color, on one key phrase. Everything else in the primary text color.
- One visual metaphor (a before/after pair, a single UI mock, an icon trio). Don't crowd it.
- 1280×720 (16:9) by default. Dimensions live in the template CSS, not the script.
- Generous margins; clear hierarchy (large headline, small uppercase label).

## Notes

- Rendering needs Playwright's Chromium. Setup installs it in the image dir (`node_modules` is gitignored; the browser binary is cached globally and reused across projects).
- **WordPress:** the MCP/abilities plugin cannot upload media. Featured images and in-body screenshots are added manually in the editor — deliver the PNG path, don't try to push it through the API.

See `references/setup.md` for one-time per-project brand configuration.
