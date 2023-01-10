<script setup lang="ts">
const route = useRoute();

const isDark = useDark();
const toggleDark = useToggle(isDark);

const authUser = useAuthUser();
await authUser.fetchUser();
const user = computed(() => authUser.user!);

provide(AuthUserKey, user);

const logout = async () => {
  await authUser.logout();
  await navigateTo('/');
};

const activeTab = computed(() => {
  const p = route.fullPath;
  if (p.startsWith('/contest')) {
    return 'contest';
  } else if (p.startsWith('/post')) {
    return 'post';
  } else if (p.startsWith('/repository')) {
    return 'repository';
  } else if (p.startsWith('/help')) {
    return 'help';
  } else if (p === '/') {
    return 'home';
  } else if (p.startsWith('/polygon')) {
    return 'polygon';
  } else {
    return '';
  }
});

const { data: repos } = await useFetchAPI<{ repos: any[] }>('/api/repos');
</script>

<template>
  <div flex justify-center px="$main-padding-y">
    <div min-h-screen pt4 w="$main-max-width" max-w="$main-max-width">
      <div h="64px">
        <div h-full flex items-center>
          <NuxtLink to="/" h-full flex items-center select-none cursor-pointer>
            <nuxt-img
              src="/favicon.png"
              alt="CaCatHead Icon"
              h-full
              preset="default"
            />
            <span ml4 lt-md:ml1 text-2xl font-bold>CaCatHead</span>
          </NuxtLink>
          <div flex-auto></div>
          <div>
            <div
              v-if="authUser.isLogin"
              flex
              items-center
              justify-center
              gap4
              lt-md:gap1
            >
              <c-button color="info" variant="text">{{
                user.nickname
              }}</c-button>
              <c-button color="danger" variant="outline" text-sm @click="logout"
                >退出</c-button
              >
            </div>
            <div v-else space-x-4 lt-md:space-x-1>
              <c-button color="info" variant="fill">
                <NuxtLink block to="/login">登录</NuxtLink>
              </c-button>
              <c-button color="success" variant="outline" lt-md:hidden>
                <NuxtLink block to="/register">注册</NuxtLink>
              </c-button>
            </div>
          </div>
        </div>
      </div>

      <nav
        h="16"
        mt4
        pl4
        flex
        gap4
        lt-md:gap0
        items-center
        shadow-box
        rounded
        select-none
      >
        <div :class="['default-nav-item', activeTab === 'home' && 'is-active']">
          <NuxtLink to="/">主页</NuxtLink>
        </div>
        <div :class="['default-nav-item', activeTab === 'post' && 'is-active']">
          <NuxtLink to="/post/">博客</NuxtLink>
        </div>
        <div
          :class="['default-nav-item', activeTab === 'contest' && 'is-active']"
        >
          <NuxtLink to="/contests/">比赛</NuxtLink>
        </div>
        <div
          :class="[
            'default-nav-item',
            activeTab === 'repository' && 'is-active',
          ]"
        >
          <NuxtLink to="/repository/" relative class="[&:hover>div]:block">
            <span>题库</span>
            <div hidden absolute top-full left="-1" w-36 pt3 font-normal>
              <div
                rounded
                border="1 base"
                divide-y
                dark:divide="gray/40"
                bg-white
                dark:bg-dark
              >
                <div v-for="repo in repos?.repos" p2>
                  <nuxt-link :to="`/repository/${repo.id}`" text-link>{{
                    repo.name
                  }}</nuxt-link>
                </div>
              </div>
            </div>
          </NuxtLink>
        </div>

        <div
          v-if="user && user.permissions.polygon"
          :class="[
            'default-nav-item',
            'lt-md:!min-w-16',
            activeTab === 'polygon' && 'is-active',
          ]"
        >
          <NuxtLink to="/polygon">Polygon</NuxtLink>
        </div>

        <div :class="['default-nav-item', activeTab === 'help' && 'is-active']">
          <NuxtLink to="/help">帮助</NuxtLink>
        </div>
      </nav>

      <div mt12 mb12 w-full>
        <slot></slot>
      </div>

      <footer block pb8 w-full text-center text-base-500>
        <div border="b-2 base" mb8></div>
        <div flex="~ gap2" mb2 items-center justify-center text-lg>
          <button
            icon-btn
            i-carbon-sun
            dark:i-carbon-moon
            lt-md:text-sm
            text-base
            @click="toggleDark()"
          />
          <nuxt-link
            i-carbon-bare-metal-server
            icon-btn
            text-gray-500
            hover:text="$c-brand"
            to="/nodes"
          ></nuxt-link>
          <a
            i-carbon-logo-github
            icon-btn
            text-gray-500
            hover:text="$c-brand"
            :href="`https://github.com/XLoJ/CaCatHead`"
            target="_blank"
          ></a>
          <a
            i-carbon-document
            icon-btn
            text-gray-500
            hover:text="$c-brand"
            :href="`https://oj-docs.onekuma.cn/`"
            target="_blank"
          ></a>
          <a
            i-carbon-gui-management
            icon-btn
            text-gray-500
            hover:text="$c-brand"
            href="/admin"
            target="_blank"
            v-if="
              user &&
              (user.permissions.is_superuser || user.permissions.is_staff)
            "
          ></a>
        </div>
        <div flex items-center justify-center gap1 align-middle>
          <span i-ic-round-electric-bolt class="text-gray-500/50"></span>
          <span
            >Powered by
            <a
              :href="`https://github.com/XLoJ/CaCatHead`"
              target="_blank"
              text-link
              >CaCatHead</a
            >
          </span>
        </div>
      </footer>
    </div>
  </div>
</template>

<style>
:root {
  --main-padding-y: 4rem;
  --main-max-width: 64rem;
}

@media (max-width: 767px) {
  :root {
    --main-padding-y: 0rem;
    --main-max-width: calc(100vw - 2rem);
  }
}

.default-nav-item {
  --at-apply: px1 py1 flex items-center;
  --at-apply: border-b border-b-3 border-transparent lt-sm:border-b-2;
  --at-apply: text-base-500;
  --at-apply: lt-md:min-w-10 lt-md:w-auto;
}

.default-nav-item > a {
  --at-apply: p1;
}

.default-nav-item:hover {
  --at-apply: text-base-700;
}

.is-active {
  --at-apply: border-b border-b-3 border-sky-500 lt-sm:border-b-2;
  --at-apply: font-bold text-base-900;
}
</style>
