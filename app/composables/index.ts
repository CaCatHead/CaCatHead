import type { Ref } from 'vue';
import type { FetchOptions } from 'ohmyfetch';

import { defineStore } from 'pinia';

import type { FullUser, ProblemRepository } from './types';

// Use cookie to store auth token
export const useToken = () => useCookie('token', { maxAge: 30 * 24 * 60 * 60 });

export const clearCookie = () => {};

// Fetch API
export const fetchAPI = <T>(url: string, options?: FetchOptions) => {
  return $fetch<T>(url, {
    ...options,
    baseURL: useRuntimeConfig().API_BASE,
    headers: {
      ...options?.headers,
      Authorization: useToken().value ?? '',
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
        token.value = '';
        await navigateTo({ path: '/login', replace: true });
      }
    },
  });
};

export const AuthUserKey = Symbol('cacathead-auth-user');

export const useUser = () => {
  return inject<Ref<FullUser>>(AuthUserKey);
};

// Store auth user
export const useAuthUser = defineStore('AuthUser', () => {
  const cookie = useToken();
  const user = ref<FullUser | undefined>();
  const repos = ref<ProblemRepository[]>([]);

  const isLogin = computed(() => {
    return user.value !== undefined && user.value !== null;
  });

  const fetchUser = async (): Promise<FullUser | undefined> => {
    if (cookie.value) {
      try {
        const { data } = await useFetch<{
          user: FullUser;
          repos: ProblemRepository[];
        }>(`/api/user/profile`, {
          key: `profile_${cookie.value}`,
          headers: {
            Authorization: cookie.value,
          },
          baseURL: useRuntimeConfig().API_BASE,
        });

        if (data.value === null) {
          cookie.value = '';
          user.value = undefined;
          await navigateTo({ path: '/login' });
          return undefined;
        } else {
          user.value = data.value.user;
          repos.value = data.value.repos;
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
    useCookie('csrftoken').value = '';
    useCookie('sessionid').value = '';

    user.value = undefined;
    const { data } = await useFetch<{ repos: ProblemRepository[] }>(
      '/api/repos',
      {
        key: `'/api/repos'`,
        baseURL: useRuntimeConfig().API_BASE,
      }
    );
    repos.value.splice(0, repos.value.length, ...(data.value?.repos ?? []));
  };

  return {
    user,
    repos,
    token: cookie,
    setToken,
    isLogin,
    fetchUser,
    logout,
  };
});
