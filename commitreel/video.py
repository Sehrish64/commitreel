"""Stitch PNG frames into an mp4 with ffmpeg."""
import shutil
import subprocess
from pathlib import Path


def make_video(frames_dir: Path, output: str, fps: int = 12) -> None:
    if not shutil.which("ffmpeg"):
        raise RuntimeError("ffmpeg not found. Install it from https://ffmpeg.org and try again.")
    cmd = [
        "ffmpeg", "-y", "-loglevel", "error",
        "-framerate", str(fps),
        "-i", str(frames_dir / "f_%05d.png"),
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        output,
    ]
    subprocess.run(cmd, check=True)
