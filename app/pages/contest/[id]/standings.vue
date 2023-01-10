<script setup lang="ts">
import type { FullContest, ContestStandings } from '@/composables/types';

const route = useRoute();

const props = defineProps<{ contest: FullContest }>();

const { contest } = toRefs(props);

useHead({
  title: `排行榜 - ${contest.value.title}`,
});

const { data } = await useFetchAPI<{ registrations: ContestStandings[] }>(
  `/api/contest/${route.params.id}/standings`
);

const alphabet = new Array(contest.value.problems.length)
  .fill(undefined)
  .map((_value, idx) => String.fromCharCode(65 + idx));

function toNumDuration(seconds: number) {
  function alignNumber(value: number) {
    return (value < 10 ? '0' : '') + value;
  }
  const hour = Math.floor(seconds / 3600);
  const minute = Math.floor((seconds % 3600) / 60);
  const sec = seconds % 60;
  return `${hour}:${alignNumber(minute)}:${alignNumber(sec)}`;
}

const registrations = computed(() => {
  const list = data?.value?.registrations ?? [];

  const items = list.map(r => {
    const problems: Record<
      string,
      { ok: boolean; time: number; dirty: number }
    > = {};

    for (const sub of r.standings?.submissions ?? []) {
      const pid = displyaIdToIndex(sub.problem.display_id);
      if (sub.verdict === Verdict.Accepted) {
        if (!problems[pid]?.ok) {
          if (!problems[pid]) {
            problems[pid] = { ok: true, time: sub.relative_time, dirty: 0 };
          } else {
            problems[pid].ok = true;
            problems[pid].time = sub.relative_time;
          }
        }
      } else {
        if (!problems[pid]) {
          problems[pid] = { ok: false, time: sub.relative_time, dirty: 1 };
        } else {
          if (!problems[pid].ok) {
            problems[pid].dirty += 1;
          }
        }
      }
    }

    return {
      ...r,
      rank: -1,
      standings: {
        submissions: r.standings.submissions,
        problems,
      },
    };
  });

  for (let i = 0; i < items.length; i++) {
    if (i === 0) {
      items[i].rank = 1;
    } else {
      if (
        items[i].score === items[i - 1].score &&
        items[i].dirty === items[i - 1].dirty
      ) {
        items[i].rank = items[i - 1].rank;
      } else {
        items[i].rank = i + 1;
      }
    }
    if (
      items[i].score === 0 &&
      (!items[i].standings.submissions ||
        items[i].standings.submissions.length === 0)
    ) {
      items[i].rank = -1;
    }
  }

  return items;
});
</script>

<template>
  <div>
    <h3 text-center text-2xl font-bold>{{ contest.title }} 排行榜</h3>
    <c-table :data="registrations" mt8>
      <template #headers>
        <c-table-header name="rank" width="80">#</c-table-header>
        <c-table-header name="name" align="left" text-left>队名</c-table-header>
        <c-table-header name="score" width="60">得分</c-table-header>
        <c-table-header name="penalty" width="120">罚时</c-table-header>
        <c-table-header
          v-for="problem in contest.problems"
          :name="displyaIdToIndex(problem.display_id)"
          width="60"
          rowClass="!p0"
          >{{ displyaIdToIndex(problem.display_id) }}</c-table-header
        >
      </template>

      <template #rank="{ row }">
        <span font-bold>{{ row.rank === -1 ? '-' : row.rank }}</span></template
      >
      <template #name="{ row }">
        <team-link :team="row.team" :name="row.name"></team-link>
      </template>
      <template #penalty="{ row }">{{ toNumDuration(row.dirty) }}</template>

      <template v-for="idx in alphabet" #[idx]="{ row }">
        <standing-result
          class="w-full h-full"
          :result="row.standings?.problems[idx]"
        ></standing-result>
      </template>
    </c-table>
  </div>
</template>
