# 📸 Instagram Automated Carousel & Post Publisher MicroSaaS API

Automated MicroSaaS API engine to turn product URLs and specs into high-converting 1080x1350 visual carousel posts, AI technical copywriting, Amazon affiliate link tagging, and direct Instagram Graph API publishing.

---

## 🚀 Quick Start

### 1. Run Locally
```bash
pip install -r requirements.txt
uvicorn api.index:app --reload
```

### 2. Run Automated Test Suite
```bash
python3 test_api.py
```

### 3. API Endpoints
- `GET /api/v1/health`: API status & telemetry check
- `POST /api/v1/generate-slides`: Generate 1080x1350 visual carousel slides (Base64 PNG) & AI copy payload
- `POST /api/v1/publish`: Generate slides, AI copy, and publish/stage post on Instagram
