import requests
import urllib.parse
import re

query = 'Stylus Pen for iPad A16 11th 10th 9th Gen'
short_q = ' '.join(query.split()[:4]) + ' product photo'

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'}
search_url = f'https://www.bing.com/images/search?q={urllib.parse.quote(short_q)}&form=HDRSC2'

r = requests.get(search_url, headers=headers, timeout=5)
murl_matches = re.findall(r'murl&quot;:&quot;(https://[^&"]+)&quot;', r.text)
if not murl_matches:
    murl_matches = re.findall(r'murl["\']:["\'](https://[^"\']+)["\']', r.text)

print("Images found:", len(murl_matches))
for img in murl_matches[:3]:
    print("FOUND IMAGE:", img)
