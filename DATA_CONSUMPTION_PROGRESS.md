# Data Consumption Progress

Dokumen ini dipakai untuk mencatat progres konsumsi/analisis data agar arah kerja tetap konsisten dan tidak lupa saat diskusi metodologi berubah.

## Pusat Dokumentasi Ringkas

Folder ringkasan per tahap sekarang ada di:
- `project_tracking/README.md`
- `project_tracking/01_data_collection_summary.md`
- `project_tracking/02_scraping_execution_summary.md`
- `project_tracking/03_theme_discovery_summary.md`
- `project_tracking/04_codebook_v1_summary.md`
- `project_tracking/05_theme_visualization_summary.md`
- `project_tracking/06_gmaps_theme_mapping_summary.md`
- `project_tracking/07_gmaps_mapping_audit_summary.md`
- `project_tracking/08_gmaps_theme_visualization_summary.md`
- `project_tracking/09_gmaps_negative_review_audit_summary.md`
- `project_tracking/10_gmaps_negative_aspect_mapping_summary.md`
- `project_tracking/11_gmaps_negative_aspect_visualization_summary.md`
- `project_tracking/12_gmaps_negative_signal_lexicon_summary.md`

## Status Data Saat Ini

### Google Maps
- Sumber utama aktif: `data/datasets/all/full_run/gmaps_reviews_all.csv`
- Versi clean: `data/datasets/clean/full_run/gmaps_reviews_clean.csv`
- Jumlah review all: `7878`
- Jumlah review clean: `3937`
- Tabel reviewer: `data/datasets/all/full_run/gmaps_reviewers_all.csv`
- Jumlah reviewer: `7878`

### Instagram Posts
- Sumber utama aktif: `data/datasets/all/shared/instagram_posts_all.csv`
- Versi clean: `data/datasets/clean/shared/instagram_posts_clean.csv`
- Jumlah post all: `1463`
- Jumlah post clean: `1461`

### Instagram Comments
- Sumber berasal dari batch `001` sampai `007`
- Total comments all terkumpul: `5351`
- Total comments clean terkumpul: `3585`
- Total post prioritas yang tercakup: `144`
- Strategi comments yang sudah selesai: semua post dengan `comment_count > 20`

## Status Struktur Analisis

Yang saat ini **masih ada dan dipakai**:
- `data/raw` untuk data mentah
- `data/processed` untuk hasil normalisasi
- `data/datasets/all` untuk semua hasil akhir per sumber/per batch
- `data/datasets/clean` untuk hasil clean per sumber/per batch
- `data/final` untuk summary/schema/progress

Yang **sudah direvert/dihapus**:
- `data/deliverables`
- `data/paper`
- `scripts/paper`
- `scripts/finalize/build_delivery_tables.py`

## Arah Baru dari Dosen

Fokus paper berubah menjadi:

1. Kelompokkan tema berdasarkan postingan Atsiri
   - sumber utama: caption dan hashtag Instagram Atsiri
2. Kelompokkan tema Google Maps reviews
3. Kelompokkan tema Instagram comments
4. Petakan Google reviewers berdasarkan jumlah review
5. Semua pengelompokan dilakukan per periode waktu
6. Plot keterkaitan tema Atsiri dengan review Google Maps berdasarkan kelompok reviewer
7. Analisis co-occurrence tema pada review dan komentar Instagram

## Keputusan yang Sudah Disepakati

### Bucket Reviewer Google Maps
- `0–500`
- `501–1000`
- `1001–1500`
- `1501–2000`
- `>2000`

### Bucket Waktu
- `2016–2017`
- `2018–2019`
- `2020–2021`
- `2022–2023`
- `2024–2025`
- `2026`

### Pendekatan Tema
- **Belum lock codebook final untuk semua sumber**
- Disepakati untuk **tidak langsung coding tema manual ke semua sumber dulu**
- Pendekatan yang lebih disukai saat ini:
  - eksplorasi seluruh caption + hashtag post Atsiri terlebih dahulu
  - dari sana identifikasi tema brand yang benar-benar muncul
  - setelah itu baru bentuk codebook final
  - codebook tersebut kemudian dipakai ke Google Maps reviews dan Instagram comments

## Posisi Metodologis Saat Ini

Saat ini kita sedang pivot dari:
- **codebook-driven dulu**

menjadi:
- **data-driven theme discovery dulu untuk post Atsiri**

Artinya:
- tema tidak dipaksakan sejak awal
- tema akan diturunkan dari seluruh caption dan hashtag post Atsiri
- baru setelah tema brand jelas, kita mapping ke reviews dan comments

## Hal yang Belum Dikerjakan

1. Menyusun codebook tema final dari hasil eksplorasi Atsiri
2. Mapping tema ke:
   - Instagram posts
   - Google Maps reviews
   - Instagram comments
