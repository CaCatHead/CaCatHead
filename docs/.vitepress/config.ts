import { defineConfig } from 'vitepress';

export default defineConfig({
  lang: 'zh-CN',
  title: '猫猫头',
  description: '一个开源的在线评测系统',
  head: [
    ['meta', { name: 'theme-color', content: '#ffffff' }],
    ['link', { rel: 'icon', href: '/favicon.png' }],
  ],
  lastUpdated: true,
  themeConfig: {
    logo: '/favicon.png',
    editLink: {
      pattern: 'https://github.com/CaCatHead/CaCatHead/tree/main/docs/:path',
      text: '反馈修改建议',
    },
    footer: {
      message: 'Released under the AGPL-3.0 License.',
      copyright: 'Copyright © 2021-PRESENT XLor',
    },
    socialLinks: [
      { icon: 'github', link: 'https://github.com/CaCatHead/CaCatHead' },
    ],
    // algolia: {
    //   appId: 'FGCMJD7ZM9',
    //   apiKey: 'dad73f46ec1ba55810109fb2fa7a472b',
    //   indexName: 'docs',
    // },
    nav: [
      { text: '部署', link: '/deploy/' },
      { text: '使用文档', link: '/usage/' },
      { text: '体验', link: 'https://cacathead.cn' },
    ],
    sidebar: {
      '/': [
        {
          text: '介绍',
          items: [{ text: '猫猫头', link: '/intro/' }],
        },
        {
          text: '部署',
          items: [
            {
              text: '开始',
              link: '/deploy/',
            },
            {
              text: '本地开发',
              link: '/deploy/development',
            },
            {
              text: '本地部署',
              link: '/deploy/local',
            },
            {
              text: '服务器部署',
              link: '/deploy/server',
            },
            {
              text: '单独部署评测机',
              link: '/deploy/judge',
            },
          ],
        },
        {
          text: '使用',
          items: [
            {
              text: '使用文档',
              link: '/usage/',
            },
          ],
        },
        {
          text: '设计',
          items: [
            {
              text: '设计文档',
              link: '/design/',
            },
          ],
        },
      ],
    },
  },
});
