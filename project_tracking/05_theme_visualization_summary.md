# Summary Tahap 5: Visualisasi Theme Discovery Atsiri

Dokumen ini merangkum visualisasi awal yang dibuat dari hasil theme discovery post Instagram Atsiri.

Seluruh visual tahap ini sekarang sudah diregenerate menggunakan `matplotlib` dan `seaborn` agar lebih layak untuk kebutuhan paper.

## Tujuan Tahap Ini

- Menyediakan visual yang mudah dibaca untuk diskusi dengan dosen.
- Menunjukkan distribusi tema brand secara keseluruhan dan per periode waktu.
- Menunjukkan hashtag dan frasa caption yang paling dominan.

## Output Visual yang Dibuat

Visual disimpan di:
- `data/final/theme_discovery/figures/`

File yang tersedia:
- `fig_01_atsiri_theme_distribution_overall.svg`
- `fig_02_atsiri_theme_distribution_by_period.svg`
- `fig_03_atsiri_top_hashtags.svg`
- `fig_04_atsiri_top_bigrams.svg`

## Penjelasan Tiap Visual

### 1. Distribusi tema keseluruhan
- File: `fig_01_atsiri_theme_distribution_overall.svg`
- Fungsi:
  memperlihatkan tema Atsiri mana yang paling sering muncul di seluruh post

### 2. Distribusi tema per periode
- File: `fig_02_atsiri_theme_distribution_by_period.svg`
- Fungsi:
  memperlihatkan perubahan distribusi tema pada bucket waktu:
  - `2016–2017`
  - `2018–2019`
  - `2020–2021`
  - `2022–2023`
  - `2024–2025`
  - `2026`

### 3. Top hashtag Atsiri
- File: `fig_03_atsiri_top_hashtags.svg`
- Fungsi:
  memperlihatkan hashtag yang paling dominan sebagai signal eksplisit brand

### 4. Top bigram caption Atsiri
- File: `fig_04_atsiri_top_bigrams.svg`
- Fungsi:
  memperlihatkan frasa dua kata yang paling sering muncul dalam caption

## Catatan

- Visual ini baru mencakup sisi brand, yaitu post Instagram Atsiri.
- Visual customer-side belum dibuat karena mapping tema ke Google Maps reviews dan Instagram comments belum dijalankan.
- Paket visual ini cocok dipakai sebagai checkpoint sebelum lanjut ke tahap mapping customer-side.
