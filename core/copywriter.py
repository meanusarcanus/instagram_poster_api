"""
AI Technical Copywriter Generator for Instagram Carousel Posts
Generates product-specific Pros & Cons and formatted specs for all e-commerce categories and platforms.
"""

import os
import json
import requests
from typing import Dict, Any, Optional

def generate_product_pros_cons(title: str, specs: Dict[str, Any]) -> tuple:
    """
    Generates product-specific Pros and Cons based on product category.
    """
    t_lower = title.lower()

    if any(w in t_lower for w in ["stand", "holder", "folding", "magnetic", "mount"]):
        pros = [
            "3-In-1 magnetic folding design for phones, tablets & laptops",
            "Ultra-portable & lightweight for travel & desktop setup",
            "Sturdy anti-slip aluminum alloy construction"
        ]
        cons = [
            "Requires magnetic plate / MagSafe case for non-magnetic phones",
            "Optimal for devices under 15-inch screen size"
        ]
    elif any(w in t_lower for w in ["stylus", "pencil", "pen", "ipad", "tablet"]):
        pros = [
            "Palm rejection for natural hand placement",
            "Tilt sensitivity for precise shading & line weight",
            "Fast USB-C charging with long-lasting battery"
        ]
        cons = [
            "Requires double-tap top button to turn on",
            "Compatible only with 2018 and newer iPad models"
        ]
    elif any(w in t_lower for w in ["headphone", "earbud", "audio", "speaker", "sound", "earphone"]):
        pros = [
            "Active Noise Cancellation with deep bass profile",
            "Ergonomic fit for long listening sessions",
            "Multi-device Bluetooth pairing"
        ]
        cons = [
            "Protective case sold separately",
            "Takes ~2 hours for full battery recharge"
        ]
    elif any(w in t_lower for w in ["watch", "band", "tracker", "smartwatch"]):
        pros = [
            "Comprehensive health & workout tracking",
            "Vibrant AMOLED touch display",
            "Water-resistant build for swimming"
        ]
        cons = [
            "Requires companion smartphone app",
            "Battery needs charging every 2-3 days"
        ]
    elif any(w in t_lower for w in ["robot", "companion", "desktop pet"]):
        pros = [
            "Interactive voice & visual AI recognition",
            "Built-in 10W wireless charging pad",
            "Expressive animations & personality"
        ]
        cons = [
            "Requires smartphone dock for full features",
            "English voice support currently"
        ]
    else:
        bullets = [str(v) for v in specs.values() if isinstance(v, str) and len(v) > 10]
        if len(bullets) >= 2:
            pros = [
                bullets[0][:55],
                bullets[1][:55],
                "Premium build quality & high durability"
            ]
        else:
            pros = [
                "Top-tier performance and precise engineering",
                "Compact, modern, and user-friendly design",
                "Instant plug-and-play setup"
            ]
        cons = [
            "Power adapter / accessories sold separately",
            "High demand may limit stock availability"
        ]

    return pros, cons

