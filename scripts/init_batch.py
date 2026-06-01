from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path

from common import ensure_parent


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Initialize batch folders for mini test.")
    parser.add_argument("--source", required=True, choices=["google_maps", "instagram"])
    parser.add_argument("--batch", required=True, type=int)
    return parser.parse_args()


def write_json_if_missing(path: Path, payload: dict) -> None:
    if not path.exists():
        ensure_parent(path).write_text(json.dumps(payload, indent=2), encoding="utf-8")


def main() -> None:
    args = parse_args()
    batch_code = f"batch_{args.batch:03d}"
    batch_dir = Path("data/raw") / args.source / batch_code
    batch_dir.mkdir(parents=True, exist_ok=True)

    readme_path = ensure_parent(batch_dir / "README.txt")
    if not readme_path.exists():
        readme_path.write_text(
            "\n".join(
                [
                    f"Source: {args.source}",
                    f"Batch: {batch_code}",
                    f"Initialized at: {datetime.now().isoformat()}",
                    "Taruh file export mentah (JSON/CSV/XLSX) di folder ini.",
                    "Simpan juga catatan manual jika ada field yang gagal diambil.",
                ]
            ),
            encoding="utf-8",
        )

    if args.source == "google_maps":
        write_json_if_missing(
            batch_dir / "apify_input.example.json",
            {
                "searchStringsArray": ["Rumah Atsiri Indonesia"],
                "maxCrawledPlacesPerSearch": 1,
                "maxReviews": 20,
                "reviewsSort": "newest",
                "language": "id",
            },
        )

    if args.source == "instagram":
        write_json_if_missing(
            batch_dir / "apify_posts_input.example.json",
            {
                "directUrls": [
                    "https://www.instagram.com/p/POST_CODE_1/",
                    "https://www.instagram.com/p/POST_CODE_2/",
                ],
                "resultsLimit": 10,
            },
        )
        write_json_if_missing(
            batch_dir / "apify_comments_input.example.json",
            {
                "directUrls": [
                    "https://www.instagram.com/p/POST_CODE_1/",
                    "https://www.instagram.com/p/POST_CODE_2/",
                ],
                "resultsLimit": 30,
            },
        )


if __name__ == "__main__":
    main()
