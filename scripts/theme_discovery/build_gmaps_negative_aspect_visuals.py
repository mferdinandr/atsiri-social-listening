from __future__ import annotations

import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", str(Path(".cache") / "matplotlib"))

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.ticker import FuncFormatter


ROOT = Path("data") / "final" / "theme_mapping" / "google_maps"
FIGURES_DIR = ROOT / "figures"
PERIOD_ORDER = ["2016-2017", "2018-2019", "2020-2021", "2022-2023", "2024-2025", "2026"]
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
THEME_COLOR_MAP = {
    "Aromatic Products": "#2E6F5E",
    "Plants and Garden": "#6BA368",
    "Museum and Education": "#3E7CB1",
    "Wellness Experience": "#9C6ADE",
    "Culinary": "#D97D54",
    "Glamping": "#B08D57",
    "Destination": "#4D908E",
    "Event and Campaign": "#C06C84",
}


def short_label(label: str) -> str:
    return (
        label.replace("Aromatic Products and Essential Oils", "Aromatic Products")
        .replace("Plants, Garden, and Botanicals", "Plants and Garden")
        .replace("Museum, Education, and Workshop", "Museum and Education")
        .replace("Wellness and Signature Experience", "Wellness Experience")
        .replace("Culinary and Resto", "Culinary")
        .replace("Glamping and Stay", "Glamping")
        .replace("Destination and Tourism", "Destination")
        .replace("Event, Campaign, and Community", "Event and Campaign")
    )


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


def style_axis(ax: plt.Axes, grid_axis: str = "x") -> None:
    ax.grid(axis=grid_axis, linestyle="-", linewidth=0.6, alpha=0.35)
    sns.despine(ax=ax, left=False, bottom=False)


def add_bar_labels_horizontal(ax: plt.Axes, values: list[int]) -> None:
    max_value = max(values) if values else 0
    pad = max_value * 0.015 if max_value else 1
    for patch, value in zip(ax.patches, values):
        x = patch.get_width()
        y = patch.get_y() + patch.get_height() / 2
        ax.text(x + pad, y, f"{value:,}".replace(",", "."), va="center", ha="left", fontsize=10, color="#222222")


def add_period_totals(ax: plt.Axes, totals: list[int]) -> None:
    max_total = max(totals) if totals else 0
    pad = max_total * 0.02 if max_total else 1
    for idx, total in enumerate(totals):
        ax.text(idx, total + pad, f"{total:,}".replace(",", "."), ha="center", va="bottom", fontsize=10, color="#222222")


def ordered_theme_labels(df: pd.DataFrame) -> list[str]:
    theme_map = {
        row["theme_code"]: short_label(row["theme_label"])
        for _, row in df.drop_duplicates("theme_code")[["theme_code", "theme_label"]].iterrows()
    }
    fallback_map = {
        "aromatic_products": "Aromatic Products",
        "plants_garden": "Plants and Garden",
        "museum_education": "Museum and Education",
        "wellness_experience": "Wellness Experience",
        "culinary_resto": "Culinary",
        "glamping_stay": "Glamping",
        "destination_tourism": "Destination",
        "event_campaign": "Event and Campaign",
    }
    return [theme_map.get(theme_code, fallback_map[theme_code]) for theme_code in THEME_ORDER]


def build_period_summary() -> pd.DataFrame:
    df = pd.read_csv(ROOT / "gmaps_negative_aspect_theme_mapping.csv")
    summary = (
        df.groupby(["theme_code", "theme_label", "time_bucket"], as_index=False)
        .size()
        .rename(columns={"size": "matched_negative_clause_count"})
    )
    summary.to_csv(ROOT / "gmaps_negative_aspects_period_summary.csv", index=False)
    return summary


def plot_overall() -> None:
    df = pd.read_csv(ROOT / "gmaps_negative_aspects_by_theme.csv")
    df["theme_label"] = df["theme_label"].map(short_label)
    df = df.sort_values("matched_negative_clause_count", ascending=True)
    colors = [THEME_COLOR_MAP[label] for label in df["theme_label"]]

    plt.figure(figsize=(11, 6))
    ax = plt.gca()
    ax.barh(df["theme_label"], df["matched_negative_clause_count"], color=colors, height=0.82, edgecolor="none")
    ax.set_title("Distribusi Negative Aspect Google Maps")
    ax.set_xlabel("Jumlah Clause Negatif yang Match")
    ax.set_ylabel("")
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{int(x):,}".replace(",", ".")))
    style_axis(ax, "x")
    ax.margins(y=0.02)
    add_bar_labels_horizontal(ax, df["matched_negative_clause_count"].tolist())
    save_current_figure(FIGURES_DIR / "fig_11_gmaps_negative_aspects_overall.svg")


