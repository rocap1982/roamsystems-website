---
name: skill-creator
description: >
  Guide for creating effective skills and iteratively improving them. Use when users want to
  create a new skill, update or improve an existing skill, optimize a skill's description for
  better triggering, or run test cases to verify skill quality. Also use when the user says
  "turn this into a skill" or asks about skill best practices, even if they don't use the
  word "skill" explicitly.
---

# Skill Creator

Create, test, and iteratively improve skills that extend Claude's capabilities.

## What Skills Are

Skills are modular packages that give Claude specialized knowledge, workflows, and tools for
specific domains. They transform a general-purpose agent into a specialist equipped with
procedural knowledge no model fully possesses on its own.

Skills provide: specialized workflows, tool integrations, domain expertise, and bundled
resources (scripts, references, assets) for complex/repetitive tasks.

## Core Principles

### Claude Is Already Smart

The context window is shared across system prompt, conversation history, other skills, and
the user's request. Only add context Claude doesn't already have. Challenge every paragraph:
"Does this justify its token cost?" Prefer concise examples over verbose explanations.

### Explain the Why, Not Heavy-Handed MUSTs

Today's LLMs respond better to reasoning than rigid directives. Instead of "ALWAYS do X" or
"NEVER do Y", explain *why* something matters. If you find yourself writing in all caps,
reframe as reasoning. This produces more robust, generalizable behavior than brittle rules.

### Set Degrees of Freedom

Match specificity to fragility:

- **High freedom** (text instructions): Multiple valid approaches, context-dependent decisions
- **Medium freedom** (pseudocode/parameterized scripts): Preferred pattern exists, some variation OK
- **Low freedom** (exact scripts, few params): Fragile operations, consistency critical

A narrow bridge needs guardrails; an open field allows many routes.

## Anatomy of a Skill

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter (name, description required)
│   └── Markdown instructions
└── Bundled Resources (optional)
    ├── scripts/    - Executable code for deterministic/repetitive tasks
    ├── references/ - Docs loaded into context as needed
    └── assets/     - Files used in output (templates, icons, fonts)
```

### SKILL.md

- **Frontmatter** (YAML): `name` and `description` (required), plus optional `compatibility`.
  Only name + description are read to determine triggering — all "when to use" info goes here.
- **Body** (Markdown): Instructions loaded only after the skill triggers.

### Bundled Resources

**Scripts** (`scripts/`): Executable code for tasks that are repeatedly rewritten or need
deterministic reliability. Token-efficient — can execute without loading into context.

**References** (`references/`): Documentation loaded as-needed. Keep SKILL.md lean by moving
detailed schemas, API docs, and domain knowledge here. For large files (>300 lines), include
a table of contents. Avoid duplication between SKILL.md and references.

**Assets** (`assets/`): Files used in output (templates, images, boilerplate) — not loaded
into context, just referenced/copied by Claude.

**Don't include**: README, CHANGELOG, INSTALLATION_GUIDE, or other auxiliary docs. Skills
contain only what an AI agent needs to do the job.

### Progressive Disclosure

Three-level loading system:

1. **Metadata** (name + description) — always in context (~100 words)
2. **SKILL.md body** — loaded when skill triggers (target <500 lines)
3. **Bundled resources** — loaded as needed (unlimited; scripts can execute without reading)

When approaching 500 lines, split into reference files with clear pointers about when to
read them. When a skill supports multiple variants/frameworks, keep core workflow in SKILL.md
and move variant-specific details to separate reference files.

**Domain organization example:**
```
cloud-deploy/
├── SKILL.md (workflow + selection guidance)
└── references/
    ├── aws.md
    ├── gcp.md
    └── azure.md
