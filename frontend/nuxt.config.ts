import { defineNuxtConfig } from 'nuxt3'

// https://v3.nuxtjs.org/docs/directory-structure/nuxt.config
export default defineNuxtConfig({
  components: true,

  meta: {
    meta: [
      { name: 'viewport', content: 'width=device-width, initial-scale=1' }
    ],
  },

  css: [
    '@/assets/scss/main.scss',
  ],

  buildModules: [
    '@pinia/nuxt',
    '@nuxtjs/tailwindcss'
  ],

  tailwindcss: {
    configPath: '@/tailwind.config.js',
    // exposeConfig: false,
    // config: {},
    // injectPosition: 0,
    // viewer: true,
  }
})
