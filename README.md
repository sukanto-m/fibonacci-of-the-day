# Fibonacci of the Day

🌻 A minimal, elegant web app that celebrates the beauty of Fibonacci spirals in nature — one image at a time.

Live: [todays-fibonacci.link](https://todays-fibonacci.link)

---

## 🌀 What It Does

* **Fetches a new image daily** from Unsplash based on Fibonacci-related queries
* Uses **GPT-4** to generate short captions explaining the pattern
* Displays **photographer credit** and image source
* Lets users **download or share** the image
* Tracks a **timeline** of past images and captions

---

## 🧰 Tech Stack

### Frontend

* React + Vite
* Tailwind CSS
* Vercel (for hosting)

### Backend

* FastAPI (Python)
* Unsplash API for images
* OpenAI GPT-4o for captions
* JSON-based timeline storage
* Render (for hosting backend)

---

## 📸 Credits & Ethics

* All images are served via the **Unsplash API** and credited to the photographer
* Captions are generated via **OpenAI GPT-4o** based on image metadata (not visual recognition)

---

## 🔧 Local Setup

```bash
# Clone the repo
https://github.com/yourusername/fibonacci-of-the-day

# Frontend
cd frontend
npm install
npm run dev

# Backend
cd ../backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### .env (for backend)

```
UNSPLASH_ACCESS_KEY=your_key
OPENAI_API_KEY=your_key
```

---

## 💡 Future Ideas

* Let users browse full timeline or specific dates
* Add educational overlays (spiral tracing, math notes)
* Add PWA support or mobile app wrapper
* Optionally use GPT-4 vision to caption real images

---

## 🧠 Built By

A curious mind exploring intersections of nature, math, and AI.

Feel free to fork, remix, or reach out!
