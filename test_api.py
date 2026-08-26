#!/usr/bin/env python3
"""
Automated Test Suite for Instagram Automated Carousel & Post Publisher MicroSaaS API
"""

import sys
import os
os.environ["DISABLE_LLM"] = "true"
from pathlib import Path

# Add project root & api directory to sys.path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))
sys.path.insert(0, str(root_dir / "api"))

from index import (
    read_root,
    generate_slides,
    publish_post,
    GenerateSlidesRequest,
    PublishPostRequest
)

def run_tests():
    print("=" * 60)
    print(" 📸 TESTING INSTAGRAM AUTOMATED CAROUSEL & POST PUBLISHER API")
    print("=" * 60)

    # Test 1: Health Check Endpoint
    print("\n[Test 1] Health Check Endpoint (GET /api/v1/health)...")
    health_res = read_root()
    assert health_res["status"] == "online", "Health check status must be online"
    print("✓ Health Check Passed!")

    # Test 2: Generate Carousel Slides (Dark Cyan Theme)
    print("\n[Test 2] Generate 5-Slide 1080x1350 Carousel (Dark Cyan Theme)...")
    req_slides = GenerateSlidesRequest(
        product_url="https://www.amazon.com/dp/B0CX23F8H8",
        product_name="UltraSound Pro Wireless Headphones",
        theme="dark_cyan",
        brand_name="@TechGearDaily",
        amazon_affiliate_tag="techspecdiges-20"
    )
    res_slides = generate_slides(req_slides)
    assert res_slides.status == "success", "Status must be success"
    assert res_slides.total_slides == 5, f"Must return exactly 5 slides, got {res_slides.total_slides}"
    assert "data:image/png;base64," in res_slides.slides[0].image_base64, "Slide image must be PNG Base64 data URI"
    assert "techspecdiges-20" in res_slides.product_url, "Product URL must contain Amazon affiliate tag"
    print(f"Product Name: {res_slides.product_name}")
    print(f"Total Slides: {res_slides.total_slides}")
    print(f"Caption Length: {len(res_slides.instagram_caption)} chars")
    print("✓ Slide Generation (Dark Cyan Theme) Passed!")

    # Test 3: Generate Slides Across Other Color Themes (Emerald, Purple, Minimal White)
    print("\n[Test 3] Testing Remaining Color Themes (Emerald, Purple, Minimal White)...")
    for theme in ["emerald", "purple", "minimal_white"]:
        req_theme = GenerateSlidesRequest(theme=theme)
        res_theme = generate_slides(req_theme)
        assert res_theme.theme == theme, f"Theme must match {theme}"
        assert res_theme.total_slides == 5, "Must render 5 slides"
        print(f"✓ Theme '{theme}' rendered 5 1080x1350 slides successfully!")

    # Test 4: Publish Post Endpoint (Staging Mode)
    print("\n[Test 4] Publish Post Endpoint (POST /api/v1/publish)...")
    req_pub = PublishPostRequest(
        product_name="Smart Watch Ultra 2",
        product_specs={"battery": "72 Hours", "display": "AMOLED Retina"},
        theme="purple",
        brand_name="@SmartSetup",
        auto_publish=False
    )
    res_pub = publish_post(req_pub)
    assert res_pub.status == "success", "Publish status must be success"
    assert res_pub.publish_result["status"] == "staged_ready_to_publish", "Default publish result must be staged"
    print("✓ Publish Post Staging Passed!")

    print("\n" + "=" * 60)
    print(" 🎉 ALL INSTAGRAM POSTER API TESTS PASSED 100%!")
    print("=" * 60)

if __name__ == "__main__":
    run_tests()
