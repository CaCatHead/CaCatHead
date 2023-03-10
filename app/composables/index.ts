import type { Ref } from 'vue';
import type { FetchOptions } from 'ohmyfetch';

import { defineStore } from 'pinia';

import type { FullUser, ProblemRepository } from './types';

import { useNotification } from './notify';

// Use cookie to store auth token
export const useToken = () => useCookie('cacathead-auth');

// Fetch API
export const fetchAPI = <T>(
  url: string,
  options?: FetchOptions & { notify?: ReturnType<typeof useNotification> }
) => {
  return $fetch<T>(url, {
    ...options,
    baseURL: useRuntimeConfig().API_BASE,
    headers: {
      ...options?.headers,
    },
    // @ts-ignore
    async onResponseError({ response }) {
      if (!options?.notify) return;
      if (response.status === 400 || response.status === 404) {
        console.log(response._data);
        if (typeof response?._data?.detail === 'string') {
          options.notify.danger(response?._data?.detail);
        } else {
          options.notify.danger('未知错误');
        }
      }
    },
  } as any);
};

// Use url as the asyncData key
export const useFetchAPI: typeof useFetch = (url: any, options: any) => {
  const token = useToken();
  const headers = { ...useRequestHeaders(['cookie']), ...options?.headers };

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
  const user = ref<FullUser | undefined>();
  const repos = ref<ProblemRepository[]>([]);

  const isLogin = computed(() => {
    return user.value !== undefined && user.value !== null;
  });

  const fetchUser = async (): Promise<FullUser | undefined> => {
    const cookie = useToken();
    if (cookie.value) {
      try {
        const { data } = await useFetch<{
          user: FullUser;
          repos: ProblemRepository[];
        }>(`/api/user/profile`, {
          key: `profile_${cookie.value}`,
          headers: useRequestHeaders(['cookie']),
          baseURL: useRuntimeConfig().API_BASE,
        });

        if (!data.value) {
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
    await fetchUser();
  };

  const logout = async () => {
    const cookie = useToken();
    await useFetchAPI('/api/auth/logout', {
      method: 'POST',
      key: `logout_${cookie.value}`,
    });
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
    setToken,
    isLogin,
    fetchUser,
    logout,
  };
});
