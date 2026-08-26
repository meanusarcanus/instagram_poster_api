import requests
import re
import json

url = 'https://www.amazon.com/dp/B0DP24FQ5M'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9'
}
r = requests.get(url, headers=headers, timeout=10)
html = r.text

print("Pattern 1 (data-old-hires):", re.findall(r'data-old-hires=["\'](https://m\.media-amazon\.com/images/I/[^"\']+)["\']', html))
print("Pattern 2 (hiRes):", re.findall(r'\"hiRes\":\"(https://m\.media-amazon\.com/images/I/[^\"]+)\"', html))
print("Pattern 3 (large):", re.findall(r'\"large\":\"(https://m\.media-amazon\.com/images/I/[^\"]+)\"', html))

dyn = re.findall(r'data-a-dynamic-image=["\'](\{.*?\})["\']', html)
if dyn:
    try:
        img_dict = json.loads(dyn[0].replace('&quot;', '"'))
        print("Pattern 4 (dynamic-image):", list(img_dict.keys()))
    except Exception as e:
        print("Pattern 4 err:", e)
