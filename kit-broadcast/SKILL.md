---
name: kit-broadcast
description: Create and schedule email broadcasts in Kit (ConvertKit) for new blog posts on Claude Code for Marketers. Use when: (1) announcing a new blog post via email, (2) scheduling a Kit broadcast, (3) creating newsletter content for claudecodeformarketers.com posts. Triggers include "send email about this post", "schedule broadcast", "announce this post", "kit broadcast", "email newsletter".
---

# Kit Broadcast Skill

Create and schedule email broadcasts for new blog posts.

## Workflow

1. **Read the blog post** from `src/content/blog/{slug}.md`
2. **Extract key information**:
   - Title from frontmatter
   - 3-4 key points from the content
   - Build post URL: `https://claudecodeformarketers.com/blog/{slug}`
3. **Generate email copy** following the template in `references/email-template.md`
4. **Present the email to user** for review (subject + HTML content)
5. **Ask for schedule time** in ISO8601 format (e.g., `2026-01-20T10:00:00-06:00`)
6. **Create broadcast** using `scripts/kit_broadcast.py`

## Script usage

```bash
# Load API key from .env in project root
source /Users/keanan/code/claude-code-for-marketers/.env && export KIT_API_KEY

# Dry run (test without sending)
python scripts/kit_broadcast.py \
  --subject "[CC4M] Post Title" \
  --content "<p>HTML content here</p>" \
  --send-at "2026-01-20T10:00:00-06:00" \
  --dry-run

# Create scheduled broadcast
python scripts/kit_broadcast.py \
  --subject "[CC4M] Post Title" \
  --content "<p>HTML content here</p>" \
  --send-at "2026-01-20T10:00:00-06:00"
```

## Timezone

User is in US Central time. When they say "10am tomorrow", convert to ISO8601 with `-06:00` offset (CST) or `-05:00` (CDT during daylight saving).

## Subscriber targeting

Broadcasts are automatically filtered to subscribers with the "CC4M" tag (ID: 14154457). This is hardcoded in the script.

## After scheduling

Report back:
- Broadcast ID from API response
- Scheduled send time
- Audience: CC4M tag subscribers
- Suggest user verify in Kit dashboard at https://app.kit.com/broadcasts
