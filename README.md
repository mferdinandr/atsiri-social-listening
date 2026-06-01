# Atsiri Data Pipeline

Struktur proyek ini saya sederhanakan khusus untuk tahap mini test.

## Struktur

```text
.
├── README.md
├── .env.example
├── pyproject.toml
├── data/
│   ├── raw/
│   │   ├── google_maps/
│   │   ├── instagram_posts/
│   │   └── instagram_comments/
│   ├── processed/
│   └── final/
└── scripts/
    ├── apify/
    ├── google_maps/
    ├── instagram_posts/
    ├── instagram_comments/
    └── normalize/
```

## Tujuan tiap folder

- `data/raw/google_maps/`: input dan output raw Google Maps
- `data/raw/instagram_posts/`: input test, output test, dan aset reusable semua post Instagram
- `data/raw/instagram_comments/`: input dan output raw komentar Instagram
- `data/processed/`: disiapkan untuk tahap berikutnya
- `data/final/`: schema final, audit field, dan dokumen acuan
- `scripts/apify/`: helper umum untuk menjalankan actor Apify
- `scripts/google_maps/`: script khusus Google Maps
- `scripts/instagram_posts/`: script khusus pengambilan dan indexing post Instagram
- `scripts/instagram_comments/`: script khusus seleksi URL post dan scraping komentar Instagram
- `scripts/normalize/`: script normalisasi raw test ke tabel final

## Struktur test

Fase sekarang memakai folder `test`. Folder `batch_xxx` baru dipakai nanti setelah mini test lolos validasi.

Contoh:

- `data/raw/google_maps/test/README.txt`
- `data/raw/google_maps/test/gmaps_input.json`
- `data/raw/google_maps/test/gmaps_output.json`
- `data/raw/google_maps/test/gmaps_output_run.json`
- `data/raw/instagram_posts/test/ig_posts_input.json`
- `data/raw/instagram_posts/all_posts/ig_posts_output.json`
- `data/raw/instagram_posts/all_posts/ig_posts_output_run.json`
- `data/raw/instagram_posts/all_posts/ig_post_index.json`
- `data/raw/instagram_posts/all_posts/ig_all_post_urls.txt`
- `data/raw/instagram_comments/test/README.txt`
- `data/raw/instagram_comments/test/ig_comments_input.json`
- `data/raw/instagram_comments/test/ig_comments_input.generated.json`
- `data/raw/instagram_comments/test/comment_post_urls.txt`
- `data/raw/instagram_comments/test/ig_comments_output.json`
- `data/raw/instagram_comments/test/ig_comments_output_run.json`

## Tool

- Scraping: `Apify`
- Processing: `Python 3.11+`
- Automation: `scripts/apify/run_actor.py`

## Install

Untuk fase sekarang, script yang aktif bisa jalan dengan `python3` standar.

Dependency data processing baru benar-benar dibutuhkan saat analisis lanjutan. Untuk normalisasi test saat ini, script masih berjalan dengan `python3` standar.

## Setup token

Isi `.env`:

```bash
APIFY_API_TOKEN=token_apify_kamu
DATA_TIMEZONE=Asia/Jakarta
PLACE_NAME=Rumah Atsiri Indonesia
INSTAGRAM_USERNAME=rumahatsiri
```

## Input yang dipakai actor

Google Maps `Xb8osYTtOjlsgI6k9`:

- `startUrls`: URL Google Maps tempat
- `maxCrawledPlacesPerSearch`: batasi jumlah place
- `maxReviews`: jumlah review yang ingin diambil
- `reviewsSort`: urutan review, untuk mini test pakai `newest`
- `reviewsOrigin`: pilih `google`
- `scrapeReviewsPersonalData`: sertakan reviewer id/url
- `language`: bahasa hasil detail

Instagram `shu8hvrXbJbY3Eb9W`:

- `directUrls`: daftar URL Instagram
- `resultsType`: `posts` atau `comments`
- `resultsLimit`: jumlah hasil per URL
- `addParentData`: opsional, berguna saat ambil posts dari profile URL

## Langkah kerja

1. Buat folder test:

```bash
python3 scripts/google_maps/init_test.py
python3 scripts/instagram_posts/init_test.py
python3 scripts/instagram_comments/init_test.py
```

2. Jalankan mini test Google Maps via API Apify:

Edit dulu file:

- `data/raw/google_maps/test/gmaps_input.json`

Default mini test sekarang memakai `startUrls` ke halaman Rumah Atsiri, review dari `google`, dan reviewer personal data aktif.

Lalu jalankan:

```bash
python3 scripts/apify/run_actor.py \
  --actor-id Xb8osYTtOjlsgI6k9 \
  --input data/raw/google_maps/test/gmaps_input.json \
  --output data/raw/google_maps/test/gmaps_output.json
```

3. Untuk Instagram posts, isi dulu:

- `data/raw/instagram_posts/test/ig_posts_input.json`

Default sekarang memakai URL profil `https://www.instagram.com/rumahatsiri/` dengan `resultsType: "posts"` dan `resultsLimit: 1500` agar bisa dipakai sebagai index master posts.

Lalu jalankan:

```bash
python3 scripts/apify/run_actor.py \
  --actor-id shu8hvrXbJbY3Eb9W \
  --input data/raw/instagram_posts/test/ig_posts_input.json \
  --output data/raw/instagram_posts/all_posts/ig_posts_output.json
```

4. Setelah output post tersedia, bangun index post yang bisa dipakai ulang:

```bash
python3 scripts/instagram_posts/build_post_index.py \
  --input data/raw/instagram_posts/all_posts/ig_posts_output.json \
  --output-json data/raw/instagram_posts/all_posts/ig_post_index.json \
  --output-txt data/raw/instagram_posts/all_posts/ig_all_post_urls.txt
```

