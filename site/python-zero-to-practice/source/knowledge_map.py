"""原创知识连接：关系及文字共用一个数据源；不依赖网络或图谱库。"""
from html import escape as esc
import json


def node(key, title, chapter, group, idea, example, memory, question, answer, pitfall):
    return dict(id=key, title=title, chapter=chapter, group=group, idea=idea,
                target=f'c{chapter:02d}', example=example, memory=memory,
                question=question, answer=answer, pitfall=pitfall)


GROUPS = ['开始与表达', '选择与重复', '组织与复用', '文件与质量', '项目与 AI']
NODES = [
    node('run','运行与执行顺序',1,0,'保存 .py 文件，交给 Python 从上到下执行；终端不是代码文件。','c01-example-01_04','先保存，再运行，再看输出。','修改代码后输出没变，先检查什么？','检查文件是否保存、终端运行的路径是否就是刚编辑的文件。','编辑器里的文字不会自动成为正在执行的程序。'),
    node('types','变量、类型与转换',2,0,'变量名引用值；类型决定允许的操作。输入得到字符串，要算术计算时显式转换。','c02-example-02_04','先问类型，再问数值。','字符串 "60" 加 "5"，与整数 60 加 5 有什么不同？','前者拼成 "605"，后者算出 65；int("60") 才得到整数。','0、空字符串、None 的含义不同，不能都当作缺失。'),
    node('strings','字符串清洗',3,0,'用 strip、split、join 组织文本；先决定清洗规则，再观察返回的新字符串。','c03-example-03_05','清洗有返回，接住才保留。','name.strip() 后 name 一定改变了吗？','没有；字符串不可变，通常需要 name = name.strip() 保存返回结果。','split() 的空白分词不等于模型 tokenizer；字符数量也不等于 token 数量。'),
    node('conditions','条件与边界',4,1,'把业务要求写成 True/False 条件，用 if 决定走哪条分支。','c04-example-04_05','先列边界，再写分支。','为什么合法的 0 分不能用 if score 排除？','0 的布尔值是假，但它仍是有效成绩；用 score is None 判断缺失，再检查范围。','条件能判断规则，不能证明信息真实。'),
    node('for','for 与累计',5,1,'逐项拿到元素，并把当前值合入累计状态；空输入意味着循环一次也不执行。','c05-example-05_02','每轮只看：旧状态、当前项、新状态。','total 从 0 开始，依次加 2、4、1，三轮后各是多少？','2、6、7；必须在循环前初始化，不能每轮都清零。','统计人数是加 1，统计分数总和是加分数。'),
    node('while','while 与停止条件',6,1,'在条件仍成立时重复；每轮更新状态，并安排成功、失败或预算耗尽的出口。','c06-example-06_07','条件、更新、出口，三个一起看。','重试三次仍失败，能把结果标成成功吗？','不能；次数只限制执行，必须独立记录是否完成任务。','break 只结束当前循环，结束循环不等于达到目标。'),
    node('lists','列表与顺序',7,2,'一个列表保存一批有顺序的数据，索引定位元素，append 增加一个元素。','c07-example-07_02','一批用列表，一项看索引。','把 [2, 3] append 到 [1]，结果是什么？','[1, [2, 3]]；若要逐个加入 2、3，使用 extend。','列表可以嵌套；外层长度不等于所有内层元素数之和。'),
    node('copy','共享对象与浅拷贝',7,2,'赋值改变名字指向；修改对象会影响指向它的其他名字。浅拷贝只新建外层容器。','c07-example-07_05','改绑名字与修改对象分开想。','a=[[1]]，b=a.copy()，b[0].append(2) 后 a 是什么？','[[1, 2]]；两个外层列表仍引用同一个内层列表。','复制外层列表不代表嵌套数据已经完全独立。'),
    node('dicts','字典与记录',8,2,'字典按字段名保存一条记录；列表中装字典，就得到一批结构一致的记录。','c08-example-08_03','一条用字段，一批保顺序。','一轮对话的 role/content，和多轮对话分别适合什么结构？','一轮可用字典，多轮可用列表保存这些字典；顺序由外层列表表达。','键存在不代表值的类型正确，也不代表内容可信。'),
    node('sets','集合与去重',8,2,'集合便于检查某值是否已出现；若要保留首次出现顺序，同时维护结果列表。','c08-example-08_06','seen 查重复，result 留顺序。','为什么只用 set(texts) 不能保证原输入顺序？','集合不提供输入顺序保证；按原列表遍历，首次出现时加入结果列表和 seen。','去重前是否先 strip，会改变哪些内容被视为同一条。'),
    node('functions','函数与 return',9,2,'把一个职责封装成函数：输入参数，处理数据，return 将结果交给调用者。','c09-example-09_02','参数进，返回出，调用处接。','只在函数里 print(5)，外面 result=f() 能得到 5 吗？','不能；没有显式 return 的函数返回 None。打印给人看，返回值供后续代码使用。','能显示结果，不表示后面的函数已经拿到可用数据。'),
    node('state','作用域与状态传递',9,2,'先明确值属于哪次调用；需要外层状态变化时，用参数传入并接住新的返回值。','c09-example-09_10','新状态返回后，还要赋值接住。','函数返回了新轮数，但外层轮数不变，可能缺了什么？','缺少 rounds = next_round(rounds) 这样的赋值；局部参数重新绑定不会替外层名字赋值。','可变对象的原地修改，与整数参数重新绑定行为不同。'),
    node('sorting','排序与推导式',10,2,'先会写普通循环，再读压缩写法；排序键表达比较规则，例如分数降序后学号升序。','c10-example-10_03','先写展开版，再读简写版。','成绩相同的时候怎样让排名可重复？','明确第二排序键，如学号；sorted(rows, key=lambda r: (-r["score"], r["student_id"]))。','list.sort() 修改原列表且返回 None；sorted() 返回新列表。'),
    node('modules','模块与环境',11,3,'import 复用模块中的定义；先分清标准库与第三方包，再确认运行脚本所用的解释器。','c11-example-11_05','解释器选对，导入才对路。','为什么导入模块时不应该自动运行整个命令行程序？','模块顶层会执行；把命令行启动放进 if __name__ == "__main__":，才能安全复用函数。','不要把自己的文件命名成 json.py 等常用标准库名，避免遮住真正模块。'),
    node('files','路径与文件',12,3,'路径用于定位文件，with 管理打开与关闭；用明确编码把字节转换成文本。','c12-example-12_06','路径找文件，编码读文字。','相同相对路径为什么从另一个终端目录运行会找错文件？','相对路径通常相对于当前工作目录；可用 Path(__file__).resolve().parent 定位脚本目录。','文件存在不代表内容格式或业务字段正确。'),
    node('formats','CSV / JSON / JSONL',12,3,'解析器把文本变成 Python 容器。CSV 字段默认仍是字符串；JSONL 每行分别解析。','c12-example-12_05','先解析格式，再检查字段。','JSON 解析成功，能直接认定 score 是 0—100 的整数吗？','不能；还要检查结构、键、值的类型与范围。','CSV 记录可以跨物理行；记录序号与文本行号不是同一个东西。'),
    node('validation','异常与数据校验',13,3,'针对转换错误处理具体异常；对可解析的数据再检查字段、范围，并记录拒绝原因。','c13-example-13_09','能读、能解析、合约定，逐层检查。','"abc"、"101"、"0" 作为成绩输入分别怎样处理？','abc 转换失败；101 转换成功但超范围；0 转换且校验通过，必须保留。','宽泛捕获后静默跳过，会掩盖程序错误；不要把所有异常都当坏数据。'),
    node('tests','断言与边界测试',13,3,'用可手算的输入核对结果，再覆盖空输入、零值、错误类型和重复值。','c13-example-13_04','先手算，再断言，再换边界。','函数处理了 [60, 80]，还应该优先测试什么？','空列表、0、刚好及格的 60、错误输入；空列表不应除以零。','少量测试通过只支持这些案例，不能证明所有输入都正确。'),
    node('classes','类与实例状态',14,4,'类把状态和操作放在一起；每个实例应该拥有属于自己的可变数据。','c14-example-14_06','类是定义，实例各有状态。','两个会话为什么不能共用同一个可变消息列表？','对一个会话追加消息会污染另一个会话；应在每次初始化时创建新列表。','学会函数后再学类；小任务可以先用函数，不必强行套类。'),
    node('generators','迭代器与生成器',15,4,'用 next 逐项取值；yield 暂停执行并交出一个值，下次从暂停处继续。','c15-example-15_06','return 结束，yield 暂停。','一个流式片段是否一定等于一个 token？','不一定；片段可能是若干字符或多个 token 的显示结果，取决于接口。','这里的流式文本是固定片段模拟，不会产生模型推理。'),
    node('dataset','AI 数据与批次',16,4,'清洗记录、保持字段对齐、划分数据、建立词表，再检查二维形状和评估分母。','c16-example-16_02','先分清样本，再保持对齐。','为什么不能分别打乱文本和标签？','会破坏一一对应；应将一条记录整体移动和划分。','只在训练集建立词表；本章简化编码不是生产模型的 tokenizer。'),
    node('agent','Agent 工具流程',16,4,'任务进入流程，规则选择工具，校验参数，调用函数，观察返回值，再判断是否结束。','c16-example-16_07','选工具、查参数、看观察、判完成。','工具调用没有报错，能说明用户问题答对了吗？','不能；还需核对返回内容是否满足原任务。执行成功与任务正确是两层判断。','本课程用规则模拟决策。真实模型的输出还可能有格式错误或事实错误。'),
    node('project','综合项目与验收',17,4,'把需求拆成读取、清洗、统计、输出四层；每层先用小样例验证，再连接完整流程。','c17-02_score_report','一层一个职责，一层一个手算样例。','成绩项目应该先处理合法性还是先把学号记入 seen？','先通过字段、转换和范围校验，再登记学号；否则第一条坏记录会错误占用该学号。','项目保留每个学号的第一条有效记录；这是一项业务约定，不是 Python 自带规则。'),
    node('next','通向深度学习与大模型',18,4,'第一阶段熟练后，再学数组与张量、线性代数、训练评估、tokenizer、模型调用和工具接口。','c18','Python 基础是起点，模型知识要另学。','运行完规则 Agent，是否已经会训练大模型？','还没有；还需数学、数据与张量、模型训练和评估。本课程提供理解后续代码的基础。','此处是后续学习路标；当前课程没有实现真实模型训练或调用。'),
]

