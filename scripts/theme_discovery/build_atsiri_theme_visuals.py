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


ROOT = Path("data") / "final" / "theme_discovery"
FIGURES_DIR = ROOT / "figures"
PERIOD_ORDER = ["2016-2017", "2018-2019", "2020-2021", "2022-2023", "2024-2025", "2026"]
THEME_ORDER = [
    "Aromatic Products",
    "Plants and Garden",
    "Museum and Education",
    "Wellness Experience",
    "Culinary",
    "Glamping",
    "Destination",
    "Event and Campaign",
]
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


def sanitize_label(value: str) -> str:
    return (
        value.replace("Aromatic Products and Essential Oils", "Aromatic Products")
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
    plt.rcParams["axes.titlesize"] = 18
    plt.rcParams["axes.labelsize"] = 12
    plt.rcParams["xtick.labelsize"] = 10
    plt.rcParams["ytick.labelsize"] = 10
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
    ax.set_xlabel("Periode", labelpad=10)
    ax.set_ylabel(ylabel)
    ax.legend(title="Tema", bbox_to_anchor=(0.98, 1.0), loc="upper left", frameon=False)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{int(x):,}".replace(",", ".")))
    ax.tick_params(axis="x", pad=-4)
    style_axis(ax, "y")
    add_period_totals(ax, totals)
    save_current_figure(output_path)


def plot_theme_distribution() -> None:
    df = pd.read_csv(ROOT / "atsiri_theme_review_summary.csv")
    df["theme_label"] = df["theme_label"].map(sanitize_label)
    df = df.sort_values("matched_post_count", ascending=True)
    colors = [THEME_COLOR_MAP[label] for label in df["theme_label"]]

    plt.figure(figsize=(11, 6))
    ax = plt.gca()
    ax.barh(df["theme_label"], df["matched_post_count"], color=colors, height=0.82, edgecolor="none")
    ax.set_title("Distribusi Tema Atsiri Secara Keseluruhan")
    ax.set_xlabel("Jumlah Post Terdeteksi")
    ax.set_ylabel("")
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{int(x):,}".replace(",", ".")))
    style_axis(ax, "x")
    ax.margins(y=0.02)
    add_bar_labels_horizontal(ax, df["matched_post_count"].tolist())
    save_current_figure(FIGURES_DIR / "fig_01_atsiri_theme_distribution_overall.svg")


def plot_theme_by_period() -> None:
    df = pd.read_csv(ROOT / "atsiri_theme_period_summary.csv")
    df["theme_label"] = df["theme_label"].map(sanitize_label)
    df["time_bucket"] = pd.Categorical(df["time_bucket"], categories=PERIOD_ORDER, ordered=True)

    pivot = (
        df.pivot_table(index="time_bucket", columns="theme_label", values="matched_post_count", aggfunc="sum", fill_value=0)
        .reindex(index=PERIOD_ORDER, columns=THEME_ORDER, fill_value=0)
    )
    plot_stacked_period_chart(
        pivot,
        "Distribusi Tema Atsiri per Periode Waktu",
        "Jumlah Post Terdeteksi",
        FIGURES_DIR / "fig_02_atsiri_theme_distribution_by_period.svg",
    )


def plot_top_hashtags() -> None:
    df = pd.read_csv(ROOT / "atsiri_top_hashtags.csv").head(15).copy()
    df["label"] = "#" + df["hashtag"].astype(str)
    df = df.sort_values("count", ascending=True)

    plt.figure(figsize=(11, 7))
    ax = plt.gca()
    ax.barh(df["label"], df["count"], color="#7C5C9A", height=0.82, edgecolor="none")
    ax.set_title("Top 15 Hashtag Post Atsiri")
    ax.set_xlabel("Frekuensi")
    ax.set_ylabel("")
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{int(x):,}".replace(",", ".")))
    style_axis(ax, "x")
    ax.margins(y=0.02)
    add_bar_labels_horizontal(ax, df["count"].tolist())
    save_current_figure(FIGURES_DIR / "fig_03_atsiri_top_hashtags.svg")


def plot_top_bigrams() -> None:
    df = pd.read_csv(ROOT / "atsiri_top_bigrams.csv").head(15).copy()
    df = df.sort_values("count", ascending=True)

    plt.figure(figsize=(11, 7))
    ax = plt.gca()
    ax.barh(df["bigram"], df["count"], color="#D97D54", height=0.82, edgecolor="none")
    ax.set_title("Top 15 Bigram Caption Atsiri")
    ax.set_xlabel("Frekuensi")
    ax.set_ylabel("")
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{int(x):,}".replace(",", ".")))
    style_axis(ax, "x")
    ax.margins(y=0.02)
    add_bar_labels_horizontal(ax, df["count"].tolist())
    save_current_figure(FIGURES_DIR / "fig_04_atsiri_top_bigrams.svg")


def write_summary() -> None:
    summary = "\n".join(
        [
            "# Atsiri Theme Discovery Visuals",
            "",
            "Visualisasi ini dibuat dari hasil theme discovery post Instagram Atsiri menggunakan matplotlib dan seaborn.",
            "",
            "## File Figure",
            "- `fig_01_atsiri_theme_distribution_overall.svg`",
            "- `fig_02_atsiri_theme_distribution_by_period.svg`",
            "- `fig_03_atsiri_top_hashtags.svg`",
            "- `fig_04_atsiri_top_bigrams.svg`",
            "",
            "## Tujuan",
            "- melihat distribusi tema secara keseluruhan",
            "- melihat distribusi tema per bucket waktu",
            "- melihat hashtag dominan brand",
            "- melihat frasa dua kata yang paling sering muncul di caption",
        ]
    )
    (ROOT / "atsiri_theme_visuals_summary.md").write_text(summary, encoding="utf-8")


def main() -> None:
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    setup_theme()
    plot_theme_distribution()
    plot_theme_by_period()
    plot_top_hashtags()
    plot_top_bigrams()
    write_summary()
    print(f"[theme_visuals] saved figures under {FIGURES_DIR}")


if __name__ == "__main__":
    main()
