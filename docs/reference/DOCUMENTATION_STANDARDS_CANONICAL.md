---
doc_type: canonical_documentation_standards
status: canonical
created: 2026-03-12
last_updated: 2026-03-13
---

# Documentation Standards (Canonical)

This document defines the authoritative rules for creating, editing, and updating canonical documentation in this repository.

## 0. Purpose and Scope

These standards govern how canonical documentation is written, structured, updated, and validated so it remains:

- deterministic and consistent
- schema-aligned
- AI-readable and human-usable
- non-duplicative across document families

### 0.1 Scope (what these standards apply to)

These standards apply to documents that define or describe authoritative contracts and system behavior, including (as applicable):

- `docs/reference/**` (canonical reference docs)
- `docs/canonical/**` (canonical/spec docs if used)
- schema documents
- API contract documents
- database contract documents
- glossary/terminology documents

### 0.2 Non-scope (what these standards do not apply to)

These standards do not apply to operational/project-management documents, including:

- sprint docs (`docs/sprints/**`)
- audits (`docs/audits/**`)
- plans/change requests (`docs/plans/**`)
- FBS install guides/checklists and other operational instructions

Operational documents may be instructional. Canonical documents must follow the rules below.

---

## 1. Authoritative Writing Style

### 1.1 Declarative specification tone

Canonical documents state facts about the system and its contracts.

Allowed examples:
- “The system defines the configuration schema.”
- “The API accepts a request body containing …”

Disallowed examples:
- “Create a configuration schema.”
- “You should use this endpoint to …”

### 1.2 Prohibited recommendation/optionality language

Canonical documents do not use optionality or recommendation language for normative behavior.

Prohibited terms include:
- should, could, recommended, might, optional

Permitted replacements include:
- “The schema includes …”
- “The request body contains …”
- “The system enforces …”

### 1.3 No narrative or conversational tone

Canonical documents do not include conversational framing, subjective commentary, or informal voice.

---

## 2. Content Integrity Rules

### 2.1 Preserve existing wording

Existing canonical content remains unchanged unless explicitly updated by an authorized change process.

### 2.2 No cross-document leakage

Edits apply only to the document currently being drafted or updated. A change in one document does not imply edits to other documents unless explicitly requested.

### 2.3 Document scope preservation

Each document is limited to the domain defined by the documentation hierarchy. Documents do not duplicate deep content owned by other families.

---

## 3. Schema, Example, and Semantics Rules

### 3.1 Mandatory triple: Schema + Example + Semantics

Any section defining an operational structure includes:

1. **Schema** — canonical structure and field set
2. **Example** — valid, copy/paste-ready example that matches schema
3. **Semantics** — behavioral meaning, constraints, interpretation rules

### 3.2 Example correctness

Examples:

- match the schema exactly
- contain no invented fields
- use correct naming conventions (e.g., `snake_case` where required)
- include all required fields
- use valid syntax (valid JSON for JSON examples)

### 3.3 No silent field introduction

New fields, enumeration values, structures, endpoints, or behaviors are not introduced silently.

When a gap is identified that blocks correct drafting:

1. The gap is raised explicitly
2. Candidate additions are proposed (as proposals/change requests)
3. Explicit approval is obtained
4. The addition is applied only after approval

### 3.4 Usage example requirement (contextual)

Usage examples are required only when a section defines:

- API request/response bodies
- data structures
- database tables/constraints
- configuration schemas
- workflow objects

Examples are not required for purely conceptual overview sections.

---

## 4. Level of Detail Rules

### 4.1 Detail-level matrix

The appropriate detail level is determined by document family:

- APIs and schemas: very high detail (schemas + semantics + valid examples)
- database contracts: high detail (tables/constraints/relationships)
- UI/UX flows: medium detail (flows and screens, not re-defining schemas)
- overview docs: conceptual detail without redefining canonical fields

### 4.2 No over-specification

Canonical documents do not include irrelevant implementation details outside the family scope (e.g., internal code structure inside schema docs).

---

## 5. Controlled Invention Rules

### 5.1 Controlled suggestion rule

A candidate new field/behavior may be proposed only when a clear gap exists and the suggestion follows from existing canonical design.

### 5.2 No silent invention

No proposed field/behavior is added without explicit approval.

### 5.3 Approval scope

Approval applies to the active change being made, not to automatic propagation across documents.

---

## 6. Canonical Source Hierarchy

Canonical documents align to a precedence stack defined by the documentation hierarchy (see `docs/reference/DOCUMENTATION_HIERARCHY_CANONICAL.md`).

Rules:

- higher-precedence documents govern conflicts
- lower-precedence documents do not redefine higher-precedence structures
- ambiguities are resolved by referencing the canonical schema/contract document for the relevant object

---

## 7. Naming, Versioning, and Structure

### 7.1 File naming and versioning

If the repository uses versioned canonical docs:

- version identifiers are explicit in filenames or frontmatter
- additive changes use minor increments
- breaking changes use major increments

### 7.2 Heading structure

Documents preserve section structure and numbering rules defined by the documentation hierarchy.

### 7.3 One document per drafting context

A drafting/editing session edits one document at a time unless explicitly instructed otherwise.

---

## 8. Editing Rules (Precision)

### 8.1 Explicit target confirmation

Before editing, the editor confirms the target document and scope.

### 8.2 Minimal, targeted edits

Edits are small, localized replacements and do not rewrite unrelated content.

### 8.3 No structural rewrites without instruction

Large restructures require explicit direction.

---

## 9. Document Size and Modularity

### 9.1 Limits

- documents remain within reasonable size limits for maintainability
- large topics are split into separate documents by hierarchy boundaries

### 9.2 Splitting rule

When a document becomes large, it is split along hierarchy-defined boundaries rather than by arbitrary chunks.

---

## 10. Validation and Compliance

### 10.1 Per-section compliance

Each edited section is validated for:

- correct tone
- schema/example/semantics presence where required
- alignment to canonical sources
- no silent invention
- correct naming conventions

### 10.2 Completion requirements

After drafting or updating a canonical document, the editor provides:

- character count (or size estimate)
- compliance confirmation
- a minimal list of follow-up improvements (if any)

---

## 11. Non-normative notes

Non-normative notes are explicitly labeled and do not define behavior, schemas, or constraints.

