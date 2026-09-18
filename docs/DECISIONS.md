# Architecture Decision Records

> Every significant decision is logged here with context, options considered, and rationale.
>
> **Note (2026-09-19):** this log started as a planning document. Where a
> decision was later reversed, the ADR carries a **Superseded** status line —
> the current state of the project lives in [`ARCHITECTURE.md`](ARCHITECTURE.md)
> and [`RELEASE_PLAN.md`](RELEASE_PLAN.md).

---

## ADR-001: Runtime Language — C++

**Date:** 2026-09-16
**Status:** ~~Accepted~~ **Superseded** — the runtime shipped as **C11**
(`runtime/src/runtime.c`); no C++ migration happened, and the C ABI boundary
turned out to be all that mattered. See `ARCHITECTURE.md`.

### Context

ezCore needs a runtime layer between the Flutter UI and the libretro cores. The runtime owns session lifecycle, AV plumbing, input, saves, cheats, and cloud sync bridging. The choice of language affects performance, safety, cross-platform support, and long-term maintainability.

### Options Considered

| Option | Pros | Cons |
|---|---|---|
| **C** | Zero ABI friction, trivial FFI, already working | Manual memory management, no bounds checking, security surface |
| **Rust** | Memory safety, fearless concurrency, modern tooling | Learning curve, slower build times, smaller ecosystem |
| **C++** | Direct libretro compatibility, RAII, mature tooling, performance | Still memory-unsafe (but better than C), build complexity |

### Decision

**C++** for the runtime layer.

### Rationale

1. **Direct libretro compatibility** — cores are C/C++, no translation layer needed
2. **Performance** — zero overhead for frame/audio processing, no GC pauses
3. **Cross-platform** — one codebase compiles to Windows, macOS, Linux, Android, iOS
4. **Mature tooling** — CMake, Conan/vcpkg, established patterns for emulator development
5. **Memory control** — RAII, smart pointers, no GC pauses during emulation
6. **Community** — most emulator projects use C++, easier to find contributors

### Consequences

- Build system is more complex than C (CMake + Conan/vcpkg)
- Memory safety is better than C but not guaranteed (use sanitizers in CI)
- Need to manage platform-specific build configs carefully

---

## ADR-002: UI Framework — Flutter/Dart

**Date:** 2026-09-16
**Status:** Accepted

### Context

The UI layer needs to render 3D scenes, handle navigation, manage state, and provide a polished cross-platform experience.

### Options Considered

| Option | Pros | Cons |
|---|---|---|
| **Flutter/Dart** | Hot reload, declarative, cross-platform, growing 3D | 3D still experimental, larger binary |
| **Native (per-platform)** | Best performance, platform-native feel | 5x code, 5x maintenance |
| **React Native** | Large ecosystem, hot reload | Not ideal for 3D, performance concerns |
| **Qt/QML** | Mature, C++ synergy | Declarative but less modern, licensing |

### Decision

**Flutter/Dart** for the UI layer.

### Rationale

1. **Hot reload** — iterate on 3D UI in seconds
2. **Declarative** — complex 3D scenes are easier to compose
3. **Cross-platform** — one UI codebase for all platforms
4. **Impeller renderer** — Flutter's new renderer is performant enough for 3D
5. **Growing 3D support** — Flutter 3D, custom shaders, community packages

### Consequences

- 3D rendering may need custom shaders or platform channels for advanced effects
- Binary size larger than native
- Some platform-specific UI tweaks needed

---

## ADR-003: Modular Core Architecture

**Date:** 2026-09-16
**Status:** Accepted

### Context

ezCore needs to support 50+ emulation systems. Monolithic core integration would bloat the app, create legal risk, and make updates difficult.

### Decision

**Modular cores** — each core is a separate binary, downloaded at runtime, loaded via dlopen/dlsym.

### Rationale

1. **Legal safety** — cores are separate binaries, not linked into ezCore
2. **Size** — users only download cores for systems they play
3. **Community** — third-party developers can build cores without touching ezCore
4. **Updates** — update cores independently of the main app
5. **Licensing** — each core can have its own license

### Consequences

- Core download system adds complexity
- Need manifest validation and sha256 verification
- Users need to manually download cores (or we provide a core store)

---

## ADR-004: Cloud Saves as Primary Feature

**Date:** 2026-09-16
**Status:** ~~Accepted~~ **Superseded** — cloud sync is deferred to v1.1
(backend, auth, conflict policy and privacy review are not v1 work); the
local Time Capsule vault is the v1 save story. See `RELEASE_PLAN.md`.

### Context

ezCore needs a primary selling point that differentiates it from existing emulators (RetroArch, OpenEmu, etc.).

### Decision

**Cloud saves** are the #1 feature. Everything else is secondary.

### Rationale

