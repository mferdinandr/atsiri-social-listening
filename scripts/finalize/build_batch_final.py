from __future__ import annotations

import argparse
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


def read_ids(path: str, key: str) -> set[str]:
    csv_path = Path(path)
    if not csv_path.exists():
        return set()
    with csv_path.open(encoding="utf-8", newline="") as handle:
        return {
            row.get(key, "")
            for row in csv.DictReader(handle)
            if row.get(key, "")
        }


def find_previous_batch_paths(current_batch: str, relative_path: str) -> list[Path]:
    try:
        current_num = int(current_batch.split("_")[-1])
    except ValueError:
        return []
    paths: list[Path] = []
    base = Path(relative_path)
    parent = base.parent.parent
    file_name = base.name
    for batch_dir in sorted(parent.glob("batch_*")):
        try:
            batch_num = int(batch_dir.name.split("_")[-1])
        except ValueError:
            continue
        if batch_num >= current_num:
            continue
        candidate = batch_dir / file_name
        if candidate.exists():
            paths.append(candidate)
    return paths


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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build final batch datasets from processed batch CSV files.")
    parser.add_argument("--batch-number", default="batch_001")
    parser.add_argument("--prev-batch-number", help="Optional previous batch number to exclude duplicates from final output")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    batch = args.batch_number
    prev_batch = args.prev_batch_number

    gmaps_reviews = read_csv(f"data/processed/{batch}/google_maps/gmaps_reviews.csv")
    gmaps_reviewers = read_csv(f"data/processed/{batch}/google_maps/gmaps_reviewers.csv")
    comments_path = Path(f"data/processed/{batch}/instagram_comments/instagram_comments.csv")
    instagram_comments = read_csv(str(comments_path)) if comments_path.exists() else []

    prev_gmaps_ids: set[str] = set()
    prev_comment_ids: set[str] = set()
    gmaps_prev_paths = find_previous_batch_paths(batch, f"data/datasets/all/{batch}/gmaps_reviews_all.csv")
    comments_prev_paths = find_previous_batch_paths(batch, f"data/datasets/all/{batch}/instagram_comments_all.csv")

    if prev_batch:
        explicit_gmaps_path = Path(f"data/datasets/all/{prev_batch}/gmaps_reviews_all.csv")
        explicit_comments_path = Path(f"data/datasets/all/{prev_batch}/instagram_comments_all.csv")
        if explicit_gmaps_path.exists() and explicit_gmaps_path not in gmaps_prev_paths:
            gmaps_prev_paths.append(explicit_gmaps_path)
        if explicit_comments_path.exists() and explicit_comments_path not in comments_prev_paths:
            comments_prev_paths.append(explicit_comments_path)

    for prev_path in gmaps_prev_paths:
        prev_gmaps_ids.update(read_ids(str(prev_path), "review_id"))
    for prev_path in comments_prev_paths:
        prev_comment_ids.update(read_ids(str(prev_path), "comment_id"))

    if prev_gmaps_ids:
        gmaps_reviews = [row for row in gmaps_reviews if row.get("review_id", "") not in prev_gmaps_ids]
        current_reviewer_ids = {r.get("reviewer_id", "") for r in gmaps_reviews if r.get("reviewer_id", "")}
        gmaps_reviewers = [row for row in gmaps_reviewers if row.get("reviewer_id", "") in current_reviewer_ids]
    if prev_comment_ids and instagram_comments:
        instagram_comments = [row for row in instagram_comments if row.get("comment_id", "") not in prev_comment_ids]

    gmaps_reviews_all, gmaps_reviews_clean, gmaps_stats = append_text_audit(gmaps_reviews, "review_text", "text")
    instagram_comments_all: list[dict[str, str | int]] = []
    instagram_comments_clean: list[dict[str, str | int]] = []
    comments_stats = {
        "raw_count": 0,
        "clean_count": 0,
        "duplicate_count": 0,
        "empty_text_count": 0,
        "invalid_text_count": 0,
    }
    if instagram_comments:
        instagram_comments_all, instagram_comments_clean, comments_stats = append_text_audit(instagram_comments, "comment_text", "text")

    write_csv(
        f"data/datasets/all/{batch}/gmaps_reviews_all.csv",
        list(gmaps_reviews_all[0].keys()) if gmaps_reviews_all else [],
        gmaps_reviews_all,
    )
    if gmaps_reviewers:
        write_csv(
            f"data/datasets/all/{batch}/gmaps_reviewers_all.csv",
            list(gmaps_reviewers[0].keys()),
            gmaps_reviewers,
        )
    write_csv(
        f"data/datasets/clean/{batch}/gmaps_reviews_clean.csv",
        list(gmaps_reviews_clean[0].keys()) if gmaps_reviews_clean else [],
        gmaps_reviews_clean,
    )
    if instagram_comments_all:
        write_csv(
            f"data/datasets/all/{batch}/instagram_comments_all.csv",
            list(instagram_comments_all[0].keys()),
            instagram_comments_all,
        )
    if instagram_comments_clean:
        write_csv(
            f"data/datasets/clean/{batch}/instagram_comments_clean.csv",
            list(instagram_comments_clean[0].keys()),
            instagram_comments_clean,
        )

    batch_rows = [
        {
            "batch_number": batch,
            "source": "google_maps",
            "target_data": "gmaps_reviews",
            "started_at": "",
            "finished_at": "",
            **gmaps_stats,
            "status": "completed",
            "notes": "Batch Google Maps validation",
        },
    ]
    if instagram_comments:
        batch_rows.append(
            {
                "batch_number": batch,
                "source": "instagram",
                "target_data": "instagram_comments",
                "started_at": "",
                "finished_at": "",
                **comments_stats,
                "status": "completed",
                "notes": "Batch Instagram comments validation",
            }
        )
    write_csv(
        f"data/final/{batch}/scraping_batches.csv",
        list(batch_rows[0].keys()),
        batch_rows,
    )

    summary_path = Path(f"data/final/{batch}/summary.md")
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(
        "\n".join(
            [
                f"# {batch} Summary",
                "",
                "## Ringkasan",
                f"- Google Maps reviews raw: {gmaps_stats['raw_count']}",
                f"- Google Maps reviews clean valid: {gmaps_stats['clean_count']}",
                f"- Google Maps reviewers unique: {len(gmaps_reviewers)}",
                f"- Instagram comments raw: {comments_stats['raw_count']}" if instagram_comments else "- Instagram comments raw: batch ini tidak mengambil comments",
                f"- Instagram comments clean valid: {comments_stats['clean_count']}" if instagram_comments else "- Instagram comments clean valid: batch ini tidak mengambil comments",
                "",
                "## File utama",
                "- `gmaps_reviewers_all.csv` menyimpan tabel reviewer publik Google Maps hasil normalisasi.",
                "- Instagram posts gunakan dataset shared, bukan file per batch.",
                "- Gunakan folder `data/datasets/all` untuk arsip semua hasil scrape.",
                "- Gunakan folder `data/datasets/clean` untuk analisis NLP dan pelaporan data bersih.",
            ]
        ),
        encoding="utf-8",
    )

    print(f"[finalize] saved datasets under data/datasets/{{all,clean}}/{batch} and summaries under data/final/{batch}")


if __name__ == "__main__":
    main()
