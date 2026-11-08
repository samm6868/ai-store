import os
import json
import urllib.request
import urllib.parse
import random
from datetime import datetime

raw_key = os.environ.get("GEMINI_API_KEY", "")
API_KEY = raw_key.strip()
AFFILIATE_KEY = "_c4Lh9g5v"
AFFILIATE_LINK = "https://s.click.aliexpress.com/e/_c4Lh9g5v"
STORE_URL = "https://samm6868.github.io/ai-store"

prompt = """
Act as an elite E-Commerce Dropshipping & Marketing AI Agent.
Select 6 of the hottest viral trending physical products selling right now globally.
Return ONLY a valid JSON array with 6 objects in this exact format:
[
  {
    "title": "Catchy Product Name",
    "description": "Persuasive 2-sentence description.",
    "price": "29.99",
    "old_price": "49.99",
    "search_keyword": "simple 2 word English keyword",
    "marketing_post": "Viral TikTok/Instagram ad copy with emojis and #hashtags"
  }
]
"""

def fetch_ai_products():
    if not API_KEY:
        raise ValueError("Missing API Key")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    data = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"response_mime_type": "application/json"}
    }
    req = urllib.request.Request(
        url, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'}
    )
    with urllib.request.urlopen(req, timeout=30) as response:
        result = json.loads(response.read().decode('utf-8'))
        raw_text = result['candidates'][0]['content']['parts'][0]['text']
        clean_text = raw_text.replace("```json", "").replace("```", "").strip()
        return json.loads(clean_text)

backup_pool = [
    {
        "title": "4K Ultra-HD Mini Smart Projector",
        "description": "Turn any wall into a 130-inch home cinema! Built-in WiFi 6, Bluetooth 5.0, and 180-degree rotatable design for bedroom movie nights.",
        "price": "54.99",
        "old_price": "99.99",
        "search_keyword": "mini smart projector",
        "image": "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?auto=format&fit=crop&w=800&q=80",
        "marketing_post": "🍿 Movie nights will never be the same! Turn your ceiling into a 4K cinema with this viral Mini Projector 🔥✨ #TikTokMadeMeBuyIt #HomeCinema #ViralGadgets"
    },
    {
        "title": "Smart LED RGB Sunset Floor Lamp",
        "description": "Create instant golden-hour aesthetics in your room. App-controlled with 16 million colors and music sync mode for content creators.",
        "price": "22.99",
        "old_price": "45.00",
        "search_keyword": "sunset projection lamp",
        "image": "https://images.unsplash.com/photo-1513506003901-1e6a229e2d15?auto=format&fit=crop&w=800&q=80",
        "marketing_post": "🌅 Golden hour vibes 24/7 in your bedroom! This viral RGB Sunset Lamp changes your room's whole aesthetic 😍🔥 #RoomDecor #ViralLights #Aesthetic"
    },
    {
        "title": "Pro Noise-Cancelling Wireless Earbuds",
        "description": "Studio-grade bass with active noise cancellation and LED battery display. Waterproof design with 40 hours of playtime.",
        "price": "29.99",
        "old_price": "65.00",
        "search_keyword": "wireless earbuds anc",
        "image": "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?auto=format&fit=crop&w=800&q=80",
        "marketing_post": "🎧 Block out the world and feel the bass! Why pay $200 when these viral ANC earbuds outperform the big brands? 🔥🎵 #TechFinds #WirelessEarbuds #DealAlert"
    },
    {
        "title": "3-in-1 Foldable Magnetic Wireless Charger",
        "description": "Charge your Phone, Watch, and Earbuds simultaneously! Pocket-sized foldable travel design with fast magnetic alignment.",
        "price": "26.50",
        "old_price": "49.99",
        "search_keyword": "3 in 1 magnetic wireless charger",
        "image": "https://images.unsplash.com/photo-1615526675159-e248c3021d3f?auto=format&fit=crop&w=800&q=80",
        "marketing_post": "⚡ Say goodbye to messy cables forever! This 3-in-1 Foldable Charger powers all your devices at once 📱⌚🎧 #TechHacks #DeskSetup #MustHave"
    },
    {
        "title": "Electric Spin Scrubber Power Cleaner",
        "description": "Clean your bathroom and kitchen in half the time without bending your back! Cordless, waterproof, and comes with 7 replaceable brush heads.",
        "price": "34.99",
        "old_price": "69.99",
        "search_keyword": "electric spin scrubber",
        "image": "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?auto=format&fit=crop&w=800&q=80",
        "marketing_post": "🧼 CleaningTok's #1 obsession! Let this Electric Spin Scrubber do all the hard work for you effortlessly ✨🏠 #CleanTok #HomeHacks #TrendingNow"
    },
    {
        "title": "Smart Posture Corrector & Back Massager",
        "description": "Relieve neck and back pain instantly. Invisible under clothes with smart vibration reminders to keep your spine aligned all day.",
        "price": "19.99",
        "old_price": "39.99",
        "search_keyword": "smart posture corrector",
        "image": "https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?auto=format&fit=crop&w=800&q=80",
        "marketing_post": "💆‍♂️ Fix your posture and melt away back pain in days! The viral smart gadget everyone working from home needs 🔥✅ #HealthHacks #PostureCheck #Wellness"
    }
]

