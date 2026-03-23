---
name: ai-fluency
version: 4.0.0
description: |
  Analyze your past Claude Code conversations to measure AI fluency. Based on
  Anthropic's 4D AI Fluency Framework (Dakan & Feller, 2026) and their study of
  9,830 Claude.ai conversations. The 4 Ds: Delegation (strategic big picture),
  Description (clear communication), Discernment (critical evaluation), and
  Diligence (responsible use). Detects 11 observable behaviors, scores 7 practical
  dimensions, and compares you to population baselines. Works on any project
  with conversation history.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Task
  - AskUserQuestion
---

# AI Fluency Analysis

Analyze the user's past Claude Code conversations and produce an AI fluency report based on Anthropic's research.

## Prerequisites

This skill requires `cc-conversation-search` to locate conversations. Check and install if needed:

```bash
if command -v cc-conversation-search &> /dev/null; then
    echo "Ready: $(cc-conversation-search --version)"
else
    if command -v uv &> /dev/null; then
        uv tool install cc-conversation-search
    else
        pip install --user cc-conversation-search
        export PATH="$HOME/.local/bin:$PATH"
    fi
    cc-conversation-search init --days 14
fi
```

## Arguments

- No arguments: Analyze the last 2 weeks of conversations (default)
- A number (e.g., `7`): Analyze conversations from the last N days
- A topic (e.g., `"authentication"`): Analyze only conversations matching that topic
- `"all"`: Analyze all indexed conversations

## Workflow

### Step 1: Discover Conversations

Based on arguments, find conversations to analyze:

```bash
# Default: last 14 days
cc-conversation-search list --days 14 --json

# Or with topic filter
cc-conversation-search search "topic" --days 14 --json
```

Select a diverse sample of **up to 8 conversations** for analysis. Prefer conversations with at least 5 user messages. Aim for variety in:
- Conversation length (short and long)
- Task type (debugging, feature work, exploration, ops)
- Different projects if available

### Step 2: Analyze Each Conversation

For each selected conversation, read the JSONL file and extract only messages where `"role": "human"`. Ignore messages that are:
- Empty strings or whitespace only
- Pure tool results (automated system messages)
- Skill/command template expansions (long system prompts with frontmatter `---` patterns or "Base directory for this skill" markers)

For each conversation, do TWO things:
1. **Behavior detection** (Layer 1): Check for the presence/absence of each of the 11 Observable Behaviors + Diligence signals
2. **Dimension scoring** (Layer 2): Score the 7 Practical Dimensions on a 1-10 scale

### Step 3: Score and Generate HTML Report

After all conversation analyses are complete, aggregate the scores and generate an HTML report.

Use Task agents to analyze conversations in parallel (up to 4 at a time) for efficiency. Each agent should read one conversation file and return both the behavior checklist and dimension scores with evidence.

**HTML Report Generation:**
1. Read the template at `.claude/skills/ai-fluency/report-template.html` (relative to the project root)
2. Calculate all aggregated scores (behavior frequencies, dimension averages, population comparisons)
3. Replace all `{{PLACEHOLDER}}` markers with the actual data (see the HTML Report Placeholders section below)
4. Write the final HTML to `~/Desktop/ai-fluency-report.html`
5. Open it with `open ~/Desktop/ai-fluency-report.html`
6. Also print a brief text summary to the conversation (overall score, level, top strength, top growth edge)

---

## The 4D AI Fluency Framework

AI fluency is the practical skills, knowledge, insights, and values that help you use AI **effectively**, **efficiently**, **ethically**, and **safely**. The framework (developed by Professors Rick Dakan and Joseph Feller in collaboration with Anthropic) identifies four core competencies:

| Competency | Focus | Goal | Key Question |
|------------|-------|------|-------------|
| **Delegation** | Strategic big picture | Effective & Efficient | What's the goal? What should AI handle vs. you? How to divide the work? |
| **Description** | Clear communication | Effective | Are you articulating needs, context, format, approach, and tone clearly? |
| **Discernment** | Critical evaluation | Effective | Are the facts accurate? Does the reasoning hold? Does this output actually help? |
| **Diligence** | Responsible use | Ethical & Safe | Are you protecting data? Checking for bias? Being transparent? Taking accountability? |

Most AI interactions involve **small loops of Description and Discernment**: describe what you need, evaluate what you get, refine your request, repeat. Delegation sets up the loop; Diligence governs it.

