/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './**/templates/**/*.html',  // This will find templates in any app
    './static/src/**/*.js',

  ],
  theme: {
    extend: {},
  },
  plugins: [],
}

