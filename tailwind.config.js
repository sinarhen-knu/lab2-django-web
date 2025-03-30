/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './django_project/templates/**/*.html',
    './django_project/core/templates/**/*.html',
  ],
  theme: {
    extend: {
      colors: {
        // Main brand colors
        'brand': {
          50: '#FEF2F2',
          100: '#FDE4E3',
          200: '#FBCCCB',
          300: '#F9A8A6',
          400: '#F47C79',
          500: '#e74c3c', // Primary color
          600: '#D32617',
          700: '#B01C13',
          800: '#8D1913',
          900: '#731714',
          950: '#450A08',
        },
        // Secondary color
        'secondary': {
          50: '#F7F9FC',
          100: '#ECF0F7',
          200: '#D2DBE9',
          300: '#A9BCDA',
          400: '#7797C5',
          500: '#5378AE',
          600: '#34495e', // Secondary color
          700: '#2C3E50',
          800: '#253544',
          900: '#1F2C3A',
          950: '#0F1B29',
        },
        // For vegetarian badge
        'vegetarian': '#2ecc71',
        // For vegan badge
        'vegan': '#27ae60',
        // For gluten-free badge
        'gluten-free': '#f39c12',
        // Spice levels
        'spice': {
          1: '#27ae60',  // Mild
          2: '#2ecc71',  // Medium
          3: '#f39c12',  // Spicy
          4: '#e67e22',  // Very Spicy
          5: '#e74c3c',  // Extreme
        },
      },
    },
  },
  plugins: [
    require('tailwindcss-motion')
  ],
} 