def generate_carousel_copy(
    product_data: Dict[str, Any],
    brand_name: Optional[str] = None,
    amazon_tag: Optional[str] = None
) -> Dict[str, Any]:
    """
    Generates structured AI copywriting for 5 carousel slides + full Instagram caption for any store.
    """
    api_key = os.getenv("LLM_API_KEY") or os.getenv("GEMINI_API_KEY")
    if os.getenv("DISABLE_LLM") == "true":
        api_key = None

    title = product_data.get("title", "Premium Tech Product")
    specs = product_data.get("specs", {})
    url = product_data.get("product_url", "")
    brand = brand_name or "@TechGearDaily"
    store_info = product_data.get("store_info", {})
    platform = store_info.get("platform", "Online Store")

    pros, cons = generate_product_pros_cons(title, specs)

    if api_key:
        endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.6-flash:generateContent?key={api_key}"
        headers = {"Content-Type": "application/json"}
        prompt = (
            "Generate a high-converting 5-slide Instagram Carousel copy payload and caption for an e-commerce product review. "
            f"Product: '{title}'. Platform: '{platform}'. Specs: {json.dumps(specs)}. Brand: '{brand}'. Product URL: '{url}'. "
            "Return ONLY JSON with keys: "
            "{\"slide_1_hook\": {\"title\": \"string\", \"subtitle\": \"string\"}, "
            "\"slide_2_specs\": {\"title\": \"string\", \"items\": [\"string\"]}, "
            "\"slide_3_pros_cons\": {\"title\": \"string\", \"pros\": [\"string\"], \"cons\": [\"string\"]}, "
            "\"slide_4_verdict\": {\"title\": \"string\", \"score\": \"string\", \"summary\": \"string\"}, "
            "\"slide_5_cta\": {\"title\": \"string\", \"button_text\": \"string\", \"prompt\": \"string\"}, "
            "\"instagram_caption\": \"string\"}"
        )
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"response_mime_type": "application/json"}
        }
        try:
            res = requests.post(endpoint, headers=headers, json=payload, timeout=18)
            if res.status_code == 200:
                raw_text = res.json()["candidates"][0]["content"]["parts"][0]["text"]
                return json.loads(raw_text)
        except Exception as e:
            print(f"[Warning] Gemini Copywriter Call failed: {e}")

    # Format specs items cleanly
    spec_items = []
    for k, v in list(specs.items())[:4]:
        if k == "price":
            spec_items.append(f"Price: {v}")
        elif k.startswith("spec_") or k.startswith("feature_"):
            spec_items.append(str(v))
        else:
            spec_items.append(f"{k.replace('_', ' ').title()}: {v}")

    if "shopee" in platform.lower():
        store_cta = f"🔗 Direct Link in Bio: {brand}"
        hashtags = "#ShopeeFinds #ShopeePH #ShopeeDeals #TechReview #DeskSetup #SmartGadgets"
    elif "lazada" in platform.lower():
        store_cta = f"🔗 Direct Link in Bio: {brand}"
        hashtags = "#LazadaFinds #LazadaPH #LazadaDeals #TechReview #DeskSetup #SmartGadgets"
    elif "amazon" in platform.lower():
        store_cta = "🔗 Link in Bio: amzn.to/3xY8z"
        hashtags = "#AmazonDeals #AmazonPrime #TechReview #GadgetReview #SmartTech"
    else:
        store_cta = f"🔗 Shop Link in Bio: {brand}"
        hashtags = "#ECommerceDeals #TechReview #GadgetReview #SmartTech #ProductivityTools"

    caption_text = (
        f"⚡ Check out our full review for {title}! 📱\n\n"
        "✨ Key Highlights:\n"
        + "\n".join([f"- {item}" for item in spec_items[:3]]) + "\n\n"
        f"⭐ Verdict: 9.4/10 (Must Buy)\n\n"
        f"{store_cta}\n"
        "💬 Comment 'DEAL' below to get the direct link in your DMs!\n\n"
        f"Follow {brand} for daily tech reviews & deals! 🔥\n\n"
        f"{hashtags}"
    )

    return {
        "slide_1_hook": {
            "title": f"Is {title[:32]}... Worth It?",
            "subtitle": f"Full Technical Breakdown & Honest {platform} Verdict"
        },
        "slide_2_specs": {
            "title": "Technical Specs & Features",
            "items": spec_items if spec_items else [f"Price: {store_info.get('default_price', '$19.99')}", "Build: Premium Grade", "Design: Ultra Portable", "Warranty: 1-Year Included"]
        },
        "slide_3_pros_cons": {
            "title": "Pros & Cons Breakdown",
            "pros": pros,
            "cons": cons
        },
        "slide_4_verdict": {
            "title": "Final Verdict & Rating",
            "score": "9.4 / 10",
            "summary": f"Outstanding performance and build quality for {title[:25]}. Highly recommended daily essential."
        },
        "slide_5_cta": {
            "title": "Where To Buy",
            "button_text": store_info.get("button", "Available Online Now"),
            "prompt": f"Link in Bio: {brand}"
        },
        "instagram_caption": caption_text
    }
