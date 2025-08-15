/**
 * Base Tailwind configuration factory
 * Exports a function that accepts site-specific tokens and returns a merged config
 */

const plugin = require('tailwindcss/plugin')

module.exports = {
  content: [
    './src/**/templates/**/*.html',
    './src/**/static/**/*.js',
    './templates/**/*.html',
  ],
  plugins: [
    require('@tailwindcss/forms'),
    require('daisyui'),
  ],
};
