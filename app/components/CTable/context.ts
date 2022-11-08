import type { Ref } from 'vue';

export interface CTableColumn {
  name: string;
  width?: number | string;
  class: string | string[];
}

export interface CTableContext {
  columns: Ref<CTableColumn[]>;
}

export const CTABLE = Symbol('c-table');

export const useCTableContext = () => inject<CTableContext>(CTABLE)!;
