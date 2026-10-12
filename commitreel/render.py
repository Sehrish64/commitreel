"""Draw one commit at a time as a typewriter-style frame."""
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from .git_reader import Commit

BG = (13, 17, 23)
PANEL = (22, 27, 34)
TEXT = (230, 237, 243)
MUTED = (125, 133, 144)
GREEN = (63, 185, 80)
BLUE = (88, 166, 255)

FONT_CANDIDATES = [
    "DejaVuSansMono.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    "/System/Library/Fonts/Menlo.ttc",
    "C:/Windows/Fonts/consola.ttf",
]


def load_font(size: int):
    for name in FONT_CANDIDATES:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default(size)


def draw_frame(commit: Commit, index: int, total: int, typed: int, size, title: str) -> Image.Image:
    w, h = size
    img = Image.new("RGB", size, BG)
    d = ImageDraw.Draw(img)
    pad = int(w * 0.07)

    small = load_font(int(w * 0.035))
    medium = load_font(int(w * 0.045))
    big = load_font(int(w * 0.07))

    # header
    d.text((pad, pad), title, font=medium, fill=BLUE)
    d.text((pad, pad + int(w * 0.07)), f"commit {index + 1} / {total}", font=small, fill=MUTED)

    # progress bar
    bar_y = pad + int(w * 0.14)
    d.rounded_rectangle((pad, bar_y, w - pad, bar_y + 14), radius=7, fill=PANEL)
    filled = int((w - 2 * pad) * (index + 1) / total)
    d.rounded_rectangle((pad, bar_y, pad + filled, bar_y + 14), radius=7, fill=GREEN)

    # commit card
    card_top = int(h * 0.3)
    card_bottom = int(h * 0.78)
    d.rounded_rectangle((pad, card_top, w - pad, card_bottom), radius=24, fill=PANEL)

    x = pad + int(w * 0.05)
    y = card_top + int(w * 0.05)
    d.text((x, y), f"{commit.sha}", font=medium, fill=GREEN)
    y += int(w * 0.075)
    d.text((x, y), f"{commit.author}  ·  {commit.date}", font=small, fill=MUTED)
    y += int(w * 0.09)

    shown = commit.message[:typed]
    cursor = "█" if typed < len(commit.message) else ""
    max_chars = max(10, int((w - 2 * x) / (w * 0.07 * 0.6)))
    line_h = int(w * 0.1)
    # Keep text inside the card: cap lines, truncate with ellipsis.
    max_lines = max(2, int((card_bottom - y - pad // 2) / line_h))
    lines = textwrap.wrap(shown + cursor, width=max_chars) or [cursor]
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = lines[-1][: max(0, max_chars - 1)] + "…"
    for line in lines:
        d.text((x, y), line, font=big, fill=TEXT)
        y += line_h

    d.text((pad, h - pad - int(w * 0.04)), "made with commitreel", font=small, fill=MUTED)
    return img


def render_frames(commits, out_dir: Path, size=(720, 1280), fps=12, title="my repo"):
    """Write numbered PNG frames; return how many were written."""
    out_dir.mkdir(parents=True, exist_ok=True)
    chars_per_frame = 2
    hold_frames = fps  # 1 second pause after each message
    n = 0
    for i, commit in enumerate(commits):
        typed = 0
        while typed < len(commit.message):
            typed += chars_per_frame
            n += 1
            draw_frame(commit, i, len(commits), typed, size, title).save(out_dir / f"f_{n:05d}.png")
        final = draw_frame(commit, i, len(commits), len(commit.message), size, title)
        for _ in range(hold_frames):
            n += 1
            final.save(out_dir / f"f_{n:05d}.png")
    return n
