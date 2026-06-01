from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract Instagram post URLs from a post export or index and build a comments input file."
    )
    parser.add_argument("--input", required=True, help="Path to Instagram post CSV or JSON export")
    parser.add_argument("--output-txt", required=True, help="Path to output TXT with one URL per line")
    parser.add_argument("--output-json", help="Optional path to output actor input JSON")
    parser.add_argument("--limit", type=int, default=10, help="Maximum number of post URLs")
    parser.add_argument("--min-comments", type=int, default=1, help="Only include posts with commentsCount >= this value")
    parser.add_argument(
        "--sort-by-comments",
        action="store_true",
        help="Sort candidate posts by commentsCount descending before applying the limit.",
    )
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


def load_rows(path: str) -> list[dict[str, Any]]:
    input_path = Path(path)
    if input_path.suffix.lower() == ".json":
        payload = json.loads(input_path.read_text(encoding="utf-8"))
        if isinstance(payload, list):
            return [item for item in payload if isinstance(item, dict)]
        if isinstance(payload, dict):
            items = payload.get("items")
            if isinstance(items, list):
                return [item for item in items if isinstance(item, dict)]
            return [payload]
        return []
    return list(csv.DictReader(open(input_path, encoding="utf-8-sig")))


def main() -> None:
    args = parse_args()
    rows = load_rows(args.input)

    candidates: list[tuple[int, str]] = []
    seen: set[str] = set()
    for row in rows:
        url = str(row.get("url") or row.get("postUrl") or "").strip()
        if not url or url in seen:
            continue
        comments_count = parse_int(str(row.get("commentsCount") or "0"))
        if comments_count < args.min_comments:
            continue
        seen.add(url)
        candidates.append((comments_count, url))

    if args.sort_by_comments:
        candidates.sort(key=lambda item: item[0], reverse=True)

    urls = [url for _, url in candidates[: args.limit]]

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
