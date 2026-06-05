# Summary Tahap 13: Instagram Comments Theme Mapping

Dokumen ini merangkum hasil mapping codebook tema Atsiri v1 ke Instagram comments clean.

## Tujuan Tahap Ini

- Menerapkan codebook tema yang sama ke sumber customer-side kedua setelah Google Maps.
- Mengetahui tema apa yang paling sering muncul dalam komentar Instagram.
- Menyediakan tabel mentah, agregasi, dan audit yang setara dengan paket Google Maps.

## Output

Disimpan di:
- `data/final/theme_mapping/instagram_comments/`

File yang tersedia:
- `instagram_comment_theme_mapping.csv`
- `instagram_comment_theme_overall_summary.csv`
- `instagram_comment_theme_period_summary.csv`
- `instagram_comment_mapping_audit.csv`
- `instagram_comment_mapping_audit.md`
- `summary.md`

## Hasil Utama

- clean comments: `3585`
- matched comments: `563`
- unmatched comments: `3022`
- mapping rows: `668`
- multi-theme comments: `83`
- max themes per comment: `5`
- average themes per matched comment: `1.19`

## Tema yang Paling Sering Muncul

- `aromatic_products`: `214`
- `glamping_stay`: `104`
- `destination_tourism`: `101`
- `museum_education`: `93`
- `plants_garden`: `60`
- `wellness_experience`: `43`
- `culinary_resto`: `23`
- `event_campaign`: `17`

## Catatan Penting

- Matching pada comments cenderung lebih pendek dan lebih jarang multi-tema dibanding review Google Maps.
- Rule `destination_tourism` sudah diperketat agar frasa produk seperti `travel size` tidak salah terbaca sebagai tema destinasi.
