---
name: implement
description: Implement one planned feature test-first with test-writer and builder, then stop.
thinking: medium
argument-hint: "<feature-description-file>"
---

1. **Inspect.** Read `$1`, dependencies, conventions, and relevant code. Locate its `plan.md`. Verify dependencies are Done; never silently implement blockers. Set status to In progress.
2. **Specify tests.** Have **test-writer** add minimal, high-signal behavioral tests without changing implementation. For contract-only slices, use objective contract/schema checks.
3. **Establish baseline.** Run tests. Confirm failures represent missing behavior, not setup, syntax, or unrelated problems. If behavior already exists, verify meaningful coverage without forcing red. Report unrelated baseline failures separately.
4. **Implement.** Have **builder** implement only this slice without weakening valid tests or expanding scope. Document significant, non-obvious decisions and tradeoffs in `docs/features/<feature-name>/decisions.md`; omit routine choices. Keep entries as short as possible without loosing information or meaning.
5. **Verify.** Run relevant behavioral, regression, and applicable type, lint, build, integration, and contract checks. Investigate failures; distinguish baseline issues from regressions. Correct invalid tests through test-writer with explanation, never workarounds.
6. **Handle changes.** Escalate consequential ambiguity or changed guarantees. Update the spec and affected tests before proceeding. Do not silently redefine behavior.
7. **Complete.** Mark Done in `plan.md` only when guarantees are verified and no attributable regressions remain. Otherwise retain Blocked or In progress as appropriate. Update `Next` using satisfied dependencies.
8. **Report.** Briefly summarize guarantees, verification results, consequential decisions, and remaining gaps.

**Stop. Never start another slice automatically.**
