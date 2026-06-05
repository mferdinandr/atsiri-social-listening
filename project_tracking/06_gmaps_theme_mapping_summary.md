# Summary Tahap 6: Mapping Tema Google Maps Reviews

Dokumen ini merangkum hasil penerapan codebook tema Atsiri v1 ke Google Maps reviews.

## Tujuan Tahap Ini

- Menerapkan tema brand-side Atsiri ke customer-side dataset utama, yaitu Google Maps reviews.
- Menghasilkan tabel mapping review ke tema.
- Menghasilkan ringkasan tema per periode waktu dan per reviewer bucket.

## Sumber Data

- Review utama: `data/datasets/clean/consolidated/gmaps_reviews_clean.csv`
- Reviewer utama: `data/datasets/clean/consolidated/gmaps_reviewers_clean.csv`
- Codebook: `data/final/theme_discovery/atsiri_theme_codebook_v1.csv`

## Output Tahap Ini

Disimpan di:
- `data/final/theme_mapping/google_maps/`

File yang tersedia:
- `gmaps_review_theme_mapping.csv`
- `gmaps_theme_overall_summary.csv`
- `gmaps_theme_period_summary.csv`
- `gmaps_theme_reviewer_bucket_summary.csv`
- `gmaps_theme_reviewer_bucket_period_summary.csv`
- `summary.md`

## Hasil Utama

- total review clean sumber: `3937`
- total review yang terkena minimal satu tema: `2557`
- total row mapping review x tema: `5438`

## Tema Teratas

- `museum_education` → `1510`
- `plants_garden` → `1101`
- `destination_tourism` → `915`
- `aromatic_products` → `838`
- `culinary_resto` → `761`

## Reviewer Bucket

Reviewer dibagi ke bucket:
- `0–500`
- `501–1000`
- `1001–1500`
- `1501–2000`
- `>2000`

Pada hasil awal, sebagian besar match memang masih terkonsentrasi di bucket `0–500`, sesuai distribusi reviewer yang sangat berat di kelompok ini.

## Catatan

- Hasil ini sudah memakai refinement awal agar match tidak terlalu longgar.
- Refinement utama yang diterapkan:
  - whole-word / whole-phrase matching
  - `wellness_experience` tidak lagi mengandalkan `rest` sebagai sinyal tunggal
  - `museum_education` tidak lagi mengandalkan `lab` sebagai sinyal tunggal
  - `aromatic_products` tidak lagi mengandalkan `aroma` atau `wangi` sebagai sinyal tunggal
  - `destination_tourism` tidak lagi mengandalkan `design` atau `space` sebagai sinyal tunggal
- Meski begitu, hasil ini tetap layak direview cepat lagi sebelum lanjut ke Instagram comments.
