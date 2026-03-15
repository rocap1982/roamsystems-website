---
name: new-sprint
description: Create a sprint document that turns an approved direction into an agent-executable work plan. Use when ready to break down approved work into actionable tasks with parallel sub-agent support.
argument-hint: "[topic] [optional: sprint-number] [optional: dates]"
---

# /new-sprint — Create a Sprint Document (Agent-Executable Work Plan)

## Goal

Create a sprint document that turns an approved direction (idea/plan) into an **agent-executable work plan**: clear scope, crisp acceptance criteria, staged execution, and a task list that maps to real files and checks. Tasks should be tagged by domain so parallel sub-agents can work on independent tracks simultaneously.

## When to use

- **If the sprint will change contracts** (schemas/API/DB/business rules): the sprint **must link to the plan(s)** in `docs/plans/` and should start in `stage: planning` until approval exists.
- **If the sprint is implementation-only** (no contract changes): a plan is optional; the sprint can proceed once acceptance criteria and tasks are defined.

## Ideal workflow

```
/new-idea   -> explore architecture (discussion only)
/new-plan   -> formalize contract changes (approval required)
/new-sprint -> create agent-readable execution plan (this skill)
/start-sprint -> execute the sprint, track stage, keep status docs current
```

## Inputs

$ARGUMENTS

Gather (or infer from `CURRENT_STATUS.md` + prior docs) the following:

- **Topic**: short sprint topic (3-8 words, kebab-case friendly)
- **Sprint number**: next sequential number for the month (see filename convention below)
- **Dates**: start/end (YYYY-MM-DD)
- **Goal**: one-sentence sprint goal
- **Scope boundaries**: in-scope vs explicit non-goals
- **Links**:
  - related plan doc(s) in `docs/plans/` (required if contracts change)
  - related audits in `docs/audits/active/` (if applicable)

If minimal input is provided, ask the user for the sprint name/topic, planned dates, and goal.

## Steps

### Phase 0: Load context (read-only)

- Read:
  - `docs/sprints/sprint-template.md` (required structure)
  - `docs/sprints/CURRENT_STATUS.md` (active sprint + stage + priorities)
  - `PROJECT_STATUS.md` (resume-fast snapshot; update after sprint creation)
- If coming from an approved plan in `docs/plans/`, read it for scope and acceptance criteria.
- Optionally review recent sprints in `docs/sprints/` for examples.
- Identify whether contract changes are expected.
  - If yes, ensure plan(s) exist in `docs/plans/` and link them in the sprint doc.

### Phase 1: Choose the sprint filename + frontmatter

**Filename format**: `docs/sprints/YYYY-MM-sprint-<n>-<topic>.md`

- Use the next available sprint number `<n>` for the month.
- Keep `<topic>` short and descriptive (kebab-case).

**Frontmatter (required)**:

- `doc_type: sprint`
- `status: active`
- `stage: planning` (initial default)
- `created: YYYY-MM-DD`
- `last_updated: YYYY-MM-DD`
- `dates: { start: YYYY-MM-DD, end: YYYY-MM-DD }`
- `sprint_goal: <single clear sentence>`

### Phase 2: Write the sprint content so an agent can execute it

Fill the template fully (no placeholders). The sprint doc must include:

- **Summary**
  - Goal (one sentence)
  - Stage (must match frontmatter `stage`)
  - Scope (short, explicit list of areas)
- **Acceptance criteria**
  - 5-12 checkbox items, written as observable outcomes
  - Use "verifiable" language (what must be true at the end)
- **Contracts / governance**
  - Answer "contract-impacting changes expected?"
  - Link plan doc(s) (required when contracts change)
  - If plan approval is pending: keep `stage: planning` and record the approval dependency in `CURRENT_STATUS.md` blockers/priorities.
- **Work plan** (designed for parallel sub-agent execution)
  - Create tasks that map to real repo locations and/or concrete deliverables.
  - Format each task to be scannable:
    - `[owner]` domain tag: `[DB]`, `[API]`, `[UI]`, `[Docs]`, `[Test]`, `[Config]`, etc.
    - `[P0/P1/P2]` priority
    - `[estimate]` (rough, but present)
  - Organize tasks into logical phases (DB -> API -> UI -> tests -> docs -> verification).
  - Group independent tasks by domain so parallel sub-agents can claim and execute non-overlapping tracks simultaneously.
- **Test plan (required)**
  - Automated: specific commands to run + what they cover
  - Manual: step-by-step checklist for the primary user flows
- **Documentation DoD + Audit plan**
  - Include doc/audit tasks whenever behavior/contracts/canonical surfaces are touched.
- **Review gate**: what must pass before sprint can close
- **Notes**: empty section for runtime decisions

### Phase 3: Update status documents (required)

After creating the sprint doc:

- Update `docs/sprints/CURRENT_STATUS.md`
  - `active_sprint`: path to the new sprint doc
  - `stage`: `planning` (initially)
  - Add/adjust priorities to reflect the new sprint
  - Add blockers if the sprint is waiting on plan approval or external dependencies
- Update `PROJECT_STATUS.md`
  - `last_updated`: today
  - `active_work`: reflect the new sprint name/topic

### Phase 4: Present the result

At the end, output:

1. The created sprint file path
2. The sprint goal + dates
3. Whether contract changes are expected and which plan(s) are linked
4. The initial stage (`planning`) and what must happen to move to `in_progress`
5. Next step: use `/start-sprint` to begin implementation

## Important notes

- This skill **creates the sprint plan**; it does not implement the sprint.
- Keep **stage consistent** everywhere (frontmatter + summary + `CURRENT_STATUS.md`).
- If contracts are expected to change, do not proceed to implementation until the plan approval gate is satisfied.
- Work plan tasks tagged by domain (`[DB]`, `[API]`, etc.) enable parallel sub-agent execution during `/start-sprint`.
