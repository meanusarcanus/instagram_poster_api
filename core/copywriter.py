"""
AI Technical Copywriter Generator for Instagram Carousel Posts
Generates product-specific Pros & Cons and formatted specs for all product categories.
"""

import os
import json
import requests
from typing import Dict, Any, Optional

def generate_product_pros_cons(title: str, specs: Dict[str, Any]) -> tuple:
    """
    Generates product-specific Pros and Cons based on product title and features.
    """
    t_lower = title.lower()

    if any(w in t_lower for w in ["stylus", "pencil", "pen", "ipad", "tablet"]):
        pros = [
            "Palm rejection for natural hand placement",
            "Tilt sensitivity for precise shading & line weight",
            "Fast USB-C charging with long-lasting battery"
        ]
        cons = [
            "Requires double-tap top button to turn on",
            "Compatible only with 2018 and newer iPad models"
        ]
    elif any(w in t_lower for w in ["headphone", "earbud", "audio", "speaker", "sound"]):
        pros = [
            "Active Noise Cancellation with deep bass profile",
            "Ergonomic fit for long listening sessions",
            "Multi-device Bluetooth 5.4 pairing"
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
    else:
        # Generic Product Pros derived from feature bullets
        bullets = [str(v) for v in specs.values() if isinstance(v, str) and len(v) > 10]
        if len(bullets) >= 2:
            pros = [
                bullets[0][:50],
                bullets[1][:50],
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
    Generates structured AI copywriting for 5 carousel slides + full Instagram caption.
    """
    api_key = os.getenv("LLM_API_KEY") or os.getenv("GEMINI_API_KEY")
    if os.getenv("DISABLE_LLM") == "true":
        api_key = None
    title = product_data.get("title", "Premium Tech Product")
    specs = product_data.get("specs", {})
    url = product_data.get("product_url", "")
    brand = brand_name or "@TechGearDaily"

    pros, cons = generate_product_pros_cons(title, specs)

    if api_key:
        endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.6-flash:generateContent?key={api_key}"
        headers = {"Content-Type": "application/json"}
        prompt = (
            "Generate a high-converting 5-slide Instagram Carousel copy payload and caption for an e-commerce product review. "
            f"Product: '{title}'. Specs: {json.dumps(specs)}. Brand: '{brand}'. Product URL: '{url}'. "
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

    amazon_cta = "🔗 Link in Bio (Amazon Prime): amzn.to/3xY8z" if "amazon" in url.lower() else f"🔗 Shop at {brand}"
    comment_cta = "💬 Comment 'AMAZON' below to get the direct link in your DMs!" if "amazon" in url.lower() else "💬 Drop a comment below with your thoughts!"

    caption_text = (
        f"⚡ Check out our full review for {title}! 📱\n\n"
        "✨ Key Highlights:\n"
        + "\n".join([f"- {item}" for item in spec_items[:3]]) + "\n\n"
        f"⭐ Verdict: 9.4/10 (Must Buy)\n\n"
        f"{amazon_cta}\n"
        f"{comment_cta}\n\n"
        f"Follow {brand} for daily tech reviews & deals! 🔥\n\n"
        "#TechReview #AmazonDeals #GadgetReview #TechSetup #SmartTech"
    )

    return {
        "slide_1_hook": {
            "title": f"Is {title[:32]}... Worth It?",
            "subtitle": "Full Technical Breakdown & Honest Buyer Verdict"
        },
        "slide_2_specs": {
            "title": "Technical Specs & Features",
            "items": spec_items if spec_items else ["Price: $17.54", "Build: High Precision", "Battery: Extended Playtime", "Warranty: 1-Year Included"]
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
            "button_text": "Available on Amazon Prime",
            "prompt": f"Link in Bio: {brand}"
        },
        "instagram_caption": caption_text
    }
