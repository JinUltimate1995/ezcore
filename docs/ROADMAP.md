# ezCore Development Roadmap

> **Version:** 1.0
> **Date:** 2026-09-16
> **Status:** Draft

---

## Overview

ezCore development is divided into 7 phases over 36 weeks (9 months). Each phase has clear deliverables and exit criteria.

---

## Phase 0: Foundation (Weeks 1-4)

**Goal:** Project skeleton, build system, basic runtime

### Tasks

- [ ] Set up CMake build system (all 5 platforms)
- [ ] Create C++ runtime skeleton (session lifecycle, dlopen)
- [ ] Create Flutter project with basic navigation
- [ ] Implement C ABI (ezcore_runtime.h)
- [ ] Set up CI/CD (GitHub Actions)
- [ ] Write all MD files (this plan + specs)
- [ ] Set up Firebase project (auth, firestore, storage)
- [ ] Set up Stripe account

### Deliverable

Build system works, empty runtime loads, Flutter app launches

### Exit Criteria

- [x] `cmake --build` succeeds on Windows, macOS, Linux
- [ ] `flutter build` succeeds on all platforms
- [ ] Runtime compiles to .so/.dylib/.dll
- [ ] Flutter FFI bindings load the runtime
- [ ] CI/CD pipeline runs on every commit

---

## Phase 1: Core Runtime (Weeks 5-10)

**Goal:** Working emulator with one core

### Tasks

- [ ] Port runtime.c to C++ (session, AV, input, saves)
- [ ] Integrate first core (Mesen — NES)
- [ ] Basic Flutter UI (game list, player screen)
- [ ] Save states (local)
- [ ] Basic settings
- [ ] Frame timing and audio sync
- [ ] Performance profiling and optimization

### Deliverable

Play NES games with save states

### Exit Criteria

- [ ] Mesen core loads and runs on all desktop platforms
- [ ] Save states create and restore correctly
- [ ] Audio plays without glitches
- [ ] 60 FPS maintained during gameplay
- [ ] Basic UI navigates between list and player

---

## Phase 2: Multi-Core (Weeks 11-16)

**Goal:** Support 6+ systems

### Tasks

- [ ] Add cores: Snes9x, mGBA, Genesis Plus GX
- [ ] Add cores: Mupen64Plus, PCSX-ReARMed
- [ ] Core download system
- [ ] Core registry and manifest validation
- [ ] Auto-detect compatible core
- [ ] Settings per-game
- [ ] Android build and test
- [ ] iOS build and test (interpreter-only)

### Deliverable

Play 6 systems with automatic core management

### Exit Criteria

- [ ] All 6 cores load and run on desktop
- [ ] Core download and verification works
- [ ] Auto-detect compatible core for each game
- [ ] Android build runs (emulator or device)
- [ ] iOS build runs (simulator)

---

## Phase 3: Cloud & Automation (Weeks 17-22)

**Goal:** Cloud saves, auto scan, auto cheats

### Tasks

- [ ] Firebase integration
- [ ] User authentication (email + OAuth)
- [ ] Cloud save sync (upload/download)
- [ ] Conflict resolution (last-write-wins)
- [ ] Offline queue
- [ ] Auto scan (ROM identification via No-Intro hash)
- [ ] Metadata fetching (ScreenScraper.fr)
- [ ] Auto cheats (libretro built-in database)
- [ ] Cheat UI (toggle, import, export)

### Deliverable

Cloud saves work, auto scan identifies games, cheats are one-tap

### Exit Criteria

- [ ] Save on Windows → load on macOS successfully
- [ ] Scan 100% of test ROMs correctly
- [ ] Cheats load and apply for all supported cores
- [ ] Offline mode works correctly (queue and sync)

---

## Phase 4: 3D UI & Polish (Weeks 23-28)

**Goal:** Beautiful, fun, polished UI

### Tasks

