"""Generate site illustrations via Gemini Nano Banana 2."""
import base64
import json
import os
import sys
import urllib.error
import urllib.request

MODEL = "gemini-3.1-flash-image-preview"
OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "img")


def generate(prompt: str, outfile: str) -> bool:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("GEMINI_API_KEY not set", file=sys.stderr)
        return False

    url = (
        f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}"
        f":generateContent?key={api_key}"
    )
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"responseModalities": ["IMAGE", "TEXT"]},
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            data = json.load(resp)
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code} for {outfile}: {e.read().decode()[:500]}", file=sys.stderr)
        return False

    parts = data.get("candidates", [{}])[0].get("content", {}).get("parts", [])
    for part in parts:
        inline = part.get("inlineData")
        if inline and inline.get("data"):
            os.makedirs(os.path.dirname(outfile), exist_ok=True)
            raw = base64.b64decode(inline["data"])
            with open(outfile, "wb") as f:
                f.write(raw)
            print(f"OK {outfile} ({len(raw):,} bytes)")
            return True

    print(f"NO IMAGE in response for {outfile}", file=sys.stderr)
    return False


JOBS = [
    (
        "hero-isometric.png",
        """Generate a website hero background illustration in 16:9 aspect ratio.

Style: Premium Japanese real estate website. Isometric 3D cityscape of a Tokyo bay-side neighborhood.
Include apartment towers, detached houses with red roofs, green parks, roads, trees, small car, waterfront with subtle port crane. Bright sky-blue gradient sky with fluffy white clouds.
Illustration style: polished vector-isometric like high-end Japanese corporate sites — clean, warm, friendly, NOT photorealistic.
Colors: sky blue, yellow accents on signs, green parks, warm beige and coral buildings.

CRITICAL: No text, no letters, no watermarks, no logos. Center area slightly calmer for text overlay. Full bleed edge-to-edge.""",
    ),
    (
        "nav-buy.png",
        """Square 1:1 illustration for a real estate nav icon — "want to buy a home".
Isometric cute scene: young couple looking at a house with a small golden key. Soft white cloud-shaped backdrop, yellow accent #FFD000 highlights. Friendly Japanese real estate style. No text.""",
    ),
    (
        "nav-rent.png",
        """Square 1:1 illustration for a real estate nav icon — "want to rent".
Isometric scene: apartment building with a large key and moving box. Soft cloud backdrop, sky blue and yellow accents. Friendly Japanese illustration. No text.""",
    ),
    (
        "nav-sell.png",
        """Square 1:1 illustration for a real estate nav icon — "want to sell property".
Isometric scene: house with a for-sale sign post (blank sign, no readable text). Coins or contract document hint. Yellow accent, warm colors. No text.""",
    ),
    (
        "nav-owner.png",
        """Square 1:1 illustration for a real estate nav icon — "property owner / landlord".
Isometric scene: multi-unit building with happy owner holding a clipboard. Green and yellow accents. Friendly Japanese illustration. No text.""",
    ),
    (
        "property-apartment.png",
        """16:9 illustration of a modern Japanese apartment building exterior, sunny day, clean real estate listing photo style but illustrated — semi-realistic digital painting, blue sky, welcoming. No text, no watermark.""",
    ),
    (
        "property-house.png",
        """16:9 illustration of a cozy Japanese detached house with garden, sunny day, real estate listing style digital painting. Warm, inviting. No text.""",
    ),
    (
        "property-tower.png",
        """16:9 illustration of a luxury Tokyo tower mansion exterior, evening golden hour, real estate listing style digital painting. Premium feel. No text.""",
    ),
    (
        "page-buy.png",
        """16:9 isometric illustration: family receiving keys in front of a new home, Japanese real estate purchase celebration scene. Sky blue background gradient, yellow accents, professional website illustration. No text.""",
    ),
    (
        "page-rent.png",
        """16:9 isometric illustration: person opening door to a bright rental apartment, boxes nearby. Sky blue and coral palette, friendly Japanese real estate style. No text.""",
    ),
    (
        "page-sell.png",
        """16:9 isometric illustration: homeowner and agent shaking hands in front of sold house with blank sign post. Warm sunset tones, yellow accents. No text.""",
    ),
    (
        "page-owner.png",
        """16:9 isometric illustration: apartment building with owner reviewing portfolio charts, rental income concept. Green and blue professional palette. No text.""",
    ),
    (
        "page-properties.png",
        """16:9 isometric illustration: grid of apartment buildings and houses with magnifying glass, property search concept. Sky blue, yellow accents, Japanese real estate website style. No text.""",
    ),
    (
        "page-area.png",
        """16:9 isometric illustration: Tokyo neighborhood map with pins on districts, parks and train station. Friendly real estate area guide style. No text.""",
    ),
    (
        "page-faq.png",
        """16:9 illustration: friendly real estate agent answering questions with speech bubbles (blank, no readable text). Professional, warm, sky blue palette. No text.""",
    ),
    (
        "page-staff.png",
        """16:9 illustration: diverse team of Japanese real estate professionals in office, friendly group portrait style illustration. Business casual, warm lighting. No text.""",
    ),
    (
        "page-voice.png",
        """16:9 illustration: happy family in front of new home giving thumbs up, customer testimonial concept. Warm, trustworthy real estate style. No text.""",
    ),
    (
        "page-guide.png",
        """16:9 isometric illustration: step-by-step path with icons for consultation, viewing, contract — first-time buyer guide. Clean infographic style, blue and yellow. No text.""",
    ),
    (
        "property-interior.png",
        """16:9 photo-realistic digital painting of bright modern Japanese apartment living room interior, large windows, minimalist furniture, real estate listing photo style. No text.""",
    ),
    # ── Realistic photos for design upgrade ──
    (
        "photo-office.png",
        """Professional real estate photography, 16:9. Bright modern Japanese real estate agency office interior, reception desk, warm wood and white decor, plants, natural light from large windows. High-end corporate photo, sharp focus, no people, no text, no watermark.""",
    ),
    (
        "photo-staff-01.png",
        """Professional corporate headshot photo, 1:1 square. Japanese businessman age 45, navy suit, friendly confident smile, neutral soft gray studio background. Real photography style, sharp, natural skin. No text.""",
    ),
    (
        "photo-staff-02.png",
        """Professional corporate headshot photo, 1:1 square. Japanese businesswoman age 32, beige blazer, warm smile, neutral soft gray studio background. Real photography style. No text.""",
    ),
    (
        "photo-staff-03.png",
        """Professional corporate headshot photo, 1:1 square. Japanese businessman age 35, light gray suit, approachable smile, studio background. Real photography style. No text.""",
    ),
    (
        "photo-staff-04.png",
        """Professional corporate headshot photo, 1:1 square. Japanese businesswoman age 28, white blouse, professional smile, studio background. Real photography style. No text.""",
    ),
    (
        "photo-staff-05.png",
        """Professional corporate headshot photo, 1:1 square. Japanese businessman age 55, dark suit, trustworthy expression, studio background. Real photography style. No text.""",
    ),
    (
        "photo-staff-06.png",
        """Professional corporate headshot photo, 1:1 square. Japanese businesswoman age 30, navy cardigan, gentle smile, studio background. Real photography style. No text.""",
    ),
    (
        "photo-lifestyle-family.png",
        """Real estate lifestyle photography, 16:9. Happy Japanese family of three in bright modern apartment living room, large windows, plants, natural daylight, warm authentic moment. Editorial quality, no text.""",
    ),
    (
        "photo-neighborhood.png",
        """Real estate neighborhood photography, 16:9. Charming Tokyo residential street near Ebisu, cherry trees, cafes, clean sidewalks, afternoon golden light. Inviting urban living atmosphere. No text, no readable signs.""",
    ),
    (
        "photo-consultation.png",
        """Real estate photography, 16:9. Japanese real estate agent in suit showing tablet to young couple in modern office meeting room, professional consultation scene, warm lighting. Authentic, no text.""",
    ),
    (
        "photo-bedroom.png",
        """Real estate interior listing photo, 16:9. Bright modern Japanese apartment bedroom, white bedding, large window, minimalist Scandinavian-Japanese style. Professional property photo. No text.""",
    ),
    (
        "photo-kitchen.png",
        """Real estate interior listing photo, 16:9. Clean modern Japanese apartment kitchen, white cabinets, wood accents, bright natural light. Professional property listing photography. No text.""",
    ),
    (
        "photo-banner-wide.png",
        """Cinematic wide real estate photo, 21:9 ultra-wide. Japanese couple walking toward beautiful modern apartment building entrance, blue sky, hopeful new home moment. Premium real estate advertising photography. No text.""",
    ),
    (
        "photo-storefront.png",
        """Real estate photography, 16:9. Modern Japanese real estate shop exterior in Tokyo, glass facade, clean signage area blank, street trees, daytime. Professional architectural photo. No readable text.""",
    ),
    (
        "photo-rent-interior.png",
        """Real estate interior photo, 16:9. Stylish compact 1LDK Tokyo rental apartment, open living dining, city view from window, warm evening light. Listing photo quality. No text.""",
    ),
]


if __name__ == "__main__":
    targets = sys.argv[1:] if len(sys.argv) > 1 else [name for name, _ in JOBS]
    ok = 0
    for name, prompt in JOBS:
        if name not in targets and len(sys.argv) > 1:
            continue
        path = os.path.normpath(os.path.join(OUT_DIR, name))
        if generate(prompt, path):
            ok += 1
    print(f"Done: {ok}/{len(targets if len(sys.argv) > 1 else JOBS)}")
