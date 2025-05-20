import os
import httpx
import random 
import openai
import json
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam

load_dotenv()

SERPAPI_KEY = os.getenv("SERPAPI_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERPAPI_URL = "https://serpapi.com/search.json"
DB_FILE = "timeline.json"

client = OpenAI(api_key=OPENAI_API_KEY)
cache = {}

async def generate_caption(image_description: str) -> str:
    messages: list[ChatCompletionMessageParam] = [
        {"role": "system", "content": "You are a science explainer."},
        {"role": "user", "content": f"Explain briefly how this image represents the Fibonacci sequence: '{image_description}'. Keep it factual and under 40 words."}
    ]
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
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
        "engine": "google",
        "q": "fibonacci spiral in nature",
        "tbm": "isch",
        "api_key": SERPAPI_KEY,
    }

    async with httpx.AsyncClient() as client_http:
        response = await client_http.get(SERPAPI_URL, params=params, timeout=10.0)
        response.raise_for_status()
        data = response.json()

        if "images_results" not in data or not data["images_results"]:
            raise ValueError("No images found from SerpAPI.")

        top_image = random.choice(data["images_results"][:5])
        image_url = top_image["original"]
        title = top_image.get("title", "a Fibonacci spiral in nature")

        caption = await generate_caption(title)

        result = {"image_url": image_url, "caption": caption}
        cache[today] = result
        save_to_timeline(today, result)
        return result
