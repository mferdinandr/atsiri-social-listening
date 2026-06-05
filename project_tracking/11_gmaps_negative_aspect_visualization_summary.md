# Summary Tahap 11: Visualisasi Negative Aspect Google Maps

Dokumen ini merangkum visualisasi untuk hasil negative aspect mapping Google Maps berbasis clause-level.

## Tujuan Tahap Ini

- Memvisualisasikan tema keluhan yang paling dominan pada review `rating <= 3`.
- Menunjukkan distribusi negative aspect per periode waktu.
- Menyediakan audit visual sederhana untuk jumlah review negatif, clause negatif, dan hasil mapping.

## Output

Disimpan di:
- `data/final/theme_mapping/google_maps/`

File yang tersedia:
- `gmaps_negative_aspect_visuals_summary.md`
- `figures/fig_11_gmaps_negative_aspects_overall.svg`
- `figures/fig_12_gmaps_negative_aspects_by_period.svg`
- `figures/fig_13_gmaps_negative_aspect_audit.svg`

## Fungsi Tiap Figure

- `fig_11_gmaps_negative_aspects_overall.svg`
  Menunjukkan tema negative aspect yang paling dominan secara keseluruhan.
- `fig_12_gmaps_negative_aspects_by_period.svg`
  Menunjukkan distribusi negative aspect per periode waktu.
- `fig_13_gmaps_negative_aspect_audit.svg`
  Menunjukkan audit jumlah review negatif, clause negatif, clause yang match tema, clause yang belum match, dan total mapping row.

## Catatan

- Visual ini dibangun dari mapping clause-level, jadi lebih tepat untuk membaca keluhan daripada tabel review negatif level penuh.
- Hasil ini bisa dipakai sebagai dasar untuk diskusi aspect keluhan sebelum lanjut ke Instagram comments.
