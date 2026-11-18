"""Check Tomorrow variant contrast and replay a synthetic session in a real Pi TUI."""

import fcntl
import json
import os
from pathlib import Path
import pty
import re
import select
import shutil
import struct
import subprocess
import tempfile
import termios
import time


ROOT = Path(__file__).resolve().parents[1]
THEMES = ROOT / "themes"
EXPECTED_VARIANTS = {
    "tomorrow": ("light", "#8e908c"),
    "tomorrow-night": ("dark", "#969896"),
    "tomorrow-night-eighties": ("dark", "#999999"),
    "tomorrow-night-blue": ("dark", "#7285b7"),
    "tomorrow-night-bright": ("dark", "#969896"),
}
FIXTURE = ROOT / "test" / "fixtures" / "preview.jsonl"
MARKERS = (
    b"Show the build, smoke test, and edit summary.",
    b"Build finished: 12 modules compiled.",
    b"Smoke test failed: expected HTTP 200, received HTTP 503.",
    b"Build review",
    b"Keep the current release until the smoke test passes.",
    b"https://example.com/guide",
    b"export function retry(max = 2)",
    b"- 2 export const retries = 1;",
    b"+ 2 export const retries = 2;",
)
ANSI = re.compile(rb"\x1b\][^\x1b\x07]*(?:\x07|\x1b\\)|\x1b\[[0-?]*[ -/]*[@-~]")


def color(theme, role):
    return theme["vars"].get(role, role)


def rgb(hex_color):
    return tuple(bytes.fromhex(hex_color.removeprefix("#")))


def luminance(hex_color):
    channels = (v / 255 for v in rgb(hex_color))
    r, g, b = (v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in channels)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def check_contrast(theme):
    colors = theme["colors"]
    pairs = [(role, "background") for role in (
        "text", "muted", "thinkingText", "mdHeading", "mdLink", "mdCode", "mdQuote"
    )]
    pairs += [("text", "selectedBg"), ("userMessageText", "userMessageBg"),
              ("customMessageText", "customMessageBg"), ("searchMatchText", "searchMatchBg")]
    pairs += [(role, surface)
              for role in ("toolTitle", "toolOutput", "toolDiffContext", "toolDiffAdded", "toolDiffRemoved")
              for surface in ("toolPendingBg", "toolSuccessBg", "toolErrorBg")]
    for foreground, background in pairs:
        light, dark = sorted((luminance(color(theme, colors[foreground])),
                              luminance(color(theme, colors.get(background, background)))), reverse=True)
        ratio = (light + 0.05) / (dark + 0.05)
        assert ratio >= 4.5, f"{foreground} on {background}: {ratio:.2f}:1"
    print(f"{theme['name']}: {len(pairs)} foreground/background pairs meet 4.5:1", flush=True)


def replay(theme_name):
    # A disposable profile and session avoid applying the test theme or writing to user settings.
    with tempfile.TemporaryDirectory(prefix="pi-tomorrow-check-") as tmp:
        session = Path(tmp) / FIXTURE.name
        shutil.copyfile(FIXTURE, session)
        env = {**os.environ, "PI_CODING_AGENT_DIR": str(Path(tmp) / "agent"), "PI_OFFLINE": "1",
               "TERM": "xterm-256color", "COLORTERM": "truecolor"}
        for key in ("NO_COLOR", "TMUX", "TMUX_PANE", "TERM_PROGRAM"):
            env.pop(key, None)
        master, slave = pty.openpty()
        data = bytearray()
        try:
            fcntl.ioctl(slave, termios.TIOCSWINSZ, struct.pack("HHHH", 55, 108, 0, 0))
            with subprocess.Popen(
                ["pi", "--no-extensions", "--no-skills", "--theme", str(THEMES),
                 "--use-theme", theme_name, "--session", str(session)],
                cwd=tmp, env=env, stdin=slave, stdout=slave, stderr=slave,
            ) as process:
                try:
                    deadline = time.monotonic() + 5
                    while process.poll() is None and time.monotonic() < deadline:
                        if select.select([master], [], [], 0.1)[0]:
                            data.extend(os.read(master, 65536))
                        if all(marker in ANSI.sub(b"", data) for marker in MARKERS):
                            break
                finally:
                    if process.poll() is None:
                        process.terminate()
                        try:
                            process.wait(timeout=2)
                        except subprocess.TimeoutExpired:
                            process.kill()
                            process.wait()
        finally:
            os.close(master)
            os.close(slave)
    return bytes(data)


def check_sample_text(name, rendered):
    assert b"Failed to load theme" not in rendered, name
    visible = ANSI.sub(b"", rendered)
    for marker in MARKERS:
        assert marker in visible, f"{name}: missing {marker!r}"


def check_rendering(theme):
    name = theme["name"]
    rendered = replay(name)
    check_sample_text(name, rendered)

    for role, layer, marker in (
        ("mdHeading", 38, b"Build review"), ("mdCode", 38, b"src/settings.ts before deploying"),
        ("syntaxComment", 38, b"// Network settings"),
        ("toolDiffAdded", 38, b"+ 2 export const retries = 2;"),
        ("toolDiffRemoved", 38, b"- 2 export const retries = 1;"),
        ("userMessageBg", 48, b"Show the build, smoke test, and edit summary."),
        ("toolSuccessBg", 48, b"Build finished: 12 modules compiled."),
        ("toolErrorBg", 48, b"Smoke test failed: expected HTTP 200, received HTTP 503."),
    ):
        r, g, b = rgb(color(theme, theme["colors"][role]))
        sgr = f"\x1b[{layer};2;{r};{g};{b}m".encode()
        assert any(sgr in line and marker in ANSI.sub(b"", line)
                   for line in rendered.split(b"\n")), f"{name}: missing {role} on {marker!r}"
    print(f"{name}: Pi TUI replayed the fixture and used eight expected styles", flush=True)


if __name__ == "__main__":
    actual = {path.stem for path in THEMES.glob("*.json")}
    assert actual == EXPECTED_VARIANTS.keys(), f"Unexpected theme set: {actual}"
    check_sample_text("dark", replay("dark"))
    for name, (appearance, upstream_comment) in EXPECTED_VARIANTS.items():
        theme = json.loads((THEMES / f"{name}.json").read_text())
        assert theme["name"] == name and theme["appearance"] == appearance, name
        assert color(theme, theme["colors"]["syntaxComment"]) == upstream_comment, name
        check_contrast(theme)
        check_rendering(theme)
