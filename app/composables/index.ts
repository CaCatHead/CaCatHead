import { defineStore } from 'pinia';

// Use cookie to store auth token
export const useToken = () => useCookie('token');

// Use url as the asyncData key
export const useFetchAPI: typeof useFetch = (url: any, options: any) => {
  const token = useToken();
  const headers = token.value
    ? { ...options?.headers, Authorization: token.value }
    : { ...options?.headers };

  return useFetch(url, {
    key: url,
    ...options,
    headers,
    baseURL: useRuntimeConfig().API_BASE,
  });
};

// Store auth user
export const useAuthUser = defineStore('AuthUser', () => {
  const cookie = useToken();
  const user = ref();

  const setToken = (token: string, _expiry: string) => {
    cookie.value = 'Token ' + token;
  };

  const isLogin = computed(() => {
    return user.value !== undefined && user.value !== null;
  });

  const fetchUser = async () => {
    if (cookie.value) {
      try {
        const { data } = await useFetchAPI<{ user: any }>(`/api/user/profile`);
        user.value = data.value.user;
        return data.value.user;
      } catch {
        return undefined;
      }
    } else {
      return undefined;
    }
  };

  return {
    user,
    token: cookie,
    setToken,
    isLogin,
    fetchUser,
  };
});
