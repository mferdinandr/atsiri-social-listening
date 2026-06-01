# Atsiri Data Mini Test

Struktur proyek ini saya sederhanakan khusus untuk tahap mini test.

## Struktur

```text
.
├── README.md
├── .env.example
├── pyproject.toml
├── data/
│   ├── raw/
│   │   ├── input/
│   │   └── output/
│   ├── processed/
│   └── final/
└── scripts/
```

## Tujuan tiap folder

- `data/raw/input/`: file input actor, template JSON, dan daftar URL
- `data/raw/output/`: hasil export mentah dari Apify
- `data/processed/`: disiapkan untuk tahap berikutnya
- `data/final/`: disiapkan untuk tahap berikutnya
- `scripts/`: semua script kerja

## Struktur batch

Setiap batch sekarang dipisah ke area `input` dan `output`, lalu dikelompokkan lagi per source.

Contoh:

- `data/raw/input/google_maps/batch_001/README.txt`
- `data/raw/input/google_maps/batch_001/gmaps_input.json`
- `data/raw/output/google_maps/batch_001/gmaps_output.json`
- `data/raw/output/google_maps/batch_001/gmaps_run.json`
- `data/raw/input/instagram/batch_001/ig_posts_input.json`
- `data/raw/input/instagram/batch_001/ig_comments_input.json`
- `data/raw/input/instagram/batch_001/ig_comments_input.generated.json`
- `data/raw/input/instagram/batch_001/comment_post_urls.txt`
- `data/raw/output/instagram/batch_001/ig_posts_output.json`
- `data/raw/output/instagram/batch_001/ig_comments_output.json`

## Tool

- Scraping: `Apify`
- Processing: `Python 3.11+`
- Automation: `scripts/run_apify_actor.py`

## Install

Untuk fase sekarang, script yang aktif bisa jalan dengan `python3` standar.

Kalau nanti masuk tahap normalisasi/cleaning, baru pasang dependency data processing.

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

1. Buat folder batch:

```bash
python3 scripts/init_batch.py --source google_maps --batch 1
python3 scripts/init_batch.py --source instagram --batch 1
```

2. Jalankan mini test Google Maps via API Apify:

Edit dulu file:

- `data/raw/input/google_maps/batch_001/gmaps_input.json`

Default mini test sekarang memakai `startUrls` ke halaman Rumah Atsiri, review dari `google`, dan reviewer personal data aktif.

Lalu jalankan:

```bash
python3 scripts/run_apify_actor.py \
  --actor-id Xb8osYTtOjlsgI6k9 \
  --input data/raw/input/google_maps/batch_001/gmaps_input.json \
  --output data/raw/output/google_maps/batch_001/gmaps_output.json
```

3. Untuk Instagram posts, isi dulu:

- `data/raw/input/instagram/batch_001/ig_posts_input.json`

Default mini test sekarang memakai URL profil `https://www.instagram.com/rumahatsiri/` dengan `resultsType: "posts"`.

Lalu jalankan:

```bash
python3 scripts/run_apify_actor.py \
  --actor-id shu8hvrXbJbY3Eb9W \
  --input data/raw/input/instagram/batch_001/ig_posts_input.json \
  --output data/raw/output/instagram/batch_001/ig_posts_output.json
```

4. Kalau kamu sudah punya export post CSV, buat daftar URL post otomatis untuk comments:

```bash
python3 scripts/extract_instagram_post_urls.py \
  --input /Users/user/Downloads/ig-post-scraper.csv \
  --output-txt data/raw/input/instagram/batch_001/comment_post_urls.txt \
  --output-json data/raw/input/instagram/batch_001/ig_comments_input.generated.json \
  --limit 5 \
  --min-comments 1
```

File JSON hasil generator akan otomatis memakai `resultsType: "comments"` agar sesuai schema actor comments.

5. Jalankan comments actor:

```bash
python3 scripts/run_apify_actor.py \
  --actor-id shu8hvrXbJbY3Eb9W \
  --input data/raw/input/instagram/batch_001/ig_comments_input.generated.json \
  --output data/raw/output/instagram/batch_001/ig_comments_output.json
```

6. Kalau kamu masih pakai file export manual dari dashboard, taruh hasil export mentah ke:

- `data/raw/output/google_maps/batch_001/`
- `data/raw/output/instagram/batch_001/`

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

- setup batch
- run actor dari terminal
- generate URL post untuk comments
- simpan raw JSON mini test

Kalau mini test raw data sudah fix, baru kita tambahkan lagi script normalisasi dan cleaning.

## Ringkasan automation

- `run_apify_actor.py`: menjalankan actor Apify dari terminal dan menyimpan hasil dataset ke JSON
- `extract_instagram_post_urls.py`: mengambil `postUrl` dari hasil scrape post supaya comments bisa dijalankan batch tanpa copy-paste manual
