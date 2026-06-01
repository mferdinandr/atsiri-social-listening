from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from scripts.normalize.common import extract_hashtags, extract_mentions, now_iso, parse_int, parse_iso, serialize_list


HEADERS = [
    "post_id",
    "post_url",
    "post_date",
    "post_type",
    "caption",
    "like_count",
    "comment_count",
    "view_count",
    "hashtag_list",
    "mention_list",
    "scraped_at",
    "batch_number",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Normalize Instagram posts raw JSON into processed CSV.")
    parser.add_argument("--raw-path", default="data/raw/instagram_posts/all_posts/ig_posts_output.json")
    parser.add_argument("--output-path", default="data/processed/test/instagram_posts/instagram_posts.csv")
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
    raw_path = Path(args.raw_path)
    output_path = Path(args.output_path)

    rows = json.loads(raw_path.read_text(encoding="utf-8"))
    normalized_at = now_iso()

    output_rows: list[dict[str, str | int]] = []
    seen_urls: set[str] = set()

    for row in rows:
        post_url = str(row.get("url") or row.get("postUrl") or "").strip()
        if not post_url or post_url in seen_urls:
            continue
        seen_urls.add(post_url)

        caption = str(row.get("caption") or "")
        hashtags = row.get("hashtags") if isinstance(row.get("hashtags"), list) else extract_hashtags(caption)
        mentions = row.get("mentions") if isinstance(row.get("mentions"), list) else extract_mentions(caption)

        view_count = row.get("videoViewCount")
        if view_count in (None, ""):
            view_count = row.get("videoPlayCount")

        output_rows.append(
            {
                "post_id": str(row.get("id") or row.get("postId") or ""),
                "post_url": post_url,
                "post_date": parse_iso(row.get("timestamp")),
                "post_type": str(row.get("type") or ""),
                "caption": caption,
                "like_count": parse_int(row.get("likesCount")),
                "comment_count": parse_int(row.get("commentsCount")),
                "view_count": parse_int(view_count) if view_count not in (None, "") else "",
                "hashtag_list": serialize_list([str(item) for item in hashtags]),
                "mention_list": serialize_list([str(item) for item in mentions]),
                "scraped_at": normalized_at,
                "batch_number": args.batch_number,
            }
        )

    write_csv(output_path, HEADERS, output_rows)
    print(f"[normalize] saved {len(output_rows)} post rows to {output_path}")


if __name__ == "__main__":
    main()
