from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path("data")
CLEAN_DIR = ROOT / "datasets" / "clean"
CONSOLIDATED_CLEAN_DIR = CLEAN_DIR / "consolidated"


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, headers: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def dedupe_rows(rows: list[dict[str, str]], key: str) -> list[dict[str, str]]:
    seen: set[str] = set()
    output: list[dict[str, str]] = []
    for row in rows:
        value = row.get(key, "")
        if not value or value in seen:
            continue
        seen.add(value)
        output.append(row)
    return output


def copy_single_source(src: Path, dest: Path) -> int:
    rows = read_csv_rows(src)
    write_csv(dest, list(rows[0].keys()) if rows else [], rows)
    return len(rows)


def combine_instagram_comments_clean() -> int:
    combined: list[dict[str, str]] = []
    for batch_dir in sorted(CLEAN_DIR.glob("batch_*")):
        csv_path = batch_dir / "instagram_comments_clean.csv"
        if csv_path.exists():
            combined.extend(read_csv_rows(csv_path))
    combined = dedupe_rows(combined, "comment_id")
    if combined:
        headers = list(combined[0].keys())
        write_csv(CONSOLIDATED_CLEAN_DIR / "instagram_comments_clean.csv", headers, combined)
    return len(combined)


def build_readme(counts: dict[str, int]) -> str:
    return "\n".join(
        [
            "# Consolidated Clean Dataset Inventory",
            "",
            "Folder ini menjadi sumber final resmi untuk dataset yang siap dipakai pada analisis.",
            "",
            "## Dataset final resmi",
            f"- `gmaps_reviews_clean.csv` → {counts['gmaps_reviews']} rows",
            f"- `gmaps_reviewers_clean.csv` → {counts['gmaps_reviewers']} rows",
            f"- `instagram_posts_clean.csv` → {counts['instagram_posts']} rows",
            f"- `instagram_comments_clean.csv` → {counts['instagram_comments']} rows",
            "",
            "## Layer dataset per entitas",
            "",
            "### Google Maps reviews",
            "- raw: `data/raw/google_maps/full_run/gmaps_output.json`",
            "- final resmi: `data/datasets/clean/consolidated/gmaps_reviews_clean.csv`",
            "",
            "### Google Maps reviewers",
            "- raw: `data/raw/google_maps/full_run/gmaps_output.json`",
            "- final resmi: `data/datasets/clean/consolidated/gmaps_reviewers_clean.csv`",
            "",
            "### Instagram posts",
            "- raw: `data/raw/instagram_posts/all_posts/ig_posts_output.json`",
            "- final resmi: `data/datasets/clean/consolidated/instagram_posts_clean.csv`",
            "",
            "### Instagram comments",
            "- raw: `data/raw/instagram_comments/batch_001` s.d. `data/raw/instagram_comments/batch_007`",
            "- final resmi: `data/datasets/clean/consolidated/instagram_comments_clean.csv`",
            "",
            "## Catatan",
            "- Konsep `data/final/final_datasets` dihapus karena redundant terhadap clean consolidated.",
            "- Untuk Instagram comments, file ini merupakan hasil penggabungan batch `001` sampai `007`.",
            "- Untuk Google Maps reviewers, layer final resmi disamakan dengan tabel reviewer publik hasil full run.",
        ]
    )


def main() -> None:
    counts: dict[str, int] = {}

    gmaps_reviews_src = CLEAN_DIR / "full_run" / "gmaps_reviews_clean.csv"
    gmaps_reviewers_src = ROOT / "datasets" / "all" / "full_run" / "gmaps_reviewers_all.csv"
    instagram_posts_src = CLEAN_DIR / "shared" / "instagram_posts_clean.csv"

    counts["gmaps_reviews"] = copy_single_source(
        gmaps_reviews_src,
        CONSOLIDATED_CLEAN_DIR / "gmaps_reviews_clean.csv",
    )
    counts["gmaps_reviewers"] = copy_single_source(
        gmaps_reviewers_src,
        CONSOLIDATED_CLEAN_DIR / "gmaps_reviewers_clean.csv",
    )
    counts["instagram_posts"] = copy_single_source(
        instagram_posts_src,
        CONSOLIDATED_CLEAN_DIR / "instagram_posts_clean.csv",
    )
    counts["instagram_comments"] = combine_instagram_comments_clean()

    CONSOLIDATED_CLEAN_DIR.mkdir(parents=True, exist_ok=True)
    (CONSOLIDATED_CLEAN_DIR / "README.md").write_text(build_readme(counts), encoding="utf-8")
    print("[finalize] saved consolidated clean datasets")


if __name__ == "__main__":
    main()
