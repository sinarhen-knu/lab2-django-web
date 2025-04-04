/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./django_project/templates/**/*.html",
    "./django_project/templates/core/**/*.html",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          300: '#93c5fd',
          500: '#3b82f6',
        },
        secondary: {
          500: '#6b7280',
          600: '#4b5563',
        }
      },
    },
  },
  plugins: [require('tailwindcss-motion')],
} 