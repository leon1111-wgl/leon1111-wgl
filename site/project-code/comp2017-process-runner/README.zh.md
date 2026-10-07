# 项目 2：有容量上限的进程记录器

Leon | Original teaching project. Leon 原创教学项目。

小梅在分享团队的传感器报告前，会运行一个本地检查程序。她需要知道三件事：
程序输出了什么、是否保留了全部输出，以及程序怎样结束。为了理解进程和管道，
她要亲手实现一个命令行记录器，每次运行一个她有权运行的程序。

这是原创学习项目，不是其他课程的作业答案，也不是生产级任务管理器。预备知识：
参数数组、内存所有权、分离编译、fork、exec/wait 和管道。

## 编译、运行和测试

需要 macOS 或 Linux，以及 Clang、Make 和 Python 3。在本目录运行：

```sh
make
./process_runner 32 -- /bin/echo 'hello team'
./process_runner 8 -- ./fixture_child burst
./process_runner 32 -- ./fixture_child fail
./process_runner 16 -- ./absent-program
make test
make clean
```

编译选项为 `clang -std=c11 -Wall -Wextra -Werror -pedantic -pthread`，并设置
`-D_POSIX_C_SOURCE=200809L`。程序是单线程的；`-pthread` 用来统一课程项目的编译要求。
`make test` 会在临时目录编译副本，测试结束后删除副本。测试前不必先运行 `make`。
最后两个运行命令故意返回 7 和 127。如果你的脚本遇到非零状态就停止，请逐条运行。

接口是 `process_runner CAP -- PROGRAM [ARG ...]`。CAP 只能包含十进制数字，范围是
0 到 65536。不含 `/` 的程序名由继承的 PATH 查找。要指定某个可执行文件时，建议
明确写出路径。示例的引号由启动记录器的 shell 处理，让 `hello team` 成为一个参数。
记录器把已有参数数组直接传给 `execvp`，不会拼接命令，不会展开 `$HOME` 或 `*`，
不会按空格拆分参数，也不会把 `;` 当成命令分隔符。

第一个命令的标准输出严格如下：

```text
stdout="hello team\n"
captured_bytes=11
truncated=no
child_exit=0
```

burst 测试程序写出 1,048,576 个 `A`，报告只保留前 8 个：

```text
stdout="AAAAAAAA"
captured_bytes=8
truncated=yes
child_exit=0
```

失败检查的标准输出如下：

```text
stdout="check failed\n"
captured_bytes=13
truncated=no
child_exit=7
```

找不到程序时，标准输出如下：

```text
stdout=""
captured_bytes=0
truncated=no
child_exit=127
```

标准错误还会收到 `process_runner: execvp failed` 和一个换行。父进程仍然读到 EOF，
并取得子进程的结束状态。执行失败不等于放弃回收子进程。

## 五个连续里程碑

1. **定义记录器的接口。** 阅读 `main.c` 和 `process.h`。先检查容量，再分配内存和
   创建进程。直接借用 `&argv[3]`，不拼接命令字符串。main 拥有缓冲区，进程模块只是写入它。
2. **给子进程一条输出通道。** 阅读 `process.c` 中的 `execute_child`。pipe 建立读端和
   写端。fork 后父子进程各有这两个描述符的副本。子进程关闭读端，用 dup2 把写端复制到
   标准输出 1，关闭原来的写端描述符，再调用 execvp。
3. **限制内存，但继续读取。** 阅读 `drain_output`。每次 read 可能返回 1 到 4096 个
   字节。只复制放得下的部分，但缓冲区满了也要继续读。CAP=0 时不保存输出，仍让子进程
   顺利写完。fragment 模式输出 `tail`，没有换行也能完整处理。
4. **完成进程生命周期。** 阅读 `process_run` 和 `report`。父进程立即关闭自己的写端，
   读到 EOF 后关闭读端，再用 waitpid 等待这个子进程。用 WIFEXITED/WEXITSTATUS 或
   WIFSIGNALED/WTERMSIG 解码结果，不要猜原始状态整数里各个位的含义。
5. **检查边界。** 阅读 `fixtures/child.c` 和 `test.py`。用手工算出的字节数、状态码、
   标准输出和标准错误作为预期结果。对四字节输出尝试容量 3、4 和 0，再测试大量输出和
   不存在的程序。这些是本项目的概念检查，不是其他课程的作业答案。

## 描述符所有权与执行顺序

| 资源 | 初始化后由谁持有 | 如何释放 |
| --- | --- | --- |
| `channel[0]` 读端 | 父进程 | EOF 或读取失败后关闭；子进程在 exec 前关闭自己的副本 |
| `channel[1]` 原写端描述符 | 初始化后双方都不再保留 | 父进程立即关闭；子进程 dup2 后关闭 |
| 子进程的标准输出 1 | 新执行的程序 | 程序主动关闭或进程结束时关闭 |
| 保存输出的缓冲区 | 父进程的 main | 运行失败或报告完成后 free |
| 直接子进程的 PID 与结束状态 | 父进程 | waitpid 取得结束状态并完成回收 |
| 参数字符串 | C 运行时或调用者 | 本模块只借用，不释放、不改写 |