3. Mapping Google reviewers ke bucket jumlah review
4. Agregasi seluruh hasil per bucket waktu
5. Visualisasi dan tabel untuk paper

## Next Step yang Disepakati

Next step **bukan coding full pipeline dulu**.

Urutan yang diinginkan:
1. diskusi tema apa saja yang benar-benar muncul dari post Atsiri
2. lock codebook tema final
3. baru lanjut implementasi pemetaan tema ke semua sumber data

## Status Theme Discovery Atsiri

Eksplorasi data-driven untuk post Atsiri **sudah dilakukan** dan output-nya ada di:
- `data/final/theme_discovery/atsiri_top_hashtags.csv`
- `data/final/theme_discovery/atsiri_top_words.csv`
- `data/final/theme_discovery/atsiri_top_bigrams.csv`
- `data/final/theme_discovery/atsiri_theme_candidates.csv`
- `data/final/theme_discovery/atsiri_post_theme_mapping.csv`
- `data/final/theme_discovery/atsiri_post_theme_mapping_full.csv`
- `data/final/theme_discovery/atsiri_theme_period_summary.csv`
- `data/final/theme_discovery/atsiri_theme_review_summary.csv`
- `data/final/theme_discovery/atsiri_theme_summary_for_dosen.md`

### Kandidat tema yang muncul dari post Atsiri
- `aromatic_products`
- `plants_garden`
- `museum_education`
- `wellness_experience`
- `culinary_resto`
- `glamping_stay`
- `destination_tourism`
- `event_campaign`

### Hasil review kandidat saat ini
- `aromatic_products` → `keep`
- `plants_garden` → `keep`
- `museum_education` → `keep`
- `wellness_experience` → `refine`
- `culinary_resto` → `keep`
- `glamping_stay` → `keep`
- `destination_tourism` → `refine`
- `event_campaign` → `refine`
- sinyal `architecture_landscape` → `merge` ke `destination_tourism`

### Arah keputusan sementara
- `aromatic_products` dan `wellness_experience` **tidak digabung dulu**
- `wellness_experience` harus diperketat agar hashtag slogan tidak otomatis melabeli tema
- `destination_tourism` dipertahankan dengan definisi sempit
- sinyal `architecture_landscape` tidak dipakai sebagai tema mandiri

### Paket yang siap dikirim ke dosen
- `atsiri_theme_summary_for_dosen.md` sebagai ringkasan utama
- `atsiri_theme_review_summary.csv` sebagai daftar ringkas kandidat tema
- `atsiri_theme_candidates.csv` sebagai detail kandidat tema
- `atsiri_post_theme_mapping_full.csv` sebagai bukti mapping per post
- `atsiri_theme_period_summary.csv` sebagai ringkasan per periode

## Status Codebook Final V1

Codebook final v1 untuk tema Atsiri **sudah disusun** dan output-nya ada di:
- `data/final/theme_discovery/atsiri_theme_codebook_v1.csv`
- `data/final/theme_discovery/atsiri_theme_codebook_v1.md`

Tema final v1 yang dipakai:
- `aromatic_products`
- `plants_garden`
- `museum_education`
- `wellness_experience`
- `culinary_resto`
- `glamping_stay`
- `destination_tourism`
- `event_campaign`

Catatan:
- sinyal `architecture_landscape` tidak dipakai sebagai tema mandiri
- diarahkan masuk ke `destination_tourism`

## Status Visualisasi Theme Discovery

Visualisasi awal untuk post Atsiri **sudah dibuat** dan output-nya ada di:
- `data/final/theme_discovery/figures/fig_01_atsiri_theme_distribution_overall.svg`
- `data/final/theme_discovery/figures/fig_02_atsiri_theme_distribution_by_period.svg`
- `data/final/theme_discovery/figures/fig_03_atsiri_top_hashtags.svg`
- `data/final/theme_discovery/figures/fig_04_atsiri_top_bigrams.svg`
- `data/final/theme_discovery/atsiri_theme_visuals_summary.md`

Visual Atsiri sekarang sudah diregenerate menggunakan `matplotlib` dan `seaborn`.

## Status Mapping Tema Google Maps

Mapping awal codebook v1 ke Google Maps reviews **sudah dijalankan** dan output-nya ada di:
- `data/final/theme_mapping/google_maps/gmaps_review_theme_mapping.csv`
- `data/final/theme_mapping/google_maps/gmaps_theme_overall_summary.csv`
- `data/final/theme_mapping/google_maps/gmaps_theme_period_summary.csv`
- `data/final/theme_mapping/google_maps/gmaps_theme_reviewer_bucket_summary.csv`
- `data/final/theme_mapping/google_maps/gmaps_theme_reviewer_bucket_period_summary.csv`
- `data/final/theme_mapping/google_maps/summary.md`

