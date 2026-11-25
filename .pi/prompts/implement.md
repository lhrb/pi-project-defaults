---
name: implement
description: Have builder deliver and verify one usable slice, then stop for review.
thinking: medium
argument-hint: "<plan-or-slice-file> [slice] | --direct <outcome>"
---

1. **Select and inspect.** If `$1` is `--direct`, use `${@:2}` as the outcome; no plan is required. Otherwise read `$1` and locate its `plan.md`. For a slice file, select it; for a plan, use `$2` or `Next`. The roadmap is context, not scope. Inspect code, conventions, dependencies, and required outcomes. If selection is ambiguous, blockers remain, or scope spans distinct review points, clarify or propose a split and stop. The request approves only the selected slice.
2. **Gate implementation.** For `Type: Experiment`, stop and give the exact `/experiment <plan-or-slice-file> [slice]` command. Check routine assumptions within scope. Plan a standalone probe only if a cheap answer would change what to build and building the slice cannot safely or practically answer it. When needed, record a `Type: Experiment` slice in `plan.md` with its question, decision, evidence, prerequisites, and safeguards. Mark dependent implementation Blocked. If ready, set `Next` to the experiment and give the exact command; otherwise say what's missing. Stop without running the standalone probe. When proceeding with implementation, mark In progress if there is a plan.
3. **Implement.** Have **builder** own the slice and its tests. Use test-first when requested; otherwise prefer it for known regressions or settled, high-risk guarantees. Use **test-writer** when independent test design adds value. When testing first, confirm failures reflect missing behavior, not setup, syntax, or unrelated problems. Never force failures for existing behavior.
4. **Verify.** Confirm builder tried the real workflow where applicable and ran relevant behavioral, regression, and applicable type, lint, build, integration, and contract checks. Use objective contract/schema checks for contract-only slices. Investigate failures and report unrelated baseline issues separately. Correct invalid tests with explanation; never weaken valid tests.
5. **Handle changes.** Let builder own internal design and routine UX. Escalate blockers, consequential ambiguity, changed guarantees, or discoveries invalidating the approach. Update the spec if present and affected tests before proceeding; do not silently redefine behavior.
6. **Complete.** In an existing plan, mark Done only when guarantees are verified and no attributable regressions remain. On Done, set `Review: <slice>: pending` and `Next: None`. Otherwise retain Blocked or In progress as appropriate.
7. **Report.** Record significant, non-obvious tradeoffs in the handoff; use `docs/features/<feature-name>/decisions.md` if they would obscure the plan. Update any plan with verification, gaps, and decision links. Use **doc-writer** if the handoff warrants it. Recommend a next direction without specifying or starting it.

**Review brief** (chat, even on early stops; also near the top of any plan for the selected slice):

- **Your call:** Exact decision or action, with a recommended reply; otherwise “No input needed.”
- **What happened:** Plain-language result. If blocked, say what failed, what it prevents, and who can unblock it.
- **See it:** One small example: how to try it, what to expect, and what you observed. Say if unverified.

**Stop. Never start another slice automatically.**