管道已经读空，并且所有写端描述符都关闭后，read 才返回 EOF。父进程必须关闭自己的
写端。孙进程若继承了标准输出，即使直接子进程已经结束，也可能推迟 EOF。反过来，
子进程可以先关闭标准输出，再继续计算。所以 EOF 和子进程结束是两个不同事件。
读取结束后仍需 waitpid；它只等待直接子进程，不等待整棵后代进程树。

父子进程没有固定调度顺序。read 返回的是已经写入管道的字节。最终报告发生在读完和
等待成功之后。如果先 wait，子进程可能因管道已满而卡在 write，父进程又在等它结束，
双方就无法前进。只保存一个小前缀，并不能成为停止读取的理由。

设输出总量为 N，容量为 C，则保存字节数为 min(N,C)，截断条件为 N>C。读取工作量为
O(N)，内存为 O(C+4096)。程序不累加已经丢弃的总字节数，因此不需要处理无限增长的
总量计数器。一个字节转义后最多用四个字符显示，所以显示长度不等于保存字节数。

## 输出、错误与适用范围

- 只捕获 stdout。stdin 和 stderr 保持继承。诊断直接送往原来的 stderr，不能假定它与
  最后 stdout 报告的显示先后。保存的字节使用可打印 ASCII 和 `\n`、`\r`、`\t`、
  `\\`、`\"`、两位十六进制 `\xHH` 显示。支持 NUL 和高位字节；这是字节视图，
  不是 Unicode 解码器，也不是原始二进制文件副本。
- 正常结束时，记录器原样返回子进程的退出码。信号结束时显示 `child_signal=N`，在
  支持的平台上返回 `128+N`。报告可以区分信号结束和恰好返回相同数字的普通退出。
- 参数错误返回 2；能够处理的记录器分配、创建、读取、等待或报告错误返回 125。
  子进程重定向失败调用 `_exit(126)`，exec 失败写固定诊断后调用 `_exit(127)`。
  程序本身也可以返回 126 或 127；本项目没有额外的 exec 错误管道来消除歧义。
  记录器错误没有完整的子进程报告。perror 的系统错误文字可能因平台或语言环境而不同。
- read、waitpid、子进程诊断 write 和 dup2 遇到 EINTR 会重试。读取发生其他错误时，
  父进程向自己的直接子进程发送 SIGKILL，关闭读端，并继续尝试 waitpid。
  fork 失败时关闭两个描述符，并保存原始 errno。子进程用 `_exit`，避免刷新继承的
  父进程 stdio 缓冲区，也不会执行父进程注册的 atexit 回调。
- API 假设调用者是单线程、标准描述符已经打开、使用普通阻塞 I/O、没有其他回收者，
  并保留默认 SIGCHLD 处理。程序先检查 0、1、2，确保新管道描述符大于 2，简化 dup2
  和 close 的所有权关系。清理时尽力关闭，不重试 close；兼容所有 POSIX 变体的
  close 中断恢复不在这个例子的范围内。
- 这不是沙箱。子进程继承工作目录、环境、stdin、stderr，以及没有设置 close-on-exec
  的其他描述符。按 POSIX 规则，execvp 遇到格式无法识别的可执行文本文件时，可能调用
  命令解释器来执行该文件。被解释的是选中的文件；记录器仍不把参数拼成 shell 命令。
  练习时使用随附的编译后测试程序，或你有权执行的本地程序。
- 没有超时、进程树清理、资源配额或信号转发策略。子进程等待输入、后代保留写端、stderr
  接收方阻塞或子进程一直不结束，都可能让记录器等待。记录器没有安装信号处理器，
  中断它可能留下仍存活的子进程。报告管道断开时，默认 SIGPIPE 可能直接结束记录器。
  完整取消机制需要更大的设计，不能只加一次 kill 就声称完成。

测试只启动有限的本地 fixture_child、`/bin/echo`，以及一个故意不存在的路径。
每次测试创建独立进程组，8 秒内未结束就清理该测试进程组。测试辅助程序不创建后代、
不读取输入，最多写出 1 MiB。编译有 30 秒超时。14 个测试覆盖错误容量、空格和特殊字符、
空输出、恰好达到与超过容量、二进制转义、stderr、普通退出、非零退出、信号退出和 exec
失败。它们不能强制覆盖罕见分配/fork/read 失败、EINTR、所有调度或进程树取消。

## 官方参考

- [POSIX fork](https://pubs.opengroup.org/onlinepubs/9799919799/functions/fork.html)
- [POSIX exec 系列](https://pubs.opengroup.org/onlinepubs/9799919799/functions/exec.html)
- [POSIX pipe](https://pubs.opengroup.org/onlinepubs/9799919799/functions/pipe.html)
- [POSIX read](https://pubs.opengroup.org/onlinepubs/9799919799/functions/read.html)
- [POSIX wait 与 waitpid](https://pubs.opengroup.org/onlinepubs/9699919799/functions/wait.html)
- [POSIX dup2](https://pubs.opengroup.org/onlinepubs/9799919799/functions/dup.html)
- [POSIX _exit](https://pubs.opengroup.org/onlinepubs/9799919799/functions/_exit.html)
