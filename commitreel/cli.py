import argparse
import shutil
import sys
import tempfile
from pathlib import Path

from . import __version__
from .git_reader import clone, is_url, read_commits
from .render import render_frames
from .video import make_video


def parse_size(text: str):
    w, h = text.lower().split("x")
    return int(w), int(h)


def main():
    p = argparse.ArgumentParser(
        prog="commitreel",
        description="Turn your Git commit history into a video.",
    )
    p.add_argument("source", help="GitHub URL or path to a local git repo")
    p.add_argument("-o", "--output", default="commitreel.mp4", help="output video file")
    p.add_argument("-n", "--limit", type=int, default=20, help="number of commits to show (default 20)")
    p.add_argument("--first", action="store_true", help="use the FIRST n commits instead of the latest")
    p.add_argument("--size", default="720x1280", help="video size, default 720x1280 (vertical, for Shorts/Reels)")
    p.add_argument("--fps", type=int, default=12)
    p.add_argument("--keep-frames", action="store_true", help="keep PNG frames (no video is made if ffmpeg is missing)")
    p.add_argument("--version", action="version", version=__version__)
    args = p.parse_args()

    cloned = None
    try:
        path = args.source
        if is_url(args.source):
            print("Cloning repo history...")
            path = cloned = clone(args.source)

        commits = read_commits(path, args.limit, args.first)
        if not commits:
            sys.exit("No commits found.")
        title = args.source.rstrip("/").split("/")[-1].removesuffix(".git") or "repo"
        if not is_url(args.source):
            title = Path(args.source).resolve().name

        frames_dir = Path(tempfile.mkdtemp(prefix="commitreel_frames_"))
        print(f"Rendering {len(commits)} commits...")
        total = render_frames(commits, frames_dir, parse_size(args.size), args.fps, title)
        print(f"Rendered {total} frames.")

        try:
            make_video(frames_dir, args.output, args.fps)
            print(f"Done: {args.output}")
        except RuntimeError as e:
            print(e)
            args.keep_frames = True

        if args.keep_frames:
            print(f"Frames kept in: {frames_dir}")
        else:
            shutil.rmtree(frames_dir, ignore_errors=True)
    except RuntimeError as e:
        sys.exit(str(e))
    finally:
        if cloned:
            shutil.rmtree(cloned, ignore_errors=True)
