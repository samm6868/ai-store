import os
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

# Verified High-Speed HD Commercial Product Images mapped by Category
STUDIO_IMAGE_BANK = {
    "Electronics": "https://images.unsplash.com/photo-1612815154858-60aa4c59eaa6?w=800&q=80",
    "Home Decor": "https://images.unsplash.com/photo-1513506003901-1e6a229e2d15?w=800&q=80",
    "Beauty & Health": "https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?w=800&q=80",
    "Kitchen Gadgets": "https://images.unsplash.com/photo-1570222094114-d054a817e56b?w=800&q=80",
    "Smart Living": "https://images.unsplash.com/photo-1558002038-1055907df827?w=800&q=80",
    "Auto Accessories": "https://images.unsplash.com/photo-1544829099-b9a0c07fad1a?w=800&q=80",
    "Audio & Music": "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=800&q=80",
    "Fitness & Massage": "https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=800&q=80",
    "Smart Lighting": "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=800&q=80",
    "Coffee & Kitchen": "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=800&q=80",
    "Mobile Accessories": "https://images.unsplash.com/photo-1583394838336-acd977736f90?w=800&q=80",
    "Content Creation": "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=800&q=80"
}

# 12 Dynamic Backup Viral Products (Used if AI quota is busy, ensuring daily rotation)
DYNAMIC_POOL = [
    {
        "title": "Mini Wireless Portable Thermal Printer",
        "price": "19.99",
        "old_price": "39.99",
        "category": "Electronics",
        "badge": "TIKTOK VIRAL",
        "rating": "4.9",
        "reviews": "3,420",
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
        "search_keyword": "portable electric travel espresso maker",
        "description": "Brew rich, crema-topped espresso on the go using capsules or ground coffee with one-button USB heating."
    },
    {
        "title": "Magnetic Magsafe Power Bank 10000mAh",
        "price": "23.99",
        "old_price": "47.99",
        "category": "Mobile Accessories",
        "badge": "BEST VALUE",
        "rating": "4.8",
        "reviews": "3,310",
        "search_keyword": "magnetic wireless power bank 10000mah",
        "description": "Snap-and-charge ultra-slim battery pack with foldable kickstand and 20W fast charging for all smartphones."
    },
    {
        "title": "Auto Face Tracking Smart Tripod Gimbal",
        "price": "25.99",
        "old_price": "51.99",
        "category": "Content Creation",
        "badge": "CREATOR PICK",
        "rating": "4.9",
        "reviews": "2,470",
        "search_keyword": "360 auto face tracking phone holder tripod",
        "description": "Hands-free 360-degree AI motion tracking camera stand—no app required, perfect for Reels, TikTok, and video calls."
    }
]


def load_previous_titles():
    try:
        if os.path.exists("products.json"):
            with open("products.json", "r", encoding="utf-8") as f:
                old_data = json.load(f)
                return [item.get("title", "") for item in old_data]
    except Exception:
        pass
    return []


def fetch_live_ai_trends(previous_titles):
    if not GEMINI_API_KEY:
        return None

    categories_list = list(STUDIO_IMAGE_BANK.keys())
    avoid_str = ", ".join(previous_titles[:6]) if previous_titles else "None"

    prompt = (
        "You are an expert e-commerce viral product hunter. "
        "Generate 6 brand-new, currently trending viral physical products selling fast on TikTok, Amazon, and AliExpress. "
        f"Do NOT repeat these previous product titles: [{avoid_str}]. "
        f"For each product, choose the closest matching category ONLY from this exact list: {json.dumps(categories_list)}, "
        "and make sure all 6 products use 6 DIFFERENT categories from that list. "
        "Return ONLY a valid JSON array of 6 objects with these exact keys: "
        "title, price (string between 15.99 and 34.99), old_price (string double the price), "
        "category (must match one from the list), badge (short uppercase like TIKTOK VIRAL, 50% OFF, BEST SELLER), "
        "rating (string 4.8 or 4.9), reviews (string like 2,450), "
        "search_keyword (3 to 5 English words for AliExpress search), "
        "description (compelling 1-2 sentence English sales pitch)."
    )

    models = ["gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-flash-latest"]
    for model in models:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={GEMINI_API_KEY}"
            payload = json.dumps({
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"temperature": 0.85}
            }).encode("utf-8")
            req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=25) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                raw_text = result["candidates"][0]["content"]["parts"][0]["text"].strip()
                if "```" in raw_text:
                    raw_text = raw_text.split("```")[1]
                    if raw_text.startswith("json"):
                        raw_text = raw_text[4:]
                items = json.loads(raw_text.strip())
                if isinstance(items, list) and len(items) >= 6:
                    print(f"✅ Successfully generated 6 fresh trending products via {model}!")
                    return items[:6]
        except Exception as e:
            print(f"⚠️ {model} notice: {e}")
    return None


