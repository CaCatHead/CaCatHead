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
const closeSubmissions = () => {
  showSubmissions.value = false;
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
  return me ? 'bg-[#ddeeff] dark:bg-sky-900/80' : '';
};

const registrations = computed(() => {
  const list = data?.value?.registrations ?? [];

  const firstSolved = new Map<string, number>();

  const items = list.map(r => {
    const problems: Record<
      string,
      {
        ok: boolean;
        time: number;
        dirty: number;
        score: number;
        first: boolean;
      }
    > = {};

    for (const sub of r.standings?.submissions ?? []) {
      const pid = displyaIdToIndex(sub.p);
      if (sub.v === Verdict.Accepted) {
        if (!problems[pid]?.ok) {
          if (!problems[pid]) {
            problems[pid] = {
              ok: true,
              time: sub.r,
              dirty: 0,
              score: 0,
              first: false,
            };
          } else {
            problems[pid].ok = true;
            problems[pid].time = sub.r;
          }
        }
        if (!firstSolved.has(pid) || firstSolved.get(pid)! > sub.r) {
          firstSolved.set(pid, sub.r);
        }
      } else {
        if (!problems[pid]) {
          problems[pid] = {
            ok: false,
            time: sub.r,
            dirty: 1,
            score: 0,
            first: false,
          };
        } else {
          if (!problems[pid].ok) {
            problems[pid].dirty += 1;
          }
        }
      }
    }

    for (const [key, value] of Object.entries(r.standings?.penalty ?? {})) {
      const index = displyaIdToIndex(+key);
      if (index in problems) {
        problems[index].dirty = +value;
      }
    }
    for (const [key, value] of Object.entries(r.standings?.scores ?? {})) {
      const index = displyaIdToIndex(+key);
      if (index in problems) {
        problems[index].score = +value;
      }
    }

    return {
      ...r,
      rank: -1,
      standings: {
        scores: r.standings.scores,
        submissions: r.standings.submissions,
        problems,
      },
    };
  });

  for (let i = 0; i < items.length; i++) {
    // 设置一血
    for (const [pid, prob] of Object.entries(items[i].standings.problems)) {
      if (firstSolved.has(pid) && firstSolved.get(pid) === prob.time) {
        prob.first = true;
      }
    }

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

const timestamp = useServerTimestamp();
const startTime = new Date(contest.value.start_time!).getTime();
const endTime = new Date(contest.value.end_time!).getTime();
const formatProgress = (value: number) => {
  function alignNumber(value: number) {
    return (value < 10 ? '0' : '') + value;
  }
  const h = Math.floor(value / 3600000);
  const m = Math.floor((value % 3600000) / 60000);
  const s = Math.floor((value % 60000) / 1000);
  return `${h}:${alignNumber(m)}:${alignNumber(s)}`;
};
</script>

<template>
  <div>
    <h3 text-center text-2xl font-bold>
      <span hidden sm:inline>{{ contest.title }} 排行榜</span>
      <div hidden lt-sm:block>{{ contest.title }}</div>
      <div hidden lt-sm:block>排行榜</div>
    </h3>
    <client-only>
      <div
        v-if="timestamp <= startTime"
        mt4
        text-center
        text-base-500
        font-mono
      >
        <span>比赛开始还有 </span>
        <span>{{ formatProgress(startTime - timestamp) }}</span>
      </div>
      <div
        v-else-if="timestamp <= endTime"
        mt4
        text-center
        text-base-500
        font-mono
      >
        <span>比赛结束还有 </span>
        <span>{{ formatProgress(endTime - timestamp) }}</span>
      </div>
      <div v-else mt4 text-center text-base-500>比赛已结束</div>
      <template #fallback>
        <div mt4 h8></div>
      </template>
    </client-only>
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
          :type="contest.type"
          :result="row.standings?.problems[idx]"
          @click="handleShowSubmissions(row, idx)"
        ></standing-result>
      </template>
    </c-table>

    <c-modal
      :show="showSubmissions && selectedSubmission.length > 0"
      @close="closeSubmissions"
    >
      <div sm:p2>
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
              @click="closeSubmissions"
              >{{ sub.i }}</nuxt-link
            ></span
          >
        </div>
      </div>
    </c-modal>
  </div>
</template>
