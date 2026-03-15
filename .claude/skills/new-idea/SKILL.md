---
name: new-idea
description: Explore new functionality architecture through discussion and create an idea artifact under docs/ideas/. Use when exploring a feature concept, discussing implementation approaches, or designing new capabilities before committing to a plan.
argument-hint: "[feature or concept to explore]"
---

# /new-idea — Explore new functionality architecture (discussion + idea artifact)

## Goal

Facilitate a **discussion-only session** to explore and design new functionality before creating a formal plan.

Creates a durable idea artifact under `docs/ideas/` so the idea can be revisited without re-deriving context.

No runtime code changes will be made during this skill.

## Inputs

$ARGUMENTS

If no topic is provided, ask the user to describe the functionality they want to build.

## Steps

### Phase 1: Discovery

- Ask the user to describe the functionality they want to build
- Ask clarifying questions about:
  - Who will use it (user roles, permissions)
  - How it relates to existing features
  - Expected user workflows
  - Data that needs to be stored/displayed
  - Any external integrations needed

### Phase 2: Codebase analysis

- Search for similar patterns in the codebase
- Review relevant schema files
- Check existing API routes
- Look at similar UI implementations
- Review existing capabilities in relevant areas
- Check canonical documentation and identify what new docs would be required

### Phase 3: Architecture recommendations

Propose a high-level design covering:
- **Database layer**: tables, relationships, migrations approach
- **API layer**: endpoints, validation, auth middleware
- **UI layer**: pages, components, routing strategy
- **Integrations**: external services, webhooks, third-party APIs
- **Permissions**: role-based access control approach

### Phase 4: Trade-offs discussion

- Explore different approaches with pros/cons
- Consider phased implementation
- Identify dependencies and prerequisites

### Phase 5: Decision summary

- Summarize the agreed-upon architecture
- List key implementation steps/phases
- Note any dependencies or prerequisites

### Phase 6: Create the idea artifact (required)

- Create `docs/ideas/YYYY-MM-DD-<short-topic>.md` using `docs/ideas/idea-template.md`
- Set `status: draft` unless the user explicitly says the idea is accepted
- Link candidate canonical docs (do not edit canonical docs from an idea; use a plan when required)

## Output

1. **Architecture summary** — clear decisions on database, API, UI, integrations
2. **Implementation phases** — logical breakdown of work
3. **Idea file created** — path to the new `docs/ideas/...` document
4. **Next step** — suggest using `/new-plan` (if contract changes) or `/new-sprint` (if implementation-only)

## Important notes

- **NO runtime code changes** during this skill — discussion + documentation artifact only
- Reference existing patterns with code citations
- Be thorough but concise — aim for clarity over exhaustiveness
- If the idea requires changes to core contracts (auth, billing, org model), flag that early
- Keep the user engaged — this is a collaborative discussion, not a lecture