def build_daily_catalog():
    previous_titles = load_previous_titles()
    raw_items = fetch_live_ai_trends(previous_titles)

    if not raw_items:
        print("🔄 Selecting fresh rotated products from Dynamic Viral Pool...")
        fresh_pool = [p for p in DYNAMIC_POOL if p["title"] not in previous_titles]
        if len(fresh_pool) < 6:
            fresh_pool = DYNAMIC_POOL[:]
        random.shuffle(fresh_pool)
        raw_items = fresh_pool[:6]

    final_products = []
    used_images = set()
    bank_urls = list(STUDIO_IMAGE_BANK.values())

    for item in raw_items:
        cat = item.get("category", "Electronics")
        img_url = STUDIO_IMAGE_BANK.get(cat)
        if not img_url or img_url in used_images:
            for candidate in bank_urls:
                if candidate not in used_images:
                    img_url = candidate
                    break
        used_images.add(img_url)

        kw = urllib.parse.quote_plus(item.get("search_keyword", item.get("title", "viral gadget")))
        buy_link = (
            f"https://www.aliexpress.com/w/wholesale-{kw}.html"
            f"?sk={AFFILIATE_KEY}&aff_fsk={AFFILIATE_KEY}&aff_platform=portals-tool"
        )

        final_products.append({
            "title": item["title"],
            "price": str(item["price"]).replace("$", ""),
            "old_price": str(item["old_price"]).replace("$", ""),
            "category": cat,
            "badge": item.get("badge", "VIRAL DEAL"),
            "rating": str(item.get("rating", "4.9")),
            "reviews": str(item.get("reviews", "2,180")),
            "image": img_url,
            "buy_link": buy_link,
            "description": item["description"]
        })

    return final_products


def generate_store_files():
    products = build_daily_catalog()

    with open("products.json", "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)

    now_rfc = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
    batch_stamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")

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

        prod_page_filename = f"product-{i}.html"
        prod_page_url = f"{STORE_URL}/{prod_page_filename}"
        target_store_url = f"{STORE_URL}/#product-{i}"

        # Create dedicated Open Graph product landing card for Facebook, X/Twitter & Pinterest
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
    <meta property="og:type" content="product" />
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

        rss_items.append(f"""    <item>
      <title>🔥 {safe_title} - Only ${p['price']} (50% OFF!)</title>
      <link>{prod_page_url}</link>
      <guid isPermaLink="false">trendify-{batch_stamp}-{i}</guid>
      <pubDate>{now_rfc}</pubDate>
      <description><![CDATA[<img src="{p['image']}" /><br/>{caption}]]></description>
      <enclosure url="{safe_img_url}" length="150000" type="image/jpeg" />
      <media:content url="{safe_img_url}" medium="image" type="image/jpeg" />
    </item>""")

    rss_xml = f"""<?xml version="1.0" encoding="UTF-8" ?>
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

    print("✅ Store catalog (products.json), product preview cards, and feed.xml updated successfully!")


if __name__ == "__main__":
    generate_store_files()
