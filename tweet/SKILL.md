---
name: tweet
description: Write tweets in Keanan's voice. Use when drafting tweets, creating Twitter threads, or crafting social media content for X/Twitter. Triggers include requests to "write a tweet", "draft a post for X", "help me tweet about", or any Twitter/X content creation. Generates punchy, first-person content mixing playful wonder with pragmatic realism.
---

# Tweet Writer

Write tweets in Keanan's distinctive voice: casual, tool-savvy, mixing playful wonder with pragmatic realism.

## Voice Summary

**Primary emotions:** energized curiosity, playful delight, practical confidence  
**Secondary notes:** humility, camaraderie, cautious realism  
**Reader should feel:** "This is within reach, and a little bit magical. I'm not alone, and there's a clear next step."

Write like a curious practitioner sharing live findings: immediate, specific, and grounded in hands-on experience.

## Workflow

1. Ask what the user wants to tweet about (if not already clear)
2. Optionally examine recent tweets for voice calibration: `bird search "from:kkoppenhaver" -n 5`
3. Check currently scheduled posts: `python3 scripts/typefully_scheduler.py --list-scheduled`
4. Draft the tweet following the voice guide in `references/voice-guide.md`
5. Run through preflight/postflight checklists
6. Present draft to user for approval
7. If approved, write to temp file and schedule via Typefully

## Tools

### bird CLI (read-only)

Use for research and voice calibration only. Do not use for posting.

- Search tweets: `bird search "from:kkoppenhaver" -n 10`
- Read a tweet: `bird read <tweet-id-or-url>`

### Typefully Scheduler (scheduling)

Use `scripts/typefully_scheduler.py` to schedule tweets via Typefully API. The script is designed for automation (no interactive prompts).

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

# Schedule a tweet from a file
python3 scripts/typefully_scheduler.py --file /tmp/tweet.txt --schedule next-free-slot

# Schedule for a specific time (ISO 8601 format)
python3 scripts/typefully_scheduler.py --file /tmp/tweet.txt --schedule 2026-01-20T18:00:00Z

# Publish immediately
python3 scripts/typefully_scheduler.py --file /tmp/tweet.txt --schedule now

# List social sets
python3 scripts/typefully_scheduler.py --list-social-sets

# View connected platforms
python3 scripts/typefully_scheduler.py --details
```

**Scheduling workflow:**
1. Write tweet content to a temp file (e.g., `/tmp/tweet.txt`)
2. Run the scheduler with `--file` and `--schedule` flags
3. The script will show existing scheduled posts before scheduling

**Note:** Posts about the same topic can go out on Twitter and LinkedIn at the same time - that's fine. Just avoid scheduling unrelated posts at conflicting times.

## Quick Reference

### Structure Blueprints

**Micro Discovery Post:**
1. Hook (spark) - one-line setup with ellipses or short exclamation
2. Context (1-2 lines) - minimal specifics: tools, files, goal
3. Reveal/Result - concise verdict with one emoji
4. Nudge - actionable suggestion in second person
5. Caveat - quick realism note

**Contrast Hack Post:**
1. Frame - "Old pattern" pain in concrete details
2. Flip - "New pattern" with imperative nudge
3. Proof touch - tiny outcome or timing delta
4. Button - micro-CTA or emoji beat

### Syntax Constraints

- Sentence length: 5-15 words average; include 1-2 ultra-short bursts (3-5 words)
- Paragraphs: 1-2 lines each with frequent line breaks
- Ellipses: 0-2 per tweet
- Exclamation marks: ≤1
- Questions: 0-2 per tweet
- Emojis: 0-2 per tweet at line ends
- **Banned:** emoji chains, over-hedging, corporate jargon, passive voice clusters

### Preflight Checklist

- [ ] One core insight or win clearly defined
- [ ] At least one concrete tool/file/outcome
- [ ] Contrast or reveal beat present
- [ ] One candid caveat or edge case
- [ ] Single emoji punctuating key moment
- [ ] Sentences mostly 5-15 words with a 3-5 word punch
- [ ] Direct, testable CTA in second person (if applicable)
- [ ] Light warmth without undercutting the result

### Postflight Checklist

- [ ] No sentence >22 words
- [ ] Emojis ≤2
- [ ] Ellipses ≤2
- [ ] One caveat included
- [ ] Read-aloud rhythm is snappy
- [ ] Tone: confident but curious, not boastful

## Detailed Voice Guide

For emotional mechanics, lexicon, and example patterns, see `references/voice-guide.md`.