<script setup lang="ts">
const props = defineProps<{ verdict: string }>();

const { verdict: _verdict } = toRefs(props);

const color = computed(() => {
  const verdict = _verdict.value;
  if (
    verdict === Verdict.Waiting ||
    verdict === Verdict.Compiling ||
    verdict === Verdict.Running
  ) {
    return '#2185D0';
  } else if (verdict === Verdict.Accepted) {
    return '#21BA45';
  } else if (
    verdict === Verdict.WrongAnswer ||
    verdict === Verdict.PartiallyCorrect
  ) {
    return '#DB2828';
  } else if (verdict === Verdict.RuntimeError) {
    return '#FBBD08';
  } else if (
    verdict === Verdict.MemoryLimitExceeded ||
    verdict === Verdict.TimeLimitExceeded ||
    verdict === Verdict.IdlenessLimitExceeded
  ) {
    return '#F2711C';
  } else {
    return '#767676';
  }
});

const message = computed(() => {
  const verdict = _verdict.value;
  if (verdict === Verdict.Running) {
    return 'Running';
  } else if (verdict === Verdict.Compiling) {
    return 'Compiling';
  } else if (verdict === Verdict.Waiting) {
    return 'Waiting';
  } else if (verdict === Verdict.Accepted) {
    return 'Accepted';
  } else if (verdict === Verdict.WrongAnswer) {
    return 'Wrong Answer';
  } else if (verdict === Verdict.TimeLimitExceeded) {
    return 'Time Limit Exceeded';
  } else if (verdict === Verdict.IdlenessLimitExceeded) {
    return 'Idleness Limit Exceeded';
  } else if (verdict === Verdict.MemoryLimitExceeded) {
    return 'Memory Limit Exceeded';
  } else if (verdict === Verdict.OutputLimitExceeded) {
    return 'Output Limit Exceeded';
  } else if (verdict === Verdict.RuntimeError) {
    return 'Runtime Error';
  } else if (verdict === Verdict.SystemError) {
    return 'System Error';
  } else if (verdict === Verdict.CompileError) {
    return 'Compile Error';
  } else if (verdict === Verdict.JudgeError) {
    return 'Judge Error';
  } else if (verdict === Verdict.TestCaseError) {
    return 'Testcase Error';
  } else if (verdict === Verdict.PartiallyCorrect) {
    return 'Partially Correct';
  }
  return 'System Error';
});
</script>

<template>
  <span :style="{ color }" class="has-text-weight-bold">{{ message }}</span>
</template>
