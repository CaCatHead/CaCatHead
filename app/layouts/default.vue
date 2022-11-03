<script setup lang="ts">
const route = useRoute();

const isDark = useDark();
const toggleDark = useToggle(isDark);

const activeTab = computed(() => {
  const p = route.fullPath;
  if (p.startsWith('/contest')) {
    return 'contest';
  } else if (p.startsWith('/repository')) {
    return 'repository';
  } else if (p.startsWith('/help')) {
    return 'help';
  } else if (p === '/') {
    return 'home';
  } else {
    return '';
  }
});
</script>

<template>
  <div flex justify-center px="$main-padding-y">
    <div min-h-screen pt4 w="$main-max-width" max-w="$main-max-width" relative>
      <div h="64px">
        <div h-full flex items-center>
          <NuxtLink to="/" h-full flex items-center select-none cursor-pointer>
            <img src="/favicon.png" alt="CaCatHead Icon" h-full />
            <span ml4 text-2xl font-bold>CaCatHead</span>
          </NuxtLink>
          <div flex-auto></div>
          <div flex items-center justify-center>
            <c-button color="info" variant="fill">
              <NuxtLink block to="/login">登录</NuxtLink>
            </c-button>
            <c-button ml4 color="success" variant="outline" lt-md:hidden>
              <NuxtLink block to="/register">注册</NuxtLink>
            </c-button>
          </div>
        </div>
      </div>

      <nav
        mt4
        h="16"
        flex
        gap4
        items-center
        border="~ 2 base"
        rounded
        p="x4"
        select-none
      >
        <div :class="['default-nav-item', activeTab === 'home' && 'is-active']">
          <NuxtLink to="/">主页</NuxtLink>
        </div>
        <div
          :class="['default-nav-item', activeTab === 'contest' && 'is-active']"
        >
          <NuxtLink to="/contest/">比赛</NuxtLink>
        </div>
        <div
          :class="[
            'default-nav-item',
            activeTab === 'repository' && 'is-active',
          ]"
        >
          <NuxtLink to="/repository/">题库</NuxtLink>
        </div>
        <div :class="['default-nav-item', activeTab === 'help' && 'is-active']">
          <NuxtLink to="/help">帮助</NuxtLink>
        </div>
      </nav>

      <div mt12 mb12 px2>
        <slot></slot>
      </div>

      <footer absolute bottom-0 block pb8 w-full text-center text-base-500>
        <div border="b-2 base" mb8></div>
        <div>
          <span>
            <button
              icon-btn
              i-carbon-sun
              dark:i-carbon-moon
              lt-md:text-sm
              text-base
              @click="toggleDark()"
            />
          </span>
        </div>
        <div flex items-center justify-center gap1 align-middle>
          <a
            i-carbon-logo-github
            icon-btn
            text-gray-500
            hover:text="$c-brand"
            :href="`https://github.com/XLoJ/CaCatHead`"
            target="_blank"
          ></a
          ><a :href="`https://github.com/XLoJ/CaCatHead`" target="_blank"
            >CaCatHead</a
          >
        </div>
      </footer>
    </div>
  </div>
</template>

<style>
.default-nav-item {
  @apply px1 py1 flex items-center;
  @apply border-b border-b-3 border-transparent;
  @apply text-base-500;
}

.default-nav-item > a {
  @apply p1;
}

.default-nav-item:hover {
  @apply text-base-700;
}

.is-active {
  @apply border-b border-b-3 border-sky-500;
  @apply font-bold text-base-900;
}
</style>
