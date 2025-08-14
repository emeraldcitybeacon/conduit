const plugin = require('tailwindcss/plugin')

module.exports = function createTailwindConfig(siteTokens = {}) {
  return {
    content: [
      './src/**/templates/**/*.html',
      './src/**/static/**/*.js',
      './templates/**/*.html',
    ],
    theme: {
      extend: {
        // Base tokens will be merged with site-specific tokens
        colors: siteTokens.colors || {},
        fontFamily: siteTokens.fontFamily || {},
        spacing: siteTokens.spacing || {},
        borderRadius: siteTokens.borderRadius || {},
        boxShadow: siteTokens.shadows || {},
      },
    },
    plugins: [
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
  }
}
