# Summary Tahap 9: Audit Review Negatif Google Maps

Dokumen ini merangkum audit awal untuk review Google Maps negatif dengan definisi `rating <= 3`.

## Tujuan Tahap Ini

- Menentukan dulu berapa jumlah review negatif pada dataset Google Maps clean.
- Melihat berapa review negatif yang berhasil dipetakan ke tema.
- Mengetahui tema apa saja yang paling sering muncul pada review negatif.

## Output Audit

Disimpan di:
- `data/final/theme_mapping/google_maps/`

File yang tersedia:
- `gmaps_negative_review_audit.csv`
- `gmaps_negative_review_theme_mapping.csv`
- `gmaps_negative_reviews_by_theme.csv`
- `gmaps_negative_review_audit.md`

## Hasil Utama

- clean reviews: `3937`
- negative reviews (`rating <= 3`): `195`
- rating 1: `44`
- rating 2: `28`
- rating 3: `123`
- negative reviews matched to theme: `104`
- negative reviews unmatched: `91`
- negative review x theme mapping rows: `193`

## Tema yang Paling Sering Muncul pada Review Negatif

- `culinary_resto`: `56`
- `museum_education`: `48`
- `plants_garden`: `40`
- `destination_tourism`: `23`
- `aromatic_products`: `17`
- `glamping_stay`: `6`
- `wellness_experience`: `2`
- `event_campaign`: `1`

## Interpretasi Awal

- Dengan definisi `rating <= 3`, jumlah review negatif masih relatif kecil dibanding total review clean.
- Tidak semua review negatif berhasil masuk tema, jadi masih ada ruang untuk analisis aspect negatif yang lebih spesifik di luar codebook tema utama.
- Tema yang paling sering muncul pada review negatif saat ini condong ke `culinary_resto`, `museum_education`, dan `plants_garden`.
- File `gmaps_negative_review_theme_mapping.csv` bisa dipakai untuk audit per-row karena format kolomnya mengikuti `gmaps_review_theme_mapping.csv`, hanya difilter ke review `rating <= 3`.
