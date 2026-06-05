# Summary Tahap 1: Hasil Pengumpulan Data

Dokumen ini merangkum data utama yang sudah berhasil dikumpulkan dan akan menjadi dasar analisis paper.

## Tujuan Tahap Ini

- Menyelesaikan pengumpulan data utama dari setiap sumber.
- Memastikan ada dataset yang cukup untuk analisis brand-side dan customer-side.
- Menyediakan dataset yang sudah dipisahkan antara versi `all` dan `clean`.

## Hasil Data yang Sudah Dimiliki

### 1. Google Maps Reviews

Sumber utama aktif berasal dari full scrape Google Maps:
- `data/datasets/all/full_run/gmaps_reviews_all.csv`
- `data/datasets/clean/full_run/gmaps_reviews_clean.csv`

Hasil:
- total review `all`: `7878`
- total review `clean`: `3937`

Catatan:
- dataset `all` menyimpan seluruh hasil scrape
- dataset `clean` menyimpan review yang teksnya layak dipakai untuk analisis
- full run ini menjadi sumber utama final untuk Google Maps

### 2. Google Maps Reviewers

Tabel reviewer aktif:
- `data/datasets/all/full_run/gmaps_reviewers_all.csv`

Hasil:
- total reviewer: `7878`

Catatan:
- tabel ini dipakai untuk membaca karakter reviewer berdasarkan jumlah total review yang mereka miliki
- bucket reviewer yang dipakai ke depan adalah:
  - `0–500`
  - `501–1000`
  - `1001–1500`
  - `1501–2000`
  - `>2000`

### 3. Instagram Posts Atsiri

Sumber utama aktif:
- `data/datasets/all/shared/instagram_posts_all.csv`
- `data/datasets/clean/shared/instagram_posts_clean.csv`

Hasil:
- total post `all`: `1463`
- total post `clean`: `1461`

Catatan:
- dataset ini dipakai sebagai sumber utama untuk membaca signal dari brand Atsiri
- post tidak perlu discrape ulang karena sudah dipakai sebagai shared dataset

### 4. Instagram Comments

Sumber aktif berasal dari batch `001` sampai `007`.

Hasil:
- total comments `all`: `5351`
- total comments `clean`: `3585`
- total post prioritas yang tercakup: `144`

Catatan:
- comments diambil dari post prioritas dengan `comment_count > 20`
- comments dipakai sebagai salah satu representasi signal yang muncul dari pelanggan

## Posisi Data Saat Ini

Secara umum, proyek sudah memiliki tiga kelompok data utama:
- signal dari brand: Instagram posts Atsiri
- signal pelanggan utama: Google Maps reviews
- signal pelanggan tambahan: Instagram comments

Dengan data ini, proyek sudah siap untuk masuk ke tahap pengelompokan tema dan analisis per periode waktu.
