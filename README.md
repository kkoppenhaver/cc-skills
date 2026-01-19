# Claude Code Skills

A collection of custom skills for [Claude Code](https://github.com/anthropics/claude-code) that extend its capabilities with specialized workflows for content creation, design, and image generation.

## Skills

### frontend-design

Create distinctive, production-grade frontend interfaces with high design quality. Generates creative, polished code that avoids generic AI aesthetics.

**Triggers:** Building web components, pages, applications, dashboards, React components, HTML/CSS layouts, or any web UI styling.

**Features:**
- Bold aesthetic direction with intentional design choices
- Typography, color, motion, and spatial composition guidance
- Production-grade, functional code output

### nano-banana

Generate and edit images using the Gemini CLI's nanobanana extension.

**Triggers:** Any request to create, generate, draw, design, or edit images, graphics, illustrations, thumbnails, icons, diagrams, or visual content.

**Commands:**
- `/generate` - Text-to-image generation
- `/edit` - Modify existing images
- `/restore` - Repair damaged photos
- `/icon` - App icons and UI elements
- `/diagram` - Flowcharts and architecture diagrams
- `/pattern` - Seamless textures and patterns

**Requirements:** Gemini CLI with nanobanana extension installed, `GEMINI_API_KEY` environment variable set.

### linkedin

Write LinkedIn posts in an upbeat, builder-centric voice mixing practical how-tos with candid humor.

**Triggers:** Drafting LinkedIn content, creating professional posts, or sharing builder-focused insights.

**Features:**
- Quick Hack/Tip and Process Mini-Guide structures
- Before/after contrast framing
- Preflight and postflight quality checklists
- Post scheduling via Typefully API

**Scripts:**
- `scripts/typefully_scheduler.py` - Schedule LinkedIn posts via Typefully

**Requirements:** See [Configuration](#configuration) for Typefully setup.

### tweet

Write tweets in a distinctive voice mixing playful wonder with pragmatic realism.

**Triggers:** Drafting tweets, creating Twitter threads, or crafting X/Twitter content.

**Features:**
- Voice calibration using existing tweets
- Micro Discovery and Contrast Hack post structures
- Preflight and postflight quality checklists
- Tweet scheduling via Typefully API

**Scripts:**
- `scripts/typefully_scheduler.py` - Schedule tweets via Typefully

**Requirements:** `bird` CLI for research/voice calibration. See [Configuration](#configuration) for Typefully setup.

### youtube-producer

Transform vague video ideas into fully developed YouTube content with viral titles, compelling hooks, structured outlines, and promotional shorts.

**Triggers:** Brainstorming video ideas, developing concepts, creating titles/thumbnails, writing scripts, or planning shorts.

**Features:**
- Mark Rober's "Hiding the Vegetables" framework
- Aaron Francis's "Nugget + Packaging" approach
- 30-second hook structure templates
- Three-act video structure guidance
- YouTube Shorts extraction
- Title generation with proven formulas
- Thumbnail design principles

**Scripts:**
- `scripts/title_generator.py` - Generate titles with scoring
- `scripts/hook_analyzer.py` - Evaluate hook effectiveness
- `scripts/shorts_extractor.py` - Extract shorts from outlines

## Installation

Skills in this directory are automatically available to Claude Code. Place each skill in its own subdirectory with a `SKILL.md` file defining the skill's name, description, and instructions.

## Usage

Skills are invoked automatically when Claude Code detects relevant requests, or explicitly via slash commands:

```
/frontend-design
/linkedin
/nano-banana
/tweet
/youtube-producer
```

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

### Getting Credentials

**Gemini API Key** (nano-banana):
- Get from [Google AI Studio](https://aistudio.google.com/apikey)

**Typefully API Key** (tweet/LinkedIn scheduling):
- Get from Typefully Settings > API & Integrations

**Typefully Social Set ID** (tweet/LinkedIn scheduling):
- Run `python ~/.claude/skills/tweet/scripts/typefully_scheduler.py --list-social-sets` to find your ID
- Run `python ~/.claude/skills/tweet/scripts/typefully_scheduler.py --details` to see connected platforms

## License

See individual skill directories for license information.
