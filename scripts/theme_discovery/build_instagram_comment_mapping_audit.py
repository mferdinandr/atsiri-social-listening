from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path("data")
COMMENTS_PATH = ROOT / "datasets" / "clean" / "consolidated" / "instagram_comments_clean.csv"
MAPPING_PATH = ROOT / "final" / "theme_mapping" / "instagram_comments" / "instagram_comment_theme_mapping.csv"
OUTPUT_DIR = ROOT / "final" / "theme_mapping" / "instagram_comments"


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, headers: list[str], rows: list[dict[str, str | int | float]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    comments = read_csv_rows(COMMENTS_PATH)
    mapping_rows = read_csv_rows(MAPPING_PATH)

    total_clean_comments = len(comments)
    matched_comment_ids = [row["comment_id"] for row in mapping_rows]
    matched_comment_id_set = set(matched_comment_ids)
    matched_comments = len(matched_comment_id_set)
    unmatched_comments = total_clean_comments - matched_comments

    per_comment_counts: dict[str, int] = {}
    for comment_id in matched_comment_ids:
        per_comment_counts[comment_id] = per_comment_counts.get(comment_id, 0) + 1

    multi_theme_comments = sum(1 for count in per_comment_counts.values() if count > 1)
    max_themes_per_comment = max(per_comment_counts.values(), default=0)
    average_themes_per_matched_comment = round(len(mapping_rows) / matched_comments, 2) if matched_comments else 0.0

    audit_rows = [
        {"metric": "clean_comments", "value": total_clean_comments, "note": "Jumlah total Instagram comments clean"},
        {"metric": "matched_comments", "value": matched_comments, "note": "Jumlah comment yang match minimal satu tema"},
        {"metric": "unmatched_comments", "value": unmatched_comments, "note": "Jumlah comment yang belum match tema mana pun"},
        {"metric": "mapping_rows", "value": len(mapping_rows), "note": "Jumlah total pasangan comment x tema"},
        {"metric": "multi_theme_comments", "value": multi_theme_comments, "note": "Jumlah comment yang match lebih dari satu tema"},
        {"metric": "max_themes_per_comment", "value": max_themes_per_comment, "note": "Jumlah tema maksimum pada satu comment"},
        {
            "metric": "avg_themes_per_matched_comment",
            "value": average_themes_per_matched_comment,
            "note": "Rata-rata jumlah tema per matched comment",
        },
    ]
    write_csv(OUTPUT_DIR / "instagram_comment_mapping_audit.csv", ["metric", "value", "note"], audit_rows)

    summary = "\n".join(
        [
            "# Instagram Comment Mapping Audit",
            "",
            f"- Clean comments: `{total_clean_comments}`",
            f"- Matched comments: `{matched_comments}`",
            f"- Unmatched comments: `{unmatched_comments}`",
            f"- Mapping rows: `{len(mapping_rows)}`",
            f"- Multi-theme comments: `{multi_theme_comments}`",
            f"- Max themes per comment: `{max_themes_per_comment}`",
            f"- Average themes per matched comment: `{average_themes_per_matched_comment}`",
        ]
    )
    (OUTPUT_DIR / "instagram_comment_mapping_audit.md").write_text(summary, encoding="utf-8")
    print(f"[mapping_audit] saved Instagram comment mapping audit under {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
