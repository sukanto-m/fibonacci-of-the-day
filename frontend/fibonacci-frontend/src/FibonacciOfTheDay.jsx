import { useState, useEffect } from "react";

export default function FibonacciOfTheDay() {
  const [imageUrl, setImageUrl] = useState("");
  const [caption, setCaption] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [timeline, setTimeline] = useState({});

  const handleClick = async () => {
    setLoading(true);
    setError(null);

    try {
      const res = await fetch("/api/image-of-the-day");
      const data = await res.json();
      setImageUrl(data.image_url);
      setCaption(data.caption || "This image reflects a natural occurrence of the Fibonacci sequence.");
    } catch (err) {
      setError("Failed to load image.");
    } finally {
      setLoading(false);
    }
  };

  const handleShare = () => {
    if (navigator.share) {
      navigator.share({
        title: "Fibonacci of the Day",
        text: caption,
        url: imageUrl,
      });
    } else {
      alert("Sharing not supported on this browser.");
    }
  };

  useEffect(() => {
    fetch("/api/timeline")
      .then((res) => res.json())
      .then((data) => setTimeline(data));
  }, []);

  return (
    <div className="h-screen w-screen flex flex-col justify-start items-center bg-white text-black p-4 overflow-y-auto">
      {/* Typing header */}
      <div className="mt-10 mb-4">
        <p className="text-2xl font-bold uppercase whitespace-nowrap overflow-hidden border-r-2 border-black pr-2 animate-typing">
          Fibonacci of the Day
          <span className="animate-blink">|</span>
        </p>
      </div>

      {/* Button */}
      <button
        onClick={handleClick}
        className="px-6 py-2 text-white bg-black rounded hover:bg-gray-800 transition mb-6"
      >
        Show me today's Fibonacci
      </button>

      {/* Image and Caption */}
      <div className="flex flex-col items-center text-center px-4">
        {loading && <p>Loading image...</p>}
        {error && <p className="text-red-500">{error}</p>}
        {imageUrl && (
          <>
            <img
              src={imageUrl}
              alt="Fibonacci of the Day"
              className="max-w-full h-auto rounded-xl shadow-md mb-4"
            />
            <p className="text-gray-700 italic max-w-2xl text-center mb-2">{caption}</p>
            <div className="flex gap-4">
              <a
                href={imageUrl}
                download
                className="text-sm text-blue-600 underline"
              >
                Download this image
              </a>
              <button
                onClick={handleShare}
                className="px-4 py-1 text-sm text-white bg-blue-600 rounded hover:bg-blue-700"
              >
                Share this
              </button>
            </div>
          </>
        )}
      </div>

      {/* Timeline */}
      <div className="mt-10 w-full max-w-3xl">
        <h2 className="text-lg font-semibold mb-4">Past Fibonacci Images</h2>
        {Object.entries(timeline).slice(-5).reverse().map(([date, entry]) => (
          <div key={date} className="mt-4 border-t pt-4">
            <p className="text-sm font-semibold mb-2">{date}</p>
            <img src={entry.image_url} className="w-full max-w-md rounded mb-2" />
            <p className="text-xs italic text-gray-600 text-center max-w-md mx-auto">{entry.caption}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

// Tailwind config additions (in tailwind.config.js):
/*
  extend: {
    keyframes: {
      typing: {
        '0%': { width: '0' },
        '100%': { width: '100%' },
      },
      blink: {
        '0%, 100%': { borderColor: 'transparent' },
        '50%': { borderColor: 'black' },
      },
    },
    animation: {
      typing: 'typing 4s steps(30, end) 1',
      blink: 'blink 0.75s step-end infinite',
    },
  }
*/