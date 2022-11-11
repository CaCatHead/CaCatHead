import type { FetchOptions } from 'ohmyfetch';

import { defineStore } from 'pinia';

import type { User } from './types';

// Use cookie to store auth token
export const useToken = () => useCookie('token');

// Fetch API
export const fetchAPI = <T>(url: string, options?: FetchOptions) => {
  return $fetch<T>(url, {
    ...options,
    baseURL: useRuntimeConfig().API_BASE,
    headers: {
      ...options?.headers,
      Authorization: useToken().value,
    },
  });
};

// Use url as the asyncData key
export const useFetchAPI: typeof useFetch = (url: any, options: any) => {
  const token = useToken();
  const headers = token.value
    ? { ...options?.headers, Authorization: token.value }
    : { ...options?.headers };

  return useFetch(url, {
    key: token.value + '$' + url,
    ...options,
    headers,
    baseURL: useRuntimeConfig().API_BASE,
    async onResponseError({ response }) {
      if (response.status === 401) {
        await navigateTo({ path: '/login' });
      }
    },
  });
};

// Store auth user
export const useAuthUser = defineStore('AuthUser', () => {
  const cookie = useToken();
  const user = ref<User | undefined>();

  const isLogin = computed(() => {
    return user.value !== undefined && user.value !== null;
  });

  const fetchUser = async (): Promise<User | undefined> => {
    if (cookie.value) {
      try {
        const { data } = await useFetch<{ user: User }>(`/api/user/profile`, {
          key: `profile_${cookie.value}`,
          headers: {
            Authorization: cookie.value,
          },
          baseURL: useRuntimeConfig().API_BASE,
        });
        
        if (data.value === null) {
          cookie.value = '';
          user.value = undefined;
          await navigateTo({ path: '/login', query: { redirect: '' } });
          return undefined;
        } else {
          user.value = data.value.user;
          return data.value.user;
        }
      } catch {
        return undefined;
      }
    } else {
      return undefined;
    }
  };

  const setToken = async (token: string, _expiry: string) => {
    cookie.value = 'Token ' + token;
    await fetchUser();
  };

  const logout = async () => {
    await useFetchAPI('/api/auth/logout', {
      method: 'POST',
      key: `logout_${cookie.value}`,
    });
    cookie.value = '';
    user.value = undefined;
  };

  return {
    user,
    token: cookie,
    setToken,
    isLogin,
    fetchUser,
    logout,
  };
});
