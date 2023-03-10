<script setup lang="ts">
import type { FullContest, ContestExtraInfo } from '@/composables/types';

const route = useRoute();

const notify = useNotification();

const props = defineProps<{
  contest: FullContest;
  extra_info: ContestExtraInfo | null;
}>();

const { contest } = toRefs(props);

const file = ref([] as File[]);

const uploadTeams = async () => {};
</script>

<template>
  <div>
    <div space-x-2>
      <c-file-input
        id="teams"
        v-model="file"
        accept=".csv"
        @change="uploadTeams"
        >导入队伍列表</c-file-input
      >
    </div>
    <div></div>
  </div>
</template>
