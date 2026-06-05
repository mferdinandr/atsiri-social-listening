# Data Consumption Progress

Dokumen ini dipakai untuk mencatat progres konsumsi/analisis data agar arah kerja tetap konsisten dan tidak lupa saat diskusi metodologi berubah.

## Pusat Dokumentasi Ringkas

Folder ringkasan per tahap sekarang ada di:
- `project_tracking/README.md`
- `project_tracking/01_data_collection_summary.md`
- `project_tracking/02_scraping_execution_summary.md`
- `project_tracking/03_theme_discovery_summary.md`

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
- `architecture_landscape`

### Hasil review kandidat saat ini
- `aromatic_products` → `keep`
- `plants_garden` → `keep`
- `museum_education` → `keep`
- `wellness_experience` → `refine`
- `culinary_resto` → `keep`
- `glamping_stay` → `keep`
- `destination_tourism` → `refine`
- `event_campaign` → `refine`
- `architecture_landscape` → `merge` ke `destination_tourism`

### Arah keputusan sementara
- `aromatic_products` dan `wellness_experience` **tidak digabung dulu**
- `wellness_experience` harus diperketat agar hashtag slogan tidak otomatis melabeli tema
- `destination_tourism` dipertahankan dengan definisi sempit
- `architecture_landscape` tidak dipakai sebagai tema mandiri

### Paket yang siap dikirim ke dosen
- `atsiri_theme_summary_for_dosen.md` sebagai ringkasan utama
- `atsiri_theme_review_summary.csv` sebagai daftar ringkas kandidat tema
- `atsiri_theme_candidates.csv` sebagai detail kandidat tema
- `atsiri_post_theme_mapping_full.csv` sebagai bukti mapping per post
- `atsiri_theme_period_summary.csv` sebagai ringkasan per periode

## Catatan Penting

- Angka `comment_count` metadata Instagram tidak sama dengan hasil real scrape comments.
- Untuk post dengan `comment_count > 20`:
  - total komentar teoretis menurut metadata: `7875`
  - komentar yang benar-benar berhasil discrape: `5351`
  - clean comments: `3585`
- Jadi analisis ke depan harus membedakan:
  - **metadata count**
  - **real scraped count**
