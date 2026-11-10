import os
import re
import json
import random
import urllib.parse
import urllib.request
from datetime import datetime

# ==========================================
# CONFIGURATION & AFFILIATE SETTINGS
# ==========================================
AFFILIATE_KEY = "_c4Lh9g5v"
STORE_URL = "https://samm6868.github.io/ai-store"
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "").strip()

EXPLORE_HASHTAGS = (
    "#tiktokmademebuyit #amazonfinds #viralgadgets #cooltech "
    "#smartliving #musthaves #trendingnow #gadgetlover #techfinds "
    "#homedecor #lifehacks #giftideas #shopsmall #onlinefinds "
    "#dailydeals #futuretech #innovative #bestfinds #shoppingonline #explorepage"
)

# 24 Verified 1200px HD Commercial Product Images & Curated Viral Catalog
VIRAL_PRODUCT_VAULT = [
    {
        "title": "Mini Wireless Portable Thermal Printer",
        "price": "19.99",
        "old_price": "39.99",
        "category": "Electronics",
        "badge": "TIKTOK VIRAL",
        "rating": "4.9",
        "reviews": "3,420",
        "image": "https://images.unsplash.com/photo-1612815154858-60aa4c59eaa6?w=1200&q=80",
        "search_keyword": "mini wireless thermal pocket printer",
        "description": "Print notes, labels, and photos instantly from your smartphone without a single drop of ink! Pocket-sized and Bluetooth-ready."
    },
    {
        "title": "Crystal Galaxy Levitating Moon Lamp",
        "price": "24.50",
        "old_price": "49.00",
        "category": "Home Decor",
        "badge": "BEST SELLER",
        "rating": "4.8",
        "reviews": "2,150",
        "image": "https://images.unsplash.com/photo-1513506003901-1e6a229e2d15?w=1200&q=80",
        "search_keyword": "3d crystal galaxy moon night lamp",
        "description": "Transform your bedroom into a cosmic oasis with 16 mesmerizing RGB colors and touch-control ambiance."
    },
    {
        "title": "Ultrasonic Facial Pore Cleanser Pro",
        "price": "18.75",
        "old_price": "37.50",
        "category": "Beauty & Health",
        "badge": "TRENDING",
        "rating": "4.9",
        "reviews": "1,890",
        "image": "https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?w=1200&q=80",
        "search_keyword": "ultrasonic skin scrubber pore cleanser",
        "description": "Deep-cleanse pores, gently exfoliate, and boost glow in 5 minutes a day using high-frequency micro-vibrations."
    },
    {
        "title": "Portable USB Rechargeable Blender Bottle",
        "price": "21.99",
        "old_price": "44.00",
        "category": "Kitchen Gadgets",
        "badge": "50% OFF",
        "rating": "4.8",
        "reviews": "4,110",
        "image": "https://images.unsplash.com/photo-1570222094114-d054a817e56b?w=1200&q=80",
        "search_keyword": "portable usb personal smoothie blender",
        "description": "Blend fresh smoothies, protein shakes, and crushed ice anywhere in 30 seconds with 6 stainless steel blades."
    },
    {
        "title": "3-in-1 Foldable Magnetic Wireless Charger",
        "price": "26.99",
        "old_price": "53.99",
        "category": "Smart Living",
        "badge": "HOT DEAL",
        "rating": "4.9",
        "reviews": "2,780",
        "image": "https://images.unsplash.com/photo-1558002038-1055907df827?w=1200&q=80",
        "search_keyword": "3 in 1 foldable magnetic wireless charger",
        "description": "Charge your phone, smartwatch, and earbuds simultaneously on one sleek travel-friendly magnetic pad."
    },
    {
        "title": "Smart Cordless Tire Inflator Air Pump",
        "price": "29.99",
        "old_price": "59.99",
        "category": "Auto Accessories",
        "badge": "MUST HAVE",
        "rating": "4.9",
        "reviews": "5,040",
        "image": "https://images.unsplash.com/photo-1544829099-b9a0c07fad1a?w=1200&q=80",
        "search_keyword": "portable cordless digital car tire inflator",
        "description": "Inflate car, bike, and sports tires in seconds with auto shut-off digital pressure control and built-in LED flashlight."
    },
    {
        "title": "TWS Active Noise Cancelling Gaming Earbuds",
        "price": "22.49",
        "old_price": "45.00",
        "category": "Audio & Music",
        "badge": "TOP RATED",
        "rating": "4.9",
        "reviews": "3,890",
        "image": "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=1200&q=80",
        "search_keyword": "wireless anc bluetooth gaming earbuds",
        "description": "Experience studio-grade deep bass and zero-latency wireless audio with futuristic LED charging case."
    },
    {
        "title": "Deep Tissue Percussion Mini Massage Gun",
        "price": "27.99",
        "old_price": "55.99",
        "category": "Fitness & Massage",
        "badge": "FLASH SALE",
        "rating": "4.8",
        "reviews": "2,640",
        "image": "https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=1200&q=80",
        "search_keyword": "mini pocket deep tissue massage gun",
        "description": "Relieve muscle tension and post-workout soreness anywhere with ultra-quiet high-torque percussion therapy."
    },
    {
        "title": "Sunset Projection LED Aesthetic Floor Lamp",
        "price": "15.99",
        "old_price": "31.99",
        "category": "Smart Lighting",
        "badge": "VIRAL HIT",
        "rating": "4.9",
        "reviews": "6,120",
        "image": "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=1200&q=80",
        "search_keyword": "sunset projection lamp 16 colors",
        "description": "Create golden-hour studio lighting in any room with 180-degree rotation and app-controlled color presets."
    },
    {
        "title": "Portable Electric Espresso Coffee Maker",
        "price": "32.50",
        "old_price": "65.00",
        "category": "Coffee & Kitchen",
        "badge": "NEW DROP",
        "rating": "4.9",
        "reviews": "1,950",
        "image": "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=1200&q=80",
        "search_keyword": "portable electric travel espresso maker",
        "description": "Brew rich, crema-topped espresso on the go using capsules or ground coffee with one-button USB heating."
    },
    {
        "title": "Studio Wireless Over-Ear ANC Headphones",
        "price": "28.99",
        "old_price": "57.99",
        "category": "Audio & Music",
        "badge": "BEST VALUE",
        "rating": "4.9",
        "reviews": "4,310",
        "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=1200&q=80",
        "search_keyword": "wireless active noise cancelling over ear headphones",
        "description": "Immerse yourself in pure 3D surround sound with plush memory-foam earcups and 40-hour battery life."
    },
    {
        "title": "Auto Face Tracking Smart Tripod Gimbal",
        "price": "25.99",
        "old_price": "51.99",
        "category": "Content Creation",
        "badge": "CREATOR PICK",
        "rating": "4.9",
        "reviews": "2,470",
        "image": "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=1200&q=80",
        "search_keyword": "360 auto face tracking phone holder tripod",
        "description": "Hands-free 360-degree AI motion tracking camera stand—no app required, perfect for Reels, TikTok, and video calls."
    },
    {
        "title": "Ultra-Slim AMOLED Fitness Smartwatch Pro",
        "price": "31.99",
        "old_price": "63.99",
        "category": "Smartwatches",
        "badge": "HOT TREND",
        "rating": "4.9",
        "reviews": "5,280",
        "image": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=1200&q=80",
        "search_keyword": "amoled waterproof fitness smartwatch heart rate",
        "description": "Track heart rate, sleep, and 100+ workouts on a crystal-clear bezel-less display with 10-day battery life."
    },
    {
        "title": "Magnetic Sport Strap Health Tracker Watch",
        "price": "27.50",
        "old_price": "55.00",
        "category": "Smartwatches",
        "badge": "50% OFF",
        "rating": "4.8",
        "reviews": "3,190",
        "image": "https://images.unsplash.com/photo-1546868871-7041f2a55e12?w=1200&q=80",
        "search_keyword": "smart watch bluetooth call fitness tracker",
        "description": "Answer calls directly from your wrist with instant message alerts, blood oxygen monitoring, and IP68 waterproofing."
    },
    {
        "title": "Ultrasonic Flame Aroma Diffuser & Humidifier",
        "price": "20.99",
        "old_price": "41.99",
        "category": "Home Decor",
        "badge": "TIKTOK VIRAL",
        "rating": "4.9",
        "reviews": "4,750",
        "image": "https://images.unsplash.com/photo-1585386959984-a4155224a1ad?w=1200&q=80",
        "search_keyword": "flame air diffuser humidifier essential oil",
        "description": "Combines soothing cool mist aromatherapy with a realistic LED fireplace flame effect for ultimate relaxation."
    },
    {
        "title": "Retro Instant Print Digital Pocket Camera",
        "price": "29.50",
        "old_price": "59.00",
        "category": "Content Creation",
        "badge": "GIFT IDEA",
        "rating": "4.9",
        "reviews": "2,840",
        "image": "https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=1200&q=80",
        "search_keyword": "mini retro digital instant print camera",
        "description": "Snap vintage-style HD photos and print memories in seconds—compact, rechargeable, and loved by creators."
    },
    {
        "title": "Pro Spatial Audio Touch-Control Earphones",
        "price": "19.50",
        "old_price": "39.00",
        "category": "Audio & Music",
        "badge": "BEST SELLER",
        "rating": "4.8",
        "reviews": "6,430",
        "image": "https://images.unsplash.com/photo-1572569511254-d8f925fe2cbb?w=1200&q=80",
        "search_keyword": "pro wireless bluetooth touch earbuds charging case",
        "description": "Crystal-clear calls, smart touch sensors, and instant pop-up pairing in an ultra-compact pocket charging case."
    },
    {
        "title": "Ergonomic Ultra-Light Wireless Gaming Mouse",
        "price": "23.99",
        "old_price": "47.99",
        "category": "Electronics",
        "badge": "PRO GAMING",
        "rating": "4.9",
        "reviews": "3,620",
        "image": "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=1200&q=80",
        "search_keyword": "lightweight wireless gaming mouse rechargeable rgb",
        "description": "Glide effortlessly with precision optical tracking, silent clicks, and dual-mode Bluetooth + 2.4GHz wireless speed."
    },
    {
        "title": "Hot-Swappable RGB Mechanical Gaming Keyboard",
        "price": "34.50",
        "old_price": "69.00",
        "category": "Electronics",
        "badge": "FLASH SALE",
        "rating": "4.9",
        "reviews": "4,910",
        "image": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=1200&q=80",
        "search_keyword": "60 percent rgb wireless mechanical keyboard",
        "description": "Compact 60% layout with customizable rainbow RGB backlighting and satisfying tactile mechanical switches."
    },
    {
        "title": "Breathable Ultra-Cushion Running Sneakers",
        "price": "33.99",
        "old_price": "67.99",
        "category": "Fitness & Lifestyle",
        "badge": "TRENDING",
        "rating": "4.8",
        "reviews": "5,540",
        "image": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=1200&q=80",
        "search_keyword": "lightweight breathable mesh running sneakers",
        "description": "Engineered with cloud-soft shock absorption and breathable knit mesh for all-day walking and gym comfort."
    },
    {
        "title": "Anti-Theft Waterproof USB Travel Backpack",
        "price": "28.50",
        "old_price": "57.00",
        "category": "Smart Living",
        "badge": "TRAVEL MUST",
        "rating": "4.9",
        "reviews": "4,180",
        "image": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=1200&q=80",
        "search_keyword": "anti theft waterproof laptop backpack usb charging",
        "description": "Keep your laptop and gear safe with hidden zippers, water-repellent fabric, and built-in external USB charging port."
    },
    {
        "title": "UV400 Polarized Retro Designer Sunglasses",
        "price": "16.99",
        "old_price": "33.99",
        "category": "Fashion & Style",
        "badge": "SUMMER HIT",
        "rating": "4.9",
        "reviews": "7,120",
        "image": "https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=1200&q=80",
        "search_keyword": "uv400 polarized vintage sunglasses unisex",
        "description": "Block 100% of glare and harmful UV rays with lightweight scratch-resistant lenses and timeless vintage frames."
    },
    {
        "title": "Smart LED Temperature Display Insulated Flask",
        "price": "17.99",
        "old_price": "35.99",
        "category": "Kitchen Gadgets",
        "badge": "SMART GADGET",
        "rating": "4.9",
        "reviews": "8,340",
        "image": "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=1200&q=80",
        "search_keyword": "smart led temperature display vacuum thermos bottle",
        "description": "Touch the waterproof LED cap to check your drink's exact temperature! Keeps beverages ice-cold or piping hot for 24 hours."
    },
    {
        "title": "Hi-Fi Bass Foldable Wireless Studio Headset",
        "price": "24.99",
        "old_price": "49.99",
        "category": "Audio & Music",
        "badge": "TOP DEAL",
        "rating": "4.8",
        "reviews": "3,760",
        "image": "https://images.unsplash.com/photo-1583394838336-acd977736f90?w=1200&q=80",
        "search_keyword": "foldable wireless bluetooth stereo bass headphones",
        "description": "Fold-and-go portability meets punchy stereo bass and built-in HD mic for travel, study, and workouts."
    }
]


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def load_multi_day_history():
    history = []
    # 1. Read multi-day history embedded in feed.xml
    try:
        if os.path.exists("feed.xml"):
            with open("feed.xml", "r", encoding="utf-8") as f:
                content = f.read()
                match = re.search(r"<!-- HISTORY: (\[.*?\]) -->", content)
                if match:
                    history.extend(json.loads(match.group(1)))
    except Exception:
        pass

    # 2. Read current products.json so we never repeat currently displayed items
    try:
        if os.path.exists("products.json"):
            with open("products.json", "r", encoding="utf-8") as f:
                old_data = json.load(f)
                for item in old_data:
                    t = item.get("title", "")
                    if t and t not in history:
                        history.append(t)
    except Exception:
        pass

    # Keep the last 18 shown products blocked (3 full days of 6 products)
    return history[-18:]