The Anthropic study measured 11 of 24 framework behaviors that are directly observable in conversation text. The remaining 13 (many Diligence behaviors) occur outside the chat. However, some Diligence signals ARE detectable in Claude Code conversations.

---

## Layer 1: The 11 Observable Behaviors + Diligence Signals

These are the exact behaviors from Anthropic's study, organized by competency. For each conversation, mark whether the behavior is **present** or **absent**. A behavior is present if the user demonstrates it at least once in the conversation.

### Description Behaviors (green -- task specification)

| # | Behavior | Population Baseline | What to look for |
|---|----------|-------------------|------------------|
| 1 | **Iterates and refines** | 85.7% | Multi-turn exchanges that build on previous output. Requesting changes, adjustments, or improvements to AI output. |
| 2 | **Provides examples of what good looks like** | 41.1% | Pasting sample output, reference code, documentation, screenshots, or "make it look like X". |
| 3 | **Specifies format and structure needed** | 30.0% | Requesting specific output format (table, list, JSON), code structure, file organization, or response length. |
| 4 | **Sets interaction mode** | 30.0% | Telling the AI how to behave: "be concise", "explain step by step", "don't make changes yet, just analyze", "use tool X not Y". |
| 5 | **Communicates tone and style preferences** | 22.7% | Directing voice, formality, audience-appropriate language. "Keep it technical", "explain like I'm new to this". |
| 6 | **Defines audience for the output** | 17.6% | Specifying who will read/use the output: "this is for the team", "the PR reviewer needs to understand...", "the end user will...". |

### Delegation Behaviors (purple -- strategic big picture)

Delegation is about having a clear vision and strategically choosing how AI fits into your process. It's not just offloading tasks -- it's understanding your goal, recognizing what AI can and can't do well, and thoughtfully dividing the work.

| # | Behavior | Population Baseline | What to look for |
|---|----------|-------------------|------------------|
| 7 | **Clarifies goal before asking for help** | 51.1% | Providing context, background, and the "why" before making requests. Explaining the problem before jumping to a solution. Understanding what you're trying to accomplish. |
| 8 | **Consults AI on approach before execution** | 10.1% | Asking "how should we approach this?", "what are the options?", requesting a plan before implementation. Letting the AI propose strategy rather than dictating every step. |

### Discernment Behaviors (pink -- critical evaluation)

| # | Behavior | Population Baseline | What to look for |
|---|----------|-------------------|------------------|
| 9 | **Identifies when AI might be missing context** | 20.3% | Proactively providing information the AI wouldn't know. "You should also know that...", "the thing you're missing is...", pointing out codebase-specific context. |
| 10 | **Questions when AI reasoning doesn't hold up** | 15.8% | Pushing back on AI suggestions. "Why X over Y?", "That doesn't seem right because...", "Are you sure about...?", challenging assumptions. |
| 11 | **Checks facts and claims that matter** | 8.7% | Verifying AI output against reality. Testing code, checking API responses, reviewing diffs, fact-checking assertions, pasting evidence that contradicts AI output. |

### Diligence Signals (the 4th D -- responsible use)

Diligence means taking ownership of AI-assisted work and being willing to stand behind it. Most Diligence behaviors occur outside the chat (e.g., reviewing before publishing, attributing AI involvement), but some signals ARE observable in Claude Code conversations. These don't have population baselines from the Anthropic study, so mark as present/absent without comparison.

| # | Signal | What to look for |
|---|--------|------------------|
| D1 | **Protects sensitive data** | Avoids pasting secrets, credentials, PII into conversations. Redacts sensitive info. Uses environment variables instead of hardcoding. |
| D2 | **Considers bias and fairness** | Questions whether AI-generated content could be biased. Asks about edge cases for different user groups. Considers accessibility. |
| D3 | **Takes accountability for AI output** | Reviews diffs before committing. Tests code before shipping. Doesn't blindly merge AI-generated PRs. Treats AI output as a draft, not a final product. |
| D4 | **Is transparent about AI involvement** | Uses Co-Authored-By tags, mentions AI assistance in PRs/docs where appropriate. Doesn't misrepresent AI work as purely their own in contexts where it matters. |
| D5 | **Verifies before impacting others** | Confirms before pushing, deploying, sending messages, or modifying shared resources. Asks "should I push this?" rather than assuming. |

---

## Layer 2: The 7 Practical Dimensions (1-10 scale)

