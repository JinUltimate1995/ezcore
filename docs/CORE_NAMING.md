# ezCORE core identity & provenance

> **Status:** names chosen by maintainer 2026-09-19. 12 settled, **5 flagged**
> for a collision swap (§3). Repos are not renamed until §3 closes.
> Supersedes the earlier candidate-menu draft.

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

Upstream is credited **inside** the repo — source URL + license + a
not-affiliated note — never in the name. See the `provenance` block in §5.

Corollary, learned the hard way: **do not create one of our cores per upstream
core.** Two third-party GB/GBC emulators do not justify two ezCORE GB/GBC
cores. One system → one core.

## 2. Settled names

| System | Core name | Upstream engine | Upstream license | Distributable? |
|---|---|---|---|---|
| NES / FDS | **NesByte** | libretro/Mesen | GPL-3+ | yes |
| GB / GBC | **PocketBit** | LIJI32/SameBoy | Expat (MIT) | yes |
| GBA | **AdvanceBit** | libretro/mgba | MPL-2.0 | yes |
| SNES | Mode7 *(flagged)* | snes9xgit/snes9x | non-commercial custom | **no — recipe only** |
| Genesis / MD / SMS / GG | Blast *(flagged)* | Genesis-Plus-GX | non-commercial custom | **no — recipe only** |
| Atari 2600 | **Joystick** | libretro/stella2023 | GPL-2+ | yes |
| PC Engine / TG-16 | **CardCon** | beetle-pce-fast-libretro | GPL-3+ | yes |
| Saturn | Parallax *(flagged)* | beetle-saturn-libretro | GPL-2+ | yes |
| PS1 | **Geometry1** | libretro/swanstation | GPL-3 | yes |
| N64 | **RCP64** | mupen64plus-libretro-nx | GPL-3+ | yes |
| NDS | Twin *(flagged)* | libretro/melonDS | GPL-3 | yes |
| PSP | **PortComp** | hrydgard/ppsspp | GPL-2+ | yes |
| Dreamcast | **DreamArc** | flyinghead/flycast | GPL-2+ | yes |
| GameCube / Wii | Box *(flagged)* | libretro/dolphin | GPLv2+ (states GPLv3-compatible) | yes |
| Arcade / Neo Geo | **CoinBox** | libretro/FBNeo | non-commercial custom | **no — recipe only** |
| DOS | **RealMode** | libretro/dosbox-pure | GPL-2+ | yes |
| SCUMM / adventure | **PointClick** | scummvm/scummvm | GPL-3+ | yes |

**GB/GBC is one core, not two.** Engine chosen is SameBoy (Expat/MIT) — and
that is not a preference, it is forced by §4: Gambatte is GPL-2.0-**only** and
cannot ship alongside our GPL-3.0 app. `ColorBit` is therefore unused and free
if a second GB core is ever wanted.

## 3. Open — 5 names need a swap (real software collisions)

Screened against existing software. These five have a notable live collision;
the other twelve are clean.

| Pick | What it collides with | Suggested swap (same style) |
|---|---|---|
| `mode7` | Mode 7 Limited (UK game studio, *Frozen Synapse*); several repos | `LayerBit` · `AffineBit` |
| `blast` | julianshapiro/blast (1.5k★); NVIDIAGameWorks/Blast (453★) | `BlastBit` · `RushBit` |
| `parallax` | wagerfield/parallax (16.6k★ — widely known) | `ParallaxBit` · `TwinSH2` |
| `box` | Box, Inc.; cdgriffith/Box (2.8k★); box-project/box | `PowerBox` · `CubeBit` |
| `twin` | cosmos72/twin (1.1k★ — terminal WM) | `TwinBit` · `DuoScreen` |

The `*Bit` pattern is already your own family (NesByte, PocketBit, AdvanceBit),
so a swap keeps the set coherent.

## 4. License finding — Gambatte cannot ship

`native/src/gambatte-libretro/libgambatte/src/gambatte.cpp`:

```
 *   it under the terms of the GNU General Public License version 2 as
 *   published by the Free Software Foundation.
```

No "or later" grant anywhere in the tree (0 files). **Gambatte is
GPL-2.0-only.** Our app is **GPL-3.0**. GPL-2.0-only and GPL-3.0 are mutually
incompatible — the FSF treats a dlopen'd plugin shipped in the same bundle as
a combined work, so that combination cannot be distributed. **Gambatte is
currently marked `bundled` for macOS and Android.** Dropping it (as decided)
closes the issue.

Corrected false alarms — flagged by a crude scan, then verified properly and
**fine**:

| Core | Evidence |
|---|---|
| flycast | 527 source files grant "any later version", 0 say v2-only → GPL-2+ |
| ppsspp | 5236 files "any later version", 0 v2-only → GPL-2+ |
| dolphin | COPYING states GPLv2+ and "in aggregate … compatible with GPLv3" |

Still open, lower priority:

- **Stella** ships a bare GPL-2 `License.txt` with only thin "or later"
  evidence (3 files). Needs a proper per-file pass before release. Not showing
  as v2-only today, so no action yet.
- **SameBoy**'s Expat grant explicitly **excludes** its `iOS` and `HexFiend`
  directories — we do not build those; do not borrow from them.
- snes9x / genesis_plus_gx / fbneo are non-commercial custom licences, so
  their GPL-version question is moot: they never ship a binary.

## 5. Provenance block (to add to every manifest)

```json
"provenance": {
  "built_from": "https://github.com/libretro/Mesen",
  "upstream_license": "GPL-3.0-or-later",
  "relationship": "independent build of upstream source; not affiliated with, endorsed by, or supported by the upstream project",
  "modifications": "none beyond build configuration"
}
```

Attribution becomes explicit rather than implied by a name.
`THIRD_PARTY_NOTICES.md` stays the index of record.

## 6. Not verified

`web_search` is unavailable in this session, so **no trademark register,
domain, or app-store search was done.** §3 is screened against known software
only. Before a name goes on a public repo it needs a real trademark search.

## 7. Next steps

1. Close §3 (5 swaps) and §4 (confirm Gambatte removal).
2. Rename the private repos to `ezcore-core-<name>`; delete the Gambatte one.
3. Set `name` + add `provenance` in each `cores/<id>/manifest.json`.
4. Regenerate `cores/catalog.json`; re-run `scripts/legal_audit.py`.
5. Revert the `boot_gambatte` CTest entry added while wiring Mesen.
