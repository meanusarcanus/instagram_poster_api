# 📸 Instagram Automated Carousel & Post Publisher Python SDK

Official Python SDK for `instagram-poster-api`. Turn product URLs into 5-slide 1080x1350 visual carousel posts, AI copywriting, Amazon affiliate link tagging, and Instagram publishing in 1 line of Python code.

## 🚀 Installation
```bash
pip install instagram-poster-api
```

## 💻 Quick Usage
```python
from instagram_poster import InstagramPosterClient

client = InstagramPosterClient(api_key="YOUR_RAPIDAPI_KEY")
res = client.generate_slides(
    product_url="https://www.amazon.com/dp/B0CX23F8H8",
    theme="dark_cyan",
    brand_name="@TechGearDaily"
)

print(f"Generated {res['total_slides']} 1080x1350 slides for {res['product_name']}!")
```
