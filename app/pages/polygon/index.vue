<script setup lang="ts">
useHead({
  title: 'Polygon',
});

const { data } = await useFetchAPI<{ problems: any[] }>(`/api/polygon/own`);
</script>

<template>
  <div>
    <div flex mb8 items-center>
      <div>
        <h2 text-2xl font-bold mb4>Polygon</h2>
        <h3 text-lg font-500>程序设计竞赛试题创建系统</h3>
      </div>
      <div flex-auto></div>
      <div>
        <c-button color="success" mr4 variant="outline">新建题目</c-button>
        <c-button color="success">上传题目</c-button>
      </div>
    </div>

    <c-table :data="data.problems">
      <template #headers>
        <c-table-header
          name="id"
          label="#"
          width="64px"
          row-class="text-center"
        ></c-table-header>
        <c-table-header
          name="title"
          label="标题"
          class="text-left"
        ></c-table-header>
        <c-table-header
          name="owner"
          label="创建者"
          row-class="text-center"
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
      <template #owner="{ row }">
        <user-link :user="row.owner"></user-link>
      </template>
    </c-table>
  </div>
</template>
