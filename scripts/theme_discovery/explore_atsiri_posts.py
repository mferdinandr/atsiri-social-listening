from __future__ import annotations

import csv
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path


ROOT = Path("data")
POSTS_PATH = ROOT / "datasets" / "all" / "shared" / "instagram_posts_all.csv"
OUTPUT_DIR = ROOT / "final" / "theme_discovery"


STOPWORDS = {
    "dan",
    "yang",
    "untuk",
    "dengan",
    "dari",
    "pada",
    "dalam",
    "oleh",
    "akan",
    "atau",
    "agar",
    "jadi",
    "juga",
    "adalah",
    "hingga",
    "bagi",
    "tidak",
    "sudah",
    "setiap",
    "satu",
    "hari",
    "tahun",
    "baru",
    "banyak",
    "seperti",
    "melalui",
    "apa",
    "sendiri",
    "salam",
    "kita",
    "kami",
    "bisa",
    "dapat",
    "this",
    "that",
    "with",
    "from",
    "your",
    "our",
    "the",
    "and",
    "for",
    "you",
    "are",
    "was",
    "were",
    "have",
    "has",
    "had",
    "can",
    "not",
    "all",
    "just",
    "about",
    "into",
    "their",
    "them",
    "its",
    "it",
    "new",
    "more",
    "one",
    "two",
    "three",
}


TIME_BUCKETS = [
    ("2016", "2017", "2016-2017"),
    ("2018", "2019", "2018-2019"),
    ("2020", "2021", "2020-2021"),
    ("2022", "2023", "2022-2023"),
    ("2024", "2025", "2024-2025"),
    ("2026", "2026", "2026"),
]


@dataclass
class ThemeRule:
    theme_code: str
    theme_label: str
    evidence_hashtags: list[str]
    evidence_keywords: list[str]
    rationale: str
    review_note: str


