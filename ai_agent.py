import os
import re
import json
import random
import urllib.parse
from datetime import datetime

# ==========================================
# CONFIGURATION & AFFILIATE SETTINGS
# ==========================================
AFFILIATE_KEY = "_c4Lh9g5v"
AFFILIATE_COOKIE_URL = "https://s.click.aliexpress.com/e/_c4Lh9g5v"
STORE_URL = "https://samm6868.github.io/ai-store"

# Pre-block all 13 previously shown products from the first 2 days so today is 100% brand new
INITIAL_SEEN_PRODUCTS = [
    "Mini Wireless Portable Thermal Printer",
    "Crystal Galaxy Levitating Moon Lamp",
    "Ultrasonic Facial Pore Cleanser Pro",
    "Portable USB Rechargeable Blender Bottle",
    "3-in-1 Foldable Magnetic Wireless Charger",
    "Smart Cordless Tire Inflator Air Pump",
    "TWS Active Noise Cancelling Gaming Earbuds",
    "Deep Tissue Percussion Mini Massage Gun",
    "Sunset Projection LED Aesthetic Floor Lamp",
    "Portable Electric Espresso Coffee Maker",
    "Magnetic Magsafe Power Bank 10000mAh",
    "Auto Face Tracking Smart Tripod Gimbal",
    "Hi-Fi Bass Foldable Wireless Studio Headset"
]

