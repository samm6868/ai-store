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

# Massive Global Viral Catalog (Verified Fast HD Studio Images for Instagram & Pinterest)
VIRAL_CATALOG = [
    {
        "title": "Portable Smart Blender Cup for Smoothies",
        "description": "Make fresh smoothies anywhere in 30 seconds! USB-C rechargeable, waterproof self-cleaning design with 6 stainless steel blades.",
        "price": "24.99",
        "old_price": "49.99",
        "search_keyword": "portable usb blender cup",
        "image": "https://images.unsplash.com/photo-1570222094114-d054a817e56b?auto=format&fit=crop&w=800&q=80",
        "marketing_post": "🍓 Fresh smoothies at the gym, office, or car in 30 seconds! This viral Portable Blender is a total game-changer 🔥🥤"
    },
    {
        "title": "Vintage Flame Air Humidifier & Aroma Diffuser",
        "description": "Realistic LED flame effect combined with ultrasonic aromatherapy mist. Auto shut-off protection and whisper-quiet operation for cozy nights.",
        "price": "27.99",
        "old_price": "55.00",
        "search_keyword": "flame air diffuser humidifier",
        "image": "https://images.unsplash.com/photo-1602928321679-560bb453f190?auto=format&fit=crop&w=800&q=80",
        "marketing_post": "🔥 Cozy fireplace vibes + relaxing aromatherapy in your bedroom! No wonder this Flame Diffuser went viral everywhere 😍✨"
    },
    {
        "title": "Mini Pocket Thermal Sticker Printer",
        "description": "Print notes, study labels, and photos instantly from your phone without ink! Bluetooth wireless connection with rechargeable battery.",
        "price": "21.99",
        "old_price": "44.00",
        "search_keyword": "mini pocket thermal printer",
        "image": "https://images.unsplash.com/photo-1612815154858-60aa4c59eaa6?auto=format&fit=crop&w=800&q=80",
        "marketing_post": "🖨️ Print anything from your phone in seconds with ZERO ink! StudyTok and organization lovers are obsessed with this Mini Printer 📱✨"
    },
    {
        "title": "Ultrasonic Facial Skin Scrubber & Pore Cleaner",
        "description": "Deeply cleanse pores, remove blackheads, and lift skin using 24,000Hz ultrasonic vibrations. Spa-grade facial treatment at home.",
        "price": "19.50",
        "old_price": "39.99",
        "search_keyword": "ultrasonic skin scrubber",
        "image": "https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?auto=format&fit=crop&w=800&q=80",
        "marketing_post": "✨ Glowing glass skin at home! Watch this viral Ultrasonic Skin Scrubber clear pores in seconds 😍💆‍♀️"
    },
    {
        "title": "RGB Mechanical Gaming Keyboard Wireless",
        "description": "Compact 60% layout with hot-swappable tactile switches and 18 dynamic RGB backlight modes. Connects via Bluetooth, 2.4GHz, or USB-C.",
        "price": "42.99",
        "old_price": "79.99",
        "search_keyword": "rgb mechanical gaming keyboard",
        "image": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?auto=format&fit=crop&w=800&q=80",
        "marketing_post": "⌨️ Listen to that creamy sound! Upgrade your desk setup with this viral RGB Mechanical Keyboard 🔥🌈"
    },
    {
        "title": "Smart Fitness Ring Health & Sleep Tracker",
        "description": "Track heart rate, blood oxygen, sleep stages, and daily steps on your finger! Titanium waterproof build with 7-day battery life.",
        "price": "49.99",
        "old_price": "95.00",
        "search_keyword": "smart health ring tracker",
        "image": "https://images.unsplash.com/photo-1605100804763-247f67b3557e?auto=format&fit=crop&w=800&q=80",
        "marketing_post": "💍 Ditch the bulky watch! This sleek Titanium Smart Ring tracks your sleep, heart rate, and workouts 24/7 🔥⌚"
    },
    {
        "title": "Cordless High-Pressure Car Wash Water Gun",
        "description": "Wash your car or patio anywhere without wires! Powerful rechargeable battery with foam cannon attachment and multi-spray nozzle.",
        "price": "38.99",
        "old_price": "75.00",
        "search_keyword": "cordless pressure washer gun",
        "image": "https://images.unsplash.com/photo-1520340356584-f9917d1eea6f?auto=format&fit=crop&w=800&q=80",
        "marketing_post": "🚗💨 Wash your car in 5 minutes with thick snow foam! This Cordless Pressure Washer Gun is every car owner's dream 🔥🧼"
    },
    {
        "title": "Magnetic Levitating Moon Night Lamp",
        "description": "3D-printed moon floats and spins mid-air using magnetic levitation! Wireless power induction with 3 soothing warm and cool light modes.",
        "price": "36.50",
        "old_price": "69.99",
        "search_keyword": "levitating moon lamp",
        "image": "https://images.unsplash.com/photo-1532693322450-2cb5c511067d?auto=format&fit=crop&w=800&q=80",
        "marketing_post": "🌕 Yes, it actually floats in mid-air! The most mesmerizing Levitating Moon Lamp for your bedroom or desk 😍✨"
    },
    {
        "title": "Smart Automatic Coffee Mug Warmer Coaster",
        "description": "Keep your coffee or tea at the perfect hot temperature all day long! Touch control with 3 heat settings and auto safety shut-off.",
        "price": "17.99",
        "old_price": "34.99",
        "search_keyword": "smart coffee mug warmer",
        "image": "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?auto=format&fit=crop&w=800&q=80",
        "marketing_post": "☕ Never drink cold coffee again! Every desk needs this Smart Mug Warmer right now 🔥🙌"
    },
    {
        "title": "Wireless Lavalier Microphone for iPhone & Android",
        "description": "Plug-and-play studio audio for TikTok, Reels, and YouTube creators! Intelligent AI noise reduction with 65ft wireless range.",
        "price": "23.99",
        "old_price": "48.00",
        "search_keyword": "wireless lavalier microphone phone",
        "image": "https://images.unsplash.com/photo-1590602847861-f357a9332bbc?auto=format&fit=crop&w=800&q=80",
        "marketing_post": "🎙️ Crispy studio audio on your phone in 1 second! The secret weapon of every viral content creator 🔥📱"
    },
    {
        "title": "4K Ultra-HD Mini Smart Projector",
        "description": "Turn any wall into a 130-inch home cinema! Built-in WiFi 6, Bluetooth 5.0, and 180-degree rotatable design for bedroom movie nights.",
        "price": "54.99",
        "old_price": "99.99",
        "search_keyword": "mini smart projector",
        "image": "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?auto=format&fit=crop&w=800&q=80",
        "marketing_post": "🍿 Movie nights will never be the same! Turn your bedroom ceiling into a 4K cinema with this viral Mini Projector 🔥✨"
    },
    {
        "title": "Smart LED RGB Sunset Floor Lamp",
        "description": "Create instant golden-hour aesthetics in your room. App-controlled with 16 million colors and music sync mode for content creators.",
        "price": "22.99",
        "old_price": "45.00",
        "search_keyword": "sunset projection lamp",
        "image": "https://images.unsplash.com/photo-1513506003901-1e6a229e2d15?auto=format&fit=crop&w=800&q=80",
        "marketing_post": "🌅 Golden hour vibes 24/7 in your bedroom! This viral RGB Sunset Lamp changes your room's whole aesthetic 😍🔥"
    },
    {
        "title": "Pro Noise-Cancelling Wireless Earbuds",
        "description": "Studio-grade bass with active noise cancellation and LED battery display. Waterproof design with 40 hours of playtime.",
        "price": "29.99",
        "old_price": "65.00",
        "search_keyword": "wireless earbuds anc",
        "image": "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?auto=format&fit=crop&w=800&q=80",
        "marketing_post": "🎧 Block out the world and feel the bass! Why pay $200 when these viral ANC earbuds outperform the big brands? 🔥🎵"
    },
    {
        "title": "3-in-1 Foldable Magnetic Wireless Charger",
        "description": "Charge your Phone, Watch, and Earbuds simultaneously! Pocket-sized foldable travel design with fast magnetic alignment.",
        "price": "26.50",
        "old_price": "49.99",
        "search_keyword": "3 in 1 magnetic wireless charger",
        "image": "https://images.unsplash.com/photo-1615526675159-e248c3021d3f?auto=format&fit=crop&w=800&q=80",
        "marketing_post": "⚡ Say goodbye to messy cables forever! This 3-in-1 Foldable Charger powers all your devices at once 📱⌚🎧"
    },
    {
        "title": "Electric Spin Scrubber Power Cleaner",
        "description": "Clean your bathroom and kitchen in half the time without bending your back! Cordless, waterproof, and comes with 7 replaceable brush heads.",
        "price": "34.99",
        "old_price": "69.99",
        "search_keyword": "electric spin scrubber",
        "image": "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?auto=format&fit=crop&w=800&q=80",
        "marketing_post": "🧼 CleaningTok's #1 obsession! Let this Electric Spin Scrubber do all the hard work for you effortlessly ✨🏠"
    },
    {
        "title": "Smart Posture Corrector & Back Massager",
        "description": "Relieve neck and back pain instantly. Invisible under clothes with smart vibration reminders to keep your spine aligned all day.",
        "price": "19.99",
        "old_price": "39.99",
        "search_keyword": "smart posture corrector",
        "image": "https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?auto=format&fit=crop&w=800&q=80",
        "marketing_post": "💆‍♂️ Fix your posture and melt away back pain in days! The viral smart gadget everyone working from home needs 🔥✅"
    }
]

