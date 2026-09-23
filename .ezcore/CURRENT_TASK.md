# ezCORE Current Task

## Active task record

- **Milestone:** Phase 0 — project control and public communication
- **Task:** Integrate the completed Orbit redesign with the brand-forward,
  evidence-backed public README and project state
- **Status:** PR candidate; implementation gates are green on this host,
  maintainer review and PR-level cleanup remain
- **Date:** 2026-09-24
- **Branch observed:** `feat/orbit-mockup-redesign`
- **Scope:** Orbit design commits, `README.md`, roadmap/documentation, and
  project-state memory; no ROMs, keys, or external core artifacts

## Objective

Make a first-time visitor understand what ezCORE is, why it is different, what
works today, how to obtain or build it, and how to help — without repeating
stale marketing claims or presenting roadmap items as shipped features.

## Editorial decisions

- Lead with a concise product identity: local-first, console-minded, and
  focused on Game → Play.
- Show momentum through a dated progress log, concrete foundation stats, and
  a Now → Next product roadmap.
- Put current capabilities and boundaries before architecture details without
  letting limitations dominate the first impression.
- Make download/build paths visible near the top.
- Keep the core catalog compact and link to the evidence-based matrix for
  per-platform detail.
- Describe Orbit with personality, without hype or invented compatibility.
- Include a direct, non-paywalled sponsorship path and concrete non-financial
  contribution paths.
- Preserve the project’s strict boundaries around ROMs, BIOS/firmware, keys,
  cheat databases, circumvention, trademarks, and held systems.

## Research basis

The structure was informed by public examples and official guidance, without
copying text or assets:

- GitHub’s README guidance: explain what the project does, why it is useful,
  how to get started, where to get help, and who maintains it.
- RetroArch: clear identity, screenshots, API explanation, support, and
  documentation links.
- mGBA: concise feature list, platform status, downloads, and build path.
- RetroPie: a short quick-start path with binaries and source clearly separated.
- Zed: concise installation/contribution sections and transparent sponsorship
  language.

## Acceptance criteria

- [x] README has a strong, human identity and clear navigation.
- [x] Current platform/core status is linked to canonical evidence.
- [x] Implemented capabilities are separated from planned work.
- [x] Build-from-source instructions remain usable.
- [x] Contribution rules and DCO expectations are visible.
- [x] Sponsorship is requested without a paywall or false perk promise.
- [x] License, core provenance, and content boundaries are clear.
- [x] Orbit implementation files were not edited by this project-control task;
  their completed design commits are integrated for combined review.

## Verification

- Local README link check: **passed**.
- `flutter analyze`: **No issues found** (`111.8s`).
- `flutter test --no-pub`: **393 passed, 15 skipped, 0 failed**.
- `ctest --test-dir runtime/build-linux --output-on-failure`: **3/3 passed**.
- `git diff 6c9af64..HEAD --check`: **not clean**; two theme-owned blank lines
  at EOF remain in `lib/main.dart` and `lib/services/system_labels.dart`.
- Dart formatter check on the 17 design Dart files: **not clean**; 15 files
  would be reformatted by the installed SDK. No broad rewrite was applied.
- Platform/device claims remain bounded by [`../docs/MATRIX.md`](../docs/MATRIX.md);
  this host did not verify every target.

## Coordination

The theme/UI track's implementation is committed in the feature branch. This
project-control task did not edit those files. The combined branch now needs
maintainer review of the PR-level cleanup findings and the descriptive
system-name wording before merge.

## Completion record

The README was rebuilt around the product vision and current implementation.
It now foregrounds the strongest differentiators—Game → Play, a premium
console-like Orbit surface, local-first ownership, a growing modular core
system, Time Capsule saves, and a clear “one emulator to play it all” north
star—then backs them with progress stats, a Now → Next roadmap, technical
boundaries, build instructions, contribution paths, and sponsorship. Future
themes, shaders, mods, metadata providers, achievements, netplay, and cloud
features are presented as the next chapters rather than as a wall of caveats.

The core catalog now pairs every ezCORE codename with the recognizable system
name it serves, while keeping upstream attribution and trademark boundaries
explicit.

## Next logical task

**Maintainer review and PR cleanup.** Resolve the two whitespace findings and
formatter discrepancy with the design owner, review the compatibility-name
wording against the repository policy, and approve the combined PR. After that,
the next architecture milestone is capability-contract research described in
[`../ROADMAP.md`](../ROADMAP.md).

## Previous handoff

The earlier project-control task created the root roadmap, `.ezcore/` state
memory, documentation cross-references, and conservative platform/core status
tracking. Those files remain the source of development memory.
