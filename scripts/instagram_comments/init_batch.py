from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path


def ensure_parent(path: str | Path) -> Path:
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    return file_path


def write_json_if_missing(path: Path, payload: dict) -> None:
    if not path.exists():
        ensure_parent(path).write_text(json.dumps(payload, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Initialize an Instagram comments batch folder.")
    parser.add_argument("--batch", type=int, required=True, help="Batch number, e.g. 1")
    parser.add_argument("--results-limit", type=int, default=30, help="Results limit for the comments actor")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    batch_name = f"batch_{args.batch:03d}"
    batch_dir = Path("data/raw/instagram_comments") / batch_name
    batch_dir.mkdir(parents=True, exist_ok=True)

    readme_path = ensure_parent(batch_dir / "README.txt")
    if not readme_path.exists():
        readme_path.write_text(
            "\n".join(
                [
                    "Source: instagram_comments",
                    f"Stage: {batch_name}",
                    f"Initialized at: {datetime.now().isoformat()}",
                    "Folder ini menyimpan daftar URL post, input actor, hasil scrape JSON, dan metadata run untuk batch komentar Instagram.",
                ]
            ),
            encoding="utf-8",
        )

    write_json_if_missing(
        batch_dir / "ig_comments_input.json",
        {
            "directUrls": [
                "https://www.instagram.com/p/POST_CODE_1/",
                "https://www.instagram.com/p/POST_CODE_2/",
            ],
            "resultsType": "comments",
            "resultsLimit": args.results_limit,
        },
    )


if __name__ == "__main__":
    main()