Ringkasan hasil awal:
- total review clean sumber: `3937`
- total review yang terkena minimal satu tema: `2557`
- total row mapping review x tema: `5438`

## Status Audit Mapping Google Maps

Audit untuk membedakan `matched reviews` dan `mapping rows` **sudah dibuat** dan output-nya ada di:
- `data/final/theme_mapping/google_maps/gmaps_mapping_audit.csv`
- `data/final/theme_mapping/google_maps/gmaps_mapping_audit.md`
- `data/final/theme_mapping/google_maps/figures/fig_05_gmaps_review_audit_funnel.svg`
- `data/final/theme_mapping/google_maps/figures/fig_06_gmaps_mapping_density.svg`

## Status Audit Review Negatif Google Maps

Audit review negatif Google Maps dengan definisi `rating <= 3` **sudah dibuat** dan output-nya ada di:
- `data/final/theme_mapping/google_maps/gmaps_negative_review_audit.csv`
- `data/final/theme_mapping/google_maps/gmaps_negative_review_theme_mapping.csv`
- `data/final/theme_mapping/google_maps/gmaps_negative_reviews_by_theme.csv`
- `data/final/theme_mapping/google_maps/gmaps_negative_review_audit.md`

Ringkasan hasil:
- negative reviews (`rating <= 3`): `195`
- negative reviews matched to theme: `104`
- negative reviews unmatched: `91`
- negative review x theme mapping rows: `193`

## Status Negative Aspect Mapping Google Maps

Mapping negative aspect berbasis clause/kalimat negatif pada review Google Maps **sudah dibuat** dan output-nya ada di:
- `data/final/theme_mapping/google_maps/gmaps_negative_aspect_theme_mapping.csv`
- `data/final/theme_mapping/google_maps/gmaps_negative_aspects_by_theme.csv`
- `data/final/theme_mapping/google_maps/gmaps_negative_aspect_audit.csv`
- `data/final/theme_mapping/google_maps/gmaps_negative_aspect_theme_mapping.md`
- `data/final/theme_mapping/google_maps/gmaps_negative_signal_lexicon.csv`
- `data/final/theme_mapping/google_maps/gmaps_negative_signal_lexicon.md`

Ringkasan hasil:
- negative reviews (`rating <= 3`): `195`
- negative clauses detected: `147`
- negative clauses matched to theme: `55`
- negative clauses unmatched: `92`
- negative clause x theme mapping rows: `76`

Catatan tambahan:
- negative aspect kini memakai lexicon terpisah yang bisa diaudit dan diedit
- `gmaps_negative_aspect_theme_mapping.csv` sekarang memuat `negative_strength` dan `negative_signal_groups`
- false positive `destination_tourism` dari nama lokasi generik pada clause resto sudah dikurangi

## Status Visualisasi Negative Aspect Google Maps

Visualisasi negative aspect Google Maps **sudah dibuat** dan output-nya ada di:
- `data/final/theme_mapping/google_maps/gmaps_negative_aspect_visuals_summary.md`
- `data/final/theme_mapping/google_maps/figures/fig_11_gmaps_negative_aspects_overall.svg`
- `data/final/theme_mapping/google_maps/figures/fig_12_gmaps_negative_aspects_by_period.svg`
- `data/final/theme_mapping/google_maps/figures/fig_13_gmaps_negative_aspect_audit.svg`

## Status Visualisasi Tema Google Maps

Visualisasi awal untuk hasil mapping tema Google Maps **sudah dibuat** dan output-nya ada di:
- `data/final/theme_mapping/google_maps/gmaps_theme_visuals_summary.md`
- `data/final/theme_mapping/google_maps/figures/fig_07_gmaps_theme_distribution_overall.svg`
- `data/final/theme_mapping/google_maps/figures/fig_08_gmaps_theme_distribution_by_period.svg`
- `data/final/theme_mapping/google_maps/figures/fig_09_gmaps_theme_by_reviewer_bucket.svg`
- `data/final/theme_mapping/google_maps/figures/fig_10_gmaps_theme_reviewer_bucket_heatmap.svg`

Visual Google Maps sekarang sudah diregenerate menggunakan `matplotlib` dan `seaborn`.

Fungsi visualisasi ini:
- melihat tema Google Maps yang paling dominan secara keseluruhan
- melihat distribusi tema per bucket waktu 2 tahunan
- melihat komposisi reviewer bucket per tema
- melihat berapa kali setiap tema dibahas oleh masing-masing reviewer bucket

## Catatan Penting

- Angka `comment_count` metadata Instagram tidak sama dengan hasil real scrape comments.
- Untuk post dengan `comment_count > 20`:
  - total komentar teoretis menurut metadata: `7875`
  - komentar yang benar-benar berhasil discrape: `5351`
  - clean comments: `3585`
- Jadi analisis ke depan harus membedakan:
  - **metadata count**
  - **real scraped count**
