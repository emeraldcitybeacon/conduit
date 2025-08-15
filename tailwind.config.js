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
    plugin(function ({ addComponents, theme }) {
      addComponents({
        '.dashboard-card': {
          borderRadius: theme('borderRadius.lg'),
          boxShadow: theme('boxShadow.md'),
          backgroundColor: theme('colors.neutral.100'),
          padding: theme('spacing.4'),
          display: 'flex',
          alignItems: 'center',
        },
        '.dashboard-toast': {
          position: 'fixed',
          right: theme('spacing.4'),
          bottom: theme('spacing.4'),
          borderRadius: theme('borderRadius.lg'),
          boxShadow: theme('boxShadow.md'),
          backgroundColor: theme('colors.neutral.100'),
          padding: theme('spacing.4'),
          fontSize: theme('fontSize.sm')[0],
        },
      })
    }),
  ],
};
