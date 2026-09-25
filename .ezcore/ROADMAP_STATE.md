# ezCORE Roadmap State

> Snapshot date: 2026-09-25
> Canonical roadmap: [`../ROADMAP.md`](../ROADMAP.md)
> Release evidence: [`../docs/MATRIX.md`](../docs/MATRIX.md)

## Current milestone

**M0 — Project control and baseline** — `[~] In Review`

The replacement stack now has a long-term roadmap, state memory, a rebuilt
public README, real Linux UI captures, and the completed Orbit redesign split
across two signed branches. The base branch contains the artwork/provenance
and compact-shell evidence repair; the child branch adds the cover-flow
lifecycle, input, accessibility, and responsive hardening. The stack is ready
for independent review and sequential merge. Platform/device limits remain
explicitly recorded.

**Completed communication slice:** README rebuilt with the ezCORE mission,
current capabilities, dated progress stats, a Now → Next roadmap, technical
boundaries, build instructions, contribution guidance, and optional GitHub
Sponsorship support.

**Completed UI slice:** the Orbit shell now has desktop, tablet landscape,
tablet portrait, phone-landscape, and phone-portrait layouts. Desktop and phone
use the cover flow; both tablet orientations retain the focused
Continue/Recently Added hub. Shared library state, reduced-motion behavior,
compact-shell protections, and permanent layout/backdrop tests are included.

## Why the next task is first

The latest checks on 2026-09-25 observed:

- `flutter analyze`: **No issues found** (`18.3s`).
- `flutter test --no-pub`: **440 passed, 15 skipped, 0 failed**.
- `ctest --test-dir runtime/build-linux --output-on-failure`: **3/3 passed**.
- `flutter build linux --debug`: **passed**.
- `flutter build apk --debug`: **passed**; device boot remains unverified.
- Focused formatter checks: **0 changed** for the repaired files; the existing
  `player_screen.dart` formatting debt is outside this slice.
- Manifest, license, artwork provenance, WebP decode, banned-content, and
  whitespace gates: **passed**.
- Linux debug captures: desktop Library/Systems/Capsule/Settings and an
  834×700 tablet hub were visually reviewed; temporary ROM/save data stayed
  outside the repository.

The code and evidence baseline is ready for independent review. Finish the
maintainer review and sequential merge before starting the capability-contract
milestone.

## Milestone order

| Order | Milestone | Status | Gate |
|---:|---|---|---|
| 0 | Project control and baseline | [~] In Review | Maintainer-approved sequential replacement PRs with clean diff and recorded platform limits |
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

**Independent review and sequential merge.** Review the base artwork/evidence
commit range, then the child cover-flow commits, confirm the recorded platform
limits and provenance statement, obtain maintainer approval, and merge the
replacement PRs in order. No additional architecture task should start until
that handoff is clean.

## State-file maintenance rule

After each completed task, update:

1. [`CURRENT_TASK.md`](CURRENT_TASK.md) with the result and tests.
2. [`KNOWN_ISSUES.md`](KNOWN_ISSUES.md) with newly observed failures.
3. [`CORE_MATRIX.md`](CORE_MATRIX.md) when verification evidence changes.
4. [`ARCHITECTURE_STATE.md`](ARCHITECTURE_STATE.md) when implemented boundaries
   change.
5. The root [`ROADMAP.md`](../ROADMAP.md) status and next queue.

This file is development memory, not a substitute for code or tests.
