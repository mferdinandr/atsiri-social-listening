from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from scripts.normalize.common import now_iso, parse_int, parse_iso


HEADERS = [
    "comment_id",
    "post_id",
    "post_url",
    "comment_date",
    "commenter_username",
    "comment_text",
    "comment_like_count",
    "scraped_at",
    "batch_number",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Normalize Instagram comments raw JSON into processed CSV.")
    parser.add_argument("--raw-path", default="data/raw/instagram_comments/test/ig_comments_output.json")
    parser.add_argument("--posts-index-path", default="data/raw/instagram_posts/all_posts/ig_post_index.json")
    parser.add_argument("--output-path", default="data/processed/test/instagram_comments/instagram_comments.csv")
    parser.add_argument("--batch-number", default="", help="Batch number label, e.g. batch_001")
    return parser.parse_args()


def write_csv(path: Path, headers: list[str], rows: list[dict[str, str | int]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    args = parse_args()
    comments_path = Path(args.raw_path)
    posts_index_path = Path(args.posts_index_path)
    output_path = Path(args.output_path)

    comments = json.loads(comments_path.read_text(encoding="utf-8"))
    post_index = json.loads(posts_index_path.read_text(encoding="utf-8"))
    normalized_at = now_iso()

    post_lookup = {
        str(row.get("postUrl") or ""): str(row.get("postId") or "")
        for row in post_index
    }

    output_rows: list[dict[str, str | int]] = []
    for row in comments:
        post_url = str(row.get("postUrl") or "")
        output_rows.append(
            {
                "comment_id": str(row.get("id") or ""),
                "post_id": post_lookup.get(post_url, ""),
                "post_url": post_url,
                "comment_date": parse_iso(row.get("timestamp")),
                "commenter_username": str(row.get("ownerUsername") or ""),
                "comment_text": str(row.get("text") or ""),
                "comment_like_count": parse_int(row.get("likesCount")),
                "scraped_at": normalized_at,
                "batch_number": args.batch_number,
            }
        )

    write_csv(output_path, HEADERS, output_rows)
    print(f"[normalize] saved {len(output_rows)} comment rows to {output_path}")


if __name__ == "__main__":
    main()
