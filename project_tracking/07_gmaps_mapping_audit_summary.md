# Summary Tahap 7: Audit Mapping Google Maps

Dokumen ini merangkum audit untuk menjelaskan perbedaan antara jumlah review yang berhasil dipetakan dan jumlah row mapping review x tema.

## Tujuan Tahap Ini

- Menjelaskan kenapa `matched reviews` dan `mapping rows` tidak sama.
- Menyediakan angka audit yang mudah dibawa ke diskusi dengan dosen.
- Menyediakan visual sederhana untuk membaca funnel review dan kepadatan tema.

## Output Audit

Disimpan di:
- `data/final/theme_mapping/google_maps/`

File yang tersedia:
- `gmaps_mapping_audit.csv`
- `gmaps_mapping_audit.md`
- `figures/fig_05_gmaps_review_audit_funnel.svg`
- `figures/fig_06_gmaps_mapping_density.svg`

## Hasil Audit

- raw reviews all: `7878`
- clean reviews: `3937`
- matched reviews: `2557`
- unmatched reviews: `1380`
- mapping rows: `5438`
- multi-theme reviews: `1505`
- max themes per review: `7`
- average themes per matched review: `2.13`

## Interpretasi

- `matched reviews` adalah jumlah review unik yang terkena minimal satu tema.
- `mapping rows` adalah jumlah total pasangan review x tema.
- Karena satu review bisa masuk lebih dari satu tema, maka `mapping rows` memang wajar lebih besar daripada `matched reviews`.

## Fungsi Tahap Ini

Tahap audit ini membantu memastikan bahwa hasil mapping Google Maps bisa dijelaskan dengan jernih sebelum lanjut ke Instagram comments.
