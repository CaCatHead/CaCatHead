import {
  Highlighter,
  getHighlighter,
  setCDN,
  setWasm,
  Lang,
  IShikiTheme,
} from 'shiki-es';

import EvaDark from '~/assets/shiki/themes/eva-dark.json';
import EvaLight from '~/assets/shiki/themes/eva-light.json';

export let highlighter: Highlighter | undefined = undefined;

const themes: IShikiTheme[] = [];

const supportLangs: Lang[] = [
  'c',
  'cpp',
  'java',
  'javascript',
  'json',
  'python',
  'typescript',
  'yaml',
  'html',
  'css',
];

export const alias: Map<string, Lang> = new Map([
  ['c++', 'cpp'],
  ['C++', 'cpp'],
  ['C', 'c'],
  ['js', 'javascript'],
  ['ts', 'typescript'],
  ['py', 'python'],
]);

export function isLangSupport(lang: string): lang is Lang {
  return !!supportLangs.find(l => l === lang);
}

async function setup(...langs: Lang[]) {
  if (!highlighter) {
    if (process.server) {
      // SSR 渲染
      setCDN('');
    } else {
      // CSR 渲染
      const SHIKI_CDN = useRuntimeConfig().SHIKI_CDN;
      if (!!SHIKI_CDN) {
        setCDN(SHIKI_CDN);
      } else {
        // @ts-ignore
        const { default: OnigUrl } = await import('shiki/dist/onig.wasm?url');
        setWasm(await fetch(OnigUrl).then(res => res.arrayBuffer()));
        setCDN('/shiki/');
      }
    }

    // @ts-ignore
    themes.push(EvaDark);
    // @ts-ignore
    themes.push(EvaLight);

    return (highlighter = await getHighlighter({
      themes,
      langs,
    }));
  } else {
    return (highlighter = await getHighlighter({
      themes,
      langs,
    }));
  }
}

export async function preSetup() {
  await setup(supportLangs[0]);
  await Promise.all(supportLangs.slice(1).map(lang => setup(lang)));
  return setup(...supportLangs);
}

export function escapeCode(raw: string) {
  return raw.replace(/[<>"& ]/g, match => {
    switch (match) {
      case '<':
        return '&lt;';
      case '>':
        return '&gt;';
      case '"':
        return '&quot;';
      case '&':
        return '&amp;';
      case ' ':
        return '&nbsp;';
      default:
        return '';
    }
  });
}

export async function highlight(
  code: string,
  lang: string,
  isDark: boolean = false
) {
  const renderText = () =>
    `<pre class="shiki"><code>${escapeCode(code)
      .split('\n')
      .map(l => `<span class="line">${l}</span>`)
      .join('\n')}</code></pre>`;

  if (lang === 'text') {
    return renderText();
  } else {
    if (isLangSupport(lang)) {
      try {
        return (await setup(lang)).codeToHtml(code, {
          lang,
          theme: isDark ? 'Eva Dark' : 'Eva Light',
        });
      } catch (error: any) {
        console.error(error);
        return renderText();
      }
    } else {
      return renderText();
    }
  }
}
