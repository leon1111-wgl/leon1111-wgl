# COMP2017 — 有界文件统计流水线

> Leon | Original engineering workshop

![Leon learning route](../assets/maps/comp2017-thread-pipeline.zh.svg)

[English](comp2017-thread-pipeline.en.md) · [中文](comp2017-thread-pipeline.zh.md)

构建可实际使用的 pthread 工作线程池，统计文件的字节、行和单词。四槽队列协调任务，每个输入拥有独立结果槽，使最终报告顺序确定。

[下载完整工程 ZIP](../downloads/comp2017-thread-pipeline.zip)

## 故事

米娜在学校机器人社做志愿者。每次活动结束，她收到几份小笔记，想知道各文件有多少字节、逻辑行和单词。有些笔记是空的，有些末尾没有换行，抄写的文件名也可能有误。即使一个文件打不开，她仍需要有用的报告。

她先做一个定义清楚的单文件扫描器，用很小的合成笔记核对。接着给文件参数编号，把编号放进只有四个位置的队列。位置用完时，生产者等待空位。多个工作线程可以领取不同任务，但每个线程只打开自己的文件，只写该任务的结果。这样先说清所有权，再引入并发。

最后一个任务入队，并不等于最后一个任务已经完成。米娜关闭队列，表示不再有新任务，让消费者处理剩余任务，再等待所有工作线程结束。之后才按输入顺序打印结果槽。打不开的文件会明确标为失败，不会假装得到全零统计。

最后，她用长短不同的输入、重复调度和可控故障检验程序。这个项目展示正确的协调方式，小样例并不证明线程越多越快。代码、样例和说明都是 Leon 原创教学内容，与所提供的作业无关。

### 开始前先读

