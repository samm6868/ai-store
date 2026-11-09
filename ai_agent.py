import os
import json
import urllib.request
import urllib.parse
import random
from datetime import datetime

raw_key = os.environ.get("GEMINI_API_KEY", "")
API_KEY = raw_key.strip()
AFFILIATE_KEY = "_c4Lh9g5v"
STORE_URL = "https://samm6868.github.io/ai-store"

# Mega Viral SEO Hashtags for 0-Follower Explore Boost
EXPLORE_HASHTAGS = (
    "\n\n🛍️ Tap the LINK IN BIO to order yours with 40% OFF + Free Worldwide Shipping! 🌍✨\n.\n.\n"
    "#TikTokMadeMeBuyIt #AmazonFinds #ViralGadgets #CoolTech #SmartHome #TrendingProducts "
    "#GadgetLover #MustHave #GiftIdeas #RoomDecor #AestheticFinds #TechHacks #OnlineShopping "
    "#DealAlert #ViralProducts #BestSellers #HomeGadgets #LifeHacks"
)

# Verified Ultra-Fast HD Commercial Studio Photo Bank mapped by Niche (100% Instagram & Pinterest Safe)
STUDIO_IMAGE_BANK = {
    "projector": "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?auto=format&fit=crop&w=800&q=80",
    "lamp": "https://images.unsplash.com/photo-1513506003901-1e6a229e2d15?auto=format&fit=crop&w=800&q=80",
    "lighting": "https://images.unsplash.com/photo-1532693322450-2cb5c511067d?auto=format&fit=crop&w=800&q=80",
    "audio": "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?auto=format&fit=crop&w=800&q=80",
    "headphones": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=800&q=80",
    "speaker": "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?auto=format&fit=crop&w=800&q=80",
    "charger": "https://images.unsplash.com/photo-1615526675159-e248c3021d3f?auto=format&fit=crop&w=800&q=80",
    "phone": "https://images.unsplash.com/photo-1586816879360-004f5b0c51e3?auto=format&fit=crop&w=800&q=80",
    "cleaning": "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?auto=format&fit=crop&w=800&q=80",
    "wellness": "https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?auto=format&fit=crop&w=800&q=80",
    "kitchen": "https://images.unsplash.com/photo-1570222094114-d054a817e56b?auto=format&fit=crop&w=800&q=80",
    "coffee": "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?auto=format&fit=crop&w=800&q=80",
    "aroma": "https://images.unsplash.com/photo-1602928321679-560bb453f190?auto=format&fit=crop&w=800&q=80",
    "printer": "https://images.unsplash.com/photo-1612815154858-60aa4c59eaa6?auto=format&fit=crop&w=800&q=80",
    "beauty": "https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?auto=format&fit=crop&w=800&q=80",
    "skincare": "https://images.unsplash.com/photo-1556228720-195a672e8a03?auto=format&fit=crop&w=800&q=80",
    "gaming": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?auto=format&fit=crop&w=800&q=80",
    "smartwatch": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=800&q=80",
    "ring": "https://images.unsplash.com/photo-1605100804763-247f67b3557e?auto=format&fit=crop&w=800&q=80",
    "car": "https://images.unsplash.com/photo-1520340356584-f9917d1eea6f?auto=format&fit=crop&w=800&q=80",
    "microphone": "https://images.unsplash.com/photo-1590602847861-f357a9332bbc?auto=format&fit=crop&w=800&q=80",
    "camera": "https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?auto=format&fit=crop&w=800&q=80",
    "drone": "https://images.unsplash.com/photo-1507582020474-9a35b7d455d9?auto=format&fit=crop&w=800&q=80",
    "fitness": "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?auto=format&fit=crop&w=800&q=80",
    "backpack": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?auto=format&fit=crop&w=800&q=80",
    "sunglasses": "https://images.unsplash.com/photo-1511499767150-a48a237f0083?auto=format&fit=crop&w=800&q=80",
    "pet": "https://images.unsplash.com/photo-1541781774459-bb2af2f05b55?auto=format&fit=crop&w=800&q=80",
    "watch": "https://images.unsplash.com/photo-1524805444758-089113d48a6d?auto=format&fit=crop&w=800&q=80"
}

# Read previous products so AI never repeats yesterday's items
previous_titles = set()
if os.path.exists("products.json"):
    try:
        with open("products.json", "r", encoding="utf-8") as f:
            old_data = json.load(f)
            for item in old_data:
                previous_titles.add(item.get("title", ""))
    except Exception:
        pass

categories_list = ", ".join(STUDIO_IMAGE_BANK.keys())
avoid_list = ", ".join(previous_titles) if previous_titles else "None"

