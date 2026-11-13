/* Explain a failed run in plain words, in Chinese or English, for someone who has never seen an error message.
   It reads what the browser runners actually print: Python tracebacks (Pyodide), xcc's "main.c(N): message" and
   javac's "Main.java:N: message". It names the line, says what usually causes this error, and what to try.
   Errors it does not know get a plain fallback that still points at the line; the raw message stays on screen. */

const ZH = {
  line: (n) => `第 ${n} 行`,
  inTests: (n) => `第 ${n} 行在测试代码里，不在你写的部分：你的代码运行了，但测试发现结果不对，或者它在测试调用时出错。`,
  inTestsCompile: (n) => `${n ? `第 ${n} 行` : '报错的位置'}在测试代码里，不在你写的部分。程序没有通过编译，所以什么都没有运行。常见原因：测试用到的名字在你的代码里没有定义（对照题目检查函数名和参数），或者你的代码里有一个 { 没有关上。`,
  lineBefore: (n) => `编译器在第 ${n} 行发现问题；漏掉的东西常常在上一行的末尾。`,
  tryIt: '试试：',
  fallback: { title: '程序出错停止了', what: '下面是原始报错。先看它指出的那一行，再对照讲解里的代码逐字比较。' },
  fallbackNoLine: { title: '程序出错停止了', what: '下面是原始报错，它没有指出是哪一行。可以在程序里加几行打印，看看运行到哪里停下，再对照讲解里的代码检查那一段。' },
};
const EN = {
  line: (n) => `Line ${n}`,
  inTests: (n) => `Line ${n} is in the test code, not in what you wrote: your code ran, but a test found a wrong result or your code failed when the test called it.`,
  inTestsCompile: (n) => `${n ? `Line ${n}` : 'The error'} is in the test code, not in what you wrote. The program did not compile, so nothing ran. Usually the test uses a name your code does not define (check the function name and its parameters against the question), or a { in your code is never closed.`,
  lineBefore: (n) => `The compiler noticed it on line ${n}; the missing piece is often at the end of the line before.`,
  tryIt: 'Try: ',
  fallback: { title: 'The program stopped with an error', what: 'The raw message is below. Look at the line it names first, then compare that line with the code in the lesson, character by character.' },
  fallbackNoLine: { title: 'The program stopped with an error', what: 'The raw message is below; it does not name a line. Add a few prints to see how far the program gets, then compare that part with the code in the lesson.' },
};

