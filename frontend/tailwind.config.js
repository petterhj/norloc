const defaultTheme = require('tailwindcss/defaultTheme')

console.log(defaultTheme)

module.exports = {
  // mode: 'jit',
  
  // purge: [
  //   './components/**/*.{vue,js}',
  //   './layouts/**/*.vue',
  //   './pages/**/*.vue',
  //   './plugins/**/*.{js,ts}',
  //   './nuxt.config.{js,ts}',
  // ],
  
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
};
