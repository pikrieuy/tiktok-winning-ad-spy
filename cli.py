#!/usr/bin/env python3
"""
CLI Tool for Winning Ad & Burn-Rate Spy (Gebrakan 1 - v2.0 Maximized).
Inspect high-converting TikTok winning ads in Indonesia and SEA,
with second-by-second Hook Retention curves and direct video download URLs.
"""
import sys
import os
import argparse
import json
import urllib.request

sys.path.insert(0, "/root/winning-ad-spy")
from engine.tiktok_ad_spy import TikTokTopAdSpy, OBJECTIVE_PRODUCT_SALES, OBJECTIVE_CONVERSIONS, OBJECTIVE_LEADS

def cmd_top_ads(args):
    print(f"\n🔍 Memindai Iklan Paling Menghasilkan di TikTok ({args.country}, Periode: {args.period} Hari)...")
    spy = TikTokTopAdSpy()
    ads = spy.fetch_top_ads(
        country_code=args.country,
        period=args.period,
        objective=args.objective,
        limit=args.limit,
        order_by=args.sort,
        enrich_retention=args.retention
    )

    if not ads:
        print("❌ Tidak ada iklan yang ditemukan atau terjadi kendala jaringan.")
        return

    print("="*80)
    print(f"  🔥 TOP {len(ads)} WINNING ADS INDONESIA ({args.country}) — SORT BY: {args.sort.upper()}")
    print("="*80)

    for idx, ad in enumerate(ads, 1):
        print(f"{idx}. [{ad['ad_id']}] {ad['title'][:70]}...")
        print(f"   • CTR       : {ad['ctr_pct']:.2f}% | Likes: {ad['likes']:,} | Durasi: {ad['duration_seconds']:.1f}s")
        if args.retention and ad.get("hook_grade") != "N/A":
            print(f"   • Hook Score: {ad.get('hook_grade')} (2s: {ad.get('hook_retention_2s_pct')}%, 6s: {ad.get('hold_retention_6s_pct')}%)")
        print(f"   • Video MP4 : {ad['video_url_mp4'][:85]}...")
        print("-" * 80)

    if args.download_dir:
        os.makedirs(args.download_dir, exist_ok=True)
        print(f"\n📥 Mengunduh {len(ads)} video MP4 ke folder '{args.download_dir}'...")
        for ad in ads:
            v_url = ad.get("video_url_mp4")
            if v_url:
                out_path = os.path.join(args.download_dir, f"{ad['ad_id']}.mp4")
                try:
                    urllib.request.urlretrieve(v_url, out_path)
                    print(f"  ✅ Tersimpan: {out_path} ({os.path.getsize(out_path):,} bytes)")
                except Exception as e:
                    print(f"  ❌ Gagal unduh {ad['ad_id']}: {e}")

    if args.export:
        out_file = args.export
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(ads, f, indent=2, ensure_ascii=False)
        print(f"\n💾 Berhasil mengekspor {len(ads)} iklan winning ke: {out_file}\n")

def cmd_detail(args):
    print(f"\n🔎 Mengambil rincian analitik mendalam untuk Iklan ID: {args.id}...")
    spy = TikTokTopAdSpy()
    detail = spy.fetch_ad_detail(args.id, country_code=args.country)
    curve = spy.fetch_retention_curve(args.id)

    if detail:
        print("="*70)
        print("  DETAIL METRIK IKLAN WINNING & HOOK ANALYSIS")
        print("="*70)
        print(f"• Judul         : {detail.get('ad_title')}")
        print(f"• Brand         : {detail.get('brand_name') or '(Unbranded Direct Seller)'}")
        print(f"• Objective     : {detail.get('objective_key')}")
        print(f"• Likes         : {detail.get('like', 0):,}")
        print(f"• Komentar      : {detail.get('comment', 0):,}")
        print(f"• Share         : {detail.get('share', 0):,}")
        print(f"• CTR Score     : {detail.get('ctr', 0):.2f}%")
        if curve.get("hook_grade") != "N/A":
            print(f"• Hook Grade    : {curve.get('hook_grade')}")
            print(f"• Hook (2s)     : {curve.get('hook_retention_2s_pct')}% penonton bertahan")
            print(f"• Hold (6s)     : {curve.get('hold_retention_6s_pct')}% penonton lanjut")
        print("="*70 + "\n")
    else:
        print("❌ Gagal memuat detail iklan.")

def main():
    parser = argparse.ArgumentParser(description="Winning Ad & Burn-Rate Spy CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subcommand: list top ads
    p_top = subparsers.add_parser("top", help="Pindai iklan-iklan winning produk laris")
    p_top.add_argument("--country", default="ID", help="Kode negara (ID, SG, MY, US)")
    p_top.add_argument("--period", type=int, default=30, choices=[7, 30, 180], help="Periode hari (7, 30, 180)")
    p_top.add_argument("--objective", type=int, default=OBJECTIVE_PRODUCT_SALES, choices=[15, 3, 8], help="15=Product Sales, 3=Conversions, 8=Leads")
    p_top.add_argument("--sort", default="cvr", choices=["cvr", "like", "ctr"], help="Urutkan berdasarkan: cvr (konversi), like, ctr")
    p_top.add_argument("--limit", type=int, default=5, help="Jumlah iklan yang diambil (max 50)")
    p_top.add_argument("--retention", action="store_true", help="Bedah kurva retensi hook detik ke-2 & ke-6")
    p_top.add_argument("--download-dir", help="Folder tujuan untuk mengunduh file video MP4 720p")
    p_top.add_argument("--export", help="Path file JSON untuk menyimpan hasil")

    # Subcommand: inspect ad detail
    p_det = subparsers.add_parser("detail", help="Rincian analitik sebuah iklan")
    p_det.add_argument("id", help="Material ID / Ad ID")
    p_det.add_argument("--country", default="ID", help="Kode negara")

    args = parser.parse_args()
    if args.command == "top":
        cmd_top_ads(args)
    elif args.command == "detail":
        cmd_detail(args)

if __name__ == "__main__":
    main()
