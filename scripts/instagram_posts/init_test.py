from __future__ import annotations

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


def main() -> None:
    test_dir = Path("data/raw/instagram_posts/test")
    test_dir.mkdir(parents=True, exist_ok=True)

    readme_path = ensure_parent(test_dir / "README.txt")
    if not readme_path.exists():
        readme_path.write_text(
            "\n".join(
                [
                    "Source: instagram_posts",
                    "Stage: mini_test",
                    f"Initialized at: {datetime.now().isoformat()}",
                    "Folder ini menyimpan input actor untuk mini test posts Instagram.",
                    "Output master posts disimpan ke folder all_posts/ karena reusable lintas test dan batch.",
                ]
            ),
            encoding="utf-8",
        )

    write_json_if_missing(
        test_dir / "ig_posts_input.json",
        {
            "directUrls": [
                "https://www.instagram.com/rumahatsiri/"
            ],
            "resultsType": "posts",
            "resultsLimit": 1500,
            "addParentData": True,
        },
    )


if __name__ == "__main__":
    main()
