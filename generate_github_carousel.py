#!/usr/bin/env python3
"""
Standalone runner script for GitHub Actions interactive carousel generation
"""

import sys
import os
import base64
from pathlib import Path

# Add api directory to sys.path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir / "api"))

from index import generate_slides, GenerateSlidesRequest

def main():
    product_url = os.getenv("INPUT_PRODUCT_URL", "").strip() or "https://www.amazon.com/dp/B0CX23F8H8"
    image_url = os.getenv("INPUT_IMAGE_URL", "").strip()
    theme = os.getenv("INPUT_THEME", "").strip() or "dark_cyan"
    brand_name = os.getenv("INPUT_BRAND_NAME", "").strip() or "@TechGearDaily"
    amazon_tag = os.getenv("INPUT_AMAZON_TAG", "").strip() or "techspecdiges-20"

    print("=" * 60)
    print(" 🚀 INSTAGRAM CAROUSEL GENERATOR (GITHUB ACTIONS RUNNER)")
    print("=" * 60)
    print(f"Product URL : {product_url}")
    print(f"Image URL   : {image_url or '(Auto-Search Engine Active)'}")
    print(f"Theme       : {theme}")
    print(f"Brand Name  : {brand_name}")
    print(f"Amazon Tag  : {amazon_tag}")
    print("=" * 60 + "\n")

    req = GenerateSlidesRequest(
        product_url=product_url,
        image_url=image_url or None,
        theme=theme,
        brand_name=brand_name,
        amazon_affiliate_tag=amazon_tag
    )

    res = generate_slides(req)

    os.makedirs("generated_slides", exist_ok=True)

    print("\n" + "=" * 60)
    print(" 📝 GENERATED INSTAGRAM CAPTION:")
    print("=" * 60)
    print(res.instagram_caption)
    print("=" * 60 + "\n")

    for slide in res.slides:
        b64_data = slide.image_base64.split("base64,")[-1]
        file_path = f"generated_slides/slide_{slide.slide_number}.png"
        with open(file_path, "wb") as f:
            f.write(base64.b64decode(b64_data))
        print(f"✓ Saved 1080x1350 Slide #{slide.slide_number} -> {file_path}")

    print("\n🎉 All 5 Carousel Slides Saved to 'generated_slides/' folder!")

if __name__ == "__main__":
    main()
