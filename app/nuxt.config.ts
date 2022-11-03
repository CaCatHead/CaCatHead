import { presetCore, presetThemeDefault } from 'anu-vue';
import {
  presetUno,
  presetIcons,
  presetWebFonts,
  presetAttributify,
  transformerDirectives,
  transformerVariantGroup,
} from 'unocss';

const API_BASE = 'http://127.0.0.1:8000';

// https://v3.nuxtjs.org/api/configuration/nuxt.config
export default defineNuxtConfig({
  app: {
    head: {
      title: 'CaCatHead',
      link: [{ rel: 'icon', href: '/favicon.png' }],
    },
  },
  modules: ['@unocss/nuxt', '@pinia/nuxt'],
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
      presetWebFonts({
        fonts: {
          sans: 'Inter:100,200,400,700,800',
          mono: 'Fira Code',
        },
      }),
      presetCore(),
      presetThemeDefault(),
    ],
    transformers: [transformerDirectives(), transformerVariantGroup()],
    shortcuts: [],
    rules: [],
    include: [/.*\/anu-vue\.js(.*)?$/, './**/*.vue', './**/*.md'],
  },
});