1. **Differentiation** — most emulators are local-only
2. **User value** — pick up where you left off on any device
3. **Lock-in** — users who invest in cloud saves are less likely to switch
4. **Monetization** — cloud saves are a natural Pro feature

### Consequences

- Need backend infrastructure (Firebase/Supabase)
- Need account system
- Need conflict resolution strategy
- Ongoing server costs

---

## ADR-005: Legal Holds — No Switch/3DS/PS2

**Date:** 2026-09-16
**Status:** Accepted

### Context

Some emulation systems are legally risky due to active litigation from console manufacturers.

### Decision

**Never build or ship** cores for Switch, 3DS, or PS2.

### Rationale

1. **Nintendo litigation** — 2024 Yuzu settlement set precedent
2. **Proprietary firmware** — these systems require copyrighted firmware
3. **Risk/reward** — legal risk far outweighs user demand
4. **Community reputation** — associating with litigation is bad for the project

### Consequences

- Some users will be disappointed
- Need clear communication about why these systems aren't supported
- May need to actively prevent community cores for these systems

---

## ADR-006: Vibe Coding via MD Files

**Date:** 2026-09-16
**Status:** Accepted

### Context

The user wants to drive development through MD files, with AI (me) reading specs and writing code.

### Decision

**All development is driven by MD files.** Specs before code. Documentation is part of the work.

### Rationale

1. **AI-friendly** — MD files are easy for AI to read and follow
2. **Human-readable** — user can review and steer without reading code
3. **Version-controlled** — MD files live in git, track changes
4. **Living documentation** — docs stay in sync with code

### Consequences

- Need to maintain MD files as code changes
- Need clear MD file hierarchy
- Need discipline to always update docs

---

## ADR-007: Privacy-First Architecture — Login Optional

**Date:** 2026-09-16
**Status:** Accepted

### Context

Emulation is a sensitive topic. Users are rightfully concerned about privacy — what they play, when they play, and whether their data is being collected. ezCore must be privacy-first by design, not as an afterthought.

### Decision

**Login is optional.** Users can use ezCore fully without creating an account. Cloud saves are an opt-in feature, not a requirement.

### Privacy Principles

1. **No usage analytics** — we don't track what games you play, when you play, or how long you play
2. **No telemetry** — no crash reports with usage data, no performance metrics
3. **Only save files in cloud** — if you opt into cloud sync, only your save state bytes are stored
4. **Local-first** — all data lives on your device first; cloud is a backup, not the source of truth
5. **Transparent** — clear privacy policy, open-source code, no hidden data collection

### Architecture

```
Guest Mode (default):
  - All saves stored locally
  - No account needed
  - No cloud sync
  - Full functionality (except cloud features)

Opt-In Cloud:
  - User creates account (email or OAuth)
  - Only save state bytes uploaded to Firebase Storage
  - Firestore stores: uid, pro status, last login (no usage data)
  - No analytics events logged
```

### What We Store

| Data | Stored? | Where |
|---|---|---|
| Save state bytes | ✅ (if opt-in) | Firebase Storage |
| User email | ✅ (if opt-in) | Firebase Auth |
| Pro status | ✅ (if opt-in) | Firestore |
| Last login | ✅ (if opt-in) | Firestore |
| Games played | ❌ | — |
| Play time | ❌ | — |
| IP address | ❌ | — |
| Device info | ❌ | — |
| Crash logs | ❌ | — |

### Rationale

1. **Trust** — emulation community is privacy-conscious; we earn trust by not collecting data
2. **Legal** — less data = less liability (GDPR, CCPA compliance by design)
3. **Simplicity** — no analytics pipeline to build and maintain
4. **Differentiation** — "we don't track you" is a selling point

---

## ADR-008: Cheat Database — Agent-Tested

**Date:** 2026-09-16
**Status:** Accepted

### Context

Most emulators ship with community-sourced cheat databases that are untested — codes may be wrong, outdated, or game-specific. ezCore can differentiate by building a **tested, verified cheat database** using automated agents.

### Decision

Build our own cheat database using Hermes cron agents that:
1. **Harvest** cheats from community sources
2. **Validate** each cheat by loading it into the actual core and testing
3. **Curate** the database with confidence scores and categories

### Agent Architecture

```
Hermes Cron Agents (scheduled)
├── Agent 1: Cheat Harvester (weekly)
│   ├── Scrapes community cheat sources
│   ├── Deduplicates and normalizes codes
│   └── Outputs: raw_cheats.json
│
├── Agent 2: Cheat Validator (weekly)
│   ├── Loads each core via ezCore runtime
│   ├── Applies each cheat via ezcore_cheat_set
│   ├── Runs frames, checks if cheat took effect
│   └── Outputs: validated_cheats.json
│
└── Agent 3: Database Curator (weekly)
    ├── Merges validated cheats into master database
    ├── Categorizes (Gameplay, Items, Power-ups, etc.)
    ├── Assigns confidence scores
    └── Outputs: ezcore_cheats.db
```