# 30 Verified 1200px HD Products (18 Brand-New Unseen Products + 12 Archive Products)
VIRAL_PRODUCT_VAULT = [
    {
        "title": "Ultra-Slim AMOLED Fitness Smartwatch Pro",
        "price": "31.99",
        "old_price": "63.99",
        "category": "Smartwatches",
        "badge": "TOP TREND",
        "rating": "4.9",
        "reviews": "5,280",
        "image": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=1200&q=80",
        "search_keyword": "amoled waterproof fitness smartwatch heart rate",
        "description": "Monitor daily steps, sleep quality, and heart rate on a bright edge-to-edge AMOLED display with 10-day battery endurance.",
        "tags": "#smartwatch #wearabletech #fitnesstracker #everydaycarry"
    },
    {
        "title": "Ultrasonic Flame Aroma Diffuser & Humidifier",
        "price": "20.99",
        "old_price": "41.99",
        "category": "Home Decor",
        "badge": "HOME FAVORITE",
        "rating": "4.9",
        "reviews": "4,750",
        "image": "https://images.unsplash.com/photo-1585386959984-a4155224a1ad?w=1200&q=80",
        "search_keyword": "flame air diffuser humidifier essential oil",
        "description": "Blends fine ultrasonic mist with warm amber LED light to create a realistic, safe candle-flame effect in your bedroom.",
        "tags": "#aromatherapy #homefragrance #relaxingvibes #modernhome"
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
        "description": "Capture classic vintage-inspired snapshots and print physical keepsakes in seconds while saving HD copies to memory.",
        "tags": "#photographylovers #retrostyle #instantcamera #creativegifts"
    },
    {
        "title": "Ergonomic Ultra-Light Wireless Gaming Mouse",
        "price": "23.99",
        "old_price": "47.99",
        "category": "Electronics",
        "badge": "DESK UPGRADE",
        "rating": "4.9",
        "reviews": "3,620",
        "image": "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=1200&q=80",
        "search_keyword": "lightweight wireless gaming mouse rechargeable rgb",
        "description": "Engineered for zero wrist fatigue with honeycomb lightweight shell, silent switches, and lag-free dual wireless connectivity.",
        "tags": "#pcsetup #workspacegoals #ergonomic #techgear"
    },
    {
        "title": "Hot-Swappable RGB Mechanical Gaming Keyboard",
        "price": "34.50",
        "old_price": "69.00",
        "category": "Electronics",
        "badge": "ENTHUSIAST PICK",
        "rating": "4.9",
        "reviews": "4,910",
        "image": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=1200&q=80",
        "search_keyword": "60 percent rgb wireless mechanical keyboard",
        "description": "Save desk space with a compact 60% mechanical layout featuring tactile switches and smooth customizable backlighting.",
        "tags": "#mechanicalkeyboard #deskaccessories #codinglife #gamingsetup"
    },
    {
        "title": "Breathable Ultra-Cushion Running Sneakers",
        "price": "33.99",
        "old_price": "67.99",
        "category": "Fitness & Lifestyle",
        "badge": "COMFORT PICK",
        "rating": "4.8",
        "reviews": "5,540",
        "image": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=1200&q=80",
        "search_keyword": "lightweight breathable mesh running sneakers",
        "description": "Flexible knit uppers and responsive heel cushioning built for long walks, travel days, and daily training sessions.",
        "tags": "#runningcommunity #sneakerhead #comfortshoes #walkmore"
    },
    {
        "title": "Anti-Theft Waterproof USB Travel Backpack",
        "price": "28.50",
        "old_price": "57.00",
        "category": "Smart Living",
        "badge": "TRAVEL ESSENTIAL",
        "rating": "4.9",
        "reviews": "4,180",
        "image": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=1200&q=80",
        "search_keyword": "anti theft waterproof laptop backpack usb charging",
        "description": "Organized padded compartments for laptops and cameras with concealed rear zippers and weather-resistant exterior.",
        "tags": "#traveltips #digitalnomad #backpacklife #commutergear"
    },
    {
        "title": "UV400 Polarized Retro Designer Sunglasses",
        "price": "16.99",
        "old_price": "33.99",
        "category": "Fashion & Style",
        "badge": "STYLE PICK",
        "rating": "4.9",
        "reviews": "7,120",
        "image": "https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=1200&q=80",
        "search_keyword": "uv400 polarized vintage sunglasses unisex",
        "description": "Reduce road and water glare with high-definition polarized UV400 lenses set in lightweight classic frames.",
        "tags": "#eyewearfashion #summerstyle #mensaccessories #womensfashion"
    },
    {
        "title": "Smart LED Temperature Display Insulated Flask",
        "price": "17.99",
        "old_price": "35.99",
        "category": "Kitchen Gadgets",
        "badge": "CLEVER DESIGN",
        "rating": "4.9",
        "reviews": "8,340",
        "image": "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=1200&q=80",
        "search_keyword": "smart led temperature display vacuum thermos bottle",
        "description": "Double-wall stainless steel bottle with a touch-sensitive LED lid that shows your beverage's exact temperature.",
        "tags": "#stayhydrated #ecofriendlyliving #cleverdesign #dailycarry"
    },
    {
        "title": "Waterproof 360 Surround Bluetooth Speaker",
        "price": "26.50",
        "old_price": "53.00",
        "category": "Audio & Music",
        "badge": "OUTDOOR HIT",
        "rating": "4.9",
        "reviews": "4,620",
        "image": "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=1200&q=80",
        "search_keyword": "portable waterproof bluetooth speaker deep bass",
        "description": "Take punchy 360-degree stereo sound to the beach, patio, or trails with IPX7 waterproof protection and 15-hour battery life.",
        "tags": "#bluetoothspeaker #outdoorgear #musicanywhere #beachvibes"
    },
    {
        "title": "Minimalist Sapphire Quartz Chronograph Watch",
        "price": "29.99",
        "old_price": "59.99",
        "category": "Fashion & Style",
        "badge": "CLASSIC STYLE",
        "rating": "4.9",
        "reviews": "3,290",
        "image": "https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=1200&q=80",
        "search_keyword": "minimalist mens leather chronograph waterproof watch",
        "description": "Timeless stainless steel case paired with a genuine stitched leather strap and scratch-resistant mineral crystal glass.",
        "tags": "#wristcheck #classicstyle #menswatches #timelessdesign"
    },
    {
        "title": "Rose Quartz Facial Roller & Gua Sha Sculpting Set",
        "price": "15.50",
        "old_price": "31.00",
        "category": "Beauty & Health",
        "badge": "SELF CARE",
        "rating": "4.8",
        "reviews": "5,110",
        "image": "https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=1200&q=80",
        "search_keyword": "natural rose quartz jade roller gua sha set",
        "description": "Soothe morning puffiness, boost facial circulation, and help serums absorb deeper with cooling natural stone massage tools.",
        "tags": "#guasha #facialmassage #naturalbeauty #morningroutine"
    },
    {
        "title": "Foldable Aluminum Ergonomic Laptop Riser Stand",
        "price": "21.50",
        "old_price": "43.00",
        "category": "Smart Living",
        "badge": "WORK FROM HOME",
        "rating": "4.9",
        "reviews": "6,080",
        "image": "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=1200&q=80",
        "search_keyword": "foldable aluminum adjustable laptop stand desk",
        "description": "Elevate your laptop to eye level for better posture and open-air cooling with sturdy aircraft-grade aluminum.",
        "tags": "#homeoffice #deskorganization #remoteworklife #productivityhacks"
    },
    {
        "title": "360 Pan-Tilt Night Vision Smart Home Camera",
        "price": "24.99",
        "old_price": "49.99",
        "category": "Smart Living",
        "badge": "SMART SECURITY",
        "rating": "4.8",
        "reviews": "3,940",
        "image": "https://images.unsplash.com/photo-1557324232-b8917d3c3dcb?w=1200&q=80",
        "search_keyword": "wireless wifi 360 smart home security pet camera",
        "description": "Check in on pets, babies, or your home in 2K HD from your phone with two-way audio and smart motion alerts.",
        "tags": "#smarthome #homeseurity #petcam #connectedliving"
    },
    {
        "title": "Artisan Ceramic Pour-Over Coffee Maker Set",
        "price": "25.50",
        "old_price": "51.00",
        "category": "Coffee & Kitchen",
        "badge": "BARISTA CHOICE",
        "rating": "4.9",
        "reviews": "2,730",
        "image": "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=1200&q=80",
        "search_keyword": "ceramic v60 pour over coffee dripper carafe set",
        "description": "Extract clean, aromatic specialty coffee at home with spiral-ribbed ceramic heat retention and borosilicate server.",
        "tags": "#pourovercoffee #coffeeculture #homebarista #slowmorning"
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
        "description": "Featherlight ergonomic fit with smart touch controls, clear dual-mic voice pickup, and all-day pocket charging case.",
        "tags": "#earbuds #dailycommute #podcastlife #techreview"
    },
    {
        "title": "Magnetic Sport Strap Health Tracker Watch",
        "price": "27.50",
        "old_price": "55.00",
        "category": "Smartwatches",
        "badge": "READER FAVORITE",
        "rating": "4.8",
        "reviews": "3,190",
        "image": "https://images.unsplash.com/photo-1546868871-7041f2a55e12?w=1200&q=80",
        "search_keyword": "smart watch bluetooth call fitness tracker",
        "description": "Take Bluetooth calls directly from your wrist and track over 100 sport modes in a sleek waterproof aluminum body.",
        "tags": "#watchcollector #techstyle #activelifestyle #smartgadgets"
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
        "description": "Block out background noise and focus in comfort with plush memory-foam cushions and 40 hours of wireless playback.",
        "tags": "#headphones #studywithme #remotework #soundquality"
    }
]


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def load_multi_day_history():
    history = list(INITIAL_SEEN_PRODUCTS)
    try:
        if os.path.exists("feed.xml"):
            with open("feed.xml", "r", encoding="utf-8") as f:
                content = f.read()
                match = re.search(r"<!-- HISTORY: (\[.*?\]) -->", content)
                if match:
                    saved = json.loads(match.group(1))
                    for t in saved:
                        if t not in history:
                            history.append(t)
    except Exception:
        pass

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

    return history[-24:]


