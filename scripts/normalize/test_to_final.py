from __future__ import annotations

import subprocess
from pathlib import Path


SCRIPTS = [
    "scripts/normalize/google_maps.py",
    "scripts/normalize/instagram_posts.py",
    "scripts/normalize/instagram_comments.py",
]


def main() -> None:
    for script in SCRIPTS:
        print(f"[normalize] running {script}")
        subprocess.run(["python3", script], check=True)

    print("[normalize] all test normalization jobs completed")
    print(f"[normalize] outputs available under {Path('data/processed/test').resolve()}")


if __name__ == "__main__":
    main()