```
Claude reads only the relevant reference file.

## Creating a Skill

### When to Create a Skill

Extract a skill when:

- You've solved the same problem 2+ times across sessions
- The solution required multi-step domain knowledge Claude won't remember next session
- A sprint or session produced reusable procedural knowledge
- You keep re-discovering the same schemas, APIs, or workflows

Don't create a skill when a one-line note in `CLAUDE.md` or a reference doc in `docs/` would
suffice. Skills are for procedural knowledge that guides action, not passive reference data.

### Skill Scope

A skill should have a clear, cohesive domain. Signs it's too broad:

- It has 3+ unrelated workflows that never co-occur in a single user prompt
- The description needs "and" more than twice to explain what it covers
- Different sections would benefit from different trigger conditions

When this happens, split into separate skills. A `crm-data-model` skill and an
`api-platform` skill are more useful than a single `backend-everything` skill — they
trigger precisely, load less context, and are easier to iterate on independently.

On the other end: don't make skills too narrow. A skill that only handles "rotating PDFs
clockwise by 90 degrees" should be `pdf-editor` covering all PDF operations. The trigger
description handles routing.

Rule of thumb: **one skill per domain that a user would think of as one task category.**

### Updating an Existing Skill

When improving rather than creating:

1. **Read the current skill first** — understand what's there before changing it
2. **Preserve the directory name and `name` field** — renaming breaks slash-command registration
3. **Diff-based iteration** — make targeted edits, don't rewrite from scratch unless the
   skill is fundamentally broken. Small changes are easier to evaluate.
4. **Test before and after** — run the same prompt against the old and new version to see
   whether the change actually helped

### Step 1: Capture Intent

Start by understanding what the skill should do. The conversation may already contain a
workflow to capture ("turn this into a skill"). If so, extract the tools used, sequence of
steps, corrections made, and input/output formats observed.

Key questions (ask incrementally, not all at once):

1. What should this skill enable Claude to do?
2. When should it trigger? What user phrases/contexts?
3. What's the expected output format?
4. Are there edge cases or variants to handle?

Conclude when you have a clear picture of the functionality and trigger conditions.

### Step 2: Plan and Scaffold

Analyze concrete examples to identify reusable resources:

- **Same code rewritten every time?** → Bundle as a script
- **Same boilerplate/template needed?** → Bundle as an asset
- **Same schemas/docs re-discovered?** → Bundle as a reference

Example: A `pdf-editor` skill for rotating PDFs → bundle `scripts/rotate_pdf.py`.
Example: A `bigquery` skill for querying data → bundle `references/schema.md`.

To scaffold a new skill directory with proper frontmatter and example structure:

```bash
python .claude/skills/skill-creator/scripts/init_skill.py my-skill --path .claude/skills
```

This creates the directory, a SKILL.md template with TODO placeholders, and example
`scripts/`, `references/`, `assets/` directories. Delete any you don't need.

To validate structure and frontmatter before testing:

```bash
python .claude/skills/skill-creator/scripts/quick_validate.py .claude/skills/my-skill
```

### Step 3: Write the Skill

#### Frontmatter

The description is the primary trigger mechanism. Write it to be slightly "pushy" — Claude
tends to under-trigger skills, so lean toward broader matching.

```yaml
---
name: my-skill
description: >
  What this skill does and when to use it. Include specific trigger contexts.
  Use this skill whenever the user mentions X, Y, or Z, even if they don't
  explicitly ask for "skill-name" by name.
---
```

Bad: "Helps with documents"
Good: "Create, edit, and analyze Word documents (.docx). Use when Claude needs to work with
professional documents for creating new docs, modifying content, working with tracked changes,
adding comments, or any .docx task. Trigger whenever user mentions 'Word doc', '.docx',
'report', 'memo', or similar deliverables."

#### Body

Write instructions for another Claude instance to follow. Use imperative form. Focus on
what's non-obvious — don't explain things Claude already knows. A minimal complete body:

```markdown
# CSV Data Cleaner

## Workflow

1. Read the input file and detect encoding (watch for BOM markers in Windows CSVs)
2. Identify column types by sampling first 100 rows
3. Apply cleaning rules per column type:
   - Dates: normalize to ISO 8601 (many sources use MM/DD/YYYY)
   - Currency: strip symbols, convert to decimal
   - Phone: normalize to E.164