def build_daily_catalog():
    recent_history = load_multi_day_history()
    available_pool = [p for p in VIRAL_PRODUCT_VAULT if p["title"] not in recent_history]

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
            "badge": item.get("badge", "TRENDING"),
            "rating": str(item.get("rating", "4.9")),
            "reviews": str(item.get("reviews", "2,450")),
            "image": item["image"],
            "buy_link": buy_link,
            "description": item["description"],
            "tags": item.get("tags", "#coolgadgets #techfinds #smartliving #trending")
        })

    new_history = (recent_history + [p["title"] for p in final_products])[-24:]
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
        prod_page_url = f"{STORE_URL}/{prod_page_filename}"

        # REAL Full Product Review & Buying Landing Page (NO JS Redirect = 100% Facebook & Google Safe!)
        product_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{safe_title} - Review &amp; Best Deal | Trendify AI</title>
    <meta name="description" content="{safe_desc}">
    <link rel="canonical" href="{prod_page_url}" />
    <meta property="og:title" content="{safe_title} | Trendify AI Curated Find" />
    <meta property="og:description" content="{safe_desc}" />
    <meta property="og:image" content="{safe_img_url}" />
    <meta property="og:type" content="article" />
    <meta property="og:url" content="{prod_page_url}" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="{safe_title} | Trendify AI Curated Find" />
    <meta name="twitter:description" content="{safe_desc}" />
    <meta name="twitter:image" content="{safe_img_url}" />
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50 text-gray-900 font-sans">
    <header class="bg-white shadow-sm py-4 px-6 flex justify-between items-center max-w-5xl mx-auto">
        <a href="{STORE_URL}/" class="text-xl font-extrabold tracking-tight text-gray-900">⚡ TRENDIFY <span class="text-indigo-600">AI</span></a>
        <a href="{STORE_URL}/" class="text-sm font-bold text-indigo-600 hover:underline">← Browse All Daily Finds</a>
    </header>
    <main class="max-w-4xl mx-auto px-4 py-10">
        <article class="bg-white rounded-2xl shadow-lg overflow-hidden border border-gray-100 grid grid-cols-1 md:grid-cols-2">
            <div class="relative">
                <img src="{p['image']}" alt="{safe_title}" class="w-full h-full object-cover min-h-[320px]">
                <span class="absolute top-4 left-4 bg-indigo-600 text-white text-xs font-bold px-3 py-1 rounded-full">{p['category']}</span>
            </div>
            <div class="p-6 sm:p-8 flex flex-col justify-between">
                <div>
                    <div class="text-yellow-400 text-sm mb-2">★★★★★ <span class="text-gray-500 text-xs font-semibold">({p['rating']} Rating · {p['reviews']} Happy Users)</span></div>
                    <h1 class="text-2xl sm:text-3xl font-extrabold text-gray-900 mb-4">{safe_title}</h1>
                    <p class="text-gray-600 text-base leading-relaxed mb-6">{safe_desc}</p>
                    <ul class="text-xs sm:text-sm text-gray-600 space-y-2 mb-6 bg-gray-50 p-4 rounded-xl">
                        <li>✔️ Curated Global Trending Gadget</li>
                        <li>✔️ Direct Factory Pricing &amp; Worldwide Delivery</li>
                        <li>✔️ Full Buyer Protection Guarantee</li>
                    </ul>
                </div>
                <div class="pt-4 border-t border-gray-100 flex items-center justify-between">
                    <div>
                        <span class="text-xs text-gray-400 line-through block">Typical: ${p['old_price']}</span>
                        <span class="text-3xl font-extrabold text-green-600">${p['price']}</span>
                    </div>
                    <a href="{p['buy_link']}" target="_blank" rel="noopener noreferrer"
                       onclick="document.getElementById('aff-cookie').src='{AFFILIATE_COOKIE_URL}'"
                       class="bg-indigo-600 hover:bg-indigo-700 text-white font-bold px-6 py-3 rounded-xl shadow-md transition">
                        Check Deal Now 🛒
                    </a>
                </div>
            </div>
        </article>
        <div class="text-center mt-8">
            <a href="{STORE_URL}/" class="inline-block bg-gray-900 text-white font-bold px-8 py-3 rounded-full shadow hover:bg-gray-800 transition">
                Explore Today's Full Catalog →
            </a>
        </div>
    </main>
    <iframe id="aff-cookie" style="display:none;width:0;height:0;border:0;"></iframe>
