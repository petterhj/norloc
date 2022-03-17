import { defineConfig } from 'windicss/helpers'

const defaultTheme = require('windicss/defaultTheme')

const NorlocTheme = {
  // colors: {
  // },
  fontFamily: {
    sans: ['UnicaOne', ...defaultTheme.fontFamily.sans],
    serif: ['Vollkorn', ...defaultTheme.fontFamily.serif],
  },
}

export default defineConfig({
  // preflight: false,
  // extract: {
  //   include: ['**/*.{vue}'],
  //   exclude: ['node_modules', '.git'],
  // },
  theme: {
    extend: {
      // maxWidth: {
      //   '8xl': '90rem',
      // },
      colors: {
        // primary: NorlocTheme.colors.green[500],
        // gray: NorlocTheme.colors.gray,
      },
      fontFamily: NorlocTheme.fontFamily,
    }
  },
  plugins: [
    require('windicss/plugin/typography'),
  ],
})
