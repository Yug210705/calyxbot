# Contributing to Calyx

Welcome to the Calyx engineering team. We value clean architecture, maintainability, and production-quality code.

## Branch Strategy

- `main`: Production-ready code. Protected branch.
- `feat/ticket-id-description`: For new features (e.g., `feat/BF-001-init-fastapi`).
- `fix/ticket-id-description`: For bug fixes.
- `chore/description`: For maintenance, dependency updates, and refactoring.

## Pull Request Process

1. Create a PR against `main` using the provided template.
2. Ensure all CI checks (lint, format, test, type check) pass.
3. Request review from at least one Staff Engineer or Code Owner.
4. Address feedback promptly.
5. Squash and merge into `main` using Conventional Commits for the final commit message.

## Code Review Checklist

- [ ] Does this follow the architecture outlined in `architecture/`?
- [ ] Is it covered by unit/integration tests?
- [ ] Are edge cases handled gracefully?
- [ ] Are errors structured and typed?
- [ ] Does this impact scalability or security?

## Definition of Done

A ticket is considered "Done" when:
1. The implementation fulfills all Acceptance Criteria.
2. The code adheres to `CODE_STYLE.md`.
3. Unit and integration tests are written and passing.
4. Relevant documentation (API docs, README, Architecture) is updated.
5. The Staff Engineer review identifies no critical security, performance, or maintainability concerns.

## Commit Message Convention

We follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat(auth): add google oauth flow`
- `fix(db): correct connection pool timeout`
- `docs(api): update swagger schemas`
- `chore(deps): update pydantic to v2.6`
- `test(core): add coverage for config loader`

## Testing Requirements

- **Backend**: `pytest` coverage must remain > 90%. Every endpoint requires a happy-path and error-path test.
- **Frontend**: Vitest + React Testing Library. Core user flows must be tested.
