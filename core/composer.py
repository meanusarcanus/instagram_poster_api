"""
Pillow (PIL) 1080x1350 Visual Carousel Slide Card Composer with Real Product Image Rendering
"""

import io
import base64
import requests
from typing import List, Dict, Any, Optional
from PIL import Image, ImageDraw, ImageFont, ImageOps

COLOR_THEMES = {
    "dark_cyan": {
        "bg": (11, 19, 43),
        "card_bg": (28, 37, 65),
        "accent": (0, 229, 255),
        "accent_secondary": (0, 255, 135),
        "text": (255, 255, 255),
        "text_sub": (148, 163, 184),
        "pro_color": (0, 255, 135),
        "con_color": (255, 77, 109)
    },
    "emerald": {
        "bg": (6, 44, 34),
        "card_bg": (15, 76, 58),
        "accent": (16, 185, 129),
        "accent_secondary": (163, 230, 53),
        "text": (255, 255, 255),
        "text_sub": (167, 243, 208),
        "pro_color": (163, 230, 53),
        "con_color": (248, 113, 113)
    },
    "purple": {
        "bg": (19, 0, 43),
        "card_bg": (35, 11, 78),
        "accent": (217, 70, 239),
        "accent_secondary": (139, 92, 246),
        "text": (255, 255, 255),
        "text_sub": (221, 214, 254),
        "pro_color": (52, 211, 153),
        "con_color": (244, 63, 94)
    },
    "minimal_white": {
        "bg": (248, 250, 252),
        "card_bg": (237, 242, 247),
        "accent": (37, 99, 235),
        "accent_secondary": (13, 148, 136),
        "text": (15, 23, 42),
        "text_sub": (100, 116, 139),
        "pro_color": (16, 185, 129),
        "con_color": (225, 29, 72)
    }
}

def get_font(size: int, bold: bool = False):
    try:
        font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
        return ImageFont.truetype(font_path, size)
    except Exception:
        return ImageFont.load_default()

def fetch_product_image(image_url: Optional[str], target_size: tuple = (400, 400)) -> Optional[Image.Image]:
    """
    Fetches and resizes real product image over HTTP.
    """
    if not image_url or os.getenv("DISABLE_LLM") == "true":
        return None
    try:
        res = requests.get(image_url, timeout=4)
        if res.status_code == 200:
            img = Image.open(io.BytesIO(res.content)).convert("RGBA")
            img = ImageOps.fit(img, target_size, method=Image.Resampling.LANCZOS)
            return img
    except Exception:
        pass
    return None

import os

