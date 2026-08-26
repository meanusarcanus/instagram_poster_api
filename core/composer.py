"""
Pillow (PIL) 1080x1350 Visual Carousel Slide Card Composer
"""

import io
import base64
from typing import List, Dict, Any, Optional
from PIL import Image, ImageDraw, ImageFont

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
    """
    Loads default PIL font with specified size fallback.
    """
    try:
        font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
        return ImageFont.truetype(font_path, size)
    except Exception:
        return ImageFont.load_default()

def render_slide_card(
    slide_num: int,
    slide_data: Dict[str, Any],
    theme_name: str = "dark_cyan",
    brand_name: str = "@TechGearDaily"
) -> Image.Image:
    """
    Renders a single 1080x1350 px Instagram Carousel Slide.
    """
    width, height = 1080, 1350
    palette = COLOR_THEMES.get(theme_name.lower(), COLOR_THEMES["dark_cyan"])

    img = Image.new("RGB", (width, height), palette["bg"])
    draw = ImageDraw.Draw(img)

    # 1. Header Bar & Brand Watermark
    font_brand = get_font(28, bold=True)
    draw.text((60, 60), brand_name, fill=palette["accent"], font=font_brand)
    draw.text((width - 160, 60), f"SLIDE {slide_num}/5", fill=palette["text_sub"], font=get_font(24, bold=True))

    # Decorative header divider line
    draw.line([(60, 110), (width - 60, 110)], fill=palette["card_bg"], width=4)

    # 2. Render Slide Specific Cards
    font_title = get_font(46, bold=True)
    font_body = get_font(32, bold=False)

    if slide_num == 1:
        # HOOK SLIDE
        h_data = slide_data.get("slide_1_hook", {})
        title_text = h_data.get("title", "Product Review")
        sub_text = h_data.get("subtitle", "Full Specs Breakdown")

        # Large Hook Box Card
        draw.rounded_rectangle([(60, 240), (width - 60, 1050)], radius=30, fill=palette["card_bg"])
        
        # Badge
        draw.rounded_rectangle([(100, 300), (450, 370)], radius=20, fill=palette["accent"])
        draw.text((120, 320), "FEATURED REVIEW", fill=palette["bg"], font=get_font(24, bold=True))

        # Title & Subtitle Text
        draw.text((100, 430), title_text[:75], fill=palette["text"], font=font_title)
        draw.text((100, 650), sub_text[:110], fill=palette["text_sub"], font=font_body)

        # Swipe indicator badge
        draw.rounded_rectangle([(width // 2 - 180, 920), (width // 2 + 180, 990)], radius=25, fill=palette["accent_secondary"])
        draw.text((width // 2 - 140, 940), "SWIPE FOR SPECS ➔", fill=palette["bg"], font=get_font(24, bold=True))

    elif slide_num == 2:
        # SPECS SLIDE
        s_data = slide_data.get("slide_2_specs", {})
        draw.text((60, 160), s_data.get("title", "Technical Specifications"), fill=palette["accent"], font=font_title)

        items = s_data.get("items", ["Spec 1", "Spec 2", "Spec 3", "Spec 4"])
        y_pos = 280
        for item in items[:4]:
            draw.rounded_rectangle([(60, y_pos), (width - 60, y_pos + 180)], radius=20, fill=palette["card_bg"])
            draw.text((100, y_pos + 40), "• " + str(item)[:55], fill=palette["text"], font=font_body)
            y_pos += 210

    elif slide_num == 3:
        # PROS & CONS SLIDE
        pc_data = slide_data.get("slide_3_pros_cons", {})
        draw.text((60, 160), pc_data.get("title", "Pros & Cons Breakdown"), fill=palette["accent"], font=font_title)

        # Pros Card
        draw.rounded_rectangle([(60, 270), (width - 60, 680)], radius=24, fill=palette["card_bg"])
        draw.text((100, 300), "✅ THE GOOD (PROS)", fill=palette["pro_color"], font=get_font(32, bold=True))
        y_p = 380
        for pro in pc_data.get("pros", [])[:3]:
            draw.text((100, y_p), f"✓ {pro[:45]}", fill=palette["text"], font=font_body)
            y_p += 75

        # Cons Card
        draw.rounded_rectangle([(60, 720), (width - 60, 1130)], radius=24, fill=palette["card_bg"])
        draw.text((100, 750), "⚠️ CONSIDERATIONS (CONS)", fill=palette["con_color"], font=get_font(32, bold=True))
        y_c = 830
        for con in pc_data.get("cons", [])[:2]:
            draw.text((100, y_c), f"✗ {con[:45]}", fill=palette["text"], font=font_body)
            y_c += 75

    elif slide_num == 4:
        # VERDICT & SCORE SLIDE
        v_data = slide_data.get("slide_4_verdict", {})
        draw.text((60, 160), v_data.get("title", "Final Verdict"), fill=palette["accent"], font=font_title)

        # Big Rating Card
        draw.rounded_rectangle([(60, 260), (width - 60, 1100)], radius=30, fill=palette["card_bg"])
        
        # Rating Circle Badge
        draw.ellipse([(width // 2 - 130, 330), (width // 2 + 130, 590)], fill=palette["accent"])
        draw.text((width // 2 - 90, 420), v_data.get("score", "9.4/10"), fill=palette["bg"], font=get_font(42, bold=True))

        draw.text((100, 650), "EDITOR'S BUYER RATING", fill=palette["accent_secondary"], font=get_font(28, bold=True))
        draw.text((100, 720), v_data.get("summary", "Highly recommended.")[:180], fill=palette["text"], font=font_body)

    else:
        # CTA SLIDE (SLIDE 5)
        cta_data = slide_data.get("slide_5_cta", {})
        draw.rounded_rectangle([(60, 240), (width - 60, 1050)], radius=30, fill=palette["card_bg"])
        
        draw.text((100, 320), "READY TO BUY?", fill=palette["accent"], font=get_font(32, bold=True))
        draw.text((100, 400), cta_data.get("title", "Where To Buy"), fill=palette["text"], font=font_title)

        # Store Button
        draw.rounded_rectangle([(100, 550), (width - 100, 670)], radius=25, fill=palette["accent"])
        draw.text((140, 590), "🛍️ " + cta_data.get("button_text", "Available on Amazon Prime")[:35], fill=palette["bg"], font=get_font(32, bold=True))

        # Bio Link Prompt
        draw.rounded_rectangle([(100, 720), (width - 100, 840)], radius=25, fill=palette["accent_secondary"])
        draw.text((140, 760), "🔗 " + cta_data.get("prompt", f"Link in Bio: {brand_name}")[:35], fill=palette["bg"], font=get_font(32, bold=True))

        draw.text((width // 2 - 180, 940), "💬 Comment 'AMAZON' for direct link!", fill=palette["text_sub"], font=get_font(22, bold=True))

    # 3. Footer Branding
    draw.line([(60, 1240), (width - 60, 1240)], fill=palette["card_bg"], width=3)
    draw.text((60, 1270), brand_name, fill=palette["text_sub"], font=get_font(22, bold=False))
    draw.text((width - 320, 1270), "SAVE THIS POST 🔖", fill=palette["accent"], font=get_font(22, bold=True))

    return img

def compose_full_carousel(
    copy_payload: Dict[str, Any],
    theme_name: str = "dark_cyan",
    brand_name: str = "@TechGearDaily"
) -> List[Dict[str, Any]]:
    """
    Renders all 5 carousel slides and returns Base64 encoded PNG data strings.
    """
    slides_output = []

    for i in range(1, 6):
        pil_img = render_slide_card(i, copy_payload, theme_name=theme_name, brand_name=brand_name)
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
