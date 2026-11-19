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

1. Select GitHub’s **Use this template**, or install from a local template checkout with Python 3.8+:

   ```sh
   mkdir new-repo-name
   ./template/install.sh new-repo-name/
   ```

   `install.sh` requires an existing project directory. It copies missing defaults, adopts matching files, and reports differences without overwriting them. Run it for existing projects too, including those created with GitHub or `copy.sh`. Use `copy.sh` for a one-off copy without registration.

2. Install Pi and configure a model provider. Set `model` in both agent files or remove it to inherit the parent model. Defaults reflect Lukas’s setup.
3. Run `pi` from the project root. Review instructions and package declarations before granting project trust. Pi then installs configured [`@gotgenes/pi-subagents`](https://www.npmjs.com/package/@gotgenes/pi-subagents). Use `/reload` after edits.

## Sync projects

After testing a change in a project, copy it back to this template. Run these commands from the template directory:

```sh
./update.sh                                    # Sync agents, prompts, and skills; skip local changes
./update.sh --overwrite AGENTS.md architecture.md  # Replace only these files
./update.sh --overwrite --all                   # Replace all managed files
```

The template keeps absolute project paths and last-synced file hashes in its local, gitignored `.template-installs.json`. Missing or moved projects are reported without blocking other projects. Register a moved project at its new path with `install.sh`.

By default, `update.sh` syncs only files under `.pi/agents/`, `.pi/prompts/`, and `.pi/skills/`. It reports local edits and deletions but still syncs the remaining files across all registered projects. It leaves `AGENTS.md`, `architecture.md`, and `.pi/settings.json` alone.

`--overwrite` replaces local edits and restores local deletions across all registered projects. Pass exact template-relative file paths or `--all` to include every managed default. Sync never deletes project files or replaces symlinks or directories. Install and update return a nonzero status if they skip a conflict, even if other files synced successfully.

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
