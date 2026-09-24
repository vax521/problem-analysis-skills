# 框架图谱与选型

本文件是框架集合的索引，框架本体保存在各原子技能中，此处不重复。

## 框架清单与承载位置

| 框架名 | 原子技能 | 类型 | 适用问题特征 | 主要输出 |
|---|---|---|---|---|
| problem_reframing | `problem-reframing` | 定义类 | 模糊、无成功标准、直接要方案 | 问题陈述、成功标准、归属 |
| mece_decomposition | `mece-decomposition` | 分解类 | 复杂、多变量、需分工 | 逻辑树、优先级、分析计划 |
| five_whys | `five-whys` | 分析类 | 单一因果链、异常、复盘 | 因果链、根因、干预动作 |
| system_loops | `system-loops` | 分析类 | 反复出现、有反馈、长期动态 | 回路图、延迟、杠杆点 |
| pyramid_expression | `pyramid-expression` | 表达类 | 需说服、需汇报 | 结论、SCQA 开场、论据 |
| mckinsey_7step | `mckinsey-7step` | 复合类 | 端到端复杂项目 | 七步全交付物 |

框架卡字段名（snake_case）与原子技能名（hyphen-case）一一对应，转换规则为下划线换连字符。

## 选型对照

| 问题特征 | 首选 | 备选 |
|---|---|---|
| 问题模糊 | `problem-reframing` | `mckinsey-7step` |
| 问题复杂 | `mece-decomposition` | `mckinsey-7step` |
| 需要找根因 | `five-whys` | `mece-decomposition` |
| 长期动态 | `system-loops` | — |
| 需要说服别人 | `pyramid-expression` | — |
| 个人重大决策 | `problem-reframing` + `mece-decomposition` | `system-loops`（看二阶影响） |
| 需要完整流程 | `mckinsey-7step` | — |

## 应用场景映射

| 场景 | 典型问题 | 常用组合 |
|---|---|---|
| 商业与咨询 | 利润下滑、增长停滞、市场进入 | `mece-decomposition` + `pyramid-expression` |
| 产品与运营 | 需求模糊、用户流失 | `problem-reframing` + `five-whys` |
| 战略与组织 | 转型、组织调整、跨部门推不动 | `system-loops` + `mece-decomposition` |
| 个人决策 | 选 offer、转行、重大投资 | `problem-reframing` + `mece-decomposition` |
| 沟通汇报 | 方案评审、向上汇报 | `pyramid-expression` |
| 学术研究 | 选题、文献综述、论证评估 | `problem-reframing` + `five-whys` |
| 公共政策 | 拥堵、环保、公共卫生 | `system-loops` |
| 创新与创业 | 新产品方向、商业模式 | `problem-reframing` + `mece-decomposition` |
| 团队冲突 | 立场分歧、责任推诿 | `problem-reframing` + `system-loops` |
| 风险与危机 | 风险评估、应急预案、复盘 | `five-whys` + `system-loops` |

## 框架间关系

- `problem-reframing` 是所有其他框架的前置步骤；未通过其质量检查时不要进入下一框架。
- `mece-decomposition` 负责"切得对"，`five-whys` / `system-loops` 负责"看得深"，二者常串联使用。
- `pyramid-expression` 是出口框架，任何分析最终都应经过它组织表达。
- `mckinsey-7step` 是容器，按顺序调度上述五个原子框架。

## 组合规则

1. 按"定义 → 分解 → 分析 → 综合 → 表达"的顺序组合，不跳级。
2. 单一因果链问题不要引入 `system-loops`，会过度复杂化。
3. 分解维度必须与问题陈述中的目标口径一致，否则退回 `problem-reframing`。
4. 同一问题最多同时使用两个分析类框架，避免结论互相稀释。
