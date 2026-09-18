# ezCORE v1 Release Plan

> **Date:** 2026-09-18
> **Status:** Active — supersedes `ROADMAP.md` (stale pre-build draft) for v1 scope.
> **Goal:** a first public build an actual user can install, import their own
> dumps into, play, save, and update — on macOS first, then mobile.

Definition of v1 done: unsigned GitHub release for macOS (notarized if an
Apple identity is available) + published store listings or TestFlight/beta
tracks for iOS/Android **only if** their P1 gates clear; otherwise v1 is
explicitly "macOS + Windows/Linux desktop, mobile beta to follow."

## Where v1 stands (verified 2026-09-18, updated in place)

- Orbit console UI complete, no placeholders: full suite green (see CI),
  `analyze lib/` clean, banned-content scan green, live cheats / slots /
  vault / autosave / covers all wired.
- App builds: macOS debug (launch-verified, no crash), iOS release
  unsigned (19.5 MB `.app`), Android debug APK — all green.
- Core matrix: 17/18 macOS cores identify-or-better (3 render with
  fixtures); 9–10 iOS + 10 Android artifacts built (arch/platform/minos/
  symbols verified, boot pending device lab). See `docs/MATRIX.md`.
- Known red: `integration_test/player_flow_test.dart` still fails in the
  macOS sandbox for typed paths (bookmarks cover picker/imported paths;
  typed-path-in-sandbox remains honestly impossible).
- `native/cores/`, `runtime/build*/`, `native/src/`, `native/test-roms/`
  exist only on dev machines (gitignored). `scripts/release.sh` exists
  (macOS path executes once scummvm-macOS lands).

## Phase A — macOS actually works (P0)

1. **Sandboxed file access** — DONE (2026-09-18). System picker
   (`file_selector`, powerbox-native) + `BookmarkStore.swift` security-
   scoped bookmarks (`ezcore/files` channel) + `ScopedFiles` seam with
   passthrough elsewhere; player holds access across session open.
2. **Fresh-clone bootstrap** — SCRIPTS DONE, full nuke-verify pending
   (last gate before release: move `native/`+`runtime/build*` aside and
   run the documented chain to green).
3. **BIOS check + guidance** — DONE (`BiosCheck` service + player boot
   gate naming exact missing files + Systems dock row; the dead
   `biosStatus` map was removed instead of populated).
4. **SRAM / battery saves** — MECHANISM VERIFIED, no ABI change needed:
   cores self-manage SRAM through the `save_dir` handoff (already in the
   runtime); player now passes **per-game** SRAM dirs (shared dir would
   corrupt across games). Content-level round-trip pending a
   save-exercising ROM.
5. **Release packaging** — `scripts/release.sh` EXISTS (macOS/Windows/
   Linux/Android carry runtime+cores; iOS unsigned until a signing
   identity exists). Executes fully once scummvm-macOS completes the set.

## Phase B — desktop complete (P1)

6. **Windows + Linux builds** — CODE DONE, execution in CI. `dynload_win32.c`
   seam, ALSA + waveOut FFI sinks, XInput + evdev gamepads, Linux shell,
   shell branding normalized, 5-OS CI matrix written. This machine cannot
   execute foreign binaries; first green CI run is the gate.
7. **Desktop core updates** — DECIDED 2026-09-18: no download infrastructure
   in v1. Delivery is `bundled` (manifest data matches): cores ship inside
   the app bundle and update with app releases, hash-verified at staging.
   (iOS never downloads — stays bundled, App Review 2.5.2/4.7.)

## Phase C — mobile real (P1)

8. **Mobile foundations** — CODE DONE: `path_provider` dirs, pure-Dart
   SHA-256, system picker import, AudioTrack/AVAudioEngine sinks, staged
   vault + runtime loader + `ezcore/native` channels both sides.
9. **Device builds + iOS policy** — Binaries built locally (10 Android
   ELF, 9 iOS Mach-O, iOS runtime, unsigned `.app` + debug `.apk` all
   green). Boot-on-device pending a device lab. iOS policy enforced in
   data: tiers + manifest validation forbid dynarec; JIT-default cores
   excluded until interpreter flags are verified.
10. **Mobile input** — DONE in code (Android KeyEvent/motion, GCController
    both Apple platforms, XInput, evdev; canonical vocab + mapping +
    Settings status row). Physical-pad verification pending hardware.

## Phase D — product-complete (P2, post-v1 unless trivial)

- Cloud sync (spec in `CLOUD_SAVES.md`, marked P0 there — **recommend
  deferring to v1.1**: needs backend, auth, conflict policy, and a privacy
  review; local vault fully covers v1).
- Out-of-process crash isolation, rewind, per-game core options (ABI v2),
  netplay.
- Native hardening (small, could ride along): make `retro_cheat_*` symbols
  optional at load instead of failing cores without them.

## Explicitly out of v1

Commercial-game compatibility claims, RetroAchievements, libretro-database
cheat downloads (ship the comment fix only), Firebase/Stripe scaffolding
from the old roadmap draft.

## Decisions needed from you (* = blocking)

- Distribution: GitHub releases only, or also Mac App Store? (Store =
  stricter sandbox review + calendar time.)
- Apple Developer identity available for notarization / TestFlight? *
- Cloud sync in v1.1: build backend vs iCloud/Play-data vs drop?
- Android signing key + Play account owner?

## Risks

- Emulator cores are third-party code: a core update can break saves or
  perf; pinning + the matrix test mitigate, not eliminate.
- iOS JIT-less interpreter cores for late systems (N64/PSP-class) may be
  too slow on old phones — scope iOS system list by measurement, not hope.
- Legal posture depends on the holds staying holds and the provenance
  audit completing before any public binary.
