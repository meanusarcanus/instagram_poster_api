"""
Pillow (PIL) 1080x1350 Visual Carousel Slide Card Composer with Real Product Image Rendering
"""

import io
import os
import base64
import textwrap
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

def fetch_product_image(image_url: Optional[str], target_size: tuple = (540, 540)) -> Optional[Image.Image]:
    """
    Fetches and resizes real high-resolution product image over HTTP with image headers.
    """
    if not image_url:
        return None
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
        "Referer": "https://www.google.com/"
    }
    try:
        print(f"[Composer Engine] Fetching high-res product photo: {image_url}")
        res = requests.get(image_url, headers=headers, timeout=8)
        print(f"[Composer Engine] HTTP Response: {res.status_code}, Length: {len(res.content)} bytes")
        if res.status_code == 200 and len(res.content) > 500:
            img = Image.open(io.BytesIO(res.content))
            if img.mode != "RGB":
                img = img.convert("RGB")
            img = ImageOps.fit(img, target_size, method=Image.Resampling.LANCZOS)
            print(f"✓ [Composer Engine] Successfully fitted high-res product photo to {target_size}!")
            return img
    except Exception as e:
        print(f"[Warning] Failed to fetch image '{image_url}': {e}")
    return None

def render_slide_card(
    slide_num: int,
    slide_data: Dict[str, Any],
    theme_name: str = "dark_cyan",
    brand_name: str = "@TechGearDaily",
    product_image_url: Optional[str] = None
) -> Image.Image:
    """
    Renders a single 1080x1350 px Instagram Carousel Slide with high-res product image & multi-line text wrapping.
    """
    width, height = 1080, 1350
    palette = COLOR_THEMES.get(theme_name.lower(), COLOR_THEMES["dark_cyan"])

    img = Image.new("RGB", (width, height), palette["bg"])
    draw = ImageDraw.Draw(img)

    # Header Bar
    font_brand = get_font(28, bold=True)
    draw.text((60, 60), brand_name, fill=palette["accent"], font=font_brand)
    draw.text((width - 160, 60), f"SLIDE {slide_num}/5", fill=palette["text_sub"], font=get_font(24, bold=True))
    draw.line([(60, 110), (width - 60, 110)], fill=palette["card_bg"], width=4)

    font_title = get_font(38, bold=True)
    font_body = get_font(28, bold=False)

    # Fetch High-Res Product Image (540x540 px)
    prod_img = fetch_product_image(product_image_url, target_size=(540, 540))

    if slide_num == 1:
        # HOOK SLIDE
        h_data = slide_data.get("slide_1_hook", {})
        title_text = h_data.get("title", "Product Review")
        sub_text = h_data.get("subtitle", "Full Specs Breakdown")

        # Outer Hook Box Card
        draw.rounded_rectangle([(60, 140), (width - 60, 1180)], radius=30, fill=palette["card_bg"])
        
        # Featured Review Badge
        draw.rounded_rectangle([(90, 175), (440, 235)], radius=18, fill=palette["accent"])
        draw.text((110, 193), "FEATURED REVIEW", fill=palette["bg"], font=get_font(22, bold=True))

        # Title (wrapped to 26 chars per line) & Subtitle
        wrapped_title = textwrap.fill(title_text[:85], width=26)
        draw.text((90, 255), wrapped_title, fill=palette["text"], font=font_title)
        
        # Position subtitle below wrapped title
        title_lines = len(wrapped_title.split("\n"))
        sub_y = 255 + (title_lines * 48) + 15
        draw.text((90, sub_y), sub_text[:80], fill=palette["text_sub"], font=font_body)

        # High-Res Product Photo Showcase Box (540x540 px)
        photo_box = [(width // 2 - 270, 480), (width // 2 + 270, 1020)]
        draw.rounded_rectangle(photo_box, radius=28, fill=palette["bg"], outline=palette["accent"], width=4)

        if prod_img:
            img.paste(prod_img, (width // 2 - 270, 480))
        else:
            draw.text((width // 2 - 140, 720), "📷 PRODUCT PHOTO", fill=palette["accent_secondary"], font=get_font(28, bold=True))

        # Swipe Badge
        draw.rounded_rectangle([(width // 2 - 200, 1060), (width // 2 + 200, 1140)], radius=24, fill=palette["accent_secondary"])
        draw.text((width // 2 - 150, 1085), "SWIPE FOR SPECS ➔", fill=palette["bg"], font=get_font(24, bold=True))

    elif slide_num == 2:
        # SPECS SLIDE
        s_data = slide_data.get("slide_2_specs", {})
        draw.text((60, 140), s_data.get("title", "Technical Specifications"), fill=palette["accent"], font=font_title)

        items = s_data.get("items", ["Spec 1", "Spec 2", "Spec 3", "Spec 4"])
        y_pos = 230
        font_spec = get_font(26, bold=False)

        for item in items[:4]:
            wrapped_item = textwrap.fill("• " + str(item), width=42)
            num_lines = len(wrapped_item.split("\n"))
            box_height = max(140, num_lines * 34 + 40)
            
            draw.rounded_rectangle([(60, y_pos), (width - 60, y_pos + box_height)], radius=20, fill=palette["card_bg"])
            draw.text((90, y_pos + 20), wrapped_item, fill=palette["text"], font=font_spec)
            y_pos += box_height + 20

    elif slide_num == 3:
        # PROS & CONS SLIDE
        pc_data = slide_data.get("slide_3_pros_cons", {})
        draw.text((60, 140), pc_data.get("title", "Pros & Cons Breakdown"), fill=palette["accent"], font=font_title)

        draw.rounded_rectangle([(60, 240), (width - 60, 660)], radius=24, fill=palette["card_bg"])
        draw.text((100, 270), "✅ THE GOOD (PROS)", fill=palette["pro_color"], font=get_font(28, bold=True))
        y_p = 340
        font_pc = get_font(26, bold=False)
        for pro in pc_data.get("pros", [])[:3]:
            wrapped_pro = textwrap.fill("✓ " + str(pro), width=40)
            draw.text((100, y_p), wrapped_pro, fill=palette["text"], font=font_pc)
            y_p += (len(wrapped_pro.split("\n")) * 32) + 20

        draw.rounded_rectangle([(60, 700), (width - 60, 1120)], radius=24, fill=palette["card_bg"])
        draw.text((100, 730), "⚠️ CONSIDERATIONS (CONS)", fill=palette["con_color"], font=get_font(28, bold=True))
        y_c = 800
        for con in pc_data.get("cons", [])[:2]:
            wrapped_con = textwrap.fill("✗ " + str(con), width=40)
            draw.text((100, y_c), wrapped_con, fill=palette["text"], font=font_pc)
            y_c += (len(wrapped_con.split("\n")) * 32) + 20

    elif slide_num == 4:
        # VERDICT SLIDE (Multi-Line Text Wrapping Fix)
        v_data = slide_data.get("slide_4_verdict", {})
        draw.text((60, 140), v_data.get("title", "Final Verdict"), fill=palette["accent"], font=font_title)

        draw.rounded_rectangle([(60, 240), (width - 60, 1120)], radius=30, fill=palette["card_bg"])
        
        # Rating Circle
        draw.ellipse([(width // 2 - 130, 300), (width // 2 + 130, 560)], fill=palette["accent"])
        draw.text((width // 2 - 90, 390), v_data.get("score", "9.4/10"), fill=palette["bg"], font=get_font(42, bold=True))

        draw.text((100, 620), "EDITOR'S BUYER RATING", fill=palette["accent_secondary"], font=get_font(26, bold=True))
        
        # Multi-Line Summary Wrapping
        summary_raw = v_data.get("summary", "Highly recommended daily essential.")
        wrapped_summary = textwrap.fill(summary_raw, width=38)
        draw.text((100, 680), wrapped_summary, fill=palette["text"], font=font_body)

    else:
        # CTA SLIDE (Multi-Line Text Wrapping Fix)
        cta_data = slide_data.get("slide_5_cta", {})
        draw.rounded_rectangle([(60, 220), (width - 60, 1120)], radius=30, fill=palette["card_bg"])
        
        draw.text((100, 290), "READY TO BUY?", fill=palette["accent"], font=get_font(30, bold=True))
        
        cta_title = textwrap.fill(cta_data.get("title", "Where To Buy"), width=34)
        draw.text((100, 360), cta_title, fill=palette["text"], font=font_title)

        draw.rounded_rectangle([(100, 540), (width - 100, 680)], radius=24, fill=palette["accent"])
        btn_text = textwrap.fill("🛍️ " + cta_data.get("button_text", "Available Online Now"), width=30)
        draw.text((130, 580), btn_text, fill=palette["bg"], font=get_font(28, bold=True))

        draw.rounded_rectangle([(100, 730), (width - 100, 870)], radius=24, fill=palette["accent_secondary"])
        prompt_text = textwrap.fill("🔗 " + cta_data.get("prompt", f"Link in Bio: {brand_name}"), width=30)
        draw.text((130, 770), prompt_text, fill=palette["bg"], font=get_font(28, bold=True))

        draw.text((width // 2 - 200, 960), "💬 Comment 'DEAL' for direct link!", fill=palette["text_sub"], font=get_font(22, bold=True))

    # Footer
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
