import type { Ref, InjectionKey } from 'vue';

export interface LoadingIndicatorContext {
  loading: Ref<boolean>;

  progress: Ref<number>;

  start(): void;

  update(progress?: number): void;

  stop(): void;
}

export const LoadingIndicatorSymbol = Symbol(
  'loading-indicator'
) as InjectionKey<LoadingIndicatorContext>;

export const useLoadingIndicator = () => {
  return inject(LoadingIndicatorSymbol)!;
};
