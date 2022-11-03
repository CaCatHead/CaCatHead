const API_BASE = 'http://127.0.0.1:8000';

// https://v3.nuxtjs.org/api/configuration/nuxt.config
export default defineNuxtConfig({
  app: {
    head: {
      title: 'CaCatHead',
      link: [{ rel: 'icon', href: '/favicon.png' }],
    },
  },
  modules: ['nuxt-proxy', '@unocss/nuxt'],
  runtimeConfig: {
    api: API_BASE,
  },
  proxy: {
    options: {
      target: API_BASE,
      changeOrigin: true,
      pathFilter: ['/api/'],
    },
  },
  unocss: {
    uno: true, // enabled `@unocss/preset-uno`
    icons: true, // enabled `@unocss/preset-icons`
    attributify: true, // enabled `@unocss/preset-attributify`,
    // core options
    shortcuts: [],
    rules: [],
  },
});
