"""Read commits from a local repo or a GitHub URL."""
import shutil
import subprocess
import tempfile
from dataclasses import dataclass

SEP = "\x1f"


@dataclass
class Commit:
    sha: str
    author: str
    date: str
    message: str


def is_url(source: str) -> bool:
    return source.startswith(("http://", "https://", "git@"))


def clone(url: str) -> str:
    """Clone a repo into a temp folder (history only, no file contents)."""
    tmp = tempfile.mkdtemp(prefix="commitreel_")
    result = subprocess.run(
        ["git", "clone", "--quiet", "--filter=blob:none", "--no-checkout", url, tmp],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        shutil.rmtree(tmp, ignore_errors=True)
        raise RuntimeError(f"Could not clone {url}:\n{result.stderr.strip()}")
    return tmp


def read_commits(path: str, limit: int = 30, first: bool = False) -> list[Commit]:
    """Return commits oldest -> newest.

    By default the latest `limit` commits; with first=True the first `limit`.
    """
    fmt = SEP.join(["%h", "%an", "%ad", "%s"])
    result = subprocess.run(
        ["git", "-C", path, "log", "--reverse", f"--pretty=format:{fmt}", "--date=short"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"Not a git repo or no commits:\n{result.stderr.strip()}")
    commits = []
    for line in result.stdout.splitlines():
        parts = line.split(SEP)
        if len(parts) == 4:
            commits.append(Commit(*parts))
    return commits[:limit] if first else commits[-limit:]
