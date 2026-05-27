# Claude Code Skills

A collection of custom skills for [Claude Code](https://github.com/anthropics/claude-code) that extend its capabilities with specialized workflows for content, marketing, social media, video, images, and design.

Skills are invoked automatically when Claude detects a relevant request, or explicitly via a slash command (e.g. `/tweet`, `/nano-banana`).

## Skills

### Copywriting & Content

| Skill | What it does |
|-------|--------------|
| **copywriting** | Write, rewrite, or improve marketing copy for any page — homepage, landing, pricing, feature, about, or product pages. Headlines, CTAs, value props, taglines, hero sections. |
| **copy-editing** | Edit, review, and polish *existing* copy rather than writing from scratch — tighten, proofread, sharpen messaging, fix awkward phrasing. |
| **content-strategy** | Plan a content strategy — what to write about, topic clusters, content pillars, editorial calendars, blog roadmaps. |
| **fact-check** | Audit a published article or URL for factual accuracy: extract claims, research each against current sources, and generate an accuracy report. Can apply corrections to local files or via MCP (WordPress, Google Docs). |

### Social Media & Voice

| Skill | What it does |
|-------|--------------|
| **tweet** | Write tweets and threads in Keanan's voice — punchy, first-person, mixing playful wonder with pragmatic realism. Includes Typefully scheduling. |
| **linkedin** | Write LinkedIn posts in Keanan's voice — upbeat, builder-centric, practical how-tos with candid humor. Includes Typefully scheduling. |
| **social-content** | Create, schedule, or optimize social content across platforms (LinkedIn, X, Instagram, TikTok, Facebook). Content calendars, repurposing, engagement strategy. |

### Marketing & Growth

| Skill | What it does |
|-------|--------------|
| **marketing-ideas** | Brainstorm marketing, growth, and promotion strategies for a SaaS or software product. A starting point when you're stuck or looking for inspiration. |
| **cold-email** | Write B2B cold outreach and multi-touch follow-up sequences that get replies — subject lines, openers, body copy, CTAs, personalization. |
| **lead-magnets** | Plan and optimize lead magnets for email capture — ebooks, checklists, templates, content upgrades, opt-ins. |
| **free-tool-strategy** | Plan, evaluate, or build a free tool as marketing (engineering as marketing) — calculators, generators, graders, audit tools for lead gen and links. |
| **kit-broadcast** | Create and schedule email broadcasts in Kit (ConvertKit) for new blog posts on Claude Code for Marketers. |

### Video (HyperFrames)

| Skill | What it does |
|-------|--------------|
| **hyperframes** | Author HTML-based video compositions — animations, title cards, overlays, captions/subtitles, voiceovers, audio-reactive visuals, and scene transitions. |
| **hyperframes-cli** | Use the HyperFrames CLI — init, lint, preview, render, transcribe, tts, doctor, and more. |
| **hyperframes-registry** | Install and wire registry blocks and components into HyperFrames compositions (`hyperframes add`). |
| **website-to-hyperframes** | Capture a website from a URL and turn it into a HyperFrames video — social ads, product tours, promos. |
| **gsap** | GSAP animation reference for HyperFrames — tweens, easing, stagger, timelines, and performance patterns. |
| **youtube-producer** | Turn vague video ideas into developed YouTube concepts — viral titles, hooks, outlines, and promotional shorts. Uses Mark Rober and Aaron Francis frameworks. |

### Images & Design

| Skill | What it does |
|-------|--------------|
| **nano-banana** | Generate and edit images using Nano Banana (Gemini CLI) — featured images, thumbnails, icons, diagrams, patterns, illustrations, photos. Required for all image generation. |
| **featured-image** | Generate branded blog/social featured images by authoring an HTML card and rendering it to PNG with headless Chromium ("HTML first, then to PNG"). |
| **frontend-design** | Build distinctive, production-grade frontend interfaces — components, pages, dashboards, layouts — that avoid generic AI aesthetics. |

### Meta & Utility

| Skill | What it does |
|-------|--------------|
| **skill-creator** | Guidance for creating and updating skills — structure, SKILL.md authoring, and best practices. |
| **ai-fluency** | Analyze past Claude Code conversations to measure AI fluency against Anthropic's 4D framework (Delegation, Description, Discernment, Diligence). |

## Installation

Skills in this directory are automatically available to Claude Code. Each skill lives in its own subdirectory with a `SKILL.md` file defining its name, description, and instructions. Several skills here are symlinks into a shared `.agents/skills` library.

## Configuration

Some skills require API keys or credentials. Add these to your Claude Code settings file at `~/.claude/settings.json`:

```json
{
  "env": {
    "GEMINI_API_KEY": "your-gemini-api-key",
    "TYPEFULLY_API_KEY": "your-typefully-api-key",
    "TYPEFULLY_SOCIAL_SET_ID": "your-social-set-id"
  }
}
```

| Variable | Used by | Where to get it |
|----------|---------|-----------------|
| `GEMINI_API_KEY` | nano-banana | [Google AI Studio](https://aistudio.google.com/apikey) |
| `TYPEFULLY_API_KEY` | tweet, linkedin | Typefully → Settings → API & Integrations |
| `TYPEFULLY_SOCIAL_SET_ID` | tweet, linkedin | `python tweet/scripts/typefully_scheduler.py --list-social-sets` |
| `KIT_API_KEY` | kit-broadcast | Kit (ConvertKit) → Settings → Advanced → API |

**Other requirements:**
- **tweet** — `bird` CLI for research and voice calibration
- **featured-image** / **fact-check** — headless Chromium / web access for rendering and research
- **hyperframes** — the HyperFrames CLI (see the `hyperframes-cli` skill)

## License

See individual skill directories for license information.
