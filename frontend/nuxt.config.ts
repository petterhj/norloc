import { defineNuxtConfig } from 'nuxt3'

// https://v3.nuxtjs.org/docs/directory-structure/nuxt.config
export default defineNuxtConfig({
  components: true,

  // css: [
  //   "@/assets/global.css",
  // ],

  build: {
    transpile: ['@headlessui/vue'],
  },

  buildModules: [
    'nuxt-windicss',
  ],
})
