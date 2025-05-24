from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from image_service import get_image_of_the_day
import os
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",                 # for dev
        "https://todays-fibonacci.link",         # your custom domain
        "https://fibonacci.vercel.app",          # optional Vercel fallback
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/image-of-the-day")
async def image_of_the_day():
    try:
        return await get_image_of_the_day()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/timeline")
def get_timeline():
    try:
        if os.path.exists("timeline.json"):
            with open("timeline.json", "r") as f:
                return json.load(f)
        return {}
    except:
        return {}
