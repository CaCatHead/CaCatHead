<script setup lang="ts">
const authUser = useAuthUser();

useHead({
  title: '登录',
});

const route = useRoute();

definePageMeta({
  middleware: ['auth', 'redirect'],
});

const notify = useNotification();

const username = ref('');
const password = ref('');
const login = async () => {
  try {
    const resp = await $fetch<{ token: string; expiry: string }>(
      '/api/auth/login',
      {
        method: 'POST',
        body: {
          username: username.value.trim(),
          password: password.value,
        },
      }
    );
    const token = resp.token;
    const expiry = resp.expiry;
    await authUser.setToken(token, expiry);

    if (!!route.query.redirect && typeof route.query.redirect === 'string') {
      await navigateTo(route.query.redirect, { replace: true });
    } else {
      await navigateTo('/', { replace: true });
    }
  } catch (error: any) {
    // show error message
    notify.danger(error?.response?._data?.detail ?? '未知错误');
  }
};
</script>

<template>
  <div>
    <h2 text-2xl font-bold>登录</h2>
    <form class="block" @submit.prevent="login" mt4>
      <c-input
        id="username"
        type="text"
        color="info"
        v-model="username"
        :tab-index="1"
      >
        <template #label><label for="username">用户名</label></template>
      </c-input>
      <c-input
        mt4
        id="password"
        type="password"
        color="info"
        v-model="password"
        :tab-index="2"
      >
        <template #label><label for="password">密码</label></template>
      </c-input>
    </form>
    <div mt4>
      <c-button color="success" @click="login" :tab-index="3">登录</c-button>
    </div>
  </div>
</template>
