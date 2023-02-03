<script setup lang="ts">
import type { Post } from '@/composables/types';

const route = useRoute();

const user = useUser();

const { data: post } = await useFetchAPI<{ post: Post }>(
  `/api/post/${route.params.id}`
);

if (!post.value) {
  await navigateTo('/posts', { replace: true });
}
</script>

<template>
  <div v-if="post">
    <Head>
      <Title>{{ post.post.title }}</Title>
    </Head>
    <div flex justify-between>
      <h2 text-2xl font-bold>{{ post.post.title }}</h2>
      <div
        md:block
        v-if="
          post.post.owner.id === user?.id ||
          user?.permissions.is_staff ||
          user?.permissions.is_superuser
        "
      >
        <c-button
          icon="i-carbon-edit"
          variant="outline"
          @click="navigateTo(`/post/edit/${route.params.id}`)"
        ></c-button>
      </div>
    </div>
    <p mt2 text-sm font-light>
      <span>用户 </span>
      <user-link :user="post.post.owner" />
      <span>
        发表于<time-interval
          :left="post.post.created"
          :right="new Date()"
        ></time-interval
      ></span>
    </p>
    <div mt4 pl4 py2 border="l-4 base">
      <c-markdown :content="post.post.content"></c-markdown>
    </div>
  </div>
</template>
