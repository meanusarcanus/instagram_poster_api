"""
AI Technical Copywriter Generator for Instagram Carousel Posts
"""

import os
import json
import requests
from typing import Dict, Any, Optional

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
            res = requests.post(endpoint, headers=headers, json=payload, timeout=8)
            if res.status_code == 200:
                raw_text = res.json()["candidates"][0]["content"]["parts"][0]["text"]
                return json.loads(raw_text)
        except Exception as e:
            print(f"[Warning] Gemini Copywriter Call failed: {e}")

    # High-converting Fallback Copy Engine
    pros = ["Top-tier sound quality with deep bass", "Ultra-comfortable 40-hour battery life", "Fast USB-C Quick Charging"]
    cons = ["Carrying case sold separately", "Slightly bulky for small heads"]

    amazon_cta = "🔗 Link in Bio (Amazon Prime): amzn.to/3xY8z" if "amazon" in url.lower() else f"🔗 Shop at {brand}"
    comment_cta = "💬 Comment 'AMAZON' below to get the direct link in your DMs!" if "amazon" in url.lower() else "💬 Drop a comment below with your thoughts!"

    caption_text = (
        f"🎧 Looking for the ultimate upgrade? Check out our full review for {title}! ⚡\n\n"
        "✨ Key Highlights:\n"
        + "\n".join([f"- {k.replace('_', ' ').title()}: {v}" for k, v in list(specs.items())[:3]]) + "\n\n"
        f"⭐ Verdict: 9.4/10 (Must Buy)\n\n"
        f"{amazon_cta}\n"
        f"{comment_cta}\n\n"
        f"Follow {brand} for daily tech reviews & deals! 🔥\n\n"
        "#TechReview #AmazonDeals #AudioTech #GadgetGear #HeadphonesReview #TechSetup"
    )

    return {
        "slide_1_hook": {
            "title": f"Is {title[:32]}... Worth It?",
            "subtitle": "Full Technical Breakdown & Honest Buyer Verdict"
        },
        "slide_2_specs": {
            "title": "Technical Specs & Features",
            "items": [f"{k.replace('_', ' ').title()}: {v}" for k, v in list(specs.items())[:4]]
        },
        "slide_3_pros_cons": {
            "title": "Pros & Cons Breakdown",
            "pros": pros,
            "cons": cons
        },
        "slide_4_verdict": {
            "title": "Final Verdict & Rating",
            "score": "9.4 / 10",
            "summary": "Outstanding build quality and battery life. Highly recommended for daily listening."
        },
        "slide_5_cta": {
            "title": "Where To Buy",
            "button_text": "Available on Amazon Prime",
            "prompt": f"Link in Bio: {brand}"
        },
        "instagram_caption": caption_text
    }
