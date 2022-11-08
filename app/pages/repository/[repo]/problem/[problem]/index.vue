<script setup lang="ts">
const route = useRoute();

interface Problem {
  display_id: number;
  title: string;
  problem_info: {
    problem_content: {
      description: string;
      input: string;
      output: string;
      sample: Array<{ input: string; answer: string }>;
      hint: string;
    };
  };
}

const { data } = await useFetchAPI<{ problem: Problem }>(
  `/api/repo/${route.params.repo}/problem/${route.params.problem}`
);

async function copyToClipboard(text: string) {
  await navigator.clipboard.writeText(text);
}
</script>

<template>
  <div class="w-full text-base prose prose-truegray">
    <Head>
      <Title>{{ data.problem.title }}</Title>
    </Head>

    <h2>{{ data.problem.display_id }}. {{ data.problem.title }}</h2>

    <h3>题目描述</h3>
    <p>{{ data.problem.problem_info.problem_content.description }}</p>

    <h3>输入格式</h3>
    <p>{{ data.problem.problem_info.problem_content.input }}</p>

    <h3>输出格式</h3>
    <p>{{ data.problem.problem_info.problem_content.output }}</p>

    <h3>样例</h3>
    <div w-full>
      <div
        v-for="(sample, index) in data.problem.problem_info.problem_content
          .sample"
        :key="index"
        class="mb4 w-full"
      >
        <div
          py1
          px2
          flex
          items-center
          justify-between
          select-none
          class="subtitle is-6 mb-0 border"
        >
          <span font-bold>输入</span>
          <c-button
            variant="text"
            color="info"
            text-sm
            @click="copyToClipboard(sample.input)"
            >复制</c-button
          >
        </div>
        <div>
          <pre border="l-1 r-1" my0 p2 bg="[#efefef]" rounded-0>{{
            sample.input
          }}</pre>
        </div>
        <div
          py1
          px2
          flex
          items-center
          justify-between
          select-none
          class="subtitle is-6 mb-0 border"
        >
          <span font-bold>输出</span>
          <c-button
            variant="text"
            color="info"
            text-sm
            @click="copyToClipboard(sample.answer)"
            >复制</c-button
          >
        </div>
        <div>
          <pre border="l-1 r-1 b-1" my0 p2 bg="[#efefef]" rounded-0>{{
            sample.answer
          }}</pre>
        </div>
      </div>
    </div>

    <h3>提示</h3>
    <p>{{ data.problem.problem_info.problem_content.hint }}</p>
  </div>
</template>
