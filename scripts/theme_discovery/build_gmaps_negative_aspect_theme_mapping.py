from __future__ import annotations

import csv
import re
from pathlib import Path

from map_gmaps_reviews_to_themes import (
    keyword_hits,
    load_codebook,
    load_reviewers,
    normalize_text,
    reviewer_bucket,
    split_pipe,
    year_bucket,
)


ROOT = Path("data")
REVIEWS_PATH = ROOT / "datasets" / "clean" / "consolidated" / "gmaps_reviews_clean.csv"
OUTPUT_DIR = ROOT / "final" / "theme_mapping" / "google_maps"
NEGATIVE_LEXICON_PATH = OUTPUT_DIR / "gmaps_negative_signal_lexicon.csv"

CLAUSE_SPLIT_PATTERN = re.compile(
    r"(?:\n+|[.!?]+|\u2705|;|,\s+tapi\s+|,\s+namun\s+|,\s+sayangnya\s+|\s+but\s+|\s+however\s+)",
    flags=re.IGNORECASE,
)

NEGATIVE_THEME_EXTRA_KEYWORDS = {
    "culinary_resto": ["restaurant", "restoran", "food", "makan", "fish and chips", "sarapan", "kantin", "kopi"],
    "museum_education": ["guide", "pemandu", "tour guide"],
    "plants_garden": ["kebun", "aromatic garden", "kolam"],
    "destination_tourism": ["parkir", "akses", "jalan", "lokasi"],
    "aromatic_products": ["goods", "store", "toiletries"],
    "glamping_stay": ["nginap"],
}

