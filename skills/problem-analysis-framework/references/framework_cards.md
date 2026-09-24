# 框架卡字段规范与提取方法

框架卡是"书 → 原子技能"编译流程的中间产物。本文件定义卡的字段标准与提取方法，供新增框架时使用。

## 1. 字段规范

每张框架卡必须包含以下 17 个字段。字段名使用英文字段键（snake_case），渲染后的卡片使用中文标签。

| 字段键 | 中文标签 | 必填 | 说明 |
|---|---|---|---|
| name | 框架名 | 是 | 唯一标识，snake_case |
| source | 来源 | 是 | 出处书籍，可多个 |
| one_line_definition | 一句话定义 | 是 | 一句话说清框架要做什么 |
| when_to_use | 适用场景 | 是 | 列表，可判定的触发条件 |
| when_not_to_use | 不适用场景 | 是 | 列表，防止误用 |
| goal | 目标 | 是 | 使用后应得到的改变 |
| inputs | 输入 | 是 | 列表，标注类型与是否必填 |
| outputs | 输出 | 是 | 列表，可交付物 |
| steps | 核心步骤 | 是 | 列表，有序，不可合并 |
| decision_rules | 判断规则 | 是 | 列表，"如果……则……" |
| question_checklist | 提问清单 | 是 | 列表，执行中要问的问题 |
| common_tools | 常用工具 | 否 | 列表，配套工具 |
| common_mistakes | 常见错误 | 是 | 列表 |
| quality_checks | 检查清单 | 是 | 列表，输出前自检项 |
| positive_example | 正例 | 是 | 输入 → 输出 |
| negative_example | 反例 | 是 | 应避免的输出 |
| source_location | 原文位置 | 否 | 章节或页码，便于回溯 |

## 2. 提取方法

从书里提取时重点抓四类东西：

- **显性步骤**：书里明确写的流程，如"定义问题 → 分解 → 排序 → 分析"，直接落到 `steps`。
- **隐性规则**：作者的判断经验，转成"如果……则……"，落到 `decision_rules`。
- **案例**：书中的正反案例，转成 `positive_example` / `negative_example`。
- **检查清单**：作者的验收标准，转成 `quality_checks`。

约束：

1. 不复制大段原文，用自己的话重述，在 `source_location` 标注来源。
2. `when_not_to_use` 必须非空，否则框架容易被滥用。
3. `quality_checks` 必须可判定（可回答是 / 否），不写"分析要深刻"这类主观项。
4. 步骤必须有序且不可合并，合并后要重新编号。

## 3. 工具链

用 `scripts/framework_card_tool.py` 完成卡的生成、校验与渲染（路径相对本技能根目录）：

```bash
# 生成一张空白卡模板
python scripts/framework_card_tool.py scaffold --card-name problem_reframing --output ./problem_reframing.yaml

# 校验字段是否齐全、必填项是否为空
python scripts/framework_card_tool.py validate --card-path ./problem_reframing.yaml

# 批量校验目录下所有卡
python scripts/framework_card_tool.py validate --card-path ./cards/

# 渲染为 Markdown 卡片
python scripts/framework_card_tool.py render --card-path ./problem_reframing.yaml --output ./problem_reframing.md
```

校验失败时脚本返回非零退出码，并列出缺失或为空的字段。

## 4. 图例：YAML 卡格式

```yaml
name: problem_reframing
source: 《你的灯亮着吗？》
one_line_definition: 在解决问题前先澄清和重构问题，避免解决错误的问题。
when_to_use:
  - 用户直接提出解决方案
  - 多方对问题定义不一致
when_not_to_use:
  - 问题已明确定义且只需执行
goal: 产出一个不含解决方案、有成功标准、有归属的问题陈述。
inputs:
  - initial_problem（string，必填）
  - stakeholders（list，选填）
outputs:
  - problem_statement
steps:
  - 澄清"这是谁的问题"
decision_rules:
  - 如果用户说"我要做 X"，则追问"X 要解决什么"
question_checklist:
  - 现状与理想状态的差距是什么
common_tools:
  - 利益相关者矩阵
common_mistakes:
  - 把用户说的解决方案当成问题本身
quality_checks:
  - 问题陈述不含解决方案
positive_example: 输入"我需要一个更好的 CRM"，输出"销售团队跟进效率低，导致线索转化差"
negative_example: 输出"建议引入某某 CRM 系统"——这是解决方案，不是问题陈述
source_location: 第 2 章
```

## 5. 从框架卡编译出原子技能

一张卡对应一个独立子技能，编译规则：

| 卡的字段 | 去向 |
|---|---|
| name | 子技能目录名与 frontmatter `name`，下划线换连字符（`problem_reframing` → `problem-reframing`） |
| one_line_definition | frontmatter `description` 的开头，并补上触发场景与适用范围 |
| when_to_use / when_not_to_use | SKILL.md 的"何时使用 / 何时不使用" |
| inputs / outputs | SKILL.md 的同名表格 |
| steps | SKILL.md 的"执行步骤"，按序编号 |
| decision_rules | SKILL.md 的"判断规则"表 |
| question_checklist / common_tools / common_mistakes | SKILL.md 的对应章节 |
| quality_checks | SKILL.md 的"质量检查"清单 |
| positive_example / negative_example | SKILL.md 的"正例 / 反例" |
| source | SKILL.md 的"来源" |

编译后还需补两样卡里没有的东西：

1. **前置条件**：本技能开始前必须先完成什么（例如 `mece-decomposition` 的前置是已通过检查的问题陈述）。
2. **测试案例**：从正反例与 `decision_rules` 扩写出输入、期望行为、禁止行为三列表。

## 6. 版本化

- 框架卡与对应原子技能的版本必须同步，两者内容不一致时以框架卡为源、重新编译。
- 修改后更新版本并在卡头记录变更原因。
- 规则调整需同步更新对应原子技能的"测试案例"章节与本技能 `test_cases.md` 中的路由测试。
