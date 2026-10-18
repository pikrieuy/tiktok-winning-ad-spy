# 🎯 Winning Ad & Creative Intelligence Spy Engine

> **Reverse-Engineered TikTok Creative Center Top Ads & Hook Analytics.**
> Membedah iklan dengan konversi tertinggi (*Winning Ads*) di Indonesia & Asia Tenggara secara real-time.
> Menghitung **Hook Retention Rate (Detik ke-2 & ke-6)** secara matematis dan mengunduh video MP4 720p bersih tanpa browser headless (RAM footprint: ~15MB).

Tersedia dalam 3 mode penggunaan:
1. **CLI Standalone**: Pemindaian cepat, analitik kurva retensi penonton, dan download otomatis video.
2. **FastMCP Server**: Menyediakan antarmuka Model Context Protocol (MCP) untuk AI Agent seperti Claude Desktop / Hermes.
3. **Apify Cloud Actor**: Siap dijalankan terjadwal di cloud melalui platform Apify.

---

## 🚀 Fitur Utama
1. **Analitik Hook Retensi Penonton:**  
   Mengekstrak kurva drop-off penonton detik-demi-detik dan menghitung **Hook Score**:
   - `🔥 GOD_TIER`: Retensi detik ke-2 $\ge 30\%$ (Hook sangat memikat).
   - `⚡ STRONG`: Retensi detik ke-2 $20\% - 30\%$.
   - `⚪ STANDARD`: Retensi detik ke-2 $< 20\%$.
2. **Filter Bot & Anti-AI Slop:**  
   Penyaringan matematis untuk menyingkirkan konten bot vanity dan video generic slop.
3. **Session Persistence (Anti Rate-Limit):**  
   Meniru perilaku browser asli dengan mempertahankan `anonymous-user-id` per session untuk mencegah galat `40103 limited access`.
4. **Downloader Video Otomatis:**  
   Menyediakan opsi `--download-dir` untuk otomatis mengunduh video MP4 720p resolusi penuh tanpa watermark.
5. **Multi-Sorting & Niche Scoping:**  
   Penyortiran berdasarkan `cvr` (Conversion Rate), `like`, atau `ctr`, dengan cakupan kategori industri (food, otomotif, beauty, fashion, education, tech).

---

## 🛠️ Instalasi & Cara Pakai CLI

### 1. Setup Environment
```bash
git clone https://github.com/pikrieuy/tiktok-winning-ad-spy.git
cd tiktok-winning-ad-spy
python -m venv .venv
source .venv/bin/activate  # atau .venv\Scripts\activate di Windows
pip install -r requirements.txt
```

### 2. Pindai Top Ads dengan Analisis Hook
```bash
python cli.py top --country ID --period 30 --limit 5 --retention
```

### 3. Pindai dan Unduh Video MP4 Sekaligus
```bash
python cli.py top --country ID --limit 3 --download-dir ./videos
```

### 4. Lihat Rincian Analitik Sebuah Iklan
```bash
python cli.py detail <MATERIAL_ID>
```

---

## 🤖 Menjalankan FastMCP Server (Untuk AI Agent)

Engine ini dilengkapi dengan server FastMCP (`mcp_server.py`) yang menyediakan tools:
- `get_top_winning_ads`: Mengambil daftar iklan teratas beserta metrik retensi dan CTR/CVR.
- `get_ad_retention_curve`: Mendapatkan detail drop-off penonton detik-demi-detik untuk analisis naskah.

Jalankan server MCP:
```bash
python mcp_server.py
```

Konfigurasi untuk Claude Desktop (`claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "winning-ad-spy": {
      "command": "python",
      "args": ["/path/to/tiktok-winning-ad-spy/mcp_server.py"]
    }
  }
}
```

---

## ☁️ Menjalankan sebagai Apify Actor

Actor siap di-deploy langsung ke Apify:
```bash
apify login
apify push
```
Package sudah mencakup konfigurasi `.actor/actor.json`, `.actor/input_schema.json`, dan `Dockerfile` teroptimasi.

---

## 🧪 Pengujian Unit Test
```bash
python -m unittest test_ad_spy.py test_mcp_server.py
```
Status: **7/7 Lulus 100%**.