/* each rule: a pattern on the message, and the explanation in both languages; $1 is the first captured name */
const PYTHON = [
  [/NameError: name '([^']+)' is not defined(?:\. Did you mean: '([^']+)'\?)?/, (m) => ({
    zh: { title: `不认识名字 ${m[1]}（NameError）`, what: `Python 不知道 \`${m[1]}\` 是什么。最常见的原因是拼写错误，其次是变量还没有赋值就先使用了，或者文字忘了加引号。${m[2] ? `Python 猜你想写的是 \`${m[2]}\`。` : ''}`, fix: m[2] ? `把 \`${m[1]}\` 改成 \`${m[2]}\`。` : `检查 \`${m[1]}\` 的拼写和大小写，确认它在这一行之前已经赋值。` },
    en: { title: `Python does not know the name ${m[1]} (NameError)`, what: `Python has no idea what \`${m[1]}\` is. Most often it is a typo; otherwise a variable is used before it gets a value, or some text is missing its quotes.${m[2] ? ` Python guesses you meant \`${m[2]}\`.` : ''}`, fix: m[2] ? `change \`${m[1]}\` to \`${m[2]}\`.` : `check the spelling and capitals of \`${m[1]}\`, and that it gets a value before this line.` },
  })],
  [/IndentationError: (.+)/, (m) => ({
    zh: { title: '缩进不对（IndentationError）', what: `Python 用行首的空格来分组：if、for、while、def 这一行以冒号结尾，下面属于它的每一行都要多缩进一层（通常 4 个空格）。这里的情况是：${m[1]}。`, fix: '让同一组的行左边对齐，冒号下面的行多缩进 4 个空格，不要混用 Tab 和空格。' },
    en: { title: 'The indentation is wrong (IndentationError)', what: `Python groups lines by the spaces at their start: a line ending in a colon (if, for, while, def) must be followed by lines indented one more level, usually 4 spaces. Here: ${m[1]}.`, fix: 'line up the lines of one block, indent the lines under a colon by 4 more spaces, and do not mix tabs and spaces.' },
  })],
  [/SyntaxError: (?:invalid syntax\. )?Maybe you meant '==' or ':=' instead of '='\?/, () => ({
    zh: { title: '比较要用 ==（SyntaxError）', what: '在 if 或 while 里比较两个值要写 ==。一个 = 是赋值，Python 不允许在这里赋值。', fix: '把这一行的 = 改成 ==。' },
    en: { title: 'Use == to compare (SyntaxError)', what: 'Comparing two values in an if or while needs ==. A single = stores a value, which is not allowed here.', fix: 'change = to == on this line.' },
  })],
  [/SyntaxError: '(.)' was never closed/, (m) => ({
    zh: { title: `括号 ${m[1]} 没有关上（SyntaxError）`, what: `这一行打开了 \`${m[1]}\`，但后面没有对应的右括号。`, fix: '数一数这一行的左括号和右括号，补上缺的那个。' },
    en: { title: `A ${m[1]} is never closed (SyntaxError)`, what: `This line opens \`${m[1]}\` and never closes it.`, fix: 'count the opening and closing brackets on this line and add the missing one.' },
  })],
  [/SyntaxError: unterminated (?:triple-quoted )?string literal/, () => ({
    zh: { title: '引号没有配对（SyntaxError）', what: '一段文字用引号开始，却没有用同样的引号结束。', fix: '在文字末尾补上和开头一样的引号（\' 或 "；如果开头是三个引号，结尾也要三个）。' },
    en: { title: 'A quote is never closed (SyntaxError)', what: 'Some text starts with a quote but never ends with the same quote.', fix: 'add the same quote (\' or ") at the end of the text (three quotes if it started with three).' },
  })],
  [/SyntaxError: expected ':'/, () => ({
    zh: { title: '少了冒号（SyntaxError）', what: 'if、elif、else、for、while、def、class 这些行的末尾必须有冒号。', fix: '在这一行末尾加上 :。' },
    en: { title: 'A colon is missing (SyntaxError)', what: 'Lines starting with if, elif, else, for, while, def or class must end with a colon.', fix: 'add : at the end of this line.' },
  })],
  [/SyntaxError: (.+)/, (m) => ({
    zh: { title: '这一行不符合 Python 的写法（SyntaxError）', what: `Python 还没开始运行就停下了，因为这一行写法不对：${m[1]}。常见原因是括号或引号没配对、少了冒号、或者多打了符号。`, fix: '对照讲解里的代码逐字检查这一行和它的上一行。' },
    en: { title: 'This line is not valid Python (SyntaxError)', what: `Python stopped before running anything because this line is not valid: ${m[1]}. Usually a bracket or quote does not pair up, a colon is missing, or there is an extra symbol.`, fix: 'compare this line and the one before it with the lesson, character by character.' },
  })],
  [/TypeError: can only concatenate str \(not "([^"]+)"\) to str/, (m) => ({
    zh: { title: '文字和数字不能直接相加（TypeError）', what: `+ 两边一个是文字（str），一个是 ${m[1]}。Python 不会自动把数字变成文字。`, fix: '用 str(数字) 先转成文字，或者写 f"...{数字}..."。' },
    en: { title: 'Text and a number cannot be added (TypeError)', what: `One side of + is text (str) and the other is ${m[1]}. Python does not turn numbers into text by itself.`, fix: 'convert with str(number) first, or write f"...{number}...".' },
  })],
  [/TypeError: (.+) missing (\d+) required positional argument/, (m) => ({
    zh: { title: '调用函数时少给了参数（TypeError）', what: `${m[1]} 需要的参数比你给的多 ${m[2]} 个。`, fix: '对照函数定义里括号中的参数个数，调用时一一给出。' },
    en: { title: 'A function call is missing arguments (TypeError)', what: `${m[1]} needs ${m[2]} more argument(s) than the call gives.`, fix: 'count the parameters in the function definition and give one value for each.' },
  })],
  [/TypeError: (.+)/, (m) => ({
    zh: { title: '这种值不能这样用（TypeError）', what: `某个值的类型不支持这里的操作：${m[1]}。比如把数字当列表取下标，或者把列表当函数调用。`, fix: '用 print(type(变量)) 看看这一行用到的值到底是什么类型。' },
    en: { title: 'This kind of value cannot be used this way (TypeError)', what: `A value's type does not support this operation: ${m[1]}. For example indexing a number, or calling a list as if it were a function.`, fix: 'print(type(value)) for the values on this line to see what they really are.' },
  })],
  [/ZeroDivisionError/, () => ({
    zh: { title: '除以了 0（ZeroDivisionError）', what: '除法、整除或取余的右边是 0，数学上没有定义。', fix: '先用 if 判断除数是不是 0，再做除法。' },
    en: { title: 'Division by zero (ZeroDivisionError)', what: 'The right-hand side of /, // or % is 0, which has no value in mathematics.', fix: 'check with an if that the divisor is not 0 before dividing.' },
  })],
  [/IndexError: (.+)/, (m) => ({
    zh: { title: '下标超出范围（IndexError）', what: `${m[1]}。下标从 0 开始，长度为 n 的列表最后一个下标是 n − 1。`, fix: '打印 len(列表) 和你用的下标，看看是不是多数了一个。' },
    en: { title: 'Index out of range (IndexError)', what: `${m[1]}. Indexes start at 0, so a list of length n ends at index n − 1.`, fix: 'print len(the list) and the index you use; check for an off-by-one.' },
  })],
  [/KeyError: (.+)/, (m) => ({
    zh: { title: `字典里没有键 ${m[1]}（KeyError）`, what: `你要取的键 ${m[1]} 不在字典里。注意大小写和空格也要完全一样。`, fix: '先用 if 键 in 字典 判断，或者用 字典.get(键, 默认值)。' },
    en: { title: `The dictionary has no key ${m[1]} (KeyError)`, what: `The key ${m[1]} is not in the dictionary. Capitals and spaces must match exactly.`, fix: 'test with if key in d first, or use d.get(key, default).' },
  })],
  [/AttributeError: 'NoneType' object has no attribute '([^']+)'/, (m) => ({
    zh: { title: `None 没有 ${m[1]}（AttributeError）`, what: `这个值是 None，通常是因为某个函数没有返回值（没有写 return），或者一个方法在原处修改、返回的是 None，例如 list.sort()。`, fix: `往前找这个变量是从哪里得到的值，确认那个函数确实 return 了结果。` },
    en: { title: `None has no ${m[1]} (AttributeError)`, what: `The value is None, usually because a function returned nothing (no return), or a method that changes things in place returned None, such as list.sort().`, fix: `find where this variable got its value, and make sure that function really returns a result.` },
  })],
  [/AttributeError: '([^']+)' object has no attribute '([^']+)'/, (m) => ({
    zh: { title: `${m[1]} 没有 ${m[2]}（AttributeError）`, what: `这个值的类型是 ${m[1]}，它没有叫 \`${m[2]}\` 的方法或属性。常见原因是变量里装的不是你以为的类型，或者方法名拼错。`, fix: `检查 \`${m[2]}\` 的拼写，并打印这个变量看看它是什么。` },
    en: { title: `A ${m[1]} has no ${m[2]} (AttributeError)`, what: `This value is a ${m[1]}, which has no method or attribute called \`${m[2]}\`. Either the variable holds a different type than you think, or the name is misspelt.`, fix: `check the spelling of \`${m[2]}\` and print the variable to see what it holds.` },
  })],
  [/ValueError: invalid literal for int\(\) with base 10: (.+)/, (m) => ({
    zh: { title: '这段文字不能变成整数（ValueError）', what: `int() 只能转换像 "42" 这样的整数文字，${m[1]} 不是。`, fix: '先检查文字的内容，或者用 try/except 处理不是数字的输入。' },
    en: { title: 'This text is not a whole number (ValueError)', what: `int() converts text like "42"; ${m[1]} is not like that.`, fix: 'check the text first, or handle non-numbers with try/except.' },
  })],
  [/RecursionError/, () => ({
    zh: { title: '递归没有停下来（RecursionError）', what: '函数一直在调用自己，始终没有到达不再调用的终止情况，直到调用层数超过上限。', fix: '检查终止条件，以及每次递归调用是否让问题变小、一步步走向终止条件。' },
    en: { title: 'The recursion never stops (RecursionError)', what: 'The function keeps calling itself and never reaches a case that stops, until the call depth runs out.', fix: 'check the base case, and that every recursive call moves closer to it.' },
  })],
  [/UnboundLocalError: .*'([^']+)'/, (m) => ({
    zh: { title: `函数里先用了 ${m[1]} 再赋值（UnboundLocalError）`, what: `函数内部给 \`${m[1]}\` 赋了值，所以 Python 把它当作局部变量；但在赋值之前就读取了它。`, fix: '在函数里先给它赋初值，或者把它作为参数传进来。' },
    en: { title: `${m[1]} is used before it is assigned in the function (UnboundLocalError)`, what: `The function assigns \`${m[1]}\`, so Python treats it as local, but reads it before that assignment.`, fix: 'give it a value at the start of the function, or pass it in as a parameter.' },
  })],
  [/ModuleNotFoundError: No module named '([^']+)'/, (m) => ({
    zh: { title: `找不到模块 ${m[1]}（ModuleNotFoundError）`, what: `\`${m[1]}\` 拼错了，或者浏览器里的 Python 没有这个库。`, fix: '检查拼写；如果确实需要这个库，请在自己电脑上安装后运行。' },
    en: { title: `No module named ${m[1]} (ModuleNotFoundError)`, what: `\`${m[1]}\` is misspelt, or the Python in this browser does not have that library.`, fix: 'check the spelling; if you really need the library, install it on your computer and run there.' },
  })],
  [/AssertionError/, () => ({
    zh: { title: '一个测试没有通过（AssertionError）', what: 'assert 检查的条件不成立：你的代码算出的结果和测试期望的不一样。', fix: '看这一行测试用了什么输入、期望什么结果，用这个输入手算一遍你的代码。' },
    en: { title: 'A test did not pass (AssertionError)', what: 'The condition an assert checks is false: your code gave a different result from the one the test expects.', fix: 'read which input this test uses and what it expects, then trace your code by hand on that input.' },
  })],
];

