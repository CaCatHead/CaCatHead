export const useFetchAPI: typeof useFetch = (url: any, options: any) =>
  useFetch(url, { ...options, baseURL: useRuntimeConfig().API_BASE });
