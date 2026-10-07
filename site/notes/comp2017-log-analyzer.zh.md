# COMP2017 — 流式日志分析器

> Leon | Original engineering workshop

![Leon learning route](../assets/maps/comp2017-log-analyzer.zh.svg)

[English](comp2017-log-analyzer.en.md) · [中文](comp2017-log-analyzer.zh.md)

把机器人模拟器的轨迹变成可信的命令行报告。用一个小型 C 程序练习有边界地读行、校验记录、累积统计和解释失败。

[下载完整工程 ZIP](../downloads/comp2017-log-analyzer.zip)

## 故事

Leon 正在测试课堂用的机器人模拟器。每个模拟动作都会记录级别与耗时，例如 WARN 40。长日志中的慢动作很容易被漏掉，损坏的记录又可能让平均值失真。我们先让一条有效记录走通，再明确记录规则，加入连续读行和累积统计。完成后的工具能够报告 INFO、WARN、ERROR 的次数、耗时范围与平均值，还能说明丢弃了多少行。所有数据都是人工构造。这是原创工程项目及其概念检查，不是课程提供的作业或答案。

### 开始前先读

- [位、C 类型与明确的控制流程](../courses/comp2017.zh.html#representation-control): 使用比较、循环、无符号值和明确的返回码。单次耗时的范围很小，累积总和需要更宽的类型。

- [字符串、有界输入与解析](../courses/comp2017.zh.html#strings-parsing): C 字符串在 NUL 字节处结束。缓冲区要为结束符留空间，数值字段必须整体合法才接受。

- [结构体、对齐、联合体与类型标签](../courses/comp2017.zh.html#structured-data): 记录结构体把一个级别和一个耗时放在一起；统计结构体保存每行处理后仍需保持一致的状态。

- [文件流、二进制记录与错误](../courses/comp2017.zh.html#file-streams): 通过 FILE 指针读取，区分文件结束和流错误，只关闭自己打开的流。

- [翻译单元、符号与程序库](../courses/comp2017.zh.html#compilation-linkage): 头文件描述接口，独立 C 编译单元实现接口，链接器再把目标文件组合起来。

### 学习成果

- 把自然语言输入规则转成解析器契约：要么提交完整记录，要么保持输出对象不变。

- 用固定大小的应用内存处理输入流，遇到坏数据后仍保住物理行边界。

- 根据已证明的边界选择数值类型，独立计算预期结果，同时测试标准输出、错误输出和退出码。

## 需求与契约

### 恰好接受一个输入参数：文件名，或表示标准输入的 -。

明确而单一的接口便于使用和测试，不需要额外交互菜单。

没有参数或有两个参数时退出码为 2，stdout 为空。复制的示例文件和管道标准输入都能读取。

### 每行包含 INFO、WARN 或 ERROR，再加一个 0 到 60000 的十进制整数。字段之间只允许空格和制表符。

明确语法，避免把 12ms、-1、1.5 或多余字段悄悄转成有效测量值。

测试两个端点、超出上限一单位的值，以及未知级别、正负号、后缀和极长整数。

### 每条物理行在 LF 之前最多 127 字节，末尾 CR 也计入。嵌入 NUL 或超长的整行只算一条坏记录。

固定缓冲区还要给结束符留一字节。读完坏行的剩余部分，防止尾巴冒充下一行。

127 字节行成功，128 字节行失败，紧接其后的有效行仍然只计数一次。

### 最多处理 1,048,576 个输入字节，另允许一个用于探测的字节。输入超限属于致命错误。

这限制了字节处理工作量，也便于证明计数和耗时总和不会溢出。

恰好 1 MiB 的有效填充行成功，再多一个字节则退出码为 1，stdout 为空。

### 部分行损坏时保留有效行统计，但返回 3 并统计全部坏行。发生致命输入错误时不输出报告。

读报告的人能够判断缺失数据的程度，脚本也能识别不完全成功的运行。

混合样本报告 3 行有效、3 行错误；不存在的文件返回 1 且不生成报告。

### 报告计数、有效耗时总和、最小值、最大值和均值。没有有效行时，最后三个指标输出 n/a。

没有观测值不等于观测到零耗时，而且不能除以零。

手算示例总和 200、均值 33.333；检查空样本中的全部 n/a。

## 结构与所有权

**main.c：命令与资源归属**

校验 argc，打开文件或借用 stdin，连接读取器 → 解析器 → 统计，关闭自己打开的文件并选择退出码。整体处理策略集中在这里。

**reader.c：字节变成完整行**

将字节流读入调用者的固定缓冲区。区分完整行、行结构错误、正常 EOF、I/O 失败和输入超限。在总字节预算内读完坏行。

**record.c：文本变成记录值**

读取完整 C 字符串，不修改它。校验级别、分隔符、数字、数值边界和文本末尾。所有检查通过后才提交局部候选记录。

**stats.c：记录值变成报告**

无需保存全部记录，逐步维护行数、计数、总和和极值的约束。最后格式化一次报告并刷新输出，以发现缓冲写入错误。

argv → FILE 流 → 有边界的物理行 → 合法记录 → 累积统计 → stdout。坏行转到错误计数与数量受限的 stderr 警告。致命输入错误在输出报告前停止。应用程序不需要线程，也不需要在堆上保存记录。

- fopen 返回的 FILE * → main 打开文件，把指针借给 analyze 和 read_line。 → 分析结束后 main 调用一次 fclose，即使分析因输入错误而失败也会关闭。

- stdin 和 stdout → C 运行时提供这些流，本项目只是借用。 → 不关闭借来的 stdin。stats_print 刷新 stdout；正常进程结束时由运行时收尾。

- 128 字节行缓冲区及解析记录 → analyze 拥有局部栈存储。read_line 写缓冲区，parse_record 将数值写入记录。 → 当前行处理完成后才重用缓冲区。没有函数保留其指针；离开作用域时局部存储结束。

- 统计结构体 → main 拥有零初始化的结构体，借给其他函数更新和打印。 → 无需 free：它具有自动存储期，内部只保存数值，不包含动态分配的指针。

<a id="milestone-one-row"></a>

## 1. 跟踪一行文本变成报告

先走通最小的完整路径：一条有效记录从 stdin 进入，并生成正确报告。先理解数据形状，再研究错误分支。

从一个能手算的问题开始：INFO 12 应输出什么？它表示一个事件，因此 valid 和 INFO 都为 1；总和、最小值、最大值和均值都对应 12 毫秒。这把输入规则和可观察结果连接起来。先把完整下载文件作为可运行的基线，再一次理解一条路径。结构体把相关值组合起来，传递一条记录时不容易混淆级别与耗时。

1. 在项目目录运行 make，再运行 printf 'INFO 12\n' | ./log_analyzer -。把终端输出与手算预测放在一起比较。短横线是一个参数；管道把 printf 的输出接到程序的 stdin。

2. 阅读 record.h 摘录。enum 为三个类别提供易读名字；LEVEL_COUNT 后续用于确定三个计数器组成的数组大小。unsigned 保存非负耗时，但解析器仍要额外限制到 60000。

3. 只跟踪 main.c 中成功的调用：read_line 填入文本，parse_record 填入局部记录，stats_accept 更新统计，stats_print 输出报告。圈出文本变成有类型数值的位置。不要把摘录复制成独立程序；请一起编译全部源文件。

教学摘录；运行时使用完整工程。

```c
enum log_level { LEVEL_INFO, LEVEL_WARN, LEVEL_ERROR, LEVEL_COUNT };

struct record {
    enum log_level level;
    unsigned duration_ms;
};
```

摘自 record.h。记录保存的是值，不是指向输入行的指针。下一次读行可以覆盖原文本，而不会改变已交给统计代码的记录。这已经是一次资源归属设计，尽管没有出现 malloc。

**如果输入换成 ERROR 12，进程应该报错退出吗？**

不应该。ERROR 是格式中的合法级别。它让 ERROR 计数变为 1；因为输入本身合法，进程仍返回 0。

<a id="milestone-validated-record"></a>

## 2. 让校验要么全部成功，要么不提交

为单行路径增加严格的解析契约：只有整行完全合法，才能形成记录。

如果转换函数从 12ms 中只读取前缀 12，就会掩盖输入错误。我们的解析器先读取完整级别，要求分隔符，再读至少一个数字，最后确保只剩允许的尾部空白。它先构造局部 candidate，最后一次性赋值给 *out。因此失败时调用者不会收到半条新记录。对每个数字 d，新值应为 10v+d。把 10v+d <= 60000 改写为 v <= (60000-d)/10，就能在乘法之前检查。

1. 先读 record.h 中 parse_record 上方的承诺，再读实现。把输入标为借用且 const，把 out 标为调用者拥有的可写存储。函数调用后不保留这两个指针。

2. 逐位跟踪 INFO 60000 的 candidate。最后一个零之前 v 为 6000，检查允许继续。对于 INFO 60001，最后一位让阈值成为 5999，因此在写入超范围值之前就停止。

3. 运行 make test 并找到数字语法测试。先预测 +1、-1、1.5、12ms、1 2 和 60001 会被拒绝，再读断言。让有效行后面跟一条坏行，确认只有有效耗时进入总和。

教学摘录；运行时使用完整工程。

```c
    while (*p >= '0' && *p <= '9') {
        unsigned digit = (unsigned)(*p - '0');
        if (candidate.duration_ms > (MAX_DURATION_MS - digit) / 10U) {
            return false;
        }
        candidate.duration_ms = candidate.duration_ms * 10U + digit;
        ++p;
    }
    if (*skip_space(p) != '\0') {
        return false;
    }
    *out = candidate;
    return true;
```

摘自 record.c，位于级别与首位数字校验之后。边界检查先于乘加运算。最后的 NUL 检查拒绝后缀和额外字段。*out = candidate 是提交点：此前所有失败分支都不修改调用者输出。

**为什么识别 INFO 后不立即写入 out->level？**

因为后续耗时错误会让输出只改变一部分。局部 candidate 让接口更清晰：成功就替换整条记录，失败就什么也不替换。

<a id="milestone-bounded-stream"></a>

## 3. 连续读取时保住行边界

将单行输入扩展成连续记录，不把整份文件保存在内存中，也不把损坏行的尾部误认为另一行。

读取器处理字节和换行，解析器处理完整行的含义。分开这两项任务，更容易定位错误。127 字节的内容需要 128 字节数组，因为 C 字符串还需要 NUL 结束符。一旦发现坏行，如果马上停下，尾部仍留在流中。应继续读到 LF 或 EOF，同时继续检查总字节预算。单看 EOF 不能证明成功，还要用 ferror 区分读取失败。

1. 先读 reader.h 中五种 line_status，再读循环。main 只能解析 LINE_OK。LINE_BAD 使拒绝次数加一；LINE_END 正常结束；LINE_IO_ERROR 与 LINE_LIMIT 终止且不生成报告。

2. 对 127 字节以及第 128 个字节，跟踪摘录中的 used 和 bad。used 永远不超过 127。bad 变为真后停止写入，但继续读取。嵌入 NUL 走同一拒绝路径，避免伪装结束符之后藏着文本。

3. 用行长度与二进制字节测试检查恢复行为。再查看 EOF 分支怎样处理缺少 LF 的最后一行，以及去掉 CR 如何支持 CRLF。1 MiB 测试检查另一个边界：总输入大小，而非单行容量。

教学摘录；运行时使用完整工程。

```c
        if (ch == '\n') {
            break;
        }
        if (ch == '\0' || used == MAX_LINE_BYTES) {
            bad = true;
        }
        if (!bad) {
            line[used++] = (char)ch;
        }
        /* Keep consuming a bad line so its tail is not a new record. */
```

摘自 reader.c 的字节循环。同一循环中用 int 保存 fgetc 返回值，以区分 EOF 与普通字节。缓冲区属于 analyze，read_line 只是借用。LINE_BAD 后不要使用缓冲区内容，因为该路径不承诺提供完整 C 字符串。

**为什么一条长行即使够填满多次缓冲区，也只能算一次拒绝？**

输入契约按物理行计数，不按缓冲区大小的分块计数。读到行尾才能保住边界，让下次调用从真正的下一行开始。

<a id="milestone-running-summary"></a>

## 4. 用明确约束维护累积统计

用固定大小的状态，把多条合法记录变成有用的计数与耗时统计。

计算数量、总和、最小值和最大值，不必记住每个耗时。每条完整行处理后，lines = valid + malformed；每条有效行处理后，INFO + WARN + ERROR = valid。只有有效记录影响耗时指标。用第一条有效耗时初始化两个极值，否则零初始化的最小值在全正数数据中会一直为零。计数与总和的保守边界较大，因此用 uint64_t；单条 0–60000 耗时用 unsigned 即可。

1. 用 {0} 初始化 totals，再读 stats_accept 和 stats_reject。跟踪示例的前两行：INFO 10 与 WARN 40 之后，数量为 2，总和 50，最小值 10，最大值 40。确认坏行的耗时不会进入此函数。

2. 先手算六行结果，再运行示例。总和为 200，200/6 为 33.333… 。在 stats_print 中，先转类型再相除，显示三位小数。均值显示会舍入，但整数累积仍然精确。

3. 运行空样本。valid 为零时，没有观测到最小或最大值，也不能做除法。找到 n/a 分支，再运行耗时全为正数的混合样本；它能发现含零示例单独测试时可能漏掉的最小值初始化错误。

教学摘录；运行时使用完整工程。

```c
void stats_accept(struct stats *s, const struct record *record)
{
    if (s->valid == 0 || record->duration_ms < s->min_ms) {
        s->min_ms = record->duration_ms;
    }
    if (s->valid == 0 || record->duration_ms > s->max_ms) {
        s->max_ms = record->duration_ms;
    }
    ++s->lines;
    ++s->valid;
    ++s->by_level[record->level];
    s->total_ms += record->duration_ms;
}
```

摘自 stats.c。先更新极值，再增加 valid，所以 valid == 0 表示当前是第一条有效记录。record->level 能安全作为索引，是因为调用者必须传入解析成功的记录。头文件写明此前置条件；这是内部接口，不是接受任意数据的 API。

**仅靠目前的状态，可以计算精确中位数吗？**

不能。数量、总和和极值丢失了中位数需要的顺序信息。增加这个功能需要其他表示，例如有限范围的直方图，并重新论证内存与正确性。

<a id="milestone-cli-proof"></a>

## 5. 完成接口并测试失败路径

交付真正的命令行工具，包含清楚的退出规则、资源清理、可复现样本，以及能发现错误结果的测试。

看起来合理的报告还不够。调用者还要知道是否检查了全部输入、是否排除了记录。main 负责决策：完整且无坏行返回 0，完整但有坏行返回 3，用法错误返回 2，输入、容量或输出函数报告的错误返回 1。即使 analyze 失败也关闭自己打开的文件。输入与关闭成功前不写 stdout；输出错误本身仍可能留下部分结果。测试将真实子进程行为与独立预期比较，并把临时输入放在各自的目录中。

1. 从参数校验一直读到 main 的 return。fopen 提供流时标记 owns_input；借用 stdin 时为假。跟踪摘录中成功与失败的清理路径：只有一个 fclose 位置，栈上的 totals 不需要 free。

2. 运行混合样本，立即用 echo $? 检查：虽然 stdout 有用，退出码仍为 3。再运行不存在的文件名和缺少参数的情况：预期分别是 1 和 2，stdout 均为空。stderr 是单独诊断通道，脚本可将报告与警告分开。

3. 运行 make test。说出每个测试能抓到的错误：均值类型错误、只解析前缀、坏行没有读完、退出码丢失，或总字节边界差一。测试使用五秒子进程超时和写死的手算预期。它们不模拟所有输出或关闭故障，也不等于普通命令行运行自带时限。

教学摘录；运行时使用完整工程。

```c
    struct stats totals = {0};
    bool completed = analyze(input, &totals);
    if (owns_input && fclose(input) != 0) {
        fputs("error: cannot close input\n", stderr);
        completed = false;
    }
    if (!completed) {
        return EXIT_IO;
    }
    if (!stats_print(stdout, &totals)) {
        fputs("error: cannot write report\n", stderr);
        return EXIT_IO;
    }
    return totals.malformed == 0 ? EXIT_CLEAN : EXIT_DATA;
```

摘自 main.c 末尾。completed 表明输入处理是否真正完成。检查该结果之前，先对自己拥有的输入调用 fclose。stats_print 用 fflush 检查缓冲输出；它失败也返回 1。完整读取但存在坏行的情况在最后的 return 区分。

**既然 stdout 已与预期一致，为什么还要测试 returncode 和 stderr？**

报告可能对接受的行算得正确，却隐藏了数据损失。退出码 3 和行号警告负责告知调用者有行被拒绝。三个通道一起测试，才能覆盖工具对外的完整契约。

## 构建与运行

使用 macOS 或 Linux 上支持 C11 的 Clang、make 和 Python 3。Windows 可使用 WSL 等 Linux 环境。这里的 Makefile 默认使用 Clang。在下载目录打开终端，解压并进入工程文件夹。make 构建可执行文件；make test 检查程序行为。

```sh
unzip comp2017-log-analyzer.zip
cd comp2017-log-analyzer
make
make test
```

### 完整的机器人轨迹

```sh
./log_analyzer fixtures/demo.log
```

```text
lines=6
valid=6
malformed=0
INFO=3
WARN=2
ERROR=1
total_ms=200
min_ms=0
max_ms=100
mean_ms=33.333
```

退出状态：0



先 make，再在项目目录运行。退出码 0，stderr 为空。六条有效记录总和为 200 毫秒，因此 200/6 显示为 33.333。ERROR=1 是事件计数，不表示进程失败。

### 有坏行，也有诚实的报告

```sh
./log_analyzer fixtures/mixed.log
```

```text
lines=6
valid=3
malformed=3
INFO=1
WARN=1
ERROR=1
total_ms=30
min_ms=5
max_ms=15
mean_ms=10.000
```

退出状态：3



退出码 3。stdout 只统计三条有效记录。stderr 分三行输出 warning: line 2: malformed record、warning: line 4: malformed record 和 warning: line 5: malformed record。DEBUG、-1 和 60001 被拒绝。执行后立刻运行 echo $? 可查看退出码。

### 尚无观测记录

```sh
./log_analyzer fixtures/empty.log
```

```text
lines=0
valid=0
malformed=0
INFO=0
WARN=0
ERROR=0
total_ms=0
min_ms=n/a
max_ms=n/a
mean_ms=n/a
```

退出状态：0



退出码 0，stderr 为空。零字节样本不含任何物理行。有效数量为零时，n/a 明确表示没有观测到最小值、最大值或平均值。

## 调试

### 输入耗时全部为正，最小值却是 0。

把初始化的零误当成了实际观测。

用耗时 5 和 15 的两行复现，检查第一次 stats_accept 更新前的 s->valid。

valid 为零时，先用第一条真实记录设置两个极值，再增加 valid。保留全正数的混合样本测试。

### 耗时 1、2、2 得到均值 1.000。

转换成 double 之前，整数除法已经丢掉了小数。

先写出 5/3 = 1.666…，再检查 stats_print 中除法操作数的类型，而不只是接收结果的变量类型。

在除法之前转换：(double)total_ms / (double)valid。小数均值测试要求输出 1.667。

### 一条长行导致多次拒绝，或弄丢了下一条有效行。

缓冲区满时读取器立即返回，没有消费完同一物理行。

把一条 128 字节行放在 WARN 7 前面。最终报告必须只有两条物理行，其中恰好一条坏行。

标记坏行后继续读取到 LF 或 EOF，同时仍检查整个输入预算。不要解析 LINE_BAD 的缓冲区。

### INFO 12ms 或 INFO 1 2 被接受。

解析器只验证了数字前缀，没有验证剩余文本。

数字循环结束后，查看跳过尾部空白后的字符。它必须是字符串结束符 NUL。

拒绝任何剩余的非空白文本，最后才赋值给 *out。分别测试后缀与额外字段。

### 读取失败看起来像成功生成了一份较短的报告。

只看到 EOF 就断定文件正常结束，没有检查 ferror。

在 macOS/Linux 上运行目录输入测试：可能打开就失败，也可能打开后读取失败。两种情况的 stdout 都必须为空。

fgetc 返回 EOF 时检查 ferror。通过 analyze 传递 LINE_IO_ERROR，使 main 返回 1 且不调用 stats_print。

## 测试计划

### 六条可手算的有效记录

退出码 0；INFO 3 次、WARN 2 次、ERROR 1 次；总和 200，范围 0–100，均值 33.333。

使用独立于程序计算的结果，发现级别索引、遗漏更新或聚合计算错误。

### 有效与错误记录混合

退出码 3；有效 3 行、错误 3 行；总和 30；警告指出第 2、4、5 行。

验证拒绝数据只增加错误计数，并且后面的有效记录仍能处理。

### 空输入与二十个空白行

空输入：退出码 0，全部计数为零，耗时为 n/a。空白行：退出码 3，拒绝二十行，五条详细警告加一条省略提示。

区分没有数据和错误数据，并防止诊断信息无限增长。

### 整数与级别校验

接受 0、60000 和前导零；拒绝 60001、正负号、小数、后缀、超大整数、多余字段和不匹配的级别。

覆盖契约的两个端点，防止宽松的部分转换。

### 行边界与二进制字节

接受 CRLF、制表符和缺少末尾 LF 的最后一行。拒绝 NUL 与 0xff 所在行，同时保留后面的 ERROR 9。

检查字符串结束、普通字节与 EOF 的区分，以及损坏后的继续处理。

### 127 字节行、128 字节行，再接有效行

恰好 3 行，接受 2 行、拒绝 1 行；耗时总和 8。

发现缓冲区边界差一错误，并验证读到换行的行为。

### 一 MiB 与多一字节

8192 条填充后的有效行恰好占 1,048,576 字节，能够成功。再加一字节返回 1 且不输出报告。

同时验证允许的一侧与拒绝的一侧，检查总输入工作量边界。

### 命令行与真实文件系统错误

错误参数数量返回 2；文件不存在或输入是目录时返回 1；所有情况的 stdout 均为空。

运行真实子进程并操作真实文件系统，不用模拟成功输出来替代测试。

### 由 1、2、2 计算小数均值

退出码 0，mean_ms=1.667。

发现整数平均值样本容易漏掉的整数除法截断。

## 工程取舍

### 固定行缓冲区与总字节预算

getline 的可增长缓冲区很方便，但第一个项目用 128 字节固定数组，更容易看清内存与结束符。我们拒绝较长行并读完其余部分。处理 B 个字节用 O(B) 时间，应用状态用 O(1) 空间，超过 1 MiB 后最多再检查一个字节。标准 I/O 另有自己的内部缓冲区。字节预算不是时间期限：stdin 可能等待生产者，建议先读已完成的普通文件。

### 用边界证明整数安全

耗时用 unsigned，最大 60000。解析器先检查再做乘法。计数和总和用 uint64_t；即使用保守边界 1,048,576 × 60,000 = 62,914,560,000 也能容纳。静态断言在常量变化时保护这个边界。完成整数累积后，均值才使用浮点除法；显示三位小数不会改变精确的整数总和。

### 保留有用数据，也要诚实标记状态

错误行不应毁掉其他有效观测。退出码 3 表明完整报告排除了部分行。致命输入错误则禁止输出报告，因为输入尚未完整检查。详细警告最多五条，再加一条省略提示。这既方便终端使用，也便于脚本判断。合法的 ERROR 事件本身不会让程序失败。

### 按变化原因拆成小模块

改变空白规则应修改 record.c；改变行容量应修改 reader.c；增加统计指标应修改 stats.c；改变命令行策略应修改 main.c。头文件注明借用指针与前置条件。解析器承诺不保留文本指针，因此记录不依赖会被重用的缓冲区。实现保持四个源文件，不为每个小辅助函数另建文件。

### 知道成品的边界

格式是人工设计的：没有时间戳、任意消息、实时追踪或百分位数。会检查读、写和关闭函数返回的错误，但写错误可能留下部分 stdout，断开的管道还可能触发 POSIX 默认 SIGPIPE 信号。不重试 stderr 写入失败。测试验证确定性的接口行为，不涵盖每种设备或文件系统故障，也不把耗时或调度顺序当作正确答案。

## 完整源文件

### record.h

记录接口

[下载文件](../project-code/comp2017-log-analyzer/record.h)

```c
/* Leon | Original teaching project. */
#ifndef RECORD_H
#define RECORD_H

#include <stdbool.h>

#define MAX_DURATION_MS 60000U

enum log_level { LEVEL_INFO, LEVEL_WARN, LEVEL_ERROR, LEVEL_COUNT };

struct record {
    enum log_level level;
    unsigned duration_ms;
};

/* line: readable NUL-terminated text; out: writable caller-owned record.
 * Return true and assign *out only for a complete valid record.
 * Neither pointer is retained; a failed parse leaves *out unchanged. */
bool parse_record(const char *line, struct record *out);

#endif
```

1. 把 enum 和 struct 一起读：级别是类别，耗时是有范围的非负值。

2. 解析器接收借用的文本和调用者拥有的输出地址，用 bool 表示成功。

3. 失败承诺很明确：*out 不变。用这个承诺检查实现。

### record.c

严格的整行解析

[下载文件](../project-code/comp2017-log-analyzer/record.c)

```c
/* Leon | Original teaching project. */
#include "record.h"

#include <stddef.h>
#include <string.h>

static bool is_space(char ch)
{
    return ch == ' ' || ch == '\t';
}

static const char *skip_space(const char *p)
{
    while (is_space(*p)) {
        ++p;
    }
    return p;
}

bool parse_record(const char *line, struct record *out)
{
    struct record candidate = {LEVEL_INFO, 0U};
    const char *start = skip_space(line);
    const char *p = start;

    while (*p != '\0' && !is_space(*p)) {
        ++p;
    }
    size_t length = (size_t)(p - start);
    if (length == 4 && memcmp(start, "INFO", 4) == 0) {
        candidate.level = LEVEL_INFO;
    } else if (length == 4 && memcmp(start, "WARN", 4) == 0) {
        candidate.level = LEVEL_WARN;
    } else if (length == 5 && memcmp(start, "ERROR", 5) == 0) {
        candidate.level = LEVEL_ERROR;
    } else {
        return false;
    }
    if (!is_space(*p)) {
        return false;
    }
    p = skip_space(p);
    if (*p < '0' || *p > '9') {
        return false;
    }
    while (*p >= '0' && *p <= '9') {
        unsigned digit = (unsigned)(*p - '0');
        if (candidate.duration_ms > (MAX_DURATION_MS - digit) / 10U) {
            return false;
        }
        candidate.duration_ms = candidate.duration_ms * 10U + digit;
        ++p;
    }
    if (*skip_space(p) != '\0') {
        return false;
    }
    *out = candidate;
    return true;
}
```

1. 两个 static 空白辅助函数只接受空格与制表符，让语法不依赖地区设置。

2. 数字解析前，先用词长和 memcmp 检查完整级别单词。

3. 数字循环在运算前检查范围；最终字符串末尾检查和赋值共同实现整体提交。

### reader.h

行与字节预算接口

[下载文件](../project-code/comp2017-log-analyzer/reader.h)

```c
/* Leon | Original teaching project. */
#ifndef READER_H
#define READER_H

#include <stddef.h>
#include <stdio.h>

#define MAX_LINE_BYTES 127U
#define MAX_INPUT_BYTES 1048576U

enum line_status { LINE_OK, LINE_BAD, LINE_END, LINE_IO_ERROR, LINE_LIMIT };

struct line_reader {
    FILE *stream;       /* Borrowed: only the caller closes this stream. */
    size_t bytes_read;  /* Start at zero; includes newline and CR bytes. */
};

/* Caller supplies MAX_LINE_BYTES + 1 writable bytes.
 * LINE_OK: complete NUL-terminated line, without LF or a final CR.
 * LINE_BAD: oversized or NUL-containing line was consumed through LF/EOF.
 * LINE_END: clean EOF with no pending line. Other results are fatal.
 * LINE_LIMIT may consume one byte beyond the budget to distinguish EOF.
 * Do not parse the buffer unless the result is LINE_OK. */
enum line_status read_line(struct line_reader *reader,
                           char line[MAX_LINE_BYTES + 1U]);

#endif
```

1. MAX_LINE_BYTES 不包含 LF，但包含 CR；分配 C 字符串缓冲区时还要加一字节。

2. line_reader 保存借用的流和累计字节数，每个输入开始时初始化一次计数。

3. 每个枚举结果对应不同的调用者动作，只有 LINE_OK 承诺缓冲区可供解析。

### reader.c

物理行边界处理

[下载文件](../project-code/comp2017-log-analyzer/reader.c)

```c
/* Leon | Original teaching project. */
#include "reader.h"

#include <stdbool.h>

enum line_status read_line(struct line_reader *reader,
                           char line[MAX_LINE_BYTES + 1U])
{
    size_t used = 0;
    bool seen_byte = false;
    bool bad = false;

    for (;;) {
        int ch = fgetc(reader->stream);
        if (ch == EOF) {
            if (ferror(reader->stream)) {
                return LINE_IO_ERROR;
            }
            if (!seen_byte) {
                return LINE_END;
            }
            break;
        }
        if (reader->bytes_read == MAX_INPUT_BYTES) {
            return LINE_LIMIT;
        }
        ++reader->bytes_read;
        seen_byte = true;
        if (ch == '\n') {
            break;
        }
        if (ch == '\0' || used == MAX_LINE_BYTES) {
            bad = true;
        }
        if (!bad) {
            line[used++] = (char)ch;
        }
        /* Keep consuming a bad line so its tail is not a new record. */
    }
    if (bad) {
        return LINE_BAD;
    }
    if (used > 0 && line[used - 1] == '\r') {
        --used;
    }
    line[used] = '\0';
    return LINE_OK;
}
```

1. fgetc 返回 int。遇到 EOF 时先检查 ferror，再判断是否还有未结束的最后一行。

2. 每个消费的字节都计入输入预算，包括换行和被丢弃的字节。

3. bad 会停止写缓冲区，但不会停止读流。成功的行在返回前处理末尾 CR，并加 NUL 结束符。

### stats.h

状态与统计接口

[下载文件](../project-code/comp2017-log-analyzer/stats.h)

```c
/* Leon | Original teaching project. */
#ifndef STATS_H
#define STATS_H

#include "record.h"

#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>

struct stats {
    uint64_t lines;
    uint64_t valid;
    uint64_t malformed;
    uint64_t by_level[LEVEL_COUNT];
    uint64_t total_ms;
    unsigned min_ms;
    unsigned max_ms;
};

/* Start with struct stats s = {0}. Add at most MAX_INPUT_BYTES records.
 * record must come from a successful parse_record call.
 * All pointers are borrowed for the duration of each call. */
void stats_accept(struct stats *s, const struct record *record);
void stats_reject(struct stats *s);

/* Write the final summary; false means a write/flush error.
 * A failed output may already contain a prefix. Do not close output here. */
bool stats_print(FILE *output, const struct stats *s);

#endif
```

1. 分开 valid 和 malformed，避免把总行数当作有效观测数。

2. 重复累积的计数和总和用 uint64_t，极值使用与单次耗时相同的类型。

3. 阅读前置条件：状态零初始化，记录已校验，更新次数不超过输入预算。

### stats.c

统计更新与报告格式

[下载文件](../project-code/comp2017-log-analyzer/stats.c)

```c
/* Leon | Original teaching project. */
#include "stats.h"
#include "reader.h"

#include <inttypes.h>

_Static_assert((uint64_t)MAX_INPUT_BYTES <= UINT64_MAX / MAX_DURATION_MS,
               "The byte budget must keep duration totals representable");

void stats_accept(struct stats *s, const struct record *record)
{
    if (s->valid == 0 || record->duration_ms < s->min_ms) {
        s->min_ms = record->duration_ms;
    }
    if (s->valid == 0 || record->duration_ms > s->max_ms) {
        s->max_ms = record->duration_ms;
    }
    ++s->lines;
    ++s->valid;
    ++s->by_level[record->level];
    s->total_ms += record->duration_ms;
}

void stats_reject(struct stats *s)
{
    ++s->lines;
    ++s->malformed;
}

bool stats_print(FILE *output, const struct stats *s)
{
    if (fprintf(output,
                "lines=%" PRIu64 "\nvalid=%" PRIu64 "\nmalformed=%" PRIu64 "\n"
                "INFO=%" PRIu64 "\nWARN=%" PRIu64 "\nERROR=%" PRIu64 "\n"
                "total_ms=%" PRIu64 "\n",
                s->lines, s->valid, s->malformed,
                s->by_level[LEVEL_INFO], s->by_level[LEVEL_WARN],
                s->by_level[LEVEL_ERROR], s->total_ms) < 0) {
        return false;
    }
    if (s->valid == 0) {
        if (fputs("min_ms=n/a\nmax_ms=n/a\nmean_ms=n/a\n", output) == EOF) {
            return false;
        }
    } else {
        double mean = (double)s->total_ms / (double)s->valid;
        if (fprintf(output, "min_ms=%u\nmax_ms=%u\nmean_ms=%.3f\n",
                    s->min_ms, s->max_ms, mean) < 0) {
            return false;
        }
    }
    return fflush(output) == 0;
}
```

1. 静态断言在编译时把输入上限与可表示的耗时总和联系起来。

2. stats_accept 先处理第一条记录的极值，再一起更新相关计数与总和。

3. stats_print 用 PRIu64 可移植地格式化 uint64_t，避免空数据除法，并在报告成功前刷新输出。

### main.c

命令行、流程与清理

[下载文件](../project-code/comp2017-log-analyzer/main.c)

```c
/* Leon | Original teaching project. */
#include "reader.h"
#include "record.h"
#include "stats.h"

#include <inttypes.h>
#include <stdio.h>
#include <string.h>

enum exit_status { EXIT_CLEAN = 0, EXIT_IO = 1, EXIT_USAGE = 2, EXIT_DATA = 3 };
#define WARNING_LIMIT 5U

static void warn_bad_line(const struct stats *s)
{
    if (s->malformed <= WARNING_LIMIT) {
        fprintf(stderr, "warning: line %" PRIu64 ": malformed record\n", s->lines);
    } else if (s->malformed == WARNING_LIMIT + 1U) {
        fputs("warning: further malformed lines omitted\n", stderr);
    }
}

/* Borrow input and caller-owned statistics. Report only complete input. */
static bool analyze(FILE *input, struct stats *s)
{
    struct line_reader reader = {input, 0};
    char line[MAX_LINE_BYTES + 1U];

    for (;;) {
        enum line_status status = read_line(&reader, line);
        if (status == LINE_END) {
            return true;
        }
        if (status == LINE_IO_ERROR) {
            fputs("error: cannot read input\n", stderr);
            return false;
        }
        if (status == LINE_LIMIT) {
            fprintf(stderr, "error: input exceeds %u bytes\n", MAX_INPUT_BYTES);
            return false;
        }
        struct record record;
        if (status == LINE_BAD || !parse_record(line, &record)) {
            stats_reject(s);
            warn_bad_line(s);
        } else {
            stats_accept(s, &record);
        }
    }
}

int main(int argc, char **argv)
{
    if (argc != 2) {
        fputs("usage: log_analyzer FILE|-\n", stderr);
        return EXIT_USAGE;
    }
    bool owns_input = strcmp(argv[1], "-") != 0;
    FILE *input = owns_input ? fopen(argv[1], "rb") : stdin;
    if (input == NULL) {
        fprintf(stderr, "error: cannot open input: %s\n", argv[1]);
        return EXIT_IO;
    }

    struct stats totals = {0};
    bool completed = analyze(input, &totals);
    if (owns_input && fclose(input) != 0) {
        fputs("error: cannot close input\n", stderr);
        completed = false;
    }
    if (!completed) {
        return EXIT_IO;
    }
    if (!stats_print(stdout, &totals)) {
        fputs("error: cannot write report\n", stderr);
        return EXIT_IO;
    }
    return totals.malformed == 0 ? EXIT_CLEAN : EXIT_DATA;
}
```

1. main 检查参数数量，区分自己打开的文件输入和借用的 stdin。

2. analyze 将读行结果映射成解析、拒绝、正常结束或致命失败。|| 的短路求值避免解析 LINE_BAD 缓冲区。

3. 警告输出数量限制与计数分开处理。先清理输入再打印，最后通过返回值传达数据质量。

### Makefile

可复现的多文件构建

[下载文件](../project-code/comp2017-log-analyzer/Makefile)

```make
# Leon | Original teaching project.
CC = clang
CFLAGS = -std=c11 -Wall -Wextra -Werror -pedantic -pthread
OBJECTS = main.o reader.o record.o stats.o

.PHONY: all test clean
all: log_analyzer

log_analyzer: $(OBJECTS)
	$(CC) $(CFLAGS) $(LDFLAGS) -o $@ $(OBJECTS) $(LDLIBS)

main.o: main.c reader.h record.h stats.h
reader.o: reader.c reader.h
record.o: record.c record.h
stats.o: stats.c stats.h record.h reader.h

%.o: %.c
	$(CC) $(CPPFLAGS) $(CFLAGS) -c $< -o $@

test: log_analyzer
	python3 test.py

clean:
	rm -f log_analyzer $(OBJECTS)
```

1. all 指向可执行文件，四个目标文件对应四个 C 实现文件。

2. 头文件依赖让接口变化时重新构建相关文件。模式规则负责编译，可执行文件规则负责链接。

3. test 先构建，再运行 python3 test.py。clean 只移除本项目列出的程序和目标文件。

### fixtures/demo.log

有效的模拟机器人记录

[下载文件](../project-code/comp2017-log-analyzer/fixtures/demo.log)

```text
INFO 10
WARN 40
INFO 20
ERROR 100
INFO 0
WARN 30
```

1. 六行全部符合语法，包含合法的零耗时和 ERROR 事件。

2. 运行前先算 10 + 40 + 20 + 100 + 0 + 30 = 200。

3. 用这个小样本比较终端输出和 test.py 中明确写出的预期报告。

### fixtures/mixed.log

三条坏行夹杂的有效数据

[下载文件](../project-code/comp2017-log-analyzer/fixtures/mixed.log)

```text
INFO 5
DEBUG 8
WARN 10
ERROR -1
INFO 60001
ERROR 15
```

1. 第 2、4、5 行分别违反级别、正负号和耗时上限规则。

2. 剩余的 5、10、15 总和为 30；全部为正数，因此能检查第一条记录的最小值初始化。

3. 预期有完整报告和警告，但退出码为 3，体现有报告不等于完全成功。

### fixtures/empty.log

真正的空输入流

[下载文件](../project-code/comp2017-log-analyzer/fixtures/empty.log)

不可见字节视图（十六进制）：空文件；零字节

1. 该文件是零字节，没有表头，也没有换行。

2. 它用于测试没有观测值时的正常完成，并非测试坏行。

3. 对比发送空白行的测试：空白行确实形成物理行，也产生错误计数。

### test.py

可执行程序的行为测试

[下载文件](../project-code/comp2017-log-analyzer/test.py)

```python
# Leon | Original teaching project.
"""Behavior tests: run `make test`; every generated input stays in a temp dir."""
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent
PROGRAM = ROOT / "log_analyzer"


class AnalyzerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="log-analyzer-test-")
        self.addCleanup(self.temp.cleanup)
        self.work = Path(self.temp.name)

    def run_log(self, data=b"", args=None):
        if args is None:
            args = ["-"]
        self.assertTrue(PROGRAM.is_file(), "Build log_analyzer with make first")
        return subprocess.run(
            [str(PROGRAM), *args], input=data, capture_output=True,
            cwd=self.work, timeout=5, check=False,
        )

    def fields(self, result):
        lines = result.stdout.decode("ascii").splitlines()
        self.assertEqual(len(lines), 10, result.stdout)
        return dict(line.split("=", 1) for line in lines)

    def test_demo_has_hand_calculated_totals(self):
        shutil.copyfile(ROOT / "fixtures/demo.log", self.work / "demo.log")
        result = self.run_log(args=["demo.log"])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, b"")
        self.assertEqual(result.stdout, (
            b"lines=6\nvalid=6\nmalformed=0\nINFO=3\nWARN=2\nERROR=1\n"
            b"total_ms=200\nmin_ms=0\nmax_ms=100\nmean_ms=33.333\n"
        ))

    def test_mixed_file_keeps_good_rows_and_reports_exit_3(self):
        shutil.copyfile(ROOT / "fixtures/mixed.log", self.work / "mixed.log")
        result = self.run_log(args=["mixed.log"])
        self.assertEqual(result.returncode, 3)
        self.assertEqual(result.stdout, (
            b"lines=6\nvalid=3\nmalformed=3\nINFO=1\nWARN=1\nERROR=1\n"
            b"total_ms=30\nmin_ms=5\nmax_ms=15\nmean_ms=10.000\n"
        ))
        for number in (2, 4, 5):
            self.assertIn(f"line {number}: malformed record".encode(), result.stderr)

    def test_empty_has_no_invented_latency(self):
        result = self.run_log()
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, (
            b"lines=0\nvalid=0\nmalformed=0\nINFO=0\nWARN=0\nERROR=0\n"
            b"total_ms=0\nmin_ms=n/a\nmax_ms=n/a\nmean_ms=n/a\n"
        ))

    def test_duration_boundaries(self):
        result = self.run_log(b"INFO 0\nERROR 60000\n")
        self.assertEqual(result.returncode, 0)
        fields = self.fields(result)
        self.assertEqual(fields["total_ms"], "60000")
        self.assertEqual(fields["min_ms"], "0")
        self.assertEqual(fields["max_ms"], "60000")
        self.assertEqual(fields["mean_ms"], "30000.000")

    def test_integer_grammar_rejects_signs_suffixes_and_overflow(self):
        bad = [b"", b"+1", b"-1", b"1.5", b"1ms", b"1 2", b"60001",
               b"999999999999999999999999", b"0x10", b"1e2"]
        for token in bad:
            with self.subTest(token=token):
                result = self.run_log(b"INFO " + token + b"\n")
                self.assertEqual(result.returncode, 3)
                fields = self.fields(result)
                self.assertEqual(fields["valid"], "0")
                self.assertEqual(fields["malformed"], "1")
                self.assertEqual(fields["mean_ms"], "n/a")

    def test_level_must_match_whole_uppercase_word(self):
        for level in (b"info", b"DEBUG", b"INF", b"INFOx", b"WARN3"):
            with self.subTest(level=level):
                result = self.run_log(level + b" 2\n")
                self.assertEqual(result.returncode, 3)
                self.assertEqual(self.fields(result)["valid"], "0")

    def test_crlf_tabs_leading_zero_and_unterminated_last_line(self):
        result = self.run_log(b" \tINFO\t0007 \r\nWARN 3")
        self.assertEqual(result.returncode, 0)
        fields = self.fields(result)
        self.assertEqual(fields["lines"], "2")
        self.assertEqual(fields["total_ms"], "10")
        self.assertEqual(fields["mean_ms"], "5.000")

    def test_line_limit_is_exact_and_drains_one_bad_record(self):
        exact = b"INFO " + b"0" * 121 + b"1"
        too_long = b"INFO 2" + b" " * 122
        self.assertEqual(len(exact), 127)
        self.assertEqual(len(too_long), 128)
        result = self.run_log(exact + b"\n" + too_long + b"\nWARN 7\n")
        self.assertEqual(result.returncode, 3)
        fields = self.fields(result)
        self.assertEqual(fields["lines"], "3")
        self.assertEqual(fields["malformed"], "1")
        self.assertEqual(fields["valid"], "2")
        self.assertEqual(fields["total_ms"], "8")

    def test_binary_bytes_do_not_hide_suffix_or_imitate_eof(self):
        result = self.run_log(b"INFO 2\x00hidden\n\xff\nERROR 9\n")
        self.assertEqual(result.returncode, 3)
        fields = self.fields(result)
        self.assertEqual(fields["lines"], "3")
        self.assertEqual(fields["malformed"], "2")
        self.assertEqual(fields["total_ms"], "9")

    def test_blank_lines_count_and_diagnostics_are_capped(self):
        result = self.run_log(b"\n" * 20)
        self.assertEqual(result.returncode, 3)
        self.assertEqual(self.fields(result)["malformed"], "20")
        self.assertEqual(result.stderr.count(b"malformed record"), 5)
        self.assertEqual(result.stderr.count(b"further malformed lines omitted"), 1)

    def test_mean_uses_fractional_division(self):
        result = self.run_log(b"INFO 1\nINFO 2\nINFO 2\n")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(self.fields(result)["mean_ms"], "1.667")

    def test_byte_budget_accepts_exactly_one_mebibyte(self):
        row = b"INFO 0" + b" " * 121 + b"\n"
        result = self.run_log(row * 8192)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.fields(result)["valid"], "8192")
        self.assertEqual(self.fields(result)["total_ms"], "0")

    def test_byte_budget_failure_has_no_partial_report(self):
        row = b"INFO 0" + b" " * 121 + b"\n"
        result = self.run_log(row * 8192 + b"x")
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout, b"")
        self.assertIn(b"input exceeds 1048576 bytes", result.stderr)

    def test_argument_count_is_a_usage_error(self):
        for args in ([], ["one", "two"]):
            with self.subTest(args=args):
                result = self.run_log(args=args)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(result.stdout, b"")
                self.assertIn(b"usage:", result.stderr)

    def test_missing_file_is_an_io_error(self):
        result = self.run_log(args=["missing.log"])
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout, b"")
        self.assertIn(b"cannot open", result.stderr)

    def test_directory_is_not_a_successful_input(self):
        result = self.run_log(args=[str(self.work)])
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout, b"")
        self.assertTrue(b"cannot open" in result.stderr or
                        b"cannot read" in result.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
```

1. setUp 创建新的临时目录，addCleanup 负责删除。run_log 不经 shell 调用真实程序，并设置超时。

2. 样本预期输出使用独立计算的明确常量。其他测试针对具体失败模式或边界。

3. 每个限制都测试两侧。文件缺失和目录情况使用真实临时路径；没有穷尽模拟所有输出和关闭故障。

### README.md

完整英文运行指南

[下载文件](../project-code/comp2017-log-analyzer/README.md)

1. 先阅读构建、运行、测试命令和退出码表。

2. 把五个阶段和文件顺序当作阅读源码的路线。

3. 复现三次实际示例，再阅读取舍和扩展验收标准。

### README.zh.md

完整中文运行指南

[下载文件](../project-code/comp2017-log-analyzer/README.zh.md)

1. 中文指南提供与英文指南一致的命令和输入契约。

2. 把其中的类型、资源归属和调试说明与源码里的英文标识符对照。

3. 两种指南中的输出键都保持固定英文，因此切换指南语言不会改变程序和测试。

## 扩展方向

### 为各级别增加耗时统计

先增加可手算的测试。为每个级别保存数量与总和，只在解析成功后更新，再用一致的空级别规则打印均值。

示例中 INFO 均值为 10.000，WARN 为 35.000，ERROR 为 100.000。缺失级别输出 n/a，错误行不参与统计，原有全局指标保持不变。

### 增加明确的严格模式

把 --strict 加入参数契约。编码前先确定策略：遇到第一条坏行即停止，关闭自己拥有的流，stdout 保持为空。保留当前默认行为。

严格模式读取混合样本时返回 3，只警告第 2 行，且没有报告。不加选项时输出保持原样；有效输入和空输入仍返回 0。

## 一手参考资料

- [WG14 N1570 — C11 committee draft: integer types and standard I/O](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)

- [Clang Compiler User’s Manual](https://clang.llvm.org/docs/UsersManual.html)

- [Python documentation — subprocess management](https://docs.python.org/3/library/subprocess.html)

---
Leon