- [ ] 3D game shelf (parallax depth)
- [ ] 3D box art rotation (drag to inspect)
- [ ] 3D screen transitions
- [ ] Controller support (auto-map)
- [ ] Touch controls (mobile overlay)
- [ ] Shaders (CRT, Scanline, Pixel Perfect)
- [ ] Themes (Ink, Porcelain, Retro Neon)
- [ ] Animations (scroll, press, transition)
- [ ] Haptic feedback
- [ ] Performance optimization (60 FPS UI)
- [ ] Bug fixes and polish

### Deliverable

UI that looks and feels like a premium product

### Exit Criteria

- [ ] 3D shelf renders at 60 FPS on all platforms
- [ ] Controller auto-maps for Xbox, PlayStation, Switch Pro
- [ ] Touch controls work on Android and iOS
- [ ] All shaders render correctly
- [ ] UI passes design review (no rough edges)

---

## Phase 5: Monetization (Weeks 29-32)

**Goal:** Pro tier, payments, in-game items

### Tasks

- [ ] Stripe integration (desktop)
- [ ] In-app purchases (mobile)
- [ ] Account system (email/password + OAuth)
- [ ] Pro badge and profile
- [ ] Skin store (browse, purchase, apply)
- [ ] Upgrade flow (free → Pro)
- [ ] Payment success/failure handling
- [ ] Receipt validation
- [ ] Subscription management (cancel, renew)

### Deliverable

Free and Pro tiers working, payments processing

### Exit Criteria

- [ ] Stripe checkout completes successfully
- [ ] In-app purchases complete on App Store / Play Store
- [ ] Pro features unlock immediately after payment
- [ ] Account syncs across devices
- [ ] Refund flow works correctly

---

## Phase 6: Launch (Weeks 33-36)

**Goal:** Public release

### Tasks

- [ ] Closed beta (invite-only, 100 users)
- [ ] Open beta (public, 1000 users)
- [ ] Bug fixes from beta feedback
- [ ] Performance optimization
- [ ] Documentation (user guide, developer guide)
- [ ] Marketing (website, social media, trailers)
- [ ] Launch on itch.io / GitHub
- [ ] Submit to App Store / Play Store
- [ ] Launch day monitoring

### Deliverable

Public launch

### Exit Criteria

- [ ] Beta feedback addressed (top 20 issues fixed)
- [ ] App Store / Play Store approved
- [ ] Website live with download links
- [ ] Social media accounts active
- [ ] Launch day zero critical bugs

---

## Timeline Summary

| Phase | Weeks | Duration | Key Milestone |
|---|---|---|---|
| 0: Foundation | 1-4 | 4 weeks | Build system works |
| 1: Core Runtime | 5-10 | 6 weeks | Play NES games |
| 2: Multi-Core | 11-16 | 6 weeks | 6 systems supported |
| 3: Cloud & Automation | 17-22 | 6 weeks | Cloud saves live |
| 4: 3D UI & Polish | 23-28 | 6 weeks | Premium UI |
| 5: Monetization | 29-32 | 4 weeks | Pro tier live |
| 6: Launch | 33-36 | 4 weeks | Public release |
| **Total** | **1-36** | **36 weeks** | **Launch** |

---

## Dependencies

```
Phase 0 ──▶ Phase 1 ──▶ Phase 2 ──▶ Phase 3 ──▶ Phase 4 ──▶ Phase 5 ──▶ Phase 6
```

Each phase depends on the previous. No parallel execution.

---

## Risks & Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Core build failures | High | Start with 1 core, verify before adding more |
| Firebase/Stripe integration delays | Medium | Use mock services in dev, integrate early |
| 3D performance issues | Medium | Profile early, optimize hot paths |
| App Store rejection | High | Follow guidelines, submit early for review |
| Scope creep | Medium | Stick to spec, defer non-essential features |
| Burnout | Medium | Take breaks, celebrate milestones |

---

## Success Metrics

| Metric | Target |
|---|---|
| Monthly active users (MAU) | 10,000 by month 12 |
| Pro conversion rate | 5-10% |
| Core support | 20+ systems by month 12 |
| App Store rating | 4.5+ stars |
| GitHub stars | 5,000+ |
| Discord members | 2,000+ |
