<script setup lang="ts">
const { data } = await useFetchAPI<{ problems: any[] }>(`/api/polygon/own`);
</script>

<template>
  <div>
    <h2 text-xl font-bold mb8>我的题目</h2>

    <c-table :data="data.problems">
      <template #headers>
        <c-table-header
          name="title"
          label="标题"
          class="text-left"
        ></c-table-header>
      </template>

      <template #title="{ row }">
        <nuxt-link
          :to="`/polygon/problem/${row.display_id}/`"
          text-sky-700
          text-op-80
          hover:text-op-100
          >{{ row.title }}</nuxt-link
        >
      </template>
    </c-table>
  </div>
</template>
