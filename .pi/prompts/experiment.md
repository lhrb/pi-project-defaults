---
name: experiment
description: Answer one planned experiment question, record evidence, and stop for review.
thinking: medium
argument-hint: "<plan-or-slice-file> [slice]"
---

1. **Select.** Read `$1` and locate its `plan.md`. Select the supplied slice or, for a plan, use `$2` or `Next`. Run only a slice marked `Type: Experiment`. Stop and clarify ambiguous selection, unmet prerequisites, or an unclear question or decision. Mark In progress before probing.
2. **Probe.** State the question, the decision it informs, and what evidence would answer it. Prefer existing evidence or a safe no-code check. If code is needed, have **builder** create the smallest in-scope probe. Check prerequisites and safeguards, then seek direct evidence promptly. Use test-first only if it helps answer the question. Use **test-writer** for tests that provide useful evidence or protect guarantees worth keeping.
3. **Keep useful work.** Keep useful prototypes or MVPs rerunnable and consistent with existing architecture and safeguards. Verify affected guarantees without out-of-scope hardening. Remove temporary probe artifacts, instrumentation, and test data unless needed for reproduction. Document reusable work and verification gaps.
4. **Record and stop.** Write the review brief and record the question, reproduction steps, observations, conclusion, limitations, and cleanup or recovery in `plan.md`. Use **doc-writer** if the handoff warrants it. Keep direct evidence separate from prerequisite checks. Mark Done only with a conclusive answer, even a negative one, and no attributable regressions. On Done, set `Review: <slice>: pending` and `Next: None`. Otherwise keep In progress or Blocked and report what is needed. Keep dependent implementation blocked if its prerequisite was not established. Recommend the next direction without starting it.

**Review brief** (chat, even on early stops; also near the top of `plan.md` when a slice is selected):

- **Your call:** Exact decision or action, with a recommended reply; otherwise “No input needed.”
- **What happened:** Plain-language result. If blocked, say what failed, what it prevents, and who can unblock it.
- **See it:** One small example: how to try it, what to expect, and what you observed. Say if unverified.
