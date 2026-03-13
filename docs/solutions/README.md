# Solutions Library

Solved problem records with prevention steps. Created via `/compound`.

## Categories

Organize solutions into category subdirectories:
- `build-errors/`
- `test-failures/`
- `runtime-errors/`
- `performance/`
- `database/`
- `security/`
- `ui/`
- `integrations/`
- `other/`

## Anti-staleness Rules

- Every solution must include `last_verified`, a fix reference, and a prevention step.
- Solutions that are no longer valid should be marked `status: deprecated`.
- Solutions that evolve into reusable procedures should become skills (set `superseded_by`).