### Unique Selling Point

"Every cheat in our database is tested and verified to work."

No other emulator does this. Users trust our database because we prove each code works.

### Rationale

1. **Quality** — tested cheats > untested cheats
2. **Trust** — users know our database is reliable
3. **Automation** — agents run on cron, minimal manual effort
4. **Community** — open-source database, community can contribute

---

## ADR-009: Metadata Source — OpenVGDB + No-Intro

**Date:** 2026-09-16
**Status:** Accepted

### Context

ezCore needs to identify ROMs and fetch metadata (title, box art, screenshots, genre, release year). Two main sources exist: ScreenScraper.fr (requires API key, rate-limited) and OpenVGDB (open-source, community-maintained).

### Decision

**OpenVGDB + No-Intro** for v1, with optional ScreenScraper.fr enhancement.

### Architecture

```
ROM dropped in folder
       ↓
1. Hash ROM header (SHA-256)
       ↓
2. Match against No-Intro DAT → game ID
       ↓
3. Look up metadata in OpenVGDB → title, box art, genre, year
       ↓
4. (Optional) User adds ScreenScraper API key → richer metadata
```

### Why This Approach

| Factor | OpenVGDB + No-Intro | ScreenScraper.fr |
|---|---|---|
| API key | Not required | Required |
| Rate limits | None | Yes |
| Cost | Free | Free (with limits) |
| Completeness | Good | Excellent |
| Open source | Yes | No |
| Works offline | Yes (after download) | No |

### Rationale

1. **Works out of the box** — no API key needed
2. **Open-source** — aligns with ezCore's values
3. **Offline capable** — download database once, works forever
4. **Extensible** — users can add ScreenScraper for richer data

---

## ADR-010: Payment Platform — Stripe + RevenueCat

**Date:** 2026-09-16
**Status:** ~~Accepted~~ **Superseded** — payments are not part of v1; no
payment code ships (the old roadmap's Firebase/Stripe scaffolding was
explicitly dropped). Revisit if/when a paid tier exists.

### Context

ezCore needs payment processing for Pro tier and in-app purchases. Desktop and mobile have different requirements.

### Decision

**Stripe for desktop, RevenueCat for mobile.**

### Architecture

```
Desktop (Windows/macOS/Linux):
  - Stripe checkout (web-based)
  - Payment methods: Card, Apple Pay, Google Pay
  - Stripe handles PCI compliance

Mobile (Android/iOS):
  - RevenueCat (unified IAP)
  - App Store / Play Store
  - RevenueCat handles receipt validation
```

### Why RevenueCat for Mobile

1. **Unified API** — one integration for App Store + Play Store
2. **Receipt validation** — server-side validation built in
3. **Subscription management** — cancel, renew, upgrade/downgrade
4. **Analytics** — subscription metrics without usage tracking

### Why Stripe for Desktop

1. **Best checkout experience** — customizable, fast
2. **PCI compliance** — Stripe handles everything
3. **Payment methods** — cards, Apple Pay, Google Pay, more
4. **No platform fees** — unlike App Store (15-30%)

### Rationale

1. **Platform-appropriate** — each platform gets the best tool
2. **Minimize fees** — Stripe on desktop avoids Apple/Google fees
3. **Unified Pro status** — one account, Pro on all devices

---

## ADR-011: First functional release uses the existing runtime seam

**Status:** Accepted for the current implementation brief.

Preserve the existing C ABI rather than rewriting it as part of UI integration.
Use one worker isolate as the owner of a native session, with bounded frame
requests and a separate platform PCM adapter. The isolate moves execution off
UI work; it does not sandbox native code. Verify manifest artifact hashes before
launch and keep local persistence as the default.

Current implementation uses software RGBA frame copies and a macOS audio adapter.
Release acceptance requires an actual app-level content/import/play/input/audio/
save/reopen run; contract tests and a successful build alone are insufficient.
Earlier monetization/cloud-first release priorities are not goals of this slice.

## Open Decisions

These need to be made before Phase 1:

| # | Question | Options |
|---|---|---|
| 1 | Free tier save slots | 3 / 5 / 10 |
| 2 | Lifetime Pro slots | 500 / 1000 / Unlimited |
| 3 | Refund policy | 14-day / 30-day / No refunds |
| 4 | Family sharing | No / Yes (up to 5) |
| 5 | Open source from day 1 | Yes / No (private until launch) |
| 6 | Development pace | Full-time (36 weeks) / Part-time (52-72 weeks) |
| 7 | Team | Just you + me / + core contributors / + UI designer |
| 8 | Desktop-first or mobile-first | Desktop / Mobile / Simultaneous |