prompt = f"""
Act as an elite Global E-Commerce Trend Hunter & Viral TikTok/Instagram Marketer.
Discover 6 brand-new, hottest viral physical products trending right now globally on TikTok Shop, Amazon Movers & Shakers, and AliExpress.
DO NOT repeat any of these previous titles: [{avoid_list}].

For each product:
1. 'title': Catchy, high-converting Shopify-style product name.
2. 'description': Persuasive 2-sentence sales description highlighting benefits.
3. 'price': Smart impulse-buy price between 17.99 and 59.99.
4. 'old_price': Higher original price (approx 40-50% higher).
5. 'search_keyword': Simple 2 to 3 English words to find this exact item on AliExpress.
6. 'category': Pick the single closest matching visual category from this exact list: [{categories_list}] (use a different category for each of the 6 products).
7. 'marketing_post': Exciting viral Instagram/TikTok ad hook with emojis.

Return ONLY a valid JSON array of 6 objects.
"""

def fetch_live_ai_trends():
    if not API_KEY:
        raise ValueError("Missing API Key")
    models = ["gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-flash-latest"]
    for model in models:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={API_KEY}"
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
                parsed = json.loads(clean_text)
                if isinstance(parsed, list) and len(parsed) >= 6:
                    print(f"Live AI Trends generated using {model}!")
                    return parsed[:6]
        except Exception as err:
            print(f"Model {model} skipped: {err}")
    raise RuntimeError("All AI models busy, switching to Dynamic Trend Generator")

# Dynamic Fallback Pool (18+ products) in case API quota is temporarily reached
DYNAMIC_POOL = [
    {"title": "Smart WiFi Galaxy Starry Sky Projector", "description": "Voice-controlled nebula and laser star projector that turns any bedroom into a soothing cosmic oasis.", "price": "31.99", "old_price": "59.99", "search_keyword": "smart galaxy projector", "category": "projector", "marketing_post": "🌌 Sleep under the stars every single night! This voice-controlled Galaxy Projector is pure magic 🔥✨"},
    {"title": "Cryo-Glow Ultrasonic Ice Facial Roller & Scrubber", "description": "Depuff, tighten pores, and sculpt your jawline instantly with sonic vibrations and cooling therapy.", "price": "21.50", "old_price": "42.00", "search_keyword": "ultrasonic facial pore cleaner", "category": "beauty", "marketing_post": "💆‍♀️ Instant glass skin in 2 minutes a day! BeautyTok cannot stop talking about this sonic facial tool 😍✨"},
    {"title": "Magnetic MagSafe PowerBank 10000mAh Ultra-Slim", "description": "Snaps magnetically to the back of your phone for effortless wireless fast charging on the go without cables.", "price": "28.99", "old_price": "54.00", "search_keyword": "magnetic wireless power bank", "category": "charger", "marketing_post": "🔋 Snap & charge anywhere with zero cables! The sleekest magnetic power bank you'll ever own 📱⚡"},
    {"title": "Mini Folding 4K HD Dual-Camera Pocket Drone", "description": "Capture breathtaking aerial videos with one-key takeoff, altitude hold, and gesture selfie mode. Fits right in your pocket!", "price": "46.99", "old_price": "89.99", "search_keyword": "mini 4k foldable drone", "category": "drone", "marketing_post": "🚁 A 4K camera drone that folds into your pocket?! Wait until you see the footage this captures 🔥📸"},
    {"title": "Smart Titanium Health & Sleep Tracking Ring", "description": "Monitor sleep quality, heart rate, blood oxygen, and stress 24/7 in a featherlight waterproof titanium ring.", "price": "49.99", "old_price": "99.00", "search_keyword": "smart health sleep ring", "category": "ring", "marketing_post": "💍 The future of fitness tracking fits right on your finger! No bulky screen, just pure smart tech 🔥🙌"},
    {"title": "Cordless High-Pressure Foam Car Washer Gun", "description": "Blast away dirt and cover your car in thick snow foam anywhere using a bucket or hose—no outlets needed!", "price": "37.99", "old_price": "74.00", "search_keyword": "cordless car pressure washer", "category": "car", "marketing_post": "🚗🧼 Save hundreds on car washes! This Cordless Foam Blaster makes washing your car so satisfying 🔥💦"},
    {"title": "Retro Pixel Art Bluetooth Speaker & Smart Alarm", "description": "Customizable LED pixel screen with booming bass, retro mini-games, weather display, and bedside alarm clock.", "price": "34.50", "old_price": "65.00", "search_keyword": "pixel art bluetooth speaker", "category": "speaker", "marketing_post": "👾 The coolest desk gadget of the year! Retro Pixel Art Display + booming Bluetooth speaker in one 🔥🎵"},
    {"title": "Anti-Theft Waterproof USB Charging Laptop Backpack", "description": "Hidden zippers, built-in external USB charging port, and ergonomic shockproof compartments for travel and work.", "price": "33.99", "old_price": "68.00", "search_keyword": "usb anti theft backpack", "category": "backpack", "marketing_post": "🎒 Charge your phone while walking! This waterproof Anti-Theft Smart Backpack is built for modern travelers 🌍⚡"},
    {"title": "Interactive Self-Rolling Laser Cat & Dog Chaser Ball", "description": "Motion-activated smart pet toy that automatically avoids obstacles and keeps indoor pets active for hours.", "price": "16.99", "old_price": "32.99", "search_keyword": "smart interactive pet ball", "category": "pet", "marketing_post": "🐾 Your pet will never be bored again! Watch this smart obstacle-avoiding ball entertain them for hours 😍🐶"},
    {"title": "Pocket Bluetooth Inkless Thermal Label & Photo Printer", "description": "Print study notes, to-do lists, stickers, and memories straight from your smartphone without ever buying ink.", "price": "22.99", "old_price": "45.00", "search_keyword": "pocket thermal printer bluetooth", "category": "printer", "marketing_post": "🖨️ Zero ink, infinite stickers! Print notes and photos straight from your phone in seconds 📱✨"},
    {"title": "Levitating 3D Magnetic Floating Moon Lamp", "description": "Spins 360 degrees floating in mid-air via magnetic induction with 3 warm and cool ambient touch light modes.", "price": "36.99", "old_price": "72.00", "search_keyword": "levitating moon lamp magnetic", "category": "lighting", "marketing_post": "🌕 Everyone who visits my room asks where I got this floating Moon Lamp! Pure bedroom magic 😍✨"},
    {"title": " Volcanic Flame Ultrasonic Essential Oil Diffuser", "description": "Creates a realistic dancing fireplace flame mist that humidifies dry air and fills your room with luxury fragrance.", "price": "26.99", "old_price": "52.00", "search_keyword": "volcano flame aroma diffuser", "category": "aroma", "marketing_post": "🔥 Touch-safe mist flames + relaxing essential oils! The #1 cozy room upgrade on TikTok right now 😍✨"}
]