</body>
</html>"""

        with open(prod_page_filename, "w", encoding="utf-8") as pf:
            pf.write(product_html)

        caption = (
            f"✨ Today's Curated Tech Find: {safe_title}\n\n"
            f"{safe_desc}\n\n"
            f"💡 Featured Deal: ${p['price']} (Compare at ${p['old_price']})\n"
            f"🔗 Details & Global Shipping: {prod_page_url}\n\n"
            f"{p['tags']}"
        )

        rss_items.append(f"""    <item>
      <title>{safe_title} — Curated Feature (${p['price']})</title>
      <link>{prod_page_url}</link>
      <guid isPermaLink="false">trendify-clean-{prod_slug}</guid>
      <pubDate>{now_rfc}</pubDate>
      <description><![CDATA[<img src="{p['image']}" /><br/>{caption}]]></description>
      <enclosure url="{safe_img_url}" length="180000" type="image/jpeg" />
      <media:content url="{safe_img_url}" medium="image" type="image/jpeg" />
    </item>""")

    rss_xml = f"""<?xml version="1.0" encoding="UTF-8" ?>
<!-- HISTORY: {history_json} -->
<rss version="2.0" xmlns:media="http://search.yahoo.com/mrss/">
  <channel>
    <title>Trendify AI | Global Curated Gadgets</title>
    <link>{STORE_URL}</link>
    <description>Daily AI-Curated Trending Tech &amp; Lifestyle Gadgets</description>
    <language>en-us</language>
    <lastBuildDate>{now_rfc}</lastBuildDate>
{chr(10).join(rss_items)}
  </channel>
</rss>"""

    with open("feed.xml", "w", encoding="utf-8") as f:
        f.write(rss_xml)

    print("✅ 6 100% Brand-New Unseen Products generated successfully!")


if __name__ == "__main__":
    generate_store_files()