These dimensions provide nuanced scoring beyond binary behavior detection. They measure how WELL the user exhibits fluency behaviors, not just whether they appear.

### Dimension 1: Specification (1-10)
How clearly the user defines tasks, constraints, and desired output.

| Score | Behavior |
|-------|----------|
| 1-2 | Vague, single-word requests ("fix it", "help") |
| 3-4 | States what they want but no constraints, format, or context |
| 5-6 | Provides context and basic constraints; occasionally ambiguous |
| 7-8 | Clear task definition with format, audience, scope, and examples |
| 9-10 | Pre-written specs with parameter tables, acceptance criteria, edge cases |

**Maps to behaviors:** #2 Provides examples, #3 Specifies format, #5 Tone/style, #6 Defines audience, #7 Clarifies goal

### Dimension 2: Iteration (1-10)
Whether the user refines through multi-turn dialogue vs. accepting first output.

| Score | Behavior |
|-------|----------|
| 1-2 | Single-turn: one request, accepts whatever comes back |
| 3-4 | Occasional follow-up, but mostly accepts first output |
| 5-6 | Regular follow-ups that build on previous output |
| 7-8 | Multi-turn refinement with specific change requests |
| 9-10 | Systematic iteration where each message advances toward a clear goal; conversation has a visible arc |

**Maps to behavior:** #1 Iterates and refines

**Key research finding:** Iteration is the gateway behavior. Users who iterate show 2x more fluency behaviors across ALL other dimensions. Specifically:
- Clarifies goal: 54.5% vs 30.9% (+23.6pp)
- Provides examples: 44.4% vs 21.8% (+22.6pp)
- Identifies missing context: 22.8% vs 5.7% (+17.1pp)
- Specifies format: 32.4% vs 16.1% (+16.3pp)
- Questions reasoning: 17.9% vs 3.2% (+14.7pp)

### Dimension 3: Discernment (1-10)
Whether the user critically evaluates AI output rather than accepting it.

| Score | Behavior |
|-------|----------|
| 1-2 | Never questions output, accepts everything at face value |
| 3-4 | Notices obvious errors but doesn't probe reasoning |
| 5-6 | Points out specific problems in output; asks for fixes |
| 7-8 | Challenges assumptions, asks "why X over Y?", identifies missing context |
| 9-10 | Fact-checks claims, tests hypotheses against output, reviews diffs before merging, provides contradicting evidence |

**Maps to behaviors:** #9 Identifies missing context, #10 Questions reasoning, #11 Checks facts

**Key research finding:** These are the RAREST behaviors in the population. Only 8.7% of users check facts. This is the highest-leverage area for improvement for most users.

### Dimension 4: Delegation (1-10)
The strategic big picture: understanding your goal, recognizing what AI can and can't do, and thoughtfully dividing the work. Delegation isn't just offloading tasks -- it's having a clear vision and strategically choosing how AI fits into your process.

| Score | Behavior |
|-------|----------|
| 1-2 | No strategic awareness; treats AI as a command executor |
| 3-4 | Occasional tool specification ("use grep for this") but no strategic division of work |
| 5-6 | Understands what AI should handle vs. what requires human judgment; sets basic expectations |
| 7-8 | Shapes the collaboration: "analyze first, then implement", consults on strategy, reserves critical decisions for themselves while delegating research/execution |
| 9-10 | Expert division of labor: knows exactly which work AI excels at, sets up feedback loops, adjusts collaboration style per task type, delegates decomposition when the structure exists elsewhere |

**Maps to behaviors:** #4 Sets interaction mode, #7 Clarifies goal, #8 Consults AI on approach

### Dimension 5: Task Decomposition (1-10)
Whether the user breaks complex work into appropriate sub-tasks.

| Score | Behavior |
|-------|----------|
| 1-2 | Dumps entire complex problem as one request |
| 3-4 | Occasionally sequences steps but mostly single-shot requests |
| 5-6 | Naturally phases work (investigate -> plan -> implement) |
| 7-8 | Explicit sub-task creation, parallel workstreams, ticketing integration |
| 9-10 | Knows when to decompose manually vs. delegate decomposition; uses project management tools to structure work across sessions |

### Dimension 6: Tool Awareness (1-10)
Whether the user understands AI capabilities and limitations, and leverages the tool ecosystem effectively.

