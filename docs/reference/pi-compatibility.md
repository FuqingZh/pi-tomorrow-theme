# Pi version compatibility

**Minimum supported Pi version: 0.99.0.** This is the first Pi release that
understands the whole theme configuration, including each variant's declared
`appearance` (`light` or `dark`). It is not a claim that earlier versions
cannot load these palettes.

## Evidence

Tests used official Linux x64 Pi release binaries in temporary directories.
Each version installed `npm:pi-tomorrow-theme@0.2.0` in an isolated
`PI_CODING_AGENT_DIR`. Each variant was selected in settings and a fresh copy
of the synthetic session in `test/fixtures/preview.jsonl` was replayed
offline. The PTY output was checked for the expected ANSI colors on the
heading, inline code, syntax comment, added and removed diff lines, user
message, successful tool result, and failed tool result.

| Pi version | Install and basic rendering | Theme field support |
| --- | --- | --- |
| 0.84.4 | All five variants, all eight ANSI checks | Does not use `scrollbarTrack`; the thumb uses the older background slot. No `appearance`. |
| 0.85.0 and 0.87.1 | All five variants, all eight ANSI checks on each version | Current scrollbar color roles, but no `appearance`. |
| 0.99.0 | All five variants, all eight ANSI checks; checkout suite also passed | First release with `appearance`. |
| 1.5.2 | All five variants, all eight ANSI checks with the checkout-based suite | All theme fields supported. |

The scrollbar and appearance boundaries come from Pi's
[0.84.4 theme loader][old], [0.85.0 theme schema][mid], and
[0.99.0 release notes][minimum]. The transcript replay did not test fullscreen
scrollbars or terminal light/dark transitions. Earlier releases are not part
of the support contract.

## Recheck

Run `python3 test/check.py` with a target Pi binary on `PATH` for current
checkout rendering coverage. For the published-package check, use the target
Pi binary to run `pi install npm:pi-tomorrow-theme@0.2.0` under a throwaway
`PI_CODING_AGENT_DIR`, then select each variant via `settings.json` and start
Pi with a scratch copy of `test/fixtures/preview.jsonl` via `--session`.
Retest the boundary when adding any theme fields or changing the manifest.

[old]: https://github.com/earendil-works/pi/blob/v0.84.4/packages/coding-agent/src/modes/interactive/theme/theme.ts
[mid]: https://github.com/earendil-works/pi/blob/v0.85.0/packages/coding-agent/src/modes/interactive/theme/theme-json.ts
[minimum]: https://github.com/earendil-works/pi/releases/tag/v0.99.0
