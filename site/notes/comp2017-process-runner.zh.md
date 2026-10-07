# COMP2017 — 有容量上限的进程记录器

> Leon | Original engineering workshop

![Leon learning route](../assets/maps/comp2017-process-runner.zh.svg)

[English](comp2017-process-runner.en.md) · [中文](comp2017-process-runner.zh.md)

运行一个本地程序，保存有容量上限的标准输出前缀，继续读完其余字节，并准确解释子进程怎样结束。

[下载完整工程 ZIP](../downloads/comp2017-process-runner.zip)

## 故事

小梅在分享团队的传感器报告前，会先运行检查程序。有的检查只输出一句成功提示，有的会打印很多细节后返回错误。复制终端文字容易漏掉退出状态，保存所有字节又浪费内存。她实现一个小记录器，只保留前 C 个字节，说明是否还有更多输出，并记录子进程结果。先从带空格参数的 echo 开始，再解决管道写满、程序不存在、最后一行没有换行的问题。完成后，她能说明每个描述符和保存字节的来历，也能说明工具尚未覆盖的情况。这是Leon 原创学习项目，与现成课程作业无关。

### 开始前先读

- [字符串、有界输入与解析](../courses/comp2017.zh.html#strings-parsing): 把 argv 看成独立字符串数组，并在不溢出的前提下检查十进制容量。

- [动态分配与对象生命周期](../courses/comp2017.zh.html#allocation-ownership): 命令行模块分配缓冲区，借给进程模块，最后只释放一次。

- [翻译单元、符号与程序库](../courses/comp2017.zh.html#compilation-linkage): 通过 process.h 的接口约定，把 main.c 与 process.c 编译链接在一起。

- [进程、虚拟内存与 fork](../courses/comp2017.zh.html#process-fork): fork 在两个进程中返回；它们拥有独立内存和复制后的描述符表。

- [执行新程序并回收子进程](../courses/comp2017.zh.html#exec-wait): 替换子进程程序，再用 waitpid 取得结束状态。

- [管道、FIFO 端点与字节分帧](../courses/comp2017.zh.html#pipes-fifos): 利用管道 EOF 和描述符所有权协调输出与结束。

### 学习成果

- 使用 fork 和 execvp 执行程序，并保留原有参数边界。

- 限制保存输出的内存，同时持续读取，让子进程能够继续执行。

- 区分 EOF、成功等待、正常退出、信号终止和记录器自身错误。

- 测试可观察的字节与状态码，不依赖进程调度先后。

## 需求与契约

### 接受 CAP -- PROGRAM [ARG ...]，CAP 范围是 0 到 65536。

内存预算必须明确，并在工作开始前完成检查。

格式错误、负数、超大、缺少或混入字母的容量返回 2，不生成标准输出报告。

### 把已有 argv 的一部分直接传给 execvp。

拼接字符串会破坏参数边界，还可能引入 shell 解释。

测试程序将 two words 作为一个参数收到，并原样收到 $HOME;*。

### 最多保存 CAP 个字节，但一直读取到 EOF。

达到上限就停止读取，可能让子进程卡在写满的管道上。

1 MiB 输出在容量为 8 或 0 时都能完成，并报告截断。

### 只捕获 stdout；继承 stdin 与 stderr。

单一管道让所有权清楚，也不把两个流说成具有可靠的统一顺序。

stderr 测试生成包含 ok 的报告，同时单独输出诊断。

### 关闭不用的描述符，回收直接子进程，并解码其等待状态。

EOF 要求所有写端都关闭；进程结束仍需要 waitpid 处理。

分别验证正常退出 0、退出 7、缺少程序 127 和 SIGTERM。

### 用确定的 ASCII 转义显示字节。

保存的前缀可能包含 NUL、控制字节或多字节字符的一部分。

验证 NUL、0xFF、引号、反斜杠、制表符、回车和换行都保留原字节含义。

## 结构与所有权

**命令行与报告：main.c**

检查容量、分配字节缓冲区、借用 argv、调用进程模块、转义保存的字节，并返回子进程结果。

**进程生命周期：process.c / process.h**

创建管道和子进程，重定向子进程 stdout，父进程读取读端，并回收这个子进程。公开结果包含字节数、截断标记和原始等待状态。

**有限测试程序：fixtures/child.c**

产生受控输出和结果，不使用文件、后代进程、输入、睡眠或网络。burst 模式恰好写出 256 个 4096 字节块。

**独立检查：test.py**

在临时目录编译副本，把实际输出与返回码同手工预期比较。每次运行都有 8 秒看门狗和独立进程组。

检查参数 → 分配 → pipe → fork。子进程：关读端 → dup2(写端,1) → 关原写端 → execvp。父进程：关写端 → 读到 EOF → 关读端 → waitpid → 转义并报告 → free。父子进程并发运行，没有固定调度顺序。read 读取已经写入的字节，所有写端关闭且队列读空后才有 EOF，最终报告在成功等待之后生成。

- 管道读端 → fork 后由父进程保留；子进程最初也有副本。 → 子进程在 exec 前关闭副本；父进程读取结束或失败后关闭。

- 原始管道写端 → fork 后双方短暂持有。 → 父进程立即关闭；子进程 dup2 后关闭，stdout 仍指向同一管道。

- 子进程标准输出，描述符 1 → 执行后的程序，以及继承它的后代进程。 → 程序关闭或进程结束时释放；所有写端都关闭后才可能有 EOF。

- 输出缓冲区与参数数组 → main 拥有分配内存；process_run 借用该内存和 argv 字符串。 → main 在错误时或报告后释放缓冲区；本模块不释放借用的 argv。

- 直接子进程及结束状态 → 父进程负责回收 fork 返回的 PID。 → waitpid 遇到 EINTR 重试并取得结束状态；读取失败也尝试终止并回收。

<a id="milestone-contract"></a>

## 1. 定义一次运行的约定

检查命令行，并给缓冲区明确的所有者。

小梅先决定字节预算，再运行检查程序。有限范围的十进制解析器在乘法前防止溢出；argv 已经提供所需的参数边界。

1. 用 make 编译完整项目。先读 process.h，再看 main。

2. 跟踪 65536 的解析过程，再说明为什么 65537 和 8x 被拒绝。

3. 跟踪 malloc、process_run(&argv[3], ...) 和 free。进程模块不能释放借来的内存。

教学摘录；运行时使用完整工程。

```c
static int parse_capacity(const char *text, size_t *capacity)
{
    size_t value = 0;
    if (*text == '\0') {
        return -1;
    }
    for (const char *p = text; *p != '\0'; ++p) {
        if (*p < '0' || *p > '9') {
            return -1;
        }
        size_t digit = (size_t)(*p - '0');
        if (value > (PROCESS_MAX_CAPTURE - digit) / 10) {
            return -1;
        }
        value = value * 10 + digit;
    }
    *capacity = value;
    return 0;
}
```

这是 main.c 的节选，不是独立程序。digit 范围是 0–9。先检查 value <= (MAX-digit)/10，才能保证 value*10+digit 不超过上限。空字符串和任何非数字都会失败。

**为什么传 &argv[3]，而不是把后面的字符串拼起来？**

它指向程序名、已有参数和末尾 NULL。拼接后就无法区分哪些空格属于参数内部。

<a id="milestone-wire-child"></a>

## 2. 给子进程连接输出通道

把子进程 stdout 改为管道，同时保留 stdin 和 stderr。

fork 会复制描述符，所以双方最初都持有两端。exec 替换程序之前，子进程描述符 1 必须已经指向管道。

1. 画出 fork 后的两张描述符表，每张都有读端和写端。

2. 子进程先关读端，把写端 dup2 到描述符 1，再关原写端。

3. 使用未改写的参数数组调用 execvp。失败时向 stderr 写固定诊断，然后调用 _exit(127)。

教学摘录；运行时使用完整工程。

```c
static void execute_child(int read_end, int write_end, char *const argv[])
{
    static const char setup_error[] = "process_runner: stdout setup failed\n";
    static const char exec_error[] = "process_runner: execvp failed\n";
    (void)close(read_end);
    int copied;
    do {
        copied = dup2(write_end, STDOUT_FILENO);
    } while (copied == -1 && errno == EINTR);
    if (copied == -1) {
        (void)close(write_end);
        child_failure(setup_error, sizeof(setup_error) - 1, 126);
    }
    (void)close(write_end);
    /* The original argument boundaries survive; no command string is built. */
    execvp(argv[0], argv);
    child_failure(exec_error, sizeof(exec_error) - 1, 127);
}
```

这是 process.c 的节选。调用者检查 0–2 已打开，保证新管道描述符大于 2。dup2 让 stdout 成为写端的另一个引用；关闭原描述符不会关闭 stdout。exec 成功就不会返回。_exit 跳过复制来的 stdio 缓冲区和 atexit 回调。

**关闭原写端描述符，会不会破坏子进程输出通道？**

不会。dup2 成功后，描述符 1 仍指向管道。这个引用在 exec 后保留，到程序主动关闭或退出时才关闭。

<a id="milestone-drain-bound"></a>

## 3. 保存前缀并持续读取

用有限内存处理空输出、恰好达到上限、超过上限和没有换行的输出。

内核管道容量也有限。如果小梅缓冲区满了就停止读取并开始等待，大量输出的子进程可能正在等管道腾出空间，双方就都无法前进。

1. 每次 read 返回正数后，计算 space=capacity-captured，再计算 keep=min(count,space)。

2. 只复制 keep 个字节。只有确实有字节放不下时才标记截断；刚好达到上限不算截断。

3. 继续读，直到返回 0 表示 EOF。EINTR 要重试；没有换行的末尾片段也是数据。

教学摘录；运行时使用完整工程。

```c
static int drain_output(int read_end, unsigned char *buffer, size_t capacity,
                        struct process_result *result)
{
    unsigned char chunk[4096];
    for (;;) {
        ssize_t received = read(read_end, chunk, sizeof(chunk));
        if (received == -1 && errno == EINTR) {
            continue;
        }
        if (received == -1) {
            return -1;
        }
        if (received == 0) {
            return 0;
        }
        size_t count = (size_t)received;
        size_t space = capacity - result->captured;
        size_t keep = count < space ? count : space;
        if (keep > 0) {
            memcpy(buffer + result->captured, chunk, keep);
            result->captured += keep;
        }
        if (keep < count) {
            result->truncated = true;
        }
        /* A full buffer stops copying, never reading. The child must progress. */
    }
}
```

这是 process.c 的节选。不变量是 0<=captured<=capacity。一次 read 可能只读到少量字节，一次 write 不一定对应一次 read。N 字节输出需要 O(N) 读取工作，容量 C 对应 O(C+4096) 内存。没有累加丢弃总量的计数器，所以不会在该计数上溢出。

**子进程输出 tail，恰好四个字节。容量 4、3、0 有何区别？**

容量 4 保存 tail，truncated=no；容量 3 保存 tai，truncated=yes；容量 0 不保存字节，truncated=yes。三者仍会读完相同的四个字节。

<a id="milestone-reap-report"></a>

## 4. 回收并解释结束结果

完成描述符清理，并区分正常退出和信号终止。

EOF 不能证明子进程结束：它可能关闭 stdout 后继续运行。反过来，后代也可能在直接子进程结束后继续持有写端。小梅还需要 waitpid 检查另一种完成条件。

1. 读取前关闭父进程写端，否则父进程自己就会阻止 EOF。

2. 读完后关读端，再等待指定子进程 PID。只有 errno 为 EINTR 时重试 waitpid。

3. 使用等待状态宏，显示转义字节前缀与状态，然后释放缓冲区。读取失败时终止直接子进程，并仍尝试回收。

教学摘录；运行时使用完整工程。

```c
static int report(const unsigned char *data, const struct process_result *result)
{
    print_bytes(data, result->captured);
    printf("captured_bytes=%zu\ntruncated=%s\n", result->captured,
           result->truncated ? "yes" : "no");
    if (WIFEXITED(result->wait_status)) {
        int code = WEXITSTATUS(result->wait_status);
        printf("child_exit=%d\n", code);
        return code;
    }
    if (WIFSIGNALED(result->wait_status)) {
        int number = WTERMSIG(result->wait_status);
        printf("child_signal=%d\n", number);
        return 128 + number;
    }
    fputs("process_runner: unexpected wait status\n", stderr);
    return 125;
}
```

这是 main.c 的节选。先判断 WIFEXITED 才用 WEXITSTATUS；先判断 WIFSIGNALED 才用 WTERMSIG。原始等待整数本身不是退出码。普通退出返回子进程代码；信号单独显示，在支持的平台上映射为 128+信号编号。

**只看 child_exit=127，能证明 execvp 失败吗？**

不能。所选程序自己也可能返回 127。本项目在 exec 失败时另写固定 stderr 信息，但没有独立 exec 错误协议。可通过额外的 close-on-exec 错误管道扩展。

<a id="milestone-test-boundaries"></a>

## 5. 用受控子进程检查记录器

验证字节、截断、stderr 策略和状态，不假定调度先后。

运行真实子进程比检查源码文字更有说服力。合成测试程序的行为有限且已知，小梅能够独立算出预期，并为整个运行加看门狗。

1. 运行 make test。它在临时目录严格编译，只调用本地测试程序、/bin/echo 和故意不存在的路径。

2. 比较精确输出、字节数、子进程状态和独立 stderr。无论 read 如何分块，burst 都是 256*4096=1048576 个字节。

3. 测试零容量、恰好与超过上限、字面特殊字符、非零退出、信号退出、二进制转义和缺失程序。超时只清理独立的测试进程组。

教学摘录；运行时使用完整工程。

```c
int main(int argc, char **argv)
{
    if (argc < 2) {
        return 2;
    }
    if (strcmp(argv[1], "args") == 0) {
        for (int i = 2; i < argc; ++i) {
            printf("[%s]", argv[i]);
        }
    } else if (strcmp(argv[1], "burst") == 0) {
        char block[4096];
        memset(block, 'A', sizeof(block));
        for (int i = 0; i < 256; ++i) {
            if (fwrite(block, 1, sizeof(block), stdout) != sizeof(block)) {
                return 3;
            }
        }
    } else if (strcmp(argv[1], "fragment") == 0) {
        fputs("tail", stdout);
    } else if (strcmp(argv[1], "fail") == 0) {
        puts("check failed");
        return 7;
    } else if (strcmp(argv[1], "stderr") == 0) {
        fputs("diagnostic\n", stderr);
        puts("ok");
    } else if (strcmp(argv[1], "bytes") == 0) {
        const unsigned char bytes[] = {0, 255, '"', '\\', '\t', '\r', '\n'};
        if (fwrite(bytes, 1, sizeof(bytes), stdout) != sizeof(bytes)) {
            return 3;
        }
    } else if (strcmp(argv[1], "signal") == 0) {
        (void)raise(SIGTERM);
        return 3;
    } else if (strcmp(argv[1], "empty") != 0) {
        return 2;
    }
    return fflush(stdout) == 0 ? 0 : 3;
}
```

这是 fixtures/child.c 的节选，它是测试使用的独立有限程序。辅助程序既不 fork，也不读取 stdin。burst 输出有限，fail 返回 7，fragment 不带换行。这些例子用于测试本项目，不是现成作业答案。

**burst 测试通过说明了什么？还有什么无法证明？**

它说明本次运行在只保留容量上限的同时，读完了有限的大输出并回收子进程。它不能证明所有调度、强制 EINTR 或错误路径、后代清理和生产级超时策略。

## 构建与运行

使用 macOS 或 Linux 上支持 C11 的 Clang、make 和 Python 3。Windows 可使用 WSL 等 Linux 环境。这里的 Makefile 默认使用 Clang。在下载目录打开终端，解压并进入工程文件夹。make 构建可执行文件；make test 检查程序行为。

```sh
unzip comp2017-process-runner.zip
cd comp2017-process-runner
make
make test
```

### 第一次运行：一个含空格的参数

```sh
./process_runner 32 -- /bin/echo 'hello team'
```

```text
stdout="hello team\n"
captured_bytes=11
truncated=no
child_exit=0
```

退出状态：0



shell 引号在记录器启动前构造一个 hello team 参数。子进程写出 11 字节，包含换行。记录器在 EOF 和 waitpid 后返回 0。

### 一兆字节输出，八字节预算

```sh
./process_runner 8 -- ./fixture_child burst
```

```text
stdout="AAAAAAAA"
captured_bytes=8
truncated=yes
child_exit=0
```

退出状态：0



辅助程序写出 1,048,576 个 A。只保存八个，但读完其余全部输出，让子进程能够结束。截断不会让子进程失败：记录器返回 0。

### 报告失败的检查程序

```sh
./process_runner 32 -- ./fixture_child fail
```

```text
stdout="check failed\n"
captured_bytes=13
truncated=no
child_exit=7
```

退出状态：7



13 字节信息完整保存，但子进程返回 7。记录器也返回 7。捕获成功与子进程成功是不同结论。

### 程序不存在，生命周期仍须完成

```sh
./process_runner 16 -- ./absent-program
```

```text
stdout=""
captured_bytes=0
truncated=no
child_exit=127
```

退出状态：127



子进程向继承的 stderr 写出 process_runner: execvp failed 和换行（不在此 stdout 区块中），再调用 _exit(127)。父进程读到 EOF、回收它，并返回 127。真实程序也能返回 127，因此只看状态存在歧义。

### 恰好填满，而且没有末尾换行

```sh
./process_runner 4 -- ./fixture_child fragment
```

```text
stdout="tail"
captured_bytes=4
truncated=no
child_exit=0
```

退出状态：0



tail 恰好四字节。没有丢弃字节，所以容量虽然已满，仍是 truncated=no。字节流结束不要求换行。记录器返回 0。

### 原样传递空格和 shell 特殊字符

```sh
./process_runner 64 -- ./fixture_child args 'two words' '$HOME;*'
```

```text
stdout="[two words][$HOME;*]"
captured_bytes=20
truncated=no
child_exit=0
```

退出状态：0



测试程序给每个参数加方括号。20 字节结果说明 two words 保持完整，$HOME;* 保持字面含义。记录器返回 0，从未构造命令字符串。

## 调试

### 大量输出的命令一直不结束。

父进程先等待再读取，或达到容量就停止读取。

用 make test 在容量 8 下运行有限 burst；检查每次正数读取后是否继续 read。

即使 keep 变成 0，也要读到 EOF，再调用 waitpid。

### 子进程已退出，但一直没有 EOF。

父进程保留了写端，或其他进程继承了写端。

画出双方所有写端描述符；检查父进程是否在 fork 后立即 close。

关闭父进程不用的写端。后代保留写端的问题需要未来的进程树策略。

### 四字节 tail 在容量 4 时被错误标成截断。

代码把容量满了误当成已经丢弃数据。

比较 fragment 在容量 4 和 3 下的结果；只有后者丢失一个字节。

只在真实正数读取中 keep<count 时设置截断。

### 报告退出码看起来是 1792，而不是 7。

代码把原始等待状态当成退出码输出。

运行 fail 测试，检查 WEXITSTATUS 前是否判断 WIFEXITED。

用等待宏解码，并在独立分支检查信号终止。

### NUL 字节之后的输出消失。

对原始捕获字节使用了 strlen 等字符串函数。

运行 bytes 测试：七个字节都必须以字符或转义形式可见。

循环到 result.captured，使用 unsigned char，并逐字节转义。

### 含空格的参数变成两个，或 $HOME 被展开。

外层 shell 调用没有正确引用，或实现中引入了命令字符串。

使用 args 测试，并在终端用单引号包围字面参数。

记录器保留收到的 argv；只在构造初始参数时使用 shell 引号。

## 测试计划

### 包含空格的一个参数

echo 输出 hello team 和换行：11 字节，退出 0。

发现意外拆分参数或丢失换行。

### 字面参数 $HOME;*

args 测试输出 [two words][$HOME;*]：20 字节。

发现命令拼接或展开。

### 1 MiB 输出，容量分别为 8、0、65536

恰好保留容量个字节，报告 truncated=yes，并在看门狗之前退出 0。

验证容量用完后仍有进展，并覆盖容量两端。

### 零容量下的空输出

保存零字节，truncated=no，退出 0。

预算为零本身不能证明丢失数据。

### 末尾片段 tail，容量 4 与 3

分别得到 tail/no 和 tai/yes，不要求换行。

区分刚好达到容量和溢出，也区分字节流与文本行。

### 检查程序返回 7

保存 check failed 和换行，显示 child_exit=7，返回 7。

记录器运行成功不能抹掉子进程失败状态。

### 本地可执行文件不存在

空捕获、固定 execvp 标准错误诊断、child_exit=127、返回 127。

覆盖子进程 _exit 路径和父进程 EOF/wait 生命周期。

### 子进程标准错误和二进制标准输出

stderr 保持独立；bytes 测试用可逆转义显示全部七个字节。

防止流混合、NUL 截断和原始终端控制字节输出。

### 子进程用 SIGTERM 结束自己

用平台信号编号显示 child_signal，并返回 128 加该编号。

不依赖时序地覆盖另一种等待状态分支。

### 错误命令行、负数或过大容量、缺少程序

返回 2，在 stderr 显示用法，没有 stdout 报告。

检查在分配或 fork 前拒绝输入，并防止数字溢出。

## 工程取舍

### 字节预算不是时间预算

保存字节数=min(N,C)，截断=(N>C)。读取仍需 O(N) 工作，内存为 O(C+4096)。没有超时或进程树控制。子进程等输入、后代保留 stdout、stderr 接收端阻塞或子进程一直不结束，都可能让运行停住。测试看门狗属于 test.py，不属于记录器。

### 两种输出流，只捕获一种

stdout 被捕获并在结束后显示。stdin 和 stderr 保持继承，stderr 可能先于稍后的 stdout 报告出现，但这不代表存在统一顺序。字节用 ASCII 转义显示，不做 Unicode 解码；容量可能切断 UTF-8 序列，但保留的字节仍可见。这不是原始二进制复制工具。

### 不构造命令字符串

argv 参数边界保持不变。无路径程序名使用继承的 PATH；明确路径更容易确定目标。POSIX execvp 对格式无法识别的可执行文本文件可能调用解释器。回退解释的是该文件，不是新拼接的参数字符串。程序继承权限、目录、环境和其他未设置 close-on-exec 的描述符；这不是沙箱。

### 状态码存在明确限制

普通子进程退出码原样返回。信号单独显示并映射为 128+N。命令行错误返回 2，已处理的记录器错误返回 125，子进程配置错误返回 126，exec 失败返回 127。子进程本身也能返回这些代码。没有 exec 错误管道，因此单看 127 无法识别 exec 失败。固定子进程诊断保留在独立 stderr 上。

### 有限 POSIX 范围与明确清理

模块假设单线程、描述符 0–2 已打开、阻塞 I/O、默认 SIGCHLD 处理且没有其他回收者。read/waitpid/dup2/子进程诊断 write 遇到 EINTR 会重试。读取失败只终止直接子进程并尝试回收。close 尽力执行而不重试；省略跨平台 close 中断恢复。没有应用信号处理器、转发或用户取消策略。中断记录器可能留下子进程，报告管道断开可能触发默认 SIGPIPE 终止。

## 完整源文件

### README.md

英文构建与工程指南

[下载文件](../project-code/comp2017-process-runner/README.md)

1. 先读四个实际命令例子及退出含义。

2. 按五个里程碑与描述符所有权表阅读。

3. 运行有限测试程序以外的程序前，先读适用范围。

### README.zh.md

完整中文配套指南

[下载文件](../project-code/comp2017-process-runner/README.zh.md)

1. 使用相同的编译、运行、测试和清理命令。

2. 把 EOF 与 wait 作为两个不同条件跟踪。

3. 查看信号、exec 回退和资源继承的中文解释。

### process.h

公开数据与所有权约定

[下载文件](../project-code/comp2017-process-runner/process.h)

```c
/* Leon | Original teaching project. */
#ifndef LEON_PROCESS_H
#define LEON_PROCESS_H

#include <stdbool.h>
#include <stddef.h>

#define PROCESS_MAX_CAPTURE 65536U

struct process_result {
    size_t captured;
    bool truncated;
    int wait_status;
};

/* Synchronous, single-threaded caller; standard descriptors 0, 1, 2 must be open.
 * argv is a nonempty, NULL-terminated argument vector, borrowed for this call.
 * buffer belongs to the caller and holds at least capacity bytes (0 is valid).
 * Return 0 after reaping the direct child, even if it failed. On -1, errno
 * describes a runner error; do not consume result. No timeout is provided. */
int process_run(char *const argv[], unsigned char *buffer, size_t capacity,
                struct process_result *result);

#endif
```

1. 查看容量上限与 process_result 的三个字段。

2. 注意缓冲区与 argv 只是借用，没有转移所有权。

3. 返回 0 表示成功回收子进程，即使子进程本身返回非零。

### main.c

命令行检查、字节显示与退出码映射

[下载文件](../project-code/comp2017-process-runner/main.c)

```c
/* Leon | Original teaching project. */
#include "process.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/wait.h>

static int parse_capacity(const char *text, size_t *capacity)
{
    size_t value = 0;
    if (*text == '\0') {
        return -1;
    }
    for (const char *p = text; *p != '\0'; ++p) {
        if (*p < '0' || *p > '9') {
            return -1;
        }
        size_t digit = (size_t)(*p - '0');
        if (value > (PROCESS_MAX_CAPTURE - digit) / 10) {
            return -1;
        }
        value = value * 10 + digit;
    }
    *capacity = value;
    return 0;
}

/* A byte view: no strlen on captured data, and no raw terminal controls. */
static void print_bytes(const unsigned char *data, size_t length)
{
    fputs("stdout=\"", stdout);
    for (size_t i = 0; i < length; ++i) {
        unsigned char byte = data[i];
        switch (byte) {
        case '\n': fputs("\\n", stdout); break;
        case '\r': fputs("\\r", stdout); break;
        case '\t': fputs("\\t", stdout); break;
        case '\\': fputs("\\\\", stdout); break;
        case '"': fputs("\\\"", stdout); break;
        default:
            if (byte >= 32 && byte <= 126) {
                putchar((int)byte);
            } else {
                printf("\\x%02X", (unsigned int)byte);
            }
        }
    }
    puts("\"");
}

static int report(const unsigned char *data, const struct process_result *result)
{
    print_bytes(data, result->captured);
    printf("captured_bytes=%zu\ntruncated=%s\n", result->captured,
           result->truncated ? "yes" : "no");
    if (WIFEXITED(result->wait_status)) {
        int code = WEXITSTATUS(result->wait_status);
        printf("child_exit=%d\n", code);
        return code;
    }
    if (WIFSIGNALED(result->wait_status)) {
        int number = WTERMSIG(result->wait_status);
        printf("child_signal=%d\n", number);
        return 128 + number;
    }
    fputs("process_runner: unexpected wait status\n", stderr);
    return 125;
}

int main(int argc, char **argv)
{
    size_t capacity;
    if (argc < 4 || strcmp(argv[2], "--") != 0 || argv[3][0] == '\0' ||
        parse_capacity(argv[1], &capacity) == -1) {
        fputs("usage: process_runner CAP -- PROGRAM [ARG ...]\n"
              "CAP must be decimal digits from 0 to 65536.\n", stderr);
        return 2;
    }
    unsigned char *data = malloc(capacity > 0 ? capacity : 1);
    if (data == NULL) {
        fputs("process_runner: allocation failed\n", stderr);
        return 125;
    }
    struct process_result result;
    if (process_run(&argv[3], data, capacity, &result) == -1) {
        perror("process_runner");
        free(data);
        return 125;
    }
    int code = report(data, &result);
    free(data);
    if (fflush(stdout) == EOF || ferror(stdout)) {
        fputs("process_runner: report write failed\n", stderr);
        return 125;
    }
    return code;
}
```

1. parse_capacity 在分配前拒绝格式错误或越界输入。

2. print_bytes 使用字节数而非 strlen，因此保留内部 NUL。

3. report 解码等待状态；main 在已处理路径释放内存，并检查最终 stdout 刷新。

### process.c

管道配置、fork/exec、连续读取与等待

[下载文件](../project-code/comp2017-process-runner/process.c)

```c
/* Leon | Original teaching project. */
#include "process.h"

#include <errno.h>
#include <fcntl.h>
#include <signal.h>
#include <string.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

/* Child failure: no stdio flushing or parent atexit handlers after fork. */
static void child_failure(const char *message, size_t length, int code)
{
    while (length > 0) {
        ssize_t sent = write(STDERR_FILENO, message, length);
        if (sent < 0 && errno == EINTR) {
            continue;
        }
        if (sent <= 0) {
            break;
        }
        message += (size_t)sent;
        length -= (size_t)sent;
    }
    _exit(code);
}

static void execute_child(int read_end, int write_end, char *const argv[])
{
    static const char setup_error[] = "process_runner: stdout setup failed\n";
    static const char exec_error[] = "process_runner: execvp failed\n";
    (void)close(read_end);
    int copied;
    do {
        copied = dup2(write_end, STDOUT_FILENO);
    } while (copied == -1 && errno == EINTR);
    if (copied == -1) {
        (void)close(write_end);
        child_failure(setup_error, sizeof(setup_error) - 1, 126);
    }
    (void)close(write_end);
    /* The original argument boundaries survive; no command string is built. */
    execvp(argv[0], argv);
    child_failure(exec_error, sizeof(exec_error) - 1, 127);
}

static int drain_output(int read_end, unsigned char *buffer, size_t capacity,
                        struct process_result *result)
{
    unsigned char chunk[4096];
    for (;;) {
        ssize_t received = read(read_end, chunk, sizeof(chunk));
        if (received == -1 && errno == EINTR) {
            continue;
        }
        if (received == -1) {
            return -1;
        }
        if (received == 0) {
            return 0;
        }
        size_t count = (size_t)received;
        size_t space = capacity - result->captured;
        size_t keep = count < space ? count : space;
        if (keep > 0) {
            memcpy(buffer + result->captured, chunk, keep);
            result->captured += keep;
        }
        if (keep < count) {
            result->truncated = true;
        }
        /* A full buffer stops copying, never reading. The child must progress. */
    }
}

int process_run(char *const argv[], unsigned char *buffer, size_t capacity,
                struct process_result *result)
{
    if (argv == NULL || argv[0] == NULL || argv[0][0] == '\0' ||
        result == NULL || capacity > PROCESS_MAX_CAPTURE ||
        (capacity > 0 && buffer == NULL)) {
        errno = EINVAL;
        return -1;
    }
    /* Keeps both pipe descriptors above 2, so dup2/close ownership is simple. */
    for (int fd = STDIN_FILENO; fd <= STDERR_FILENO; ++fd) {
        if (fcntl(fd, F_GETFD) == -1) {
            return -1;
        }
    }
    *result = (struct process_result){0, false, 0};
    int channel[2];
    if (pipe(channel) == -1) {
        return -1;
    }
    pid_t child = fork();
    if (child == -1) {
        int saved = errno;
        (void)close(channel[0]);
        (void)close(channel[1]);
        errno = saved;
        return -1;
    }
    if (child == 0) {
        execute_child(channel[0], channel[1], argv);
    }
    /* Parent owns only the read end. Keeping any write end would prevent EOF. */
    (void)close(channel[1]);
    int failure = 0;
    if (drain_output(channel[0], buffer, capacity, result) == -1) {
        failure = errno;
        /* On a read error, abort our direct child before trying to reap it. */
        (void)kill(child, SIGKILL);
    }
    (void)close(channel[0]);
    pid_t waited;
    do {
        waited = waitpid(child, &result->wait_status, 0);
    } while (waited == -1 && errno == EINTR);
    if (waited == -1 && failure == 0) {
        failure = errno;
    }
    if (failure != 0) {
        errno = failure;
        return -1;
    }
    return 0;
}
```

1. 先检查标准描述符，再在 fork 前创建管道，让双方都能引用。

2. 把 execute_child 与 drain_output 分开，便于跟踪描述符所有权。

3. 清理前保存 errno，在适当处重试 EINTR，并在读取失败后仍尝试回收。

### fixtures/child.c

有限的合成输出与状态生成器

[下载文件](../project-code/comp2017-process-runner/fixtures/child.c)

```c
/* Leon | Original teaching project. */
#include <signal.h>
#include <stdio.h>
#include <string.h>

/* Synthetic, finite output only: no files, descendants, input, or sleeps. */
int main(int argc, char **argv)
{
    if (argc < 2) {
        return 2;
    }
    if (strcmp(argv[1], "args") == 0) {
        for (int i = 2; i < argc; ++i) {
            printf("[%s]", argv[i]);
        }
    } else if (strcmp(argv[1], "burst") == 0) {
        char block[4096];
        memset(block, 'A', sizeof(block));
        for (int i = 0; i < 256; ++i) {
            if (fwrite(block, 1, sizeof(block), stdout) != sizeof(block)) {
                return 3;
            }
        }
    } else if (strcmp(argv[1], "fragment") == 0) {
        fputs("tail", stdout);
    } else if (strcmp(argv[1], "fail") == 0) {
        puts("check failed");
        return 7;
    } else if (strcmp(argv[1], "stderr") == 0) {
        fputs("diagnostic\n", stderr);
        puts("ok");
    } else if (strcmp(argv[1], "bytes") == 0) {
        const unsigned char bytes[] = {0, 255, '"', '\\', '\t', '\r', '\n'};
        if (fwrite(bytes, 1, sizeof(bytes), stdout) != sizeof(bytes)) {
            return 3;
        }
    } else if (strcmp(argv[1], "signal") == 0) {
        (void)raise(SIGTERM);
        return 3;
    } else if (strcmp(argv[1], "empty") != 0) {
        return 2;
    }
    return fflush(stdout) == 0 ? 0 : 3;
}
```

1. args 给每个参数加方括号，让空格边界可见。

2. burst 写 256 个固定块；empty 与 fragment 在不依赖行的情况下检查 EOF。

3. fail、stderr、bytes 和 signal 分别产生不同可观察行为。

### test.py

十四个真实进程回归测试

[下载文件](../project-code/comp2017-process-runner/test.py)

```python
#!/usr/bin/env python3
# Leon | Original teaching project.
"""Build a temporary copy and exercise only bounded, local fixture programs."""
import os
from pathlib import Path
import shutil
import signal
import subprocess
import tempfile
import unittest

SOURCE = Path(__file__).resolve().parent


class RunnerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix="guoliang-process-test-")
        cls.addClassCleanup(cls.temp.cleanup)
        cls.work = Path(cls.temp.name)
        for name in ("main.c", "process.c", "process.h", "Makefile"):
            shutil.copy2(SOURCE / name, cls.work / name)
        shutil.copytree(SOURCE / "fixtures", cls.work / "fixtures")
        built = subprocess.run(["make", "all"], cwd=cls.work, text=True,
                               capture_output=True, timeout=30, check=False)
        if built.returncode:
            raise AssertionError(built.stdout + built.stderr)

    def run_runner(self, *args):
        # A new group lets a timeout clean up both runner and its own child.
        child = subprocess.Popen(["./process_runner", *args], cwd=self.work,
                                 stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE, start_new_session=True)
        try:
            out, err = child.communicate(timeout=8)
        except subprocess.TimeoutExpired:
            os.killpg(child.pid, signal.SIGKILL)
            child.communicate()
            self.fail("bounded fixture timed out; possible pipe/wait deadlock")
        return child.returncode, out.decode("ascii"), err.decode("ascii")

    def test_echo_and_literal_space_argument(self):
        # Catches splitting one argument or losing the trailing newline.
        self.assertEqual(self.run_runner("32", "--", "/bin/echo", "hello team"),
                         (0, 'stdout="hello team\\n"\ncaptured_bytes=11\n'
                          'truncated=no\nchild_exit=0\n', ""))

    def test_metacharacters_are_arguments(self):
        # No shell may expand the dollar sign, wildcard, or semicolon.
        self.assertEqual(self.run_runner("64", "--", "./fixture_child", "args",
                                        "two words", "$HOME;*"),
                         (0, 'stdout="[two words][$HOME;*]"\ncaptured_bytes=20\n'
                          'truncated=no\nchild_exit=0\n', ""))

    def test_large_output_is_drained_after_cap(self):
        self.assertEqual(self.run_runner("8", "--", "./fixture_child", "burst"),
                         (0, 'stdout="AAAAAAAA"\ncaptured_bytes=8\n'
                          'truncated=yes\nchild_exit=0\n', ""))

    def test_zero_cap_still_drains(self):
        self.assertEqual(self.run_runner("0", "--", "./fixture_child", "burst"),
                         (0, 'stdout=""\ncaptured_bytes=0\n'
                          'truncated=yes\nchild_exit=0\n', ""))

    def test_empty_output_is_not_truncation(self):
        self.assertEqual(self.run_runner("0", "--", "./fixture_child", "empty"),
                         (0, 'stdout=""\ncaptured_bytes=0\n'
                          'truncated=no\nchild_exit=0\n', ""))

    def test_exact_cap_and_final_fragment(self):
        self.assertEqual(self.run_runner("4", "--", "./fixture_child", "fragment"),
                         (0, 'stdout="tail"\ncaptured_bytes=4\n'
                          'truncated=no\nchild_exit=0\n', ""))

    def test_one_byte_over_cap(self):
        self.assertEqual(self.run_runner("3", "--", "./fixture_child", "fragment"),
                         (0, 'stdout="tai"\ncaptured_bytes=3\n'
                          'truncated=yes\nchild_exit=0\n', ""))

    def test_nonzero_child_status_is_returned(self):
        self.assertEqual(self.run_runner("32", "--", "./fixture_child", "fail"),
                         (7, 'stdout="check failed\\n"\ncaptured_bytes=13\n'
                          'truncated=no\nchild_exit=7\n', ""))

    def test_missing_program_is_reaped(self):
        self.assertEqual(self.run_runner("16", "--", "./absent-program"),
                         (127, 'stdout=""\ncaptured_bytes=0\n'
                          'truncated=no\nchild_exit=127\n',
                          "process_runner: execvp failed\n"))

    def test_stderr_is_inherited_not_captured(self):
        self.assertEqual(self.run_runner("16", "--", "./fixture_child", "stderr"),
                         (0, 'stdout="ok\\n"\ncaptured_bytes=3\n'
                          'truncated=no\nchild_exit=0\n', "diagnostic\n"))

    def test_byte_escaping_is_lossless_for_the_prefix(self):
        self.assertEqual(self.run_runner("16", "--", "./fixture_child", "bytes"),
                         (0, 'stdout="\\x00\\xFF\\\"\\\\\\t\\r\\n"\ncaptured_bytes=7\n'
                          'truncated=no\nchild_exit=0\n', ""))

    def test_signal_status_is_reported(self):
        code, out, err = self.run_runner("16", "--", "./fixture_child", "signal")
        self.assertEqual(code, 128 + signal.SIGTERM)
        self.assertEqual(out, 'stdout=""\ncaptured_bytes=0\ntruncated=no\n'
                             f'child_signal={signal.SIGTERM}\n')
        self.assertEqual(err, "")

    def test_maximum_cap(self):
        code, out, err = self.run_runner("65536", "--", "./fixture_child", "burst")
        self.assertEqual(code, 0)
        self.assertEqual(out, 'stdout="' + "A" * 65536 + '"\ncaptured_bytes=65536\n'
                             'truncated=yes\nchild_exit=0\n')
        self.assertEqual(err, "")

    def test_bad_cli_never_starts_a_child(self):
        cases = [(), ("8", "--"), ("8", "--", ""),
                 ("-1", "--", "./fixture_child", "empty"),
                 ("65537", "--", "./fixture_child", "empty"),
                 ("8x", "--", "./fixture_child", "empty"),
                 (" 8", "--", "./fixture_child", "empty"),
                 ("9999999999999999999999999", "--", "./fixture_child", "empty"),
                 ("8", "wrong", "./fixture_child", "empty")]
        for args in cases:
            with self.subTest(args=args):
                code, out, err = self.run_runner(*args)
                self.assertEqual(code, 2)
                self.assertEqual(out, "")
                self.assertEqual(err, "usage: process_runner CAP -- PROGRAM [ARG ...]\n"
                                     "CAP must be decimal digits from 0 to 65536.\n")


if __name__ == "__main__":
    unittest.main(verbosity=2)
```

1. 只把项目输入复制到 TemporaryDirectory，再在那里编译。

2. Popen 使用参数列表、DEVNULL 输入、分离的输出管道、新会话和 8 秒看门狗。

3. 断言把实际 stdout、stderr 和返回码与手工预期比较；超时只终止测试进程组。

### Makefile

严格且可重复的 all/test/clean 入口

[下载文件](../project-code/comp2017-process-runner/Makefile)

```make
# Leon | Original teaching project.
CC = clang
CFLAGS = -std=c11 -Wall -Wextra -Werror -pedantic -pthread
CPPFLAGS = -D_POSIX_C_SOURCE=200809L

.PHONY: all test clean
all: process_runner fixture_child

process_runner: main.c process.c process.h
	$(CC) $(CPPFLAGS) $(CFLAGS) main.c process.c -o $@

fixture_child: fixtures/child.c
	$(CC) $(CPPFLAGS) $(CFLAGS) fixtures/child.c -o $@

test:
	python3 test.py

clean:
	rm -f process_runner fixture_child
```

1. all 编译记录器和独立测试辅助程序。

2. 明确指定 C11、POSIX 功能声明、警告和 Werror。

3. test 调用 Python；clean 只删除两个生成的可执行文件。

## 扩展方向

### 增加独立的 exec 错误通道

增加第二条管道，给子进程写端设置 close-on-exec。exec 成功自动关闭它，exec 失败则先写入简短 errno 记录，再 _exit。保持清晰所有权，并完整处理错误通道和 stdout。

区分真实程序返回 127 与无法执行缺失路径；两者都回收子进程且不泄漏描述符。

### 把截止时间与取消作为独立功能设计

先明确进程组所有权、单调时钟截止时间、基于 poll 的读取、终止宽限期、最终强制清理，以及后代和调用者信号策略，再编码。开发时只用有限且自己拥有的测试程序。

受控子进程超过预算时，在有界时间内产生超时结果；所有自己管理的子进程被回收、管道关闭、保存输出正确。测试不能断言精确调度时间。

## 一手参考资料

- [The Open Group: POSIX fork](https://pubs.opengroup.org/onlinepubs/9799919799/functions/fork.html)

- [The Open Group: POSIX exec family](https://pubs.opengroup.org/onlinepubs/9799919799/functions/exec.html)

- [The Open Group: POSIX pipe](https://pubs.opengroup.org/onlinepubs/9799919799/functions/pipe.html)

- [The Open Group: POSIX read](https://pubs.opengroup.org/onlinepubs/9799919799/functions/read.html)

- [The Open Group: POSIX wait and waitpid](https://pubs.opengroup.org/onlinepubs/9699919799/functions/wait.html)

- [The Open Group: POSIX dup and dup2](https://pubs.opengroup.org/onlinepubs/9799919799/functions/dup.html)

- [The Open Group: POSIX _Exit and _exit](https://pubs.opengroup.org/onlinepubs/9799919799/functions/_exit.html)

---
Leon
