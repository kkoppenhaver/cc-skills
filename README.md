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

### tweet

Write tweets in a distinctive voice mixing playful wonder with pragmatic realism.

**Triggers:** Drafting tweets, creating Twitter threads, or crafting X/Twitter content.

**Features:**
- Voice calibration using existing tweets
- Micro Discovery and Contrast Hack post structures
- Preflight and postflight quality checklists
- Direct posting via `bird` CLI

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
/nano-banana
/tweet
/youtube-producer
```

## Structure

```
skills/
├── frontend-design/
│   └── SKILL.md
├── nano-banana/
│   ├── SKILL.md
│   ├── LICENSE
│   └── README.md
├── tweet/
│   ├── SKILL.md
│   └── references/
│       └── voice-guide.md
└── youtube-producer/
    ├── SKILL.md
    ├── references/
    │   ├── aaron-francis-framework.md
    │   ├── hook-examples.md
    │   ├── mark-rober-framework.md
    │   ├── mrbeast-framework.md
    │   ├── script-templates.md
    │   ├── title-formulas.md
    │   └── veritasium-framework.md
    └── scripts/
        ├── hook_analyzer.py
        ├── shorts_extractor.py
        └── title_generator.py
```

## License

See individual skill directories for license information.
