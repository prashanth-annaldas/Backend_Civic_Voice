from dotenv import load_dotenv
import os
from google import genai
from PIL import Image
import io
from fastapi import HTTPException

# Load env only for local development
load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")

# Create client only if key exists
client = genai.Client(api_key=API_KEY) if API_KEY else None


def detect_issue(image_bytes: bytes) -> str:
    if not API_KEY or not client:
        raise HTTPException(
            status_code=500,
            detail="Gemini API key not configured on server"
        )

    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    prompt = """
Return ONLY one label:
pothole
garbage
water_leak
street_light
electric_transformer
unknown
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[prompt, image]
    )

    text = (response.text or "").lower()

    if "pothole" in text:
        return "pothole"
    elif "garbage" in text:
        return "garbage"
    elif "water" in text:
        return "water_leak"
    elif "light" in text:
        return "street_light"
    elif "electric" in text:
        return "electric_transformer"
    else:
        return "unknown"