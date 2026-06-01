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
│   │   ├── google_maps/
│   │   └── instagram/
│   ├── processed/
│   └── final/
└── scripts/
```

## Tujuan tiap folder

- `data/raw/`: hasil export mentah dari Apify
- `data/processed/`: disiapkan untuk tahap berikutnya
- `data/final/`: disiapkan untuk tahap berikutnya
- `scripts/`: semua script kerja

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

## Langkah kerja

1. Buat folder batch:

```bash
python3 scripts/init_batch.py --source google_maps --batch 1
python3 scripts/init_batch.py --source instagram --batch 1
```

2. Jalankan mini test Google Maps via API Apify:

Edit dulu file:

- `data/raw/google_maps/batch_001/apify_input.example.json`

Lalu jalankan:

```bash
python3 scripts/run_apify_actor.py \
  --actor-id Xb8osYTtOjlsgI6k9 \
  --input data/raw/google_maps/batch_001/apify_input.example.json \
  --output data/raw/google_maps/batch_001/raw_export.json
```

3. Untuk Instagram posts, isi dulu:

- `data/raw/instagram/batch_001/apify_posts_input.example.json`

Lalu jalankan:

```bash
python3 scripts/run_apify_actor.py \
  --actor-id shu8hvrXbJbY3Eb9W \
  --input data/raw/instagram/batch_001/apify_posts_input.example.json \
  --output data/raw/instagram/batch_001/posts_raw.json
```

4. Kalau kamu sudah punya export post CSV, buat daftar URL post otomatis untuk comments:

```bash
python3 scripts/extract_instagram_post_urls.py \
  --input /Users/user/Downloads/ig-post-scraper.csv \
  --output-txt data/raw/instagram/batch_001/comment_post_urls.txt \
  --output-json data/raw/instagram/batch_001/apify_comments_input.generated.json \
  --limit 5 \
  --min-comments 1
```

5. Jalankan comments actor:

```bash
python3 scripts/run_apify_actor.py \
  --actor-id shu8hvrXbJbY3Eb9W \
  --input data/raw/instagram/batch_001/apify_comments_input.generated.json \
  --output data/raw/instagram/batch_001/comments_raw.json
```

6. Kalau kamu masih pakai file export manual dari dashboard, taruh hasil export mentah ke:

- `data/raw/google_maps/batch_001/`
- `data/raw/instagram/batch_001/`

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
