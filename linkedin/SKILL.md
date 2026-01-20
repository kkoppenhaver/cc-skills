---
name: linkedin
description: Write LinkedIn posts in Keanan's voice. Use when drafting LinkedIn content, creating professional posts, or sharing builder-focused insights. Triggers include requests to "write a LinkedIn post", "draft something for LinkedIn", "help me post on LinkedIn", or any LinkedIn content creation. Generates upbeat, builder-centric content mixing practical how-tos with candid humor.
---

# LinkedIn Post Writer

Write LinkedIn posts in Keanan's distinctive voice: upbeat, builder-centric, mixing practical how-tos with candid, self-deprecating humor.

## Voice Summary

**Primary emotions:** capability, curiosity, momentum
**Secondary notes:** playful warmth, inclusion, low-ego confidence
**Reader should feel:** "I can try this right now, and it'll probably work. Also, this is fun and I'm not alone."

Write like a hands-on practitioner sharing a fresh discovery: conversational, concise, and generous with specifics. Keep the focus on what you did, how you did it, and how the reader can do it.

## Scheduling Context

**Important:** Before scheduling, check today's date from the system context (provided in the env section). Use this to correctly map day names to calendar dates (e.g., if today is Tuesday Jan 20, then "Wednesday" = Jan 21, not Jan 22).

## Workflow

1. Ask what the user wants to post about (if not already clear)
2. Check currently scheduled posts: `python3 scripts/typefully_scheduler.py --list-scheduled`
3. Draft the post following the voice guide in `references/voice-guide.md`
4. Run through preflight/postflight checklists
5. Present draft to user for approval
6. If approved, write to temp file and schedule via Typefully

## Tools

### Typefully Scheduler

Use `scripts/typefully_scheduler.py` to schedule LinkedIn posts via Typefully API. The script is designed for automation (no interactive prompts).

**Setup:** Add to `~/.claude/settings.json`:
```json
{
  "env": {
    "TYPEFULLY_API_KEY": "your-api-key",
    "TYPEFULLY_SOCIAL_SET_ID": "your-social-set-id"
  }
}
```

Get your API key from Typefully Settings > API & Integrations. To find your social set ID, run: `python3 scripts/typefully_scheduler.py --list-social-sets`

**Usage:**
```bash
# Check what's already scheduled (do this first to avoid conflicts)
python3 scripts/typefully_scheduler.py --list-scheduled

# Schedule a post from a file
python3 scripts/typefully_scheduler.py --file /tmp/linkedin-post.txt --schedule next-free-slot

# Schedule for a specific time (ISO 8601 format)
python3 scripts/typefully_scheduler.py --file /tmp/linkedin-post.txt --schedule 2026-01-20T18:00:00Z

# Publish immediately
python3 scripts/typefully_scheduler.py --file /tmp/linkedin-post.txt --schedule now

# List social sets
python3 scripts/typefully_scheduler.py --list-social-sets

# View connected platforms
python3 scripts/typefully_scheduler.py --details
```

**Scheduling workflow:**
1. Write post content to a temp file (e.g., `/tmp/linkedin-post.txt`)
2. Run the scheduler with `--file` and `--schedule` flags
3. The script will show existing scheduled posts before scheduling

**Note:** Posts about the same topic can go out on Twitter and LinkedIn at the same time - that's fine. Just avoid scheduling unrelated posts at conflicting times.

## Quick Reference

### Structure Blueprints

**Quick Hack/Tip:**
1. Hook - name the friction in one line
2. Contrast - old vs. new in two short blocks
3. Steps - 1-3 lines with prompt/command to replicate
4. Payoff - what changed: time saved, result
5. CTA - soft invite to try or respond

**Process Mini-Guide:**
1. Goal statement - what you wanted to achieve
2. Toolchain overview - who/what you used
3. Stepwise narrative - chronology with 3-6 concise beats
4. Outcome and metrics - what you got; any artifacts
5. Reflection - what you'd improve (light self-deprecation)
6. Resources + CTA - links, repo, "reply if..."

### Syntax Constraints

- Sentence length: 8-18 words average; 10-20% very short punchlines (2-6 words)
- Paragraphs: 1-3 sentences; use blank lines between sections
- Exclamation points: 1-2 per 120 words
- Questions: up to 2 per 120 words
- Emojis: 0-2 per post; expressive, context-aligned
- Quotes/code: use for prompts and commands; single lines
- **Banned hedges:** "maybe," "kinda," "sort of," "I think," "probably"
- **Avoid:** "leverage," "utilize," "optimize" (vague), "solution," "content," "efficiency"

### Preflight Checklist

- [ ] One clear friction or goal in line one
- [ ] Chose contrast OR stepwise narrative (not both)
- [ ] At least two concrete specifics (tool names, commands, files)
- [ ] Quantified effort or outcome with at least one number
- [ ] Single, light human moment (aside, wink, or emoji)
- [ ] Prompt/command is copy-ready and short
- [ ] Paragraphs ≤3 sentences and mostly under 18 words
- [ ] Exactly one soft CTA aligned to the content
- [ ] Avoided hedges and corporate filler
- [ ] Links present only where helpful and labeled clearly

### Postflight Checklist

- [ ] Hook lands in first sentence (names the friction)
- [ ] Can skim and see the win (before/after block if needed)
- [ ] ≥2 proper nouns and ≥1 numeral
- [ ] At least one prompt/command/link for actionability
- [ ] One playful beat max
- [ ] Average sentence length 8-18 words
- [ ] Emojis/exclamations ≤2 each
- [ ] CTA present and optional (not pushy)
- [ ] Artifact mentioned (repo/file/transcript)
- [ ] Fresh phrasing (no recycled/templated lines)

## Detailed Voice Guide

For emotional mechanics, lexicon, and rewrite operators, see `references/voice-guide.md`.
