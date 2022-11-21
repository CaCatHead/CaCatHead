import type { Ref } from 'vue';

export interface CNavContext {
  prefix: Ref<string>;
}

export const CNAV = Symbol('c-nav');

export const useCNavContext = () => inject<CNavContext>(CNAV)!;
