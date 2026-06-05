# Summary Tahap 4: Codebook Tema Final V1

Dokumen ini merangkum hasil penguncian codebook tema final v1 yang lahir dari eksplorasi data-driven post Atsiri.

## Tujuan Tahap Ini

- Mengubah kandidat tema menjadi codebook operasional.
- Menetapkan definisi tiap tema secara lebih stabil.
- Menentukan indikator hashtag/keyword dan batas ambiguitas sebelum diterapkan ke sumber lain.

## Tema Final V1

- `aromatic_products`
- `plants_garden`
- `museum_education`
- `wellness_experience`
- `culinary_resto`
- `glamping_stay`
- `destination_tourism`
- `event_campaign`

## Keputusan Penting

- `aromatic_products` dan `wellness_experience` **tidak digabung**
- `wellness_experience` diperketat agar hashtag slogan tidak otomatis memicu tema
- `destination_tourism` tetap dipakai, tetapi dengan definisi sempit
- `event_campaign` tetap dipakai, tetapi keyword umum seperti `program` dan `special` tidak boleh terlalu longgar
- `architecture_landscape` tidak dipakai sebagai tema mandiri dan diarahkan masuk ke `destination_tourism`

## Output Tahap Ini

- `data/final/theme_discovery/atsiri_theme_codebook_v1.csv`
- `data/final/theme_discovery/atsiri_theme_codebook_v1.md`

## Fungsi Codebook Ini

Codebook v1 ini akan menjadi dasar untuk:
- mapping tema ke post Atsiri
- mapping tema ke Google Maps reviews
- mapping tema ke Instagram comments
- agregasi per periode waktu
- analisis reviewer bucket Google Maps
- analisis co-occurrence tema

## Next Step

Langkah berikutnya adalah menerapkan codebook ini ke Google Maps reviews terlebih dahulu, karena sumber itu merupakan customer-side dataset utama.
