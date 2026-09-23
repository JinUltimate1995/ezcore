# ezCORE Known Issues

> Snapshot date: 2026-09-24
> This file records observed problems separately from the roadmap. Historical
> release checkpoints remain in [`../docs/IMPLEMENTATION_STATUS.md`](../docs/IMPLEMENTATION_STATUS.md).

## Open issues

### EZC-001 — Resolved: analyzer gate is clean

- **Description:** The earlier unused-import warning and timeout were observed
  while the theme files were still changing. The completed branch now passes
  `flutter analyze` with no issues.
- **Affected platform:** Flutter targets (source-level gate).
- **Affected core/system:** None; presentation/test files only.
- **Verification:** `flutter analyze` — **No issues found** (`111.8s`).
- **Status:** Resolved for the current checkout; CI/device coverage remains
  separate.

### EZC-002 — Resolved: full Flutter suite is green

- **Description:** The earlier full run reported 373 passed, 15 skipped, and
  10 failed while the theme files were changing. The completed branch now
  passes the complete suite.
- **Affected platform:** Flutter widget-test host; theme/layout code paths.
- **Affected core/system:** None.
- **Verification:** `flutter test --no-pub` — **393 passed, 15 skipped, 0
  failed**.
- **Status:** Resolved for the current checkout; skipped integration cases
  remain explicitly unverified rather than silently counted as gameplay.

### EZC-003 — App-level external-file acceptance is not re-verified

- **Description:** The historical macOS integration checkpoint reported that
  typed external paths could fail under the app sandbox before import/player
  acceptance. The repository now contains picker/bookmark seams, but the
  complete sandboxed import → play → save/load → reopen path has not been
  rerun in this audit.
- **Affected platform:** macOS app sandbox.
- **Affected core/system:** Any user-imported content.
- **Reproduction:** Run `integration_test/player_flow_test.dart` on a macOS
  build with the documented checkout define and a permitted file path.
- **Severity:** Medium/High for the user flow; not proven as a current
  regression.
- **Workaround:** Use the system picker and grant security-scoped access; do
  not bypass sandbox entitlements.
- **Status:** Needs re-verification.
- **Follow-up:** Platform acceptance task after the coordinated theme-track
  stabilization and integration review.

### EZC-004 — Native execution is not crash-isolated in the app

- **Description:** The Dart worker isolate owns a session, but native core code
  still runs in the application process. The C runtime also uses a
  process-global active-session pointer.
- **Affected platform:** All platforms.
- **Affected core/system:** Any native core; particularly GL-dependent cores.
- **Reproduction:** Load/run a core that crashes or exercise concurrent session
  ownership; do not use this as a routine test because a native crash can
  terminate the app/test process.
- **Severity:** Medium/High.
- **Workaround:** One owner per runtime process and fork-isolated native tests.
- **Status:** Known limitation; architectural follow-up required.

### EZC-005 — Battery-save content round trips are not fully verified

- **Description:** The player gives each game a separate SRAM directory and
  the runtime passes save/system directories to cores, but a save-exercising
  public-domain fixture and per-core round-trip evidence are incomplete.
- **Affected platform:** All platforms where a core uses SRAM.
- **Affected core/system:** Core-specific.
- **Reproduction:** Load permitted homebrew, make a persistent change, close,
  reopen with the same game directory, and compare the expected state.
- **Severity:** Medium.
- **Workaround:** Keep per-game directories; do not share one SRAM folder
  between games.
- **Status:** Open verification gap.

### EZC-006 — GL/default-renderer cores lack frame evidence

- **Description:** Several desktop cores identify or load but require a GL
  context or core options not supplied by the current runtime path.
- **Affected platform:** Desktop, especially Linux/macOS as listed in the
  canonical matrix.
- **Affected core/system:** Geometry1, RCP64, DualScreen, PortComp, DreamArc,
  and PowerCube may require renderer/core-option work.
- **Reproduction:** Attempt content boot without a suitable GL context or
  software-renderer configuration.
- **Severity:** Medium.
- **Workaround:** Use cores/paths already marked RENDERS in the matrix; do not
  infer gameplay from I/B status.
- **Status:** Blocked on renderer/options architecture and fixtures.

### EZC-007 — Platform and device verification is uneven

- **Description:** macOS has the strongest current run evidence. Linux app
  launch/build evidence exists, while Windows/iOS/Android execution and
  physical-controller/audio behavior require their own verification runs.
- **Affected platform:** Linux, Windows, Android, iOS, and hardware input.
- **Affected core/system:** Platform shell and device integrations.
- **Reproduction:** Follow the commands in `docs/BUILDING.md` and record the
  exact host/device and result.
- **Severity:** Medium.
- **Workaround:** Treat source presence and artifact inspection as
  implementation evidence only, not runtime compatibility.
- **Status:** Open platform verification queue.

### EZC-008 — Responsive policy needs an explicit tablet-portrait decision

- **Description:** `Layout.ofSize` currently maps every portrait viewport to
  `OrbitLayout.phonePortrait`, including an 834×1194 tablet-sized viewport.
  The new layout test explicitly expects that behavior, while the broader
  product direction calls out tablet responsiveness as a distinct target.
