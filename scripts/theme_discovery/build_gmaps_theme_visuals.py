from __future__ import annotations

import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", str(Path(".cache") / "matplotlib"))

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.ticker import FuncFormatter, PercentFormatter


ROOT = Path("data") / "final" / "theme_mapping" / "google_maps"
FIGURES_DIR = ROOT / "figures"

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
PERIOD_ORDER = ["2016-2017", "2018-2019", "2020-2021", "2022-2023", "2024-2025", "2026"]
REVIEWER_BUCKET_ORDER = ["0-500", "501-1000", "1001-1500", "1501-2000", ">2000"]
PALETTE = ["#2E6F5E", "#4C956C", "#73A942", "#A7C957", "#FFC857", "#D95D39", "#8E5572", "#6C757D"]
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
REVIEWER_BUCKET_COLORS = ["#DCEAF7", "#A8D0E6", "#6FA8DC", "#457B9D", "#1D3557"]


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


def ordered_theme_labels(df: pd.DataFrame) -> list[str]:
    theme_map = {
        row["theme_code"]: short_label(row["theme_label"])
        for _, row in df.drop_duplicates("theme_code")[["theme_code", "theme_label"]].iterrows()
    }
    return [theme_map.get(theme_code, theme_code) for theme_code in THEME_ORDER]


def style_axis(ax: plt.Axes, grid_axis: str = "x") -> None:
    ax.grid(axis=grid_axis, linestyle="-", linewidth=0.6, alpha=0.35)
    sns.despine(ax=ax, left=False, bottom=False)


def add_bar_labels_horizontal(ax: plt.Axes, values: list[int]) -> None:
    max_value = max(values) if values else 0
    pad = max_value * 0.01 if max_value else 1
    for patch, value in zip(ax.patches, values):
        x = patch.get_width()
        y = patch.get_y() + patch.get_height() / 2
        ax.text(x + pad, y, f"{value:,}".replace(",", "."), va="center", ha="left", fontsize=10, color="#222222")


def add_period_totals(ax: plt.Axes, totals: list[int]) -> None:
    max_total = max(totals) if totals else 0
    pad = max_total * 0.015 if max_total else 1
    for idx, total in enumerate(totals):
        ax.text(idx, total + pad, f"{total:,}".replace(",", "."), ha="center", va="bottom", fontsize=10, color="#222222")


def plot_stacked_period_chart(pivot: pd.DataFrame, title: str, ylabel: str, output_path: Path) -> None:
    theme_labels = pivot.columns.tolist()
    colors = [THEME_COLOR_MAP[theme] for theme in theme_labels]
    totals = pivot.sum(axis=1).tolist()
    ax = pivot.plot(kind="bar", stacked=True, figsize=(12.8, 7), color=colors, width=0.9, edgecolor="white", linewidth=1)
    ax.set_title(title)
    ax.set_xlabel("Periode", labelpad=8)
    ax.set_ylabel(ylabel)
    ax.legend(title="Tema", bbox_to_anchor=(0.98, 1.0), loc="upper left", frameon=False)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{int(x):,}".replace(",", ".")))
    ax.tick_params(axis="x", pad=-3)
    style_axis(ax, "y")
    add_period_totals(ax, totals)
    save_current_figure(output_path)


def plot_overall() -> None:
    df = pd.read_csv(ROOT / "gmaps_theme_overall_summary.csv")
    df["theme_label"] = df["theme_label"].map(short_label)
    df = df.sort_values("matched_review_count", ascending=True)
    colors = [THEME_COLOR_MAP[label] for label in df["theme_label"]]

    plt.figure(figsize=(11, 6))
    ax = plt.gca()
    ax.barh(df["theme_label"], df["matched_review_count"], color=colors, height=0.82, edgecolor="none")
    ax.set_title("Distribusi Tema Google Maps Secara Keseluruhan")
    ax.set_xlabel("Jumlah Review yang Match")
    ax.set_ylabel("")
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{int(x):,}".replace(",", ".")))
    style_axis(ax, "x")
    ax.margins(y=0.02)
    add_bar_labels_horizontal(ax, df["matched_review_count"].tolist())
    save_current_figure(FIGURES_DIR / "fig_07_gmaps_theme_distribution_overall.svg")


