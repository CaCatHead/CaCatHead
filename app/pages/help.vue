<script setup lang="ts">
import type { JudgeNode } from '@/composables/types';

useHead({
  title: '帮助',
});

const title = useAppConfig().title;

const { data } = await useFetchAPI<{ nodes: JudgeNode[] }>(`/api/judge/nodes`);

const compiler = [
  {
    language: 'C',
    compile: [
      'gcc',
      '代码路径',
      '-o',
      'a.out',
      '-fdiagnostics-color=always',
      '-Wall',
      '-Wextra',
      '-Wno-unused-result',
      '-static',
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
      '-fdiagnostics-color=always',
      '-Wall',
      '-Wextra',
      '-Wno-unused-result',
      '-static',
      '-lm',
      '-std=c++2a',
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
  cin >> a >> b;
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
          >这是 {{ title }}，由开源的在线评测系统
          <a
            href="https://github.com/CaCatHead/CaCatHead"
            text-link
            target="_blank"
            >猫猫头</a
          >
          驱动。虽然目前尚未开源，因为项目仍在快速迭代中，计划在到达一定完成度后开源。</template
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
            <judge-nodes :nodes="data?.nodes"></judge-nodes>
          </div>
        </template>
      </q-a>
      <q-a>
        <template #q>{{ title }} 在线评测系统支持哪些语言？</template>
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
                <c-table-header name="run" width="120px"
                  >运行命令</c-table-header
                >
              </template>

              <template #language="{ row }">{{ row.language }}</template>
              <template #compile="{ row }">
                <span text-sm font-mono mx2>
                  <span v-for="(t, index) in row.compile" inline-block>{{
                    (index > 0 ? '&nbsp;' : '') + t
                  }}</span>
                </span>
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
              例如，如果你使用的是 C/C++ 语言，那么你可以用 C 中的
              <a
                href="https://zh.cppreference.com/w/c/io/fscanf"
                text-link
                target="_blank"
                ><code>scanf</code></a
              >，或者 C++ 中的
              <a
                href="https://zh.cppreference.com/w/cpp/io/cin"
                text-link
                target="_blank"
                ><code>cin</code></a
              >，从标准输入里读入数据；你可以使用 C 中的
              <a
                href="https://en.cppreference.com/w/cpp/io/cout"
                text-link
                target="_blank"
                ><code>printf</code></a
              >
              或者 C++ 的
              <a
                href="https://zh.cppreference.com/w/c/io/fprintf"
                text-link
                target="_blank"
                ><code>cout</code></a
              >
              输出到标准输出。
            </p>
            <p>
              评测机禁止用户程序读取或者写入文件。如果你这样做，系统可能返回
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
            <p>下面是题目 A + B 的 C 的样例程序：</p>
            <code-box :code="CExample" language="c"></code-box>
            <p>下面是题目 A + B 的 C++ 的样例程序：</p>
            <code-box :code="CppExample" language="cpp"></code-box>
            <p>下面是题目 A + B 的 Java 的样例程序：</p>
            <code-box :code="JavaExample" language="java"></code-box>
          </div>
        </template>
      </q-a>
      <q-a>
        <template #q>返回的评测结果具体含义和可能出现的原因？</template>
        <template #a>
          <ul list-circle pl4 space-y-2>
            <li>
              <display-verdict :verdict="Verdict.Waiting"></display-verdict
              >：<span
                >提交的代码尚未开始运行，可能是正在等待空闲的评测机，或者评测机正在和主服务器通信；</span
              >
            </li>
            <li>
              <display-verdict :verdict="Verdict.Compiling"></display-verdict
              >：<span>提交的代码正在进行编译；</span>
            </li>
            <li>
              <display-verdict :verdict="Verdict.Running"></display-verdict
              >：<span
                >提交的代码正在运行，若提交的代码长时间保持以上这三种等待状态，请及时联系管理员处理；</span
              >
            </li>
            <li>
              <display-verdict :verdict="Verdict.Accepted"></display-verdict>：
              <span>提交的代码运行正常，正确通过了所有测试数据；</span>
            </li>
            <li>
              <display-verdict :verdict="Verdict.WrongAnswer"></display-verdict
              >：<span
                >提交的代码运行正常，但是没有正确通过所有测试数据，请检查你的算法是否正确，是否忽略了某些边界情况等等；</span
              >
            </li>
            <li>
              <display-verdict
                :verdict="Verdict.TimeLimitExceeded"
              ></display-verdict
              >：<span
                >提交的代码由于超过运行时间限制导致运行失败，请检查你的算法的时间复杂度是否正确，如果显示的运行时间小于题目标出的时间限制，那么可能是由于你的代码在内核态运行了过长时间（可能是由于输入输出超时，或者使用
                <code>sleep</code> 等）；</span
              >
            </li>
            <li>
              <display-verdict
                :verdict="Verdict.IdlenessLimitExceeded"
              ></display-verdict
              >：<span
                >未使用，该情况暂时被包含在
                <display-verdict
                  :verdict="Verdict.TimeLimitExceeded"
                ></display-verdict>
                内；</span
              >
            </li>
            <li>
              <display-verdict
                :verdict="Verdict.MemoryLimitExceeded"
              ></display-verdict
              >：<span
                >提交的代码由于超过运行内存限制导致运行失败，请检查你是否创建了过大的数组，或者动态分配了过多的内存空间；</span
              >
            </li>
            <li>
              <display-verdict
                :verdict="Verdict.PartiallyCorrect"
              ></display-verdict
              >：<span>在 OI 赛制下，提交返回了多种不同的错误结果；</span>
            </li>
            <li>
              <display-verdict
                :verdict="Verdict.OutputLimitExceeded"
              ></display-verdict
              >：<span
                >提交的代码由于输出过多导致运行失败，请检查你的输出代码是否陷入了死循环等情况；</span
              >
            </li>
            <li>
              <display-verdict :verdict="Verdict.RuntimeError"></display-verdict
              >：<span>提交的代码由于某些错误导致运行失败，可能的原因是：</span>
              <ul list-initial pl4 space-y-1 mt1>
                <li>提交的代码退出时，没有返回 0；</li>
                <li>提交的代码运行时，访问了非法的内存地址；</li>
                <li>试图攻击系统，触发了评测机的安全机制；</li>
                <li>...</li>
              </ul>
            </li>
            <li>
              <display-verdict :verdict="Verdict.CompileError"></display-verdict
              >：<span
                >提交的代码编译失败，请在本地开发环境确认代码能否正确编译，你可以在提交详情中查看到具体的编译错误信息（或者编译警告信息）；</span
              >
            </li>
            <li>
              <display-verdict :verdict="Verdict.SystemError"></display-verdict>
              /
              <display-verdict :verdict="Verdict.JudgeError"></display-verdict>
              /
              <display-verdict
                :verdict="Verdict.TestCaseError"
              ></display-verdict
              >：<span>评测机内部出错，请及时反馈给管理员。</span>
            </li>
          </ul>
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
