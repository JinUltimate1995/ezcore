# ezCORE Roadmap State

> Snapshot date: 2026-09-24
> Canonical roadmap: [`../ROADMAP.md`](../ROADMAP.md)
> Release evidence: [`../docs/MATRIX.md`](../docs/MATRIX.md)

## Current milestone

**M0 — Project control and baseline** — `[~] In Review`

The repository now has a long-term roadmap, state memory, a rebuilt public
README, and the completed Orbit redesign integrated on the feature branch.
The combined branch is ready for maintainer review, not automatic merge:
implementation tests are green on this host, while two PR-level whitespace
findings and a formatter discrepancy remain to be resolved by the design
owner. This project-control track did not edit the theme/UI implementation
files.

**Completed communication slice:** README rebuilt with the ezCORE mission,
current capabilities, dated progress stats, a Now → Next roadmap, technical
boundaries, build instructions, contribution guidance, and optional GitHub
Sponsorship support.

**Completed UI slice:** the Orbit shell now has desktop, tablet, phone-
landscape, and phone-portrait layouts, shared library state, an animated
backdrop with reduced-motion behavior, and permanent layout/backdrop tests.

## Why the next task is first

The latest combined read-only checks on 2026-09-24 observed:

- `flutter analyze`: **No issues found** (`111.8s`).
- `flutter test --no-pub`: **393 passed, 15 skipped, 0 failed**.
- `ctest --test-dir runtime/build-linux --output-on-failure`: **3/3 passed**.
- `git diff 6c9af64..HEAD --check`: reports two blank lines at EOF in
  `lib/main.dart` and `lib/services/system_labels.dart`.
- Dart formatter check on the 17 design Dart files reports that 15 would
  change under the installed SDK; no broad formatter rewrite was applied.

The code and test baseline is now stronger than the earlier theme-track
snapshot. Finish the PR-level cleanup and policy review before starting the
capability-contract milestone.

## Milestone order

| Order | Milestone | Status | Gate |
|---:|---|---|---|
| 0 | Project control and baseline | [~] In Review | Maintainer-approved combined PR with clean diff and recorded platform limits |
| 1 | Runtime and core contract | [~] Partially implemented | Capabilities, lifecycle, media, and config are explicit |
| 2 | Controller profiles | [ ] Planned | Hierarchical profiles and portable packages |
| 3 | Library and metadata | [~] Partially implemented | Provider-independent durable library model |
| 4 | BIOS/firmware | [~] Partially implemented | Complete manager and validation UX |
| 5 | Saves and portability | [~] Partially implemented | Migration, backup, and import/export tests |
| 6 | Themes and graphics | [ ] Planned | Installable theme/graphics packages |
| 7 | Shaders and mods | [?] Needs research | Safe renderer and mod package designs |
| 8 | Capture, diagnostics, achievements | [~] Partially implemented | Shared service seams without provider coupling |
| 9 | Netplay and ecosystem | [ ] Planned | Reviewed local-first package and transport designs |

## Current reality

- **Implemented foundation:** Flutter UI, C11 ABI v1, runtime lifecycle/AV/input/
  cheats/opaque states, worker-based player, local state, core catalog and
  pin verification, hybrid core delivery, import validation, BIOS presence
  guidance, local save vault, and platform input/audio seams.
- **Not implemented as a complete product:** capability discovery, full
  configuration hierarchy, metadata providers, controller profiles, theme or
  graphics packages, shaders, mods, achievements, netplay, recording/replay,
  centralized diagnostics, cloud sync, and most multi-disc/community workflows.
- **Verification is uneven:** macOS has the strongest evidence; Linux/Windows
  and mobile artifacts have different evidence; most cores identify or build
  but do not have verified gameplay. See the canonical matrix, not this
  summary, for per-platform claims.

## Next logical task

**Combined PR review and quality cleanup.** The maintainer should review the
Orbit diff, resolve the two whitespace findings and formatter discrepancy
without broad unrelated churn, and confirm the descriptive system-name wording
against the repository's trademark policy. No additional architecture task
should start until that handoff is clean.

## State-file maintenance rule

After each completed task, update:

1. [`CURRENT_TASK.md`](CURRENT_TASK.md) with the result and tests.
2. [`KNOWN_ISSUES.md`](KNOWN_ISSUES.md) with newly observed failures.
3. [`CORE_MATRIX.md`](CORE_MATRIX.md) when verification evidence changes.
4. [`ARCHITECTURE_STATE.md`](ARCHITECTURE_STATE.md) when implemented boundaries
   change.
5. The root [`ROADMAP.md`](../ROADMAP.md) status and next queue.

This file is development memory, not a substitute for code or tests.
