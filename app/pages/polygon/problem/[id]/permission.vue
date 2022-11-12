<script setup lang="ts">
import type { FullPolygonProblem } from '@/composables/types';
import {
  type UserPermission,
  groupUserPermissions,
} from '@/composables/permission';

const props = defineProps<{ problem: FullPolygonProblem }>();

const { problem } = toRefs(props);

const { data } = await useFetchAPI<{
  user_permissions: UserPermission[];
  group_permissions: any[];
}>(`/api/polygon/${problem.value.id}/permission`);

const uesrPerms = computed(() => {
  const owner_perm = {
    user: problem.value.owner,
    permissions: {
      read_problem: true,
      read_submission: true,
      submit: true,
      edit: true,
      copy: true,
    },
  };
  return [
    owner_perm,
    ...groupUserPermissions(data.value?.user_permissions ?? [], {
      read_problem: false,
      read_submission: false,
      submit: false,
      edit: false,
      copy: false,
    }),
  ];
});
</script>

<template>
  <div>
    <c-table :data="uesrPerms">
      <template #headers>
        <c-table-header name="user" label="用户"></c-table-header>
        <c-table-header name="read_problem" label="访问题目"></c-table-header>
        <c-table-header
          name="read_submission"
          label="访问提交列表"
        ></c-table-header>
        <c-table-header name="submit" label="提交代码"></c-table-header>
        <c-table-header name="edit" label="编辑题目"></c-table-header>
        <c-table-header name="copy" label="加入题库"></c-table-header>
      </template>

      <template #user="{ row }">
        <user-link :user="row.user"></user-link>
      </template>
      <template #read_problem="{ row }">
        <c-switch v-model="row.permissions.read_problem"></c-switch>
      </template>
      <template #read_submission="{ row }">
        <c-switch v-model="row.permissions.read_submission"></c-switch>
      </template>
      <template #submit="{ row }">
        <c-switch v-model="row.permissions.submit"></c-switch>
      </template>
      <template #edit="{ row }">
        <c-switch v-model="row.permissions.edit"></c-switch>
      </template>
      <template #copy="{ row }">
        <c-switch v-model="row.permissions.copy"></c-switch>
      </template>
    </c-table>

    <!-- <c-table :data="data?.group_permissions ?? []">
      <template #headers>
        <c-table-header name="group_id" label="用户组"></c-table-header>
        <c-table-header name="codename" label="权限"></c-table-header>
      </template>
    </c-table> -->
  </div>
</template>
