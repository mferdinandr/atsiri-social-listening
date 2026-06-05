from __future__ import annotations

import csv
from pathlib import Path
import re


ROOT = Path("data")
REVIEWS_PATH = ROOT / "datasets" / "clean" / "consolidated" / "gmaps_reviews_clean.csv"
REVIEWERS_PATH = ROOT / "datasets" / "clean" / "consolidated" / "gmaps_reviewers_clean.csv"
CODEBOOK_PATH = ROOT / "final" / "theme_discovery" / "atsiri_theme_codebook_v1.csv"
OUTPUT_DIR = ROOT / "final" / "theme_mapping" / "google_maps"

TIME_BUCKETS = [
    ("2016", "2017", "2016-2017"),
    ("2018", "2019", "2018-2019"),
    ("2020", "2021", "2020-2021"),
    ("2022", "2023", "2022-2023"),
    ("2024", "2025", "2024-2025"),
    ("2026", "2026", "2026"),
]

THEME_ORDER = [
    "aromatic_products",
    "plants_garden",
    "museum_education",
    "wellness_experience",
    "culinary_resto",
    "glamping_stay",
    "destination_tourism",
    "event_campaign",
]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, headers: list[str], rows: list[dict[str, str | int]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def normalize_text(value: str) -> str:
    return (value or "").lower().strip()


def split_pipe(value: str) -> list[str]:
    return [item.strip().lower() for item in (value or "").split("|") if item.strip()]


def year_bucket(date_value: str) -> str:
    year = (date_value or "")[:4]
    for start, end, label in TIME_BUCKETS:
        if start <= year <= end:
            return label
    return "unknown"


def reviewer_bucket(total_reviews: str) -> str:
    try:
        value = int(float(total_reviews or 0))
    except ValueError:
        return "unknown"
    if value <= 500:
        return "0-500"
    if value <= 1000:
        return "501-1000"
    if value <= 1500:
        return "1001-1500"
    if value <= 2000:
        return "1501-2000"
    return ">2000"


def load_reviewers() -> dict[str, dict[str, str]]:
    reviewers = read_csv_rows(REVIEWERS_PATH)
    return {row.get("reviewer_id", ""): row for row in reviewers if row.get("reviewer_id", "")}


def load_codebook() -> list[dict[str, str]]:
    rows = read_csv_rows(CODEBOOK_PATH)
    row_map = {row["theme_code"]: row for row in rows}
    return [row_map[theme_code] for theme_code in THEME_ORDER if theme_code in row_map]


def keyword_hits(text: str, keywords: list[str]) -> list[str]:
    hits: list[str] = []
    for keyword in keywords:
        if not keyword:
            continue
        pattern = r"(?<![a-z0-9])" + re.escape(keyword) + r"(?![a-z0-9])"
        if re.search(pattern, text):
            hits.append(keyword)
    return hits


def match_theme(theme_code: str, text: str, keywords: list[str]) -> list[str]:
    hits = keyword_hits(text, keywords)
    if not hits:
        return []

    if theme_code == "aromatic_products":
        strong_terms = {
            "essential oil",
            "essential oils",
            "minyak atsiri",
            "produk",
            "parfum",
            "diffuser",
            "fragrance",
            "blend",
            "shop",
        }
        return hits if any(hit in strong_terms for hit in hits) else []

    if theme_code == "museum_education":
        strong_terms = {
            "museum",
            "workshop",
            "class",
            "kelas",
            "tur",
            "factory",
            "pabrik",
            "knowledge",
            "edukasi",
            "belajar",
        }
        return hits if any(hit in strong_terms for hit in hits) else []

    if theme_code == "wellness_experience":
        strong_terms = {
            "wellness",
            "healing",
            "relax",
            "self care",
            "restore",
            "ritual",
            "calm",
            "aromatic wellness",
            "slow rhythm",
        }
        return hits if any(hit in strong_terms for hit in hits) else []

    if theme_code == "destination_tourism":
        strong_terms = {
            "wisata",
            "berkunjung",
            "visit",
            "destination",
            "travel",
            "trip",
            "tawangmangu",
            "karanganyar",
            "architecture",
            "landscape",
            "plaza",
        }
        return hits if any(hit in strong_terms for hit in hits) else []

    if theme_code == "event_campaign":
        weak_terms = {"program", "special"}
        strong_terms = {"event", "promo", "campaign", "community", "playlist", "coming soon", "launch", "ramadan"}
        if any(hit in strong_terms for hit in hits):
            return hits
        if any(hit in weak_terms for hit in hits):
            return []

    return hits


def build_mapping() -> tuple[
    list[dict[str, str]],
    list[dict[str, str | int]],
    list[dict[str, str | int]],
    list[dict[str, str | int]],
    list[dict[str, str | int]],
]:
    reviews = read_csv_rows(REVIEWS_PATH)
    reviewers = load_reviewers()
    codebook = load_codebook()

    mapping_rows: list[dict[str, str]] = []
    overall_counts: dict[str, int] = {row["theme_code"]: 0 for row in codebook}
    period_counts: dict[tuple[str, str], int] = {}
    bucket_counts: dict[tuple[str, str], int] = {}
    bucket_period_counts: dict[tuple[str, str, str], int] = {}

    for review in reviews:
        review_id = review.get("review_id", "")
        reviewer_id = review.get("reviewer_id", "")
        reviewer = reviewers.get(reviewer_id, {})
        text = normalize_text(review.get("clean_text") or review.get("review_text"))
        time_bucket = year_bucket(review.get("review_date", ""))
        bucket = reviewer_bucket(reviewer.get("reviewer_total_reviews", ""))

        for theme in codebook:
            hits = match_theme(theme["theme_code"], text, split_pipe(theme.get("include_keywords", "")))
            if not hits:
                continue
            overall_counts[theme["theme_code"]] += 1
            period_counts[(theme["theme_code"], time_bucket)] = period_counts.get((theme["theme_code"], time_bucket), 0) + 1
            bucket_counts[(theme["theme_code"], bucket)] = bucket_counts.get((theme["theme_code"], bucket), 0) + 1
            bucket_period_counts[(theme["theme_code"], bucket, time_bucket)] = (
                bucket_period_counts.get((theme["theme_code"], bucket, time_bucket), 0) + 1
            )
            mapping_rows.append(
                {
                    "review_id": review_id,
                    "reviewer_id": reviewer_id,
                    "review_date": review.get("review_date", ""),
                    "time_bucket": time_bucket,
                    "rating": review.get("rating", ""),
                    "reviewer_name": reviewer.get("reviewer_name", ""),
                    "reviewer_total_reviews": reviewer.get("reviewer_total_reviews", ""),
                    "reviewer_bucket": bucket,
                    "theme_code": theme["theme_code"],
                    "theme_label": theme["theme_label"],
                    "matched_keywords": "|".join(hits),
                    "review_text": review.get("review_text", ""),
                    "clean_text": review.get("clean_text", ""),
                }
            )

    overall_rows: list[dict[str, str | int]] = []
    for theme in codebook:
        overall_rows.append(
            {
                "theme_code": theme["theme_code"],
                "theme_label": theme["theme_label"],
                "matched_review_count": overall_counts.get(theme["theme_code"], 0),
            }
        )

    period_rows: list[dict[str, str | int]] = []
    for theme in codebook:
        for _, _, label in TIME_BUCKETS:
            period_rows.append(
                {
                    "theme_code": theme["theme_code"],
                    "theme_label": theme["theme_label"],
                    "time_bucket": label,
                    "matched_review_count": period_counts.get((theme["theme_code"], label), 0),
                }
            )

    bucket_order = ["0-500", "501-1000", "1001-1500", "1501-2000", ">2000"]
    reviewer_bucket_rows: list[dict[str, str | int]] = []
    reviewer_bucket_period_rows: list[dict[str, str | int]] = []
    for theme in codebook:
        for bucket in bucket_order:
            reviewer_bucket_rows.append(
                {
                    "theme_code": theme["theme_code"],
                    "theme_label": theme["theme_label"],
                    "reviewer_bucket": bucket,
                    "matched_review_count": bucket_counts.get((theme["theme_code"], bucket), 0),
                }
            )
            for _, _, label in TIME_BUCKETS:
                reviewer_bucket_period_rows.append(
                    {
                        "theme_code": theme["theme_code"],
                        "theme_label": theme["theme_label"],
                        "reviewer_bucket": bucket,
                        "time_bucket": label,
                        "matched_review_count": bucket_period_counts.get((theme["theme_code"], bucket, label), 0),
                    }
                )

    return mapping_rows, overall_rows, period_rows, reviewer_bucket_rows, reviewer_bucket_period_rows


def write_summary(mapping_rows: list[dict[str, str]], overall_rows: list[dict[str, str | int]]) -> None:
    total_reviews = len({row["review_id"] for row in mapping_rows})
    top_rows = sorted(overall_rows, key=lambda row: int(row["matched_review_count"]), reverse=True)
    lines = [
        "# Google Maps Theme Mapping Summary",
        "",
        "Mapping ini menerapkan codebook tema Atsiri v1 ke Google Maps reviews clean.",
        "",
        f"- Total review yang terkena minimal satu tema: {total_reviews}",
        f"- Total row mapping review x tema: {len(mapping_rows)}",
        "",
        "## Tema teratas",
    ]
    for row in top_rows[:5]:
        lines.append(f"- `{row['theme_code']}`: {row['matched_review_count']} review")
    (OUTPUT_DIR / "summary.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    mapping_rows, overall_rows, period_rows, reviewer_bucket_rows, reviewer_bucket_period_rows = build_mapping()

    if mapping_rows:
        write_csv(
            OUTPUT_DIR / "gmaps_review_theme_mapping.csv",
            list(mapping_rows[0].keys()),
            mapping_rows,
        )
    write_csv(
        OUTPUT_DIR / "gmaps_theme_overall_summary.csv",
        ["theme_code", "theme_label", "matched_review_count"],
        overall_rows,
    )
    write_csv(
        OUTPUT_DIR / "gmaps_theme_period_summary.csv",
        ["theme_code", "theme_label", "time_bucket", "matched_review_count"],
        period_rows,
    )
    write_csv(
        OUTPUT_DIR / "gmaps_theme_reviewer_bucket_summary.csv",
        ["theme_code", "theme_label", "reviewer_bucket", "matched_review_count"],
        reviewer_bucket_rows,
    )
    write_csv(
        OUTPUT_DIR / "gmaps_theme_reviewer_bucket_period_summary.csv",
        ["theme_code", "theme_label", "reviewer_bucket", "time_bucket", "matched_review_count"],
        reviewer_bucket_period_rows,
    )
    write_summary(mapping_rows, overall_rows)
    print(f"[theme_mapping] saved Google Maps theme mapping under {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
