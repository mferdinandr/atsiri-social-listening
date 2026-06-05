from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


ROOT = Path("data")
REVIEWS_PATH = ROOT / "datasets" / "clean" / "consolidated" / "gmaps_reviews_clean.csv"
MAPPING_PATH = ROOT / "final" / "theme_mapping" / "google_maps" / "gmaps_review_theme_mapping.csv"
OUTPUT_DIR = ROOT / "final" / "theme_mapping" / "google_maps"


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
    reviews = read_csv_rows(REVIEWS_PATH)
    mappings = read_csv_rows(MAPPING_PATH)

    rating_counter: Counter[int] = Counter()
    negative_reviews: list[dict[str, str]] = []
    negative_ids: set[str] = set()

    for row in reviews:
        rating = int(float(row["rating"])) if row.get("rating") else None
        if rating is None:
            continue
        rating_counter[rating] += 1
        if rating <= 3:
            negative_reviews.append(row)
            negative_ids.add(row["review_id"])

    theme_counter: Counter[tuple[str, str]] = Counter()
    matched_negative_ids: set[str] = set()
    negative_mapping_rows: list[dict[str, str]] = []

    for row in mappings:
        review_id = row["review_id"]
        if review_id in negative_ids:
            matched_negative_ids.add(review_id)
            key = (row["theme_code"], row["theme_label"])
            theme_counter[key] += 1
            negative_mapping_rows.append(row)

    negative_unmatched = negative_ids - matched_negative_ids

    audit_rows = [
        {"metric": "clean_reviews", "value": len(reviews), "note": "Jumlah seluruh review clean Google Maps"},
        {"metric": "negative_reviews_rating_le_3", "value": len(negative_ids), "note": "Jumlah review dengan rating <= 3"},
        {"metric": "negative_reviews_rating_1", "value": rating_counter.get(1, 0), "note": "Jumlah review dengan rating 1"},
        {"metric": "negative_reviews_rating_2", "value": rating_counter.get(2, 0), "note": "Jumlah review dengan rating 2"},
        {"metric": "negative_reviews_rating_3", "value": rating_counter.get(3, 0), "note": "Jumlah review dengan rating 3"},
        {"metric": "negative_reviews_matched_to_theme", "value": len(matched_negative_ids), "note": "Jumlah review negatif yang kena minimal satu tema"},
        {"metric": "negative_reviews_unmatched", "value": len(negative_unmatched), "note": "Jumlah review negatif yang tidak kena tema mana pun"},
        {"metric": "negative_theme_mapping_rows", "value": sum(theme_counter.values()), "note": "Jumlah total pasangan review negatif x tema"},
    ]
    write_csv(OUTPUT_DIR / "gmaps_negative_review_audit.csv", ["metric", "value", "note"], audit_rows)
    if negative_mapping_rows:
        write_csv(
            OUTPUT_DIR / "gmaps_negative_review_theme_mapping.csv",
            list(negative_mapping_rows[0].keys()),
            negative_mapping_rows,
        )

    theme_rows = [
        {
            "theme_code": theme_code,
            "theme_label": theme_label,
            "matched_negative_review_count": count,
        }
        for (theme_code, theme_label), count in sorted(theme_counter.items(), key=lambda item: item[1], reverse=True)
    ]
    write_csv(
        OUTPUT_DIR / "gmaps_negative_reviews_by_theme.csv",
        ["theme_code", "theme_label", "matched_negative_review_count"],
        theme_rows,
    )

    summary = "\n".join(
        [
            "# Google Maps Negative Review Audit",
            "",
            "Audit ini memakai definisi review negatif sebagai review dengan `rating <= 3`.",
            "",
            f"- Clean reviews: `{len(reviews)}`",
            f"- Negative reviews (`rating <= 3`): `{len(negative_ids)}`",
            f"- Rating 1: `{rating_counter.get(1, 0)}`",
            f"- Rating 2: `{rating_counter.get(2, 0)}`",
            f"- Rating 3: `{rating_counter.get(3, 0)}`",
            f"- Negative reviews matched to theme: `{len(matched_negative_ids)}`",
            f"- Negative reviews unmatched: `{len(negative_unmatched)}`",
            f"- Negative review x theme mapping rows: `{sum(theme_counter.values())}`",
            "",
            "## File mapping negatif",
            "",
            "- `gmaps_negative_review_theme_mapping.csv` berisi subset dari `gmaps_review_theme_mapping.csv` yang hanya memuat review dengan `rating <= 3`.",
            "",
            "## Tema yang paling sering muncul pada review negatif",
            "",
        ]
        + [
            f"- `{theme_label}`: `{count}`"
            for (_, theme_label), count in sorted(theme_counter.items(), key=lambda item: item[1], reverse=True)
        ]
    )
    (OUTPUT_DIR / "gmaps_negative_review_audit.md").write_text(summary, encoding="utf-8")

    print(f"[negative_audit] saved negative review audit under {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
