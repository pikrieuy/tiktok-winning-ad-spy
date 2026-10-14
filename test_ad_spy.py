"""
Unit tests for TikTokTopAdSpy.
Tests:
1. Reverse-engineered signature algorithm (MD5 XOR key hashing).
2. Live API top ads retrieval with mock/live verification.
3. Payload normalization.
"""
import unittest
from engine.tiktok_ad_spy import TikTokTopAdSpy, TIKTOK_SALT

class TestTikTokAdSpy(unittest.TestCase):
    def test_signature_algorithm(self):
        # Test that signature produces valid 16-char hex string
        anon_id = "test-uuid-12345"
        ts = 1791850000
        sign = TikTokTopAdSpy.generate_signature(anon_id, ts)
        self.assertEqual(len(sign), 16)
        # Hexadecimal string check
        int(sign, 16)

    def test_normalization(self):
        spy = TikTokTopAdSpy()
        raw = [{
            "id": "123456",
            "ad_title": "  Sample Skincare Video  ",
            "brand_name": "GlowBrand",
            "ctr": 1.25,
            "like": 500,
            "video_info": {
                "duration": 15.5,
                "cover": "https://img.com/cover.jpg",
                "video_url": {"720p": "https://video.com/720.mp4"}
            },
            "objective_key": "campaign_objective_product_sales"
        }]
        cleaned = spy._normalize_ads(raw)
        self.assertEqual(len(cleaned), 1)
        self.assertEqual(cleaned[0]["ad_id"], "123456")
        self.assertEqual(cleaned[0]["title"], "Sample Skincare Video")
        self.assertEqual(cleaned[0]["ctr_pct"], 1.25)
        self.assertEqual(cleaned[0]["likes"], 500)
        self.assertEqual(cleaned[0]["duration_seconds"], 15.5)
        self.assertEqual(cleaned[0]["video_url_mp4"], "https://video.com/720.mp4")

    def test_live_top_ads_fetch(self):
        spy = TikTokTopAdSpy()
        ads = spy.fetch_top_ads(country_code="ID", period=30, limit=3)
        self.assertIsInstance(ads, list)
        if ads:
            ad = ads[0]
            self.assertIn("ad_id", ad)
            self.assertIn("title", ad)
            self.assertIn("ctr_pct", ad)
            self.assertIn("video_url_mp4", ad)

if __name__ == '__main__':
    unittest.main()
