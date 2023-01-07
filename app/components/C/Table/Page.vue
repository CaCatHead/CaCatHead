<script setup lang="ts">
const props = withDefaults(
  defineProps<{ count: number; page?: number; pageSize: number }>(),
  { page: 1 }
);

const emit = defineEmits<{
  (e: 'change', page: number): Promise<void>;
}>();

const { count, pageSize } = toRefs(props);
const page = ref(props.page);

const first = 0;
const pageView = 5;
const last = computed(() => Math.ceil(count.value / pageSize.value));

const prePage = async () => {
  if (page.value - 1 >= first) {
    await emit('change', page.value - 1);
    page.value -= 1;
  }
};
const nextPage = async () => {
  if (page.value + 1 < last.value) {
    await emit('change', page.value + 1);
    page.value += 1;
  }
};
const goPage = async (to: number) => {
  if (first <= to && to < last.value) {
    await emit('change', to);
    page.value = to;
  }
};
</script>

<template>
  <div class="flex justify-center" space-x-2>
    <c-button
      padding="p-2"
      @click="prePage"
      :disabled="page <= first"
      color="info"
      variant="outline"
      icon="i-mdi-chevron-left"
    ></c-button>

    <template v-if="last - first <= pageView">
      <c-button
        v-for="index in last - first"
        :key="index"
        color="info"
        :variant="index + first === page + 1 ? 'fill' : 'outline'"
        @click="goPage(index + first - 1)"
      >
        <span>{{ index + first }}</span>
      </c-button>
    </template>
    <template v-else-if="page - first < pageView">
      <c-button
        v-for="index in pageView"
        :key="index"
        color="info"
        :variant="index + first === page + 1 ? 'fill' : 'outline'"
        @click="goPage(index + first - 1)"
      >
        <span>{{ index + first }}</span>
      </c-button>
      <span
        v-if="pageView + 1 < last"
        class="select-none inline-flex justify-center items-center py-2 md:px-2"
        >...</span
      >
      <c-button color="info" variant="outline" @click="goPage(last - 1)">{{
        last
      }}</c-button>
    </template>
    <template v-else-if="last - page <= pageView">
      <c-button color="info" variant="outline" @click="goPage(first)">{{
        first + 1
      }}</c-button>
      <span
        v-if="last - pageView > 1"
        class="select-none inline-flex justify-center items-center py-2 md:px-2"
        >...</span
      >
      <c-button
        v-for="index in pageView"
        :key="index"
        color="info"
        :variant="last - pageView + index === page + 1 ? 'fill' : 'outline'"
        @click="goPage(last - pageView + index - 1)"
      >
        <span>{{ last - pageView + index }}</span>
      </c-button>
    </template>
    <template v-else>
      <c-button color="info" variant="outline" @click="goPage(first)">{{
        first + 1
      }}</c-button>
      <span
        class="select-none inline-flex justify-center items-center py-2 md:px-2"
        >...</span
      >
      <c-button
        v-for="index in pageView"
        :key="index"
        color="info"
        :variant="
          page - Math.floor(pageView / 2) + index === page + 1
            ? 'fill'
            : 'outline'
        "
        @click="goPage(page - Math.floor(pageView / 2) + index - 1)"
      >
        <span>{{ page - Math.floor(pageView / 2) + index }}</span>
      </c-button>
      <span
        class="select-none inline-flex justify-center items-center py-2 md:px-2"
        >...</span
      >
      <c-button color="info" variant="outline" @click="goPage(last - 1)">{{
        last
      }}</c-button>
    </template>

    <c-button
      padding="p-2"
      @click="nextPage"
      :disabled="page + 1 >= last"
      color="info"
      variant="outline"
      icon="i-mdi-chevron-right"
    ></c-button>
  </div>
</template>