NEGATIVE_THEME_STRONG_TERMS = {
    "aromatic_products": {
        "essential oil", "essential oils", "minyak atsiri", "produk", "parfum", "diffuser", "fragrance", "blend", "shop", "goods", "store", "toiletries",
    },
    "plants_garden": {
        "tanaman", "bunga", "garden", "taman", "citronella", "plants", "aromatic garden", "botanical", "kebun", "kolam",
    },
    "museum_education": {
        "museum", "workshop", "class", "kelas", "tur", "factory", "pabrik", "knowledge", "edukasi", "belajar", "guide", "pemandu", "tour guide",
    },
    "wellness_experience": {
        "wellness", "healing", "relax", "self care", "restore", "ritual", "calm", "aromatic wellness", "slow rhythm",
    },
    "culinary_resto": {
        "resto", "restaurant", "restoran", "recipe", "menu", "tea", "kuliner", "makanan", "minuman", "coffee", "lunch", "dinner", "food", "makan", "sarapan", "kantin", "kopi", "fish and chips",
    },
    "glamping_stay": {
        "glamping", "stay", "cabin", "camp", "room", "menginap", "staycation", "nginap",
    },
    "destination_tourism": {
        "wisata", "destination", "travel", "trip", "parkir", "akses", "jalan", "lokasi",
    },
    "event_campaign": {
        "event", "promo", "campaign", "community", "playlist", "coming soon", "launch", "ramadan",
    },
}


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, headers: list[str], rows: list[dict[str, str | int]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def load_negative_lexicon() -> list[dict[str, str]]:
    with NEGATIVE_LEXICON_PATH.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    return [row for row in rows if row.get("signal_text", "").strip()]


def split_clauses(text: str) -> list[str]:
    raw_parts = CLAUSE_SPLIT_PATTERN.split(text or "")
    clauses: list[str] = []
    for part in raw_parts:
        cleaned = " ".join(part.split()).strip(" -")
        if cleaned:
            clauses.append(cleaned)
    return clauses


def negative_hit_rows(text: str, lexicon_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    normalized = normalize_text(text)
    hits = [row for row in lexicon_rows if normalize_text(row["signal_text"]) in normalized]
    # `tidk`/`tdk` are noisy; keep only when no stronger indicator exists
    if hits and any(row["signal_text"] not in {"tidk", "tdk"} for row in hits):
        hits = [row for row in hits if row["signal_text"] not in {"tidk", "tdk"}]
    return hits


def negative_strength(hit_rows: list[dict[str, str]]) -> str:
    strengths = {row.get("negative_strength", "mild_negative") for row in hit_rows}
    if "hard_negative" in strengths:
        return "hard_negative"
    if "mixed_negative" in strengths:
        return "mixed_negative"
    return "mild_negative"


def negative_clause_theme_hits(theme_code: str, clause_text: str, base_keywords: list[str]) -> list[str]:
    keywords = list(dict.fromkeys(base_keywords + NEGATIVE_THEME_EXTRA_KEYWORDS.get(theme_code, [])))
    hits = keyword_hits(clause_text, keywords)
    if not hits:
        return []
    strong_terms = NEGATIVE_THEME_STRONG_TERMS.get(theme_code, set())
    return hits if any(hit in strong_terms for hit in hits) else []


def main() -> None:
    reviews = read_csv_rows(REVIEWS_PATH)
    reviewers = load_reviewers()
    codebook = load_codebook()
    negative_lexicon_rows = load_negative_lexicon()

    mapping_rows: list[dict[str, str]] = []
    theme_counts: dict[str, int] = {theme["theme_code"]: 0 for theme in codebook}
    negative_review_ids: set[str] = set()
    negative_clause_ids: set[tuple[str, str]] = set()
    matched_negative_clause_ids: set[tuple[str, str]] = set()

    for review in reviews:
        rating = int(float(review["rating"])) if review.get("rating") else None
        if rating is None or rating > 3:
            continue

        review_id = review.get("review_id", "")
        reviewer_id = review.get("reviewer_id", "")
        reviewer = reviewers.get(reviewer_id, {})
        time_bucket = year_bucket(review.get("review_date", ""))
        bucket = reviewer_bucket(reviewer.get("reviewer_total_reviews", ""))
        review_text = review.get("review_text", "")
        clean_text = review.get("clean_text") or review_text

        negative_review_ids.add(review_id)
        clauses = split_clauses(clean_text)
        for idx, clause in enumerate(clauses, start=1):
            clause_key = (review_id, str(idx))
            neg_hit_rows = negative_hit_rows(clause, negative_lexicon_rows)
            if not neg_hit_rows:
                continue
            negative_clause_ids.add(clause_key)
            normalized_clause = normalize_text(clause)
            clause_strength = negative_strength(neg_hit_rows)
            for theme in codebook:
                hits = negative_clause_theme_hits(theme["theme_code"], normalized_clause, split_pipe(theme.get("include_keywords", "")))
                if not hits:
                    continue
                matched_negative_clause_ids.add(clause_key)
                theme_counts[theme["theme_code"]] += 1
                mapping_rows.append(
                    {
                        "review_id": review_id,
                        "clause_id": f"{review_id}__{idx}",
                        "reviewer_id": reviewer_id,
                        "review_date": review.get("review_date", ""),
                        "time_bucket": time_bucket,
                        "rating": review.get("rating", ""),
                        "reviewer_name": reviewer.get("reviewer_name", ""),
                        "reviewer_total_reviews": reviewer.get("reviewer_total_reviews", ""),
                        "reviewer_bucket": bucket,
                        "theme_code": theme["theme_code"],
                        "theme_label": theme["theme_label"],
                        "negative_strength": clause_strength,
                        "negative_signals": "|".join(row["signal_text"] for row in neg_hit_rows),
                        "negative_signal_groups": "|".join(dict.fromkeys(row.get("signal_group", "") for row in neg_hit_rows if row.get("signal_group"))),
                        "matched_keywords": "|".join(hits),
                        "negative_clause_text": clause,
                        "review_text": review_text,
                        "clean_text": clean_text,
                    }
                )

    mapping_headers = [
        "review_id",
        "clause_id",
        "reviewer_id",
        "review_date",
        "time_bucket",
        "rating",
        "reviewer_name",
        "reviewer_total_reviews",
        "reviewer_bucket",
        "theme_code",
        "theme_label",
        "negative_strength",
        "negative_signals",
        "negative_signal_groups",
        "matched_keywords",
        "negative_clause_text",
        "review_text",
        "clean_text",
    ]
    write_csv(OUTPUT_DIR / "gmaps_negative_aspect_theme_mapping.csv", mapping_headers, mapping_rows)

    summary_rows: list[dict[str, str | int]] = []
    for theme in codebook:
        summary_rows.append(
            {
                "theme_code": theme["theme_code"],
                "theme_label": theme["theme_label"],
                "matched_negative_clause_count": theme_counts.get(theme["theme_code"], 0),
            }
        )
    summary_rows.sort(key=lambda row: int(row["matched_negative_clause_count"]), reverse=True)
    write_csv(
        OUTPUT_DIR / "gmaps_negative_aspects_by_theme.csv",
        ["theme_code", "theme_label", "matched_negative_clause_count"],
        summary_rows,
    )

    negative_clause_unmatched = negative_clause_ids - matched_negative_clause_ids
    audit_rows = [
        {"metric": "negative_reviews_rating_le_3", "value": len(negative_review_ids), "note": "Jumlah review negatif dengan rating <= 3"},
        {"metric": "negative_clauses_detected", "value": len(negative_clause_ids), "note": "Jumlah clauses/kalimat negatif yang terdeteksi"},
        {
            "metric": "negative_clauses_matched_to_theme",
            "value": len(matched_negative_clause_ids),
            "note": "Jumlah clauses negatif yang berhasil dipetakan ke tema",
        },
        {
            "metric": "negative_clauses_unmatched",
            "value": len(negative_clause_unmatched),
            "note": "Jumlah clauses negatif yang belum berhasil dipetakan ke tema",
        },
        {
            "metric": "negative_aspect_mapping_rows",
            "value": len(mapping_rows),
            "note": "Jumlah total pasangan negative clause x tema",
        },
    ]
    write_csv(OUTPUT_DIR / "gmaps_negative_aspect_audit.csv", ["metric", "value", "note"], audit_rows)

    summary = "\n".join(
        [
            "# Google Maps Negative Aspect Theme Mapping",
            "",
            "Mapping ini memakai basis review negatif dengan definisi `rating <= 3`, lalu hanya memetakan kalimat atau clause yang mengandung sinyal keluhan.",
            "",
            f"- Negative reviews (`rating <= 3`): `{len(negative_review_ids)}`",
            f"- Negative clauses detected: `{len(negative_clause_ids)}`",
            f"- Negative clauses matched to theme: `{len(matched_negative_clause_ids)}`",
            f"- Negative clauses unmatched: `{len(negative_clause_unmatched)}`",
            f"- Negative clause x theme mapping rows: `{len(mapping_rows)}`",
            "",
            "## Output",
            "",
            "- `gmaps_negative_aspect_theme_mapping.csv`",
            "- `gmaps_negative_aspects_by_theme.csv`",
            "- `gmaps_negative_aspect_audit.csv`",
            "- `gmaps_negative_signal_lexicon.csv`",
        ]
    )
    (OUTPUT_DIR / "gmaps_negative_aspect_theme_mapping.md").write_text(summary, encoding="utf-8")

    print(f"[negative_aspect_mapping] saved negative aspect mapping under {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
