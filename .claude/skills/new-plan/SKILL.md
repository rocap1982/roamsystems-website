---
name: new-plan
description: Create a formal plan document for contract-impacting changes (schema/API/integration/business rules). Use when a change requires explicit approval before implementation.
argument-hint: "[topic]"
---

# /new-plan — Create a comprehensive plan document

## Goal

Create a formal plan document for **contract-impacting changes** (schema/API/integration/business rules) that requires explicit approval before implementation.

## When to use

Create a plan for changes to:
- **Database schemas** (tables, columns, constraints, migrations)
- **API contracts** (endpoints, request/response shapes, error envelopes)
- **Integration contracts** (external payloads, webhooks, partner APIs)
- **Business rules** (documented canonical behavior)

**Not required for:**
- Internal refactors with no contract change
- Bug fixes restoring compliance with existing specs

## Ideal workflow

```
/new-idea   -> discuss architecture and design
/new-plan   -> formalize design (this skill)
  pause: wait for approval
/new-sprint -> create sprint doc (agent-readable execution plan)
  execute implementation
```

Note: `/new-sprint` creates a sprint document that breaks down the approved plan into actionable tasks for agents to execute. It's the bridge between "what to build" (plan) and "how to build it" (sprint plan).

## Steps

### Phase 1: Gather context

If coming from `/new-idea`, you should already have:
- Clear problem statement
- Proposed architecture
- Implementation phases
- Key decisions

If not, ask the user to provide:
- What contract is changing (schema/API/integration/business rule)
- Why the change is needed
- What alternatives were considered

### Phase 2: Read the plan template and context

- Read `docs/plans/plan-template.md` to understand the required structure
- Read `docs/plans/README.md` for governance context (if exists)
- Optionally review recent plans in `docs/plans/` for examples

### Phase 3: Create the plan file

**Filename format**: `docs/plans/YYYY-MM-DD-<short-topic>.md`
- Use today's date
- Use kebab-case for topic
- Keep topic concise (3-6 words)

### Phase 4: Fill each section thoughtfully

Use the template structure, ensuring each section is complete:

#### Required Metadata (frontmatter)
- **Status**: Always start as "Draft"
- **Created**: Today's date
- **Author**: AI or human name
- **Approver**: leave blank initially
- **Related Issues**: link to relevant audit issues if applicable

#### Problem Statement
- **Current State**: What exists now (be specific, reference code/files)
- **Desired State**: What should exist (concrete outcomes)
- **Why This Matters**: Impact if not addressed (user/business value)

#### Proposed Solution
- **Canonical Changes Required**:
  - List affected docs (or note if canonical docs need to be created)
  - Specify change type: Minor (additive), Major (breaking), or Patch (clarification)
- **Proposed Specification**:
  - Schema definitions (database table types)
  - API endpoint signatures
  - Example usage (actual code snippets)
  - Semantics/business rules

#### Implementation Impact
- **Code Changes Required**: list files to modify with descriptions
- **New Files**: list new files with purposes
- **Test Changes**: existing tests to update + new tests needed
- **Data/Migration Impact**: migration required? Describe approach

#### Migration Plan (if breaking)
- Is it backward compatible?
- Migration steps (specific, numbered)
- Rollback procedure

#### Alternatives Considered
For each alternative:
- Description
- Pros/cons
- Why not chosen

#### Traceability
Link the plan to:
- Canonical docs (before and after)
- Implementation files (anticipated)
- Test files (anticipated)
- Related audits (if any)

#### Risks
Table format:
| Risk | Likelihood | Impact | Mitigation |

Consider:
- Data loss/corruption risks
- Breaking changes to existing features
- Performance impacts
- Security implications
- Migration failure scenarios

### Phase 5: Review checklist

Before presenting to user, verify:
- [ ] Filename follows `YYYY-MM-DD-<topic>.md` format
- [ ] All required sections are filled (not just placeholders)
- [ ] Code examples are realistic (reference actual project patterns)
- [ ] File paths reference actual locations in the repo
- [ ] Migration impact is assessed
- [ ] Risks are identified with mitigations
- [ ] Alternatives show you considered multiple approaches
- [ ] Traceability links are specific (not vague)
- [ ] Schema examples follow existing project patterns
- [ ] API examples follow project's routing and auth patterns

### Phase 6: Present to user

1. **Show the plan location** - Full path to the created file
2. **Summarize key points**:
   - What's being proposed
   - Why it's needed
   - Major implementation steps
   - Key risks/mitigations
3. **Explain approval requirement**: Stop here - do not implement until approved
4. **Ask for review**: Request user to review and approve/request changes

### Phase 7: Stop and wait

**CRITICAL**: Do not implement any code changes until the user explicitly approves the plan.

The user may:
- Approve as-is -> proceed to `/new-sprint` to create execution plan
- Request changes -> update plan and re-present
- Reject -> discuss alternatives or abandon

## Best practices

### Writing clear problem statements
- Be specific about current limitations
- Quantify impact where possible
- Reference actual user pain points or business needs

### Designing good specifications
- Follow existing project patterns (check similar features)
- Show before/after examples
- Include validation rules
- Consider edge cases

### Assessing risks realistically
- Don't downplay risks to make plan look better
- Think about what could go wrong
- Provide concrete mitigations (not "we'll be careful")

### Considering alternatives thoroughly
- Show you explored multiple approaches
- Explain trade-offs honestly
- Document why the proposed solution is best

## After approval

Once approved:
1. User updates plan status to "Approved" and adds approval date
2. Use `/new-sprint` to create a sprint document with agent-readable execution plan
3. Sprint doc breaks plan into phases/tasks with clear acceptance criteria
4. Implement sprint tasks with traceability (reference plan in commits)
5. Update canonical docs after implementation
6. Mark plan as "Implemented" when complete

## Common pitfalls to avoid

- Vague problem statements ("we need to improve X")
- Missing migration plans for schema changes
- No alternatives considered
- Unrealistic risk assessments ("no risks")
- Plans that skip straight to implementation details without context
- Not linking to canonical docs that need updating
- Missing traceability links to actual project files
