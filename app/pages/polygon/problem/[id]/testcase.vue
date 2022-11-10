<script setup lang="ts">
import type { FullPolygonProblem } from '@/composables/types';

const props = defineProps<{ problem: FullPolygonProblem }>();

const { problem } = toRefs(props);

const files = ref<File[]>([]);

const onUploadTestcase = (ev: Event) => {
  const target = ev.target as HTMLInputElement;
  const uploaded = target.files;
};
</script>

<template>
  <div>
    <div>
      <c-file-input id="testcase" @change="onUploadTestcase" multiple
        >上传测试用例</c-file-input
      >
    </div>
    <div>
      <div v-for="file in files">
        <span>{{ file.name }}</span>
      </div>
    </div>
  </div>
</template>
