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


def build_gmaps_reviews(rows: list[dict[str, str]]) -> tuple[list[dict[str, str | int]], dict[str, int]]:
    output: list[dict[str, str | int]] = []
    clean_count = 0
    empty_count = 0
    invalid_count = 0

    for row in rows:
        clean_text, word_count, is_valid, filter_reason = evaluate_text(row.get("review_text"))
        if is_valid:
            clean_count += 1
        elif filter_reason == "empty_text":
            empty_count += 1
            invalid_count += 1
        else:
            invalid_count += 1

        output.append(
            {
                **row,
                "text_word_count": word_count,
                "is_valid_text": "true" if is_valid else "false",
                "filter_reason": filter_reason,
                "clean_text": clean_text,
            }
        )

    stats = {
        "raw_count": len(rows),
        "clean_count": clean_count,
        "duplicate_count": 0,
        "empty_text_count": empty_count,
        "invalid_text_count": invalid_count,
    }
    return output, stats


def build_instagram_posts(rows: list[dict[str, str]]) -> tuple[list[dict[str, str | int]], dict[str, int]]:
    output: list[dict[str, str | int]] = []
    clean_count = 0
    empty_count = 0
    invalid_count = 0

    for row in rows:
        clean_text, word_count, is_valid, filter_reason = evaluate_text(row.get("caption"))
        if is_valid:
            clean_count += 1
        elif filter_reason == "empty_text":
            empty_count += 1
            invalid_count += 1
        else:
            invalid_count += 1

        output.append(
            {
                **row,
                "caption_word_count": word_count,
                "is_valid_caption": "true" if is_valid else "false",
                "filter_reason": filter_reason,
                "clean_caption": clean_text,
            }
        )

    stats = {
        "raw_count": len(rows),
        "clean_count": clean_count,
        "duplicate_count": 0,
        "empty_text_count": empty_count,
        "invalid_text_count": invalid_count,
    }
    return output, stats


def build_instagram_comments(rows: list[dict[str, str]]) -> tuple[list[dict[str, str | int]], dict[str, int]]:
    output: list[dict[str, str | int]] = []
    clean_count = 0
    empty_count = 0
    invalid_count = 0

    for row in rows:
        clean_text, word_count, is_valid, filter_reason = evaluate_text(row.get("comment_text"))
        if is_valid:
            clean_count += 1
        elif filter_reason == "empty_text":
            empty_count += 1
            invalid_count += 1
        else:
            invalid_count += 1

        output.append(
            {
                **row,
                "text_word_count": word_count,
                "is_valid_text": "true" if is_valid else "false",
                "filter_reason": filter_reason,
                "clean_text": clean_text,
            }
        )

    stats = {
        "raw_count": len(rows),
        "clean_count": clean_count,
        "duplicate_count": 0,
        "empty_text_count": empty_count,
        "invalid_text_count": invalid_count,
    }
    return output, stats


def build_batch_rows(
    gmaps_stats: dict[str, int],
    posts_stats: dict[str, int],
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
            "target_data": "instagram_posts",
            "started_at": "",
            "finished_at": "",
            **posts_stats,
            "status": "passed",
            "notes": "Mini test Instagram posts",
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
                "- `gmaps_reviews_final.csv`",
                "- `gmaps_reviewers_final.csv`",
                "- `instagram_posts_final.csv`",
                "- `instagram_comments_final.csv`",
                "- `scraping_batches_test.csv`",
                "",
                "## Catatan",
                "- Dataset final untuk teks menyertakan kolom clean dan audit filter NLP.",
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

    gmaps_reviews_final, gmaps_stats = build_gmaps_reviews(gmaps_reviews)
    instagram_posts_final, posts_stats = build_instagram_posts(instagram_posts)
    instagram_comments_final, comments_stats = build_instagram_comments(instagram_comments)

    write_csv(
        "data/final/test/gmaps_reviews_final.csv",
        list(gmaps_reviews_final[0].keys()) if gmaps_reviews_final else [],
        gmaps_reviews_final,
    )
    write_csv(
        "data/final/test/gmaps_reviewers_final.csv",
        list(gmaps_reviewers[0].keys()) if gmaps_reviewers else [],
        gmaps_reviewers,
    )
    write_csv(
        "data/final/test/instagram_posts_final.csv",
        list(instagram_posts_final[0].keys()) if instagram_posts_final else [],
        instagram_posts_final,
    )
    write_csv(
        "data/final/test/instagram_comments_final.csv",
        list(instagram_comments_final[0].keys()) if instagram_comments_final else [],
        instagram_comments_final,
    )

    batch_rows = build_batch_rows(gmaps_stats, posts_stats, comments_stats)
    write_csv(
        "data/final/test/scraping_batches_test.csv",
        list(batch_rows[0].keys()) if batch_rows else [],
        batch_rows,
    )
    write_summary("data/final/test/final_test_summary.md", gmaps_stats, posts_stats, comments_stats)

    print("[finalize] saved final test datasets under data/final/test")


if __name__ == "__main__":
    main()
