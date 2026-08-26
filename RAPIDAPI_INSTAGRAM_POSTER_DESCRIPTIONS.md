# 📝 RapidAPI Short & Long Descriptions for Instagram Poster Pro

Below are the pre-written **Short Description** and **Long Description** formatted specifically for your RapidAPI Studio listing.

---

## 📌 1. Short Description (Tagline / Summary - Under 250 Chars)

```text
Turn any product or Amazon URL into 5 high-converting 1080x1350 visual carousel slides, AI technical copywriting, Amazon affiliate link tagging, and automated Instagram publishing! Just $4.99/1k posts—80% cheaper!
```

---

## 📜 2. Long Description (RapidAPI Overview Tab)

```markdown
# 📸 Instagram Automated Carousel & Post Publisher Pro

Turn any product link, specs, or Amazon URL into a complete 5-slide **1080x1350 px** visual carousel post, AI technical copywriting (Hook, Specs, Pros/Cons, Verdict, CTA), Amazon affiliate link tagging, and automated Instagram Graph API publishing.

---

## 🚀 Key Features & Output Data Fields

* **🎨 1080x1350 Visual Slide Cards**: Generates 5 distinct high-resolution visual cards (`dark_cyan`, `emerald`, `purple`, `minimal_white`).
* **📝 AI Technical Copywriting**: High-converting Hook, Specs Grid, Pros/Cons Breakdown, Verdict Score (e.g. 9.4/10), and Instagram Caption with hashtags.
* **💵 Amazon Affiliate Monetization**: Automatic tag injection (`?tag=yourtag-20`) for commission earnings.
* **📲 Instagram Graph API & Webhook Dispatcher**: Direct live publishing or staging callbacks.

---

## 📥 Sample Request JSON

```json
{
  "product_url": "https://www.amazon.com/dp/B0CX23F8H8",
  "theme": "dark_cyan",
  "brand_name": "@TechGearDaily",
  "amazon_affiliate_tag": "techspecdiges-20"
}
```

## 📤 Sample Response JSON

```json
{
  "status": "success",
  "product_name": "UltraSound Pro Wireless Headphones",
  "theme": "dark_cyan",
  "brand_name": "@TechGearDaily",
  "total_slides": 5,
  "slides": [
    {
      "slide_number": 1,
      "width": 1080,
      "height": 1350,
      "theme": "dark_cyan",
      "image_base64": "data:image/png;base64,..."
    }
  ],
  "instagram_caption": "🎧 Looking for top-tier audio quality? Check out our full review for UltraSound Pro Wireless Headphones! ⚡\n\n✨ Key Highlights:\n- Battery: 40 Hours Playtime\n- Noise Canceling: Active Hybrid ANC\n\n⭐ Verdict: 9.4/10 (Must Buy)\n\n📦 Available on Amazon with Prime!\n🔗 Link in Bio (Amazon Prime): amzn.to/3xY8z\n💬 Comment 'AMAZON' below to get the direct link in your DMs!\n\n#TechReview #AmazonDeals #AudioTech #HeadphonesReview"
}
```
```
