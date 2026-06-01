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
    test_dir = Path("data/raw/instagram_comments/test")
    test_dir.mkdir(parents=True, exist_ok=True)

    readme_path = ensure_parent(test_dir / "README.txt")
    if not readme_path.exists():
        readme_path.write_text(
            "\n".join(
                [
                    "Source: instagram_comments",
                    "Stage: mini_test",
                    f"Initialized at: {datetime.now().isoformat()}",
                    "Folder ini menyimpan input actor, daftar URL post, hasil scrape JSON, dan metadata run untuk mini test komentar Instagram.",
                    "Folder batch baru dipakai setelah mini test lolos validasi.",
                ]
            ),
            encoding="utf-8",
        )

    write_json_if_missing(
        test_dir / "ig_comments_input.json",
        {
            "directUrls": [
                "https://www.instagram.com/p/POST_CODE_1/",
                "https://www.instagram.com/p/POST_CODE_2/",
            ],
            "resultsType": "comments",
            "resultsLimit": 30,
        },
    )


if __name__ == "__main__":
    main()
