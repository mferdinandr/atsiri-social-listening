from __future__ import annotations

import csv
from pathlib import Path
from xml.sax.saxutils import escape


ROOT = Path("data") / "final" / "theme_discovery"
FIGURES_DIR = ROOT / "figures"


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


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


def svg_header(width: int, height: int) -> list[str]:
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
    ]


def svg_footer() -> list[str]:
    return ["</svg>"]


def save_svg(path: Path, lines: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def add_text(lines: list[str], x: float, y: float, text: str, size: int = 12, weight: str = "normal", anchor: str = "start", fill: str = "#222") -> None:
    lines.append(
        f'<text x="{x}" y="{y}" font-family="Arial, Helvetica, sans-serif" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" fill="{fill}">{escape(text)}</text>'
    )


def draw_horizontal_bar_chart(
    labels: list[str],
    values: list[int],
    title: str,
    xlabel: str,
    output_path: Path,
    color: str,
) -> None:
    width = 1000
    top = 70
    left = 250
    right = 80
    row_h = 34
    bar_h = 20
    bottom = 70
    height = top + bottom + row_h * len(labels)
    chart_w = width - left - right
    max_value = max(values) if values else 1

    lines = svg_header(width, height)
    add_text(lines, width / 2, 32, title, size=20, weight="bold", anchor="middle")
    add_text(lines, left + chart_w / 2, height - 20, xlabel, size=12, anchor="middle")
    lines.append(f'<line x1="{left}" y1="{top}" x2="{left}" y2="{height - bottom}" stroke="#333" stroke-width="1"/>')

    for i, (label, value) in enumerate(zip(labels, values)):
        y = top + i * row_h + 8
        bar_w = 0 if max_value == 0 else (value / max_value) * (chart_w - 10)
        add_text(lines, left - 10, y + 10, label, size=11, anchor="end")
        lines.append(f'<rect x="{left}" y="{y}" width="{bar_w}" height="{bar_h}" fill="{color}"/>')
        add_text(lines, left + bar_w + 8, y + 14, str(value), size=11)

    lines.extend(svg_footer())
    save_svg(output_path, lines)


def draw_stacked_bar_chart(periods: list[str], series: dict[str, list[int]], title: str, output_path: Path) -> None:
    width = 1100
    height = 620
    left = 90
    right = 260
    top = 70
    bottom = 90
    chart_w = width - left - right
    chart_h = height - top - bottom
    colors = ["#2E6F5E", "#4C956C", "#73A942", "#B5C99A", "#FFC857", "#D95D39", "#6C757D", "#8E5572"]

    totals = [sum(series[label][i] for label in series) for i in range(len(periods))]
    max_total = max(totals) if totals else 1
    bar_group_w = chart_w / max(len(periods), 1)
    bar_w = bar_group_w * 0.6

    lines = svg_header(width, height)
    add_text(lines, width / 2, 32, title, size=20, weight="bold", anchor="middle")
    lines.append(f'<line x1="{left}" y1="{top}" x2="{left}" y2="{top + chart_h}" stroke="#333" stroke-width="1"/>')
    lines.append(f'<line x1="{left}" y1="{top + chart_h}" x2="{left + chart_w}" y2="{top + chart_h}" stroke="#333" stroke-width="1"/>')

    for idx, period in enumerate(periods):
        x = left + idx * bar_group_w + (bar_group_w - bar_w) / 2
        y_cursor = top + chart_h
        total = totals[idx] if idx < len(totals) else 0
        for color_idx, label in enumerate(series):
            value = series[label][idx]
            seg_h = 0 if max_total == 0 else (value / max_total) * chart_h
            y_cursor -= seg_h
            lines.append(f'<rect x="{x}" y="{y_cursor}" width="{bar_w}" height="{seg_h}" fill="{colors[color_idx % len(colors)]}"/>')
        add_text(lines, x + bar_w / 2, top + chart_h + 25, period, size=11, anchor="middle")
        total_y = top + chart_h - (0 if max_total == 0 else (total / max_total) * chart_h) - 8
        add_text(lines, x + bar_w / 2, total_y, str(total), size=10, anchor="middle")

    legend_x = left + chart_w + 20
    legend_y = top + 20
    for idx, label in enumerate(series):
        y = legend_y + idx * 28
        lines.append(f'<rect x="{legend_x}" y="{y - 12}" width="16" height="16" fill="{colors[idx % len(colors)]}"/>')
        add_text(lines, legend_x + 24, y, label, size=11)

    lines.extend(svg_footer())
    save_svg(output_path, lines)


def plot_theme_distribution() -> None:
    rows = read_csv_rows(ROOT / "atsiri_theme_review_summary.csv")
    rows.sort(key=lambda row: int(row["matched_post_count"]))
    labels = [sanitize_label(row["theme_label"]) for row in rows]
    values = [int(row["matched_post_count"]) for row in rows]
    draw_horizontal_bar_chart(
        labels,
        values,
        "Distribusi Tema Atsiri Secara Keseluruhan",
        "Jumlah Post Terdeteksi",
        FIGURES_DIR / "fig_01_atsiri_theme_distribution_overall.svg",
        "#2E6F5E",
    )


def plot_theme_by_period() -> None:
    rows = read_csv_rows(ROOT / "atsiri_theme_period_summary.csv")
    period_order = ["2016-2017", "2018-2019", "2020-2021", "2022-2023", "2024-2025", "2026"]
    theme_order = [
        "Aromatic Products",
        "Plants and Garden",
        "Museum and Education",
        "Wellness Experience",
        "Culinary",
        "Glamping",
        "Destination",
        "Event and Campaign",
    ]

    pivot: dict[str, dict[str, int]] = {period: {} for period in period_order}
    for row in rows:
        period = row["time_bucket"]
        theme = sanitize_label(row["theme_label"])
        pivot.setdefault(period, {})[theme] = int(row["matched_post_count"])

    series = {
        theme: [pivot.get(period, {}).get(theme, 0) for period in period_order]
        for theme in theme_order
    }

    draw_stacked_bar_chart(
        period_order,
        series,
        "Distribusi Tema Atsiri per Periode Waktu",
        FIGURES_DIR / "fig_02_atsiri_theme_distribution_by_period.svg",
    )


def plot_top_hashtags() -> None:
    rows = read_csv_rows(ROOT / "atsiri_top_hashtags.csv")[:15]
    rows.sort(key=lambda row: int(row["count"]))
    labels = [f"#{row['hashtag']}" for row in rows]
    values = [int(row["count"]) for row in rows]
    draw_horizontal_bar_chart(
        labels,
        values,
        "Top 15 Hashtag Post Atsiri",
        "Frekuensi",
        FIGURES_DIR / "fig_03_atsiri_top_hashtags.svg",
        "#8E5572",
    )


def plot_top_bigrams() -> None:
    rows = read_csv_rows(ROOT / "atsiri_top_bigrams.csv")[:15]
    rows.sort(key=lambda row: int(row["count"]))
    labels = [row["bigram"] for row in rows]
    values = [int(row["count"]) for row in rows]
    draw_horizontal_bar_chart(
        labels,
        values,
        "Top 15 Bigram Caption Atsiri",
        "Frekuensi",
        FIGURES_DIR / "fig_04_atsiri_top_bigrams.svg",
        "#D95D39",
    )


def write_summary() -> None:
    summary = "\n".join(
        [
            "# Atsiri Theme Discovery Visuals",
            "",
            "Visualisasi ini dibuat dari hasil theme discovery post Instagram Atsiri.",
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
    plot_theme_distribution()
    plot_theme_by_period()
    plot_top_hashtags()
    plot_top_bigrams()
    write_summary()
    print(f"[theme_visuals] saved figures under {FIGURES_DIR}")


if __name__ == "__main__":
    main()
