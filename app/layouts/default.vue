<script setup lang="ts">
const images = useAppConfig().images;
const title = useAppConfig().title;

const route = useRoute();

const isDark = useDark();
const toggleDark = useToggle(isDark);

const authUser = useAuthUser();
await authUser.fetchUser();
const user = computed(() => authUser.user!);

provide(AuthUserKey, user);

const logout = async () => {
  await Promise.all([authUser.logout(), navigateTo('/')]);
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

const lastSync = ref(useLocalStorage('global/last-sync-time', 0));
const cacheSync = ref(useLocalStorage('global/sync-time', 0));
const clientTimestamp = new Date();
const Expire = 60 * 60 * 1000;
const timestamp = process.server
  ? useTimestamp()
  : clientTimestamp.getTime() - lastSync.value <= Expire
  ? useTimestamp({ offset: cacheSync.value })
  : await fetchAPI<{ diff: number; timestamp: number }>(`/api/sync`, {
      method: 'GET',
      query: {
        timestamp: (clientTimestamp.getTime() / 1000).toFixed(0),
      },
    })
      .then(resp => {
        const nowTimeStamp = new Date().getTime();
        const serverClientRequestDiffTime = resp.diff;
        const serverTimestamp = resp.timestamp;
        const serverClientResponseDiffTime = nowTimeStamp - serverTimestamp;
        const diffTime =
          (serverClientRequestDiffTime + serverClientResponseDiffTime) / 2;

        lastSync.value = nowTimeStamp;
        cacheSync.value = resp.timestamp - clientTimestamp.getTime() - diffTime;

        return useTimestamp({
          offset: resp.timestamp - clientTimestamp.getTime() - diffTime,
        });
      })
      .catch(() => {
        return useTimestamp();
      });

provide(ServerTimestamp, timestamp);

const progress = ref(0);
const loading = ref(false);
provide(LoadingIndicatorSymbol, {
  loading,
  progress,
  start() {
    progress.value = 0;
    loading.value = true;
  },
  update(value) {
    if (value !== undefined && value !== null) {
      progress.value = value;
    } else {
      progress.value = Math.min(90, progress.value + 10);
    }
  },
  stop() {
    progress.value = 100;
    loading.value = false;
  },
});

const commit = useAppConfig().COMMIT_SHA;
</script>

<template>
  <div flex justify-center px="$main-padding-y">
    <loading-indicator
      :progress="progress"
      :loading="loading"
    ></loading-indicator>
    <div min-h-screen pt4 w="$main-max-width" max-w="$main-max-width">
      <div h="64px">
        <div h-full flex items-center>
          <NuxtLink to="/" h-full flex items-center select-none cursor-pointer>
            <nuxt-img
              :src="images.logo"
              alt="CaCatHead Icon"
              h-full
              preset="default"
            />
            <span ml4 lt-md:ml1 text-2xl font-bold>{{ title }}</span>
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
              <c-dropdown class="[&>.c-dropdown]:pt1 [&>.c-dropdown]:right-0">
                <nuxt-link :to="`/user/profile/${authUser.user?.username}`"
                  ><c-button
                    color="info"
                    variant="text"
                    border="!base"
                    class="!text-base-900 !font-bold hover:!bg-gray-200/40 !bg-gray-200/10"
                  >
                    <display-rating
                      :rating="user.rating"
                      :admin="
                        user.permissions.is_staff ||
                        user.permissions.is_superuser
                      "
                      >{{ user.nickname }}</display-rating
                    >
                  </c-button></nuxt-link
                >
                <template #dropdown>
                  <div
                    w-36
                    font-normal
                    rounded
                    border="1 base"
                    divide-y
                    dark:divide="gray/40"
                    bg-white
                    dark:bg-dark
                  >
                    <nuxt-link
                      to="/user/settings"
                      block
                      p2
                      text-link
                      class="rounded-t hover:bg-gray-200/40"
                      >设置</nuxt-link
                    >
                    <nuxt-link
                      v-if="
                        user.permissions.add_post ||
                        user.permissions.is_staff ||
                        user.permissions.is_superuser
                      "
                      to="/post/write"
                      block
                      p2
                      text-link
                      class="rounded-t hover:bg-gray-200/40"
                      >创建博客</nuxt-link
                    >
                    <span
                      cursor-pointer
                      to="/user/settings"
                      block
                      p2
                      text-link
                      class="rounded-b hover:bg-gray-200/40"
                      @click="logout()"
                      >退出</span
                    >
                  </div>
                </template>
              </c-dropdown>
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
        h16
        mt4
        pl4
        z10
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
          <NuxtLink to="/post/">公告</NuxtLink>
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
          <c-dropdown class="[&>.c-dropdown]:pt3 [&>.c-dropdown]:left--1">
            <NuxtLink to="/repository/">题库</NuxtLink>
            <template #dropdown>
              <div w-36 font-normal>
                <div
                  v-if="authUser.repos && authUser.repos.length > 1"
                  rounded
                  border="1 base"
                  divide-y
                  dark:divide="gray/40"
                  bg-white
                  dark:bg-dark
                >
                  <nuxt-link
                    v-for="repo in authUser.repos"
                    :to="`/repository/${repo.id}`"
                    block
                    text-link
                    p2
                    z10
                    class="hover:bg-gray-200/40"
                    >{{ repo.name }}</nuxt-link
                  >
                </div>
              </div></template
            >
          </c-dropdown>
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
        <div mb2 flex="~ gap2" items-center justify-center text-lg>
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
            v-if="!commit"
            i-carbon-logo-github
            icon-btn
            text-gray-500
            hover:text="$c-brand"
            :href="`https://github.com/CaCatHead/CaCatHead`"
            target="_blank"
          ></a>
          <a
            i-carbon-document
            icon-btn
            text-gray-500
            hover:text="$c-brand"
            :href="`https://docs.cacathead.cn/`"
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
        <div v-if="commit" flex items-center justify-center gap1 align-middle>
          <a
            i-carbon-logo-github
            class="text-gray-500/50 hover:text-gray-500"
            :href="`https://github.com/CaCatHead/CaCatHead/tree/${commit}`"
            target="_blank"
          ></a>
          <a
            :href="`https://github.com/CaCatHead/CaCatHead/tree/${commit}`"
            target="_blank"
            text-link
            >{{ commit.slice(0, 7) }}
          </a>
        </div>
        <div flex items-center justify-center gap1 align-middle>
          <span i-ic-round-electric-bolt class="text-gray-500/50"></span>
          <span
            >Powered by
            <a
              :href="`https://github.com/CaCatHead/CaCatHead`"
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
