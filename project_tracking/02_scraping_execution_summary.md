# Summary Tahap 2: Hasil dan Strategi Scraping

Dokumen ini menjelaskan strategi scraping yang sudah dijalankan, hasilnya, dan keputusan metodologis yang diambil selama pengumpulan data.

## Tujuan Tahap Ini

- Mendapatkan data yang cukup dari setiap sumber utama.
- Menentukan strategi scraping yang paling hemat dan paling stabil.
- Membedakan hasil teoretis dari metadata dan hasil real scrape yang benar-benar dimiliki.

## Ringkasan Strategi yang Dijalankan

### Google Maps

Pada awalnya sempat dicoba strategi batch kumulatif, tetapi strategi ini dihentikan karena biaya per batch terus naik akibat pengambilan ulang data yang sama.

Keputusan akhir:
- Google Maps diambil melalui **satu full run**

Hasil utama:
- total review raw: `7878`
- total review clean: `3937`

Catatan metodologis:
- full run menjadi sumber utama final
- batch kumulatif lama tidak dipakai sebagai sumber utama analisis

### Instagram Posts

Instagram posts diambil satu kali sebagai shared dataset.

Hasil utama:
- total post raw: `1463`
- total post clean: `1461`

Catatan metodologis:
- post tidak perlu dibatch ulang
- dataset ini dipakai sebagai sumber utama untuk membaca tema/signal yang dikirim brand

### Instagram Comments

Instagram comments tidak diambil secara acak. Strategi yang dipakai adalah:
- memprioritaskan post dengan `comment_count > 20`
- mengambil comments secara bertahap tanpa overlap post

Hasil utama:
- total comments real scrape: `5351`
- total comments clean: `3585`
- total post prioritas tercakup: `144`

## Catatan Penting Tentang Metadata vs Real Scrape

Pada Instagram comments, ada perbedaan antara:
- jumlah komentar **menurut metadata post**
- jumlah komentar yang **benar-benar berhasil discrape**

Untuk post dengan `comment_count > 20`:
- total komentar teoretis menurut metadata: `7875`
- total komentar yang benar-benar berhasil discrape: `5351`

Artinya:
- `7875` bukan dataset yang dimiliki
- `5351` adalah dataset real yang benar-benar tersedia untuk analisis

## Kesimpulan Tahap Ini

Tahap scraping sudah menghasilkan dataset yang cukup kuat untuk analisis lanjutan:
- Google Maps full run sudah selesai
- Instagram posts sudah selesai
- Instagram comments prioritas sudah selesai

Dengan demikian, fokus proyek bisa bergeser dari pengumpulan data ke pengelompokan tema dan analisis isi.
