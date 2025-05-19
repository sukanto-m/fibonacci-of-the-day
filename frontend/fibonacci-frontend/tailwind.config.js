/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
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
  },
},
  plugins: [],
};
