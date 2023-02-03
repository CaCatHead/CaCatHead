import type { format } from 'wastyle';
import type { Highlighter, Lang, IShikiTheme } from 'shiki-es';

import EvaDark from '~/assets/shiki/themes/eva-dark.json';
import EvaLight from '~/assets/shiki/themes/eva-light.json';

// @ts-ignore
const themes: IShikiTheme[] = [EvaDark, EvaLight];
const registeredLang = ref(new Map<string, boolean>());

let shikiImport: Promise<void> | undefined;
let wastyleImport: Promise<void> | undefined;

const shiki = ref<Highlighter>();
const wastyleFormatter = ref<typeof format>();

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

async function setupWastyle() {
  try {
    const wastyle = await import('wastyle');
    // @ts-ignore
    const astyleBinaryUrl = (await import('wastyle/dist/astyle.wasm?url'))
      .default;
    await wastyle.init(astyleBinaryUrl);
    wastyleFormatter.value = wastyle.format;
  } catch (e) {
    console.error(e);
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

export function useFormatter() {
  if (!wastyleImport) {
    wastyleImport = setupWastyle();
  }
  return wastyleFormatter.value;
}

export function useShikiTheme() {
  return useColorMode().value === 'dark' ? 'Eva Dark' : 'Eva Light';
}

interface HighLightOption {
  tabwidth?: number;
  format?: boolean;
}

const DefaultFormatOption = [
  'style=java',
  'attach-namespaces',
  'attach-classes',
  'attach-inlines',
  'attach-extern-c',
  'attach-closing-while',
  'indent-col1-comments',
  'break-blocks',
  'pad-oper',
  'pad-comma',
  'pad-header',
  'unpad-paren',
  'align-pointer=name',
  'break-one-line-headers',
  'attach-return-type',
  'attach-return-type-decl',
  'convert-tabs',
  'close-templates',
  'max-code-length=100',
  'break-after-logical',
];

export function highlight(
  code: string,
  lang: string,
  { tabwidth = 2, format = false }: HighLightOption = {}
) {
  const shiki = useHightlighter(lang as Lang);
  const theme = useShikiTheme();

  const renderText = () => ({
    language: 'text',
    html: `<pre class="shiki"><code>${escapeCode(code)
      .split('\n')
      .map(l => `<span class="line">${l.trimEnd()}</span>`)
      .join('\n')}</code></pre>`,
    option: { tabwidth, format: false },
  });

  if (lang === 'text') {
    return renderText();
  } else if (shiki) {
    try {
      const formater = useFormatter();
      if (
        format &&
        formater &&
        (lang === 'c' || lang === 'cpp' || lang === 'java')
      ) {
        const [success, result] = formater(
          code,
          [
            ...DefaultFormatOption,
            `indent=spaces=${tabwidth}`,
            `mode=${lang === 'cpp' ? 'c' : lang}`,
          ].join(' ')
        );
        if (success) {
          format = true;
          code = result.trim();
        } else {
          format = false;
        }
      } else {
        format = false;
      }

      const html = shiki.codeToHtml(code, {
        lang,
        theme,
      });

      return { language: lang, html, option: { tabwidth, format } };
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