def plot_by_period() -> None:
    df = build_period_summary()
    df["theme_label"] = df["theme_label"].map(short_label)
    df["time_bucket"] = pd.Categorical(df["time_bucket"], categories=PERIOD_ORDER, ordered=True)
    theme_labels = ordered_theme_labels(df)
    pivot = (
        df.pivot_table(index="time_bucket", columns="theme_label", values="matched_negative_clause_count", aggfunc="sum", fill_value=0)
        .reindex(index=PERIOD_ORDER, columns=theme_labels, fill_value=0)
    )
    totals = pivot.sum(axis=1).tolist()
    colors = [THEME_COLOR_MAP[theme] for theme in theme_labels]

    ax = pivot.plot(kind="bar", stacked=True, figsize=(12.8, 7), color=colors, width=0.9, edgecolor="white", linewidth=1)
    ax.set_title("Distribusi Negative Aspect Google Maps per Periode")
    ax.set_xlabel("Periode", labelpad=8)
    ax.set_ylabel("Jumlah Clause Negatif yang Match")
    ax.legend(title="Tema", bbox_to_anchor=(0.98, 1.0), loc="upper left", frameon=False)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{int(x):,}".replace(",", ".")))
    style_axis(ax, "y")
    add_period_totals(ax, totals)
    save_current_figure(FIGURES_DIR / "fig_12_gmaps_negative_aspects_by_period.svg")


def plot_audit() -> None:
    df = pd.read_csv(ROOT / "gmaps_negative_aspect_audit.csv")
    key_order = [
        "negative_reviews_rating_le_3",
        "negative_clauses_detected",
        "negative_clauses_matched_to_theme",
        "negative_clauses_unmatched",
        "negative_aspect_mapping_rows",
    ]
    label_map = {
        "negative_reviews_rating_le_3": "Neg Reviews",
        "negative_clauses_detected": "Neg Clauses",
        "negative_clauses_matched_to_theme": "Matched Clauses",
        "negative_clauses_unmatched": "Unmatched Clauses",
        "negative_aspect_mapping_rows": "Mapping Rows",
    }
    df = df.set_index("metric").reindex(key_order).reset_index()
    labels = [label_map[m] for m in df["metric"]]
    values = df["value"].astype(int).tolist()
    colors = ["#6C757D", "#D97D54", "#2E6F5E", "#C06C84", "#3E7CB1"]

    plt.figure(figsize=(10, 5.5))
    ax = sns.barplot(x=labels, y=values, hue=labels, palette=colors, legend=False)
    ax.set_title("Audit Negative Aspect Google Maps")
    ax.set_xlabel("")
    ax.set_ylabel("Jumlah")
    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{int(x):,}".replace(",", ".")))
    style_axis(ax, "y")
    for idx, value in enumerate(values):
        ax.text(idx, value + max(values) * 0.02, f"{value:,}".replace(",", "."), ha="center", va="bottom", fontsize=10)
    save_current_figure(FIGURES_DIR / "fig_13_gmaps_negative_aspect_audit.svg")


def write_summary() -> None:
    summary = "\n".join(
        [
            "# Google Maps Negative Aspect Visuals",
            "",
            "Visualisasi ini dibuat dari hasil mapping negative aspect Google Maps berbasis clause-level.",
            "",
            "## File Figure",
            "- `fig_11_gmaps_negative_aspects_overall.svg`",
            "- `fig_12_gmaps_negative_aspects_by_period.svg`",
            "- `fig_13_gmaps_negative_aspect_audit.svg`",
            "",
            "## File Tabel Pendukung",
            "- `gmaps_negative_aspects_by_theme.csv`",
            "- `gmaps_negative_aspects_period_summary.csv`",
            "- `gmaps_negative_aspect_audit.csv`",
        ]
    )
    (ROOT / "gmaps_negative_aspect_visuals_summary.md").write_text(summary, encoding="utf-8")


def main() -> None:
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    setup_theme()
    plot_overall()
    plot_by_period()
    plot_audit()
    write_summary()
    print(f"[negative_aspect_visuals] saved figures under {FIGURES_DIR}")


if __name__ == "__main__":
    main()
