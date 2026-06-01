from __future__ import annotations

import csv
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from scripts.normalize.common import evaluate_text


def read_csv(path: str) -> list[dict[str, str]]:
    with Path(path).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: str, headers: list[str], rows: list[dict[str, str | int]]) -> None:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def append_text_audit(rows: list[dict[str, str]], text_key: str, mode: str) -> tuple[list[dict[str, str | int]], list[dict[str, str | int]], dict[str, int]]:
    output_all: list[dict[str, str | int]] = []
    output_clean: list[dict[str, str | int]] = []
    clean_count = 0
    empty_count = 0
    invalid_count = 0

    for row in rows:
        clean_text, word_count, is_valid, filter_reason = evaluate_text(row.get(text_key))
        if is_valid:
            clean_count += 1
        elif filter_reason == "empty_text":
            empty_count += 1
            invalid_count += 1
        else:
            invalid_count += 1

        payload = dict(row)
        if mode == "caption":
            payload.update(
                {
                    "caption_word_count": word_count,
                    "is_valid_caption": "true" if is_valid else "false",
                    "filter_reason": filter_reason,
                    "clean_caption": clean_text,
                }
            )
        else:
            payload.update(
                {
                    "text_word_count": word_count,
                    "is_valid_text": "true" if is_valid else "false",
                    "filter_reason": filter_reason,
                    "clean_text": clean_text,
                }
            )
        output_all.append(payload)
        if is_valid:
            output_clean.append(payload)

    stats = {
        "raw_count": len(rows),
        "clean_count": clean_count,
        "duplicate_count": 0,
        "empty_text_count": empty_count,
        "invalid_text_count": invalid_count,
    }
    return output_all, output_clean, stats


def build_batch_rows(
    gmaps_stats: dict[str, int],
    comments_stats: dict[str, int],
) -> list[dict[str, str | int]]:
    return [
        {
            "batch_number": "test",
            "source": "google_maps",
            "target_data": "gmaps_reviews",
            "started_at": "",
            "finished_at": "",
            **gmaps_stats,
            "status": "passed",
            "notes": "Mini test Google Maps",
        },
        {
            "batch_number": "test",
            "source": "instagram",
            "target_data": "instagram_comments",
            "started_at": "",
            "finished_at": "",
            **comments_stats,
            "status": "passed",
            "notes": "Mini test Instagram comments",
        },
    ]


def write_summary(path: str, gmaps_stats: dict[str, int], posts_stats: dict[str, int], comments_stats: dict[str, int]) -> None:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        "\n".join(
            [
                "# Final Test Summary",
                "",
                "Tahap ini menunjukkan bentuk output final yang akan dipakai sebelum masuk batch produksi.",
                "",
                "## Ringkasan",
                f"- Google Maps reviews raw: {gmaps_stats['raw_count']}",
                f"- Google Maps reviews clean valid: {gmaps_stats['clean_count']}",
                f"- Instagram posts raw: {posts_stats['raw_count']}",
                f"- Instagram posts valid caption: {posts_stats['clean_count']}",
                f"- Instagram comments raw: {comments_stats['raw_count']}",
                f"- Instagram comments clean valid: {comments_stats['clean_count']}",
                "",
                "## File final test",
                "- `data/datasets/all/test/gmaps_reviews_all.csv`",
                "- `data/datasets/clean/test/gmaps_reviews_clean.csv`",
                "- `data/datasets/all/shared/instagram_posts_all.csv`",
                "- `data/datasets/clean/shared/instagram_posts_clean.csv`",
                "- `data/datasets/all/test/instagram_comments_all.csv`",
                "- `data/datasets/clean/test/instagram_comments_clean.csv`",
                "- `scraping_batches_test.csv`",
                "",
                "## Catatan",
                "- Folder `data/datasets/all` berisi semua row hasil scrape plus audit filter.",
                "- Folder `data/datasets/clean` hanya berisi row yang valid untuk NLP.",
                "- Instagram posts diperlakukan sebagai dataset shared, tidak diulang per batch.",
                "- Kolom `batch_number` masih `test` karena belum masuk `batch_001`.",
                "- Field yang memang tidak tersedia dari raw tetap tidak dipaksakan muncul.",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    gmaps_reviews = read_csv("data/processed/test/google_maps/gmaps_reviews.csv")
    gmaps_reviewers = read_csv("data/processed/test/google_maps/gmaps_reviewers.csv")
    instagram_posts = read_csv("data/processed/test/instagram_posts/instagram_posts.csv")
    instagram_comments = read_csv("data/processed/test/instagram_comments/instagram_comments.csv")

    gmaps_reviews_all, gmaps_reviews_clean, gmaps_stats = append_text_audit(gmaps_reviews, "review_text", "text")
    instagram_posts_all, instagram_posts_clean, posts_stats = append_text_audit(instagram_posts, "caption", "caption")
    instagram_comments_all, instagram_comments_clean, comments_stats = append_text_audit(instagram_comments, "comment_text", "text")

    write_csv(
        "data/datasets/all/test/gmaps_reviews_all.csv",
        list(gmaps_reviews_all[0].keys()) if gmaps_reviews_all else [],
        gmaps_reviews_all,
    )
    write_csv(
        "data/datasets/clean/test/gmaps_reviews_clean.csv",
        list(gmaps_reviews_clean[0].keys()) if gmaps_reviews_clean else [],
        gmaps_reviews_clean,
    )
    write_csv(
        "data/datasets/all/shared/instagram_posts_all.csv",
        list(instagram_posts_all[0].keys()) if instagram_posts_all else [],
        instagram_posts_all,
    )
    write_csv(
        "data/datasets/clean/shared/instagram_posts_clean.csv",
        list(instagram_posts_clean[0].keys()) if instagram_posts_clean else [],
        instagram_posts_clean,
    )
    write_csv(
        "data/datasets/all/test/instagram_comments_all.csv",
        list(instagram_comments_all[0].keys()) if instagram_comments_all else [],
        instagram_comments_all,
    )
    write_csv(
        "data/datasets/clean/test/instagram_comments_clean.csv",
        list(instagram_comments_clean[0].keys()) if instagram_comments_clean else [],
        instagram_comments_clean,
    )

    batch_rows = build_batch_rows(gmaps_stats, comments_stats)
    write_csv(
        "data/final/test/scraping_batches_test.csv",
        list(batch_rows[0].keys()) if batch_rows else [],
        batch_rows,
    )
    write_summary("data/final/test/final_test_summary.md", gmaps_stats, posts_stats, comments_stats)

    print("[finalize] saved shared instagram posts, test datasets, and summaries")


if __name__ == "__main__":
    main()
