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
  <div w-full flex="~ gap8 lt-md:col-reverse">
    <div w="4/5 lt-md:full">
      <c-table :data="problems.problems">
        <template #headers>
          <c-table-header
            name="id"
            label="#"
            width="80"
            row-class="text-center"
          ></c-table-header>
          <c-table-header name="title" label="标题"></c-table-header>
        </template>

        <template #id="{ row }">
          <span font-bold>{{ row.display_id }}</span>
        </template>
        <template #title="{ row }">
          <nuxt-link
            :to="`/repository/${route.params.repo}/problem/${row.display_id}/`"
            >{{ row.title }}</nuxt-link
          >
        </template>
      </c-table>
    </div>

    <div w="1/5 lt-md:full" overflow-auto pb2 shadow-box rounded p4>
      <div v-for="repo in repos.repos">
        <c-button
          variant="text"
          color="info"
          @click="navigateTo(`/repository/${repo.id}`)"
          >{{ repo.name }}</c-button
        >
      </div>
    </div>
  </div>
</template>
