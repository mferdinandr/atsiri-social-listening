from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract Instagram post URLs from a post export and build a batch input file."
    )
    parser.add_argument("--input", required=True, help="Path to Instagram post CSV export")
    parser.add_argument("--output-txt", required=True, help="Path to output TXT with one URL per line")
    parser.add_argument("--output-json", help="Optional path to output actor input JSON")
    parser.add_argument("--limit", type=int, default=10, help="Maximum number of post URLs")
    parser.add_argument("--min-comments", type=int, default=1, help="Only include posts with commentsCount >= this value")
    parser.add_argument(
        "--input-key",
        default="directUrls",
        help="JSON key to use when building output JSON for the actor input",
    )
    return parser.parse_args()


def parse_int(value: str | None) -> int:
    try:
        return int((value or "").strip())
    except ValueError:
        return 0


def main() -> None:
    args = parse_args()
    rows = list(csv.DictReader(open(args.input, encoding="utf-8-sig")))

    urls: list[str] = []
    seen: set[str] = set()
    for row in rows:
        url = (row.get("url") or "").strip()
        if not url or url in seen:
            continue
        comments_count = parse_int(row.get("commentsCount"))
        if comments_count < args.min_comments:
            continue
        seen.add(url)
        urls.append(url)
        if len(urls) >= args.limit:
            break

    output_txt = Path(args.output_txt)
    output_txt.parent.mkdir(parents=True, exist_ok=True)
    output_txt.write_text("\n".join(urls) + ("\n" if urls else ""), encoding="utf-8")
    print(f"[instagram] saved {len(urls)} post URLs to {output_txt}")

    if args.output_json:
        payload = {
            args.input_key: urls,
            "resultsType": "comments",
            "resultsLimit": min(max(len(urls), 1) * 10, 30),
        }
        output_json = Path(args.output_json)
        output_json.parent.mkdir(parents=True, exist_ok=True)
        output_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        print(f"[instagram] saved actor input JSON to {output_json}")


if __name__ == "__main__":
    main()
