<script setup lang="ts">
const route = useRoute();
const { data } = await useFetchAPI<{ post: any }>(
  `/api/post/${route.params.id}`
);
</script>

<template>
  <div>
    <Head>
      <Title>{{ data.post?.title ?? '公告' }}</Title>
    </Head>
  </div>
</template>
