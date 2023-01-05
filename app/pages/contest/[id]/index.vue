<script setup lang="ts">
import type { FullContest } from '@/composables/types';

const route = useRoute();

const props = defineProps<{ contest: FullContest }>();

const { contest } = toRefs(props);
</script>

<template>
  <div>
    <c-table :data="contest.problems">
      <template #headers>
        <c-table-header name="display_id" width="80">#</c-table-header>
        <c-table-header name="title" align="left" text-left
          >标题</c-table-header
        >
      </template>
      <template #display_id="{ row }">{{
        displyaIdToIndex(row.display_id)
      }}</template>
      <template #title="{ row }">
        <nuxt-link
          :to="`/contest/${route.params.id}/problem/${displyaIdToIndex(
            row.display_id
          )}`"
          class="text-link"
          >{{ row.title }}</nuxt-link
        >
      </template>
    </c-table>
  </div>
</template>