def build_daily_catalog():
    recent_history = load_multi_day_history()
    print(f"📚 Multi-day memory loaded ({len(recent_history)} recent products excluded from repeat).")

    # Filter vault for products NOT shown in the last 3 cycles (18 products)
    available_pool = [p for p in VIRAL_PRODUCT_VAULT if p["title"] not in recent_history]

    # If fewer than 6 remain, reset oldest history while still blocking the last 6 shown
    if len(available_pool) < 6:
        last_six = recent_history[-6:] if len(recent_history) >= 6 else []
        available_pool = [p for p in VIRAL_PRODUCT_VAULT if p["title"] not in last_six]

    random.shuffle(available_pool)
    selected_items = available_pool[:6]

    final_products = []
    for item in selected_items:
        kw = urllib.parse.quote_plus(item.get("search_keyword", item["title"]))
        buy_link = (
            f"https://www.aliexpress.com/w/wholesale-{kw}.html"
            f"?sk={AFFILIATE_KEY}&aff_fsk={AFFILIATE_KEY}&aff_platform=portals-tool"
        )

        final_products.append({
            "title": item["title"],
            "price": str(item["price"]).replace("$", ""),
            "old_price": str(item["old_price"]).replace("$", ""),
            "category": item["category"],
            "badge": item.get("badge", "VIRAL DEAL"),
            "rating": str(item.get("rating", "4.9")),
            "reviews": str(item.get("reviews", "2,450")),
            "image": item["image"],
            "buy_link": buy_link,
            "description": item["description"]
        })

    new_history = (recent_history + [p["title"] for p in final_products])[-18:]
    return final_products, new_history


