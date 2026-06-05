# Summary Tahap 15: Instagram Negative Aspect Mapping

Dokumen ini merangkum deteksi dan mapping negative aspect pada Instagram comments.

## Tujuan Tahap Ini

- Mengidentifikasi comments yang benar-benar mengandung keluhan atau sinyal negatif.
- Memetakan hanya clause atau comment negatif ke tema, bukan seluruh comments.
- Menyediakan baseline negative comment analysis yang lebih konservatif daripada Google Maps karena comments lebih pendek dan lebih noisy.

## Output

Disimpan di:
- `data/final/theme_mapping/instagram_comments/`

File yang tersedia:
- `instagram_negative_signal_lexicon.csv`
- `instagram_negative_signal_lexicon.md`
- `instagram_negative_aspect_theme_mapping.csv`
- `instagram_negative_aspects_by_theme.csv`
- `instagram_negative_aspect_audit.csv`
- `instagram_negative_aspect_theme_mapping.md`

## Hasil Utama

- negative comments detected: `19`
- negative clauses detected: `20`
- negative clauses matched to theme: `6`
- negative clauses unmatched: `14`
- negative clause x theme mapping rows: `6`

## Tema Keluhan yang Terdeteksi

- `aromatic_products`: `5`
- `culinary_resto`: `1`
- tema lain: `0`

## Catatan Penting

- Hasil ini sengaja dibuat konservatif agar tidak mudah false positive dari bahasa komentar yang sangat pendek, slang, atau konteks bercanda.
- Lexicon comments dibuat terpisah dari Google Maps dan sudah dipersempit dengan menghapus sinyal yang terlalu umum seperti `lama`, `parah`, dan pola negatif yang terlalu kontekstual.
