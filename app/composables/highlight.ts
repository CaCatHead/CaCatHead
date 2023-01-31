import type { Highlighter, Lang, IShikiTheme } from 'shiki-es';

import EvaDark from '~/assets/shiki/themes/eva-dark.json';
import EvaLight from '~/assets/shiki/themes/eva-light.json';

// @ts-ignore
const themes: IShikiTheme[] = [EvaDark, EvaLight];

const shiki = ref<Highlighter>();

const registeredLang = ref(new Map<string, boolean>());

let shikiImport: Promise<void> | undefined;

export const alias: Map<string, Lang> = new Map([
  ['c++', 'cpp'],
  ['C++', 'cpp'],
  ['C', 'c'],
  ['js', 'javascript'],
  ['ts', 'typescript'],
  ['py', 'python'],
]);

async function setup(...langs: Lang[]) {
  const { getHighlighter, setCDN, setWasm } = await import('shiki-es');

  if (process.server) {
    // SSR 渲染
    setCDN('');
  } else {
    // CSR 渲染
    // @ts-ignore
    const SHIKI_CDN = useAppConfig().SHIKI_CDN;
    if (!!SHIKI_CDN) {
      setCDN(SHIKI_CDN);
    } else {
      // @ts-ignore
      const { default: OnigUrl } = await import('shiki/dist/onig.wasm?url');
      setWasm(await fetch(OnigUrl).then(res => res.arrayBuffer()));
      setCDN('/shiki/');
    }
  }

  shiki.value = await getHighlighter({
    langs,
    themes,
  });
  for (const l of langs) {
    registeredLang.value.set(l, true);
  }
}

export function useHightlighter(lang: Lang) {
  if (!shikiImport) {
    shikiImport = setup('c', 'cpp');
  }

  if (!shiki.value) return undefined;

  if ((lang as string) !== 'text' && !registeredLang.value.get(lang)) {
    shiki.value
      .loadLanguage(lang)
      .then(() => {
        registeredLang.value.set(lang, true);
      })
      .catch(error => {
        console.error(error);
      });

    return undefined;
  }

  return shiki.value;
}

export function useShikiTheme() {
  return useColorMode().value === 'dark' ? 'Eva Dark' : 'Eva Light';
}

export function highlight(code: string, lang: string) {
  const shiki = useHightlighter(lang as Lang);
  const theme = useShikiTheme();

  const renderText = () => ({
    language: 'text',
    html: `<pre class="shiki"><code>${escapeCode(code)
      .split('\n')
      .map(l => `<span class="line">${l.trimEnd()}</span>`)
      .join('\n')}</code></pre>`,
  });

  if (lang === 'text') {
    return renderText();
  } else if (shiki) {
    try {
      const html = shiki.codeToHtml(code.replace('\t', '    '), {
        lang,
        theme,
      });
      return { language: lang, html };
    } catch (error) {
      console.error(error);
      return renderText();
    }
  } else {
    return renderText();
  }
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