- **Affected platform:** Flutter UI on tablets and large phones.
- **Affected core/system:** None.
- **Reproduction:** Call `Layout.ofSize(const Size(834, 1194),
  Orientation.portrait)` and inspect the result.
- **Severity:** Medium — this is a product/UX policy ambiguity, not a proven
  user-facing defect.
- **Workaround:** None yet; preserve the current behavior until the maintainer
  and theme owner settle the breakpoint policy.
- **Status:** `[?]` Needs maintainer decision.
- **Follow-up:** Resolve before adding more layout-specific branches or
  treating the tablet layout as complete.

### EZC-009 — Theme-track diff has whitespace-only gate failures

- **Description:** The combined PR diff still reports new blank lines at EOF
  in `lib/main.dart` and `lib/services/system_labels.dart`. The working-tree
  diff is clean because these lines are already in the design commits, but
  `git diff 6c9af64..HEAD --check` is the relevant PR check.
- **Affected platform:** Repository quality gate.
- **Affected core/system:** None; theme/UI files.
- **Reproduction:** `git diff 6c9af64..HEAD --check`.
- **Severity:** Low, but it blocks a clean merge diff.
- **Workaround:** Do not hide the failure with a broad formatter rewrite; have
  the design owner remove the two extra blank lines in a focused cleanup.
- **Status:** Open; owned by the theme/UI track and must be resolved before
  merge.

### EZC-010 — Desktop/tablet Favorites chip does not apply its filter

- **Description:** In the theme redesign, the library strip's Favorites chip
  calls `_setFilter('Favorites')`, which sets `tab = 'all'`. The shared
  `filtered` predicate explicitly ignores `filter == 'Favorites'`, so desktop
  and tablet users can see the chip become inactive without the collection
  being filtered. The phone-portrait tab path is separate.
- **Affected platform:** Flutter desktop/tablet library layouts.
- **Affected core/system:** None.
- **Reproduction:** Open a library with at least one favorite and one
  non-favorite game, then activate the Favorites chip in the desktop/tablet
  strip.
- **Severity:** Medium — a visible navigation control does not apply its
  promised filter.
- **Workaround:** Use the phone-portrait Favorites tab, or filter through a
  different surface until the theme owner reconciles the two paths.
- **Status:** Open; identified during read-only integration review and owned
  by the theme/UI track.
- **Follow-up:** Add a regression test at desktop/tablet size, then choose one
  shared filter representation for both UI paths.

### EZC-011 — Tablet “Recently added” row renders the filtered collection

- **Description:** The theme redesign defines a `recentlyAdded` getter, but the
  tablet hub's `Recently added` section passes `games` (the current filtered
  list) to `_tileRow` instead of `recentlyAdded`. The section heading therefore
  does not necessarily describe its contents.
- **Affected platform:** Flutter tablet layout.
- **Affected core/system:** None.
- **Reproduction:** Open a tablet-sized library with a non-empty library and a
  system/search filter, then inspect the “Recently added” row.
- **Severity:** Medium — visible library metadata is misleading.
- **Workaround:** Clear filters or use the desktop/phone collection until the
  data path is reconciled.
- **Status:** Open; identified during read-only integration review and owned
  by the theme/UI track.
- **Follow-up:** Decide whether the section means import order or current
  filter results, then add a regression test matching that contract.

### EZC-012 — Theme helper splits paths only on `/`

- **Description:** The new `_systemNote` helper uses
  `g.filePath.split('/')`, which does not extract the filename from a native
  Windows path. A Windows library tile can therefore display a full path in
  its footnote.
- **Affected platform:** Windows Flutter UI.
- **Affected core/system:** None.
- **Reproduction:** Display a game whose `filePath` uses `\\` separators in a
  tablet/portrait tile.
- **Severity:** Low/Medium.
- **Workaround:** None needed for core execution; presentation is misleading.
- **Status:** Open; identified during read-only integration review and owned
  by the theme/UI track.
- **Follow-up:** Use platform-neutral path parsing or the existing path
  dependency without changing the persisted `GameEntry` format.

### EZC-013 — Dart formatter check differs on the design slice

- **Description:** Running the installed Dart formatter in check-only mode on
  the 17 Dart files changed by the Orbit design reports that 15 files would
  change. A repository-wide check reports additional legacy files, so a broad
  automatic rewrite would be unrelated churn.
- **Affected platform:** Flutter source formatting gate.
- **Affected core/system:** None; design-owned Dart files.
- **Reproduction:** Run `dart format --output=none --set-exit-if-changed` on
  the design file list from `git diff 6c9af64..HEAD --name-only`.
- **Severity:** Medium for a strict formatting gate; no analyzer or test
  failure was observed.
- **Workaround:** Review and format only the design slice, then rerun analyzer,
  tests, and the PR diff check; do not mass-reformat the repository.
- **Status:** Open; owned by the theme/UI track and must be resolved or
  explicitly waived before merge.

## Known limitations that are not defects

- No ROMs, BIOS, firmware, keys, or proprietary content are distributed.
- Cloud sync, accounts, telemetry, achievements, netplay, shaders, mods,
  theme packages, and a marketplace are not current features.
- Local save states are opaque core bytes; ezCORE does not guarantee that a
  state from one core version loads in another.
- The roadmap is a plan, not evidence of implementation.
