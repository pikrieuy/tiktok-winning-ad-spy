"""
TikTok Winning Ads & Creative Intelligence Spy — Apify Actor Entrypoint.
Extracts top-performing e-commerce ads meeting high conversion / sales criteria,
with optional second-by-second viewer hook retention curve analysis.
"""
import asyncio
import os
import sys
from typing import Dict, Any

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from apify import Actor
from engine.tiktok_ad_spy import TikTokTopAdSpy, OBJECTIVE_PRODUCT_SALES

async def main() -> None:
    async with Actor:
        actor_input: Dict[str, Any] = await Actor.get_input() or {}
        
        country_code = str(actor_input.get("countryCode", "ID")).upper()
        period = int(actor_input.get("period", 30))
        objective = int(actor_input.get("objective", OBJECTIVE_PRODUCT_SALES))
        order_by = str(actor_input.get("sortBy", "cvr")).lower()
        max_results = int(actor_input.get("maxResults", 10))
        enrich_retention = bool(actor_input.get("enrichHookRetention", True))
        filter_authentic = bool(actor_input.get("filterAuthenticOnly", True))

        Actor.log.info(
            f"🚀 Memulai pindaian TikTok Winning Ads | Negara: {country_code} | "
            f"Periode: {period} hari | Sort: {order_by} | Target: {max_results} iklan | "
            f"Filter Anti-Bot/AI: {'AKTIF' if filter_authentic else 'NONAKTIF'}"
        )

        spy = TikTokTopAdSpy()
        all_ads = []
        page = 1
        remaining = max_results

        while remaining > 0:
            batch_size = min(20, remaining)
            Actor.log.info(f"Mengambil halaman {page} (batch {batch_size} item)...")
            batch = spy.fetch_top_ads(
                country_code=country_code,
                period=period,
                objective=objective,
                page=page,
                limit=batch_size,
                order_by=order_by,
                enrich_retention=enrich_retention,
                filter_authentic_only=filter_authentic
            )

            if not batch:
                Actor.log.warning("Tidak ada iklan tambahan yang ditemukan dari API.")
                break

            all_ads.extend(batch)
            remaining -= len(batch)
            page += 1

            if len(batch) < batch_size:
                break

        Actor.log.info(f"✅ Berhasil menyedot {len(all_ads)} winning ads. Menyimpan ke Apify Dataset...")
        if all_ads:
            await Actor.push_data(all_ads)
        
        Actor.log.info("🏁 Eksekusi Actor tuntas 100%. Data siap diunduh dalam format Excel, CSV, atau JSON.")

if __name__ == "__main__":
    asyncio.run(main())
