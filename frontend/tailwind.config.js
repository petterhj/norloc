import { defaultTheme } from 'tailwindcss/defaultTheme'

module.exports = { 
  content: [
    // `components/**/*.{vue,js}`,
    // `layouts/**/*.vue`,
    // `pages/**/*.vue`,
    // `plugins/**/*.{js,ts}`,
    // `nuxt.config.{js,ts}`,
    `error.vue`
  ],
  theme: {
    extend: {
      colors: {
        'accent': '#c31',
      },
      fontFamily: {
        sans: ['UnicaOne', ...defaultTheme.fontFamily.sans],
        serif: ['Vollkorn', ...defaultTheme.fontFamily.serif],
      },
    },
  },
}
