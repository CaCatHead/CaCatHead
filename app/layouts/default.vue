<script setup lang="ts">
const router = useRouter();
</script>

<template>
  <div pl="$main-padding" pr="$main-padding">
    <div h="64px" mt="4">
      <div
        h-full
        flex
        items-center
        select-none
        cursor-pointer
        @click="() => router.push('/')"
      >
        <img src="/favicon.png" alt="CaCatHead Icon" h-full />
        <span ml4 text-2xl font-bold>CaCatHead</span>
      </div>
    </div>
    <nav mt4 h="48px" flex gap4 items-center border="~ 1" rounded p4>
      <div>
        <router-link to="/">主页</router-link>
      </div>
      <div>
        <router-link to="/contest/">比赛</router-link>
      </div>
      <div>
        <router-link to="/repository">题库</router-link>
      </div>
      <div>
        <router-link to="/help">帮助</router-link>
      </div>
    </nav>
    <div mt4>
      <slot></slot>
    </div>
  </div>
</template>