4. Write cleaned output, preserving original column order

## Edge cases

- Mixed encodings: if detection fails, try UTF-8 then Latin-1 then ask the user
- Merged cells from Excel exports: split into individual rows before processing

## Resources

- For column type detection heuristics, see `references/type-detection.md`
- For locale-specific date formats, see `references/locale-formats.md`
```

Include: workflow overview, input/output examples where helpful, resource pointers with
clear "when to read" triggers, and edge cases that would trip up a naive approach.

#### Output Patterns

When the skill needs consistent output, provide templates. Match strictness to the stakes —
a data pipeline needs exact structure, a report format is a sensible default the model can
adapt. Frame both as guidance with reasoning, not commands:

```markdown
## Report structure
Follow this structure because stakeholders expect a consistent format they can skim:
# [Title]
## Executive summary
## Key findings
## Recommendations
```

For style-dependent output, input/output examples teach better than descriptions:

```markdown
**Example 1:**
Input: Added user authentication with JWT tokens
Output: feat(auth): implement JWT-based authentication
```

#### Workflow Patterns

For multi-step tasks, give an overview up front:
```markdown
Filling a PDF form:
1. Analyze the form (run analyze_form.py)
2. Create field mapping (edit fields.json)
3. Fill the form (run fill_form.py)
4. Verify output (run verify_output.py)
```

For branching logic, guide through decision points:
```markdown
1. Determine the modification type:
   **Creating new content?** → Follow "Creation workflow"
   **Editing existing content?** → Follow "Editing workflow"
