import os
import json
import requests
import re
from typing import List, Optional, Dict, Any

try:
    from fastapi import FastAPI, HTTPException
    from pydantic import BaseModel, Field
except ImportError:
    class BaseModel:
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)
        def dict(self, *args, **kwargs):
            return self.__dict__

    def Field(*args, **kwargs):
        return kwargs.get("default", None)

    class FastAPI:
        def __init__(self, **kwargs): pass
        def get(self, *args, **kwargs): return lambda fn: fn
        def post(self, *args, **kwargs): return lambda fn: fn
        def openapi(self): return {"openapi": "3.0.2", "info": {"title": "Instagram Automated Carousel & Post Publisher MicroSaaS API", "version": "1.0.0"}}

    class HTTPException(Exception): pass

from core.scraper import scrape_product_details
from core.copywriter import generate_carousel_copy
from core.composer import compose_full_carousel
from core.publisher import publish_instagram_carousel

app = FastAPI(
    title="Instagram Automated Carousel & Post Publisher MicroSaaS API",
    description="Automated MicroSaaS API engine to turn product URLs and specs into high-converting 1080x1350 visual carousel posts, AI technical copywriting, and direct Instagram Graph API publishing.",
    version="1.0.0"
)

# ==============================================================================
# Pydantic Schemas
# ==============================================================================
class GenerateSlidesRequest(BaseModel):
    product_url: Optional[str] = Field(default="https://www.amazon.com/dp/B0CX23F8H8", description="Product or E-commerce URL")
    product_name: Optional[str] = Field(default=None, description="Raw product title if no URL provided")
    product_specs: Optional[Dict[str, str]] = Field(default=None, description="Technical specs key-value map")
    image_url: Optional[str] = Field(default=None, description="Direct product photo URL to render on slides")
    theme: Optional[str] = Field(default="dark_cyan", description="Visual theme: dark_cyan, emerald, purple, minimal_white")
    brand_name: Optional[str] = Field(default="@TechGearDaily", description="Brand handle or watermark text")
    amazon_affiliate_tag: Optional[str] = Field(default="techspecdiges-20", description="Amazon Associates affiliate tag")

class PublishPostRequest(GenerateSlidesRequest):
    instagram_credentials: Optional[Dict[str, str]] = Field(default=None, description="Instagram Graph API account_id & access_token")
    webhook_url: Optional[str] = Field(default=None, description="Webhook URL for staging notification callback")
    auto_publish: Optional[bool] = Field(default=False, description="Set to true for live Instagram Graph API publish")

class SlideOutput(BaseModel):
    slide_number: int
    width: int
    height: int
    theme: str
    image_base64: str

class GenerateSlidesResponse(BaseModel):
    status: str
    product_name: str
    product_url: str
    theme: str
    brand_name: str
    total_slides: int
    slides: List[SlideOutput]
    instagram_caption: str
    copy_breakdown: Dict[str, Any]

class PublishPostResponse(GenerateSlidesResponse):
    publish_result: Dict[str, Any]

# ==============================================================================
# Health Check Endpoint
# ==============================================================================
@app.get("/")
@app.get("/api/v1/health")
def read_root():
    return {
        "status": "online",
        "service": "Instagram Automated Carousel & Post Publisher MicroSaaS API",
        "version": "1.0.0",
        "endpoints": {
            "POST /api/v1/generate-slides": "Generate 1080x1350 visual carousel slides & AI copy payload",
            "POST /api/v1/publish": "Generate carousel slides, AI copy, and publish/stage post on Instagram"
        }
    }

# ==============================================================================
# Endpoint 1: POST /api/v1/generate-slides
# ==============================================================================
@app.post("/api/v1/generate-slides", response_model=GenerateSlidesResponse)
def generate_slides(payload: GenerateSlidesRequest):
    product_data = scrape_product_details(
        product_url=payload.product_url,
        product_name=payload.product_name,
        product_specs=payload.product_specs,
        image_url=payload.image_url,
        amazon_affiliate_tag=payload.amazon_affiliate_tag
    )

    theme = (payload.theme or "dark_cyan").lower()
    brand = payload.brand_name or "@TechGearDaily"

    copy_payload = generate_carousel_copy(
        product_data=product_data,
        brand_name=brand,
        amazon_tag=payload.amazon_affiliate_tag
    )

    slides = compose_full_carousel(
        copy_payload=copy_payload,
        theme_name=theme,
        brand_name=brand,
        product_image_url=product_data.get("image_url")
    )

    slides_objs = [SlideOutput(**s) for s in slides]

    return GenerateSlidesResponse(
        status="success",
        product_name=product_data.get("title", "Product"),
        product_url=product_data.get("product_url", ""),
        theme=theme,
        brand_name=brand,
        total_slides=len(slides_objs),
        slides=slides_objs,
        instagram_caption=copy_payload.get("instagram_caption", ""),
        copy_breakdown=copy_payload
    )

# ==============================================================================
# Endpoint 2: POST /api/v1/publish
# ==============================================================================
@app.post("/api/v1/publish", response_model=PublishPostResponse)
def publish_post(payload: PublishPostRequest):
    gen_res = generate_slides(payload)

    pub_res = publish_instagram_carousel(
        slides=[s.dict() for s in gen_res.slides],
        caption=gen_res.instagram_caption,
        instagram_credentials=payload.instagram_credentials,
        webhook_url=payload.webhook_url
    )

    return PublishPostResponse(
        status="success",
        product_name=gen_res.product_name,
        product_url=gen_res.product_url,
        theme=gen_res.theme,
        brand_name=gen_res.brand_name,
        total_slides=gen_res.total_slides,
        slides=gen_res.slides,
        instagram_caption=gen_res.instagram_caption,
        copy_breakdown=gen_res.copy_breakdown,
        publish_result=pub_res
    )
