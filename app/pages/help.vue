<script setup lang="ts">
import type { JudgeNode } from '@/composables/types';

useHead({
  title: '帮助',
});

const { data } = await useFetchAPI<{ nodes: JudgeNode[] }>(`/api/judge/nodes`);

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

const MacroExample = `#ifdef ONLINE_JUDGE
  // 这段代码只会在评测机里运行
#endif

#ifndef ONLINE_JUDGE
  // 这段代码只会在本地运行
  // 例如，本地运行时读取输入文件
  freopen("in.txt", "r", stdin);
#endif`;

const CppExample = `#include <iostream>
using namespace std;

int main() {
  int a, b;
  cin >> a >> b
  cout << a + b << '\\n';
  return 0;
}`;

const CExample = `#include <stdio.h>

int main() {
  int a, b;
  scanf("%d%d", &a, &b);
  printf("%d\\n", a + b);
  return 0;
}`;

const JavaExample = `import java.util.Scanner;

public class Main {
  public static void main(String[] args) {
    Scanner cin = new Scanner(System.in);
    int a = cin.nextInt();
    int b = cin.nextInt();
    System.out.println(a + b);
  }
}`;
</script>

<template>
  <div class="qa-page">
    <div class="!max-w-full !w-full prose prose-truegray dark:prose-invert">
      <h2 text-center>常见问题及解答</h2>
    </div>
    <div space-y-4>
      <q-a>
        <template #q>这是什么网站？</template>
        <template #a
          >这是<a
            href="https://github.com/XLoJ/CaCatHead"
            text-link
            target="_blank"
            >猫猫头</a
          >，是一个开源的在线评测系统。</template
        >
      </q-a>
      <q-a v-if="!!data?.nodes">
        <template #q
          ><nuxt-link to="/nodes" text-link>评测机</nuxt-link
          >的运行情况？</template
        >
        <template #a>
          <div space-y-2 w-full>
            <div>
              共有
              {{ data.nodes.filter(n => n.active).length }} 台评测机正在运行。
            </div>
            <judge-nodes lt-sm:p1 :nodes="data?.nodes"></judge-nodes>
          </div>
        </template>
      </q-a>
      <q-a>
        <template #q>CaCatHead Online Judge 支持哪些语言？</template>
        <template #a>
          <div space-y-2 w-full>
            <div>目前为止，你可以使用 C, C++, Java。</div>
            <p>相应的编译程序和运行命令：</p>
            <c-table :data="compiler" w-full>
              <template #headers>
                <c-table-header name="language" width="72px"
                  >语言</c-table-header
                >
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
            <p>
              <strong>提示</strong>：如果你使用的是 C/C++ 语言，你可以使用
              <code>ONLINE_JUDGE</code>
              宏和<a
                href="https://zh.cppreference.com/w/c/preprocessor/conditional"
                target="_blank"
                text-link
                >条件编译</a
              >来判断代码是否运行在评测机上。
            </p>
            <code-box :code="MacroExample"></code-box>
          </div>
        </template>
      </q-a>
      <q-a>
        <template #q>程序的输入和输出什么？</template>
        <template #a>
          <div space-y-2>
            <p>
              你的程序需要从
              <strong>标准输入 (stdin)</strong> 里读取数据，并且输出到
              <strong>标准输出 (stdout)</strong>。
            </p>
            <p>
              例如，如果你是用的是 C/C++ 语言，你可以用 C 中的
              <a
                href="https://zh.cppreference.com/w/c/io/fscanf"
                text-link
                target="_blank"
                ><code>scanf</code></a
              >，或者使用 C++ 的
              <a
                href="https://zh.cppreference.com/w/cpp/io/cin"
                text-link
                target="_blank"
                ><code>cin</code></a
              >，从标准输入里读入数据；并且使用 C 中的
              <a
                href="https://en.cppreference.com/w/cpp/io/cout"
                text-link
                target="_blank"
                ><code>printf</code></a
              >
              或者使用 C++ 的
              <a
                href="https://zh.cppreference.com/w/c/io/fprintf"
                text-link
                target="_blank"
                ><code>cout</code></a
              >
              输出到标准输出。
            </p>
            <p>
              评测机禁止用户的程序读取或者写入文件。如果你这样做，系统可能返回
              <display-verdict verdict="RuntimeError"></display-verdict>
              等错误结果。
            </p>
            <p>
              你不能在提交的程序最后使用
              <code>system("pause");</code>
              等等便于调试的命令，这可能会导致程序无法正常终止。如果你这样做，系统可能返回
              <display-verdict verdict="RuntimeError"></display-verdict>
              等错误结果。
            </p>
            <p>下面是题目 A + B 的 C 的样例程序:</p>
            <code-box :code="CExample" language="c"></code-box>
            <p>下面是题目 A + B 的 C++ 的样例程序:</p>
            <code-box :code="CppExample" language="cpp"></code-box>
            <p>下面是题目 A + B 的 Java 的样例程序:</p>
            <code-box :code="JavaExample" language="java"></code-box>
          </div>
        </template>
      </q-a>
    </div>
  </div>
</template>

<style>
.qa-page [text-link=""] {
  --at-apply: text-sky-500 dark:text-sky-200;
  --at-apply: hover:text-sky-700 hover:dark:text-sky-400;
}
</style>
