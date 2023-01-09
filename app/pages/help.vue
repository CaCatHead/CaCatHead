<script setup lang="ts">
useHead({
  title: '帮助',
});

const compiler = [
  {
    language: 'C',
    compile: [
      'gcc',
      '代码路径',
      '-o',
      'a.out',
      '-static',
      '-w',
      '-lm',
      '-std=c11',
      '-O2',
      '-DONLINE_JUDGE',
    ],
    run: ['./a.out'],
  },
  {
    language: 'C++',
    compile: [
      'g++',
      '代码路径',
      '-o',
      'a.out',
      '-static',
      '-w',
      '-lm',
      '-std=c++11',
      '-O2',
      '-DONLINE_JUDGE',
    ],
    run: ['./a.out'],
  },
  {
    language: 'Java',
    compile: ['javac', '代码路径', '-d', '.'],
    run: ['java', 'Main'],
  },
];
</script>

<template>
  <div !max-w-full !w-full prose prose-truegray dark:prose-invert>
    <h2 text-center>常见问题及解答</h2>
    <div space-y-4>
      <q-a>
        <template #q>这是什么网站？</template>
        <template #a
          >这是<a href="https://github.com/XLoJ/CaCatHead">猫猫头</a
          >，是一个开源的在线评测系统。</template
        >
      </q-a>
      <q-a>
        <template #q>CaCatHead Online Judge 支持哪些语言？</template>
        <template #a>
          <div>目前为止，你可以使用 C, C++, Java。</div>
          <p>相应的编译程序和运行命令：</p>
          <c-table :data="compiler" w-full>
            <template #headers>
              <c-table-header name="language" width="72px">语言</c-table-header>
              <c-table-header name="compile">编译命令</c-table-header>
              <c-table-header name="run">运行命令</c-table-header>
            </template>

            <template #language="{ row }">{{ row.language }}</template>
            <template #compile="{ row }">
              <span text-sm font-mono mx2>{{ row.compile.join(' ') }}</span>
            </template>
            <template #run="{ row }">
              <span text-sm font-mono mx2>{{ row.run.join(' ') }}</span>
            </template>
          </c-table>
        </template>
      </q-a>
    </div>
  </div>
</template>
