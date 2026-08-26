"""
Instagram Graph API Publisher & Webhook Notification Dispatcher
"""

import requests
from typing import Dict, Any, List, Optional

def publish_instagram_carousel(
    slides: List[Dict[str, Any]],
    caption: str,
    instagram_credentials: Optional[Dict[str, str]] = None,
    webhook_url: Optional[str] = None
) -> Dict[str, Any]:
    """
    Publishes or stages an Instagram Carousel post via Instagram Graph API.
    """
    creds = instagram_credentials or {}
    ig_user_id = creds.get("instagram_account_id")
    access_token = creds.get("access_token")

    if ig_user_id and access_token:
        try:
            # 1. Create Media Items Containers for each slide image
            item_ids = []
            for slide in slides:
                # In live Graph API, slides must be public CDN image URLs
                image_url = slide.get("image_url") or "https://raw.githubusercontent.com/meanusarcanus/shopee_scraper_api/master/assets/shopee_logo.jpg"
                container_url = f"https://graph.facebook.com/v19.0/{ig_user_id}/media"
                res = requests.post(container_url, data={
                    "image_url": image_url,
                    "is_carousel_item": "true",
                    "access_token": access_token
                }, timeout=10)
                if res.status_code == 200:
                    item_ids.append(res.json()["id"])

            if item_ids:
                # 2. Create Carousel Container
                carousel_res = requests.post(container_url, data={
                    "caption": caption,
                    "media_type": "CAROUSEL",
                    "children": ",".join(item_ids),
                    "access_token": access_token
                }, timeout=10)

                if carousel_res.status_code == 200:
                    creation_id = carousel_res.json()["id"]

                    # 3. Publish Carousel Container
                    pub_url = f"https://graph.facebook.com/v19.0/{ig_user_id}/media_publish"
                    pub_res = requests.post(pub_url, data={
                        "creation_id": creation_id,
                        "access_token": access_token
                    }, timeout=10)

                    if pub_res.status_code == 200:
                        post_id = pub_res.json()["id"]
                        return {
                            "status": "published_live",
                            "post_id": post_id,
                            "creation_id": creation_id,
                            "permalink": f"https://www.instagram.com/p/{post_id}/"
                        }
        except Exception as e:
            print(f"[Warning] Instagram Graph API call failed: {e}")

    # Fallback / Staging Mode Response
    staged_payload = {
        "status": "staged_ready_to_publish",
        "message": "Carousel slides and AI caption generated successfully. Ready for manual upload or Graph API webhook dispatch.",
        "slides_count": len(slides),
        "caption_length": len(caption)
    }

    if webhook_url:
        try:
            requests.post(webhook_url, json=staged_payload, timeout=5)
            staged_payload["webhook_delivered"] = True
        except Exception:
            staged_payload["webhook_delivered"] = False

    return staged_payload
