# Pi project defaults

**Specify the guarantees. Delegate the mechanics.**

Opinionated architecture and [Pi](https://pi.dev) instructions for AI-assisted projects—not an application scaffold, framework, or fixed stack.

Distilled from [Lukas’s](https://github.com/lhrb) AI-assisted projects for fast feedback without sacrificing architectural judgment. README: AI-generated.

## Approach

Favor a working first version over exhaustive specifications. Humans own outcomes, consequential constraints, product policy, security, privacy, data lifecycle, and public compatibility. Agents choose internal implementation and routine UX defaults; revise defaults when results fall short.

Develop bottom-up: grow structure with demonstrated needs, not unbounded generation.

## Defaults

| File | Purpose |
|---|---|
| [`architecture.md`](architecture.md) | Feature-first, hexagonal boundaries; portable domain, explicit mappings, inward dependencies. No unnecessary layers or files. |
| [`AGENTS.md`](AGENTS.md) | Load architecture guidance; focused work, concise communication. |
| [`.pi/agents/builder.md`](.pi/agents/builder.md) | Own internal design and routine UX; implement, review, verify; preserve valid guarantees. |
| [`.pi/agents/test-writer.md`](.pi/agents/test-writer.md) | Minimal behavioral—not implementation—tests; signal over coverage counts. |
| [`.pi/skills/plan-feature/`](.pi/skills/plan-feature/SKILL.md) | Clarify consequential questions; plan minimal, independently verifiable slices without prescribing implementation. |
| [`.pi/prompts/implement.md`](.pi/prompts/implement.md) | Coordinate test-first implementation of one slice, then stop. |
| [`.pi/settings.json`](.pi/settings.json) | Load the required subagent extension. |

## Setup

1. Select GitHub’s **Use this template**, or run `./template/copy.sh existing-project/` from the template’s parent directory. Copying requires an existing destination and refuses file/directory conflicts; merge existing configuration manually. It includes `architecture.md`, `AGENTS.md`, and maintained `.pi/` configuration—not local dependencies, README, or itself. For a new project:

   ```sh
   mkdir new-repo-name
   ./template/copy.sh new-repo-name/
   ```

2. Install Pi and configure a model provider. Set `model` in both agent files or remove it to inherit the parent model. Defaults reflect Lukas’s setup.
3. Run `pi` from the project root. Review instructions and package declarations before granting project trust. Pi then installs configured [`@gotgenes/pi-subagents`](https://www.npmjs.com/package/@gotgenes/pi-subagents). Use `/reload` after edits.

## Workflow

**Small task:** describe the outcome and request `builder`; omit planning artifacts that add no value.

**Larger feature:**

```text
/skill:feature-planner <desired outcome and constraints>
/implement docs/features/<feature-name>/<slice-name>.md
```

1. Review generated `plan.md`, guarantees, assumptions, and blockers. Resolve consequential questions before implementation.
2. `test-writer` adds behavioral tests. Failures must reflect missing behavior; never force failures for existing behavior.
3. `builder` implements the slice. Run relevant regression, type, lint, build, integration, and contract checks.
4. Record significant decisions in `decisions.md`. Mark Done only after verification without attributable regressions.
5. Inspect and refine the result. Explicitly start the next ready slice.

Instructions neither enforce permissions nor guarantee correctness. Human review remains necessary.