| Score | Behavior |
|-------|----------|
| 1-2 | No awareness of what the AI can/cannot do |
| 3-4 | Basic awareness (knows AI can write code, search files) |
| 5-6 | Knows about specific integrations (MCP tools, CLI features) |
| 7-8 | Understands capability boundaries, provides manual help where AI cannot access, specifies which tools to use |
| 9-10 | Expert orchestration: teams, worktrees, parallel agents, custom skills; knows when AI is the wrong tool; acts as human proxy for things AI cannot access |

### Dimension 7: Diligence (1-10)
Taking ownership of AI-assisted work. Using AI responsibly: protecting data, checking for bias, being transparent about AI involvement, and being willing to stand behind the final product.

| Score | Behavior |
|-------|----------|
| 1-2 | No awareness of responsible AI use; shares secrets freely, ships without review |
| 3-4 | Basic caution (doesn't share passwords) but no systematic approach |
| 5-6 | Reviews AI output before shipping; aware of data sensitivity; uses Co-Authored-By tags |
| 7-8 | Systematic review process; considers bias/fairness; confirms before impacting shared systems; transparent about AI involvement |
| 9-10 | Treats AI output as draft requiring human validation; established review workflows; actively considers downstream impact on users; would stand behind every piece of AI-assisted work |

**Maps to signals:** D1-D5

**Note:** Many Diligence behaviors happen outside the chat (e.g., how you present AI work to colleagues, whether you review before publishing). Score based on what's observable in the conversation, but note that this dimension may be underestimated.

---

## The Artifact Paradox

**CRITICAL DIAGNOSTIC**: When AI generates artifacts (code, documents, structured output), a specific pattern emerges that you MUST check for:

**Description and Delegation behaviors INCREASE with artifacts:**
- Iterates and refines: 94.1% vs 84.5% (+9.7pp)
- Clarifies goal: 64% vs 49.3% (+14.7pp)
- Provides examples: 52.9% vs 39.5% (+13.4pp)
- Specifies format: 42.8% vs 28.3% (+14.5pp)

**But ALL THREE Discernment behaviors DECREASE:**
- Checks facts: 5.5% vs 9.2% (-3.7pp)
- Questions reasoning: 13% vs 16.2% (-3.1pp)
- Identifies missing context: 15.8% vs 21% (-5.2pp)

This means: **When AI produces polished-looking output (especially code), users become MORE directive but LESS critical.** They tell the AI what to build but stop questioning whether it's correct.

**How to detect this in conversations:**
1. Identify conversations where the AI generated code, PRs, documents, or other artifacts
2. Compare the user's discernment behaviors in those conversations vs. non-artifact conversations
3. Look specifically for: requesting PRs without reviewing diffs, accepting generated code without testing, not questioning architectural decisions when AI produces a working implementation

**In the report**, explicitly call out whether the user shows the artifact paradox and provide specific examples.

---

## Scoring Guidelines

### Per-Conversation Scoring
- Read ALL user messages in the conversation
- For Layer 1 (behaviors): binary present/absent for each of the 11 behaviors + 5 Diligence signals
- For Layer 2 (dimensions): score each of the 7 dimensions; score reflects the user's typical behavior, not their best single moment
- If a dimension is not applicable (e.g., no complex task to decompose), note "N/A" and exclude from averages

### Cross-Conversation Scoring
- **Behavior prevalence**: Calculate what percentage of conversations each behavior appeared in
- **Dimension averages**: Average each dimension across all analyzed conversations, weighting longer conversations slightly more
- **Consistency note**: Flag if scores vary significantly by task type (some users are highly fluent in debugging but not in feature specification)

### Overall Score
- Average of all 7 dimension averages
- Round to one decimal place

### Fluency Levels

| Score | Level | Description |
|-------|-------|-------------|
| 1-2 | Basic | Accepts first output, minimal direction |
| 3-4 | Directed | Specifies what they want but not how to get there |
| 5-6 | Iterative | Refines through dialogue, builds on output |
| 7-8 | Evaluative | Questions reasoning, catches errors, shapes collaboration |
| 9-10 | Orchestrative | Directs the collaboration itself, expert tool usage |

---

## HTML Report Placeholders

The HTML template at `.claude/skills/ai-fluency/report-template.html` uses `{{PLACEHOLDER}}` markers. Replace each one:

### Inline value placeholders

- `{{HEADER_META}}` — e.g. `8 conversations &middot; 14 days &middot; Feb 26, 2026`
- `{{HERO_SUBTITLE}}` — e.g. `Based on <span>8 conversations</span> over <span>14 days</span> &mdash; Anthropic 4D AI Fluency Index <em>(Dakan &amp; Feller, 2026)</em>`
- `{{OVERALL_SCORE}}` — e.g. `5.7` (displayed in gauge)
- `{{LEVEL_BADGE}}` — e.g. `Iterative <span class="arrow">&rarr;</span> approaching Evaluative` (use the fluency level from scoring guidelines)
- `{{TOTAL_CONVERSATIONS}}` — e.g. `8`
- `{{OVERALL_SCORE_NUM}}` — e.g. `5.7` (used in JS gauge animation)

### Behavior cards placeholder (`{{BEHAVIOR_CARDS}}`)

Generate 4 `<div class="card">` blocks — one for each 4D competency (Description, Delegation, Discernment, Diligence). Each card contains behavior items:

```html
<div class="card">
  <div class="card-title"><span class="dim-dot description"></span> <span class="dim-label description">Description</span> &mdash; clear communication</div>
  <div class="behavior-item">
    <div class="behavior-freq" style="color: var(--color-green);">6/8</div>
    <div class="behavior-text">Iterates and refines <span class="pct">(pop: 85.7%)</span></div>
    <span class="status-badge above">Above</span>
  </div>
  <!-- ... more behavior-items ... -->
</div>
```

Status badge classes: `well-above`, `above`, `at`, `below`, `violation`. Freq color: green if above population baseline, amber if within 10pp, red if below or 0.

### Strengths placeholder (`{{STRENGTHS_HTML}}`)

Generate 2-3 `<div class="insight-card strength">` blocks with quotes in `<blockquote>` tags:

```html
<div class="insight-card strength">
  <div class="insight-number strength">Strength 1</div>
  <div class="insight-title">Title with score</div>
  <div class="insight-body">
    <p>Description paragraph.</p>
    <blockquote>"user quote here" <span class="conv-ref">&mdash; Conv N</span></blockquote>
    <p>More analysis.</p>
  </div>
</div>
```

### Growth edges placeholder (`{{EDGES_HTML}}`)

Generate 2-3 `<div class="insight-card edge">` blocks. Include `<div class="suggestion-box">` for actionable advice:

```html
<div class="insight-card edge">
  <div class="insight-number edge">Edge 1</div>
  <div class="insight-title">Title with score</div>
  <div class="insight-body">
    <p>Description.</p>
    <blockquote>"user quote" <span class="conv-ref">&mdash; Conv N</span></blockquote>
    <div class="suggestion-box"><strong>Suggestion:</strong> Actionable advice here.</div>
  </div>
</div>
```

### Artifact paradox placeholder (`{{PARADOX_HTML}}`)

Generate an `<div class="insight-card paradox">` with a `<div class="paradox-grid">` containing two `paradox-case` divs (one `.bad`, one `.good`) for comparison:

```html
<div class="insight-card paradox">
  <div class="insight-number paradox">Verdict: [Present/Absent/Partial]</div>
  <div class="insight-title">Summary title</div>
  <div class="insight-body">
    <p>Analysis paragraph.</p>
    <div class="paradox-grid">
      <div class="paradox-case bad">
        <div class="paradox-case-title">Textbook Paradox &mdash; Conv N</div>
        <p>Description of the paradox case.</p>
        <div class="paradox-scores">
          <span class="paradox-score bad">Disc: 3</span>
          <span class="paradox-score bad">Iter: 1</span>
        </div>
      </div>
      <div class="paradox-case good">
        <div class="paradox-case-title">Counter-example &mdash; Conv N</div>
        <p>Description.</p>
        <div class="paradox-scores">
          <span class="paradox-score good">Disc: 8</span>
          <span class="paradox-score good">Iter: 8</span>
        </div>
      </div>
    </div>
    <p><strong>Pattern:</strong> Summary of when the paradox activates.</p>
  </div>
</div>
```

If no artifact paradox is detected, use a single `.good` case with an explanation.

### Profile summary placeholder (`{{PROFILE_SUMMARY_HTML}}`)

Generate 2-3 `<p>` tags summarizing the comparison to population norms. Use `<strong>` for emphasis.

### JS data array placeholders

**`{{CONVERSATIONS_JS_ARRAY}}`** — JSON array of conversation objects:
```js
[
  { num: 1, topic: 'Topic name', msgs: 6, spec: 2, iter: 2, disc: 4, deleg: 6, decomp: 2, tools: 5, dilig: 3, overall: 3.4 },
  // ... one per conversation
]
```

**`{{DIMENSIONS_JS_ARRAY}}`** — JSON array of dimension objects:
```js
[
  { name: 'Specification', score: 4.4, assessment: 'Brief assessment text' },
  // ... 7 dimensions + Overall
]
```

**`{{COMPARISONS_JS_ARRAY}}`** — JSON array of population comparison objects:
```js
[
  { label: 'Iteration rate', pop: 85.7, user: 75.0, delta: -10.7 },
  // ... 11 behaviors
]
```

### Methodology and footer placeholders

- `{{METHODOLOGY_TEXT}}` — Methodology paragraph explaining the framework, sample size, scoring approach, and baseline source
- `{{FOOTER_DATE_LINE}}` — e.g. `Generated February 26, 2026 &middot; Framework: Anthropic 4D AI Fluency Index v1.0`

## Report Content Guidelines

For each report section, follow these content guidelines:

### Section 4: Signature Strengths
Top 2-3 patterns with specific quotes from conversations as evidence.

### Section 5: Growth Edges
Top 2-3 areas for improvement with specific quotes and actionable suggestions.

### Section 6: The Artifact Paradox Check
Explicitly state whether the user shows the artifact paradox pattern. Compare their discernment behaviors in artifact-producing conversations vs. non-artifact conversations. Provide specific examples.

### Section 7: Comparison to Anthropic's Research

Highlight behaviors where the user significantly exceeds or falls below the baseline (>10pp delta).

---

## Analyzing User Messages from JSONL

Conversation files are JSONL (one JSON object per line). To extract user messages:

1. Each line is a JSON object with fields including `type`, `message` (which has `role` and `content`)
2. User messages have `"role": "human"` inside the `message` object
3. The `content` field may be a string or an array of content blocks
4. Filter out:
   - Empty or whitespace-only content
   - Messages that are purely `tool_result` blocks (automated responses to tool calls)
   - Very long messages that are clearly system-generated skill/command expansions (check for frontmatter `---` patterns or "Base directory for this skill" markers)
5. Count and analyze the remaining substantive human messages

Use Task agents to analyze conversations in parallel (up to 4 at a time) for efficiency. Each agent should read one conversation file and return both the behavior checklist and dimension scores with evidence.

---

## Reference

This skill is based on:
- **Anthropic's AI Fluency Index** (Jan 2026): https://www.anthropic.com/research/AI-fluency-index
- **4D AI Fluency Framework** by Professor Rick Dakan (Ringling College of Art and Design) and Professor Joseph Feller, developed in collaboration with Anthropic
- Analysis of **9,830 Claude.ai conversations** from January 2026
- The framework identifies **24 total behaviors** for safe and effective human-AI collaboration; **11 are directly observable** in conversation text (the remaining 13 occur outside the chat interface)

### The 4 Ds (from Rick Dakan's lecture):
- **Delegation**: The big picture. What are you trying to accomplish? What work should you handle yourself? Where might AI be helpful? "Delegation isn't just about offloading tasks. It's about having a clear vision and strategically choosing how AI fits into your process."
- **Description**: Clear communication. Goes beyond just writing prompts -- it's about detailed, context-rich conversations that establish what you're hoping to achieve, format of output, how you want AI to approach the task, context it needs, and tone/style of interaction.
- **Discernment**: Thoughtfully evaluating what AI gives you. Are the facts accurate? Does the reasoning make sense? Does this output actually help you move forward? "Most of our interactions with AI involve small loops of description and discernment."
- **Diligence**: Responsible AI interactions. Ensuring fairness, verifying accuracy, protecting sensitive data, being transparent about AI involvement, and taking ownership. "Diligence means taking ownership of your AI-assisted work and being willing to stand behind final products created using AI."

### Key findings from the study:
- 85.7% of conversations show iteration (the gateway behavior)
- Iterators exhibit 2.67 additional fluency behaviors (~2x the non-iterative rate)
- Only 8.7% of users check facts; only 15.8% question reasoning
- The **artifact paradox**: when AI generates code/documents, users become more directive but less critical (all 3 discernment behaviors decrease)
- Only 30% of users set interaction mode (direct how the AI should work with them)
- Only 10.1% consult the AI on approach before execution
- These competencies "aren't tied to specific AI tools or techniques that might become outdated -- they're fundamental skills that will help you adapt and grow alongside this rapidly evolving technology"
