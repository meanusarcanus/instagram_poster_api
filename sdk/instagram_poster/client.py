"""
Official Python SDK Client for Instagram Automated Carousel & Post Publisher MicroSaaS API
"""

import requests
from typing import Optional, Dict, Any

class InstagramPosterClient:
    """
    Python SDK Client for Instagram Poster API.
    """
    def __init__(self, api_key: str, base_url: str = "https://microsaas-agent-api.vercel.app"):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.headers = {
            "X-RapidAPI-Key": self.api_key,
            "Content-Type": "application/json"
        }

    def generate_slides(self, product_url: Optional[str] = None, product_name: Optional[str] = None, theme: str = "dark_cyan", brand_name: str = "@TechGearDaily", amazon_affiliate_tag: str = "techspecdiges-20") -> dict:
        """
        Generate 1080x1350 visual carousel slides and AI caption.
        """
        url = f"{self.base_url}/api/v1/generate-slides"
        payload = {
            "product_url": product_url,
            "product_name": product_name,
            "theme": theme,
            "brand_name": brand_name,
            "amazon_affiliate_tag": amazon_affiliate_tag
        }
        response = requests.post(url, json=payload, headers=self.headers, timeout=30)
        response.raise_for_status()
        return response.json()

    def publish_post(self, product_url: Optional[str] = None, theme: str = "dark_cyan", instagram_credentials: Optional[dict] = None, auto_publish: bool = False) -> dict:
        """
        Generate slides, AI copy, and publish/stage post on Instagram.
        """
        url = f"{self.base_url}/api/v1/publish"
        payload = {
            "product_url": product_url,
            "theme": theme,
            "instagram_credentials": instagram_credentials,
            "auto_publish": auto_publish
        }
        response = requests.post(url, json=payload, headers=self.headers, timeout=45)
        response.raise_for_status()
        return response.json()
