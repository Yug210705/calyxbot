# Calyx Code Style Guide

## Python Style Guide (Backend)

- **Formatter**: `ruff format` (100 character line limit).
- **Linter**: `ruff check`.
- **Typing**: Strict `mypy`. All functions and methods must have type annotations.
- **Docstrings**: Google style docstrings for classes, modules, and complex functions.
- **Imports**: Absolute imports preferred.

## TypeScript Style Guide (Frontend)

- **Formatter**: Prettier.
- **Linter**: ESLint with strict TypeScript rules.
- **Typing**: `any` is strictly prohibited. Avoid `unknown` where possible.
- **Components**: React Functional Components using standard `function` syntax over const arrow functions for top-level exports.

## Naming Conventions

- **Python Variables/Functions**: `snake_case`
- **Python Classes**: `PascalCase`
- **TypeScript Variables/Functions**: `camelCase`
- **TypeScript Types/Interfaces**: `PascalCase`
- **React Components**: `PascalCase`
- **Constants**: `UPPER_SNAKE_CASE`

## Folder Conventions

- Modules group related logic (`routes`, `services`, `schemas`).
- Test files mirror the `app` structure (`tests/modules/auth/test_services.py`).

## API Naming Conventions

- Endpoints are noun-based, lowercase, pluralized (e.g., `/users`, `/organizations`).
- Use HTTP methods appropriately (GET for read, POST for create, PUT/PATCH for update, DELETE for remove).
- Sub-resources use nested routes if tightly coupled (e.g., `/organizations/{id}/members`).

## Error Handling Standards

- **Backend**: Do not leak stack traces or internal implementation details. Raise custom exceptions extending `CalyxException` to automatically map to standard HTTP errors.
- **Frontend**: Catch errors explicitly, show user-friendly toasts, and report to observability tools.

## Logging Standards

- Use structured JSON logging (`structlog`).
- Every log entry during a request must contain `request_id`, `user_id` (if authenticated), and `org_id`.
- Never log PII, passwords, or tokens.

## Documentation Standards

- Architectural decisions go to `architecture/adr/`.
- Code comments should explain *why*, not *what*.
