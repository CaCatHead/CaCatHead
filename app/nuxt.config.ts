const API_BASE = 'http://127.0.0.1:8000';

// https://v3.nuxtjs.org/api/configuration/nuxt.config
export default defineNuxtConfig({
  modules: ['nuxt-proxy'],
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
});
