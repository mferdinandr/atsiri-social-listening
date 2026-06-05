# Atsiri Data Pipeline

Repositori ini dipakai untuk scraping, pembersihan, dan persiapan analisis data Rumah Atsiri dari:
- Google Maps reviews
- Instagram posts
- Instagram comments

Status proyek saat ini sudah melewati fase mini test dan full scraping dasar. Dataset final resmi yang dipakai untuk analisis sekarang berada di `data/datasets/clean/consolidated/`.

## Struktur Folder

```text
.
├── README.md
├── DATA_CONSUMPTION_PROGRESS.md
├── project_tracking/
├── data/
│   ├── raw/
│   ├── processed/
│   ├── datasets/
│   │   ├── all/
│   │   └── clean/
│   │       └── consolidated/
│   └── final/
└── scripts/
    ├── apify/
    ├── google_maps/
    ├── instagram_posts/
    ├── instagram_comments/
    ├── normalize/
    ├── finalize/
    └── theme_discovery/
```

## Fungsi Tiap Folder

### `data/raw/`
Hasil scrape asli dari actor Apify. File di sini tidak diubah manual.

- `data/raw/google_maps/full_run/`
  Raw full scrape Google Maps utama
- `data/raw/instagram_posts/all_posts/`
  Raw semua post Instagram Atsiri
- `data/raw/instagram_comments/batch_001` s.d. `batch_007`
  Raw comments Instagram per batch

### `data/processed/`
Output normalisasi per run atau per batch sebelum dikonsolidasikan lebih lanjut.

### `data/datasets/all/`
Dataset hasil scrape yang masih menyimpan semua row per source/per batch, termasuk yang belum lolos filter teks.

### `data/datasets/clean/`
Dataset yang sudah lolos filter teks dan siap dipakai untuk analisis.

Subfolder penting:
- `data/datasets/clean/shared/`
  Dataset reusable yang cukup dibangun sekali, misalnya `instagram_posts`
- `data/datasets/clean/full_run/`
  Dataset clean hasil full run Google Maps
- `data/datasets/clean/consolidated/`
  **Sumber final resmi untuk analisis**

### `data/final/`
Dokumen ringkasan, schema, progress, theme discovery, visualisasi, dan output analisis pendukung.

Subfolder penting:
- `data/final/theme_discovery/`
  Hasil eksplorasi tema dari post Atsiri
- `data/final/batch_*`
  Ringkasan per batch historis
- `data/final/full_run/`
  Ringkasan Google Maps full run

### `project_tracking/`
Ringkasan naratif per tahap supaya progres proyek tidak tercecer.

### `scripts/`
Script operasional proyek.

- `scripts/apify/`
  Helper umum untuk menjalankan actor Apify
- `scripts/google_maps/`
  Inisialisasi test/batch Google Maps
- `scripts/instagram_posts/`
  Inisialisasi dan indexing post Instagram
- `scripts/instagram_comments/`
  Seleksi post dan setup scraping comments
- `scripts/normalize/`
  Normalisasi raw menjadi tabel
- `scripts/finalize/`
  Konsolidasi dataset dan progress
- `scripts/theme_discovery/`
  Eksplorasi tema dan visualisasi awal

## Dataset Final Resmi

Gunakan folder ini sebagai sumber utama untuk analisis:
- `data/datasets/clean/consolidated/gmaps_reviews_clean.csv`
- `data/datasets/clean/consolidated/gmaps_reviewers_clean.csv`
- `data/datasets/clean/consolidated/instagram_posts_clean.csv`
- `data/datasets/clean/consolidated/instagram_comments_clean.csv`

Ringkasan inventarisnya ada di:
- `data/datasets/clean/consolidated/README.md`

## Ringkasan Data Saat Ini

- Google Maps reviews clean: `3937`
- Google Maps reviewers: `7878`
- Instagram posts clean: `1461`
- Instagram comments clean: `3585`

Catatan:
- `instagram_comments_clean.csv` merupakan hasil gabungan batch `001` sampai `007`
- `gmaps_reviewers_clean.csv` diambil dari tabel reviewer publik hasil full run Google Maps

## Dokumentasi Progress

Untuk membaca progres proyek dengan cepat:

1. `project_tracking/README.md`
2. `project_tracking/01_data_collection_summary.md`
3. `project_tracking/02_scraping_execution_summary.md`
4. `project_tracking/03_theme_discovery_summary.md`
5. `project_tracking/04_codebook_v1_summary.md`
6. `project_tracking/05_theme_visualization_summary.md`

Dokumen induk yang lebih detail:
- `DATA_CONSUMPTION_PROGRESS.md`

## Theme Discovery dan Codebook

Hasil eksplorasi tema brand-side Atsiri ada di:
- `data/final/theme_discovery/atsiri_theme_summary_for_dosen.md`
- `data/final/theme_discovery/atsiri_theme_candidates.csv`
- `data/final/theme_discovery/atsiri_theme_review_summary.csv`
- `data/final/theme_discovery/atsiri_post_theme_mapping_full.csv`
- `data/final/theme_discovery/atsiri_theme_period_summary.csv`

Codebook final v1:
- `data/final/theme_discovery/atsiri_theme_codebook_v1.csv`
- `data/final/theme_discovery/atsiri_theme_codebook_v1.md`

Visualisasi awal:
- `data/final/theme_discovery/figures/fig_01_atsiri_theme_distribution_overall.svg`
- `data/final/theme_discovery/figures/fig_02_atsiri_theme_distribution_by_period.svg`
- `data/final/theme_discovery/figures/fig_03_atsiri_top_hashtags.svg`
- `data/final/theme_discovery/figures/fig_04_atsiri_top_bigrams.svg`

## Setup

Isi `.env`:

```bash
APIFY_API_TOKEN=token_apify_kamu
DATA_TIMEZONE=Asia/Jakarta
PLACE_NAME=Rumah Atsiri Indonesia
INSTAGRAM_USERNAME=rumahatsiri
```

## Script yang Paling Sering Dipakai

### Rebuild consolidated clean datasets

```bash
rtk python3 scripts/finalize/build_consolidated_clean_datasets.py
```

### Rebuild master progress

```bash
rtk python3 scripts/finalize/build_master_progress.py
```

### Rebuild theme discovery Atsiri

```bash
rtk python3 scripts/theme_discovery/explore_atsiri_posts.py
```

### Rebuild visualisasi theme discovery

```bash
rtk python3 scripts/theme_discovery/build_atsiri_theme_visuals.py
```

## Catatan Penting

- `raw` = hasil scrape asli
- `clean/consolidated` = final resmi untuk analisis
- `final/` = summary, schema, theme discovery, visualisasi, dan progress
- `comment_count` metadata Instagram tidak sama dengan jumlah comment yang benar-benar berhasil discrape
- untuk post dengan `comment_count > 20`:
  - komentar teoretis menurut metadata: `7875`
  - komentar real yang berhasil discrape: `5351`
  - komentar clean: `3585`