# kind=learn 表示本课程建议的学习联系；不是语言的严格依赖声明。
EDGES = []
def edge(a,b,why,kind='learn'):
    EDGES.append(dict(source=a,target=b,why=why,kind=kind))

for a,b,why in [
 ('run','types','先能运行并观察值，才能核对变量和类型。'),
 ('types','strings','字符串也是一种类型；清洗方法的结果仍是字符串。'),
 ('types','conditions','比较前先区分数值、字符串和缺失值。'),
 ('conditions','for','每轮可用条件决定是否累计当前项。'),
 ('conditions','while','while 要反复检查一个布尔条件。'),
 ('types','lists','列表把多个值放在有顺序的容器中。'),
 ('lists','copy','列表可变，才需要追踪多个名字是否共享它。'),
 ('lists','dicts','先看一批元素，再用字典描述每条记录的字段。'),
 ('for','sets','遍历输入并查 seen，可以保留首次出现顺序。'),
 ('dicts','functions','记录作为参数传入，结果作为字典返回；函数也可处理简单数值。'),
 ('functions','state','调用之间怎样保留新状态，需要理解参数和返回值。'),
 ('copy','state','函数可能修改共享对象，也可能只改绑局部名字。'),
 ('for','sorting','先能展开逐项处理，再读推导式与排序键。'),
 ('functions','modules','把可复用函数放进模块，并把启动逻辑隔开。'),
 ('modules','files','用标准库 pathlib 管理路径，学习 with 管理文件。'),
 ('files','formats','读到文本后，选择与文件约定相符的解析器。'),
 ('dicts','formats','JSON 对象和数组可对应 Python 字典和列表。'),
 ('formats','validation','可解析只是第一层，还要验证数据结构与含义。'),
 ('conditions','validation','字段存在、值类型和范围，都需要明确的条件。'),
 ('functions','tests','一个函数职责清楚，才能独立准备输入和预期返回值。'),
 ('validation','tests','把每类拒绝原因转成能重复运行的边界案例。'),
 ('state','classes','把属于一个会话的状态保存在该实例上。'),
 ('for','generators','理解逐项消费后，再理解按需生产一项的 yield。'),
 ('functions','generators','比较函数的 return 结束与 yield 暂停。'),
 ('sets','dataset','清洗后检查重复样本，避免无意重复统计。'),
 ('validation','dataset','无效记录先被识别，再进入划分与编码。'),
 ('functions','agent','工具首先是有明确参数和返回值的可调用函数。'),
 ('validation','agent','在执行工具前检查参数，执行后检查观察结果。'),
 ('while','agent','限定最多执行多少步，并保留独立完成状态。'),
 ('tests','project','每层的预期结果组成最终验收条件。'),
 ('sorting','project','把有效成绩整理成有稳定规则的排名。'),
 ('files','project','项目从输入文件读取，并把结果写成报告。'),
 ('dataset','next','张量、训练与评估将接在数据准备之后。'),
 ('agent','next','接入真实模型后，仍需工具契约、错误处理与任务评估。'),
 ('classes','next','后续模型和数据集 API 常把操作组织为类与实例。'),
]: edge(a,b,why)
for a,b,why in [
 ('strings','formats','普通 split(",") 不处理带引号逗号；CSV 要交给 csv 解析器。'),
 ('copy','classes','浅拷贝和会话串线都要追踪：谁引用了哪个可变对象？'),
 ('for','generators','for 负责取值；生成器负责按需提供值，不要求先装满列表。'),
 ('functions','sorting','print、list.sort 与显式 return 的返回值要分别核对。'),
 ('state','while','状态若没有更新，循环可能停不下来。'),
 ('formats','agent','工具参数格式合法不等于工具已执行，更不等于任务正确。'),
 ('strings','dataset','字符数、空白分词数、token 数不可混用。'),
]: edge(a,b,why,'connect')

