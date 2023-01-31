<script setup lang="ts">
const props = withDefaults(
  defineProps<{
    rating?: number | undefined;
    rank?: string;
    admin?: boolean;
  }>(),
  {
    rating: undefined,
    rank: undefined,
    admin: false,
  }
);

const { rating, rank } = toRefs(props);

const color = computed(() => {
  const rt = rating?.value;
  if (rt === undefined || rt === null) return null;
  if (rt < 1200) return 'newbie';
  if (rt < 1400) return 'pupil';
  if (rt < 1600) return 'specialist';
  if (rt < 1900) return 'expert';
  if (rt < 2100) return 'candidate-master';
  if (rt < 2400) return 'master';
  if (rt < 3000) return 'grandmaster';
  return 'grandmaster';
});
</script>

<template>
  <span :class="['rating', admin || rank === 'rainbow' ? 'rainbow' : color]"
    ><slot></slot
  ></span>
</template>

<style>
.rating {
  display: inline-block;
  color: black;
  font-weight: bold;
}

.rating.rainbow {
  background-image: linear-gradient(
    to left,
    #ee4035,
    #f37736,
    #7bc043,
    #0392cf
  );
  -webkit-background-clip: text;
  color: transparent;
  user-select: none;
}

.rating.legendary-grandmaster::first-letter {
  color: black !important;
}

.rating.legendary-grandmaster,
.rating.international-grandmaster,
.rating.grandmaster {
  color: #ff0000 !important;
}

.rating.international-master,
.rating.master {
  color: #ff8c00 !important;
}

.rating.candidate-master {
  color: #aa00aa !important;
}

.rating.expert {
  color: #0000ff !important;
}

.rating.specialist {
  color: #03a89e !important;
}

.rating.pupil {
  color: #008000 !important;
}

.rating.newbie {
  color: gray !important;
}
</style>