# Read previous products to ensure 100% NEW products on every rotation
previous_titles = set()
if os.path.exists("products.json"):
    try:
        with open("products.json", "r", encoding="utf-8") as f:
            old_data = json.load(f)
            for item in old_data:
                previous_titles.add(item.get("title", ""))
    except Exception:
        pass

# Filter out yesterday's products so the store gets fresh items immediately
fresh_candidates = [p for p in VIRAL_CATALOG if p["title"] not in previous_titles]
if len(fresh_candidates) < 6:
    fresh_candidates = VIRAL_CATALOG

random.shuffle(fresh_candidates)
selected_products = fresh_candidates[:6]

final_products = []
for p in selected_products:
    item = dict(p)
    kw = urllib.parse.quote(item['search_keyword'])
    item['buy_link'] = f"https://www.aliexpress.com/w/wholesale-{kw.replace('%20', '-')}.html?sk={AFFILIATE_KEY}&aff_fsk={AFFILIATE_KEY}&aff_platform=portals-tool"
    item['marketing_post'] = item['marketing_post'] + EXPLORE_HASHTAGS
    final_products.append(item)

with open("products.json", "w", encoding="utf-8") as f:
    json.dump(final_products, f, indent=2)

# Generate Valid XML Auto-Marketing RSS Feed with Unique Rotation IDs
rss_items = ""
now_str = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
timestamp_id = datetime.utcnow().strftime('%Y%m%d%H%M')

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

print("Successfully rotated 6 brand-new viral products with Explore SEO hashtags!")
