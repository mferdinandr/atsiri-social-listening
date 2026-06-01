from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build a compact reusable Instagram post index from actor output JSON."
    )
    parser.add_argument("--input", required=True, help="Path to ig_posts_output.json")
    parser.add_argument("--output-json", required=True, help="Path to compact post index JSON")
    parser.add_argument("--output-txt", required=True, help="Path to plain TXT list of post URLs")
    return parser.parse_args()


def load_records(path: str) -> list[dict[str, Any]]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    if isinstance(payload, dict):
        items = payload.get("items")
        if isinstance(items, list):
            return [item for item in items if isinstance(item, dict)]
        return [payload]
    return []


def parse_int(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def main() -> None:
    args = parse_args()
    rows = load_records(args.input)

    seen: set[str] = set()
    index_rows: list[dict[str, Any]] = []
    urls: list[str] = []

    for row in rows:
        post_url = str(row.get("url") or "").strip()
        if not post_url or post_url in seen:
            continue
        seen.add(post_url)

        item = {
            "postId": row.get("id"),
            "postUrl": post_url,
            "shortCode": row.get("shortCode"),
            "inputUrl": row.get("inputUrl"),
            "username": row.get("username"),
            "ownerUsername": row.get("ownerUsername"),
            "timestamp": row.get("timestamp"),
            "type": row.get("type"),
            "commentsCount": parse_int(row.get("commentsCount")),
            "likesCount": parse_int(row.get("likesCount")),
            "isCommentsDisabled": row.get("isCommentsDisabled"),
            "caption": row.get("caption"),
        }
        index_rows.append(item)
        urls.append(post_url)

    output_json = Path(args.output_json)
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(index_rows, indent=2, ensure_ascii=False), encoding="utf-8")

    output_txt = Path(args.output_txt)
    output_txt.parent.mkdir(parents=True, exist_ok=True)
    output_txt.write_text("\n".join(urls) + ("\n" if urls else ""), encoding="utf-8")

    print(f"[instagram] indexed {len(index_rows)} unique posts")
    print(f"[instagram] saved JSON index to {output_json}")
    print(f"[instagram] saved URL list to {output_txt}")


if __name__ == "__main__":
    main()
