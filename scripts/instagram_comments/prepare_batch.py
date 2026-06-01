from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


def parse_int(value: str | int | None) -> int:
    try:
        return int(value or 0)
    except (TypeError, ValueError):
        return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Prepare an Instagram comments batch from all_posts index.")
    parser.add_argument("--batch", type=int, required=True, help="Batch number, e.g. 1")
    parser.add_argument(
        "--input",
        default="data/raw/instagram_posts/all_posts/ig_post_index.json",
        help="Path to post index JSON",
    )
    parser.add_argument("--limit", type=int, default=10, help="How many post URLs to include")
    parser.add_argument("--min-comments", type=int, default=1, help="Minimum comment count")
    parser.add_argument("--results-limit", type=int, default=30, help="resultsLimit for comments actor")
    parser.add_argument("--exclude-file", help="Optional TXT file containing post URLs to exclude")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    batch_name = f"batch_{args.batch:03d}"
    batch_dir = Path("data/raw/instagram_comments") / batch_name
    batch_dir.mkdir(parents=True, exist_ok=True)

    rows = json.loads(Path(args.input).read_text(encoding="utf-8"))
    excluded_urls: set[str] = set()
    if args.exclude_file:
        exclude_path = Path(args.exclude_file)
        if exclude_path.exists():
            excluded_urls = {
                line.strip()
                for line in exclude_path.read_text(encoding="utf-8").splitlines()
                if line.strip()
            }

    candidates: list[tuple[int, str]] = []
    seen: set[str] = set()
    for row in rows:
        post_url = str(row.get("postUrl") or row.get("url") or "").strip()
        if not post_url or post_url in seen or post_url in excluded_urls:
            continue
        comments_count = parse_int(row.get("commentsCount"))
        if comments_count < args.min_comments:
            continue
        seen.add(post_url)
        candidates.append((comments_count, post_url))

    candidates.sort(key=lambda item: item[0], reverse=True)
    selected_urls = [url for _, url in candidates[: args.limit]]

    txt_path = batch_dir / "comment_post_urls.txt"
    txt_path.write_text("\n".join(selected_urls) + ("\n" if selected_urls else ""), encoding="utf-8")

    json_payload = {
        "directUrls": selected_urls,
        "resultsType": "comments",
        "resultsLimit": args.results_limit,
    }
    json_path = batch_dir / "ig_comments_input.generated.json"
    json_path.write_text(json.dumps(json_payload, indent=2), encoding="utf-8")

    print(f"[instagram_comments] saved {len(selected_urls)} URLs to {txt_path}")
    print(f"[instagram_comments] saved actor input to {json_path}")


if __name__ == "__main__":
    main()