THEME_RULES = [
    ThemeRule(
        "aromatic_products",
        "Aromatic Products and Essential Oils",
        ["essentialoils", "atsirishop", "thearomaofindonesia", "atsiri"],
        ["essential oil", "essential oils", "minyak atsiri", "produk", "aroma", "wangi", "parfum"],
        "Muncul kuat dari hashtag essential oils/shop dan kosakata minyak, aroma, wangi, produk.",
        "Dipertahankan sebagai tema mandiri yang mewakili signal produk, essential oils, dan shop.",
    ),
    ThemeRule(
        "plants_garden",
        "Plants, Garden, and Botanicals",
        ["rumahatsiriplants", "atsiriplants", "atsirigardenstory", "taman"],
        ["tanaman", "bunga", "marigold", "garden", "taman", "citronella", "plants", "aromatic garden"],
        "Muncul dari fokus tanaman atsiri, taman aromatik, marigold, dan citronella.",
        "Dipertahankan karena sangat grounded ke identitas kebun/tanaman Atsiri.",
    ),
    ThemeRule(
        "museum_education",
        "Museum, Education, and Workshop",
        ["museumatsiri", "visitmuseumatsiri2017", "workshop", "rumahatsiriclass", "rumahatsirimuseum", "rumahatsirilab"],
        ["museum", "workshop", "class", "kelas", "lab", "tur", "factory", "pabrik", "knowledge", "edukasi"],
        "Muncul dari hashtag museum/class/lab dan kata workshop, kelas, museum, tur, pabrik.",
        "Dipertahankan sebagai tema inti tentang pembelajaran, museum, workshop, dan tur edukatif.",
    ),
    ThemeRule(
        "wellness_experience",
        "Wellness and Signature Experience",
        ["experiencetheessence", "aromatesexperience"],
        ["wellness", "experience", "healing", "relax", "self care", "aromatic wellness"],
        "Muncul sangat kuat dari hashtag experience dan kata wellness/experience.",
        "Dipertahankan tetapi harus diperketat; hashtag slogan seperti #ExperienceTheEssence tidak boleh berdiri sendiri tanpa konteks wellness.",
    ),
    ThemeRule(
        "culinary_resto",
        "Culinary and Resto",
        ["rumahatsiriresto", "rumahatsirirecipe"],
        ["resto", "recipe", "menu", "tea", "kuliner", "makanan", "minuman"],
        "Muncul dari resto/recipe dan kata tentang makanan-minuman.",
        "Dipertahankan sebagai tema kuliner/resto yang cukup jelas dan relevan untuk perbandingan dengan pelanggan.",
    ),
    ThemeRule(
        "glamping_stay",
        "Glamping and Stay",
        ["atsiriglamping"],
        ["glamping", "stay", "cabin", "camp", "room", "menginap"],
        "Muncul dari hashtag glamping dan kata tentang pengalaman menginap.",
        "Dipertahankan sebagai tema mandiri karena cukup spesifik dan stabil lintas periode.",
    ),
    ThemeRule(
        "destination_tourism",
        "Destination and Tourism",
        [
            "tawangmangu",
            "karanganyar",
            "plumbon",
            "wonderfulindonesia",
            "visitindonesia",
            "rumahatsiriarchitecture",
            "rumahatsirilandscape",
        ],
        [
            "wisata",
            "berkunjung",
            "visit",
            "destination",
            "travel",
            "tawangmangu",
            "karanganyar",
            "architecture",
            "landscape",
            "design",
            "plaza",
            "space",
        ],
        "Muncul dari penanda lokasi/wisata seperti Tawangmangu, Karanganyar, visit Indonesia, serta framing arsitektur/landscape tempat.",
        "Dipertahankan dengan definisi sempit sebagai framing destinasi/kunjungan; sinyal architecture/landscape digabung ke tema ini.",
    ),
    ThemeRule(
        "event_campaign",
        "Event, Campaign, and Community",
        ["peoplebehindrai", "momenramadan", "atsiriartistplaylist", "atsiricuratedplaylist", "behindcloseddoors"],
        ["event", "promo", "campaign", "community", "playlist", "coming soon", "special", "program"],
        "Muncul dari kampanye musiman, playlist, people behind, dan kata program/event.",
        "Dipertahankan sebagai tema sekunder; keyword seperti program/special tidak boleh terlalu longgar.",
    ),
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


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def normalize_text(value: str) -> str:
    return (value or "").lower().strip()


def extract_hashtags(text: str) -> list[str]:
    return re.findall(r"#([a-z0-9_]+)", normalize_text(text))


def extract_tokens(text: str) -> list[str]:
    cleaned = re.sub(r"https?://\S+", " ", normalize_text(text))
    cleaned = re.sub(r"[@#][a-z0-9_]+", " ", cleaned)
    return [token for token in re.findall(r"[a-z]{3,}", cleaned) if token not in STOPWORDS]


def year_bucket(post_date: str) -> str:
    year = (post_date or "")[:4]
    for start, end, label in TIME_BUCKETS:
        if start <= year <= end:
            return label
    return "unknown"


def match_theme(text: str, hashtags: list[str], rule: ThemeRule) -> tuple[bool, list[str], list[str]]:
    normalized = normalize_text(text)
    hashtag_hits = [tag for tag in rule.evidence_hashtags if tag in hashtags]
    keyword_hits = [kw for kw in rule.evidence_keywords if kw in normalized]
    return bool(hashtag_hits or keyword_hits), hashtag_hits, keyword_hits


def main() -> None:
    posts = read_csv_rows(POSTS_PATH)

    hashtag_counts: Counter[str] = Counter()
    word_counts: Counter[str] = Counter()
    bigram_counts: Counter[str] = Counter()

    theme_post_counts: Counter[str] = Counter()
    theme_period_counts: dict[tuple[str, str], int] = Counter()
    theme_examples: dict[str, list[str]] = defaultdict(list)
    mapping_rows: list[dict[str, str]] = []
    mapping_rows_full: list[dict[str, str]] = []

    for row in posts:
        caption = row.get("caption", "")
        hashtags = extract_hashtags(caption)
        for hashtag in hashtags:
            hashtag_counts[hashtag] += 1

        tokens = extract_tokens(caption)
        for token in tokens:
            word_counts[token] += 1
        for left, right in zip(tokens, tokens[1:]):
            bigram_counts[f"{left} {right}"] += 1

        bucket = year_bucket(row.get("post_date", ""))
        caption_snippet = caption.replace("\n", " ").strip()[:180]

        for rule in THEME_RULES:
            matched, hashtag_hits, keyword_hits = match_theme(caption, hashtags, rule)
            if not matched:
                continue
            theme_post_counts[rule.theme_code] += 1
            theme_period_counts[(rule.theme_code, bucket)] += 1
            if len(theme_examples[rule.theme_code]) < 5:
                theme_examples[rule.theme_code].append(caption_snippet)
            mapping_rows.append(
                {
                    "post_id": row.get("post_id", ""),
                    "post_date": row.get("post_date", ""),
                    "time_bucket": bucket,
                    "post_url": row.get("post_url", ""),
                    "theme_code": rule.theme_code,
                    "theme_label": rule.theme_label,
                    "matched_hashtags": "|".join(hashtag_hits),
                    "matched_keywords": "|".join(keyword_hits),
                    "caption_snippet": caption_snippet,
                }
            )
            mapping_rows_full.append(
                {
                    "post_id": row.get("post_id", ""),
                    "post_date": row.get("post_date", ""),
                    "time_bucket": bucket,
                    "post_type": row.get("post_type", ""),
                    "post_url": row.get("post_url", ""),
                    "theme_code": rule.theme_code,
                    "theme_label": rule.theme_label,
                    "theme_review_note": rule.review_note,
                    "all_hashtags_detected": "|".join(hashtags),
                    "matched_hashtags": "|".join(hashtag_hits),
                    "matched_keywords": "|".join(keyword_hits),
                    "caption_full": caption,
                    "clean_caption": row.get("clean_caption", ""),
                }
            )

    write_csv(
        OUTPUT_DIR / "atsiri_top_hashtags.csv",
        ["hashtag", "count"],
        [{"hashtag": hashtag, "count": count} for hashtag, count in hashtag_counts.most_common()],
    )
    write_csv(
        OUTPUT_DIR / "atsiri_top_words.csv",
        ["word", "count"],
        [{"word": word, "count": count} for word, count in word_counts.most_common()],
    )
    write_csv(
        OUTPUT_DIR / "atsiri_top_bigrams.csv",
        ["bigram", "count"],
        [{"bigram": bigram, "count": count} for bigram, count in bigram_counts.most_common()],
    )

    candidate_rows: list[dict[str, str | int]] = []
    for rule in THEME_RULES:
        periods_present = [label for _, _, label in TIME_BUCKETS if theme_period_counts.get((rule.theme_code, label), 0) > 0]
        candidate_rows.append(
            {
                "theme_code": rule.theme_code,
                "theme_label": rule.theme_label,
                "rationale": rule.rationale,
                "evidence_hashtags": "|".join(rule.evidence_hashtags),
                "evidence_keywords": "|".join(rule.evidence_keywords),
                "matched_post_count": theme_post_counts.get(rule.theme_code, 0),
                "periods_present": "|".join(periods_present),
                "review_note": rule.review_note,
                "example_captions": " || ".join(theme_examples.get(rule.theme_code, [])),
            }
        )
    write_csv(
        OUTPUT_DIR / "atsiri_theme_candidates.csv",
        [
            "theme_code",
            "theme_label",
            "rationale",
            "evidence_hashtags",
            "evidence_keywords",
            "matched_post_count",
            "periods_present",
            "review_note",
            "example_captions",
        ],
        candidate_rows,
    )

    write_csv(
        OUTPUT_DIR / "atsiri_post_theme_mapping.csv",
        [
            "post_id",
            "post_date",
            "time_bucket",
            "post_url",
            "theme_code",
            "theme_label",
            "matched_hashtags",
            "matched_keywords",
            "caption_snippet",
        ],
        mapping_rows,
    )
    write_csv(
        OUTPUT_DIR / "atsiri_post_theme_mapping_full.csv",
        [
            "post_id",
            "post_date",
            "time_bucket",
            "post_type",
            "post_url",
            "theme_code",
            "theme_label",
            "theme_review_note",
            "all_hashtags_detected",
            "matched_hashtags",
            "matched_keywords",
            "caption_full",
            "clean_caption",
        ],
        mapping_rows_full,
    )

    period_rows: list[dict[str, str | int]] = []
    for rule in THEME_RULES:
        for _, _, label in TIME_BUCKETS:
            period_rows.append(
                {
                    "theme_code": rule.theme_code,
                    "theme_label": rule.theme_label,
                    "time_bucket": label,
                    "matched_post_count": theme_period_counts.get((rule.theme_code, label), 0),
                }
            )
    write_csv(
        OUTPUT_DIR / "atsiri_theme_period_summary.csv",
        ["theme_code", "theme_label", "time_bucket", "matched_post_count"],
        period_rows,
    )

    final_theme_rows = [
        {
            "theme_code": rule.theme_code,
            "theme_label": rule.theme_label,
            "review_note": rule.review_note,
            "matched_post_count": theme_post_counts.get(rule.theme_code, 0),
            "evidence_hashtags": "|".join(rule.evidence_hashtags),
            "evidence_keywords": "|".join(rule.evidence_keywords),
        }
        for rule in THEME_RULES
    ]
    write_csv(
        OUTPUT_DIR / "atsiri_theme_review_summary.csv",
        [
            "theme_code",
            "theme_label",
            "review_note",
            "matched_post_count",
            "evidence_hashtags",
            "evidence_keywords",
        ],
        final_theme_rows,
    )

    summary = "\n".join(
        [
            "# Atsiri Theme Discovery Summary",
            "",
            "Eksplorasi awal ini bersifat data-driven dari seluruh caption dan hashtag post Instagram Atsiri.",
            "",
            f"- Total post dibaca: {len(posts)}",
            f"- Total kandidat tema: {len(THEME_RULES)}",
            "",
            "## File output",
            "- `atsiri_top_hashtags.csv`",
            "- `atsiri_top_words.csv`",
            "- `atsiri_top_bigrams.csv`",
            "- `atsiri_theme_candidates.csv`",
            "- `atsiri_post_theme_mapping.csv`",
            "- `atsiri_post_theme_mapping_full.csv`",
            "- `atsiri_theme_period_summary.csv`",
            "- `atsiri_theme_review_summary.csv`",
            "",
            "## Catatan",
            "- Tema di file ini masih kandidat awal, belum dianggap codebook final.",
            "- Mapping bersifat multi-label: satu post bisa masuk lebih dari satu tema.",
            "- Output ini dimaksudkan untuk diperdebatkan dulu sebelum dipakai ke Google Maps reviews dan Instagram comments.",
        ]
    )
    write_text(OUTPUT_DIR / "atsiri_theme_discovery_summary.md", summary)
    print(f"[theme_discovery] saved outputs under {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
