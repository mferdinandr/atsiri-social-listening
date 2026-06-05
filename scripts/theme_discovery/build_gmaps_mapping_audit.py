from __future__ import annotations

import csv
import os
from collections import Counter
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", str(Path(".cache") / "matplotlib"))

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter


ROOT = Path("data")
ALL_REVIEWS_PATH = ROOT / "datasets" / "all" / "full_run" / "gmaps_reviews_all.csv"
CLEAN_REVIEWS_PATH = ROOT / "datasets" / "clean" / "consolidated" / "gmaps_reviews_clean.csv"
MAPPING_PATH = ROOT / "final" / "theme_mapping" / "google_maps" / "gmaps_review_theme_mapping.csv"
OUTPUT_DIR = ROOT / "final" / "theme_mapping" / "google_maps"
FIGURES_DIR = OUTPUT_DIR / "figures"


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, headers: list[str], rows: list[dict[str, str | int | float]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def setup_theme() -> None:
    sns.set_theme(style="whitegrid", context="talk")
    plt.rcParams["font.family"] = "DejaVu Sans"
    plt.rcParams["svg.fonttype"] = "none"
    plt.rcParams["axes.facecolor"] = "#FCFCFA"
    plt.rcParams["figure.facecolor"] = "white"
    plt.rcParams["grid.color"] = "#D9D9D9"
    plt.rcParams["grid.alpha"] = 0.45


def save_current_figure(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(path, format="svg", bbox_inches="tight")
    plt.close()


def style_axis(ax: plt.Axes) -> None:
    ax.grid(axis="y", linestyle="-", linewidth=0.6, alpha=0.35)
    sns.despine(ax=ax, left=False, bottom=False)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{int(x):,}".replace(",", ".")))


def plot_audit_funnel(raw_count: int, clean_count: int, matched_count: int, unmatched_count: int) -> None:
    labels = ["Raw", "Clean", "Matched", "Unmatched"]
    values = [raw_count, clean_count, matched_count, unmatched_count]
    colors = ["#6C757D", "#2E6F5E", "#4C956C", "#D95D39"]

    plt.figure(figsize=(9, 5.5))
    ax = sns.barplot(x=labels, y=values, hue=labels, palette=colors, legend=False)
    ax.set_title("Google Maps Review Audit Funnel")
    ax.set_xlabel("")
    ax.set_ylabel("Jumlah Review")
    style_axis(ax)
    for idx, value in enumerate(values):
        ax.text(idx, value + max(values) * 0.015, f"{value}", ha="center", va="bottom", fontsize=10)
    save_current_figure(FIGURES_DIR / "fig_05_gmaps_review_audit_funnel.svg")


def plot_mapping_density(matched_count: int, mapping_count: int, multi_theme_count: int) -> None:
    labels = ["Matched Reviews", "Mapping Rows", "Multi-theme Reviews"]
    values = [matched_count, mapping_count, multi_theme_count]
    colors = ["#2E6F5E", "#8E5572", "#FFC857"]

    plt.figure(figsize=(9, 5.5))
    ax = sns.barplot(x=labels, y=values, hue=labels, palette=colors, legend=False)
    ax.set_title("Google Maps Theme Mapping Density")
    ax.set_xlabel("")
    ax.set_ylabel("Jumlah")
    style_axis(ax)
    for idx, value in enumerate(values):
        ax.text(idx, value + max(values) * 0.015, f"{value}", ha="center", va="bottom", fontsize=10)
    save_current_figure(FIGURES_DIR / "fig_06_gmaps_mapping_density.svg")


def main() -> None:
    setup_theme()

    all_reviews = read_csv_rows(ALL_REVIEWS_PATH)
    clean_reviews = read_csv_rows(CLEAN_REVIEWS_PATH)
    mapping_rows = read_csv_rows(MAPPING_PATH)

    review_counter = Counter(row.get("review_id", "") for row in mapping_rows if row.get("review_id", ""))
    matched_reviews = len(review_counter)
    unmatched_reviews = len(clean_reviews) - matched_reviews
    mapping_row_count = len(mapping_rows)
    multi_theme_reviews = sum(1 for count in review_counter.values() if count > 1)
    max_themes_per_review = max(review_counter.values()) if review_counter else 0
    avg_themes_per_matched_review = round(mapping_row_count / matched_reviews, 2) if matched_reviews else 0

    audit_rows = [
        {"metric": "raw_reviews_all", "value": len(all_reviews), "note": "Jumlah seluruh review hasil full scrape Google Maps"},
        {"metric": "clean_reviews", "value": len(clean_reviews), "note": "Jumlah review clean yang dipakai sebagai basis mapping tema"},
        {"metric": "matched_reviews", "value": matched_reviews, "note": "Jumlah review clean yang kena minimal satu tema"},
        {"metric": "unmatched_reviews", "value": unmatched_reviews, "note": "Jumlah review clean yang tidak kena tema mana pun"},
        {"metric": "mapping_rows", "value": mapping_row_count, "note": "Jumlah total pasangan review x tema"},
        {"metric": "multi_theme_reviews", "value": multi_theme_reviews, "note": "Jumlah review yang kena lebih dari satu tema"},
        {"metric": "max_themes_per_review", "value": max_themes_per_review, "note": "Jumlah tema terbanyak yang menempel pada satu review"},
        {"metric": "avg_themes_per_matched_review", "value": avg_themes_per_matched_review, "note": "Rata-rata tema per review yang berhasil dipetakan"},
    ]
    write_csv(OUTPUT_DIR / "gmaps_mapping_audit.csv", ["metric", "value", "note"], audit_rows)

    summary = "\n".join(
        [
            "# Google Maps Mapping Audit",
            "",
            "Dokumen ini menjelaskan perbedaan antara jumlah review yang berhasil dipetakan dan jumlah row mapping review x tema.",
            "",
            f"- Raw reviews all: `{len(all_reviews)}`",
            f"- Clean reviews: `{len(clean_reviews)}`",
            f"- Matched reviews: `{matched_reviews}`",
            f"- Unmatched reviews: `{unmatched_reviews}`",
            f"- Mapping rows: `{mapping_row_count}`",
            f"- Multi-theme reviews: `{multi_theme_reviews}`",
            f"- Max themes per review: `{max_themes_per_review}`",
            f"- Average themes per matched review: `{avg_themes_per_matched_review}`",
            "",
            "## Cara baca",
            "",
            "- `matched_reviews` adalah jumlah review unik yang kena minimal satu tema.",
            "- `mapping_rows` adalah jumlah total pasangan review x tema.",
            "- Karena satu review bisa masuk beberapa tema, `mapping_rows` selalu bisa lebih besar daripada `matched_reviews`.",
            "",
            "## Contoh",
            "",
            "Jika satu review membahas `museum_education`, `plants_garden`, dan `culinary_resto`, maka:",
            "- matched review = `1`",
            "- mapping row = `3`",
        ]
    )
    (OUTPUT_DIR / "gmaps_mapping_audit.md").write_text(summary, encoding="utf-8")

    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    plot_audit_funnel(len(all_reviews), len(clean_reviews), matched_reviews, unmatched_reviews)
    plot_mapping_density(matched_reviews, mapping_row_count, multi_theme_reviews)

    print(f"[theme_audit] saved Google Maps mapping audit under {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