try:
    ai_products = fetch_ai_products()
    final_products = []
    for p in ai_products[:6]:
        kw = urllib.parse.quote(p['search_keyword'])
        seed = random.randint(1, 9999)
        img_prompt = urllib.parse.quote(f"bright commercial studio product photo of {p['search_keyword']} on pure white table")
        p['image'] = f"https://image.pollinations.ai/prompt/{img_prompt}?width=600&height=600&seed={seed}&nologo=true"
        target_url = f"https://www.aliexpress.com/w/wholesale-{kw.replace('%20', '-')}.html?sk={AFFILIATE_KEY}&aff_fsk={AFFILIATE_KEY}&aff_platform=portals-tool"
        p['buy_link'] = f"{AFFILIATE_LINK}?dl_target_url={urllib.parse.quote(target_url)}"
        final_products.append(p)
except Exception as e:
    final_products = []
    for p in backup_pool:
        kw = urllib.parse.quote(p['search_keyword'])
        target_url = f"https://www.aliexpress.com/w/wholesale-{kw.replace('%20', '-')}.html?sk={AFFILIATE_KEY}&aff_fsk={AFFILIATE_KEY}&aff_platform=portals-tool"
        p['buy_link'] = f"{AFFILIATE_LINK}?dl_target_url={urllib.parse.quote(target_url)}"
        final_products.append(p)

with open("products.json", "w", encoding="utf-8") as f:
    json.dump(final_products, f, indent=2)

# Generate Valid XML Auto-Marketing RSS Feed
rss_items = ""
now_str = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
for i, p in enumerate(final_products):
    safe_img_url = p['image'].replace("&", "&amp;")
    rss_items += f"""
    <item>
      <title><![CDATA[🔥 {p['title']} - Only ${p['price']}!]]></title>
      <link>{STORE_URL}</link>
      <guid isPermaLink="false">{datetime.utcnow().strftime('%Y%m%d')}-{i}</guid>
      <pubDate>{now_str}</pubDate>
      <description><![CDATA[{p['marketing_post']} 👉 Shop Here: {STORE_URL}]]></description>
      <enclosure url="{safe_img_url}" length="50000" type="image/jpeg" />
    </item>"""

rss_feed = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
  <channel>
    <title>Trendify AI Viral Store Feed</title>
    <link>{STORE_URL}</link>
    <description>Automated Viral Products and Marketing Feed</description>
    {rss_items}
  </channel>
</rss>"""

with open("feed.xml", "w", encoding="utf-8") as f:
    f.write(rss_feed.strip())

print("Affiliate Links & Feed Updated Successfully!")
