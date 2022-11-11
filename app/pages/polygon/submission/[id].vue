<script setup lang="ts">
const route = useRoute();

const { data } = await useFetchAPI<{ submission: any }>(
  `/api/polygon/submission/${route.params.id}`
);

if (data.value === null) {
  await navigateTo(`/polygon`);
}

const submission = ref(data.value!.submission);
</script>

<template>
  <div>
    <div shadow-box rounded>
      <c-table :data="[submission]">
        <template #headers>
          <c-table-header
            name="id"
            label="#"
            width="64px"
            row-class="text-center"
          ></c-table-header>
          <c-table-header
            name="created"
            label="提交时间"
            row-class="text-center"
          ></c-table-header>
          <c-table-header
            name="owner"
            label="用户"
            row-class="text-center"
          ></c-table-header>
          <c-table-header
            name="problem"
            label="题目"
            row-class="text-center"
          ></c-table-header>
          <c-table-header
            name="language"
            label="语言"
            row-class="text-center"
          ></c-table-header>
          <c-table-header
            name="verdict"
            label="结果"
            row-class="text-center"
          ></c-table-header>
        </template>

        <template #id="{ row }">
          <nuxt-link
            :to="`/polygon/submission/${row.id}`"
            text-sky-700
            text-op-70
            hover:text-op-100
            >{{ row.id }}</nuxt-link
          >
        </template>
        <template #created="{ row }">
          <span>{{ formatDateTime(row.created) }}</span>
        </template>
        <template #owner="{ row }">
          <user-link :user="row.owner"></user-link>
        </template>
        <template #problem="{ row }">
          <span>{{ row.problem.title }}</span>
        </template>
        <template #language="{ row }">{{ row.language }}</template>
        <template #verdict="{ row }">
          <verdict :verdict="row.verdict"></verdict>
        </template>
      </c-table>
    </div>
    <pre mt4 font-mono p4 shadow-box rounded>{{ submission.code }}</pre>
    <pre mt4 font-mono p4 shadow-box rounded>{{
      JSON.stringify(submission.detail, null, 2)
    }}</pre>
  </div>
</template>