def render_slide_card(
    slide_num: int,
    slide_data: Dict[str, Any],
    theme_name: str = "dark_cyan",
    brand_name: str = "@TechGearDaily",
    product_image_url: Optional[str] = None
) -> Image.Image:
    """
    Renders a single 1080x1350 px Instagram Carousel Slide with optional real product image.
    """
    width, height = 1080, 1350
    palette = COLOR_THEMES.get(theme_name.lower(), COLOR_THEMES["dark_cyan"])

    img = Image.new("RGB", (width, height), palette["bg"])
    draw = ImageDraw.Draw(img)

    # 1. Header Bar & Brand Watermark
    font_brand = get_font(28, bold=True)
    draw.text((60, 60), brand_name, fill=palette["accent"], font=font_brand)
    draw.text((width - 160, 60), f"SLIDE {slide_num}/5", fill=palette["text_sub"], font=get_font(24, bold=True))
    draw.line([(60, 110), (width - 60, 110)], fill=palette["card_bg"], width=4)

    font_title = get_font(44, bold=True)
    font_body = get_font(30, bold=False)

    # Fetch Real Product Image (if available)
    prod_img = fetch_product_image(product_image_url, target_size=(360, 360))

    if slide_num == 1:
        # HOOK SLIDE
        h_data = slide_data.get("slide_1_hook", {})
        title_text = h_data.get("title", "Product Review")
        sub_text = h_data.get("subtitle", "Full Specs Breakdown")

        # Outer Hook Box Card
        draw.rounded_rectangle([(60, 160), (width - 60, 1150)], radius=30, fill=palette["card_bg"])
        
        # Featured Review Badge
        draw.rounded_rectangle([(100, 200), (450, 260)], radius=18, fill=palette["accent"])
        draw.text((120, 218), "FEATURED REVIEW", fill=palette["bg"], font=get_font(22, bold=True))

        # Title & Subtitle
        draw.text((100, 290), title_text[:65], fill=palette["text"], font=font_title)
        draw.text((100, 480), sub_text[:90], fill=palette["text_sub"], font=font_body)

        # Real Product Photo Showcase Box
        photo_box = [(width // 2 - 200, 570), (width // 2 + 200, 970)]
        draw.rounded_rectangle(photo_box, radius=24, fill=palette["bg"], outline=palette["accent"], width=3)

        if prod_img:
            img.paste(prod_img, (width // 2 - 180, 590), prod_img)
        else:
            # Fallback Product Icon Drawing
            draw.text((width // 2 - 120, 740), "📷 PRODUCT PHOTO", fill=palette["accent_secondary"], font=get_font(24, bold=True))

        # Swipe Badge
        draw.rounded_rectangle([(width // 2 - 180, 1030), (width // 2 + 180, 1100)], radius=22, fill=palette["accent_secondary"])
        draw.text((width // 2 - 140, 1050), "SWIPE FOR SPECS ➔", fill=palette["bg"], font=get_font(24, bold=True))

    elif slide_num == 2:
        # SPECS SLIDE
        s_data = slide_data.get("slide_2_specs", {})
        draw.text((60, 140), s_data.get("title", "Technical Specifications"), fill=palette["accent"], font=font_title)

        items = s_data.get("items", ["Spec 1", "Spec 2", "Spec 3", "Spec 4"])
        y_pos = 240
        for item in items[:4]:
            draw.rounded_rectangle([(60, y_pos), (width - 60, y_pos + 190)], radius=20, fill=palette["card_bg"])
            draw.text((100, y_pos + 40), "• " + str(item)[:55], fill=palette["text"], font=font_body)
            y_pos += 220

    elif slide_num == 3:
        # PROS & CONS SLIDE
        pc_data = slide_data.get("slide_3_pros_cons", {})
        draw.text((60, 140), pc_data.get("title", "Pros & Cons Breakdown"), fill=palette["accent"], font=font_title)

        draw.rounded_rectangle([(60, 240), (width - 60, 660)], radius=24, fill=palette["card_bg"])
        draw.text((100, 270), "✅ THE GOOD (PROS)", fill=palette["pro_color"], font=get_font(30, bold=True))
        y_p = 350
        for pro in pc_data.get("pros", [])[:3]:
            draw.text((100, y_p), f"✓ {pro[:45]}", fill=palette["text"], font=font_body)
            y_p += 70

        draw.rounded_rectangle([(60, 700), (width - 60, 1120)], radius=24, fill=palette["card_bg"])
        draw.text((100, 730), "⚠️ CONSIDERATIONS (CONS)", fill=palette["con_color"], font=get_font(30, bold=True))
        y_c = 810
        for con in pc_data.get("cons", [])[:2]:
            draw.text((100, y_c), f"✗ {con[:45]}", fill=palette["text"], font=font_body)
            y_c += 70

    elif slide_num == 4:
        # VERDICT & SCORE SLIDE
        v_data = slide_data.get("slide_4_verdict", {})
        draw.text((60, 140), v_data.get("title", "Final Verdict"), fill=palette["accent"], font=font_title)

        draw.rounded_rectangle([(60, 240), (width - 60, 1120)], radius=30, fill=palette["card_bg"])
        
        # Rating Circle Badge
        draw.ellipse([(width // 2 - 130, 300), (width // 2 + 130, 560)], fill=palette["accent"])
        draw.text((width // 2 - 90, 390), v_data.get("score", "9.4/10"), fill=palette["bg"], font=get_font(42, bold=True))

        draw.text((100, 620), "EDITOR'S BUYER RATING", fill=palette["accent_secondary"], font=get_font(26, bold=True))
        draw.text((100, 690), v_data.get("summary", "Highly recommended.")[:180], fill=palette["text"], font=font_body)

    else:
        # CTA SLIDE (SLIDE 5)
        cta_data = slide_data.get("slide_5_cta", {})
        draw.rounded_rectangle([(60, 220), (width - 60, 1120)], radius=30, fill=palette["card_bg"])
        
        draw.text((100, 290), "READY TO BUY?", fill=palette["accent"], font=get_font(30, bold=True))
        draw.text((100, 360), cta_data.get("title", "Where To Buy"), fill=palette["text"], font=font_title)

        # Store Button
        draw.rounded_rectangle([(100, 520), (width - 100, 640)], radius=24, fill=palette["accent"])
        draw.text((140, 560), "🛍️ " + cta_data.get("button_text", "Available on Amazon Prime")[:35], fill=palette["bg"], font=get_font(30, bold=True))

        # Bio Link Prompt
        draw.rounded_rectangle([(100, 690), (width - 100, 810)], radius=24, fill=palette["accent_secondary"])
        draw.text((140, 730), "🔗 " + cta_data.get("prompt", f"Link in Bio: {brand_name}")[:35], fill=palette["bg"], font=get_font(30, bold=True))

        draw.text((width // 2 - 180, 920), "💬 Comment 'AMAZON' for direct link!", fill=palette["text_sub"], font=get_font(22, bold=True))

    # 3. Footer Branding
    draw.line([(60, 1240), (width - 60, 1240)], fill=palette["card_bg"], width=3)
    draw.text((60, 1270), brand_name, fill=palette["text_sub"], font=get_font(22, bold=False))
    draw.text((width - 320, 1270), "SAVE THIS POST 🔖", fill=palette["accent"], font=get_font(22, bold=True))

    return img

def compose_full_carousel(
    copy_payload: Dict[str, Any],
    theme_name: str = "dark_cyan",
    brand_name: str = "@TechGearDaily",
    product_image_url: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Renders all 5 carousel slides and returns Base64 encoded PNG data strings.
    """
    slides_output = []

    for i in range(1, 6):
        pil_img = render_slide_card(
            i,
            copy_payload,
            theme_name=theme_name,
            brand_name=brand_name,
            product_image_url=product_image_url
        )
        buffer = io.BytesIO()
        pil_img.save(buffer, format="PNG")
        b64_str = base64.b64encode(buffer.getvalue()).decode("utf-8")
        slides_output.append({
            "slide_number": i,
            "width": 1080,
            "height": 1350,
            "theme": theme_name,
            "image_base64": f"data:image/png;base64,{b64_str}"
        })

    return slides_output
