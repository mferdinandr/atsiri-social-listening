from __future__ import annotations

from pathlib import Path

from map_gmaps_reviews_to_themes import (
    THEME_ORDER,
    keyword_hits,
    load_codebook,
    normalize_text,
    split_pipe,
    write_csv,
    year_bucket,
)

import csv


ROOT = Path("data")
COMMENTS_PATH = ROOT / "datasets" / "clean" / "consolidated" / "instagram_comments_clean.csv"
OUTPUT_DIR = ROOT / "final" / "theme_mapping" / "instagram_comments"


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


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
            "wangi",
            "wangi nya",
            "wanginya",
            "unrosed",
            "farhampton",
            "alpha",
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
            "pemandu",
            "guide",
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
            "tawangmangu",
            "karanganyar",
            "plaza",
            "rumah atsiri",
            "liburan",
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
]:
    comments = read_csv_rows(COMMENTS_PATH)
    codebook = load_codebook()

    mapping_rows: list[dict[str, str]] = []
    overall_counts: dict[str, int] = {row["theme_code"]: 0 for row in codebook}
    period_counts: dict[tuple[str, str], int] = {}

    for comment in comments:
        comment_id = comment.get("comment_id", "")
        text = normalize_text(comment.get("clean_text") or comment.get("comment_text"))
        time_bucket = year_bucket(comment.get("comment_date", ""))

        for theme in codebook:
            hits = match_theme(theme["theme_code"], text, split_pipe(theme.get("include_keywords", "")))
            if not hits:
                continue
            overall_counts[theme["theme_code"]] += 1
            period_counts[(theme["theme_code"], time_bucket)] = period_counts.get((theme["theme_code"], time_bucket), 0) + 1
            mapping_rows.append(
                {
                    "comment_id": comment_id,
                    "post_id": comment.get("post_id", ""),
                    "post_url": comment.get("post_url", ""),
                    "comment_date": comment.get("comment_date", ""),
                    "time_bucket": time_bucket,
                    "commenter_username": comment.get("commenter_username", ""),
                    "comment_like_count": comment.get("comment_like_count", ""),
                    "batch_number": comment.get("batch_number", ""),
                    "theme_code": theme["theme_code"],
                    "theme_label": theme["theme_label"],
                    "matched_keywords": "|".join(hits),
                    "comment_text": comment.get("comment_text", ""),
                    "clean_text": comment.get("clean_text", ""),
                }
            )

    overall_rows: list[dict[str, str | int]] = []
    for theme in codebook:
        overall_rows.append(
            {
                "theme_code": theme["theme_code"],
                "theme_label": theme["theme_label"],
                "matched_comment_count": overall_counts.get(theme["theme_code"], 0),
            }
        )

    period_labels = ["2016-2017", "2018-2019", "2020-2021", "2022-2023", "2024-2025", "2026"]
    period_rows: list[dict[str, str | int]] = []
    for theme in codebook:
        for label in period_labels:
            period_rows.append(
                {
                    "theme_code": theme["theme_code"],
                    "theme_label": theme["theme_label"],
                    "time_bucket": label,
                    "matched_comment_count": period_counts.get((theme["theme_code"], label), 0),
                }
            )

    return mapping_rows, overall_rows, period_rows


def write_summary(mapping_rows: list[dict[str, str]], overall_rows: list[dict[str, str | int]]) -> None:
    total_comments = len({row["comment_id"] for row in mapping_rows})
    top_rows = sorted(overall_rows, key=lambda row: int(row["matched_comment_count"]), reverse=True)
    lines = [
        "# Instagram Comments Theme Mapping Summary",
        "",
        "Mapping ini menerapkan codebook tema Atsiri v1 ke Instagram comments clean.",
        "",
        f"- Total comment yang terkena minimal satu tema: {total_comments}",
        f"- Total row mapping comment x tema: {len(mapping_rows)}",
        "",
        "## Tema teratas",
    ]
    for row in top_rows[:5]:
        lines.append(f"- `{row['theme_code']}`: {row['matched_comment_count']} comment")
    (OUTPUT_DIR / "summary.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    mapping_rows, overall_rows, period_rows = build_mapping()

    if mapping_rows:
        write_csv(
            OUTPUT_DIR / "instagram_comment_theme_mapping.csv",
            list(mapping_rows[0].keys()),
            mapping_rows,
        )
    write_csv(
        OUTPUT_DIR / "instagram_comment_theme_overall_summary.csv",
        ["theme_code", "theme_label", "matched_comment_count"],
        overall_rows,
    )
    write_csv(
        OUTPUT_DIR / "instagram_comment_theme_period_summary.csv",
        ["theme_code", "theme_label", "time_bucket", "matched_comment_count"],
        period_rows,
    )
    write_summary(mapping_rows, overall_rows)
    print(f"[theme_mapping] saved Instagram comments theme mapping under {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
