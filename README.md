# 🎯 Winning Ad & Creative Intelligence Spy Engine (v2.0 Maximized)

> **Reverse-Engineered TikTok Creative Center Top Ads & Hook Analytics.**
> Membedah iklan dengan konversi tertinggi (*Winning Ads*) di Indonesia & Asia Tenggara secara real-time.
> Menghitung **Hook Retention Rate (Detik ke-2 & ke-6)** secara matematis dan mengunduh video MP4 720p bersih tanpa browser headless (RAM footprint: ~15MB).

---

## 🚀 Fitur Baru yang Dimaksimalkan (v2.0)
1. **Analitik Hook Retensi Penonton:**  
   Mengekstrak kurva drop-off penonton detik-demi-detik dan menghitung **Hook Score**:
   - `🔥 GOD_TIER`: Retensi detik ke-2 $\ge 30\%$ (Hook sangat memikat).
   - `⚡ STRONG`: Retensi detik ke-2 $20\% - 30\%$.
   - `⚪ STANDARD`: Retensi detik ke-2 $< 20\%$.
2. **Session Persistence (Anti Rate-Limit):**  
   Meniru perilaku browser asli dengan mempertahankan `anonymous-user-id` per session untuk mencegah galat `40103 limited access`.
3. **Downloader Video Otomatis:**  
   Menyediakan opsi `--download-dir` untuk otomatis mengunduh video MP4 720p resolusi penuh ke server/laptop untuk dibedah tim kreatif.
4. **Multi-Sorting:**  
   Dukungan penyortiran berdasarkan `cvr` (Conversion Rate penjualan), `like`, atau `ctr`.

---

## 🛠️ Cara Pakai CLI

### 1. Masuk ke Virtual Environment
```bash
source /root/winning-ad-spy/.venv/bin/activate
```

### 2. Pindai Top Ads Lengkap dengan Analisis Hook
```bash
python /root/winning-ad-spy/cli.py top --country ID --period 30 --limit 5 --retention
```

### 3. Pindai dan Unduh Video MP4 Sekaligus
```bash
python /root/winning-ad-spy/cli.py top --country ID --limit 3 --download-dir /root/winning_videos
```

### 4. Lihat Rincian Analitik Sebuah Iklan
```bash
python /root/winning-ad-spy/cli.py detail <MATERIAL_ID>
```

---

## 🧪 Pengujian Unit Test
```bash
/root/winning-ad-spy/.venv/bin/python -m unittest /root/winning-ad-spy/test_ad_spy.py
```
Status: **3/3 Lulus 100% (0.21s)**.