```

### Step 4: Test and Iterate

This is the most important part. Don't just write a skill and ship it — test it on
realistic prompts, evaluate the results, and improve.

#### Write Test Cases

Come up with 2-3 realistic test prompts — things a real user would actually say. Share them
with the user: "Here are a few test cases I'd like to try. Do these look right?"

Good test prompts are specific and realistic, not abstract:

Bad: "Format this data"
Good: "My boss sent me Q4-sales-final-v2.xlsx and wants a profit margin column added.
Revenue is in column C, costs in column D."

#### Run the Tests

For each test case, invoke the skill on the prompt and observe the output. Practical options:

- **Same session**: Load the skill (`/skill-name`), then give the test prompt. Quick but
  you have full context, so results may be optimistic.
- **Subagent** (preferred if available): Spawn an Agent with the skill path and test prompt.
  This runs in a clean context — closer to real-world usage. Run multiple in parallel.
- **Comparing versions**: Run the same prompt against old and new skill to see the delta.
  For updates, this is the most useful signal.

#### Evaluate Results

Two types of evaluation:

**Qualitative**: Show outputs to the user. For each test case, present the prompt and result.
Ask: "How does this look? Anything you'd change?" Empty feedback means it looked fine.

**Quantitative** (when outputs are objectively verifiable): Define assertions — specific,
checkable claims about the output. Good assertions have descriptive names and are objectively
verifiable. Don't force assertions onto subjective outputs (writing style, design quality).

#### Improve the Skill

When improving based on feedback:

1. **Generalize, don't overfit.** The skill will be used across many prompts — don't make
   fiddly changes that only fix the test cases. Understand *why* the user wanted something
   different and transmit that understanding into the instructions.

2. **Keep it lean.** If something isn't pulling its weight, remove it. Read test transcripts —
   if the skill makes Claude waste time on unproductive steps, cut those parts.

3. **Look for repeated work.** If every test case independently writes a similar helper script,
   that's a signal to bundle it in `scripts/`.

4. **Explain the reasoning.** Rather than adding rigid rules, explain why something matters.
   This is more robust and effective than brittle "ALWAYS/NEVER" directives.

#### Common Pitfalls

- **Description too vague to trigger.** "Helps with data" won't trigger on anything. Be
  specific about file types, domains, and user phrases.
- **Duplicating CLAUDE.md content.** If it's already in the project's root instructions,
  don't repeat it in the skill — it wastes context on things Claude already has.
- **Reference files with no pointers.** A `references/schema.md` that SKILL.md never
  mentions is invisible. Every reference file needs a "read this when..." pointer.
- **Covering too many unrelated domains.** If the skill handles email *and* calendar *and*
  CRM *and* documents, it's trying to be four skills. See "Skill Scope" below.
- **Overfitting to test cases.** Adding narrow rules that fix one test prompt but break
  generalization. Understand the *why* behind the feedback, not just the symptom.
- **Explaining things Claude already knows.** "JSON is a data format..." — don't. Only add
  knowledge Claude lacks (company-specific schemas, non-obvious workflows, domain quirks).

#### Iteration Loop

1. Apply improvements to the skill
2. Re-run test cases
3. Show results to user
4. Read feedback, improve again
5. If the skill isn't triggering on test prompts, jump to description optimization below
6. Repeat until feedback is empty or user is satisfied

### Step 5: Optimize the Description

After the skill content is solid — or earlier if triggering is unreliable — optimize the
description. You can return to this step any time during iteration if you notice the skill
isn't activating when it should.

#### Generate Trigger Eval Queries

Create ~20 test queries — a mix of should-trigger and should-not-trigger. Make them realistic
with detail, context, file paths, casual speech, typos, abbreviations.

**Should-trigger** (8-10): Different phrasings of the same intent — formal, casual, implicit.
Include cases where user doesn't name the skill but clearly needs it.

**Should-not-trigger** (8-10): Near-misses that share keywords but need something different.
These should be genuinely tricky, not obviously irrelevant.

Bad negative: "Write a fibonacci function" (for a PDF skill — too easy)
Good negative: "Can you read the text in this screenshot?" (shares 'read' and 'text' with
a PDF skill but needs OCR/vision, not PDF processing)

#### Test and Refine

Run each query and check whether the skill triggers correctly. Adjust the description based
on false positives (triggered when it shouldn't) and false negatives (didn't trigger when it
should). Iterate until triggering is reliable.

Note: Claude only consults skills for tasks it can't easily handle alone. Simple queries like
"read this file" may not trigger a skill regardless of description quality — they're too easy.
Test with substantive, multi-step queries.

## Project-Specific Conventions

### Location and naming

- Skills live at `.claude/skills/{skill-name}/SKILL.md`
- Use **kebab-case** for directory names: `ai-tool-design`, `db-drizzle`, `crm-data-model`
- Directory name = slash command name. A skill at `.claude/skills/my-skill/` registers as
  `/my-skill` automatically. Don't rename directories without considering this.

### Skill vs other docs

Choose the right home for your knowledge:

| Content type | Where it lives |
|---|---|
| Procedural knowledge that guides agent action | `.claude/skills/` |
| One-liner conventions/reminders | `CLAUDE.md` |
| Reference architecture, schemas, domain docs | `docs/` |
| Session-specific context | `docs/sessions/` |

Skills are for *how to do things*. If the content is purely "here's what exists" without
procedural guidance, it's probably a reference doc, not a skill.

### Progressive disclosure hierarchy

Skills fit into the project's layered context model:

1. `CLAUDE.md` — always loaded, broad project conventions
2. `PROJECT_STATUS.md` — always loaded, current state snapshot
3. `.claude/skills/` — loaded on-demand when triggered by user prompt
4. `docs/` — loaded by skills or agent as-needed

A good skill references the codebase modules it relates to (e.g., "API handlers live at
`packages/api/src/modules/{domain}/`") so the skill consumer knows where to look.

### When sprints produce skills

After completing a sprint that introduced new domain knowledge, consider whether to:

- **Create a new skill** — if the domain is new and procedural (e.g., `workflow-engine`)
- **Update an existing skill** — if the sprint extended a domain that already has one
- **Do nothing** — if the knowledge is already captured in canonical docs or `CLAUDE.md`

The `/close-session` and `/review-sprint` workflows prompt this check explicitly.
