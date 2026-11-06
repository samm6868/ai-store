import os
import json
import urllib.request
import urllib.parse

API_KEY = os.environ.get("GEMINI_API_KEY")
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

prompt = """
Act as an elite E-Commerce Dropshipping & Marketing AI Agent.
Find 6 of the hottest, most viral trending physical products selling right now globally (TikTok, Amazon, AliExpress trends).
For each product:
1. Write a catchy Shopify-style 'title'.
2. Write a persuasive, high-converting 'description' (2 sentences).
3. Set a smart selling 'price' (between 19.99 and 59.99) that guarantees high profit margins, and a higher 'old_price' to show a discount.
4. Create a 'search_keyword' (2 to 4 English words describing the product simply, e.g., 'mini portable projector').
5. Write a viral 'marketing_post' (engaging TikTok/Instagram ad copy with emojis and hashtags to market this product automatically).

Return ONLY a valid JSON array in this exact format, with no markdown or extra text:
[
  {
    "title": "Product Name",
    "description": "Persuasive description...",
    "price": "29.99",
    "old_price": "49.99",
    "search_keyword": "keyword here",
    "marketing_post": "Ad copy with #hashtags"
  }
]
"""

data = {
    "contents": [{"parts": [{"text": prompt}]}],
    "generationConfig": {"response_mime_type": "application/json"}
}

req = urllib.request.Request(
    URL, 
    data=json.dumps(data).encode('utf-8'), 
    headers={'Content-Type': 'application/json'}
)

try:
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode('utf-8'))
        raw_text = result['candidates'][0]['content']['parts'][0]['text']
        products = json.loads(raw_text)

        final_products = []
        for p in products:
            kw = urllib.parse.quote(p['search_keyword'])
            img_prompt = urllib.parse.quote(f"professional studio product photography of {p['search_keyword']}, sleek commercial lighting, white background, 8k")
            
            p['image'] = f"https://image.pollinations.ai/prompt/{img_prompt}?width=800&height=800&nologo=true"
            p['buy_link'] = f"https://www.aliexpress.com/w/wholesale-{kw.replace('%20', '-')}.html"
            final_products.append(p)

        with open("products.json", "w", encoding="utf-8") as f:
            json.dump(final_products, f, indent=2)
            
        print("AI Agent successfully updated products and marketing campaigns!")
except Exception as e:
    print(f"Error: {e}")