def generate_store_files():
    products, updated_history = build_daily_catalog()

    with open("products.json", "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)

    now_rfc = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
    history_json = json.dumps(updated_history)

    rss_items = []
    for i, p in enumerate(products):
        safe_img_url = p["image"].replace("&", "&amp;")
        safe_title = (
            p["title"]
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
        )
        safe_desc = (
            p["description"]
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
        )

        prod_slug = slugify(p["title"])
        prod_page_filename = f"product-{i}.html"
        prod_page_url = f"{STORE_URL}/{prod_page_filename}?item={prod_slug}"
        target_store_url = f"{STORE_URL}/#product-{i}"

        # Dedicated Open Graph product landing card (with 1200px HD preview)
        product_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{safe_title} - ${p['price']} | Trendify AI</title>
    <meta name="description" content="{safe_desc}">
    <link rel="canonical" href="{prod_page_url}" />
    <meta property="og:title" content="🔥 {safe_title} - Only ${p['price']} (Was ${p['old_price']})" />
    <meta property="og:description" content="{safe_desc} 🚚 Free Worldwide Shipping!" />
    <meta property="og:image" content="{safe_img_url}" />
    <meta property="og:type" content="website" />
    <meta property="og:url" content="{prod_page_url}" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="🔥 {safe_title} - Only ${p['price']} (Was ${p['old_price']})" />
    <meta name="twitter:description" content="{safe_desc} 🚚 Free Worldwide Shipping!" />
    <meta name="twitter:image" content="{safe_img_url}" />
    <script>window.location.replace("{target_store_url}");</script>
</head>
<body style="font-family:sans-serif;text-align:center;padding:40px;">
    <p>Redirecting to <strong>{safe_title}</strong>...</p>
    <p><a href="{target_store_url}">Click here if not redirected automatically</a></p>
</body>
</html>"""

        with open(prod_page_filename, "w", encoding="utf-8") as pf:
            pf.write(product_html)

        caption = (
            f"🔥 {safe_title} — Now Only ${p['price']} (Was ${p['old_price']})! "
            f"✨ {safe_desc} "
            f"🛒 Shop Link in Bio or visit: {STORE_URL} "
            f"{EXPLORE_HASHTAGS}"
        )

        # Unique slug-based GUID prevents duplicate posting of the same product
        rss_items.append(f"""    <item>
      <title>🔥 {safe_title} - Only ${p['price']} (50% OFF!)</title>
      <link>{prod_page_url}</link>
      <guid isPermaLink="false">trendify-item-{prod_slug}</guid>
      <pubDate>{now_rfc}</pubDate>
      <description><![CDATA[<img src="{p['image']}" /><br/>{caption}]]></description>
      <enclosure url="{safe_img_url}" length="180000" type="image/jpeg" />
      <media:content url="{safe_img_url}" medium="image" type="image/jpeg" />
    </item>""")

    rss_xml = f"""<?xml version="1.0" encoding="UTF-8" ?>
<!-- HISTORY: {history_json} -->
<rss version="2.0" xmlns:media="http://search.yahoo.com/mrss/">
  <channel>
    <title>Trendify AI | Global Viral Store</title>
    <link>{STORE_URL}</link>
    <description>Daily AI-Curated Viral Trending Products &amp; Exclusive Flash Deals</description>
    <language>en-us</language>
    <lastBuildDate>{now_rfc}</lastBuildDate>
{chr(10).join(rss_items)}
  </channel>
</rss>"""

    with open("feed.xml", "w", encoding="utf-8") as f:
        f.write(rss_xml)

    print("✅ Fresh non-repeating products generated with multi-day history memory!")


if __name__ == "__main__":
    generate_store_files()
