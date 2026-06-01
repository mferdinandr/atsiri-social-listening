from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Initialize an Instagram posts batch folder.")
    parser.add_argument("--batch", type=int, required=True, help="Batch number, e.g. 1")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    batch_name = f"batch_{args.batch:03d}"
    batch_dir = Path("data/raw/instagram_posts") / batch_name
    batch_dir.mkdir(parents=True, exist_ok=True)

    readme_path = batch_dir / "README.txt"
    if not readme_path.exists():
        readme_path.write_text(
            "\n".join(
                [
                    "Source: instagram_posts",
                    f"Stage: {batch_name}",
                    f"Initialized at: {datetime.now().isoformat()}",
                    "Batch posts memakai sumber reusable dari all_posts/.",
                    "Tidak perlu scrape ulang posts bila master all_posts sudah final.",
                ]
            ),
            encoding="utf-8",
        )


if __name__ == "__main__":
    main()
