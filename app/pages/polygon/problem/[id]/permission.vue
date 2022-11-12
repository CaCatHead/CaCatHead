<script setup lang="ts">
import type { FullPolygonProblem } from '@/composables/types';
import {
  type UserPermission,
  ProblemPermissions,
  groupUserPermissions,
} from '@/composables/permission';

const props = defineProps<{ problem: FullPolygonProblem }>();

const { problem } = toRefs(props);

const { data, refresh } = await useFetchAPI<{
  user_permissions: UserPermission[];
  group_permissions: any[];
}>(`/api/polygon/${problem.value.id}/permission`);

const userPerms = ref([] as any[]);
watch(
  data,
  () => {
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
    userPerms.value.splice(
      0,
      userPerms.value.length,
      owner_perm,
      ...groupUserPermissions(data.value?.user_permissions ?? [], {
        read_problem: false,
        read_submission: false,
        submit: false,
        edit: false,
        copy: false,
      })
    );
  },
  { immediate: true }
);

const username = ref('');
const grantUserPerm = async (username: string, perm: ProblemPermissions) => {
  await fetchAPI(`/api/polygon/${problem.value.id}/permission`, {
    method: 'POST',
    body: {
      username,
      grant: perm,
    },
  });
  await refresh();
};
const toggleUserPerm = async (
  username: string,
  perm: ProblemPermissions,
  flag: boolean
) => {
  const payload = flag ? { grant: perm } : { revoke: perm };
  await fetchAPI(`/api/polygon/${problem.value.id}/permission`, {
    method: 'POST',
    body: {
      username,
      ...payload,
    },
  });
  await refresh();
};
</script>

<template>
  <div>
    <div mb4>
      <c-input
        type="text"
        id="perm_username"
        name="用户名"
        v-model="username"
        @keypress.enter="
          grantUserPerm(username, ProblemPermissions.ReadProblem)
        "
      >
        <template #label
          ><label for="perm_username" font-600>用户名</label></template
        >
      </c-input>
    </div>

    <c-table :data="userPerms">
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
        <c-switch
          v-model="row.permissions.read_problem"
          @change="
            (flag: boolean) => toggleUserPerm(row.user.username, ProblemPermissions.ReadProblem, flag)
          "
        ></c-switch>
      </template>
      <template #read_submission="{ row }">
        <c-switch
          v-model="row.permissions.read_submission"
          @change="
            (flag: boolean) => toggleUserPerm(row.user.username, ProblemPermissions.ReadSubmission, flag)
          "
        ></c-switch>
      </template>
      <template #submit="{ row }">
        <c-switch
          v-model="row.permissions.submit"
          @change="
            (flag: boolean) => toggleUserPerm(row.user.username, ProblemPermissions.Submit, flag)
          "
        ></c-switch>
      </template>
      <template #edit="{ row }">
        <c-switch
          v-model="row.permissions.edit"
          @change="
            (flag: boolean) => toggleUserPerm(row.user.username, ProblemPermissions.Edit, flag)
          "
        ></c-switch>
      </template>
      <template #copy="{ row }">
        <c-switch
          v-model="row.permissions.copy"
          @change="
            (flag: boolean) => toggleUserPerm(row.user.username, ProblemPermissions.Copy, flag)
          "
        ></c-switch>
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
