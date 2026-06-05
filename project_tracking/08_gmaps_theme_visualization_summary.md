# Summary Tahap 8: Visualisasi Tema Google Maps

Dokumen ini merangkum visualisasi awal yang dibuat dari hasil mapping tema Google Maps reviews.

Seluruh visual tahap ini sekarang sudah diregenerate menggunakan `matplotlib` dan `seaborn` agar lebih layak untuk kebutuhan paper.

## Tujuan Tahap Ini

- Membuat visual yang cepat dibaca dari hasil mapping tema Google Maps.
- Menunjukkan distribusi tema secara keseluruhan dan per periode waktu.
- Menunjukkan keterkaitan tema dengan bucket reviewer.
- Menyediakan bahan visual awal sebelum lanjut ke Instagram comments.

## Output Visualisasi

Disimpan di:
- `data/final/theme_mapping/google_maps/`

File yang tersedia:
- `gmaps_theme_visuals_summary.md`
- `figures/fig_07_gmaps_theme_distribution_overall.svg`
- `figures/fig_08_gmaps_theme_distribution_by_period.svg`
- `figures/fig_09_gmaps_theme_by_reviewer_bucket.svg`
- `figures/fig_10_gmaps_theme_reviewer_bucket_heatmap.svg`

## Fungsi Tiap Figure

- `fig_07_gmaps_theme_distribution_overall.svg`
  Menunjukkan tema Google Maps yang paling dominan secara keseluruhan.
- `fig_08_gmaps_theme_distribution_by_period.svg`
  Menunjukkan distribusi tema per bucket waktu `2016–2017` sampai `2026`.
- `fig_09_gmaps_theme_by_reviewer_bucket.svg`
  Menunjukkan komposisi bucket reviewer pada setiap tema Google Maps.
- `fig_10_gmaps_theme_reviewer_bucket_heatmap.svg`
  Menunjukkan berapa kali setiap tema dibahas oleh masing-masing bucket reviewer.

## Catatan Baca

- Visualisasi ini dibangun dari hasil mapping yang sudah direfine.
- Basis sumbernya adalah `gmaps_reviews_clean.csv` dengan `2557` matched reviews dan `5438` row mapping review x tema.
- Figure ini bersifat deskriptif dan dipakai sebagai checkpoint visual sebelum analisis customer-side diperluas ke Instagram comments.
