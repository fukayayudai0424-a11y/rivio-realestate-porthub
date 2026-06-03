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
