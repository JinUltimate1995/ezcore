# ezCORE Current Task

## Active task record

- **Milestone:** Phase 0 — project control and public communication
- **Task:** Integrate the completed Orbit redesign with the brand-forward,
  evidence-backed public README and project state
- **Status:** PR ready for maintainer review and merge after the final push
- **Date:** 2026-09-24
- **Branch observed:** `feat/orbit-mockup-redesign`
- **Scope:** Orbit design commits, responsive behavior fixes, animated backdrop,
  sanitized README previews, roadmap/documentation, and project-state memory;
  no ROMs, keys, or external core artifacts

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
- [x] The earlier documentation-only slice did not edit the theme
  implementation; this explicitly approved UI cleanup now includes focused
  behavior, renderer, animation, and regression-test fixes.
- [x] Favorites, Recently added, and Windows path display have regression
  coverage and corrected shared-library behavior.
- [x] The Linux-rendered backdrop avoids the pale-wash failure and includes
  animated ORBIT edge lights, orbital signals, stars, and meteors.
- [x] README imagery is captured from the real Linux shell using only a
  temporary SameBoy test ROM and local save data outside the repository.

## Verification

- Local README link check: **passed**.
- `flutter analyze`: **No issues found** (`61.0s`).
- `flutter test --no-pub`: **396 passed, 15 skipped, 0 failed**.
- `ctest --test-dir runtime/build-linux --output-on-failure`: **3/3 passed**.
- `flutter build linux --debug`: **passed**; stale CMake output was moved aside
  before the clean rebuild.
- `flutter build apk --debug`: **passed**; device boot remains unverified.
- Focused Dart formatter check on the design slice: **0 changed**.
- Linux debug app capture: **passed**; the background was visually reviewed and
  a second capture differed over time, confirming motion.
- Platform/device claims remain bounded by [`../docs/MATRIX.md`](../docs/MATRIX.md);
  this host did not verify every target.

## Coordination

The original documentation-only slice did not edit the theme implementation.
This follow-up was explicitly authorized to fix and verify the completed UI
work, so the branch now contains focused implementation and regression-test
changes alongside the design commits. The combined branch is ready for
maintainer review of the descriptive system-name wording and final PR diff.

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

**Maintainer review and merge.** Confirm the descriptive compatibility-name
wording against the repository policy, review the final diff, and merge PR #25
when the branch checks remain green. After that, the next architecture
milestone is capability-contract research described in
[`../ROADMAP.md`](../ROADMAP.md).

## Previous handoff

The earlier project-control task created the root roadmap, `.ezcore/` state
memory, documentation cross-references, and conservative platform/core status
tracking. Those files remain the source of development memory.
