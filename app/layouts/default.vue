<script setup lang="ts">
import { ABtn } from 'anu-vue';
</script>

<template>
  <div pl="$main-padding" pr="$main-padding">
    <div h="64px" mt="4">
      <div h-full flex items-center>
        <NuxtLink to="/" h-full flex items-center select-none cursor-pointer>
          <img src="/favicon.png" alt="CaCatHead Icon" h-full />
          <span ml4 text-2xl font-bold>CaCatHead</span>
        </NuxtLink>
        <div flex-auto></div>
        <div>
          <NuxtLink to="/login">
            <ABtn variant="text" color="info">登录</ABtn>
          </NuxtLink>
        </div>
      </div>
    </div>

    <nav mt4 h="48px" flex gap4 items-center border="~ 1" rounded p4>
      <div>
        <NuxtLink to="/">主页</NuxtLink>
      </div>
      <div>
        <NuxtLink to="/contest/">比赛</NuxtLink>
      </div>
      <div>
        <NuxtLink to="/repository/">题库</NuxtLink>
      </div>
      <div>
        <NuxtLink to="/help">帮助</NuxtLink>
      </div>
    </nav>

    <div mt4>
      <slot></slot>
    </div>
  </div>
</template>
