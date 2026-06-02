from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path("data")
FINAL_DIR = ROOT / "final"


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def count_rows(path: Path) -> int:
    return len(read_csv_rows(path))


def unique_count(path: Path, key: str) -> int:
    return len({row.get(key, "") for row in read_csv_rows(path) if row.get(key, "")})


def write_csv(path: Path, headers: list[str], rows: list[dict[str, str | int]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def build_records() -> list[dict[str, str | int]]:
    records: list[dict[str, str | int]] = []

    records.append(
        {
            "scope": "shared",
            "run_name": "instagram_posts_shared",
            "source": "instagram",
            "dataset": "instagram_posts",
            "all_rows": count_rows(ROOT / "datasets/all/shared/instagram_posts_all.csv"),
            "clean_rows": count_rows(ROOT / "datasets/clean/shared/instagram_posts_clean.csv"),
            "unique_id_count": unique_count(ROOT / "datasets/all/shared/instagram_posts_all.csv", "post_id"),
            "status": "completed",
            "notes": "Dataset reusable, cukup dijalankan sekali",
        }
    )

    test_specs = [
        ("google_maps", "gmaps_reviews", "review_id"),
        ("instagram", "instagram_comments", "comment_id"),
    ]
    for source, dataset, key in test_specs:
        records.append(
            {
                "scope": "test",
                "run_name": "test",
                "source": source,
                "dataset": dataset,
                "all_rows": count_rows(ROOT / f"datasets/all/test/{dataset}_all.csv"),
                "clean_rows": count_rows(ROOT / f"datasets/clean/test/{dataset}_clean.csv"),
                "unique_id_count": unique_count(ROOT / f"datasets/all/test/{dataset}_all.csv", key),
                "status": "completed",
                "notes": "Mini test awal",
            }
        )

    records.append(
        {
            "scope": "full_run",
            "run_name": "full_run",
            "source": "google_maps",
            "dataset": "gmaps_reviews",
            "all_rows": count_rows(ROOT / "datasets/all/full_run/gmaps_reviews_all.csv"),
            "clean_rows": count_rows(ROOT / "datasets/clean/full_run/gmaps_reviews_clean.csv"),
            "unique_id_count": unique_count(ROOT / "datasets/all/full_run/gmaps_reviews_all.csv", "review_id"),
            "status": "completed",
            "notes": "Sumber utama Google Maps, hasil full scrape satu kali",
        }
    )
    records.append(
        {
            "scope": "full_run",
            "run_name": "full_run",
            "source": "google_maps",
            "dataset": "gmaps_reviewers",
            "all_rows": count_rows(ROOT / "datasets/all/full_run/gmaps_reviewers_all.csv"),
            "clean_rows": count_rows(ROOT / "datasets/all/full_run/gmaps_reviewers_all.csv"),
            "unique_id_count": unique_count(ROOT / "datasets/all/full_run/gmaps_reviewers_all.csv", "reviewer_id"),
            "status": "completed",
            "notes": "Tabel reviewer publik hasil full scrape Google Maps",
        }
    )

    for batch_csv in sorted((FINAL_DIR).glob("batch_*/scraping_batches.csv")):
        batch_name = batch_csv.parent.name
        rows = read_csv_rows(batch_csv)
        for row in rows:
            dataset = row.get("target_data", "")
            source = row.get("source", "")
            key = "review_id" if dataset == "gmaps_reviews" else "comment_id"
            dataset_prefix = dataset
            records.append(
                {
                    "scope": "batch",
                    "run_name": batch_name,
                    "source": source,
                    "dataset": dataset,
                    "all_rows": count_rows(ROOT / f"datasets/all/{batch_name}/{dataset_prefix}_all.csv"),
                    "clean_rows": count_rows(ROOT / f"datasets/clean/{batch_name}/{dataset_prefix}_clean.csv"),
                    "unique_id_count": unique_count(ROOT / f"datasets/all/{batch_name}/{dataset_prefix}_all.csv", key),
                    "status": row.get("status", ""),
                    "notes": row.get("notes", ""),
                }
            )

    return records


def build_summary(records: list[dict[str, str | int]]) -> str:
    shared_posts = next((r for r in records if r["run_name"] == "instagram_posts_shared"), None)
    gmaps_full_run = next((r for r in records if r["scope"] == "full_run" and r["dataset"] == "gmaps_reviews"), None)
    gmaps_reviewers_full_run = next((r for r in records if r["scope"] == "full_run" and r["dataset"] == "gmaps_reviewers"), None)
    gmaps_batches = [r for r in records if r["scope"] == "batch" and r["dataset"] == "gmaps_reviews"]
    ig_comment_batches = [r for r in records if r["scope"] == "batch" and r["dataset"] == "instagram_comments"]

    comments_all_total = sum(int(r["all_rows"]) for r in ig_comment_batches)
    comments_clean_total = sum(int(r["clean_rows"]) for r in ig_comment_batches)

    return "\n".join(
        [
            "# Master Progress Summary",
            "",
            "Catatan induk untuk melihat total progres scraping yang sudah tercatat sampai saat ini.",
            "",
            "## Status saat ini",
            f"- Instagram posts shared: {shared_posts['all_rows']} all / {shared_posts['clean_rows']} clean" if shared_posts else "- Instagram posts shared: belum ada",
            f"- Google Maps full run utama: {gmaps_full_run['all_rows']} all / {gmaps_full_run['clean_rows']} clean" if gmaps_full_run else "- Google Maps full run utama: belum ada",
            f"- Google Maps reviewers final: {gmaps_reviewers_full_run['all_rows']} row / {gmaps_reviewers_full_run['unique_id_count']} unique reviewer_id" if gmaps_reviewers_full_run else "- Google Maps reviewers final: belum ada",
            f"- Google Maps batch validasi historis: {len(gmaps_batches)} batch" if gmaps_batches else "- Google Maps batch validasi historis: belum ada",
            f"- Instagram comments batches tercatat: {len(ig_comment_batches)} batch, total {comments_all_total} all / {comments_clean_total} clean",
            "",
            "## Batch yang sudah ada",
            "- Test awal",
            "- batch_001",
            "- batch_002",
            "- full_run",
            "",
            "## Catatan",
            "- `instagram_posts` adalah shared dataset dan tidak perlu diulang per batch.",
            "- `google_maps full_run` adalah sumber utama dan paling hemat biaya.",
            "- Batch Google Maps kumulatif lama sudah dipindahkan ke arsip eksperimen.",
            "- `instagram_comments` tetap dicatat per batch.",
            "- Gunakan `master_progress.csv` untuk tabel ringkas semua run.",
        ]
    )


def main() -> None:
    records = build_records()
    headers = [
        "scope",
        "run_name",
        "source",
        "dataset",
        "all_rows",
        "clean_rows",
        "unique_id_count",
        "status",
        "notes",
    ]
    write_csv(FINAL_DIR / "master_progress.csv", headers, records)
    (FINAL_DIR / "master_progress_summary.md").write_text(build_summary(records), encoding="utf-8")
    print("[finalize] saved master progress files under data/final")


if __name__ == "__main__":
    main()