def plot_by_period() -> None:
    df = pd.read_csv(ROOT / "gmaps_theme_period_summary.csv")
    df["theme_label"] = df["theme_label"].map(short_label)
    df["time_bucket"] = pd.Categorical(df["time_bucket"], categories=PERIOD_ORDER, ordered=True)

    theme_labels = ordered_theme_labels(df)
    pivot = (
        df.pivot_table(index="time_bucket", columns="theme_label", values="matched_review_count", aggfunc="sum", fill_value=0)
        .reindex(index=PERIOD_ORDER, columns=theme_labels, fill_value=0)
    )
    plot_stacked_period_chart(
        pivot,
        "Distribusi Tema Google Maps per Periode",
        "Jumlah Review yang Match",
        FIGURES_DIR / "fig_08_gmaps_theme_distribution_by_period.svg",
    )


def plot_by_reviewer_bucket() -> None:
    df = pd.read_csv(ROOT / "gmaps_theme_reviewer_bucket_summary.csv")
    df["theme_label"] = df["theme_label"].map(short_label)

    theme_labels = ordered_theme_labels(df)
    pivot = (
        df.pivot_table(index="theme_label", columns="reviewer_bucket", values="matched_review_count", aggfunc="sum", fill_value=0)
        .reindex(index=theme_labels, columns=REVIEWER_BUCKET_ORDER, fill_value=0)
    )
    row_totals = pivot.sum(axis=1).replace(0, 1)
    pivot_share = pivot.div(row_totals, axis=0)
    totals = pivot.sum(axis=1).tolist()

    ax = pivot_share.plot(kind="barh", stacked=True, figsize=(12, 7), color=REVIEWER_BUCKET_COLORS, width=0.88)
    ax.set_title("Komposisi Reviewer Bucket per Tema Google Maps")
    ax.set_xlabel("Proporsi dalam Tema")
    ax.set_ylabel("")
    ax.legend(title="Reviewer Bucket", bbox_to_anchor=(1.02, 1), loc="upper left", frameon=False)
    ax.xaxis.set_major_formatter(PercentFormatter(1.0))
    style_axis(ax, "x")
    for idx, total in enumerate(totals):
        ax.text(1.01, idx, f"{total:,}".replace(",", "."), va="center", ha="left", fontsize=10, color="#222222", transform=ax.get_yaxis_transform())
    save_current_figure(FIGURES_DIR / "fig_09_gmaps_theme_by_reviewer_bucket.svg")


def plot_theme_bucket_heatmap() -> None:
    df = pd.read_csv(ROOT / "gmaps_theme_reviewer_bucket_summary.csv")
    df["theme_label"] = df["theme_label"].map(short_label)

    theme_labels = ordered_theme_labels(df)
    pivot = (
        df.pivot_table(index="theme_label", columns="reviewer_bucket", values="matched_review_count", aggfunc="sum", fill_value=0)
        .reindex(index=theme_labels, columns=REVIEWER_BUCKET_ORDER, fill_value=0)
    )

    plt.figure(figsize=(10.5, 6.8))
    ax = sns.heatmap(
        pivot,
        annot=True,
        fmt="d",
        cmap=sns.light_palette("#2E6F5E", as_cmap=True),
        linewidths=0.6,
        linecolor="white",
        cbar_kws={"label": "Jumlah Review yang Match", "shrink": 0.9},
    )
    ax.set_title("Heatmap Tema x Reviewer Bucket Google Maps")
    ax.set_xlabel("Reviewer Bucket")
    ax.set_ylabel("")
    save_current_figure(FIGURES_DIR / "fig_10_gmaps_theme_reviewer_bucket_heatmap.svg")


def write_summary() -> None:
    summary = "\n".join(
        [
            "# Google Maps Theme Visuals",
            "",
            "Visualisasi ini dibuat dari hasil mapping tema Google Maps reviews menggunakan matplotlib dan seaborn.",
            "",
            "## File Figure",
            "- `fig_07_gmaps_theme_distribution_overall.svg`",
            "- `fig_08_gmaps_theme_distribution_by_period.svg`",
            "- `fig_09_gmaps_theme_by_reviewer_bucket.svg`",
            "- `fig_10_gmaps_theme_reviewer_bucket_heatmap.svg`",
            "",
            "## Tujuan",
            "- melihat tema Google Maps yang paling dominan",
            "- melihat distribusi tema per bucket waktu 2 tahunan",
            "- melihat komposisi reviewer bucket per tema",
            "- melihat berapa kali setiap tema dibahas oleh masing-masing reviewer bucket",
        ]
    )
    (ROOT / "gmaps_theme_visuals_summary.md").write_text(summary, encoding="utf-8")


def main() -> None:
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    setup_theme()
    plot_overall()
    plot_by_period()
    plot_by_reviewer_bucket()
    plot_theme_bucket_heatmap()
    write_summary()
    print(f"[theme_visuals] saved Google Maps figures under {FIGURES_DIR}")


if __name__ == "__main__":
    main()
