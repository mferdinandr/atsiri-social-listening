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
    parser = argparse.ArgumentParser(description="Initialize a Google Maps batch folder.")
    parser.add_argument("--batch", type=int, required=True, help="Batch number, e.g. 1")
    parser.add_argument("--max-reviews", type=int, default=100, help="Max reviews for this batch")
    parser.add_argument(
        "--url",
        default="https://maps.app.goo.gl/Ns1U71ajdFzcNmLR6",
        help="Google Maps place URL",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    batch_name = f"batch_{args.batch:03d}"
    batch_dir = Path("data/raw/google_maps") / batch_name
    batch_dir.mkdir(parents=True, exist_ok=True)

    readme_path = ensure_parent(batch_dir / "README.txt")
    if not readme_path.exists():
        readme_path.write_text(
            "\n".join(
                [
                    "Source: google_maps",
                    f"Stage: {batch_name}",
                    f"Initialized at: {datetime.now().isoformat()}",
                    "Folder ini menyimpan input actor, hasil scrape JSON, dan metadata run untuk batch validasi Google Maps.",
                ]
            ),
            encoding="utf-8",
        )

    write_json_if_missing(
        batch_dir / "gmaps_input.json",
        {
            "startUrls": [{"url": args.url}],
            "maxCrawledPlacesPerSearch": 1,
            "maxReviews": args.max_reviews,
            "reviewsSort": "newest",
            "reviewsOrigin": "google",
            "scrapeReviewsPersonalData": True,
            "language": "id",
        },
    )


if __name__ == "__main__":
    main()
