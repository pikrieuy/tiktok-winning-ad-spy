"""
TikTok Top Ads & Creative Intelligence Harvester (v2.0 Maximized).
Reverse-engineered from TikTok Creative Center Web App.
Features:
- Algorithmic signature generation (MD5 XOR key hashing).
- Session-persistent anonymous ID (prevents 40103 unauthenticated rate limits).
- Hook Retention Analytics (Second-by-second audience drop-off curve).
- Automatic Hook Classification (God-Tier, Strong, Standard).
- Direct clean 720p MP4 download extraction.
"""
import time
import hashlib
import uuid
import logging
from typing import Dict, Any, List, Optional
from curl_cffi import requests

TIKTOK_SALT = "A7B&9z#1G6$2K@8M!3"
API_BASE_URL = "https://ads.tiktok.com/creative_radar_api/v1"

# Objectives mapping:
OBJECTIVE_PRODUCT_SALES = 15
OBJECTIVE_CONVERSIONS = 3
OBJECTIVE_LEADS = 8

class TikTokTopAdSpy:
    def __init__(self, profile: str = "chrome124", timeout: int = 15):
        self.profile = profile
        self.timeout = timeout
        self.anon_id = str(uuid.uuid4())
        self.session = requests.Session(impersonate=self.profile)

    @staticmethod
    def generate_signature(anon_id: str, timestamp: int) -> str:
        """
        Calculates the internal 'user-sign' header required by TikTok Creative Radar API.
        Algorithm:
        1. raw = f"{SALT}-{anon_id}-{timestamp}"
        2. md5_hex = MD5(raw) (32 hex characters)
        3. split into two 16-character halves: ec = md5[0:16], ed = md5[16:32]
        4. user_sign = XOR each hex nibble of ec with ed
        """
        raw = f"{TIKTOK_SALT}-{anon_id}-{timestamp}"
        md5_hex = hashlib.md5(raw.encode("utf-8")).hexdigest()
        ec = md5_hex[0:16]
        ed = md5_hex[16:32]
        user_sign = "".join(hex(int(ec[i], 16) ^ int(ed[i], 16))[2:] for i in range(16))
        return user_sign

    def _get_auth_headers(self) -> Dict[str, str]:
        ts = int(time.time())
        user_sign = self.generate_signature(self.anon_id, ts)

        return {
            "anonymous-user-id": self.anon_id,
            "timestamp": str(ts),
            "user-sign": user_sign,
            "lang": "en",
            "Referer": "https://ads.tiktok.com/business/creativecenter/inspiration/topads/pc/en",
            "Origin": "https://ads.tiktok.com",
            "Accept": "application/json, text/plain, */*"
        }

    def fetch_top_ads(
        self,
        country_code: str = "ID",
        period: int = 30,
        objective: int = OBJECTIVE_PRODUCT_SALES,
        page: int = 1,
        limit: int = 20,
        order_by: str = "like",
        enrich_retention: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Fetches top-performing ads meeting specified criteria.
        Optional enrich_retention fetches second-by-second keyframe curves.
        """
        url = f"{API_BASE_URL}/top_ads/v2/list"
        headers = self._get_auth_headers()
        params: Dict[str, Any] = {
            "page": page,
            "limit": limit,
            "period": period,
            "country_code": country_code,
            "objective": objective,
            "order_by": order_by
        }

        try:
            resp = self.session.get(
                url,
                params=params,
                headers=headers,
                timeout=self.timeout
            )
            if resp.status_code == 200:
                data = resp.json()
                if data.get("code") == 0:
                    materials = data.get("data", {}).get("materials", [])
                    cleaned = self._normalize_ads(materials)
                    if enrich_retention:
                        for ad in cleaned:
                            curve = self.fetch_retention_curve(ad["ad_id"])
                            ad.update(curve)
                    return cleaned
                else:
                    logging.warning(f"[TIKTOK AD SPY API ERROR] Code {data.get('code')}: {data.get('msg')}")
        except Exception as e:
            logging.error(f"[TIKTOK AD SPY FETCH EXCEPTION] {e}")

        return []

    def fetch_retention_curve(self, material_id: str) -> Dict[str, Any]:
        """
        Extracts second-by-second viewer retention curve for an ad.
        Calculates:
        - hook_retention_2s: % of viewers kept after the 2-second hook.
        - hold_retention_6s: % of viewers kept through 6 seconds.
        - hook_grade: Qualitative score (GOD_TIER, STRONG, STANDARD).
        """
        url = f"{API_BASE_URL}/top_ads/keyframe"
        headers = self._get_auth_headers()
        params = {"material_id": str(material_id)}

        try:
            resp = self.session.get(url, params=params, headers=headers, timeout=self.timeout)
            if resp.status_code == 200:
                data = resp.json()
                if data.get("code") == 0:
                    analysis = data.get("data", {}).get("analysis", [])
                    if analysis:
                        pts = len(analysis)
                        sec2_val = analysis[min(2, pts - 1)].get("value", 0.0) * 100.0
                        sec6_val = analysis[min(6, pts - 1)].get("value", 0.0) * 100.0

                        if sec2_val >= 30.0:
                            grade = "🔥 GOD_TIER"
                        elif sec2_val >= 20.0:
                            grade = "⚡ STRONG"
                        else:
                            grade = "⚪ STANDARD"

                        return {
                            "hook_retention_2s_pct": round(sec2_val, 1),
                            "hold_retention_6s_pct": round(sec6_val, 1),
                            "hook_grade": grade,
                            "retention_curve_points": len(analysis)
                        }
        except Exception as e:
            logging.debug(f"[KEYFRAME FETCH ERROR] {e}")

        return {
            "hook_retention_2s_pct": None,
            "hold_retention_6s_pct": None,
            "hook_grade": "N/A",
            "retention_curve_points": 0
        }

    def fetch_ad_detail(self, material_id: str, country_code: str = "ID") -> Optional[Dict[str, Any]]:
        """
        Fetches enriched details for a specific winning ad (performance breakdown, metrics).
        """
        url = f"{API_BASE_URL}/top_ads/v2/detail"
        headers = self._get_auth_headers()
        params = {
            "material_id": str(material_id),
            "country_code": country_code
        }
        try:
            resp = self.session.get(url, params=params, headers=headers, timeout=self.timeout)
            if resp.status_code == 200:
                data = resp.json()
                if data.get("code") == 0:
                    return data.get("data")
        except Exception as e:
            logging.error(f"[TIKTOK AD DETAIL ERROR] {e}")

        return None

    def _normalize_ads(self, raw_materials: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Cleans and standardizes raw ad payloads for intelligence analysis."""
        cleaned = []
        for m in raw_materials:
            vinfo = m.get("video_info", {})
            v_urls = vinfo.get("video_url", {})
            best_video_url = v_urls.get("720p") or v_urls.get("540p") or (list(v_urls.values())[0] if v_urls else None)

            cleaned.append({
                "ad_id": m.get("id"),
                "title": m.get("ad_title", "").strip(),
                "brand_name": m.get("brand_name", "").strip(),
                "ctr_pct": float(m.get("ctr", 0.0)),
                "likes": int(m.get("like", 0)),
                "duration_seconds": float(vinfo.get("duration", 0.0)),
                "cover_image_url": vinfo.get("cover"),
                "video_url_mp4": best_video_url,
                "objective": m.get("objective_key"),
                "industry_key": m.get("industry_key"),
                "is_search_ad": m.get("is_search", False)
            })
        return cleaned
