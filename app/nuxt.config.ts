import {
  presetUno,
  presetIcons,
  presetWebFonts,
  presetTypography,
  presetAttributify,
  transformerDirectives,
  transformerVariantGroup,
} from 'unocss';

import * as fs from 'fs-extra';

// This is the django server
const API_BASE = process.env['API_BASE'] ?? 'http://127.0.0.1:8000';

// Enable cache
const ENABLE_CACHE = process.env['ENABLE_CACHE'] === 'false' ? false : true;

// https://v3.nuxtjs.org/api/configuration/nuxt.config
export default defineNuxtConfig({
  app: {
    head: {
      title: 'CaCatHead',
      htmlAttrs: {
        lang: 'zh-Hans-CN',
      },
      link: [{ rel: 'icon', href: '/favicon.ico' }],
      meta: [
        {
          name: 'description',
          content: '猫猫头 CaCatHead 是一个开源的在线评测系统。',
        },
      ],
    },
  },
  image: {
    provider: 'ipx',
    presets: {
      default: {
        modifiers: {
          format: 'webp',
        },
      },
    },
    ipx: {
      maxAge: 2592000,
    },
  },
  css: ['@/assets/main.css'],
  runtimeConfig: {
    API_BASE,
    proxy: {
      options: {
        target: API_BASE,
        changeOrigin: true,
        pathFilter: ['/api/'],
      },
    },
  },
  routeRules: {
    // See https://github.com/nuxt/framework/issues/9318
    // Cache 30 days
    '/_nuxt/**': {
      headers: cacheControlHeader(2592000),
    },
    '/shiki/**': {
      headers: cacheControlHeader(2592000),
    },
    // Cache 30 days
    '/favicon.png': {
      headers: cacheControlHeader(2592000),
    },
    // Contest pages cache policy
    '/contest/*/problem/**': {
      headers: cacheControlHeader(60),
    },
    '/contest/*/': {
      headers: cacheControlHeader(5),
    },
    '/contest/*/submit': {
      headers: cacheControlHeader(5),
    },
    '/contest/*/status': {
      headers: cacheControlHeader(5),
    },
    '/contest/*/submissions': {
      headers: cacheControlHeader(5),
    },
    '/contest/*/standings': {
      headers: cacheControlHeader(5),
    },
    // Repository pages cache policy
    '/repository/*/problem/**': {
      headers: cacheControlHeader(24 * 60 * 60),
    },
    '/repository/*/submissions': {
      headers: cacheControlHeader(5),
    },
  },
  experimental: {
    // See https://github.com/nuxt/framework/issues/8306
    // Make it works with nginx
    writeEarlyHints: false,
    // See https://github.com/unocss/unocss/issues/1806
    // See https://github.com/unocss/unocss/issues/1545
    // Make it works with unocss
    inlineSSRStyles: false,
  },
  modules: [
    'nuxt-proxy',
    '@unocss/nuxt',
    '@pinia/nuxt',
    '@vueuse/nuxt',
    '@nuxt/image-edge',
    '@nuxtjs/device',
    // '@nuxtjs/fontaine', // TODO: not work with katex
  ],
  unocss: {
    preflight: true,
    presets: [
      presetUno(),
      presetAttributify(),
      presetIcons({
        scale: 1.1,
        extraProperties: {
          height: '1em',
          'flex-shrink': '0',
          display: 'inline-block',
        },
      }),
      presetWebFonts({
        provider: 'google',
        fonts: {
          sans: ['Inter', 'Noto Sans Simplified Chinese'],
          mono: 'Input Mono',
        },
      }),
      presetTypography(),
    ],
    transformers: [transformerDirectives(), transformerVariantGroup()],
    shortcuts: {
      'border-base': 'border-gray/40 dark:border-gray/40',
      'text-base-50': 'text-neutral-50 dark:text-light-50',
      'text-base-100': 'text-neutral-100 dark:text-light-100',
      'text-base-200': 'text-neutral-200 dark:text-light-200',
      'text-base-300': 'text-neutral-300 dark:text-light-300',
      'text-base-400': 'text-neutral-400 dark:text-light-400',
      'text-base-500': 'text-neutral-500 dark:text-light-500',
      'text-base-600': 'text-neutral-600 dark:text-light-600',
      'text-base-700': 'text-neutral-700 dark:text-light-700',
      'text-base-800': 'text-neutral-800 dark:text-light-800',
      'text-base-900': 'text-neutral-900 dark:text-light-900',
    },
    theme: {
      colors: {
        'main-50': '#fafafa',
        'main-100': '#f5f5f5',
        'main-200': '#e5e5e5',
        'main-300': '#d4d4d4',
        'main-400': '#a3a3a3',
        'main-500': '#737373',
        'main-600': '#525252',
        'main-700': '#404040',
        'main-800': '#262626',
        'main-900': '#171717',
      },
      boxShadow: {
        box: '0 2px 3px rgb(10 10 10 / 10%), 0 0 0 1px rgb(10 10 10 / 10%)',
      },
    },
  },
  hooks: {
    async 'build:before'() {
      try {
        const srcDir = './node_modules/shiki/languages/';
        const dstDir = './public/shiki/languages/';
        const languages = await fs.readdir(srcDir);
        await fs.ensureDir(dstDir);
        const tasks: Promise<void>[] = [];
        for (const lang of languages) {
          if (lang.endsWith('.json')) {
            tasks.push(
              fs.copyFile(
                './node_modules/shiki/languages/' + lang,
                './public/shiki/languages/' + lang
              )
            );
          }
        }
        await Promise.all(tasks);
      } catch (error: any) {
        console.error(error);
      }
    },
  },
  vite: {
    define: {
      // Fix shiki
      'process.env.VSCODE_TEXTMATE_DEBUG': 'false',
    },
  },
});

function cacheControlHeader(time: number) {
  if (ENABLE_CACHE) {
    return {
      'Cache-Control': `max-age=${time}, immutable, public, s-maxage=${time}`,
    };
  } else {
    return {};
  }
}
