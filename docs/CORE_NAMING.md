# ezCORE core identity & provenance

> **Status:** implemented 2026-09-19. All 17 core identifiers renamed across
> manifests, catalog, registry, app, tests and build scripts.
> Remaining: rename the private GitHub repos, and a real trademark search.

---

## 1. The rule

Every core carries a name **we invent and own**. Two things are never allowed
in a core name:

1. **Another emulator's project name** — `melonds`, `snes9x`, `mgba`, `ppsspp`,
   … A repo path is a claim, and `ezcore-core-melonds` reads as "ezCORE's
   melonDS". We neither own nor speak for that project.
2. **A platform holder's mark used as the product identifier** — the system
   names themselves (NES, Game Boy, PlayStation, Mega Drive) belong to
   Nintendo/Sony/Sega.

Upstream is credited **inside** the repo — source URL, licence, and a
not-affiliated note in the manifest `provenance` block — never in the name.

Two corollaries, both learned the hard way:

- **Do not create one of our cores per upstream core.** Two third-party GB/GBC
  emulators do not justify two ezCORE GB/GBC cores. One system → one core.
- **A bare `GPL-2.0` in a manifest is not a licence finding.** See §5.

## 2. Final names

| System | Core name | Upstream engine | Upstream licence | Ships? |
|---|---|---|---|---|
| NES / FDS | **NesByte** | libretro/Mesen | GPL-3.0-or-later | yes |
| GB / GBC | **PocketBit** | LIJI32/SameBoy | Expat (MIT) | yes |
| GBA | **AdvanceBit** | libretro/mgba | MPL-2.0 | yes |
| SNES | **SuperFX** | snes9xgit/snes9x | non-commercial custom | **no — recipe only** |
| Genesis / MD / SMS / GG | **BlastProc** | Genesis-Plus-GX | non-commercial custom | **no — recipe only** |
| Atari 2600 | **Joystick** | libretro/stella2023 | GPL-2.0-or-later | yes |
| PC Engine / TG-16 | **CardCon** | beetle-pce-fast-libretro | GPL-2.0-or-later | yes |
| Saturn | **TwinSH** | beetle-saturn-libretro | GPL-2.0-or-later | yes |
| PS1 | **Geometry1** | libretro/swanstation | GPL-3.0 | yes |
| N64 | **RCP64** | mupen64plus-libretro-nx | GPL-2.0-or-later | yes |
| NDS | **DualScreen** | libretro/melonDS | GPL-3.0 | yes |
| PSP | **PortComp** | hrydgard/ppsspp | GPL-2.0-or-later | yes |
| Dreamcast | **DreamArc** | flyinghead/flycast | GPL-2.0-or-later | yes |
| GameCube / Wii | **PowerCube** | libretro/dolphin | GPL-2.0-or-later | yes |
| Arcade / Neo Geo | **CoinBox** | libretro/FBNeo | non-commercial custom | **no — recipe only** |
| DOS | **RealMode** | libretro/dosbox-pure | GPL-2.0-or-later | yes |
| SCUMM / adventure | **PointClick** | scummvm/scummvm | GPL-3.0-or-later | yes |

**Reserved / unused — `ColorBit`.** One shippable GB/GBC engine exists today
(SameBoy), so PocketBit covers both `gb` and `gbc`. ColorBit becomes live only
if a second *shippable* GB/GBC engine is added; mGBA is MPL-2.0 and does
GB/GBC, so it is the realistic candidate.

**Gambatte gets no core name**, because it can never ship with ezCORE (§5). Its
build recipe is retained and callable by hand (`scripts/build_core.sh
gambatte`), but it is out of every TIER list, unbundled on every OS, and
documented as gated rather than presented as one of our cores.

## 3. Collision screening

Rejected outright: `vega`/`polaris` (AMD silicon), `monolith` (Monolith
Productions), `obsidian` (Obsidian.md + Obsidian Entertainment), `chroma`
(Razer Chroma), `halide` (Halide app + language), `lumen` (Laravel),
`aurora`/`glacier` (AWS), `nautilus` (GNOME), `horizon` (Switch OS codename),
`prism` (PrismLauncher), `ledger` (Ledger wallets), `vertex` (Google),
`floppy` (FlashFloppy), `corona`, `cirrus`.

Rejected on the second pass, when the maintainer's picks were checked:
`mode7` (Mode 7 Limited, UK studio), `blast` (NVIDIA Blast, 453★), `parallax`
(wagerfield/parallax, 16.6k★), `box` (Box, Inc.), `twin` (cosmos72/twin) —
replaced by **SuperFX, BlastProc, TwinSH, PowerCube, DualScreen**, which all
scan clear.

