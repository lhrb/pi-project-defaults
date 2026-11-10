# Architecture Guidelines

## Principles

- **Feature-first:** Vertical slices organized by business capability.
- **Hexagonal:** Dependencies point inward (`Adapters → Domain`).
- **Portable:** Domain is independent of infrastructure, transport, and frameworks.
- **Consistent:** Predictable structure and naming across languages.
- **Minimal:** Flat structure, no unnecessary abstractions.

## Structure

```text
features/<feature>/
├── domain/
│   ├── <Action>Command
│   ├── <Action>Result
│   ├── <Action>Error
│   ├── <Action>UseCase
│   └── ports/<Responsibility>Port
├── adapters/
│   ├── inbound/<transport>/
│   │   ├── <Action>Handler
│   │   ├── <Action>RequestDto
│   │   ├── <Action>ResponseDto
│   │   └── <Action>Mapper
│   └── outbound/<responsibility>/
│       ├── <Entity>DbModel
│       ├── <Entity>Mapper
│       └── <Implementation>
└── <Feature>Module
```

Omit unnecessary files and directories. Use language-specific syntax and extensions while preserving naming conventions.

## Responsibilities

- **Domain:** Commands (input), Results (output), Errors (expected business failures), UseCases (logic and orchestration), Ports (external capability interfaces), and optional entities, value objects, and policies.
- **Inbound adapters:** Request handling, transport validation, DTO mapping, and response mapping.
- **Outbound adapters:** Port implementations, external models, and integration mapping.
- **Feature module:** Dependency wiring and feature registration.

## Data Flow

```text
Request
  → Inbound (validate, DTO → Command)
  → UseCase → Port
  → Outbound (Domain ↔ External Model)
  → External System
  → Result
  → Inbound (Result → Response DTO)
  → Response
```

- Ports use domain-owned types; use cases access external systems only through ports.
- Adapters own mapping at their boundaries.
- Prefer explicit conversions: `toCommand()`, `toResponseDto()`, `toDomain()`, `toDbModel()`.
- Use extension functions where supported; skip mapper files for trivial conversions.

## Rules

**Validation**
- Inbound validates transport syntax, structure, and format.
- Domain independently enforces business invariants.

**Errors**
- Domain defines expected business failures.
- Inbound maps business errors to transport responses.
- Outbound handles infrastructure failures without leaking implementation details.
- Keep unexpected failures separate from business errors.

**Boundaries**
- No infrastructure, framework, transport DTO, or database model dependencies in domain.
- No direct dependencies on other features' internals.
- Reuse shared infrastructure; extract shared domain concepts only when justified.

**Testing**
- Mirror feature structure in tests.
- Test use cases with fake or mocked ports.
- Test inbound validation/mapping and outbound integrations/mapping.
- Prefer behavioral over implementation tests.

## Adding a Feature

1. Define `Command`, `Result`, `Error`, `UseCase`.
2. Define required ports.
3. Implement inbound and outbound adapters with mappings.
4. Wire dependencies in `<Feature>Module`.
5. Add boundary-focused tests.

**Goal:** Every file has an obvious location, responsibility, and dependency direction without repository-wide context.
