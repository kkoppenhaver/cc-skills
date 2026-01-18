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
3. Draft the tweet following the voice guide in `references/voice-guide.md`
4. Run through preflight/postflight checklists
5. Present draft to user for approval
6. If approved:
   - Post immediately: `bird tweet "<text>"`
   - Schedule for later: `python scripts/typefully_scheduler.py`

## Tools

### bird CLI (immediate posting)

- Search tweets: `bird search "from:kkoppenhaver" -n 10`
- Read a tweet: `bird read <tweet-id-or-url>`
- Post a tweet: `bird tweet "<text>"`
- Post with media: `bird tweet "<text>" --media <path>`

### Typefully Scheduler (scheduling)

Use `scripts/typefully_scheduler.py` to schedule tweets via Typefully API.

**Setup:** Add to `~/.claude/settings.json`:
```json
{
  "env": {
    "TYPEFULLY_API_KEY": "your-api-key",
    "TYPEFULLY_SOCIAL_SET_ID": "your-social-set-id"
  }
}
```

Get your API key from Typefully Settings > API & Integrations. To find your social set ID, run: `python scripts/typefully_scheduler.py --list-social-sets`

**Usage:**
- Schedule a tweet: `python scripts/typefully_scheduler.py`
- List social sets: `python scripts/typefully_scheduler.py --list-social-sets`

**Scheduling options:**
- Next free slot (Typefully auto-schedules)
- Publish immediately
- Specific date/time (ISO 8601 format)

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