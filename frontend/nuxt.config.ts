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
    '@/assets/main.css',
  ],

  buildModules: [
    '@pinia/nuxt',
    // https://tailwindcss.nuxtjs.org/tailwind/config/
    '@nuxtjs/tailwindcss'
  ],
})