const C_RULES = [
  [/`;' expected/, () => ({
    before: true,
    zh: { title: '少了分号', what: 'C 的每条语句都以分号结束。', fix: '在报错行的上一行（或这一行）末尾补上 ;。' },
    en: { title: 'A semicolon is missing', what: 'Every C statement ends with a semicolon.', fix: 'add ; at the end of the line before (or of this line).' },
  })],
  [/`(printf|scanf|puts|putchar|getchar|fprintf|snprintf|sprintf|sscanf|fgets|fputs|fopen|fclose|perror)' undeclared/, (m) => ({
    zh: { title: `${m[1]} 没有声明：缺少 #include <stdio.h>`, what: `\`${m[1]}\` 是标准库函数，要先包含声明它的头文件。`, fix: '在文件开头加上 #include <stdio.h>。' },
    en: { title: `${m[1]} is undeclared: #include <stdio.h> is missing`, what: `\`${m[1]}\` is a library function; its header must be included first.`, fix: 'add #include <stdio.h> at the top of the file.' },
  })],
  [/`(malloc|calloc|realloc|free|exit|atoi|abs|qsort|rand|srand|strtol)' undeclared/, (m) => ({
    zh: { title: `${m[1]} 没有声明：缺少 #include <stdlib.h>`, what: `\`${m[1]}\` 是标准库函数，要先包含声明它的头文件。`, fix: '在文件开头加上 #include <stdlib.h>。' },
    en: { title: `${m[1]} is undeclared: #include <stdlib.h> is missing`, what: `\`${m[1]}\` is a library function; its header must be included first.`, fix: 'add #include <stdlib.h> at the top of the file.' },
  })],
  [/`(strlen|strcpy|strncpy|strcmp|strncmp|strcat|strncat|strchr|strstr|memcpy|memmove|memset|memcmp)' undeclared/, (m) => ({
    zh: { title: `${m[1]} 没有声明：缺少 #include <string.h>`, what: `\`${m[1]}\` 是标准库函数，要先包含声明它的头文件。`, fix: '在文件开头加上 #include <string.h>。' },
    en: { title: `${m[1]} is undeclared: #include <string.h> is missing`, what: `\`${m[1]}\` is a library function; its header must be included first.`, fix: 'add #include <string.h> at the top of the file.' },
  })],
  ...[
    ['ctype.h', 'isdigit|isalpha|isalnum|isspace|isupper|islower|toupper|tolower'],
    ['math.h', 'sqrt|pow|fabs|floor|ceil|exp|log|sin|cos'],
    ['stdbool.h', 'bool|true|false'],
    ['limits.h', 'INT_MAX|INT_MIN|LONG_MAX|UINT_MAX|CHAR_BIT'],
    ['assert.h', 'assert'],
    ['stddef.h', 'NULL|size_t'],
  ].map(([header, names]) => [new RegExp(`\`(${names})' undeclared`), (m) => ({
    zh: { title: `${m[1]} 没有声明：缺少 #include <${header}>`, what: `\`${m[1]}\` 来自标准库，要先包含声明它的头文件。`, fix: `在文件开头加上 #include <${header}>。` },
    en: { title: `${m[1]} is undeclared: #include <${header}> is missing`, what: `\`${m[1]}\` comes from the standard library; its header must be included first.`, fix: `add #include <${header}> at the top of the file.` },
  })]),
  [/`([^']+)' undeclared/, (m) => ({
    zh: { title: `${m[1]} 没有声明`, what: `C 要求先声明再使用。\`${m[1]}\` 可能拼错了（C 区分大小写），可能在别的花括号里声明、这里看不到，也可能根本没有声明。如果它是标准库里的名字，说明缺少对应头文件的 #include。`, fix: `检查 \`${m[1]}\` 的拼写，并确认它在这一行之前、在同一作用域里声明过。` },
    en: { title: `${m[1]} is undeclared`, what: `C needs a declaration before use. \`${m[1]}\` may be misspelt (C is case-sensitive), declared inside other braces where it cannot be seen here, or never declared. If it is a library name, the #include for its header is missing.`, fix: `check the spelling of \`${m[1]}\` and that it is declared before this line, in this scope.` },
  })],
  [/`([)\]}])' expected/, (m) => ({
    zh: { title: `少了 ${m[1]}`, what: '括号没有配对：打开的括号要用同类的括号关上。', fix: `找到对应的左括号，在合适的位置补上 ${m[1]}。` },
    en: { title: `A ${m[1]} is missing`, what: 'Brackets do not pair up: each opening bracket needs a closing one of the same kind.', fix: `find the opening bracket and add ${m[1]} where it belongs.` },
  })],
  [/initializer more than array size|buffer is shorter than string/, () => ({
    zh: { title: '数组装不下初始值', what: '给数组的初始值比数组本身长。字符串还要多留 1 个位置放结尾的 \\0。', fix: '把数组改大，或者不写长度让编译器自己算，例如 char s[] = "...";。' },
    en: { title: 'The array is too small for its initial value', what: 'The initial value is longer than the array. A string also needs one more place for the closing \\0.', fix: 'make the array larger, or leave the size out and let the compiler count: char s[] = "...";.' },
  })],
  [/convert value from type `([^']+)' to `([^']+)'/, (m) => ({
    zh: { title: `类型不匹配：${m[1]} 被当成 ${m[2]}`, what: `这里需要 ${m[2]}，给的却是 ${m[1]}。例如把整数直接赋给指针。`, fix: '检查这一行两边的类型；指针要指向一个变量的地址（&变量）或 malloc 的结果。' },
    en: { title: `Types do not match: ${m[1]} used as ${m[2]}`, what: `This place needs a ${m[2]} but gets a ${m[1]}, such as an integer stored in a pointer.`, fix: 'check the types on both sides; a pointer should hold an address (&variable) or what malloc returns.' },
  })],
];

const JAVA_RULES = [
  [/';' expected/, () => ({
    zh: { title: '少了分号', what: 'Java 的每条语句都以分号结束。', fix: '在这一行末尾补上 ;。' },
    en: { title: 'A semicolon is missing', what: 'Every Java statement ends with a semicolon.', fix: 'add ; at the end of this line.' },
  })],
  [/Tests\.java:\d+: cannot find symbol\s*\n?\s*symbol:\s*\w+\s+([\w$]+)/, (m) => ({
    tests: true,
    zh: { title: `测试找不到 ${m[1]}`, what: `测试代码调用了 \`${m[1]}\`，但你的类里没有这个名字、这些参数的定义。`, fix: '对照题目检查方法名、大小写、参数个数和类型，以及它是不是 static。' },
    en: { title: `The tests cannot find ${m[1]}`, what: `The test code calls \`${m[1]}\`, which your class does not define with that name and those parameters.`, fix: 'check the method name, capitals, number and types of parameters, and whether it is static, against the question.' },
  })],
  [/cannot find symbol\s*\n?\s*symbol:\s*(\w+)\s+([\w$]+)/, (m) => ({
    zh: { title: `找不到 ${m[2]}`, what: `Java 找不到名叫 \`${m[2]}\` 的${{ variable: '变量', method: '方法', class: '类' }[m[1]] || '名字'}。常见原因：拼写或大小写不对（Java 区分大小写）、没有声明、或者它在别的花括号里声明、这里看不到。${m[1] === 'class' ? '如果它是 Scanner、ArrayList 这样的库类，文件开头需要 import，例如 `import java.util.Scanner;`。' : ''}`, fix: `检查 \`${m[2]}\` 的拼写和大小写，确认它在这里可见。` },
    en: { title: `Cannot find ${m[2]}`, what: `Java cannot find a ${m[1] || 'name'} called \`${m[2]}\`. Usually a spelling or capital-letter mistake (Java is case-sensitive), a missing declaration, or a declaration inside other braces that cannot be seen here.${m[1] === 'class' ? ' If it is a library class such as Scanner or ArrayList, the file needs an import at the top, for example `import java.util.Scanner;`.' : ''}`, fix: `check the spelling and capitals of \`${m[2]}\`, and that it is visible here.` },
  })],
  [/incompatible types: (.+) cannot be converted to (.+)/, (m) => ({
    zh: { title: '类型不匹配', what: `这里需要 ${m[2]}，给的却是 ${m[1]}。Java 不会自动在这两种类型之间转换。`, fix: '检查变量声明的类型和赋给它的值；需要时用 Integer.parseInt 或 String.valueOf 转换。' },
    en: { title: 'Types do not match', what: `This place needs ${m[2]} but gets ${m[1]}, and Java does not convert between them by itself.`, fix: 'check the declared type and the value; convert with Integer.parseInt or String.valueOf where needed.' },
  })],
  [/missing return statement/, () => ({
    zh: { title: '有的情况没有 return', what: '方法声明了返回类型，但有一条执行路径走到结尾也没有 return。', fix: '确认 if/else 的每个分支都有 return，或者在方法末尾补一个。' },
    en: { title: 'A path has no return', what: 'The method declares a return type, but some path reaches its end without a return.', fix: 'make sure every if/else branch returns, or add a return at the end.' },
  })],
  [/might not have been initialized/, () => ({
    zh: { title: '变量可能还没有赋值', what: '使用这个变量之前，至少有一条执行路径没有给它赋值。', fix: '声明时就给它一个初值。' },
    en: { title: 'A variable may not have a value yet', what: 'At least one path reaches this use without giving the variable a value.', fix: 'give it a starting value where it is declared.' },
  })],
  [/'([)\]}])' expected|reached end of file while parsing/, () => ({
    zh: { title: '括号没有配对', what: '打开的括号或花括号没有关上。', fix: '数一数 ( ) 和 { } 是否成对，补上缺的那个。' },
    en: { title: 'Brackets do not pair up', what: 'A bracket or brace is opened and never closed.', fix: 'count ( ) and { } pairs and add the missing one.' },
  })],
  [/class (\w+) is public, should be declared in a file named/, () => ({
    zh: { title: '公开类必须叫 Main', what: '这里的文件名是 Main.java，所以 public class 必须命名为 Main。', fix: '把 public class 的名字改成 Main。' },
    en: { title: 'The public class must be called Main', what: 'The file here is Main.java, so the public class must be named Main.', fix: 'rename the public class to Main.' },
  })],
  [/Uncaught exception/, () => ({
    runtime: true,
    zh: { title: '程序因为没有处理的异常而停止', what: '运行时抛出了异常，但没有 try/catch 接住它。这里的精简版 Java 不能显示是哪一种异常；最常见的是空引用（对 null 调用方法）和数组下标越界。', fix: '检查这两处；想看完整信息，请在自己电脑的 JDK 上运行。' },
    en: { title: 'The program stopped on an exception nobody caught', what: 'An exception was thrown and no try/catch handled it. The reduced Java here cannot say which one; the usual ones are calling a method on null and an array index out of bounds.', fix: 'check those two; run it on a real JDK to see the full message.' },
  })],
];

