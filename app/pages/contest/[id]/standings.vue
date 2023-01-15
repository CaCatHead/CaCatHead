<script setup lang="ts">
import type {
  FullContest,
  ContestStanding,
  ContestStandingSubmission,
} from '@/composables/types';

const route = useRoute();

const user = useUser();

const props = defineProps<{ contest: FullContest }>();

const { contest } = toRefs(props);

useHead({
  title: `排行榜 - ${contest.value.title}`,
});

const { data } = await useFetchAPI<{ registrations: ContestStanding[] }>(
  `/api/contest/${route.params.id}/standings`
);

const showSubmissions = ref(false);
const selectedSubmission = ref([] as ContestStandingSubmission[]);
const handleShowSubmissions = (row: ContestStanding, index: string) => {
  const display_id = indexToDisplayId(index);
  selectedSubmission.value =
    row.standings.submissions?.filter(s => s.p === display_id).reverse() ?? [];
  showSubmissions.value = true;
};

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

const checkMyself = (standing: ContestStanding) => {
  const me =
    user?.value && standing.team.members.some(m => m.id === user.value.id);
  return me ? 'bg-[#ddeeff]' : '';
};

const registrations = computed(() => {
  const list = data?.value?.registrations ?? [];

  const items = list.map(r => {
    const problems: Record<
      string,
      { ok: boolean; time: number; dirty: number }
    > = {};

    for (const sub of r.standings?.submissions ?? []) {
      const pid = displyaIdToIndex(sub.p);
      if (sub.v === Verdict.Accepted) {
        if (!problems[pid]?.ok) {
          if (!problems[pid]) {
            problems[pid] = { ok: true, time: sub.r, dirty: 0 };
          } else {
            problems[pid].ok = true;
            problems[pid].time = sub.r;
          }
        }
      } else {
        if (!problems[pid]) {
          problems[pid] = { ok: false, time: sub.r, dirty: 1 };
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
    if (!items[i].is_participate) {
      continue;
    }
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
  }

  return items;
});
</script>

<template>
  <div>
    <h3 text-center text-2xl font-bold>
      <span hidden sm:inline>{{ contest.title }} 排行榜</span>
      <div hidden lt-sm:block>{{ contest.title }}</div>
      <div hidden lt-sm:block>排行榜</div>
    </h3>
    <c-table :data="registrations" mt8 :row-class="checkMyself">
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
          @click="handleShowSubmissions(row, idx)"
        ></standing-result>
      </template>
    </c-table>

    <c-modal :show="showSubmissions" @close="showSubmissions = false">
      <div v-if="showSubmissions && selectedSubmission.length > 0" sm:p2>
        <div
          v-for="sub in selectedSubmission"
          space-x-2
          font-mono
          lt-md="!text-sm"
        >
          <span>{{ formatDateTime(sub.c) }}</span>
          <span
            ><nuxt-link :to="`/contest/${route.params.id}/submission/${sub.i}`"
              ><display-verdict :verdict="sub.v"></display-verdict></nuxt-link
          ></span>
          <span select-none>→</span>
          <span
            ><nuxt-link
              text-sky-700
              text-op-70
              dark:text-sky-200
              hover:text-op-100
              :to="`/contest/${route.params.id}/submission/${sub.i}`"
              >{{ sub.i }}</nuxt-link
            ></span
          >
        </div>
      </div>
    </c-modal>
  </div>
</template>