ROUTES = [
 dict(id='start',title='从零打基础',goal='按顺序学会运行、表达、选择、重复，再组织数据和函数。',nodes=['run','types','strings','conditions','for','while','lists','dicts','functions']),
 dict(id='scores',title='做成绩分析',goal='主线是把文件中的字符串变成通过校验的记录，再统计并验收；细节见下方场景链路。',nodes=['types','strings','conditions','for','dicts','functions','files','formats','validation','tests','project']),
 dict(id='data',title='整理 AI 数据',goal='先练文本规则和去重，随后验证记录，保持文本与标签对齐；暂不训练模型。',nodes=['strings','lists','sets','dicts','files','formats','validation','dataset']),
 dict(id='agent',title='理解 Agent',goal='先理解数据结构、工具参数和返回值，再把有限循环连接起来；这里使用规则决策。',nodes=['conditions','while','dicts','functions','state','validation','agent']),
 dict(id='future',title='为大模型做准备',goal='函数、对象、迭代和数据是后续代码的入口；数学、张量与模型训练要在第二阶段补学。',nodes=['functions','state','classes','generators','dataset','next']),
]

SCENARIOS = [
 dict(id='scores',title='成绩表 → 清洗 → 报告',intro='用原成绩项目的字段约定来拆解。先做能手算的小数据，再运行项目中的完整文件。下面的表是数据追踪，不是程序执行器。',target='c17-02_score_report',steps=[
  ('读文件','student_id,name,score 的 CSV 文本','DictReader 按表头解析','{"student_id": "S1", "name": " 小林 ", "score": "60"}',['files','formats','dicts']),
  ('清洗一条','name=" 小林 "，score="60"','strip 清理；int 转换；检查 0 ≤ score ≤ 100','{"student_id": "S1", "name": "小林", "score": 60}',['strings','types','conditions','validation']),
  ('收集与去重','一条无效 S2/abc，随后一条有效 S2/0','无效条记错误；只有有效且未见过的学号才加入 seen','S2 的 0 分保留；seen 不被前面的坏记录占用',['for','lists','sets']),
  ('统计小样例','有效分数 [60, 0, 90]','count=3，total=150，passed=2','mean=50.0，pass_rate=2/3；空列表时均值和及格率为 None',['functions','for','conditions']),
  ('排名与验收','有效记录和错误列表','按分数降序、学号升序排名；写报告；对照手算','JSON 报告与错误 CSV；先确认有效数、均值、比例再读排名',['sorting','files','tests']),
 ],question='第一条 S2 分数是 abc，第二条 S2 分数是 0。为什么不能在字段校验前就 seen.add("S2")？',answer='第一条无效，不应占用 S2。提前登记会让第二条合法零分被误判重复。按项目约定，seen 只记录已保留的有效学号。扩展：两条都有效时保留第一条；若需求改成保留最新一条，就必须修改规则和测试。'),
 dict(id='agent',title='任务 → 工具 → 观察 → 判断',intro='沿用第 16 章的规则工具示例。每一步的中间值都应可以查看；真实模型只会让决策来源更复杂，不会替你自动完成校验。',target='c16-example-16_07',steps=[
  ('描述任务','用户想查询指定条目的资料','保存任务文本和明确的目标','任务与目标；尚未执行工具',['strings','dicts']),
  ('决定动作','任务与当前状态','规则选出工具名和参数','一个动作字典；它只是执行请求',['conditions','dicts']),
  ('检查并执行','工具名、参数字典','检查工具是否存在、参数是否合约定，再调用函数','返回一个值或明确的失败；工具返回值是观察数据',['validation','functions']),
  ('保存观察','本轮工具结果','将结果放入轨迹；更新轮数和下一步状态','新轨迹、新轮数；参数改绑需要外层接住返回值',['lists','state']),
  ('判断结束','目标、观察和剩余预算','核对结果是否回答原问题；失败时决定继续还是停止','完成 / 未完成；达到次数上限不自动变成完成',['while','tests','agent']),
 ],question='工具返回 {"ok": True, "text": "未找到相关资料"}，仅凭 ok 能宣布任务正确吗？',answer='不能。ok 可能只说明工具顺利运行；还要检查内容是否满足任务。试着把失败原因拆成参数错误、工具执行失败、结果不满足任务，分别说明该在哪一步处理。这里没有调用真实模型。'),
]

