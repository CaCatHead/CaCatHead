import type { Ref, InjectionKey } from 'vue';

export const CModalSymbol = Symbol('c-modal-provider') as InjectionKey<{
  show: Ref<boolean>;
}>;
