import type { Ref } from 'vue';

export interface CTableColumn {
  name: string;
  disabled: Ref<boolean>;
  label: string;
  width?: number | string;
  class: string | string[];
  align: 'left' | 'right' | 'center';
  slots: ReturnType<typeof useSlots>;
}

export interface CTableContext {
  columns: Ref<CTableColumn[]>;
  mobile: Ref<boolean>;
  border: Ref<boolean>;
}

export const CTABLE = Symbol('c-table');

export const useCTableContext = () => inject<CTableContext>(CTABLE)!;