DATA = dict(nodes=NODES, edges=EDGES, routes=ROUTES, scenarios=SCENARIOS, groups=GROUPS)
BY_ID = {n['id']: n for n in NODES}


def map_link(key, label=None):
    return f'<a href="#c00-map-{key}" data-map-node="{key}">{esc(label or BY_ID[key]["title"])}</a>'


def render_map():
    groups=''.join('<section><h4>'+esc(title)+'</h4><div class="map-pills">'+''.join(map_link(n['id']) for n in NODES if n['group']==i)+'</div></section>' for i,title in enumerate(GROUPS))
    routes=''.join(f'<button type="button" data-map-route="{r["id"]}" aria-pressed="false">{esc(r["title"])}</button>' for r in ROUTES)
    anchors=''.join(f'<span id="c00-map-{n["id"]}" hidden></span>' for n in NODES)
    scenarios=[]
    for s in SCENARIOS:
        steps=[]
        for i,(title,inp,action,out,keys) in enumerate(s['steps'],1):
            steps.append(f'<li><h5>{i:02d} · {esc(title)}</h5><p><b>输入：</b><code>{esc(inp)}</code></p><p><b>处理：</b>{esc(action)}</p><p><b>输出：</b><code>{esc(out)}</code></p><div class="map-pills">'+''.join(map_link(k) for k in keys)+'</div></li>')
        scenarios.append(f'<details class="map-scenario" id="c00-scenario-{s["id"]}"><summary>{esc(s["title"])}</summary><p>{esc(s["intro"])}</p><ol class="map-flow">'+''.join(steps)+f'</ol><p><b>迁移自测：</b>{esc(s["question"])}</p><details><summary>先解释，再对照解析</summary><p>{esc(s["answer"])}</p></details><p><a href="#{s["target"]}">打开对应示例或项目 →</a></p></details>')
    payload=json.dumps(DATA,ensure_ascii=False).replace('</','<\\/')
    return f'''<section class="knowledge-map" id="c00-knowledge-map" aria-labelledby="map-title">
<div class="eyebrow">KNOWLEDGE CONNECTIONS · 从知识到用途</div><h3 id="map-title">Python 知识图谱</h3>
<p>遇到新语法时，问三句话：它接在哪个知识后面？现在解决什么问题？以后用在哪里？下面把这三件事连起来。</p>
<p class="muted">实线箭头表示本课程建议的学习联系，不是唯一学习顺序；虚线联想表示可相互对照。场景链路中的箭头才表示数据处理先后。点击节点不会自动勾选学习进度。</p>
<div class="map-routes" role="group" aria-label="选择学习目标">{routes}</div><div id="map-route-detail" aria-live="polite"></div>
<details class="map-catalog"><summary>展开全部 {len(NODES)} 个知识点 · 按主题查找</summary><label for="map-search">查找知识点、问题或联想词</label><input id="map-search" type="search" placeholder="例如：return、零分、token、浅拷贝"><p id="map-search-status" role="status"></p>{groups}</details>
{anchors}<div id="map-focus" tabindex="-1"><h4 id="map-focus-title">先选择一个知识点</h4><div class="map-graph" id="map-graph"><svg id="map-lines" aria-hidden="true" focusable="false"></svg><div id="map-before" class="map-column"></div><div id="map-current" class="map-column"></div><div id="map-after" class="map-column"></div></div><div id="map-detail"></div></div>
<h4>把知识用在同一个场景里</h4><p>沿着输入 → 处理 → 输出看数据怎样变化，再点击知识点补上卡住的环节。先口头预测下一步，再运行教材中的 Python。</p>{''.join(scenarios)}
<p><a href="知识图谱.md" download>保存完整文字图谱与联想自测 ↓</a> · 图谱无需联网，不保存额外个人数据。</p>
<script type="application/json" id="knowledge-data">{payload}</script></section>'''


