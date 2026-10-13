/** @type {import('tailwindcss').Config} */
export default {
  content: ["./src/**/*.{js,mjs,html}", "./admin/**/*.html"],
  theme: {
    extend: {
      colors: {
        paper: "#f4f0e8",
        card: "#fffcf7",
        ink: "#1a1814",
        muted: "#5c564c",
        line: "#e2d9cc",
        pine: "#1f4d3a",
        pineDark: "#16382b",
        copper: "#8a4528",
      },
      fontFamily: {
        serif: ["Iowan Old Style", "Palatino Linotype", "Palatino", "Georgia", "serif"],
        sans: ["Segoe UI", "Helvetica Neue", "Arial", "sans-serif"],
      },
    },
  },
  plugins: [],
};
