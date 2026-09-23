# ezCore — Master Plan

> **Status:** planning draft (2026-09-16) — **superseded** by
> [`RELEASE_PLAN.md`](RELEASE_PLAN.md) (v1 scope) and
> [`ARCHITECTURE.md`](ARCHITECTURE.md) (as-built). Kept for history; parts of
> it (C++ runtime, download infrastructure) were never built as written.
>
> **Version:** 1.0
> **Stack as written:** C++ (runtime) + Flutter/Dart (UI) + C/C++ (libretro cores)

---

## Table of Contents

1. [Product Vision](#1-product-vision)
2. [Architecture Overview](#2-architecture-overview)
3. [Platform Strategy](#3-platform-strategy)
4. [Modular Core System](#4-modular-core-system)
5. [Feature Set](#5-feature-set)
6. [Monetization](#6-monetization)
7. [Development Phases](#7-development-phases)
8. [Vibe Coding Workflow](#8-vibe-coding-workflow)
9. [Licensing & Copyright Strategy](#9-licensing--copyright-strategy)
10. [Repository Structure](#10-repository-structure)
11. [MD File Index](#11-md-file-index)

---

## 1. Product Vision

### What is ezCore?

ezCore is an **open-source, multi-system emulator frontend** that makes playing retro games feel modern. It combines a beautiful, fun, 3D-powered UI with intelligent automation (auto-scan, auto-cheats, cloud saves) so users spend time playing — not configuring.

### Target Audience

- **Casual retro players** who want a "Netflix for retro games" experience
- **Enthusiasts** who want save states, cheats, and shaders without manual setup
- **Cross-platform users** who play on desktop and mobile

### Core Differentiators

| Feature | Why It Matters |
|---|---|
| **Cloud Saves** | Pick up where you left off on any device. This is the #1 selling point. |
| **3D UI** | Not just flat lists — game boxes float, shelves rotate, transitions are juicy |
| **Auto Scan** | Drop ROMs in a folder, ezCore identifies games, fetches metadata, organizes |
| **Auto Cheats** | Built-in cheat database — enable GameShark/Action Replay codes with one tap |
| **Modular Cores** | Support 50+ systems without bloating the app. Licensing safety through separation. |
| **Cross-Platform** | Windows, macOS, Linux, Android, iOS — one codebase, native performance |

### Design Philosophy

- **Linear/Vercel/Stripe-level polish** — every interaction feels intentional
- **3D where it matters** — game shelves, box art, transitions — not gimmicky
- **Zero-config defaults** — it should work out of the box, power users can tweak
- **Fun to use** — haptics, animations, sound effects, delight

---

## 2. Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                        Flutter UI (Dart)                     │
│  3D rendering (Flutter 3D / custom shaders)                  │
│  State management (Riverpod)                                 │
│  Cloud sync client                                           │
│  Auto-scan / auto-cheat engine                               │
└──────────────────────────┬──────────────────────────────────┘
                           │ dart:ffi
┌──────────────────────────▼──────────────────────────────────┐
│                   C++ Runtime (ezcore_runtime)                │
│  Session lifecycle  │  AV plumbing  │  Input  │  Saves       │
│  Core loader (dlopen/dlsym)  │  Cheat engine                 │
│  Cloud sync bridge  │  Auto-scan bridge                      │
│  Exports C ABI (ezcore_runtime.h)                           │
└──────────────────────────┬──────────────────────────────────┘
                           │ C ABI
┌──────────────────────────▼──────────────────────────────────┐
│                    Modular Cores (C/C++)                      │
│  cores/<id>/manifest.json  │  cores/<id>/libretro_core.so     │
│  Versioned, sha-pinned, sandboxed                           │
└─────────────────────────────────────────────────────────────┘
```

### Layer Responsibilities

| Layer | Language | Owns |
|---|---|---|
| **UI** | Dart/Flutter | 3D rendering, navigation, settings, player chrome, animations |
| **Runtime** | C++ | Session lifecycle, AV plumbing, input, saves, cheats, core loading, cloud bridge |
| **Cores** | C/C++ | Libretro API implementation, system emulation |

### Why C++ for the Runtime?

- **Direct libretro compatibility** — cores are C/C++, no translation layer
- **Performance** — zero overhead for frame/audio processing
- **Cross-platform** — one codebase compiles to all 5 platforms
- **Mature tooling** — CMake, Conan/vcpkg, established patterns
- **Memory control** — RAII, smart pointers, no GC pauses during emulation

### Why Flutter for the UI?

- **Hot reload** — iterate on 3D UI in seconds
- **Declarative** — complex 3D scenes are easier to compose
- **Cross-platform** — one UI codebase for all platforms
- **Growing 3D support** — Flutter 3D, custom shaders, Impeller renderer

---

## 3. Platform Strategy

### Target Platforms

| Platform | Priority | Notes |
|---|---|---|
| **Windows** | P1 | Primary dev target, largest retro gaming audience |
| **macOS** | P1 | Already have 17 cores verified on arm64 |
| **Linux** | P1 | Growing retro community, Steam Deck |
| **Android** | P2 | Mobile gaming, touch controls |
| **iOS** | P2 | App Store restrictions, no JIT — interpreter-only cores |

### Platform-Specific Considerations

#### Windows
- Primary development platform
- MSVC + CMake build
- DirectX/Vulkan for 3D rendering
- Win32 file system APIs

#### macOS
- Already verified — 17 cores built on arm64
- Universal binary (arm64 + x86_64)
- Metal for 3D rendering
- App Store distribution (with limitations)

#### Linux
- GCC/Clang + CMake
- Vulkan for 3D rendering
- Flatpak/Steam distribution
- Steam Deck optimization

#### Android
- NDK + CMake
- Vulkan/OpenGL ES for 3D
- Touch controls + gamepad
- Play Store distribution

#### iOS
- Xcode + CMake
- Metal for 3D
- **No JIT** — interpreter-only cores (enforced by manifest)
- App Store distribution (restrictive)

### Build System

```
CMake (top-level)
├── runtime/           # C++ runtime → libezcore_runtime.so/dylib/dll
├── cores/<id>/        # Individual core builds
├── flutter/           # Flutter project
└── platform/          # Platform-specific configs
    ├── windows/
    ├── macos/
    ├── linux/
    ├── android/
    └── ios/
```

Package management: **vcpkg** (desktop) + **Conan** (mobile)

---

## 4. Modular Core System

### Why Modular?

1. **Licensing safety** — cores are separate binaries, not linked into the main app
2. **Size** — users only download cores for systems they play
3. **Community** — third-party developers can build cores without touching ezCore
4. **Updates** — update cores independently of the main app
5. **Licensing** — each core can have its own license

### Core Structure

```
cores/
├── mesen/
│   ├── manifest.json          # Core metadata, version, supported systems
│   ├── libretro_core.so       # The actual libretro core
│   ├── sha256.txt             # Integrity hash
│   └── README.md              # Core-specific notes
├── mgba/
│   ├── manifest.json
│   ├── libretro_core.so
│   ├── sha256.txt
│   └── README.md
└── ...
```

### Manifest Schema (v1)

```json
{
  "id": "mesen",
  "name": "Mesen",
  "version": "0.9.9",
  "systems": ["nes"],
  "author": "SourMesen",
  "license": "GPL-3.0",
  "abi_version": 1,
  "execution": {
    "windows": "dynarec",
    "macos": "dynarec",
    "linux": "dynarec",
    "android": "dynarec",
    "ios": "interpreter"
  },
  "sha256": {
    "windows-x64": "abc123...",
    "macos-arm64": "def456...",
    "linux-x64": "ghi789...",
    "android-arm64": "jkl012...",
    "ios-arm64": "mno345..."
  },
  "download_url": "https://github.com/ezcore/cores/releases/download/v1.0/mesen-{platform}.zip"
}
```

### Core Loading Flow

```
1. User selects a game
2. ezCore checks CoreRegistry for compatible cores
3. If no core installed → prompt to download
4. Download core package (zip)
5. Verify sha256
6. Extract to cores/<id>/
7. dlopen the core
8. Verify ABI version
9. Load game
```

### Core Sandboxing

- Cores run in the **same process** (libretro requirement)
- But are **dlopen'd with RTLD_LOCAL** — no symbol leakage
- File system access is **restricted** to system/save directories
- Network access is **blocked** (cores don't need internet)

### Supported Systems (Roadmap)

| Tier | Systems | Cores |
|---|---|---|
| **Tier 1** (launch) | NES, SNES, GB, GBC, GBA, Genesis | Mesen, Snes9x, mGBA, Genesis Plus GX |
| **Tier 2** (v1.1) | N64, PS1, PSP, DS | Mupen64Plus, PCSX-ReARMed, PPSSPP, DeSmuME |
| **Tier 3** (v1.2) | Arcade, Neo Geo, TurboGrafx | FBNeo, Mednafen |
| **Tier 4** (v2.0) | Saturn, Dreamcast | Yabause, Flycast |
| **Never** | Switch, 3DS, PS2 | Holds — Nintendo litigation risk |

---

## 5. Feature Set

### 5.1 Cloud Saves (Primary Selling Point)

**The #1 feature. Everything else is secondary.**

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Device A  │────▶│  Cloud API  │◀────│   Device B  │
│  (Windows)  │     │  (REST)     │     │  (Android)  │
└─────────────┘     └─────────────┘     └─────────────┘
```

**What syncs:**
- Save states (slot 0-9 per game)
- In-game saves (SRAM/EEPROM)
- Settings (per-game and global)
- Cheat states (enabled/disabled)
- Play time, last played
- Screenshots

**Implementation:**
- C++ runtime exposes save bytes (opaque)
- Dart layer handles cloud upload/download
- Conflict resolution: last-write-wins with manual merge option
- Offline queue: sync when connection restored

**Backend options:**
- **Firebase** (easiest, free tier generous)
- **Supabase** (open-source, self-hostable)
- **Custom** (most control, most work)

**Recommendation:** Firebase for v1, migrate to Supabase if self-hosting becomes important.

### 5.2 3D UI

**Not gimmicky 3D. Purposeful 3D.**

- **Game shelf** — 3D shelf with box art, hover to preview
- **Game detail** — 3D box rotation, screenshot carousel
- **Transitions** — smooth 3D transitions between screens
- **Background** — subtle 3D particle effects or parallax
- **Player** — 3D frame around the game screen

**Technical approach:**
- Flutter 3D (experimental) or custom shaders
- Impeller renderer (Flutter's new renderer) for performance
- LOD (level of detail) for mobile — reduce 3D complexity on low-end devices

### 5.3 Auto Scan

**Drop ROMs in a folder. ezCore does the rest.**

```
User action:        Drop ROMs into ~/ezCore/ROMs/
                    ↓
ezCore detects:     New files added
                    ↓
Identify:           Hash ROM header → match against No-Intro database
                    ↓
Fetch metadata:     Title, release year, genre, box art, screenshots
                    ↓
Organize:           Sort by system, create game entries
                    ↓
Match core:         Find compatible core, prompt to download
                    ↓
Ready to play:      Game appears in library
```

**Metadata sources (locked in — ADR-009):**
- **No-Intro DAT** — ROM identification (open-source, offline-capable)
- **OpenVGDB** — metadata, box art, genre, year (open-source, community-maintained)
- **ScreenScraper.fr** (optional) — richer metadata for users who add their API key

**Why OpenVGDB + No-Intro:** Works out of the box with no API key. Open-source and offline-capable. No rate limits. Extensible — power users add ScreenScraper for richer data.

### 5.4 Auto Cheats — Agent-Tested Database

**Our own cheat database, tested and verified by agents.**

This is a **unique selling point** — no other emulator ships with a verified cheat database (locked in — ADR-008).

```
Game loaded → ezCore checks our cheat database
                    ↓
Found cheats → Display with confidence score
                    ↓
User enables → Forwarded to core via retro_cheat_set
                    ↓
Cheat active → "Verified ✅" indicator in UI
```

**How the database is built:**

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
    └── Outputs: ezcore_cheats.db (ships with app)
```

**Cheat sources:**
- Community cheat databases (GameShark, Action Replay, CodeBreaker)
- User-contributed cheats (community PR)
- Open-source cheat repositories

**Implementation:**
- Database ships with app (SQLite format)
- Each cheat has: code, type, category, description, confidence score, tested core version
- C++ runtime forwards to retro_cheat_reset / retro_cheat_set
- Dart layer manages cheat UI, categories, enable/disable
- Cheats are per-game, stored in cloud sync
- Database updated via silent app background update

### 5.5 Additional Features

| Feature | Description | Priority |
|---|---|---|
| **Rewind** | Hold button to rewind gameplay | P1 |
| **Fast Forward** | 2x/4x/8x speed | P1 |
| **Shaders** | CRT, scanline, pixel-perfect filters | P1 |
| **Netplay** | Online multiplayer via rollback | P2 |
| **Achievements** | RetroAchievements integration | P2 |
| **Controller Support** | Auto-map, per-game profiles | P1 |
| **Touch Controls** | On-screen overlay for mobile | P1 |
| **Screenshot** | Capture and share | P2 |
| **Video Recording** | Record gameplay clips | P3 |

---

## 6. Monetization

### Free vs Pro

| Feature | Free | Pro |
|---|---|---|
| Core emulator | ✅ | ✅ |
| Local saves | ✅ | ✅ |
| Cloud saves | ❌ | ✅ |
| Auto scan | ❌ | ✅ |
| Auto cheats | ❌ | ✅ |
| 3D UI | Basic | Full |
| Themes | 1 | All |
| Pro badge | ❌ | ✅ |
| Skins | ❌ | ✅ |
| In-game items | ❌ | ✅ |
| Priority support | ❌ | ✅ |

### Pricing

- **Free:** $0 — core emulator, local saves, basic UI
- **Pro:** $4.99/month or $29.99/year
- **Lifetime:** $49.99 one-time (launch offer)

### In-Game Items & Skins

**Skins (cosmetic):**
- UI themes (Neon, Retro, Minimal, Cyberpunk)
- Game shelf styles (Wood, Glass, Metal)
- Box art frames (Gold, Holographic, Pixel)

**In-game items:**
- Profile badges (Pro, Early Supporter, Beta Tester)
- Animated avatars
- Custom cursor effects
- 3D background effects

**Sellable items:**
- Skin packs ($0.99-$2.99)
- Theme bundles ($4.99)
- Exclusive badges (limited events)

### Payment Integration

- **Desktop:** Stripe (web-based upgrade flow)
- **Mobile:** In-app purchases (App Store / Play Store)
- **Cross-platform:** Pro status tied to account, not device

### Revenue Projections (Year 1)

| Scenario | Users | Pro % | MRR | ARR |
|---|---|---|---||
| Conservative | 10,000 | 5% | $2,495 | $29,940 |
| Moderate | 50,000 | 8% | $19,960 | $239,520 |
| Optimistic | 200,000 | 10% | $99,800 | $1,197,600 |

---

## 7. Development Phases

### Phase 0: Foundation (Weeks 1-4)

**Goal:** Project skeleton, build system, basic runtime

- [ ] Set up CMake build system (all 5 platforms)
- [ ] Create C++ runtime skeleton (session lifecycle, dlopen)
- [ ] Create Flutter project with basic navigation
- [ ] Implement C ABI (ezcore_runtime.h)
- [ ] Set up CI/CD (GitHub Actions)
- [ ] Write all MD files (this plan + specs)

**Deliverable:** Build system works, empty runtime loads, Flutter app launches

### Phase 1: Core Runtime (Weeks 5-10)

**Goal:** Working emulator with one core

- [ ] Port runtime.c to C++ (session, AV, input, saves)
- [ ] Integrate first core (Mesen — NES)
- [ ] Basic Flutter UI (game list, player screen)
- [ ] Save states (local)
- [ ] Basic settings

**Deliverable:** Play NES games with save states

### Phase 2: Multi-Core (Weeks 11-16)

**Goal:** Support 6+ systems

- [ ] Add cores: Snes9x, mGBA, Genesis Plus GX, Mupen64Plus, PCSX-ReARMed
- [ ] Core download system
- [ ] Core registry and manifest validation
- [ ] Auto-detect compatible core
- [ ] Settings per-game

**Deliverable:** Play 6 systems with automatic core management

### Phase 3: Cloud & Automation (Weeks 17-22)

**Goal:** Cloud saves, auto scan, auto cheats

- [ ] Firebase integration
- [ ] Cloud save sync
- [ ] Auto scan (ROM identification)
- [ ] Metadata fetching
- [ ] Auto cheats (database + UI)

**Deliverable:** Cloud saves work, auto scan identifies games, cheats are one-tap

### Phase 4: 3D UI & Polish (Weeks 23-28)

**Goal:** Beautiful, fun, polished UI

- [ ] 3D game shelf
- [ ] 3D transitions
- [ ] Animations and haptics
- [ ] Themes and skins
- [ ] Controller support
- [ ] Touch controls

**Deliverable:** UI that looks and feels like a premium product

### Phase 5: Monetization (Weeks 29-32)

**Goal:** Pro tier, payments, in-game items

- [ ] Stripe integration
- [ ] In-app purchases
- [ ] Pro badge and skins
- [ ] Account system
- [ ] Upgrade flow

**Deliverable:** Free and Pro tiers working, payments processing

### Phase 6: Launch (Weeks 33-36)

**Goal:** Public release

- [ ] Beta testing
- [ ] Bug fixes
- [ ] Performance optimization
- [ ] Documentation
- [ ] Marketing (website, social media)
- [ ] Launch on itch.io / GitHub / App Store / Play Store

**Deliverable:** Public launch

---

## 8. Vibe Coding Workflow

### What is Vibe Coding?

Vibe coding = **everything is driven by MD files**. The AI (me) reads the MD files, writes the code, and updates the MD files. You review and steer.

### MD File Hierarchy

```
docs/
├── PLAN.md                    # This file — master plan
├── ARCHITECTURE.md            # Technical architecture
├── API.md                      # C ABI specification
├── CORE_SYSTEM.md              # Modular core design
├── CLOUD_SAVES.md              # Cloud sync specification
├── UI_DESIGN.md               # UI/UX design spec
├── MONETIZATION.md            # Business model
├── ROADMAP.md                  # Development timeline
└── DECISIONS.md                # Architecture decision records
```

### Workflow

```
1. You write/update MD files (specs, plans, decisions)
                    ↓
2. I read the MD files
                    ↓
3. I write the code
                    ↓
4. I update the MD files (document what was built)
                    ↓
5. You review, steer, repeat
```

### Rules

1. **MD files are the source of truth** — if it's not in an MD file, it doesn't exist
2. **Code is generated from MD files** — I don't invent features not in the specs
3. **Every decision is documented** — DECISIONS.md tracks why we chose X over Y
4. **Specs before code** — no code without a spec
5. **Update MD files after every change** — documentation is part of the work

### How to Steer

- Edit any MD file → I'll follow the updated spec
- Add a new MD file → I'll incorporate it
- Delete an MD file → I'll remove the corresponding code
- Comment in MD files → I'll address the comment

---

## 9. Licensing & Copyright Strategy

### The Core Principle

**ezCore does not distribute any copyrighted material. Ever.**

### How Modular Cores Protect Us

1. **Cores are separate binaries** — not linked into ezCore
2. **Users download cores separately** — from their own sources
3. **No BIOS files** — users provide their own
4. **No ROMs** — users provide their own
5. **No copyrighted assets** — all metadata is user-generated or public domain

### What We Don't Do

- ❌ Distribute Nintendo, Sony, Sega, or any other company's BIOS
- ❌ Distribute ROMs or game files
- ❌ Distribute cores that require proprietary firmware
- ❌ Support systems where the only cores require copyrighted firmware (Switch, 3DS, PS2)
- ❌ Link to piracy sites

### What We Do

- ✅ Provide the emulator frontend (ezCore)
- ✅ Provide the runtime that loads cores
- ✅ Provide tools for users to organize their own ROMs
- ✅ Provide cloud save infrastructure
- ✅ Provide a marketplace for community-built cores (future)

### Holds (Never Build/Ship)

| System | Reason |
|---|---|
| **Switch** | Nintendo litigation (2024 Yuzu settlement), proprietary firmware |
| **3DS** | Nintendo litigation, proprietary firmware |
| **PS2** | Sony litigation risk, complex architecture |

### License

- **ezCore runtime:** GPL-3.0 (copyleft, ensures derivatives stay open)
- **ezCore UI:** GPL-3.0
- **Cores:** Each core retains its own license
- **Metadata:** Public domain or CC0

---

## 10. Repository Structure

```
universal-emulator/
├── docs/                          # All MD files (source of truth)
│   ├── PLAN.md                    # Master plan
│   ├── ARCHITECTURE.md            # Technical architecture
│   ├── API.md                      # C ABI specification
│   ├── CORE_SYSTEM.md              # Modular core design
│   ├── CLOUD_SAVES.md              # Cloud sync specification
│   ├── UI_DESIGN.md               # UI/UX design spec
│   ├── MONETIZATION.md            # Business model
│   ├── ROADMAP.md                  # Development timeline
│   └── DECISIONS.md                # Architecture decision records
│
├── runtime/                       # C++ runtime
│   ├── CMakeLists.txt
│   ├── include/
│   │   └── ezcore_runtime.h       # C ABI header
│   ├── src/
│   │   ├── runtime.cpp            # Main runtime
│   │   ├── session.cpp            # Session management
│   │   ├── audio.cpp              # Audio plumbing
│   │   ├── video.cpp              # Video plumbing
│   │   ├── input.cpp              # Input handling
│   │   ├── saves.cpp              # Save state management
│   │   ├── cheats.cpp             # Cheat engine
│   │   ├── core_loader.cpp        # dlopen/dlsym
│   │   └── cloud_bridge.cpp       # Cloud sync bridge
│   └── test/
│       ├── test_session.cpp
│       ├── test_audio.cpp
│       ├── test_saves.cpp
│       └── test_cheats.cpp
│
├── cores/                         # Modular cores (downloaded at runtime)
│   └── README.md                  # How to add a core
│
├── flutter/                       # Flutter UI
│   ├── pubspec.yaml
│   ├── lib/
│   │   ├── main.dart
│   │   ├── screens/
│   │   │   ├── home_screen.dart
│   │   │   ├── game_list_screen.dart
│   │   │   ├── player_screen.dart
│   │   │   ├── settings_screen.dart
│   │   │   └── store_screen.dart
│   │   ├── widgets/
│   │   │   ├── game_shelf_3d.dart
│   │   │   ├── game_card_3d.dart
│   │   │   ├── player_chrome.dart
│   │   │   └── cheat_overlay.dart
│   │   ├── state/
│   │   │   ├── app_state.dart
│   │   │   ├── game_state.dart
│   │   │   └── settings_state.dart
│   │   ├── services/
│   │   │   ├── cloud_sync.dart
│   │   │   ├── auto_scan.dart
│   │   │   ├── auto_cheat.dart
│   │   │   └── core_manager.dart
│   │   └── runtime/
│   │       └── ezcore_ffi.dart    # dart:ffi bindings
│   └── test/
│
├── platform/                      # Platform-specific configs
│   ├── windows/
│   ├── macos/
│   ├── linux/
│   ├── android/
│   └── ios/
│
├── scripts/                       # Build & dev scripts
│   ├── build_all.sh
│   ├── build_core.sh
│   └── dev_status.sh
│
├── assets/                        # Static assets
│   ├── icons/
│   ├── shaders/
│   └── themes/
│
├── .github/                       # CI/CD
│   └── workflows/
│       ├── build_windows.yml
│       ├── build_macos.yml
│       ├── build_linux.yml
│       ├── build_android.yml
│       └── build_ios.yml
│
├── CMakeLists.txt                 # Top-level CMake
├── pubspec.yaml                   # Flutter dependencies
├── LICENSE                        # GPL-3.0
├── CONTRIBUTING.md
└── README.md
```

---

## 11. MD File Index

| File | Purpose | Status |
|---|---|---|
| `PLAN.md` | Master plan — this file | ✅ Complete |
| `ARCHITECTURE.md` | Technical architecture (C++ runtime) | ✅ Complete |
| `API.md` | C ABI specification | ✅ Complete |
| `CORE_SYSTEM.md` | Modular core design | ✅ Complete |
| `CLOUD_SAVES.md` | Cloud sync specification | ✅ Complete |
| `UI_DESIGN.md` | UI/UX design spec | ✅ Complete |
| `MONETIZATION.md` | Business model | ✅ Complete |
| `ROADMAP.md` | Development timeline | ✅ Complete |
| `DECISIONS.md` | Architecture decision records | ✅ Complete |

---

## Appendix A: Key Decisions Log

| Date | Decision | Rationale |
|---|---|---|
| 2026-09-16 | C++ for runtime | Direct libretro compatibility, performance, cross-platform |
| 2026-09-16 | Flutter for UI | Hot reload, declarative 3D, cross-platform |
| 2026-09-16 | Modular cores | Licensing safety, size, community, independent updates |
| 2026-09-16 | Cloud saves as #1 feature | Primary selling point, differentiator |
| 2026-09-16 | No Switch/3DS/PS2 | Holds — Nintendo/Sony litigation risk |
| 2026-09-16 | Vibe coding via MD files | AI-driven development, you steer via specs |
| 2026-09-16 | Not Rust | C++ has direct libretro compat, mature tooling, larger emulator community |
| 2026-09-16 | Firebase for cloud (v1) | Fastest to ship, free tier generous, real-time sync |
| 2026-09-16 | Stripe for payments | Best desktop checkout, handles PCI compliance |
| 2026-09-16 | Custom shaders for 3D | Full control, good performance, no experimental dependencies |

---

## Appendix B: Open Questions

These need decisions before Phase 1:

1. **Free tier save slots:** 3, 5, or 10?
2. **Lifetime Pro slots:** 500, 1000, or unlimited?
3. **Refund policy:** 14-day, 30-day, or no refunds?
4. **Family sharing:** No, or yes (up to 5 members)?
5. **Open source from day 1:** Yes, or private until launch?
6. **Development pace:** Full-time (36 weeks), or part-time (52-72 weeks)?
7. **Team:** Just you + me, + core contributors, + UI designer?
8. **Desktop-first or mobile-first:** Desktop, mobile, or simultaneous? *(pending)*

---

*This plan is a living document. Update it as decisions are made and the project evolves.*