An unrelated GitHub handle being taken is **not** disqualifying: every short
word is taken (100M+ users) and our path is already namespaced.

## 4. How the rename was applied

Our identifier changed; provenance did not. A blind find/replace would have
corrupted attribution, so the migration was deliberately narrow:

- **rewritten:** manifest `id` + `name`, `cores/catalog.json`,
  `cores/registry.json`, the id maps in `lib/screens/*` and
  `lib/widgets/hardware_art.dart`, test fixtures, `scripts/fill_manifest_data.py`
  keys, `scripts/build_core.sh` function names + `stage` ids + TIER lists,
  `native/cores*/` directories
- **never touched:** `upstream`, `homepage`, `license_url`, `provenance.*`,
  upstream clone URLs, `$SRC_DIR/<upstream>` build-scratch paths

Two traps worth remembering:

- In `build_core.sh`, `out="snes9x_libretro.$LIB_SUFFIX"` names the file
  **upstream's own makefile emits**, and `--target mgba_libretro` names
  **upstream's cmake target**. Renaming either breaks the build. Only
  `stage <our-id>` changes; `stage()` renames the artifact to ours.
- A token pass matching `'mgba'` misses path-embedded ids like
  `'cores/mgba/manifest.json'`. Both passes were needed.

## 5. Licence finding — Gambatte cannot ship

`native/src/gambatte-libretro/libgambatte/src/gambatte.cpp`:

```
 *   it under the terms of the GNU General Public License version 2 as
 *   published by the Free Software Foundation.
```

63 files grant v2-only, **zero** grant "or later". **GPL-2.0-only** cannot form
a combined work with our GPL-3.0-only app (the FSF treats a dlopen'd plugin
shipped in the same bundle as one work), and it was marked `bundled` for macOS
and Android. It is now unbundled everywhere.

`scripts/legal_audit.py` was hardened so this class of bug cannot recur:

- GPL-2.0-only is never bundleable
- **a bare, ambiguous `GPL-2.0` is now a violation when bundled** — that
  ambiguity is precisely how this shipped unnoticed
- licence classing distinguishes `-only` / `-or-later` / ambiguous

That change immediately surfaced six more cores sitting on a bare `GPL-2.0`
while bundled. Each was resolved from its own sources — vendored trees
excluded, comment-wrapped headers normalised, because C comment asterisks sit
*inside* wrapped licence phrases and defeat a plain grep:

| Core | 'or later' | v2-only | Result |
|---|---|---|---|
| beetle_pce | 38 | 0 | GPL-2.0-or-later |
| beetle_saturn | 95 | 0 | GPL-2.0-or-later |
| dosbox_pure | 240 | 0 | GPL-2.0-or-later |
| flycast | 527 | 0 | GPL-2.0-or-later |
| mupen64plus | 353 | 0 | GPL-2.0-or-later |
| stella | 4 | 0 | GPL-2.0-or-later |

**Correction:** a first crude scan flagged flycast, ppsspp and dolphin as
GPL-2.0-only. That was wrong — all three are fine (dolphin's COPYING states
GPLv2+ and "in aggregate … compatible with the GPLv3 license").

Open, lower priority: Stella's "or later" evidence is thin (4 files) — worth a
per-file pass before release. SameBoy's Expat grant excludes its `iOS` and
`HexFiend` directories; we do not build those.

## 6. Provenance block

Every manifest now carries:

```json
"provenance": {
  "built_from": "https://github.com/libretro/Mesen",
  "upstream_license": "GPL-3.0-or-later",
  "relationship": "independent build of upstream source; not affiliated with, endorsed by, or supported by the upstream project",
  "modifications": "none beyond build configuration"
}
```

Attribution is explicit rather than implied by a name, and
`THIRD_PARTY_NOTICES.md` remains the index of record.

## 7. Verified after the rename

`flutter analyze lib test` clean · `flutter test` **192/192** · CTest **5/5**
(`boot_nesbyte`, `boot_pocketbit`, `boot_advancebit`) · `scripts/legal_audit.py`
clean · catalog regenerated with 21 entries.

## 8. Remaining

1. Rename (or delete and recreate) the 18 private `ezcore-core-<upstream>` repos
   to `ezcore-core-<name>`; delete the Gambatte one.
2. A trademark search per name. `web_search` was unavailable for this entire
   session, so §3 is screened against known software only — no live register,
   domain, or app-store check has happened.
3. `docs/MATRIX.md` prose still names cores by upstream engine in places. That
   is correct as attribution, but narrative rows should lead with our core name.
