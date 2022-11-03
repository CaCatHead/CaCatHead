<script setup lang="ts">
import { AInput, ABtn } from 'anu-vue';
</script>

<template>
  <div>
    <div>
      <AInput id="username" value="" type="text">
        <template #label>
          <label for="a-input-uesrname">
            <span>用户名 </span>
            <span class="text-red">*</span>
          </label>
        </template>
      </AInput>
      <AInput id="password" value="" type="password">
        <template #label>
          <label for="a-input-password">
            <span>密码 </span>
            <span class="text-red">*</span>
          </label>
        </template>
      </AInput>
    </div>
    <div>
      <ABtn color="success">登录</ABtn>
    </div>
  </div>
</template>
