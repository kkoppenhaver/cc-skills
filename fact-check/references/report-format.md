# Report Format

Use this template when assembling the fact-check report. Present it in the conversation.

## Template

```markdown
# Fact-Check Report

**Article**: [title]
**URL**: [url]
**Checked**: [today's date]
**Claims analyzed**: [total count]

## Summary

- X claims need updating
- Y claims verified as accurate
- Z new developments worth adding
- W items to consider removing

---

## Needs Update

### 1. [Short description]

> **Original claim**: "[exact quote from article]"

**What changed**: [explanation]
**Current information**: [what is true now]
**Confidence**: High / Medium / Low
**Source**: [URL]

---

## New Information to Add

### 1. [What new information exists]

**Relevance**: [why this matters to the article's thesis]
**Details**: [the new information]
**Confidence**: High / Medium / Low
**Source**: [URL]

---

## Consider Removing

### 1. [What to consider removing]

**Reason**: [deprecated, misleading, no longer relevant]
**Confidence**: High / Medium / Low
**Source**: [URL]

---

## Still Accurate

Brief format — just confirm and cite.

1. "[claim text]" — Confirmed. Source: [URL]
2. "[claim text]" — Confirmed. Source: [URL]
```

## Formatting Rules

- **Needs Update** comes first — it is the primary reason someone runs this skill
- **Still Accurate** comes last in abbreviated format — no need to explain what has not changed
- Sort items within each section by confidence (high first)
- Always include the exact original quote so the user can find it in their article
- Every finding must have at least one source URL
- For "Cannot Verify" items, include them in "Needs Update" with a note explaining why verification failed and suggest the user check manually
