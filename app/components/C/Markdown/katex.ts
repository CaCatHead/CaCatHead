import type { KatexOptions } from 'katex';
// @ts-ignore
import katex from 'katex';

export function createKatexRender(options: KatexOptions = {}) {
  // set KaTeX as the renderer for markdown-it-simplemath
  const inlineRenderer = function (latex: string) {
    options.displayMode = false;
    try {
      return katex.renderToString(latex, options);
    } catch (error) {
      if (options.throwOnError) console.warn(error);
      return latex;
    }
  };

  const blockRenderer = function (latex: string) {
    options.displayMode = true;
    try {
      return `<p>${katex.renderToString(latex, options)}</p>`;
    } catch (error) {
      if (options.throwOnError) console.warn(error);
      return latex;
    }
  };

  return { inlineRenderer, blockRenderer };
}
