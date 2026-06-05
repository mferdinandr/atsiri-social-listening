# Summary Tahap 12: Negative Signal Lexicon Google Maps

Dokumen ini merangkum kamus sinyal negatif yang dipakai untuk mendeteksi clause keluhan pada review Google Maps.

## Tujuan Tahap Ini

- Memindahkan daftar sinyal negatif dari hardcoded script ke file yang bisa diaudit.
- Menambahkan severity label agar clause negatif dapat dibedakan menjadi `hard_negative`, `mixed_negative`, atau `mild_negative`.
- Membuat pipeline negative aspect lebih transparan dan lebih mudah direvisi.

## Output

Disimpan di:
- `data/final/theme_mapping/google_maps/`

File yang tersedia:
- `gmaps_negative_signal_lexicon.csv`
- `gmaps_negative_signal_lexicon.md`

## Struktur Lexicon

Kolom utama:
- `signal_text`
- `language`
- `signal_group`
- `negative_strength`
- `note`

## Aturan Deteksi yang Dipakai

- Review negatif didefinisikan sebagai `rating <= 3`.
- Review dipecah menjadi clause atau kalimat.
- Clause dianggap negatif bila match ke salah satu `signal_text` di lexicon.
- Severity clause ditentukan dari sinyal negatif terkuat yang match.
- Theme mapping diterapkan ke clause negatif, bukan ke seluruh review.

## Refinement Penting

- False positive `destination_tourism` karena nama lokasi seperti `Tawangmangu` pada clause keluhan resto sudah dikurangi.
- Hasil clause-level sekarang lebih fokus pada aspek keluhan yang benar-benar disebut pelanggan.
