# 问题分析框架 Skills

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Skills](https://img.shields.io/badge/skills-7-orange.svg)](#技能清单)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-3776AB.svg?logo=python&logoColor=white)](#开发)
[![Stars](https://img.shields.io/github/stars/vax521/problem-analysis-skills.svg)](https://github.com/vax521/problem-analysis-skills/stargazers)
[![Last commit](https://img.shields.io/github/last-commit/vax521/problem-analysis-skills.svg)](https://github.com/vax521/problem-analysis-skills/commits/main)
[![validate-skills](https://github.com/vax521/problem-analysis-skills/actions/workflows/validate-skills.yml/badge.svg?branch=main)](https://github.com/vax521/problem-analysis-skills/actions/workflows/validate-skills.yml)

把书里的问题分析方法论，编译成 AI Agent 可以直接调用的技能包。

[English](#english) · [许可证](#许可证) · [贡献指南](CONTRIBUTING.md)

## 这是什么

多数人不是不会分析问题，而是不知道该用哪套方法。本仓库把 12 本经典著作中的方法论
拆成 7 个可独立触发的技能：入口技能按用户意图路由，原子技能各自承载一套可执行、
可校验的协议。

核心思路是**知识编译**，而不是让 Agent 读整本书：

```
书籍 → 框架卡 → Skill Spec → Agent 工作流 → 测试迭代
```

每个技能都写清五件事：何时使用、输入什么、怎么做、输出什么、如何自检。所有技能
都带判断规则（如果……则……）、检查清单和正反例，Agent 在输出前必须逐条核对。

## 技能清单

| 技能 | 类型 | 一句话说明 | 适用场景 |
|---|---|---|---|
| [`problem-analysis-framework`](skills/problem-analysis-framework/SKILL.md) | 路由入口 | 按意图路由到原子技能，约束组合顺序与全局质量检查 | 拿不准该用哪套方法时 |
| [`problem-reframing`](skills/problem-reframing/SKILL.md) | 定义类 | 在解决问题前先澄清和重构问题 | 问题模糊、直接要方案 |
| [`mece-decomposition`](skills/mece-decomposition/SKILL.md) | 分解类 | 不重叠、不遗漏地拆解，再排序找杠杆点 | 利润下滑、增长停滞 |
| [`five-whys`](skills/five-whys/SKILL.md) | 分析类 | 沿单条因果链追问到可干预的根因 | 故障复盘、指标异常 |
| [`system-loops`](skills/system-loops/SKILL.md) | 分析类 | 用因果回路识别结构、延迟与杠杆点 | 问题反复发作、长期动态 |
| [`pyramid-expression`](skills/pyramid-expression/SKILL.md) | 表达类 | 结论先行，用 SCQA 组织论据 | 向上汇报、方案评审 |
| [`mckinsey-7step`](skills/mckinsey-7step/SKILL.md) | 复合类 | 端到端调度上述原子技能的完整流程 | 复杂项目的完整咨询流程 |

同时命中多个技能时，按「定义 → 分解 → 分析 → 综合 → 表达」串联执行，不是二选一。

## 安装

技能本体在仓库根目录的 `skills/` 下，每个子目录是一个独立技能。这个布局是
[skills CLI](https://github.com/vercel-labs/skills) 的标准容器目录，所以可以直接用
`npx skills` 安装，也可以手动复制。

### 方式一：npx skills add（推荐）

```bash
# 装到当前项目，写入 ./.codebuddy/skills/，可随项目提交给协作者
npx skills add vax521/problem-analysis-skills

# 装到用户目录，所有项目都可用
npx skills add vax521/problem-analysis-skills -g

# 跳过交互，只装给 CodeBuddy
npx skills add vax521/problem-analysis-skills -a codebuddy -y

# 先列出仓库里有哪些技能，不安装
npx skills add vax521/problem-analysis-skills --list
```

CLI 会自动探测本机已安装的 agent 并让你选择目标；默认用符号链接安装（改 `--copy`
可改为复制）。`-a` 可取 `codebuddy`、`claude-code`、`cursor`、`codex` 等。

> 不要用 `-s` 只装单个技能。`problem-analysis-framework` 靠技能名路由到其余 6 个，
> 缺任何一个都会让路由失效，请整套安装。

### 方式二：手动复制

技能目录可以直接复制。装到用户级（所有项目可用）：

- macOS / Linux：`~/.codebuddy/skills/`
- Windows：`C:\Users\<你的用户名>\.codebuddy\skills\`

```bash
git clone https://github.com/vax521/problem-analysis-skills.git
cp -r problem-analysis-skills/skills/* ~/.codebuddy/skills/
```

Windows PowerShell：

```powershell
git clone https://github.com/vax521/problem-analysis-skills.git
Copy-Item .\problem-analysis-skills\skills\* "$env:USERPROFILE\.codebuddy\skills\" -Recurse
```

装到项目级则复制到该项目的 `.codebuddy/skills/` 下。

### 方式三：下载 zip 包

从 [Releases](https://github.com/vax521/problem-analysis-skills/releases) 下载对应技能的 zip，
解压到用户技能目录。zip 内部顶层目录即技能名，不要改动层级。

> 通过 `npx skills add` 安装后，项目根目录会生成 `skills-lock.json` 记录版本，建议一并提交。

## 使用

用自然语言描述问题即可触发，例如：

| 说法 | 触发技能 |
|---|---|
| 「我要做个 App」 | `problem-reframing` 先追问这个 App 要解决谁的什么问题 |
| 「利润下滑了，帮我拆一下」 | `mece-decomposition` 拆收入与成本并排序 |
| 「服务昨天挂了 2 小时，为什么」 | `five-whys` 逐层追问并要求每层带证据 |
| 「为什么这个问题反复出现」 | `system-loops` 画出反馈回路找杠杆点 |
| 「帮我把这个方案讲给老板」 | `pyramid-expression` 结论先行 + SCQA |
| 「帮我完整分析一个复杂项目」 | `mckinsey-7step` 端到端流程 |

## 仓库结构

```text
.
├── skills/                       # 技能本体，7 个技能各占一个目录
│   ├── problem-analysis-framework/
│   │   ├── SKILL.md              # 路由表、组合规则、全局质量检查
│   │   ├── references/           # 框架图谱、框架卡规范、测试用例
│   │   └── scripts/
│   │       └── framework_card_tool.py
│   ├── problem-reframing/SKILL.md
│   ├── mece-decomposition/SKILL.md
│   ├── five-whys/SKILL.md
│   ├── system-loops/SKILL.md
│   ├── pyramid-expression/SKILL.md
│   └── mckinsey-7step/SKILL.md
├── scripts/build_dist.py         # 校验并打包
├── dist/                         # 打包产物，不入库
└── 问题分析框架skill创建指南.md    # 设计笔记：从书到技能的编译流程
```

## 开发

校验所有技能格式：

```bash
python scripts/build_dist.py --check
```

校验并生成 `dist/*.zip`：

```bash
python scripts/build_dist.py
```

新增一个框架，按四步走：

1. 用框架卡工具生成模板并填写 17 个字段：

   ```bash
   python skills/problem-analysis-framework/scripts/framework_card_tool.py \
     scaffold --card-name problem_reframing --output cards/problem_reframing.yaml
   ```

2. 把卡片编译成 `skills/<技能名>/SKILL.md`，字段规范见
   [framework_cards.md](skills/problem-analysis-framework/references/framework_cards.md)。
3. 在 `problem-analysis-framework` 的路由表与框架图谱中注册新技能。
4. 在 `references/test_cases.md` 补测试案例，然后跑一次打包脚本。

## 贡献

见 [CONTRIBUTING.md](CONTRIBUTING.md)。欢迎提交新的框架、修订判断规则、补充反例与测试案例。

## 来源与致谢

本仓库的方法论提炼自下列著作，内容为结构化重述，不含原文摘录。框架的著作权归原作者与出版社：

- 问题定义与重构：《你的灯亮着吗？》《你问对问题了吗？》《问题即答案》
- 系统化流程：《所有问题，七步解决》《拆解一切问题》《麦肯锡经典工作法》
- 分析工具：《金字塔原理》《麦肯锡问题分析与解决技巧》
- 系统思考：《系统之美》《系统化思维导论》
- 思维模型：《思考的框架》《思考，快与慢》

## 许可证

[MIT](LICENSE)。可自由用于商业与非商业场景，请保留版权声明。

## English

A collection of Agent Skills that compile problem-analysis methodologies from classic
books into executable protocols: reframe the problem, decompose it MECE, drill to root
cause, model system loops, and express conclusions pyramid-style.

Each skill declares when to use it, its inputs and outputs, ordered steps, decision
rules, quality checks, and worked examples. Skills live under `skills/`, one directory
per skill.

Install with the skills CLI — `skills/` is its standard container layout:

```bash
npx skills add vax521/problem-analysis-skills          # project scope
npx skills add vax521/problem-analysis-skills -g       # user scope
npx skills add vax521/problem-analysis-skills --list   # list without installing
```

Or copy the folders manually into `~/.codebuddy/skills/` (user scope) or
`.codebuddy/skills/` (project scope).

Note that `problem-analysis-framework` routes to the other six skills by name, so
install the whole set rather than a single folder.

Validate and package: `python scripts/build_dist.py --check`. Licensed under MIT.
