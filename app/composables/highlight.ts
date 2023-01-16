import {
  Highlighter,
  getHighlighter,
  setCDN,
  setWasm,
  Lang,
  IShikiTheme,
} from 'shiki-es';

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
      setCDN('');
    } else {
      const { default: OnigUrl } = await import(
        // @ts-ignore
        '~/node_modules/shiki/dist/onig.wasm?url'
      );
      setWasm(await fetch(OnigUrl).then(res => res.arrayBuffer()));
      setCDN('/shiki/');
    }
    // @ts-ignore
    themes.push(await import('~/assets/shiki/themes/eva-light.json'));
    // @ts-ignore
    themes.push(await import('~/assets/shiki/themes/eva-dark.json'));

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
      return (await setup(lang)).codeToHtml(code, {
        lang,
        theme: isDark ? 'Eva Dark' : 'Eva Light',
      });
    } else {
      return renderText();
    }
  }
}
