"""
Unit tests for TikTok Winning Ads MCP Server.
Verifies tool registration, argument contracts, and mock invocations.
"""
import unittest
from mcp_server import mcp, get_winning_ads, search_pc_laptop_gaming_ads, get_ad_retention_deepdive

class TestMCPServer(unittest.TestCase):
    def test_tools_registered(self):
        tool_names = [t.name for t in mcp._tool_manager.list_tools()]
        self.assertIn("get_winning_ads", tool_names)
        self.assertIn("search_pc_laptop_gaming_ads", tool_names)
        self.assertIn("get_ad_retention_deepdive", tool_names)

    def test_search_pc_laptop_tool_returns_markdown(self):
        result = search_pc_laptop_gaming_ads(limit=1)
        self.assertIsInstance(result, str)
        self.assertIn("PC & Laptop Gaming", result)

    def test_get_winning_ads_tool(self):
        result = get_winning_ads(category="fashion", country="ID", limit=1, filter_authentic=False)
        self.assertIsInstance(result, str)
        self.assertIn("TikTok Winning Ads", result)

if __name__ == '__main__':
    unittest.main()
