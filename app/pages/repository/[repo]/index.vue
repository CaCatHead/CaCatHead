<script setup lang="ts">
useHead({
  title: '题库',
});

const route = useRoute();
const { data: repos } = await useFetchAPI<{ repos: any[] }>('/api/repos');
const { data: problems } = await useFetchAPI<{ problems: any[] }>(
  `/api/repo/${route.params.repo}/problems`
);
</script>

<template>
  <div w-full>
    <div w-full overflow-auto pb2 border="b-2">
      <div v-for="repo in repos.repos" inline-block>
        <c-button variant="text" color="info">{{ repo.name }}</c-button>
      </div>
    </div>

    <div>
      <div v-for="problem in problems.problems" mt4>
        <span>{{ problem.display_id }}. </span>
        <span
          ><nuxt-link
            :to="`/repository/${route.params.repo}/problem/${problem.display_id}/`"
            >{{ problem.title }}</nuxt-link
          ></span
        >
      </div>
    </div>
  </div>
</template>