def chapter_connections(number):
    nodes=[n for n in NODES if n['chapter']==number]
    if not nodes: return ''
    return '<aside class="chapter-connections" aria-label="本章知识连接"><b>本章在图谱中的位置</b><div class="map-pills">'+''.join(map_link(n['id']) for n in nodes)+'</div><p>点击查看前置知识、后续用途和易混点。完成自测后，再回本章运行示例。</p></aside>'


def map_markdown():
    lines=['# Python 知识图谱','本图谱串联本课程的知识和用途。学习联系是建议顺序，不是语言的严格依赖；联想不表示依赖。场景中的顺序表示数据处理步骤。图谱不代替实际练习，也不会自动判断是否掌握。','## 五条目标路线']
    for r in ROUTES:
        lines += ['### '+r['title'],r['goal'],' → '.join(BY_ID[k]['title'] for k in r['nodes'])]
    for n in NODES:
        lines += ['## '+n['title'],f'第 {n["chapter"]:02d} 章；网页锚点：#{n["example"]}',n['idea'],'记忆：'+n['memory'],'易混点：'+n['pitfall']]
        for rel in EDGES:
            if rel['target']==n['id'] and rel['kind']=='learn': lines += ['- 建议先会 '+BY_ID[rel['source']]['title']+'：'+rel['why']]
            if rel['source']==n['id'] and rel['kind']=='learn': lines += ['- 后续用途 '+BY_ID[rel['target']]['title']+'：'+rel['why']]
            if rel['kind']=='connect' and n['id'] in (rel['source'],rel['target']): lines += ['- 联想对照：'+rel['why']]
        lines += ['自测：'+n['question'],'解析：'+n['answer']]
    for s in SCENARIOS:
        lines += ['## '+s['title'],s['intro']]
        for title,inp,action,out,keys in s['steps']:
            lines += ['### '+title,'输入：'+inp,'处理：'+action,'输出：'+out,'联系：'+'、'.join(BY_ID[k]['title'] for k in keys)]
        lines += ['迁移自测：'+s['question'],'解析：'+s['answer']]
    return '\n\n'.join(lines)+'\n'