- [文件流、二进制记录与错误](../courses/comp2017.zh.html#file-streams): 统计前先区分成功的短读取、文件结束和读取错误。

- [动态分配与对象生命周期](../courses/comp2017.zh.html#allocation-ownership): 所有工作线程结束前，主线程栈对象和借用的 argv 路径都必须有效。

- [创建线程、等待结束与取消](../courses/comp2017.zh.html#thread-lifecycle): 创建数量有上限的可等待线程，只 join 创建成功的句柄。

- [数据竞争、互斥锁与原子性](../courses/comp2017.zh.html#data-races-mutexes): 共享队列状态用互斥锁保护，每项结果由一个线程独占写入。

- [条件变量与生产者—消费者等待](../courses/comp2017.zh.html#condition-variables): 用 while 循环等待状态条件，每次醒来都重新检查。

- [并行模式：划分、等待与合并](../courses/comp2017.zh.html#parallel-patterns): 区分生产者、固定消费者池和按序报告阶段。

### 学习成果

- 定义并实现字节数、逻辑行数和 ASCII 分隔单词数，正确处理读取缓冲区边界。

- 解释环形队列不变量、背压、条件等待以及关闭后排空。

- 说明唯一写入者和成功 join 如何避免结果数据竞争。

- 用有界样例、独立预期结果和超时测试正常运行、启动失败与 I/O 失败。

## 需求与契约

### 接受 WORKERS 和零到 128 个文件路径，WORKERS 限于 1..16。

有限线程池和有界任务列表便于理解资源用量。零任务也是正常生命周期。

尝试 1、16、0、17、2x、不填线程数，以及 129 个文件参数。非法命令行退出码为 2，且不打印报告。

### 队列容量固定为四个编号，使用一把互斥锁及 not_empty、not_full 条件变量。

队列满时生产者等待，而非增加存储。暂时没有任务时消费者休眠。

检查两个条件 while 循环，测试少量任务、超过容量的任务和重复执行的 37 个任务。

### 每个发布的编号只取出一次，每个结果只有一个写入者，所有线程 join 后才打印。

并发完成的先后会变化。独立结果槽和之后的报告阶段保持输入顺序。

将 1、2、4、16 个线程的完整标准输出与独立顺序算法比较。

### 行数计算 LF，加上末尾未终止的逻辑行；单词仅由六种 ASCII 空白字节分隔。

空文件、末尾换行和缓冲区边界，都应先定义语义再写代码。

空文件三项计数均为 0。晚间样例只有一个 LF，但有 26 字节、2 行、5 个单词。

### 只接受普通文件，每项扫描最多 8 MiB；文件失败要报告，但不丢弃其他任务。

教学程序应有明确存储和工作量上限。部分计数不是完整结果。

测试恰好达到字节上限、多一个字节、缺失路径、目录以及没有写入方的 FIFO。

### 正常路径关闭并排空；线程创建失败时，先关闭队列，再等待已创建线程。

线程若还在等待永远不会出现的任务，join 会卡住。未成功创建的句柄不能 join。

临时测试替身强制第一个线程创建前失败，以及创建两个后失败。两者必须退出 1，无报告且不超时。

## 结构与所有权

**生产者与资源拥有者：main.c**

验证所有参数，初始化存储，创建完整线程池，每个编号只发布一次，然后关闭队列。同一主线程随后执行 join 和报告。

**有界任务交接：queue.c**

环形队列最多放四个编号。count、head、closed 和 entries 由一把锁保护。not_empty 和 not_full 唤醒线程后，线程必须重新检查条件。

**消费者与扫描器：consume + stats.c**

每个工作线程反复取一个编号，释放队列锁，打开自己的普通文件，并写入对应的 FileStats。文件可以按任意顺序完成。

**join 后按序报告**

所有 join 成功后，主线程从 0 到 J−1 读取结果槽。失败槽打印错误类别，成功槽打印完整计数。

初始化 → 创建全部线程 → 发布编号 → 关闭 → 排空 → JOIN → 报告。主线程生产时，消费者可以同时扫描。未关闭且空：消费者等待；未关闭且满：生产者等待；已关闭且非空：继续消费；已关闭且空：退出。若创建失败，此时尚未发布编号：关闭 → JOIN 已创建线程 → 销毁 → 退出 1。

- 队列字段和同步对象 → 主线程拥有生命周期。各线程借用队列，运行中的状态访问都持有队列锁。 → 所有已创建线程 join 后，主线程才销毁两个条件变量和互斥锁。

- argv 路径和 WorkerContext → 主线程把稳定只读路径和已初始化上下文借给各工作线程。 → 上下文在最后一次 join 前始终留在主线程栈帧中，argv 在进程退出前有效。

- 每个任务一个 FileStats 槽 → 取出编号 i 的工作线程独占写入 results[i]。主线程只在所有线程 join 后读取。 → 存储是主线程栈中的有界数组，无需 free，工作线程访问期间始终有效。

- 文件描述符和 4096 字节缓冲区 → 只有扫描它的工作线程使用该描述符、文件偏移、缓冲区和单词状态。 → 打开成功后，每条路径都会由 scan_file 尝试关闭，局部缓冲区随调用结束。

- 可等待的线程句柄 → 主线程用 started 表示前面多少个句柄创建成功。 → 启动成功和部分启动失败都 join 该前缀，绝不 join 未创建的句柄。

<a id="milestone-precise-counts"></a>

## 1. 先精确定义一个文件的答案

先实现正确的单文件扫描器，再加入线程池。

并发无法修复含糊定义。一行是以 LF 结束的一段，或者末尾非空的未终止片段。单词在非分隔字节跟随分隔字节或流起点时开始。这是两个小状态机，状态必须跨短读取和缓冲区边界保留。

1. 先读 stats.h：结果包含计数、状态和可选系统错误。只有 SCAN_OK 才能把计数作为完整结果报告。

2. 用空文件、a、a\n 和 a b 追踪计数器。把 in_word 和 last 放在读取循环外。转换为 size_t 前先检查 received < 0。

3. 到达 EOF 时，仅当文件非空且末尾不是 LF 才补一行。读取失败时保留错误，不报告部分计数。

教学摘录；运行时使用完整工程。

```c
static void count_stream(int descriptor, FileStats *result) {
    unsigned char buffer[4096];
    bool in_word = false;
    unsigned char last = '\n';
    for (;;) {
        ssize_t received = read(descriptor, buffer, sizeof buffer);
        if (received < 0) {
            if (errno == EINTR) {
                continue;
            }
            result->status = SCAN_READ;
            result->system_error = errno;
            return;
        }
        if (received == 0) {
            break;
        }
        size_t length = (size_t)received;
        if (length > FILE_BYTE_LIMIT - result->bytes) {
            result->status = SCAN_TOO_LARGE;
            return;
        }
        result->bytes += length;
        for (size_t i = 0; i < length; i++) {
            unsigned char byte = buffer[i];
            if (byte == '\n') {
                result->lines++;
            }
            bool space = separator(byte);
            if (!space && !in_word) {
                result->words++;
            }
            in_word = !space;
            last = byte;
        }
    }
    if (result->bytes != 0 && last != '\n') {
        result->lines++;
    }
}
```

这是最终扫描器的节选，不是独立程序。separator 和相关类型在完整项目中。result->bytes 记录已处理块，减法检查保证统计不超过 8 MiB 约定。缓冲区反复使用，in_word 和 last 则跨缓冲区保留。

**为什么六个空白字节的样例有零个单词，却有两个逻辑行？**

每个字节都是分隔符，所以没有单词开始。有一个 LF，之后还有垂直制表和换页字节，这个非空尾段构成第二行。

<a id="milestone-bounded-queue"></a>

## 2. 用有界队列代替不断增长的列表

环形队列有空位时才发布任务。

队列容量和总任务数是两回事。head 是最早的占用位置，count 是占用数量。下一插入位置为 (head + count) 对容量取模。一把锁让条件检查和随后的修改成为受保护的状态变化。等待必须释放锁，消费者才能取走任务腾出空位。

1. 画四个格子，追踪入队 0、入队 1、出队、入队 2。核对每次操作前后 0 <= count <= 4。

2. 对照阅读 queue_push 和 queue_pop。生产者等待 not_full，消费者等待 not_empty。两者都用包含 closed 的 while 条件。

3. 在锁内修改 count 后通知，再解锁。文件读取完全放在队列锁之外。

教学摘录；运行时使用完整工程。

```c
bool queue_push(WorkQueue *queue, size_t job) {
    thread_check(pthread_mutex_lock(&queue->mutex), "mutex lock");
    while (queue->count == QUEUE_CAPACITY && !queue->closed) {
        thread_check(pthread_cond_wait(&queue->not_full, &queue->mutex),
                     "wait not_full");
    }
    if (queue->closed) {
        thread_check(pthread_mutex_unlock(&queue->mutex), "mutex unlock");
        return false;
    }
    size_t tail = (queue->head + queue->count) % QUEUE_CAPACITY;
    queue->entries[tail] = job;
    queue->count++;
    thread_check(pthread_cond_signal(&queue->not_empty), "signal not_empty");
    thread_check(pthread_mutex_unlock(&queue->mutex), "mutex unlock");
    return true;
}
```

这个完整函数节选自 queue.c。条件唤醒并不预留空位，while 会重新检查共享状态。即使仍有空间，已关闭队列也拒绝新任务。queue_pop 在同一把锁下取出一个编号，并通知 not_full。

**为什么扫描文件时仍持有队列锁会破坏预期的并发？**

其他工作线程无法取任务，主线程也无法入队，直到整个文件扫描结束。锁只保护短暂队列变化，不应包住独立扫描工作。

<a id="milestone-owned-results"></a>

## 3. 给每个任务唯一写入者

用小型工作循环连接队列和扫描器，同时保持报告顺序。

共享结果数组并不自动产生竞争。每个编号只入队一次，由一次受锁保护的出队取走，因此每个元素恰好有一个写入者。工作线程共享只读上下文，但不共享可变计数器或文件偏移。主线程等待所有写入者结束后才观察数组。

1. 沿着 argv[i + 2]、queue_push(i)、queue_pop(&job) 和 results[job] 追踪任务 i。打印给用户的编号从一开始。

2. 所有 join 完成前，队列、上下文、路径和结果都要有效。不要把不断变化的循环局部任务变量地址交给线程。

3. scan_file 失败时，把错误写入同一结果槽。消费者循环仍继续领取后续任务。

教学摘录；运行时使用完整工程。

```c
static void *consume(void *argument) {
    WorkerContext *context = argument;
    size_t job;
    while (queue_pop(context->queue, &job)) {
        /* Exactly one pop receives each index. No other worker writes this
           result, and main waits for all joins before reading any result. */
        scan_file(context->paths[job], &context->results[job]);
    }
    return NULL;
}
```

这段最终程序节选使用 main.c 中声明的 WorkerContext。queue_pop 返回前已释放队列锁，扫描能够并发进行。工作线程不打印。不同 FileStats 对象有不同写入者，主线程之后的 join 保证读取前的可见性。

**任务 8 比任务 1 先结束时，结果放在哪里，何时打印？**

写入 results[7]。所有工作线程 join 后，主线程第八个打印该槽。输出顺序不由完成顺序决定。

<a id="milestone-close-drain-join"></a>

## 4. 结束时不丢弃已入队任务

区分“暂时没任务”和“再也不会有任务”，安全结束共享对象的生命周期。

空队列本身无法告诉消费者该等待还是离开，closed 补充这个信息。关闭不会删除待处理编号。关闭后 count 仍大于零就继续取出，直到变为零才返回。广播唤醒所有等待者，因为每个空闲线程都必须知道该结束了，即使文件列表一开始就为空。

1. 把出队条件读成“为空且仍未关闭时等待”。关闭但非空的队列仍然可消费。

2. 生产循环之后调用 queue_close，完成阶段切换。追踪零任务情况：所有工作线程最终都必须看到 closed 并退出。

3. 等待每个已创建线程结束，再销毁同步对象并打印。工作线程仍可能访问的互斥锁或条件变量不能销毁。

教学摘录；运行时使用完整工程。

```c
void queue_close(WorkQueue *queue) {
    thread_check(pthread_mutex_lock(&queue->mutex), "mutex lock");
    queue->closed = true;
    /* All empty-queue consumers must learn that no future job can arrive. */
    thread_check(pthread_cond_broadcast(&queue->not_empty), "broadcast not_empty");
    thread_check(pthread_cond_broadcast(&queue->not_full), "broadcast not_full");
    thread_check(pthread_mutex_unlock(&queue->mutex), "mutex unlock");
}
```

这段 queue.c 节选在两类等待共用的锁内修改 closed。not_empty 广播结束空队列等待，not_full 也会让等待的生产者检查关闭状态。在当前程序中，只有主线程在生产完成后关闭，因此正常生产者不会在这次关闭时被阻塞。queue_pop 会排空而非丢弃任务。

**关闭队列时有十六个空闲线程，为什么只通知一个不够？**

其余线程可能一直睡眠，因为之后不会再有任务到达并通知它们。广播让每个线程重新获取锁，看到已关闭且为空，然后返回。

<a id="milestone-failure-evidence"></a>

## 5. 同时检验失败路径与正常路径

用有界自动化测试检查部分启动失败、文件失败、非法命令行和确定性输出。

线程创建成功后句柄才有效。如果完整线程池创建前就发布任务，失败时部分任务可能已经运行，使清理更复杂。本设计先创建完整线程池，所以启动失败时能关闭空队列，join 成功的句柄前缀，不打印误导性的部分报告。

1. 把 started 分别取 0 和 2，追踪创建失败分支。只 join 已创建线程，此时还没有发布任何任务编号。

2. 运行 make test。它在临时副本编译，独立计算预期计数，检查负面情况，并用不同线程数重复执行 37 个任务。

3. 阅读 pthread_create 和 read 的临时故障注入替身。它们安全触发少见失败。Clang 运行环境支持时，可选运行 python3 test.py --tsan。

教学摘录；运行时使用完整工程。

```c
    for (; started < workers; started++) {
        error = pthread_create(&threads[started], NULL, consume, &context);
        if (error != 0) {
            fprintf(stderr, "thread creation failed after %zu workers "
                            "(pthread error %d)\n", started, error);
            /* No jobs are published until the whole pool exists. */
            queue_close(&queue);
            join_workers(threads, started);
            queue_destroy(&queue);
            return EXIT_FAILURE;
        }
    }
```

这是 main.c 实际的线程池创建循环，started、workers、context、queue、threads 和 error 在上方声明。运行中的互斥锁、条件变量或 join 错误采用另一套明确的快速失败策略，不能把它说成优雅恢复。完整程序及其错误检查才是可运行单元。

**48 次压力运行一致，或一次 ThreadSanitizer 无报告，能证明所有调度安全吗？**

不能。它们只能暴露实际观察到的执行中的缺陷。还需要论证任务唯一交付、每槽唯一写入者、条件受锁保护、对象生命周期正确，以及读取前完成 join。

## 构建与运行

使用 macOS 或 Linux 上支持 C11 的 Clang、make 和 Python 3。Windows 可使用 WSL 等 Linux 环境。这里的 Makefile 默认使用 Clang。在下载目录打开终端，解压并进入工程文件夹。make 构建可执行文件；make test 检查程序行为。

```sh
unzip comp2017-thread-pipeline.zip
cd comp2017-thread-pipeline
make
make test
```

### 三份笔记，三个线程

```sh
./thread_pipeline 3 fixtures/morning.txt fixtures/evening.txt fixtures/empty.txt
```

```text
job=1 bytes=37 lines=2 words=6
job=2 bytes=26 lines=2 words=5
job=3 bytes=0 lines=0 words=0
summary files=3 ok=3 failed=0
```

退出状态：0



晚间文件末尾无换行的行仍被计入，空文件也成功。标准输出按文件参数原顺序排列。退出码为 0，标准错误为空。先运行一次 make；这里的输出面板不包含编译信息。

### 任务数多于四槽队列

```sh
./thread_pipeline 1 fixtures/morning.txt fixtures/evening.txt fixtures/blank.txt fixtures/empty.txt fixtures/spaces.txt
```

```text
job=1 bytes=37 lines=2 words=6
job=2 bytes=26 lines=2 words=5
job=3 bytes=2 lines=2 words=0
job=4 bytes=0 lines=0 words=0
job=5 bytes=6 lines=2 words=0
summary files=5 ok=5 failed=0
```

退出状态：0



五个任务通过一次只放四个编号的队列，即使只有一个消费者也能完成。空行和纯空白仍是有意义的情况。退出码为 0，标准错误为空。此样例验证正确性，不衡量吞吐量。

### 零文件与十六个等待消费者

```sh
./thread_pipeline 16
```

```text
summary files=0 ok=0 failed=0
```

退出状态：0



空任务列表合法。主线程关闭队列并广播，各消费者看到空且关闭后返回，每个线程都被 join。退出码为 0，无标准错误。

### 缺失文件保留自己的位置

```sh
./thread_pipeline 2 fixtures/morning.txt fixtures/missing.txt fixtures/evening.txt
```

```text
job=1 bytes=37 lines=2 words=6
job=2 error=open
job=3 bytes=26 lines=2 words=5
summary files=3 ok=2 failed=1
```

退出状态：1



第二项报告 error=open，第三项仍成功且打印在第三位。退出码为 1，标准错误说明任务 2、路径和系统错误；系统文字因平台而异。这里仅显示精确标准输出。

### 拒绝非法线程数

```sh
./thread_pipeline 0 fixtures/morning.txt
```

```text

```

退出状态：2

没有标准输出。请查看退出状态以及标准错误中的诊断信息。

不打印报告。退出码为 2，标准错误打印用法及上限。验证在线程创建前发生。标准输出有意为空。

## 调试

### 零文件运行一直不退出。

关闭时未广播，或等待条件漏掉 closed，导致消费者继续等待。

带超时运行 ./thread_pipeline 16。一起阅读 queue_pop 和 queue_close，检查 closed 是否在锁内修改，所有等待消费者是否被通知。

条件必须为 count 为零且队列未关闭；关闭时广播，之后 join。不要用 sleep 修补卡住。

### 每次运行的输出行顺序变化。

工作线程完成时直接打印，或主线程在全部 join 前读取。

在 main.c 搜索 printf，确认逐任务打印只在 join_workers 之后执行。用 1 和 16 个线程重复运行 37 个任务。

工作线程只写自己的编号槽。主线程等待所有线程，再按参数顺序遍历结果数组。

### 晚间文件只报告一行，或空行文件报告三行。

EOF 补计遗漏，或末尾已经是 LF 时仍错误补计。

检查样例字节并数 LF。晚间文件有一个 LF 和非空尾段；blank.txt 有两个 LF，没有尾段。

仅在 bytes != 0 且 last != LF 时加一。不能因为读了一个缓冲区就推断多了一行。

### 长单词在第 4096 字节附近被算成两个。

in_word 每读一个块都重新初始化，而不是每个文件初始化一次。

使用生成的 boundary.bin，追踪第一次读取最后一个字节与下次第一个字节，它们都不是分隔符。

把 in_word 放在读取循环外。只有分隔符把它变成 false。

### 线程创建失败后进程卡住。

主线程关闭队列前就 join 等待中的线程，或 join 了未成功创建的无效句柄。

运行 test.py 的注入失败案例，追踪 started，确认此时尚未发布编号。

先关闭空队列，只 join 成功的句柄前缀，销毁后返回 1。不要继续进入生产循环。

### 缺失文件被显示为成功且计数全零。

报告忽略 ScanStatus，把初始化计数当作完成结果。

比较 empty.txt 与不存在的路径。计数起初都可能为零，但状态必须不同。

只有 SCAN_OK 才打印数值计数。在失败编号处保留错误行，进程返回非零退出码。

## 测试计划

### 十六线程、零文件参数

只有 files=0 ok=0 failed=0 的汇总行；在子进程超时前退出 0。

检验关闭广播，以及空与关闭的区别。

### 容量为四时分别处理一、二、五个任务

每个输入恰好一个结果，按输入顺序排列，所有附带文件都成功。

覆盖任务少于及多于队列槽的情况，不假设谁先运行。

### 空文件、空行、纯空白和末尾未换行样例

检查固定精确计数，包括空文件 0/0/0 和晚间文件 26/2/5。

把约定的逻辑行和单词定义与终端外观分开。

### 跨越 4096 字节缓冲区且含零字节和非 ASCII 字节的单词

独立字节正则算法与 C 计数一致，单词不会在块边界被拆开。

检查流状态保留，并避免误用 C 字符串假设。

### 非法线程数语法与任务数边界

0、17、正负号、空格、尾随文字、缺失参数、巨数和 129 项任务退出 2；128 项任务与 0002 线程合法。

验证线程启动前的参数检查及有界数字累积。

### 成功、缺失、成功的文件序列

第二行为 error=open，第三行仍有有效计数，汇总 failed=1，进程退出 1。

单文件失败不能取消其他任务，也不能隐藏其位置。

### 目录与没有写入者的 FIFO

两者均报告 error=not-regular，不能卡住；文件只创建在测试临时目录。

检查类型验证，以及拒绝 FIFO 前的非阻塞打开。

### 恰好 8 MiB，再多一个字节

恰好上限时成功，超过时报告 too-large，不打印部分数值计数。

检查包含上限的边界与减法保护。

### 37 个合成任务重复运行 48 次

1、2、4、16 个线程都与独立算法及单线程标准输出逐字节一致。

覆盖不同调度与队列复用；这是有界证据，不是所有调度的证明，也不是速度测试。

### 队列探针：填满四槽后关闭

新入队失败，已有编号按先进先出取完，最后出队返回 false，重复关闭仍安全。

直接区分关闭后排空和关闭时丢弃。

### 注入创建失败与读取失败

尚无线程或已创建两个时失败都正常退出 1；读取 EIO 报告 error=read；一次 EINTR 后成功重试。

通过临时编译替身测试少见失败路径，不耗尽系统资源。

## 工程取舍

### 为什么结果不需要互斥锁

主线程在线程创建前初始化共享上下文，队列变化由一把锁同步。每个任务编号只产生和取出一次，因此对应槽只有一个写入者。数组不同元素是不同对象。工作阶段主线程不读任何结果，报告前成功 join 与线程完成同步。这是所有权与阶段的论证，不是对时机的猜测。若工作线程更新共享总数，或主线程轮询未写完结果，此论证就不再成立。

### 队列容量约束排队任务，不代表整个进程内存

四槽队列限制等待编号并形成背压，最多 16 个文件同时扫描，最多保留 128 个结果槽用于按序输出。每个扫描器复用一个 4096 字节缓冲区，内存不随文件长度增长。系统线程栈也占内存，不包括在 4096 字节数字里。B 个字节、J 个任务的计数工作量为 O(B + J)，另有调度与等待。拒绝超大文件时，可能多读一个缓冲区才知道已超限。

### 恢复能力有明确限制

队列初始化会撤销已初始化部件，线程部分创建失败有关闭、join、销毁的正常回收路径。单文件打开、元数据、类型、读取、大小和关闭错误都会显示，其他任务继续。意外的运行时同步错误则在诊断后立即结束进程，不承诺完整报告或优雅清理。未实现线程取消、信号退出和文件读取时限。慢普通文件系统或反复 EINTR 仍可能拖延程序。

### 稳定字节语义，不是自然语言解析器

逻辑行包括末尾非空尾段，所以行数不等于只数 LF。单词仅由六种 ASCII 空白字节分隔，多字节字符和零字节只是普通非分隔字节。不声称实现 Unicode 分词或地区敏感分类。要重复得到相同结果，输入文件必须保持不变。所附合成普通文件是学习输入；接受用户路径不代表它是安全文件系统沙箱。

### 正确性证据不能证明提速

固定线程池避免每个文件都创建新线程，但启动、锁、存储带宽和文件缓存仍有成本。这些小运行有意不打印耗时。输出重复一致和可选 ThreadSanitizer 仅检查观察到的行为，不覆盖所有可能调度。测试使用独立字节/正则算法、有界自有样例、临时构建及子进程超时。真正的性能扩展必须比较相同工作量，并报告重复测量。

## 完整源文件

### stats.h

结果约定和文件大小上限

[下载文件](../project-code/comp2017-thread-pipeline/stats.h)

```c
/* Leon | Original teaching project. */
#ifndef STATS_H
#define STATS_H

#include <stddef.h>

#define FILE_BYTE_LIMIT (8u * 1024u * 1024u)

typedef enum {
    SCAN_OK,
    SCAN_OPEN,
    SCAN_METADATA,
    SCAN_NOT_REGULAR,
    SCAN_READ,
    SCAN_TOO_LARGE,
    SCAN_CLOSE
} ScanStatus;

typedef struct {
    size_t bytes;
    size_t lines;
    size_t words;
    ScanStatus status;
    int system_error;
} FileStats;

/* The caller exclusively owns *result until this call returns.
   Failure counters are partial and must not be reported as valid counts. */
void scan_file(const char *path, FileStats *result);
const char *scan_status_name(ScanStatus status);

#endif
```

1. 先读 8 MiB 的 FILE_BYTE_LIMIT，再区分三个 size_t 计数器与 ScanStatus。

2. 只有真实系统调用错误才保存 errno；逻辑拒绝无需伪造系统错误。

3. scan_file 约定调用者提供一个独占输出对象，失败时计数不完整，不能展示为完整答案。

### stats.c

单个工作线程的独立普通文件扫描器

[下载文件](../project-code/comp2017-thread-pipeline/stats.c)

```c
/* Leon | Original teaching project. */
#include "stats.h"

#include <errno.h>
#include <fcntl.h>
#include <stdbool.h>
#include <sys/stat.h>
#include <unistd.h>

/* Fixed ASCII separators make results independent of process locale. */
static bool separator(unsigned char byte) {
    return byte == ' ' || byte == '\t' || byte == '\n' || byte == '\r' ||
           byte == '\v' || byte == '\f';
}

static void count_stream(int descriptor, FileStats *result) {
    unsigned char buffer[4096];
    bool in_word = false;
    unsigned char last = '\n';
    for (;;) {
        ssize_t received = read(descriptor, buffer, sizeof buffer);
        if (received < 0) {
            if (errno == EINTR) {
                continue;
            }
            result->status = SCAN_READ;
            result->system_error = errno;
            return;
        }
        if (received == 0) {
            break;
        }
        size_t length = (size_t)received;
        if (length > FILE_BYTE_LIMIT - result->bytes) {
            result->status = SCAN_TOO_LARGE;
            return;
        }
        result->bytes += length;
        for (size_t i = 0; i < length; i++) {
            unsigned char byte = buffer[i];
            if (byte == '\n') {
                result->lines++;
            }
            bool space = separator(byte);
            if (!space && !in_word) {
                result->words++;
            }
            in_word = !space;
            last = byte;
        }
    }
    if (result->bytes != 0 && last != '\n') {
        result->lines++;
    }
}

void scan_file(const char *path, FileStats *result) {
    *result = (FileStats){0};
    /* Nonblocking open avoids waiting forever for a FIFO writer. Only a
       regular file is accepted after opening; each worker owns its fd. */
    int descriptor = open(path, O_RDONLY | O_NONBLOCK);
    if (descriptor < 0) {
        result->status = SCAN_OPEN;
        result->system_error = errno;
        return;
    }
    struct stat info;
    if (fstat(descriptor, &info) != 0) {
        result->status = SCAN_METADATA;
        result->system_error = errno;
    } else if (!S_ISREG(info.st_mode)) {
        result->status = SCAN_NOT_REGULAR;
    } else {
        count_stream(descriptor, result);
    }
    /* Preserve the first error; do not retry close after an uncertain result. */
    if (close(descriptor) != 0 && result->status == SCAN_OK) {
        result->status = SCAN_CLOSE;
        result->system_error = errno;
    }
}

const char *scan_status_name(ScanStatus status) {
    switch (status) {
        case SCAN_OK: return "ok";
        case SCAN_OPEN: return "open";
        case SCAN_METADATA: return "metadata";
        case SCAN_NOT_REGULAR: return "not-regular";
        case SCAN_READ: return "read";
        case SCAN_TOO_LARGE: return "too-large";
        case SCAN_CLOSE: return "close";
    }
    return "unknown";
}
```

1. separator 精确列出六种空白字节，count_stream 跨每次读取保留单词状态。

2. 把带符号返回值转换前先判断读取错误。EINTR 重试，EOF 后处理末行补计。

3. scan_file 打开、用 fstat 检查、只扫描普通文件，并在所有打开后路径尝试关闭。保留第一个失败。

### queue.h

共享状态和所有权边界

[下载文件](../project-code/comp2017-thread-pipeline/queue.h)

```c
/* Leon | Original teaching project. */
#ifndef QUEUE_H
#define QUEUE_H

#include <pthread.h>
#include <stdbool.h>
#include <stddef.h>

#define QUEUE_CAPACITY 4u

/* Queue entries are job indices, not owning pointers. Protect all fields
   after initialization with mutex. Destroy only after every worker joins. */
typedef struct {
    size_t entries[QUEUE_CAPACITY];
    size_t head;
    size_t count;
    bool closed;
    pthread_mutex_t mutex;
    pthread_cond_t not_empty;
    pthread_cond_t not_full;
} WorkQueue;

/* Runtime synchronization failures terminate the process; see README. */
void thread_check(int error, const char *operation);
int queue_init(WorkQueue *queue);
bool queue_push(WorkQueue *queue, size_t job);
bool queue_pop(WorkQueue *queue, size_t *job);
void queue_close(WorkQueue *queue);
void queue_destroy(WorkQueue *queue);

#endif
```

1. entries 保存四个 size_t 编号，不保存文件描述符或堆对象。

2. head、count 和 closed 描述队列状态，由同一互斥锁一起保护。

3. 两个条件变量对应不同等待条件，接口把关闭与销毁区分开来。

### queue.c

锁保护的环形变化与关闭后排空

[下载文件](../project-code/comp2017-thread-pipeline/queue.c)

```c
/* Leon | Original teaching project. */
#include "queue.h"

#include <stdio.h>
#include <stdlib.h>

void thread_check(int error, const char *operation) {
    if (error != 0) {
        fprintf(stderr, "fatal: %s failed (pthread error %d)\n", operation, error);
        /* Continuing could access unprotected data or strand a waiter.
           This teaching policy exits the process, without orderly cleanup. */
        exit(EXIT_FAILURE);
    }
}

int queue_init(WorkQueue *queue) {
    queue->head = 0;
    queue->count = 0;
    queue->closed = false;
    int error = pthread_mutex_init(&queue->mutex, NULL);
    if (error != 0) {
        return error;
    }
    error = pthread_cond_init(&queue->not_empty, NULL);
    if (error != 0) {
        thread_check(pthread_mutex_destroy(&queue->mutex), "mutex destroy");
        return error;
    }
    error = pthread_cond_init(&queue->not_full, NULL);
    if (error != 0) {
        thread_check(pthread_cond_destroy(&queue->not_empty), "condition destroy");
        thread_check(pthread_mutex_destroy(&queue->mutex), "mutex destroy");
    }
    return error;
}

bool queue_push(WorkQueue *queue, size_t job) {
    thread_check(pthread_mutex_lock(&queue->mutex), "mutex lock");
    while (queue->count == QUEUE_CAPACITY && !queue->closed) {
        thread_check(pthread_cond_wait(&queue->not_full, &queue->mutex),
                     "wait not_full");
    }
    if (queue->closed) {
        thread_check(pthread_mutex_unlock(&queue->mutex), "mutex unlock");
        return false;
    }
    size_t tail = (queue->head + queue->count) % QUEUE_CAPACITY;
    queue->entries[tail] = job;
    queue->count++;
    thread_check(pthread_cond_signal(&queue->not_empty), "signal not_empty");
    thread_check(pthread_mutex_unlock(&queue->mutex), "mutex unlock");
    return true;
}

bool queue_pop(WorkQueue *queue, size_t *job) {
    thread_check(pthread_mutex_lock(&queue->mutex), "mutex lock");
    while (queue->count == 0 && !queue->closed) {
        thread_check(pthread_cond_wait(&queue->not_empty, &queue->mutex),
                     "wait not_empty");
    }
    if (queue->count == 0) {
        thread_check(pthread_mutex_unlock(&queue->mutex), "mutex unlock");
        return false;
    }
    *job = queue->entries[queue->head];
    queue->head = (queue->head + 1) % QUEUE_CAPACITY;
    queue->count--;
    thread_check(pthread_cond_signal(&queue->not_full), "signal not_full");
    thread_check(pthread_mutex_unlock(&queue->mutex), "mutex unlock");
    return true;
}

void queue_close(WorkQueue *queue) {
    thread_check(pthread_mutex_lock(&queue->mutex), "mutex lock");
    queue->closed = true;
    /* All empty-queue consumers must learn that no future job can arrive. */
    thread_check(pthread_cond_broadcast(&queue->not_empty), "broadcast not_empty");
    thread_check(pthread_cond_broadcast(&queue->not_full), "broadcast not_full");
    thread_check(pthread_mutex_unlock(&queue->mutex), "mutex unlock");
}

void queue_destroy(WorkQueue *queue) {
    thread_check(pthread_cond_destroy(&queue->not_full), "condition destroy");
    thread_check(pthread_cond_destroy(&queue->not_empty), "condition destroy");
    thread_check(pthread_mutex_destroy(&queue->mutex), "mutex destroy");
}
```

1. queue_init 按序初始化部件；后续初始化失败时撤销先前部件。

2. 对照入队与出队：都是加锁、while 等待、修改受保护状态、通知另一方、解锁。

3. queue_close 广播但不丢弃元素。所有使用者结束后才可 queue_destroy；运行中的同步错误快速结束进程。

### main.c

命令行、生命周期、工作循环与按序输出

[下载文件](../project-code/comp2017-thread-pipeline/main.c)

```c
/* Leon | Original teaching project. */
#include "queue.h"
#include "stats.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_WORKERS 16u
#define MAX_JOBS 128u

typedef struct {
    WorkQueue *queue;
    char **paths;
    FileStats *results;
} WorkerContext;

static bool parse_workers(const char *text, size_t *workers) {
    size_t value = 0;
    if (*text == '\0') {
        return false;
    }
    for (const unsigned char *p = (const unsigned char *)text; *p != '\0'; p++) {
        if (*p < '0' || *p > '9') {
            return false;
        }
        value = value * 10 + (size_t)(*p - '0');
        if (value > MAX_WORKERS) {
            return false;
        }
    }
    if (value == 0) {
        return false;
    }
    *workers = value;
    return true;
}

static void *consume(void *argument) {
    WorkerContext *context = argument;
    size_t job;
    while (queue_pop(context->queue, &job)) {
        /* Exactly one pop receives each index. No other worker writes this
           result, and main waits for all joins before reading any result. */
        scan_file(context->paths[job], &context->results[job]);
    }
    return NULL;
}

static void join_workers(pthread_t *threads, size_t count) {
    for (size_t i = 0; i < count; i++) {
        thread_check(pthread_join(threads[i], NULL), "thread join");
    }
}

static int print_results(char **paths, FileStats *results, size_t count) {
    size_t failures = 0;
    for (size_t i = 0; i < count; i++) {
        FileStats *result = &results[i];
        if (result->status == SCAN_OK) {
            printf("job=%zu bytes=%zu lines=%zu words=%zu\n",
                   i + 1, result->bytes, result->lines, result->words);
        } else {
            const char *kind = scan_status_name(result->status);
            printf("job=%zu error=%s\n", i + 1, kind);
            fprintf(stderr, "job %zu (%s): %s", i + 1, paths[i], kind);
            if (result->system_error != 0) {
                fprintf(stderr, ": %s", strerror(result->system_error));
            }
            fputc('\n', stderr);
            failures++;
        }
    }
    printf("summary files=%zu ok=%zu failed=%zu\n",
           count, count - failures, failures);
    if (fflush(stdout) != 0 || ferror(stdout)) {
        fputs("output failed\n", stderr);
        return EXIT_FAILURE;
    }
    return failures == 0 ? EXIT_SUCCESS : EXIT_FAILURE;
}

int main(int argc, char **argv) {
    size_t workers;
    if (argc < 2 || !parse_workers(argv[1], &workers) ||
        (size_t)(argc - 2) > MAX_JOBS) {
        fputs("usage: thread_pipeline WORKERS [FILE ...]\n"
              "WORKERS: 1..16; FILE: 0..128 regular files, each <= 8388608 bytes\n",
              stderr);
        return 2;
    }
    size_t jobs = (size_t)(argc - 2);
    WorkQueue queue;
    int error = queue_init(&queue);
    if (error != 0) {
        fprintf(stderr, "queue initialization failed (pthread error %d)\n", error);
        return EXIT_FAILURE;
    }
    FileStats results[MAX_JOBS] = {{0}};
    pthread_t threads[MAX_WORKERS];
    WorkerContext context = {&queue, argv + 2, results};
    size_t started = 0;
    for (; started < workers; started++) {
        error = pthread_create(&threads[started], NULL, consume, &context);
        if (error != 0) {
            fprintf(stderr, "thread creation failed after %zu workers "
                            "(pthread error %d)\n", started, error);
            /* No jobs are published until the whole pool exists. */
            queue_close(&queue);
            join_workers(threads, started);
            queue_destroy(&queue);
            return EXIT_FAILURE;
        }
    }
    for (size_t job = 0; job < jobs; job++) {
        if (!queue_push(&queue, job)) {
            fputs("internal error: queue closed during production\n", stderr);
            queue_close(&queue);
            join_workers(threads, started);
            queue_destroy(&queue);
            return EXIT_FAILURE;
        }
    }
    queue_close(&queue);
    join_workers(threads, started);
    queue_destroy(&queue);
    return print_results(argv + 2, results, jobs);
}
```

1. parse_workers 只接受十进制数字，一超过 16 就拒绝。有界中间值避免算术溢出。

2. 主线程初始化一个上下文，创建所有工作线程后才发布编号。失败时只有 started 前缀是有效 join 列表。

3. consume 写入取出编号对应的槽。主线程依次关闭、join、销毁，再由 print_results 按输入顺序报告；任一文件失败就返回失败。

### Makefile

严格构建、隔离测试与本地清理

[下载文件](../project-code/comp2017-thread-pipeline/Makefile)

```make
# Leon | Original teaching project.
CC = clang
CPPFLAGS = -D_POSIX_C_SOURCE=200809L
CFLAGS = -std=c11 -Wall -Wextra -Werror -pedantic -O2 -pthread
LDFLAGS = -pthread

.PHONY: all test clean
all: thread_pipeline

thread_pipeline: main.o queue.o stats.o
	$(CC) $(LDFLAGS) -o $@ main.o queue.o stats.o

main.o: main.c queue.h stats.h
queue.o: queue.c queue.h
stats.o: stats.c stats.h

test:
	python3 test.py

clean:
	rm -f thread_pipeline main.o queue.o stats.o
```

1. 默认 clang，启用 C11、POSIX 功能、pthread，并把警告当作错误。

2. 头文件依赖让相关编译单元重新构建，编译与链接阶段都使用 -pthread。

3. make test 调用 python3 test.py，在临时副本构建。make clean 只删除本项目常规本地构建产物。

### test.py

独立预期算法、边界测试、压力测试与可控故障

[下载文件](../project-code/comp2017-thread-pipeline/test.py)

```python
#!/usr/bin/env python3
# Leon | Original teaching project.
"""Build only in a temporary copy; use independent byte oracles and timeouts."""
import argparse
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

SOURCE = Path(__file__).resolve().parent
FLAGS = ["-D_POSIX_C_SOURCE=200809L", "-std=c11", "-Wall", "-Wextra",
         "-Werror", "-pedantic", "-O2", "-pthread"]
LIMIT = 8 * 1024 * 1024


def command(args, cwd, timeout=20):
    return subprocess.run(args, cwd=cwd, text=True, capture_output=True,
                          timeout=timeout, check=False)


def successful(args, cwd, timeout=30):
    result = command(args, cwd, timeout)
    assert result.returncode == 0, (args, result.stdout, result.stderr)
    return result


def expected_line(index, data):
    # A regular expression oracle, independent of the C in_word state machine.
    lines = data.count(b"\n") + int(bool(data) and not data.endswith(b"\n"))
    words = len(re.findall(rb"[^ \t\r\n\v\f]+", data))
    return f"job={index} bytes={len(data)} lines={lines} words={words}\n"


def expect_files(root, files, workers, binary="thread_pipeline"):
    result = successful([f"./{binary}", str(workers), *files], root)
    expected = "".join(expected_line(i, (root / path).read_bytes())
                       for i, path in enumerate(files, 1))
    expected += f"summary files={len(files)} ok={len(files)} failed=0\n"
    assert result.stdout == expected, (result.stdout, expected)
    assert result.stderr == "", result.stderr
    return result.stdout


def variant(root, name, source, define, shim, flags):
    # Only a temporary translation unit is instrumented; shipped C is unchanged.
    (root / f"{name}_shim.c").write_text(shim, encoding="utf-8")
    successful(["clang", *flags, f"-D{define}", "-c", source,
                "-o", f"{name}.o"], root)
    successful(["clang", *flags, "-c", f"{name}_shim.c", "-o",
                f"{name}_shim.o"], root)
    objects = [f"{name}.o" if item == source else item.replace(".c", ".o")
               for item in ("main.c", "queue.c", "stats.c")]
    successful(["clang", *flags, *objects, f"{name}_shim.o", "-o", name], root)


def run_tests(root, flags):
    successful(["make", "all", "CFLAGS=" + " ".join(flags),
                "LDFLAGS=" + " ".join(flags)], root)
    supplied = [f"fixtures/{name}.txt" for name in
                ("morning", "evening", "blank", "empty", "spaces")]
    expect_files(root, [], 16)
    expect_files(root, supplied[:1], 1)
    expect_files(root, supplied[:2], 16)
    expect_files(root, supplied, 4)
    print("PASS empty queue, empty file, and fewer/more jobs than capacity")

    # Hard-coded expected counts catch an error shared by both implementations.
    exact = successful(["./thread_pipeline", "3", *supplied], root)
    assert exact.stdout == (
        "job=1 bytes=37 lines=2 words=6\n"
        "job=2 bytes=26 lines=2 words=5\n"
        "job=3 bytes=2 lines=2 words=0\n"
        "job=4 bytes=0 lines=0 words=0\n"
        "job=5 bytes=6 lines=2 words=0\n"
        "summary files=5 ok=5 failed=0\n")
    print("PASS exact fixture counts including final unterminated line")

    binary_bytes = b"x" * 4095 + b"YZ\x00\xff \r\n\tfinal"
    (root / "boundary.bin").write_bytes(binary_bytes)
    expect_files(root, ["boundary.bin"], 2)
    print("PASS word crossing read-buffer boundary and non-ASCII bytes")

    for args in ([], ["0"], ["17"], ["-1"], ["+2"], ["2x"], [""],
                 [" 2"], ["99999999999999999999999999"],
                 ["1", *([supplied[0]] * 129)]):
        result = command(["./thread_pipeline", *args], root)
        assert result.returncode == 2 and result.stdout == "", result
        assert result.stderr.startswith("usage: thread_pipeline WORKERS"), result
    expect_files(root, supplied[:1], "0002")
    expect_files(root, [supplied[0]] * 128, 16)
    print("PASS malformed CLI, accepted leading zeros, and 128-job boundary")

    result = command(["./thread_pipeline", "4", supplied[0], "missing.txt",
                      supplied[1]], root)
    assert result.returncode == 1, result
    assert result.stdout == (expected_line(1, (root / supplied[0]).read_bytes()) +
                             "job=2 error=open\n" +
                             expected_line(3, (root / supplied[1]).read_bytes()) +
                             "summary files=3 ok=2 failed=1\n"), result.stdout
    assert "job 2 (missing.txt): open:" in result.stderr, result.stderr
    print("PASS missing file preserves other results and returns failure")

    os.mkfifo(root / "pipe")
    result = command(["./thread_pipeline", "2", "fixtures", "pipe"], root)
    assert result.returncode == 1, result
    assert result.stdout == ("job=1 error=not-regular\n"
                             "job=2 error=not-regular\n"
                             "summary files=2 ok=0 failed=2\n"), result.stdout
    print("PASS directory and FIFO rejected without waiting for a writer")

    (root / "limit.txt").write_bytes(b"z" * LIMIT)
    expect_files(root, ["limit.txt"], 1)
    with (root / "limit.txt").open("ab") as handle:
        handle.write(b"z")
    result = command(["./thread_pipeline", "1", "limit.txt"], root)
    assert result.returncode == 1, result
    assert result.stdout == ("job=1 error=too-large\n"
                             "summary files=1 ok=0 failed=1\n"), result.stdout
    print("PASS exact byte limit and oversized input without partial statistics")

    stress = []
    for i in range(37):
        path = f"stress-{i:02}.txt"
        data = (b"alpha\tbeta\n\n" * (i * 71)) + (b"tail" if i % 2 else b"")
        (root / path).write_bytes(data)
        stress.append(path)
    reference = expect_files(root, stress, 1)
    for repeat in range(12):
        for workers in (1, 2, 4, 16):
            output = expect_files(root, stress, workers)
            assert output == reference, (repeat, workers)
    print("PASS 48 repeated schedules: 37 jobs, workers 1/2/4/16, stable output")

    probe = r'''/* Leon | Original teaching project. */
#include "queue.h"
#include <assert.h>
int main(void) {
    WorkQueue queue;
    assert(queue_init(&queue) == 0);
    for (size_t i = 0; i < QUEUE_CAPACITY; i++) {
        assert(queue_push(&queue, i + 10));
    }
    queue_close(&queue);
    assert(!queue_push(&queue, 99));
    for (size_t i = 0; i < QUEUE_CAPACITY; i++) {
        size_t job;
        assert(queue_pop(&queue, &job));
        assert(job == i + 10);
    }
    size_t job;
    assert(!queue_pop(&queue, &job));
    queue_close(&queue);
    queue_destroy(&queue);
    return 0;
}
'''
    (root / "queue_probe.c").write_text(probe, encoding="utf-8")
    successful(["clang", *flags, "queue_probe.c", "queue.o", "-o", "queue_probe"], root)
    successful(["./queue_probe"], root)
    print("PASS queue close drains FIFO entries and rejects new work")

    for after in (0, 2):
        shim = r'''/* Leon | Original teaching project. */
#include <errno.h>
#include <pthread.h>
static unsigned int calls;
int fixture_create(pthread_t *thread, const pthread_attr_t *attributes,
                   void *(*start)(void *), void *argument) {
    if (calls++ == FAIL_AFTER) {
        return EAGAIN;
    }
    return pthread_create(thread, attributes, start, argument);
}
'''.replace("FAIL_AFTER", str(after))
        name = f"create_failure_{after}"
        variant(root, name, "main.c", "pthread_create=fixture_create", shim, flags)
        result = command([f"./{name}", "4", *supplied], root)
        assert result.returncode == 1 and result.stdout == "", result
        assert f"thread creation failed after {after} workers" in result.stderr, result
    print("PASS injected creation failure before first/after two workers; no hang")

    for mode in ("error", "interrupt"):
        body = "errno = EIO; return -1;" if mode == "error" else (
            "static int first = 1; if (first) { first = 0; errno = EINTR; return -1; }"
            " return read(descriptor, buffer, count);")
        shim = r'''/* Leon | Original teaching project. */
#include <errno.h>
#include <stddef.h>
#include <unistd.h>
ssize_t fixture_read(int descriptor, void *buffer, size_t count) {
    (void)descriptor; (void)buffer; (void)count;
    BODY
}
'''.replace("BODY", body)
        name = f"read_{mode}"
        variant(root, name, "stats.c", "read=fixture_read", shim, flags)
        if mode == "error":
            result = command([f"./{name}", "1", supplied[0]], root)
            assert result.returncode == 1, result
            assert result.stdout == ("job=1 error=read\n"
                                     "summary files=1 ok=0 failed=1\n"), result.stdout
            assert "read:" in result.stderr, result.stderr
        else:
            expect_files(root, supplied[:1], 1, name)
    print("PASS injected read error and interrupted-read retry")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tsan", action="store_true",
                        help="require a working clang ThreadSanitizer runtime")
    args = parser.parse_args()
    flags = FLAGS + (["-O1", "-g", "-fsanitize=thread"] if args.tsan else [])
    with tempfile.TemporaryDirectory(prefix="guoliang-thread-test-") as directory:
        root = Path(directory) / "project"
        shutil.copytree(SOURCE, root, ignore=shutil.ignore_patterns(
            "*.o", "thread_pipeline", "__pycache__"))
        run_tests(root, flags)
    print("All pipeline tests passed" + (" (ThreadSanitizer)." if args.tsan else "."))


if __name__ == "__main__":
    main()
```

1. TemporaryDirectory 与 copytree 隔离构建及生成样例。subprocess 使用参数列表和明确超时。

2. 字节正则表达式独立于 C 状态机计算单词，手工固定的样例结果也检查预期算法。

3. 阅读 48 次循环、关闭排空队列探针和临时 pthread_create/read 替身。--tsan 要求检测器可用，不会静默跳过失败。

### fixtures/morning.txt

末尾有 LF 的合成笔记

[下载文件](../project-code/comp2017-thread-pipeline/fixtures/morning.txt)

```text
Robotics club
Build small test often
```

1. 第一行是 Robotics club。

2. 第二行是 Build small test often，末尾为 LF。

3. 预期 37 字节、2 个逻辑行、6 个单词；末尾 LF 不增加空行。

### fixtures/evening.txt

末尾没有 LF 的合成笔记

[下载文件](../project-code/comp2017-thread-pipeline/fixtures/evening.txt)

```text
Check	all wheels
Then rest
```

1. Check 和 all 之间是制表符。

2. 第二行 Then rest 直接结束，没有 LF。

3. 预期 26 字节、2 个逻辑行、5 个单词；EOF 补计第二行。

### fixtures/blank.txt

两个换行字节且无单词

[下载文件](../project-code/comp2017-thread-pipeline/fixtures/blank.txt)

不可见字节视图（十六进制）：0a 0a

1. 文件恰好是 LF 后跟 LF。

2. 每个 LF 结束一行，即使行内没有字母。

3. 预期 2 字节、2 行、0 个单词；EOF 后不要再加第三行。

### fixtures/empty.txt

零字节样例

[下载文件](../project-code/comp2017-thread-pipeline/fixtures/empty.txt)

不可见字节视图（十六进制）：空文件；零字节

1. 此文件有意没有内容，也没有作者注释，因为任何字节都会破坏空文件测试。

2. 扫描器第一次读取就到 EOF，不进入逐字节循环。

3. 预期 0 字节、0 行、0 个单词，但文件本身仍是成功任务。

### fixtures/spaces.txt

按固定顺序放置六种分隔字节

[下载文件](../project-code/comp2017-thread-pipeline/fixtures/spaces.txt)

不可见字节视图（十六进制）：20 09 0d 0a 0b 0c

1. 依次为空格、制表、CR、LF、垂直制表和换页。

2. LF 后有非空字节尾段，终端可能看不见。

3. 预期 6 字节、2 个逻辑行、0 个单词；它检验精确分隔定义，不检验地区设置。

### README.md

完整英文命令行指南

[下载文件](../project-code/comp2017-thread-pipeline/README.md)

1. 先读故事和精确构建运行命令，再用样例核对计数定义。

2. 按五个阅读阶段和阶段图学习，把每种资源与拥有者及生命周期结束点联系起来。

3. 修改设计前，阅读失败策略、复杂度、测试命令和有界扩展。

### README.zh.md

内容对应的中文命令行指南

[下载文件](../project-code/comp2017-thread-pipeline/README.zh.md)

1. 命令和预期标准输出与英文指南相同，程序输出仍使用英文。

2. 阅读条件、所有权、队列关闭和 join 可见性的中文解释。

3. 更改上限、计数语义或错误行为时，两种语言指南应同步更新。

## 扩展方向

### 把队列容量变成有界实验参数

增加 1 到 8 的合法容量参数，仍用固定上限存储和相同锁/条件规则。比较容量与线程数：它们分别控制等待任务和活跃消费者。

容量 1、4、8 在零任务、37 项任务和缺失文件情况下输出必须一致。非法容量在线程启动前失败，并解释修改后的不变量。

### 测量吞吐量，同时保持报告语义

生成有界的大一些的本地样例，在结果格式之外测量耗时，用相同字节比较 1、2、4、16 线程。记录编译设置、重复次数、文件大小和缓存条件。吞吐量等于成功处理总字节除以秒数。

计数保持逐字节一致。报告重复测量及其变化，只有证据支持才声称提速。样例保持有界，并在临时测试目录生成。

## 一手参考资料

- [The Open Group POSIX.1-2024 — condition waits, including pthread_cond_wait](https://pubs.opengroup.org/onlinepubs/9799919799/functions/pthread_cond_clockwait.html)

- [The Open Group POSIX.1-2024 — pthread_join](https://pubs.opengroup.org/onlinepubs/9799919799.2024edition/functions/pthread_join.html)

- [The Open Group POSIX.1-2024 — General Concepts, Memory Synchronization 4.15.2](https://pubs.opengroup.org/onlinepubs/9799919799/basedefs/V1_chap04.html)

- [The Open Group Base Specifications Issue 6 — pthread_create](https://pubs.opengroup.org/onlinepubs/000095399/functions/pthread_create.html)

- [The Open Group POSIX.1-2024 — read](https://pubs.opengroup.org/onlinepubs/9799919799/functions/read.html)

---
Leon
