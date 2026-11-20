---
name: implement
description: Implement one selected slice with test-writer and builder, verify it, then stop for review.
thinking: medium
argument-hint: "<plan-or-slice-file> [slice]"
---

1. **Select and inspect.** Read `$1` and locate its `plan.md`. For a slice file, select it; for a plan, use `$2` or `Next`. The roadmap is context, not scope. Inspect code, conventions, dependencies, and required outcomes. If selection is ambiguous, blockers remain, or scope spans distinct review points, clarify or propose a split and stop. The request approves only the selected slice.
2. **Gate implementation.** For `Type: Experiment`, stop and point to `/experiment`. If an unverified assumption could invalidate the approach, stop and propose the smallest probe without running it. Otherwise mark In progress.
3. **Specify tests.** Have **test-writer** add minimal, high-signal behavioral tests without changing implementation. For contract-only slices, use objective contract/schema checks.
4. **Establish baseline.** Run tests. Confirm failures represent missing behavior, not setup, syntax, or unrelated problems. If behavior already exists, verify meaningful coverage without forcing red. Report unrelated baseline failures separately.
5. **Implement.** Have **builder** implement only this slice without weakening valid tests or expanding scope. Document significant, non-obvious decisions and tradeoffs in `docs/features/<feature-name>/decisions.md`; omit routine choices. Keep entries brief without losing meaning.
6. **Verify.** Run relevant behavioral, regression, and applicable type, lint, build, integration, and contract checks. Investigate failures; distinguish baseline issues from regressions. Correct invalid tests through test-writer with explanation, never workarounds.
7. **Handle changes.** Let builder own internal design and routine UX. Escalate blockers, consequential ambiguity, changed guarantees, or discoveries invalidating the approach. Update the spec and affected tests before proceeding; do not silently redefine behavior.
8. **Complete.** Mark Done in `plan.md` only when guarantees are verified and no attributable regressions remain; set `Review: <slice>: pending` and `Next: None`. Otherwise retain Blocked or In progress as appropriate.
9. **Report.** Briefly state what the requester can try and how, verification results, consequential decisions, and gaps. Recommend a next direction without specifying or starting it; review feedback informs the next planning pass.

**Stop. Never start another slice automatically.**
