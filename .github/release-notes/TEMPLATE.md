# Release notes template — copy to `<tag>.md` (e.g. `v0.1.1.md`)

<!--
House style for ezCORE release notes. Keep it honest: a release that says
what does NOT work earns more trust than one that overpromises. The CI
workflow attaches `.github/release-notes/<tag>.md` to the GitHub Release
when present, else falls back to generated notes.
-->

# ezCORE <tag> — <one-line title>

<One honest paragraph: what this release is, what changed since the last
one, and the single most important caveat.>

## What's in this build

| Platform | Artifact | Notes |
|---|---|---|
| macOS arm64 | `ezcore-<version>-macos-arm64.zip` | <signed how / verified where> |
| Android arm64 | `ezcore-<version>-android-arm64.apk` | <signed how / verified where> |
| Windows / Linux | — | <reason, if absent> |

- Cores bundled: <n> (<list the additions/removals vs previous release>)
- Verification level: <render-verified count> render-verified,
  <identify count> load-and-identify — details in `docs/MATRIX.md`.

## Known limitations

- <every platform/feature that is not done yet — do not omit this section>

## Verifying your download

```
<sha256 lines — paste from SHA256SUMS.txt>
```

## Reporting

- **Found a bug?** Open an issue (bug template) with your platform + the
  exact steps.
- **Fixed it?** PRs are welcome — see `CONTRIBUTING.md`.
- This is still an early build: if something looks wrong, it probably is —
  tell us.
