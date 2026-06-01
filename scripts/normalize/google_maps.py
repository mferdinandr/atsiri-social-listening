from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from scripts.normalize.common import now_iso, parse_bool, parse_int, parse_iso


REVIEW_HEADERS = [
    "review_id",
    "reviewer_id",
    "review_date",
    "rating",
    "review_text",
    "review_like_count",
    "owner_response_text",
    "owner_response_date",
    "review_url",
    "scraped_at",
    "batch_number",
]

REVIEWER_HEADERS = [
    "reviewer_id",
    "reviewer_name",
    "reviewer_profile_url",
    "reviewer_photo_url",
    "is_local_guide",
    "reviewer_total_reviews",
    "scraped_at",
    "batch_number",
]


def write_csv(path: Path, headers: list[str], rows: list[dict[str, str | int]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    raw_path = Path("data/raw/google_maps/test/gmaps_output.json")
    reviews_output = Path("data/processed/test/google_maps/gmaps_reviews.csv")
    reviewers_output = Path("data/processed/test/google_maps/gmaps_reviewers.csv")

    rows = json.loads(raw_path.read_text(encoding="utf-8"))
    normalized_at = now_iso()

    review_rows: list[dict[str, str | int]] = []
    reviewer_map: dict[str, dict[str, str | int]] = {}

    for row in rows:
        scraped_at = parse_iso(row.get("scrapedAt")) or normalized_at
        review_rows.append(
            {
                "review_id": str(row.get("reviewId") or ""),
                "reviewer_id": str(row.get("reviewerId") or ""),
                "review_date": parse_iso(row.get("publishedAtDate")),
                "rating": parse_int(row.get("stars")),
                "review_text": str(row.get("text") or ""),
                "review_like_count": parse_int(row.get("likesCount")),
                "owner_response_text": str(row.get("responseFromOwnerText") or ""),
                "owner_response_date": parse_iso(row.get("responseFromOwnerDate")),
                "review_url": str(row.get("reviewUrl") or ""),
                "scraped_at": scraped_at,
                "batch_number": "",
            }
        )

        reviewer_id = str(row.get("reviewerId") or "")
        if reviewer_id and reviewer_id not in reviewer_map:
            reviewer_map[reviewer_id] = {
                "reviewer_id": reviewer_id,
                "reviewer_name": str(row.get("name") or ""),
                "reviewer_profile_url": str(row.get("reviewerUrl") or ""),
                "reviewer_photo_url": str(row.get("reviewerPhotoUrl") or ""),
                "is_local_guide": parse_bool(row.get("isLocalGuide")),
                "reviewer_total_reviews": parse_int(row.get("reviewerNumberOfReviews")),
                "scraped_at": scraped_at,
                "batch_number": "",
            }

    write_csv(reviews_output, REVIEW_HEADERS, review_rows)
    write_csv(reviewers_output, REVIEWER_HEADERS, list(reviewer_map.values()))

    print(f"[normalize] saved {len(review_rows)} review rows to {reviews_output}")
    print(f"[normalize] saved {len(reviewer_map)} reviewer rows to {reviewers_output}")


if __name__ == "__main__":
    main()
