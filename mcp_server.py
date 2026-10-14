#!/usr/bin/env python3
"""
TikTok Winning Ads & Creative Intelligence — Model Context Protocol (MCP) Server.
Allows AI Assistants (Claude Desktop, Cursor, Claude Code, ChatGPT) to dynamically
query real-time high-converting ads and hook analytics in Indonesia & SEA.
"""
import sys
import os
from typing import Optional, List, Dict, Any

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp.server.fastmcp import FastMCP
from engine.tiktok_ad_spy import TikTokTopAdSpy, OBJECTIVE_PRODUCT_SALES, CATEGORY_MAP

# Inisialisasi MCP Server
mcp = FastMCP(
    "TikTok-Winning-Ads-Intelligence",
    instructions="Live market intelligence and hook retention analytics for top-converting TikTok e-commerce ads in Indonesia and Southeast Asia."
)

@mcp.tool()
def get_winning_ads(
    category: str = "all",
    country: str = "ID",
    limit: int = 5,
    sort_by: str = "cvr",
    filter_authentic: bool = True
) -> str:
    """
    Pindai video-video iklan TikTok paling menghasilkan (Winning Ads) dengan konversi tinggi.
    
    Parameters:
    - category: Ceruk produk ('food', 'otomotif', 'beauty', 'fashion', 'education', 'tech', atau 'all').
    - country: Kode negara ('ID' untuk Indonesia, 'SG', 'MY', 'US').
    - limit: Jumlah iklan yang diambil (1 s.d. 20).
    - sort_by: Metrik urutan ('cvr' untuk tingkat pembelian, 'like' untuk viralitas, 'ctr' untuk rasio klik).
    - filter_authentic: Jika True, otomatis membuang video AI pendek (<12s) dan bot vanity likes palsu.
    """
    spy = TikTokTopAdSpy()
    cat_param = None if category.lower() in ["all", "semua", ""] else category.lower()
    
    ads = spy.fetch_top_ads(
        country_code=country.upper(),
        period=30,
        objective=OBJECTIVE_PRODUCT_SALES,
        limit=limit,
        order_by=sort_by.lower(),
        category=cat_param,
        enrich_retention=True,
        filter_authentic_only=filter_authentic
    )

    if not ads:
        return f"Tidak ditemukan iklan winning untuk kategori '{category}' di negara '{country}'."

    report_lines = [
        f"### 🔥 Top {len(ads)} TikTok Winning Ads ({country.upper()}) — Kategori: {category.upper()}",
        f"*Disaring otomatis dengan filter anti-bot dan kurva retensi manusia asli.*\n"
    ]

    for idx, ad in enumerate(ads, 1):
        grade = ad.get("hook_grade", "N/A")
        h2 = ad.get("hook_retention_2s_pct")
        h6 = ad.get("hold_retention_6s_pct")
        title = ad.get("title", "")
        dur = ad.get("duration_seconds", 0)
        likes = ad.get("likes", 0)
        ctr = ad.get("ctr_pct", 0)
        vurl = ad.get("video_url_mp4", "")
        
        report_lines.append(f"**{idx}. [{grade}] {title}**")
        report_lines.append(f"- **Metrik Performa:** CTR: `{ctr}%` | Likes: `{likes:,}` | Durasi: `{dur:.1f}s`")
        if h2 is not None:
            report_lines.append(f"- **Daya Pikat Hook:** Detik ke-2: `{h2}%` bertahan | Detik ke-6: `{h6}%` menyimak")
        if vurl:
            report_lines.append(f"- **Link Video MP4 (720p Clean):** [Tonton / Unduh]({vurl})")
        report_lines.append("")

    return "\n".join(report_lines)

