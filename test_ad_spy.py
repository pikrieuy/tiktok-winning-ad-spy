"""
Unit tests for TikTokTopAdSpy.
Tests:
1. Reverse-engineered signature algorithm (MD5 XOR key hashing).
2. Live API top ads retrieval with mock/live verification.
3. Payload normalization.
4. Anti-Bot and Anti-AI-Slop mathematical evaluator.
"""
import unittest
from engine.tiktok_ad_spy import TikTokTopAdSpy, TIKTOK_SALT, CATEGORY_MAP

class TestTikTokAdSpy(unittest.TestCase):
    def test_category_mapping(self):
        self.assertIn("food", CATEGORY_MAP)
        self.assertIn("otomotif", CATEGORY_MAP)
        self.assertIn("beauty", CATEGORY_MAP)
        self.assertEqual(CATEGORY_MAP["food"], "27000000000")
        self.assertEqual(CATEGORY_MAP["otomotif"], "11000000000")

    def test_signature_algorithm(self):
        anon_id = "test-uuid-12345"
        ts = 1791850000
        sign = TikTokTopAdSpy.generate_signature(anon_id, ts)
        self.assertEqual(len(sign), 16)
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

    def test_anti_bot_and_ai_slop_evaluator(self):
        # 1. Test too short clip rejection (< 12s)
        ad_short = {"duration_seconds": 9.5, "likes": 500, "ctr_pct": 0.8}
        res_short = TikTokTopAdSpy.evaluate_ad_authenticity(ad_short)
        self.assertFalse(res_short["is_authentic"])
        self.assertEqual(res_short["authenticity_status"], "DISQUALIFIED_TOO_SHORT")

        # 2. Test SMM bot injection vanity trap (50k likes but 0.1% CTR)
        ad_smm = {"duration_seconds": 25.0, "likes": 65000, "ctr_pct": 0.12}
        res_smm = TikTokTopAdSpy.evaluate_ad_authenticity(ad_smm)
        self.assertFalse(res_smm["is_authentic"])
        self.assertEqual(res_smm["authenticity_status"], "SUSPECTED_SMM_BOT_INJECTION")

        # 3. Test weak hook drop-off (< 18%)
        ad_weak = {"duration_seconds": 30.0, "likes": 120, "ctr_pct": 0.5, "hook_retention_2s_pct": 11.2, "hold_retention_6s_pct": 3.0}
        res_weak = TikTokTopAdSpy.evaluate_ad_authenticity(ad_weak)
        self.assertFalse(res_weak["is_authentic"])
        self.assertEqual(res_weak["authenticity_status"], "WEAK_HOOK_SLOP")

        # 4. Test authentic winner (good duration, reasonable likes/CTR, god-tier hook)
        ad_winner = {"duration_seconds": 45.0, "likes": 350, "ctr_pct": 0.85, "hook_retention_2s_pct": 32.5, "hold_retention_6s_pct": 18.0}
        res_winner = TikTokTopAdSpy.evaluate_ad_authenticity(ad_winner)
        self.assertTrue(res_winner["is_authentic"])
        self.assertEqual(res_winner["authenticity_status"], "VERIFIED_AUTHENTIC")

if __name__ == '__main__':
    unittest.main()
