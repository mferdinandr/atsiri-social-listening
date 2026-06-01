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
    test_dir = Path("data/raw/google_maps/test")
    test_dir.mkdir(parents=True, exist_ok=True)

    readme_path = ensure_parent(test_dir / "README.txt")
    if not readme_path.exists():
        readme_path.write_text(
            "\n".join(
                [
                    "Source: google_maps",
                    "Stage: mini_test",
                    f"Initialized at: {datetime.now().isoformat()}",
                    "Folder ini menyimpan input actor, hasil scrape JSON, dan metadata run untuk mini test Google Maps.",
                    "Folder batch baru dipakai setelah mini test lolos validasi.",
                ]
            ),
            encoding="utf-8",
        )

    write_json_if_missing(
        test_dir / "gmaps_input.json",
        {
            "startUrls": [
                {
                    "url": "https://share.google/eNJCYtgMABpSegL90"
                }
            ],
            "maxCrawledPlacesPerSearch": 1,
            "maxReviews": 20,
            "reviewsSort": "newest",
            "reviewsOrigin": "google",
            "scrapeReviewsPersonalData": True,
            "language": "id",
        },
    )


if __name__ == "__main__":
    main()
