---
name: fact-check
description: >
  Audit a published article or blog post for factual accuracy by extracting
  verifiable claims, researching each against current sources, and generating
  a detailed accuracy report. Use when the user wants to "fact-check," "verify,"
  "audit," or "review" an article, blog post, or web page for accuracy. Also
  use when the user mentions "outdated information," "is this still accurate,"
  "check if this is still true," "content freshness," "stale content," "update
  my article," or provides a URL and asks to verify the claims or facts in it.
  Works with any public URL. Can help apply corrections to local source files
  or via MCP integrations (WordPress, Google Docs, etc.).
---

# Fact-Check

Audit a published article for factual accuracy. Fetch the article, extract verifiable claims, research each claim against current sources in parallel, and generate a detailed report with confidence levels and citations.

## Workflow

1. Fetch the article and extract claims
2. Present claims to user for confirmation
3. Research claim groups in parallel
4. Generate and present the accuracy report
5. Optionally help make corrections

## Step 1: Fetch and extract claims

Ask the user for a URL if not already provided.

1. Use WebFetch to retrieve the full article content
2. If WebFetch fails (site blocks automated requests), ask the user to paste the article content directly
3. Read the article and identify every verifiable claim. A "claim" is any statement that could be confirmed or refuted with external evidence. See [references/claim-categories.md](references/claim-categories.md) for the full taxonomy
4. For each claim, record:
   - The exact quote or close paraphrase from the article
   - A category (Pricing, Features, Dates, Architecture, etc.)
   - Whether it is a **hard fact** (definitively true or false) or a **soft claim** (subjective, directional, or context-dependent)
5. Group related claims together:
   - All claims about the same product/tool/service → one group
   - All pricing claims → one group (even across products for comparison articles)
   - All date/timeline claims → one group
   - General industry or statistical claims → one group

## Step 2: Confirm claims with user

Present the extracted claims as a numbered list organized by group. Example format:

```
## Claude Cowork (7 claims)
1. [Hard] "Cowork launched in January 2026" (Date)
2. [Hard] "runs inside a sandboxed virtual machine" (Architecture)
3. [Soft] "easier on day one" (Comparison)
...

## Pricing (3 claims)
8. [Hard] "Pro ($20/month)" (Pricing)
...
```

Ask: "Do these look right? Any claims to add, remove, or skip?"

Wait for confirmation before proceeding. The user may want to exclude claims they know are fine or add ones that were missed.

## Step 3: Research claims in parallel

For each claim group, spawn a research agent using the Agent tool. Launch all agents in a single message so they run concurrently.

Each agent's prompt must include:

1. **The claims to verify** — copy the exact claims from the extraction
2. **Article context** — what the article is about, approximate publish date if detectable
3. **Source priority instructions:**
   - For product/tool claims: start with the product's official website, documentation, changelog, and pricing page. Use WebFetch on official URLs first, then WebSearch for recent changes
   - For comparison claims: check both products' current state
   - For statistical/data claims: find the original cited source or the most authoritative current source
   - For date/event claims: search for the specific event or milestone
   - For architectural/technical claims: check official documentation and recent technical posts
4. **Required output format:**

```
## [Claim Group Name]

### Claim: "[exact text]"
- **Status**: Accurate / Needs Update / Cannot Verify
- **Confidence**: High / Medium / Low
- **Current Information**: [what is true now]
- **Source**: [URL]
- **Notes**: [context, e.g., "changed as of July 2025"]
```

5. **Instructions to mark "Cannot Verify"** rather than guessing when sources are ambiguous or unavailable

### Managing scope

For articles with many claim groups (6+), suggest limiting research to the 4-5 highest-priority groups. Prioritize hard facts over soft claims. Ask the user which groups matter most.

## Step 4: Generate report

After all research agents return:

1. Aggregate findings into the report format defined in [references/report-format.md](references/report-format.md)
2. Organize into four categories:
   - **Needs Update** — claim is no longer accurate (include what changed and the correct current information)
   - **New Information to Add** — research uncovered relevant new developments the article does not mention
   - **Consider Removing** — information that is no longer relevant or could mislead
   - **Still Accurate** — claim verified as correct (abbreviated format)
3. Sort by confidence level within each category (high first)
4. Present the report directly in the conversation

Do not write the report to a file unless the user asks.

## Step 5: Optional edits

After presenting the report, ask: "Would you like help making these corrections? If so, how would you like to proceed?"

Let the user guide next steps. Possible paths:

- **Local files**: If the article source is a local file (e.g., markdown in `src/content/blog/`), read the source and apply corrections using Edit. Make surgical changes to specific claims, preserving the article's voice and style.
- **MCP tools**: If the user has WordPress, Google Docs, or similar MCP servers configured, offer to use those to make edits.
- **Manual guidance**: If neither is available, provide a concise list of specific edits with exact replacement text.
- **Save report**: If the user wants to save the report, ask where and write it as a markdown file.

After making edits, offer to re-run the fact-check on the updated article to confirm all issues are resolved.
