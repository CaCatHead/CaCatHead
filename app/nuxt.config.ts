import {
  presetUno,
  presetIcons,
  presetAttributify,
  transformerDirectives,
  transformerVariantGroup,
} from 'unocss';

// This is the django server
const API_BASE = 'http://127.0.0.1:8000';

// https://v3.nuxtjs.org/api/configuration/nuxt.config
export default defineNuxtConfig({
  app: {
    head: {
      title: 'CaCatHead',
      link: [{ rel: 'icon', href: '/favicon.png' }],
    },
  },
  runtimeConfig: {
    API_BASE,
  },
  modules: ['nuxt-proxy', '@unocss/nuxt', '@pinia/nuxt'],
  proxy: {
    options: {
      target: API_BASE,
      changeOrigin: true,
      pathFilter: ['/api/'],
    },
  },
  unocss: {
    preflight: true,
    presets: [
      presetUno(),
      presetAttributify(),
      presetIcons({
        scale: 1.2,
        extraProperties: {
          height: '1.5em',
          'flex-shrink': '0',
          display: 'inline-block',
        },
      }),
    ],
    transformers: [transformerDirectives(), transformerVariantGroup()],
    shortcuts: [],
    rules: [],
  },
});
