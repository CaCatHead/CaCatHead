<script setup lang="ts">
const authUser = useAuthUser();

useHead({
  title: '登录',
});

const username = ref('');
const password = ref('');
const login = async () => {
  try {
    const resp = await $fetch<{ token: string; expiry: string }>(
      'api/auth/login',
      {
        method: 'POST',
        body: {
          username: username.value,
          password: password.value,
        },
      }
    );
    const token = resp.token;
    const expiry = resp.expiry;
    authUser.setToken(token, expiry);

    await navigateTo('/');
  } catch (error) {
    // show error message
  }
};
</script>

<template>
  <div>
    <h2 text-2xl font-bold>登录</h2>
    <div mt4>
      <c-input id="username" type="text" color="info" v-model="username">
        <template #label><label for="username">用户名</label></template>
      </c-input>
      <c-input
        mt4
        id="password"
        type="password"
        color="info"
        v-model="password"
      >
        <template #label><label for="password">密码</label></template>
      </c-input>
    </div>
    <div mt4>
      <c-button color="success" @click="login">登录</c-button>
    </div>
  </div>
</template>