5. Dari output post atau index, buat daftar URL post untuk comments:

```bash
python3 scripts/instagram_comments/extract_post_urls.py \
  --input data/raw/instagram_posts/all_posts/ig_post_index.json \
  --output-txt data/raw/instagram_comments/test/comment_post_urls.txt \
  --output-json data/raw/instagram_comments/test/ig_comments_input.generated.json \
  --limit 5 \
  --min-comments 1 \
  --sort-by-comments
```

File JSON hasil generator akan otomatis memakai `resultsType: "comments"` agar sesuai schema actor comments.

6. Jalankan comments actor:

```bash
python3 scripts/apify/run_actor.py \
  --actor-id shu8hvrXbJbY3Eb9W \
  --input data/raw/instagram_comments/test/ig_comments_input.generated.json \
  --output data/raw/instagram_comments/test/ig_comments_output.json
```

7. Kalau kamu masih pakai file export manual dari dashboard, taruh hasil export mentah ke:

- `data/raw/google_maps/test/`
- `data/raw/instagram_posts/test/`
- `data/raw/instagram_comments/test/`

## Field realistis untuk mini test

### Google Maps

- inti: `review_text`, `review_date`, `rating`
- tambahan yang layak diuji: `owner_response`, `review_like_count`, `reviewer_name`, `local_guide`
- terbatas: `local_guide_level`, `review_url`, statistik reviewer detail

### Instagram

- inti: `post_url`, `post_date`, `caption`, `comment_count`
- tambahan yang layak diuji: `like_count`, `post_type`, hashtag, mention
- paling terbatas: `share_count`, `view_count` universal, komentar teks lengkap

## Catatan

Fase sekarang fokus ke:

- setup test
- run actor dari terminal
- generate URL post untuk comments
- simpan raw JSON mini test

Setelah mini test lolos, langkah berikutnya adalah mengunci schema final dan menurunkan raw test ke bentuk tabel final.

## Schema final yang dipakai

- `data/final/mini_test_field_availability.md`
- `data/final/final_table_schema.md`

Dokumen pertama menjelaskan field mana yang `bisa`, `opsional`, `terbatas`, atau `derived`.

Dokumen kedua mengunci bentuk output tabel final yang akan dipakai sebelum masuk `batch_001`.

## Normalisasi raw test ke tabel final

Jalankan semua normalisasi sekaligus:

```bash
python3 scripts/normalize/test_to_final.py
```

Atau per sumber:

```bash
python3 scripts/normalize/google_maps.py
python3 scripts/normalize/instagram_posts.py
python3 scripts/normalize/instagram_comments.py
```

Output normalisasi test:

- `data/processed/test/google_maps/gmaps_reviews.csv`
- `data/processed/test/google_maps/gmaps_reviewers.csv`
- `data/processed/test/instagram_posts/instagram_posts.csv`
- `data/processed/test/instagram_comments/instagram_comments.csv`

## Batch 1

Setelah mini test lolos, `batch_001` dipakai sebagai batch validasi dosen.

Asumsi batch awal yang dipakai sekarang:

- Google Maps: `100` review terbaru
- Instagram posts: memakai sumber reusable `all_posts`
- Instagram comments: `10` post teratas yang memiliki komentar

Inisialisasi batch:

```bash
python3 scripts/google_maps/init_batch.py --batch 1 --max-reviews 100
python3 scripts/instagram_posts/init_batch.py --batch 1
python3 scripts/instagram_comments/init_batch.py --batch 1 --results-limit 30
python3 scripts/instagram_comments/prepare_batch.py --batch 1 --limit 10 --min-comments 1 --results-limit 30
```

Run actor:

```bash
python3 scripts/apify/run_actor.py \
  --actor-id Xb8osYTtOjlsgI6k9 \
  --input data/raw/google_maps/batch_001/gmaps_input.json \
  --output data/raw/google_maps/batch_001/gmaps_output.json
```

```bash
python3 scripts/apify/run_actor.py \
  --actor-id shu8hvrXbJbY3Eb9W \
  --input data/raw/instagram_comments/batch_001/ig_comments_input.generated.json \
  --output data/raw/instagram_comments/batch_001/ig_comments_output.json
```

Normalisasi batch:

```bash
python3 scripts/normalize/batch_001.py
```

Finalisasi batch:

```bash
python3 scripts/finalize/build_batch_final.py --batch-number batch_001
```

Output akhir batch:

- `data/processed/batch_001/google_maps/gmaps_reviews.csv`
- `data/processed/batch_001/google_maps/gmaps_reviewers.csv`
- `data/processed/batch_001/instagram_posts/instagram_posts.csv`
- `data/processed/batch_001/instagram_comments/instagram_comments.csv`
- `data/final/batch_001/gmaps_reviews_final.csv`
- `data/final/batch_001/gmaps_reviewers_final.csv`
- `data/final/batch_001/instagram_posts_final.csv`
- `data/final/batch_001/instagram_comments_final.csv`
- `data/final/batch_001/scraping_batches.csv`
- `data/final/batch_001/summary.md`

## Ringkasan automation

- `scripts/apify/run_actor.py`: menjalankan actor Apify dari terminal dan menyimpan hasil dataset ke JSON
- `scripts/instagram_posts/build_post_index.py`: membuat manifest reusable semua post Instagram dari output actor
- `scripts/instagram_comments/extract_post_urls.py`: mengambil `postUrl` dari hasil scrape post supaya comments bisa dijalankan batch tanpa copy-paste manual
- `scripts/instagram_comments/prepare_batch.py`: membentuk input batch komentar dari index `all_posts`
- `scripts/normalize/test_to_final.py`: menjalankan seluruh normalisasi raw test ke bentuk tabel final