try:
    raw_products = fetch_live_ai_trends()
except Exception:
    fresh_pool = [p for p in DYNAMIC_POOL if p["title"] not in previous_titles]
    if len(fresh_pool) < 6:
        fresh_pool = DYNAMIC_POOL
    random.shuffle(fresh_pool)
    raw_products = fresh_pool[:6]

used_images = set()
all_bank_images = list(STUDIO_IMAGE_BANK.values())
final_products = []

for p in raw_products:
    item = dict(p)
    cat = str(item.get("category", "")).lower().strip()
    chosen_img = STUDIO_IMAGE_BANK.get(cat)
    if not chosen_img or chosen_img in used_images:
        available = [img for img in all_bank_images if img not in used_images]
        chosen_img = random.choice(available if available else all_bank_images)
    used_images.add(chosen_img)
    
    item["image"] = chosen_img
    kw = urllib.parse.quote(item.get("search_keyword", item["title"]))
    item["buy_link"] = f"https://www.aliexpress.com/w/wholesale-{kw.replace('%20', '-')}.html?sk={AFFILIATE_KEY}&aff_fsk={AFFILIATE_KEY}&aff_platform=portals-tool"
    item["marketing_post"] = item.get("marketing_post", f"🔥 Check out {item['title']}!") + EXPLORE_HASHTAGS
    final_products.append(item)

with open("products.json", "w", encoding="utf-8") as f:
    json.dump(final_products, f, indent=2)

# Generate Valid XML Auto-Marketing RSS Feed
rss_items = ""
now_str = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
timestamp_id = datetime.utcnow().strftime('%Y%m%d%H%M%S')

for i, p in enumerate(final_products):
    safe_img_url = p['image'].replace("&", "&amp;")
    unique_id = f"{timestamp_id}-{i}"
    rss_items += f"""
    <item>
      <title><![CDATA[🔥 {p['title']} - Only ${p['price']}! (40% OFF)]]></title>
      <link>{STORE_URL}</link>
      <guid isPermaLink="false">{unique_id}</guid>
      <pubDate>{now_str}</pubDate>
      <description><![CDATA[{p['marketing_post']} 👉 Shop Link in Bio or at: {STORE_URL}]]></description>
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

print("Hybrid Live AI Trend Hunter executed successfully!")
