# Summary Tahap 10: Negative Aspect Mapping Google Maps

Dokumen ini merangkum mapping negative aspect untuk Google Maps dengan pendekatan clause-level, bukan review penuh.

## Tujuan Tahap Ini

- Mengurangi bias dari review `rating <= 3` yang isinya campuran antara pujian dan keluhan.
- Memetakan hanya kalimat atau clause yang benar-benar mengandung sinyal negatif.
- Mengetahui tema apa yang benar-benar menjadi lokasi keluhan pelanggan.

## Metode Singkat

- Basis review negatif: `rating <= 3`
- Teks review dipecah menjadi clause atau kalimat
- Hanya clause yang mengandung sinyal keluhan yang dipilih
- Theme mapping diterapkan ke clause negatif tersebut, bukan ke seluruh review

## Output

Disimpan di:
- `data/final/theme_mapping/google_maps/`

File yang tersedia:
- `gmaps_negative_aspect_theme_mapping.csv`
- `gmaps_negative_aspects_by_theme.csv`
- `gmaps_negative_aspect_audit.csv`
- `gmaps_negative_aspect_theme_mapping.md`
- `gmaps_negative_signal_lexicon.csv`
- `gmaps_negative_signal_lexicon.md`

## Hasil Utama

- negative reviews (`rating <= 3`): `195`
- negative clauses detected: `147`
- negative clauses matched to theme: `55`
- negative clauses unmatched: `92`
- negative clause x theme mapping rows: `76`

## Tema yang Paling Sering Muncul pada Negative Aspect

- `culinary_resto`: `40`
- `museum_education`: `11`
- `plants_garden`: `9`
- `destination_tourism`: `9`
- `aromatic_products`: `3`
- `glamping_stay`: `3`
- `event_campaign`: `1`
- `wellness_experience`: `0`

## Catatan Penting

- Hasil ini lebih tepat untuk membaca keluhan daripada tabel `gmaps_negative_review_theme_mapping.csv`, karena tabel lama masih membaca seluruh review rendah.
- Contoh review campuran yang sebelumnya ikut terbaca sebagai `museum_education` atau `destination_tourism` kini bisa dipersempit ke clause negatif yang benar-benar relevan, misalnya `culinary_resto`.
- `gmaps_negative_aspect_theme_mapping.csv` sekarang juga menyimpan `negative_strength` dan `negative_signal_groups` agar severity keluhan bisa dibaca langsung dari level clause.
