import 'github-markdown-css';
// @ts-ignore
import MarkdownIt from 'markdown-it';
// @ts-ignore
import MathPlugin from 'markdown-it-math';

import { createKatexRender } from './katex';

export interface MarkdownItOption {
  highlight?: (code: string, lang: string) => string;
}

export function createMarkdown(options: MarkdownItOption = {}) {
  const markdown = new MarkdownIt({
    html: true,
    linkify: true,
    typographer: true,
    highlight: options.highlight,
  });

  const { inlineRenderer, blockRenderer } = createKatexRender();
  markdown.use(MathPlugin, {
    inlineOpen: '$',
    inlineClose: '$',
    blockOpen: '$$',
    blockClose: '$$',
    inlineRenderer,
    blockRenderer,
  });

  return (raw: string) => {
    return markdown.render(raw);
  };
}
