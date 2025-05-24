import os
import httpx
import openai
import json
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam

load_dotenv()

# API keys
UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

# Constants
UNSPLASH_URL = "https://api.unsplash.com/photos/random"
DB_FILE = "timeline.json"
cache = {}

async def generate_caption(image_description: str) -> str:
    prompt = (
        f"This image shows a natural pattern that illustrates the Fibonacci sequence: '{image_description}'. "
        "Explain briefly how it relates to Fibonacci numbers. Keep the explanation under 40 words."
    )

    messages: list[ChatCompletionMessageParam] = [
        {"role": "system", "content": "You are a science explainer."},
        {"role": "user", "content": prompt}
    ]

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0.7,
            max_tokens=60,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("GPT error:", e)
        return "This image likely illustrates a natural Fibonacci pattern such as a sunflower or spiral."

def save_to_timeline(date: str, entry: dict):
    try:
        if os.path.exists(DB_FILE):
            with open(DB_FILE, "r") as f:
                data = json.load(f)
        else:
            data = {}

        data[date] = entry

        with open(DB_FILE, "w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print("Failed to write to timeline:", e)

async def get_image_of_the_day():
    today = datetime.utcnow().strftime("%Y-%m-%d")
    if today in cache:
        return cache[today]

    params = {
        "query": "fibonacci spiral nature",
        "orientation": "landscape",
        "client_id": UNSPLASH_ACCESS_KEY,
    }

    async with httpx.AsyncClient() as client_http:
        response = await client_http.get(UNSPLASH_URL, params=params, timeout=10.0)
        response.raise_for_status()
        data = response.json()

        # Extract image details
        image_url = data["urls"]["regular"]
        title = data.get("alt_description") or "a Fibonacci spiral in nature"
        photographer = data["user"]["name"]
        photographer_url = data["user"]["links"]["html"]

        caption = await generate_caption(title)

        result = {
            "image_url": image_url,
            "caption": caption,
            "credit": {
                "photographer": photographer,
                "profile_url": photographer_url
            }
        }

        cache[today] = result
        save_to_timeline(today, result)
        return result