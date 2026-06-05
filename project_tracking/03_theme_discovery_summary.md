# Summary Tahap 3: Theme Discovery Post Atsiri

Dokumen ini merangkum eksplorasi tema secara data-driven dari seluruh caption dan hashtag post Instagram Atsiri.

## Tujuan Tahap Ini

- Menentukan tema brand Atsiri berdasarkan data nyata, bukan asumsi awal.
- Menyusun dasar codebook tema yang nanti akan dipakai ke Google Maps reviews dan Instagram comments.
- Menyediakan bukti yang bisa diaudit melalui CSV pendukung.

## Sumber Data

- Dataset utama: `data/datasets/all/shared/instagram_posts_all.csv`
- Total post yang dibaca: `1463`

## Pendekatan yang Dipakai

1. seluruh caption dan hashtag post Atsiri dikumpulkan
2. dihitung hashtag yang paling sering muncul
3. dihitung kata dan bigram yang sering muncul di caption
4. dari pola tersebut dibentuk kandidat tema
5. setiap post dipetakan ke satu atau lebih kandidat tema
6. hasil mapping dipakai untuk diskusi sebelum codebook final dikunci

## Kandidat Tema yang Muncul

| Tema | Jumlah Post Terdeteksi | Catatan |
|---|---:|---|
| Aromatic Products and Essential Oils | 1015 | Dipertahankan sebagai tema produk/aroma/essential oils. |
| Plants, Garden, and Botanicals | 519 | Dipertahankan karena sangat kuat pada identitas taman dan tanaman Atsiri. |
| Museum, Education, and Workshop | 684 | Dipertahankan sebagai tema edukasi, museum, workshop, dan tur. |
| Wellness and Signature Experience | 1176 | Dipertahankan, tetapi perlu diperketat agar hashtag slogan tidak otomatis melabeli tema. |
| Culinary and Resto | 355 | Dipertahankan sebagai tema kuliner/resto. |
| Glamping and Stay | 232 | Dipertahankan sebagai tema menginap/glamping. |
| Destination and Tourism | 336 | Dipertahankan dengan definisi sempit sebagai framing destinasi/kunjungan. |
| Event, Campaign, and Community | 246 | Dipertahankan sebagai tema sekunder dan perlu keyword yang lebih ketat. |
| Architecture and Landscape | 128 | Tidak dipakai sebagai tema mandiri; diarahkan untuk digabung ke `destination_tourism`. |

## Posisi Sementara Hasil Diskusi

- `aromatic_products` dipertahankan sebagai tema mandiri
- `wellness_experience` dipertahankan sebagai tema mandiri, tetapi harus diperketat
- `aromatic_products` dan `wellness_experience` tidak digabung dulu
- `destination_tourism` tetap dipakai
- `architecture_landscape` tidak dipakai sebagai tema mandiri dan akan digabung ke `destination_tourism`

## File Pendukung

- `data/final/theme_discovery/atsiri_theme_summary_for_dosen.md`
- `data/final/theme_discovery/atsiri_theme_review_summary.csv`
- `data/final/theme_discovery/atsiri_theme_candidates.csv`
- `data/final/theme_discovery/atsiri_post_theme_mapping_full.csv`
- `data/final/theme_discovery/atsiri_theme_period_summary.csv`

## Kesimpulan Tahap Ini

Eksplorasi data-driven sudah menghasilkan daftar kandidat tema yang cukup jelas untuk brand Atsiri. Tahap berikutnya bukan lagi mencari tema dari nol, tetapi mengunci codebook final dan menerapkannya ke Google Maps reviews serta Instagram comments.
