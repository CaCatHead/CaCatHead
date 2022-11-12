<script setup lang="ts">
useHead({
  title: '注册',
});

const username = ref('');
const email = ref('');
const password = ref('');
const register = async () => {
  try {
    await $fetch<{ token: string; expiry: string }>('api/auth/register', {
      method: 'POST',
      body: {
        username: username.value,
        email: email.value,
        password: password.value,
      },
    });
    await navigateTo('/login');
  } catch (error) {
    // show error message
  }
};
</script>

<template>
  <div>
    <h2 text-2xl font-bold>注册</h2>
    <div mt4>
      <c-input id="username" type="text" color="info" v-model="username">
        <template #label><label for="username">用户名</label></template>
      </c-input>
      <c-input id="email" type="email" color="info" v-model="email">
        <template #label><label for="email">邮箱</label></template>
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
      <c-button color="success" @click="register">注册</c-button>
    </div>
  </div>
</template>