const lastPythonLine = (text) => { const all = [...text.matchAll(/File "main\.py", line (\d+)/g)]; return all.length ? Number(all[all.length - 1][1]) : null; };

/* result: what run() returned. ownLines: how many lines the reader wrote, when tests were appended after them */
export function explain(result, { language, lang = 'en', ownLines = Infinity } = {}) {
  if (!result || result.status === 'ok' || result.status === 'timeout' || result.status === 'unavailable') return null;
  const T = lang === 'zh' ? ZH : EN;
  const text = `${result.stderr || ''}`;
  let line = null;
  let rules = [];
  if (language === 'python') { line = lastPythonLine(text); rules = PYTHON; }
  if (language === 'c') { const m = /main\.c\((\d+)\)/.exec(text); line = m ? Number(m[1]) : null; rules = C_RULES; }
  let inTestFile = false;
  if (language === 'java') { const m = /(Main|Tests)\.java:(\d+):/.exec(text); line = m ? Number(m[2]) : null; inTestFile = m?.[1] === 'Tests'; rules = JAVA_RULES; }
  let picked = null;
  for (const [re, make] of rules) { const m = re.exec(text); if (m) { picked = make(m); break; } }
  if (!picked && !text.trim()) return null;
  const words = picked ? picked[lang === 'zh' ? 'zh' : 'en'] : (line ? T.fallback : T.fallbackNoLine);
  // nothing ran when compilation failed; a Python syntax error also stops the program before its first line
  const compiled = result.status !== 'compile' && !(language === 'python' && /^(SyntaxError|IndentationError|TabError)\b/m.test(text));
  const inTests = inTestFile || picked?.tests || (line && line > ownLines);
  const notes = [];
  if (inTests && !picked?.tests) notes.push(compiled ? T.inTests(line) : T.inTestsCompile(inTestFile ? null : line));
  else if (line && picked?.before && !inTests) notes.push(T.lineBefore(line));
  const own = line && !inTests ? line : null;
  return { line: own, where: own ? T.line(own) : '', title: words.title, what: words.what, fix: words.fix ? `${T.tryIt}${words.fix}` : '', notes };
}

/* the same explanation as a DOM node, for the reading pages and the practice pages */
export function explainNode(result, options) {
  const e = explain(result, options);
  if (!e) return null;
  const box = document.createElement('div');
  box.className = 'run-explain';
  const head = document.createElement('p');
  head.className = 'run-explain-title';
  head.textContent = e.where ? `${e.where} · ${e.title}` : e.title;
  box.append(head);
  for (const text of [e.what, ...e.notes, e.fix].filter(Boolean)) {
    const p = document.createElement('p');
    // `code` in the explanation shows as code
    text.split(/(`[^`]+`)/).forEach((part) => { if (/^`[^`]+`$/.test(part)) { const c = document.createElement('code'); c.textContent = part.slice(1, -1); p.append(c); } else p.append(part); });
    box.append(p);
  }
  return box;
}
