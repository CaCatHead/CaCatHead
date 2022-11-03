// Use url as the asyncData key
export const useFetchAPI: typeof useFetch = (url: any, options: any) =>
  useFetch(url, { key: url, ...options, baseURL: useRuntimeConfig().API_BASE });