@mcp.tool()
def search_pc_laptop_gaming_ads(limit: int = 5) -> str:
    """
    Pindai khusus iklan-iklan PC, Laptop, dan Aksesoris Gaming paling laris di Indonesia.
    Mengambil data dari industri Komputer & Komponen Teknologi dengan hook retensi terbaik.
    """
    spy = TikTokTopAdSpy()
    # Query Computers Components (15102000000)
    ads = spy.fetch_top_ads(
        country_code="ID",
        period=180,
        objective=OBJECTIVE_PRODUCT_SALES,
        limit=20,
        order_by="cvr",
        category="tech",
        enrich_retention=True,
        filter_authentic_only=False
    )
    
    # Filter khusus Laptop/PC/Gaming
    gaming_ads = []
    keywords = ["laptop", "pc", "gaming", "game", "komputer", "asus", "lenovo", "acer", "rog", "tuf", "intel", "ryzen", "rtx"]
    for a in ads:
        title_lower = a.get("title", "").lower()
        if any(k in title_lower for k in keywords):
            gaming_ads.append(a)
            if len(gaming_ads) >= limit:
                break
                
    if not gaming_ads:
        return "Tidak ditemukan iklan spesifik PC/Laptop Gaming di bursa TikTok saat ini."

    report_lines = [
        f"### 🎮 Rekomendasi Iklan PC & Laptop Gaming Terlaris di Indonesia (Top {len(gaming_ads)})",
        "*Dianalisis dari kampanye brand dan perakit PC lokal dengan konversi penjualan riil.*\n"
    ]

    for idx, ad in enumerate(gaming_ads, 1):
        grade = ad.get("hook_grade", "⚪ STANDARD")
        h2 = ad.get("hook_retention_2s_pct")
        h6 = ad.get("hold_retention_6s_pct")
        report_lines.append(f"**{idx}. {ad.get('title')}**")
        report_lines.append(f"- **Performa:** CTR: `{ad.get('ctr_pct')}%` | Likes: `{ad.get('likes'):,}` | Durasi: `{ad.get('duration_seconds'):.1f}s`")
        if h2 is not None:
            report_lines.append(f"- **Hook Score:** `{grade}` (2s: `{h2}%`, 6s: `{h6}%`)")
        if ad.get("video_url_mp4"):
            report_lines.append(f"- **Video MP4:** [Buka Tautan Video]({ad.get('video_url_mp4')})")
        report_lines.append("")

    return "\n".join(report_lines)

@mcp.tool()
def get_ad_retention_deepdive(ad_id: str, country: str = "ID") -> str:
    """
    Analisis mendalam kurva penonton detik-demi-detik untuk satu video iklan tertentu.
    
    Parameters:
    - ad_id: ID iklan TikTok (misal: '7684118233361186824').
    - country: Kode negara ('ID').
    """
    spy = TikTokTopAdSpy()
    detail = spy.fetch_ad_detail(ad_id, country_code=country)
    curve = spy.fetch_retention_curve(ad_id)

    if not detail:
        return f"Gagal mengambil detail untuk Iklan ID '{ad_id}'."

    lines = [
        f"### 🔬 Deepdive Analitik Iklan: [{ad_id}]",
        f"**Judul:** {detail.get('ad_title')}",
        f"**Brand:** {detail.get('brand_name') or '(Toko Direct Seller / Tanpa Brand)'}",
        f"**Objektif:** `{detail.get('objective_key')}`",
        f"**Interaksi:** Likes: `{detail.get('like', 0):,}` | Komen: `{detail.get('comment', 0):,}` | Share: `{detail.get('share', 0):,}`",
        f"**CTR Benchmark:** `{detail.get('ctr', 0):.2f}%`",
        ""
    ]

    if curve.get("hook_grade") != "N/A":
        lines.append(f"#### 📈 Kurva Ketahanan Penonton:")
        lines.append(f"- **Predikat Hook:** `{curve.get('hook_grade')}`")
        lines.append(f"- **Detik ke-2 (Hook Retention):** `{curve.get('hook_retention_2s_pct')}%` penonton bertahan")
        lines.append(f"- **Detik ke-6 (Hold Rate):** `{curve.get('hold_retention_6s_pct')}%` penonton lanjut menyimak")
        lines.append(f"- **Total Titik Data Analisis:** `{curve.get('retention_curve_points')}` detik")
        lines.append("")
        lines.append("> **Wawasan Copywriting:** Jika retensi detik ke-2 >= 30%, kalimat pembuka video ini sangat efektif menahan jempol penonton dan direkomendasikan untuk ditiru.")

    return "\n".join(lines)

if __name__ == "__main__":
    # Jalankan server dalam mode standar stdio (kompatibel penuh dengan Claude Desktop / Cursor / Hermes)
    mcp.run(transport="stdio")
