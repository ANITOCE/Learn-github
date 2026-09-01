# Spec-Kit + Superpowers 规范化开发解决方案(GitHub Copilot Chat 版)

> **文档版本**: v3.0(引入"开发指南 → N 个 Phase"的分阶段开发范式,工具链收敛为 VS Code Copilot Chat)
> **分析锚点**: spec-kit @ `bf88c9f`(2026-08-14)、superpowers @ `b36e082`(2026-08-12),本机分析副本位于 `research/` 目录
> **开发环境约定**: 所有开发统一在 **VS Code 中的 GitHub Copilot Chat** 完成;**不使用 Copilot CLI**(无 CLI 依赖,无插件钩子依赖)
> **核心工具**:
> - [github/spec-kit](https://github.com/github/spec-kit) — GitHub 官方 Spec-Driven Development(SDD)工具包,以 `/speckit.*` 技能形式安装
> - [obra/superpowers](https://github.com/obra/superpowers) — 编码代理的技能库与开发方法论,以项目技能形式引入
> - Git — 版本控制与工作空间隔离的基座
> **维护原则**: 本文档是"规范"而非"说明书";spec-kit 仍在快速演进,所有命令以官方文档为准,版本号必须锚定(见 2.3)。

---

## 1. 背景与目标

### 1.1 为什么需要这份文档

AI 辅助开发大幅提高了产出速度,但带来三个典型失控点:

| 失控点 | 表现 | 后果 |
|---|---|---|
| 无规格驱动 | Copilot 凭一句话直接写代码,需求反复返工 | 返工、范围蔓延、文档与代码脱节 |
| 无测试约束 | 代码"看起来对",没有测试兜底 | 回归爆炸、不敢重构 |
| 无空间与版本纪律 | 多个会话在同一目录乱写,提交粒度混乱 | 冲突、无法回滚、无法审查 |

本方案的核心创新是**三层开发范式**:开发前先产出**开发指南(总纲)**,把项目/功能分割为 N 个 **Phase**,每个 Phase 独立执行**一轮完整的规格驱动流程**(spec-kit 的 `/speckit.*` 命令链 + superpowers 的纪律技能 + git 纪律),从而把"大项目"化解为"小闭环",并在每个闭环内强制落地**工作空间隔离、TDD 驱动、git 版本控制**三项必要能力。

### 1.2 目标与非目标

**目标**
1. 统一"从零开始新项目"(场景一)与"迭代已有项目"(场景二)的标准流程。
2. 以**开发指南**为总纲,以 **Phase** 为执行单元,消除"整体流程"与"分阶段流程"的重复定义。
3. 强制三项必要能力完整落地:**工作空间隔离**、**TDD 驱动**、**git 版本控制**。
4. 任何成员/任何 AI 代理进入任何项目,都能按同一套规则工作。

**非目标**
- 不绑定具体编程语言或框架(测试框架按项目选型,流程不变)。
- 不替代 Code Review 与人工决策;AI 产出必须过人工审查。
- 不承诺自动化一切:规格与计划的质量责任在人。

### 1.3 术语表

| 术语 | 含义 |
|---|---|
| SDD | Spec-Driven Development:先写规格,规格生成计划、任务与实现 |
| 开发指南(Dev Guide) | 整个项目/功能的**总纲文档**,含概述、Constitution 与开发路线图(N 个 Phase 的划分),由 `brainstorming` 澄清后生成 |
| Phase(阶段) | 项目/功能分割后的一个独立开发阶段;**每个 Phase = 一轮完整流程**(5.2 节) |
| 开发路线图(Roadmap) | 开发指南中 N 个 Phase 的划分表:目标、范围、依赖、产出、验收、状态 |
| Spec(规格) | 对"做什么"的精确描述,即特性目录下的 `spec.md` |
| 技能(Skill) | `SKILL.md` 定义的可复用代理工作指令;Copilot Chat 从 `.github/skills/` 加载项目技能 |
| 斜杠命令 | Copilot Chat 中的 `/speckit.*` 命令,由 spec-kit 以技能形式安装 |
| Constitution(宪章) | 项目治理准则(测试、质量、隔离、git 纪律等),随开发指南制定,落地为 `.specify/memory/constitution.md` |
| 特性目录 | `specs/<分支名>/`,一个 Phase 的全部制品(spec/plan/tasks 等) |
| 工作空间 | Agent 实际读写文件的目录/分支/环境的总称,本方案要求其**隔离** |
| 红/绿/重构 | TDD 三步:先写失败测试(红)→ 最小实现使其通过(绿)→ 清理代码(重构) |
| 公开区 | 进入版本库、可公开可见的目录(如 `src/`、`tests/`、公开文档) |
| 私有区 | 本地保留、被 `.gitignore` 排除、绝不进入公开仓库的目录(规则见 4.7) |

---

## 2. 整体架构与职责分工

### 2.1 三层开发范式(本文档的组织方式)

```
┌─────────────────────────────────────────────────────────────────┐
│ 第 1 层:开发指南(总纲,1 份/项目或功能)                          │
│   brainstorming 澄清后按《开发指南模板》生成                    │
│   内容:概述与范围 · Constitution · 开发路线图(N 个 Phase)       │
│         · 全局技术约束 · 评审与验收总纲                        │
└──────────────────────────────┬──────────────────────────────────┘
                               │ 路线图把总目标分割为 N 个 Phase
┌──────────────────────────────▼──────────────────────────────────┐
│ 第 2 层:Phase(执行单元,N 个,每个由开发指南生成)                 │
│   按《Phase 通用模板》实例化:开发任务 · 技术方案 · 评审/验收标准 │
│   每个 Phase 独立执行一轮完整流程(5.2 节)                       │
└──────────────────────────────┬──────────────────────────────────┘
                               │ 每个 Phase 的制品 + 三项必要能力
┌──────────────────────────────▼──────────────────────────────────┐
│ 第 3 层:制品与纪律(每轮流程内强制)                              │
│   spec-kit: specs/<分支>/{spec,plan,tasks}.md 等制品            │
│   superpowers: TDD 铁律 · worktree 隔离 · 完成前取证 · 分支收尾  │
│   git: 红绿重构逐步提交 · 分支与 PR 纪律                        │
└──────────────────────────────────────────────────────────────────┘
```

**职责分工**
- **开发指南负责"分解"**:把项目/功能拆成 N 个 Phase,定义每个 Phase 的目标、边界与依赖,是全项目的唯一总纲。
- **spec-kit 负责"物"**:`/speckit.*` 命令链(constitution → specify → clarify → plan → checklist → tasks → analyze → implement → converge)在**每个 Phase 内**把"规格→实现"变成有状态、可追溯的流水线。
- **superpowers 负责"法"**:需求澄清(brainstorming)、工作空间隔离(using-git-worktrees)、TDD 铁律(test-driven-development)、根因排查(systematic-debugging)、完成前取证(verification-before-completion)、分支收尾(finishing-a-development-branch)。
- **Git 负责"界"**:每次状态变更可追溯、可回滚、可并行。

### 2.2 角色分工

| 角色 | 职责 | 禁止事项 |
|---|---|---|
| 人(需求方/审查方) | 提需求;brainstorming 澄清;评审开发指南、每个 Phase 的规格/计划/任务;批准实现与合并 | 跳过开发指南直接让 Copilot 写码 |
| Copilot Chat(执行) | 生成/实例化开发指南与 Phase 文档;按规格执行 TDD;提交;报告 | 未经批准修改规格;绕过测试;直接推送到受保护分支 |
| CI(可选) | 跑测试、门禁 | 不承担规格质量判断 |

### 2.3 版本锚定原则(强制)

- 在项目 `.github/copilot-instructions.md` 中记录:specify 版本、本规范版本、superpowers 项目技能的引入版本。
- spec-kit 项目文件升级与特性制品演进是**两条独立的维护线**(见场景二),升级前先读官方 `docs/upgrade.md`。
- 升级命令:`specify self check`(只读检查)→ `specify self upgrade --dry-run`(预览)→ `specify self upgrade`(执行)。

---

## 3. 环境与安装(一次性准备)

### 3.1 前置要求

| 依赖 | 用途 | 备注 |
|---|---|---|
| [uv](https://docs.astral.sh/uv/) | 安装 specify CLI(spec-kit 官方推荐;备选 pipx) | 必需 |
| Python 3.11+ | specify CLI 运行时 | uv 会自动处理 |
| Git 2.30+ | 版本控制、worktree 隔离 | 必须配置 user.name / user.email |
| VS Code + GitHub Copilot 扩展 | **唯一开发界面**,加载 `/speckit.*` 与 superpowers 项目技能 | 必需 |
| GitHub 仓库 | PR 评审与协作 | 推荐 |

> **明确不使用 Copilot CLI**:本方案不依赖 `copilot` 命令行、不安装任何 CLI 插件、不依赖插件钩子(session-start hook)。superpowers 以**项目技能**方式引入(3.3),其"自动触发"能力由 `.github/copilot-instructions.md` 中的强制条款补足(4.1)。

### 3.2 安装 spec-kit

```bash
# 官方推荐:从 PyPI 安装(或锁定发布标签)
uv tool install specify-cli
# 锁定版本(推荐用于团队一致性,vX.Y.Z 替换为最新发布标签):
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git@vX.Y.Z

# 验证
specify --version
specify integration list        # 确认 copilot 在集成列表中
```

### 3.3 引入 superpowers(项目技能方式,VS Code Copilot Chat)

superpowers 的官方插件入口面向各 CLI 平台;本方案不使用 CLI,改用**项目技能方式**:

1. 取得 superpowers 技能文件(以本机 `research/superpowers/skills/` 为准,或按需从上游同步);
2. 将所需技能目录复制到项目 `.github/skills/` 下(与 spec-kit 的 `speckit-*` 目录共存,技能名以各 `SKILL.md` 的 frontmatter `name` 为准,不会冲突):

   ```
   .github/skills/
   ├── speckit-*/                    # spec-kit 安装的命令技能
   ├── brainstorming/SKILL.md        # superpowers:需求澄清(开发指南的生成入口)
   ├── using-git-worktrees/SKILL.md  # superpowers:工作空间隔离
   ├── test-driven-development/SKILL.md   # superpowers:TDD 铁律
   ├── systematic-debugging/SKILL.md      # superpowers:根因排查
   ├── verification-before-completion/SKILL.md  # superpowers:完成前取证
   └── finishing-a-development-branch/SKILL.md # superpowers:分支收尾
   ```

3. 使用交付的 `copilot-instructions-template.md` 模板(见 8.1,占位符替换后复制到 `.github/copilot-instructions.md`),写入**强制技能条款**,替代 CLI 插件的自动引导。

**核心技能清单(以仓库实际为准):**

| 技能 | 用途 | 触发时机 |
|---|---|---|
| `brainstorming` | 澄清需求、生成设计(Spike/Bounded/Architectural 三路径) | **生成/修订开发指南前必用** |
| `using-git-worktrees` | 隔离工作空间 + 干净基线验证 | 每个 Phase 的"隔离"步骤 |
| `test-driven-development` | 红-绿-重构铁律(含反模式与借口清单) | 每个 Phase 实现期,默认工作法 |
| `systematic-debugging` | 四阶段根因定位 | 测试失败/缺陷 |
| `verification-before-completion` | 无证据不宣称完成 | 每次宣称完成前 |
| `finishing-a-development-branch` | 合并/PR/保留三选一 + worktree 清理 | 每个 Phase 收尾 |

> 如环境支持子代理分发(Copilot Chat 的 agent 模式),可追加 `subagent-driven-development`(每任务一个全新子代理 + 两阶段评审);否则使用批量执行 + 人工检查点的方式,流程不变。

### 3.4 安装验证

```bash
specify --help                      # 列出 init/self/integration 等子命令
```
在 VS Code 中打开项目后,于 Copilot Chat 内确认:
- 输入 `/` 能看到 `speckit-*` 系列命令;
- 技能列表能看到 superpowers 项目技能(如 `brainstorming`、`test-driven-development`);
- 项目 `.github/copilot-instructions.md` 的条款被 Copilot 读取(可在对话中询问验证)。

---

## 4. 全局约定(所有 Phase 强制遵守)

> 本章是"必要功能"的落地条款。第 5 章的"单轮 Phase 标准流程"与第 6、7 章的场景编排均以本章为准则。

### 4.1 仓库结构约定

`specify init . --integration copilot` 实际生成的结构(默认技能模式)+ 团队补充:

```
<repo-root>/
├── .github/
│   ├── skills/                          # 🔒 Copilot Chat 项目技能(两层来源)
│   │   ├── speckit-<name>/SKILL.md      #   spec-kit 安装的 /speckit.* 命令
│   │   └── <superpowers 技能>/SKILL.md  #   团队引入的 superpowers 技能
│   └── copilot-instructions.md          # 🔒 项目级 Copilot 指令(团队手工维护)
├── .specify/                            # 🔒 spec-kit 状态(memory/constitution.md、feature.json 等)
├── specs/<分支名>/                      # 🔒 特性制品目录(每个 Phase 一个)
│   └── spec.md / plan.md / tasks.md …   #   需求、技术方案、任务清单(含 checklists/、contracts/ 等)
├── docs/
│   ├── dev-guides/                      # 🔒 开发指南(总纲,每项目/功能一份)
│   ├── phases/                          # 🔒 Phase 文档(每个 Phase 一份,由开发指南生成)
│   ├── templates/                       # 🔒 模板:两份文档模板 + copilot-instructions-template.md
│   └── spec-kit-解决方案.md             # ✅ 本解决方案(公开,供人阅读)
├── .superpowers/                        # 🔒 superpowers 运行期文件(SDD 台账、brainstorm 会话)
├── src/  <语言约定>/                     # ✅ 公开:实现代码
├── tests/                               # ✅ 公开:测试代码
└── .worktrees/                          # 🔒 superpowers 隔离工作树目录

图例:🔒 = 私有区(gitignore,绝不进入公开仓库,规则见 4.7);✅ = 公开区(正常入库)。
```

**`.github/copilot-instructions.md`(团队维护,spec-kit CLI 不管理该文件):**
直接使用交付的 `copilot-instructions-template.md` 模板(见 8.1):替换占位符后复制到 `.github/` 并命名为 `copilot-instructions.md` 即可,其内容已包含:
1. 本规范的引用与版本锚点;
2. **强制技能条款**(替代 CLI 自动引导):"开始任何工作前,先检查并遵循适用的 superpowers 项目技能;创意/需求类工作必须先走 `brainstorming`;实现必须遵循 `test-driven-development`;宣称完成前必须遵循 `verification-before-completion`";
3. 工作空间隔离规则(4.2)与红绿重构提交约定(4.4);
4. 禁止事项:不得改写已评审通过的规格、不得删除测试、不得强制推送等。

### 4.2 工作空间隔离规范 ★

隔离分四个层面,缺一不可:

| 层面 | 手段 | 规则 |
|---|---|---|
| ① 分支/目录 | `using-git-worktrees` 技能 + `git worktree` | 每个 Phase 独占一个分支与一个 worktree 目录;**禁止多个会话在同一检出目录并发写文件** |
| ② 依赖环境 | Python venv / 锁文件 / 容器 | 每个项目独立环境;依赖锁文件必须入库 |
| ③ 代理会话 | Phase 内分任务执行 | 每个任务只接收该任务所需的最小上下文(子代理或人工检查点分批) |
| ④ 文件读写边界 | 以当前 Phase 的规格与任务清单为界 | 未列入当前规格/任务的文件只读不写;改动清单必须在 PR 中可见 |

**worktree 规范(来自 superpowers 的 `using-git-worktrees` 技能):**

1. **先检测再创建**:`git rev-parse --git-dir` 与 `--git-common-dir` 不同且非 submodule 时,说明已在 worktree 中,直接使用;submodule 视为普通仓库(用 `git rev-parse --show-superproject-working-tree` 排除误判)。
2. **优先平台原生工具**:如 VS Code 提供原生 worktree 入口则优先使用;否则用 `git worktree add .worktrees/<分支名> -b <分支名>`。
3. **`.worktrees/` 必须被 git 忽略**:创建前用 `git check-ignore -q .worktrees` 验证,未忽略则先加 `.gitignore` 并提交(否则会把整个工作树提交进仓库)。
4. **干净基线**:进入 worktree 后先安装依赖并跑一遍全量测试,**测试通过才开始开发**;失败则先报告并决定是否调查。
5. **与 spec-kit 的状态解耦**:`/speckit.*` 命令通过 `.specify/feature.json`(或环境变量 `SPECIFY_FEATURE_DIRECTORY`)识别当前特性,**不依赖 git 分支**;因此切换 worktree 后要确认 `feature.json` 指向当前 Phase 的特性目录,`git checkout` 本身不会切换特性上下文。

### 4.3 TDD 驱动规范 ★(双保险:宪章 + superpowers 铁律)

**第一层保险 — Constitution(随开发指南制定)**:开发指南中的 Constitution 条款(见模板)必须含"Test-First(NON-NEGOTIABLE)":先写测试 → 人批准 → 确认测试失败 → 才允许实现;落地到 `.specify/memory/constitution.md` 后,`/speckit.plan` 的 Phase -1 门禁会强制"先建契约与测试文件,再写实现"。

**第二层保险 — superpowers 的 `test-driven-development` 技能铁律:**

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
(没有先失败的测试,就没有生产代码)
```

| 阶段 | 动作 | 退出条件 |
|---|---|---|
| 红 Red | 写一个最小失败测试(一个行为、清晰命名、真实代码而非 mock) | **亲眼看到它按预期原因失败**(断言失败,而非语法/环境错误) |
| 绿 Green | 写最小实现(不做测试之外的事,不顺手重构,YAGNI) | 该测试通过,其余测试仍全绿 |
| 重构 Refactor | 去重复、改名、提取,不加新行为 | 全量测试保持绿色 |

**执行规则:**
- 在写测试之前写过实现代码?**删掉重来**(不许"留作参考"、不许"边写测试边改它")。
- 每个红/绿/重构步骤完成后立即**独立提交**(见 4.4)。
- Bug 修复 = 先写能复现该 bug 的失败测试 → 红绿重构 → 测试同时是回归证明。**没有测试的修复不是修复**。
- 常见借口表("太简单不用测"、"先实现后补测试"、"手工测过了"…)全部视为违规信号,处置方式:删码重来,或取得人工豁免(仅限抛弃型原型/生成代码/配置文件三类,且必须人批准)。
- 验收命令:Phase 收尾前必须运行**全量**测试套件并留存输出证据,而非只跑新增用例。

**第三层保险 — `verification-before-completion` 技能**:宣称任何成功(测试通过、修复完成、Phase 完成)前,必须在**当前消息**中运行完整验证命令并读出结果;`should / probably / 应该通过了` 等措辞一律视为未验证。

### 4.4 git 版本控制规范 ★

1. **分支模型**:主干受保护;所有开发走特性分支。启用 spec-kit 的 git 扩展后,特性分支自动编号(`001-feature-name`),与 `specs/001-feature-name/` 目录一一对应;**一个 Phase 对应一个特性分支**。
2. **提交粒度与信息**:红/绿/重构各一个提交,信息描述行为变化(团队统一约定):

   ```text
   test: add failing test for <X>      # 红:只加测试,明确失败
   feat: implement <X>                 # 绿:最小实现,测试通过
   refactor: clean up <X>              # 重构:清理,测试保持通过
   ```

   公开仓库只提交代码、测试与公开文档;私有区文件(开发指南、Phase 文档、规格等)一律不入库(见 4.7)。若团队另设私有仓库托管私有区文档,其提交使用 `docs:`、`specs:`、`chore:` 前缀。
3. **每个提交是"可理解的最小状态"**:不得出现"半成品+调试输出"的提交;临时文件禁止入库。
4. **合并纪律(由 `finishing-a-development-branch` 技能执行)**:Phase 收尾时先跑全量测试 → 确认基线分支(合并错基线的代价高昂)→ 由人三选一:① 本地合并回基线;② 推送并创建 PR;③ 保留分支。合并后必须再跑一次测试;失败则停,worktree 与分支保留待查。
5. **历史安全**:`rebase` 只允许在未推送的分支上进行;推送被拒时调查原因,**未经人明确要求不得强推**;worktree 删除被拒(有未提交文件)时绝不 `--force`,先展示文件清单由人决定(提交/移出/删除)。
6. **清理纪律**:只清理本方案创建的 `.worktrees/` 下的工作树(`git worktree remove` + `git worktree prune`);宿主环境管理的其他工作区一律不动。

### 4.5 规格文档规范(每个 Phase 的 spec)

spec-kit 的 spec 模板强制以下质量机制,团队不得移除:

- **聚焦 WHAT/WHY,禁止 HOW**:`spec.md` 不写技术栈与实现细节(那是 `plan.md` 的职责)。
- **显式的不确定标记**:prompt 未交代的内容必须写 `[NEEDS CLARIFICATION: 具体问题]`,禁止猜测;所有标记清零后才算规格完成。
- **需求完备性清单**:可测试、无歧义、成功标准可度量。
- **特性目录即档案**:一个 Phase = `specs/<分支名>/` 一个目录,制品之间可交叉引用、可追溯,并与开发指南路线图中对应条目互相链接。
- **状态与评审**:规格写完后由人评审通过,才进入 plan/tasks;`/speckit.checklist` 生成的自定义质量清单由评审人打勾(打勾只代表需求质量合格,不代表实现完成)。

### 4.6 完成定义(Definition of Done)

**Phase 级 DoD**(单个 Phase 满足全部条件才可宣称完成):

- [ ] 该 Phase 的开发指南路线图条目与 Phase 文档齐全且经评审
- [ ] 规格(含澄清)已人工评审通过;`/speckit.analyze` 无未解决的缺口
- [ ] `/speckit.converge` 报告收敛(无剩余差距任务)
- [ ] 所有需求条目有对应测试;红-绿-重构历史完整可查(每步独立提交)
- [ ] 全量测试通过且有**本次运行的输出证据**(非"上次跑过")
- [ ] 改动文件清单与任务范围一致,无规格外"顺手改"
- [ ] 工作空间已按 `finishing-a-development-branch` 收尾:合并/PR 已获人批准,worktree 已清理
- [ ] 开发指南路线图中该 Phase 状态已更新(planned → in-review → merged → done)
- [ ] 公开提交不含私有区文件(`git status --porcelain` 仅公开区改动,见 4.7)

**项目级 DoD**(开发指南总纲层面):所有 Phase 均达到 Phase 级 DoD,开发指南中的验收总纲逐项通过(见模板第 6 节),且公开仓库无私有区文件泄漏(见 4.7)。

### 4.7 仓库公开边界与 git 忽略规则 ★

**原则**:spec-kit 与 superpowers 会产生大量包含开发细节的文档与运行期文件(技能、宪章、规格、计划、台账),它们只服务于开发过程,**一律不进入 GitHub 等公共空间**。公开仓库只包含:实现代码(`src/`)、测试(`tests/`)、公开文档(README 等)与常规配置。

**标准 `.gitignore` 块**(脚手架完成后立即加入并提交):

```gitignore
# ===== AI 开发工作流私有区(不入公开仓库)=====

# GitHub Copilot 技能与指令(spec-kit 命令技能、superpowers 方法技能、项目指令)
.github/skills/
.github/agents/
.github/prompts/
.github/copilot-instructions.md
# 可选:若启用了 SDD 的 GitHub Actions 工作流,一并忽略
# .github/workflows/specify.yml

# spec-kit 状态与模板(宪章、特性指针、集成清单、项目覆盖)
.specify/

# spec-kit 特性规格制品(开发细节)
/specs/

# superpowers 计划文档与运行期文件(SDD 台账、brainstorm 会话)
docs/superpowers/
.superpowers/

# 开发指南与 Phase 文档(总纲与执行细节)
docs/dev-guides/
docs/phases/
docs/templates/

# 隔离工作树
.worktrees/
```

**私有区目录与理由:**

| 目录/文件 | 内容 | 不入库理由 |
|---|---|---|
| `.github/skills/`、`.github/agents/`、`.github/prompts/` | spec-kit 命令技能(skills/commands 两种模式产物) | 内部工作流配置 |
| `.github/copilot-instructions.md` | AI 行为准则 | 内部开发纪律 |
| `.specify/` | constitution、feature.json、模板、脚本、扩展 | 项目治理与本地状态 |
| `/specs/` | 规格、方案、任务、清单 | 开发细节 |
| `docs/dev-guides/`、`docs/phases/`、`docs/templates/` | 开发指南、Phase 文档、模板 | 开发细节与方法 |
| `docs/superpowers/`、`.superpowers/` | superpowers 计划文档、SDD 台账、brainstorm 会话 | 运行期痕迹 |
| `.worktrees/` | 隔离工作树 | 工作区副本 |

**提交检查规则:**
1. 每次提交前执行 `git status --porcelain`,输出必须只包含公开区文件;出现任何私有区路径立即停止,检查 `.gitignore` 并移除误添加文件。
2. 公开 PR 只包含公开区改动;PR 描述**可以引用**私有区路径(如 `specs/001-x/spec.md` 作为上下文说明),**不得粘贴**其内容。
3. 开发指南评审、Phase 三件套评审等人工闸门在本地(或团队私有通道)进行,不依赖公开 PR。
4. 私有区文件未被 git 追踪(无版本历史);如团队需要版本化/共享,将其放入独立**私有仓库**或内部分发通道,公开仓库绝不收录。一旦发生泄漏,视为事故:立即从公开历史中清除并复盘。

---

## 5. 开发指南驱动的多阶段开发范式

### 5.1 三层结构关系(规范定义)

| 层 | 文档 | 数量 | 生成方式 | 内容要点 |
|---|---|---|---|---|
| 总纲 | 开发指南 | 1 份/项目或功能 | `brainstorming` 澄清后,按《开发指南模板》生成 | 概述与范围、**Constitution**、全局技术约束、**开发路线图(N 个 Phase)**、评审与验收总纲 |
| 执行 | Phase 文档 | N 份(与路线图一一对应) | 由开发指南路线图条目按《Phase 通用模板》实例化生成 | 该 Phase 的**开发任务**(一轮完整流程)、**技术方案**、**评审与验收标准** |
| 制品 | spec-kit 制品 + git | 每 Phase 一套 | 单轮流程(5.2)执行产出 | `specs/<分支>/*.md`、提交历史、PR、worktree 清理记录 |

**生成与执行链路:**

```
需求 → [brainstorming] → 开发指南(含 Constitution + 路线图)
                                    │
              ┌─────────────────────┼─────────────────────┐
              ▼                     ▼                     ▼
          Phase 1 文档          Phase 2 文档         Phase N 文档
        (开发任务/技术方案/评审验收标准,由路线图条目实例化)
              │                     │                     │
        一轮完整流程           一轮完整流程           一轮完整流程
       (5.2, 每次一个特性分支 + 一个 worktree + 一次收尾)
```

### 5.2 单轮 Phase 标准流程(每个 Phase 完整执行一遍)

> 本节是全文唯一的"完整流程"定义;第 6、7 章的场景只做**编排**(如何生成开发指南、如何推进 N 个 Phase),不再重复本节的步骤。

**步骤总览:**

```
[P0 准备输入] → [P1 /speckit.specify] → [P2 /speckit.clarify]
  → [P3 /speckit.plan] → [P4 /speckit.checklist]
  → [P5 /speckit.tasks] → [P6 /speckit.analyze]
  → [P7 人工评审闸门] → [P8 worktree 隔离 + 干净基线]
  → [P9 /speckit.implement(TDD 铁律)] → [P10 /speckit.converge]
  → [P11 全量验证取证] → [P12 收尾(合并/PR)] → [P13 回写开发指南]
```

**P0 — 准备输入**:从开发指南路线图读取本 Phase 的目标、范围、依赖与验收条目;实例化《Phase 通用模板》生成该 Phase 文档(含开发任务/技术方案/评审验收标准);确认前置 Phase 已合并、`feature.json` 后续将指向本 Phase 特性目录。

**P1 — 写规格(`/speckit.specify`)**:在 Copilot Chat 中执行,只讲"做什么、为什么做":
> `/speckit.specify <本 Phase 要实现的行为,引用开发指南目标>`
产物:`specs/<分支名>/spec.md`(自动编号并建特性分支)。检查:无 `[NEEDS CLARIFICATION]` 残留。

**P2 — 消歧(`/speckit.clarify`)**:对规格未说透的点定向提问并把答案写回 spec.md(可选带焦点)。

**P3 — 技术方案(`/speckit.plan`)**:在此提供本 Phase 的技术栈与架构选择(唯一允许谈 HOW 的环节);产物 `plan.md`(+ 按需 `research.md`、`data-model.md`、`contracts/`、`quickstart.md`)。**技术方案要点同步回填 Phase 文档的"技术方案"节**。

**P4 — 质量清单(`/speckit.checklist`)**:生成自定义质量清单("给需求写单元测试"),由**评审人**打勾。

**P5 — 任务拆分(`/speckit.tasks`)**:从 plan 推导 `tasks.md`,独立任务标 `[P]` 可并行。

**P6 — 一致性分析(`/speckit.analyze`)**:跨 spec/plan/tasks 只读检查;有缺口回源头修,重跑至干净。

**P7 — 人工评审闸门(不可跳过)**:按 Phase 文档"评审标准"节逐项评审 spec → plan → tasks 三件套 + checklist;通过后才允许实现。

**P8 — 隔离工作空间 + 干净基线(调用 `using-git-worktrees`)**:在 `.worktrees/<分支名>` 建立 worktree(遵循 4.2 的检测/忽略/基线流程);重建依赖环境,全量测试**绿色基线才开工**。

**P9 — 实现(`/speckit.implement`,按 TDD 铁律)**:按 `tasks.md` 依赖序执行;每个任务内部严格红-绿-重构,每步独立提交(4.4)。任务间如支持子代理则每任务一个全新子代理 + 两阶段评审(规格符合性→代码质量),否则批量执行 + 人工检查点。实现期间发现规格缺陷:停止实现,回到 P1/P2 修订规格并提交,再继续——**禁止为迁就实现而悄悄改规格**。任何失败先调用 `systematic-debugging`(四阶段根因),禁止症状式修补;修复必须带回归测试。

**P10 — 收敛(`/speckit.converge`)**:对照 spec/plan/tasks 评估代码库;有差距则把剩余工作追加为任务,重复 implement → converge 直到收敛。

**P11 — 全量验证取证(`verification-before-completion`)**:
```bash
<测试框架> run                    # 全量;记录输出: N 通过 / 0 失败
git status --porcelain            # 无未提交杂物
git log --oneline <分支>          # 红绿重构提交历史完整
```
对照 Phase 文档"验收标准"节逐项检查(满足 Phase 级 DoD,见 4.6)。

**P12 — 收尾(`finishing-a-development-branch`)**:再跑一次全量测试 → 确认基线分支 → 由人三选一(本地合并 / 推送建 PR / 保留);选 PR 时 worktree 保留用于响应评审意见,合并落地后清理;`git worktree remove` + `git worktree prune`,删除已合并分支。

**P13 — 回写开发指南**:更新路线图中该 Phase 状态(merged/done)、关联 PR 与特性目录、记录技术方案与验收结论的最终差异(如有)。该回写发生在私有区本地文档中,不产生公开提交(私有仓库托管场景按 4.7 处理)。

### 5.3 开发指南与 Phase 文档的生成规则

1. **开发指南**:任何开发开始前,在 Copilot Chat 中先用 `brainstorming` 技能澄清(新项目走 Architectural 路径;存量变更按 Spike/Bounded/Architectural 分类,见 7.2),澄清完成后按 `docs/templates/development-guide-template.md` 生成,存放于 `docs/dev-guides/`(私有区,不入公开仓库),并人工评审通过。
2. **Phase 文档**:每个 Phase 开工前(P0),由开发指南路线图条目按 `docs/templates/phase-template.md` 实例化生成,存放于 `docs/phases/`,与 `specs/<分支名>/` 互相链接;Phase 文档只描述**本 Phase 的**开发任务、技术方案、评审与验收标准,不重复开发指南的总纲内容。
3. **一致性**:Phase 文档的"目标/范围"必须逐字对应路线图条目;实现中若路线图需要调整(增删 Phase、调整依赖),先修订开发指南(走评审)再调整后续 Phase 文档——**禁止只改 Phase 文档不动开发指南**。

---

## 6. 场景一:从零开始的新项目

### 6.1 编排流程总览

```
[S1 环境与脚手架] → [S2 brainstorming 生成开发指南(含 Constitution + 路线图)]
  → [S3 评审开发指南] → [S4 Constitution 落地(/speckit.constitution)]
  → [S5 逐 Phase 循环:Phase 文档生成 → 单轮流程(5.2)]
  → [S6 项目级验收(按开发指南验收总纲)] → [S7 收尾归档]
```

### 6.2 步骤详解

**S1 — 环境与脚手架**(按第 3 章 + 一次性仓库准备):
```bash
mkdir <project> && cd <project>
git init -b main
# 建立依赖隔离环境(如 python -m venv .venv);.gitignore 纳入 .venv/、__pycache__/ 及 4.7 定义的私有区清单
git commit --allow-empty -m "chore: init repository"

specify init . --integration copilot        # 生成 .github/skills/speckit-*/SKILL.md 与 .specify/ 骨架(均属私有区)
git add . && git commit -m "chore: scaffold .gitignore and public baseline"
```
- 将 3.3 选定的 superpowers 技能复制到 `.github/skills/`;把交付的 `copilot-instructions-template.md` 模板替换占位符后复制为 `.github/copilot-instructions.md`(内容见 4.1)。以上均留在本地私有区,不入公开仓库;首次公开提交只包含公开区文件(含按 4.7 配置好的 `.gitignore`)。
- 检查点:Copilot Chat 中 `/` 能看到 `speckit-*` 命令与 superpowers 技能。

**S2 — brainstorming 澄清并生成开发指南**:
- 在 Copilot Chat 中调用 `brainstorming` 技能,与需求方澄清:目标用户、核心场景、范围、非目标、技术约束;
- 按《开发指南模板》生成开发指南到 `docs/dev-guides/<项目>-guide.md`,其中:
  - **Constitution** 章节:制定整个项目的治理准则(必含 Test-First TDD、工作空间隔离与 git 纪律、评审/验收闸门);
  - **开发路线图**:把项目分割为 N 个 Phase,写明每个 Phase 的目标、范围、依赖、产出与验收;
- 保存于 `docs/dev-guides/`(私有区,不入公开仓库;评审与团队共享走私有通道,见 4.7)。

**S3 — 评审开发指南**:需求方/团队评审概述、Constitution 与路线图(分割是否合理、依赖是否闭环、验收是否可测);通过后指南定稿,后续调整须走变更评审。

**S4 — Constitution 落地**:在 Copilot Chat 执行:
> `/speckit.constitution <按开发指南 Constitution 章节逐条传入>`
产物 `.specify/memory/constitution.md`(私有区);核对与开发指南 Constitution 一致(该文件不入公开仓库,见 4.7)。

**S5 — 逐 Phase 循环(核心执行段)**:对路线图中的每个 Phase(按依赖序,无依赖的 Phase 可并行):
1. 从路线图条目实例化 Phase 文档(按《Phase 通用模板》,存 `docs/phases/<项目>-phase-<NN>.md`);
2. 执行**单轮 Phase 标准流程(5.2)**:P0~P13;
3. 全部 Phase 完成(merged)前不进入 S6。

**S6 — 项目级验收**:按开发指南"评审与验收总纲"逐项验收(见模板第 6 节):所有 Phase 的 DoD 证据、路线图状态、Constitution 符合性、技术债与开放问题闭环。

**S7 — 收尾归档**:更新开发指南状态为 `done`(本地私有区);清理所有 `.worktrees/` 残留与已合并分支;`specs/`、`docs/phases/` 等私有区文档按团队私有通道归档,不进公开仓库。

### 6.3 场景一检查清单

- [ ] uv / specify 安装验证通过;`specify init --integration copilot` 已提交
- [ ] superpowers 技能已入 `.github/skills/`;`copilot-instructions.md` 含强制技能条款
- [ ] 开发指南经 `brainstorming` 生成并评审通过;Constitution 与路线图(N 个 Phase)齐全
- [ ] Constitution 已落地 `.specify/memory/constitution.md` 且与开发指南一致
- [ ] 每个 Phase:文档由路线图条目实例化 → 单轮流程(5.2)完整执行 → Phase 级 DoD 达成 → 路线图状态更新
- [ ] 项目级验收总纲逐项通过;开发指南状态 done;工作区与分支清理完毕;公开仓库无私有区文件泄漏

---

## 7. 场景二:迭代已有项目

### 7.1 编排流程总览

```
[T1 审计现状] → [T2 区分两条维护线]
  → [T3 brainstorming 分类澄清] → [T4 生成增量开发指南(变更拆为 N 个 Phase)]
  → [T5 评审增量开发指南] → [T6 逐 Phase 循环:Phase 文档 → 单轮流程(5.2)]
  → [T7 全量回归验收] → [T8 收尾归档]
```

存量项目同样以开发指南为总纲:每次迭代(一个功能或一组变更)生成一份**增量开发指南**,变更被分割为 N 个 Phase,每个 Phase 仍执行 5.2 的单轮流程。

### 7.2 前置概念与步骤详解

**T1 — 审计现状(必做)**
- 读:`.github/copilot-instructions.md`(或 `AGENTS.md`)、`.specify/memory/constitution.md`、`specs/` 全部特性目录及状态、`.specify/feature.json` 当前指向、既有开发指南。
- 跑 `git status`、`git log --oneline -10`,确认无脏工作区、无堆积分支。
- 产出:`docs/dev-guides/audit-YYYY-MM-DD.md`:现有规格清单、测试命令与基线结果、已知技术债。
- 检查点:能回答"现在有什么规格、什么测试、什么技术债"。

**T2 — 区分两条维护线**(spec-kit 官方《Evolving Specs in Existing Projects》):
- **项目文件维护线**:`specify self upgrade` 或 `specify init --here --force --integration copilot` 刷新命令/脚本/模板等受管文件。**刷新前必须备份** `.specify/memory/constitution.md` 与 `.specify/templates/`、`.specify/scripts/` 下的自定义内容(强制刷新会覆盖);`specs/` 与 `docs/` 不属于模板包,不会被覆盖。此线不产生 Phase。
- **特性制品维护线**:`specs/` 与代码的演进,走 T3~T8。规格演进有三种官方模型:

| 模型 | 适用 | 做法 |
|---|---|---|
| **Flow-Forward(前向流转)** | 每个特性目录作为历史档案保留 | 新变更走全新 `/speckit.specify` 流程,旧目录留存备查,用命名/交叉链接标注替代关系 |
| **Living Spec(活规格)** | `spec.md` 是契约,plan/tasks 由其派生 | 先改 `spec.md` → 重跑或修订 plan → 重跑或修订 tasks → `analyze` 查缺 → implement → converge |
| **Flow-Back(回填)** | 允许实现中的发现重塑制品 | 发现记录在最近制品 → 判断影响层级 → 同步所有不一致制品 → `analyze` → 继续实现 |

团队默认:小改动用 **Living Spec**,新增独立功能用 **Flow-Forward**;Flow-Back 允许但必须有 `analyze` 兜底。所选模型写入增量开发指南。

**T3 — brainstorming 分类澄清**:调用 `brainstorming` 技能,对本次变更分类(Spike 可行性探针 / Bounded 小改动 / Architectural 完整流程)并**说出来**;明确"这次改什么、**不改什么**";任何实现动作前必须有人工批准(批准门槛不随任务变小而降级)。

**T4 — 生成增量开发指南**:按《开发指南模板》生成 `docs/dev-guides/<变更名>-guide.md`:
- Constitution 章节:引用既有项目宪章(不重写);如需修订,记录修订条目与理由(走评审);
- 开发路线图:把本次变更分割为 N 个 Phase(通常 1~3 个),含回归范围说明;
- 记录所选规格演进模型与对应既有制品的关系(替代/修订/新增)。

**T5 — 评审增量开发指南**:由熟悉旧行为的成员参与评审;涉及已 accepted 规格的修订必须留痕。

**T6 — 逐 Phase 循环**:与场景一 S5 相同——每个 Phase 实例化文档后执行单轮流程(5.2),但**范围约束更严**:只实现本 Phase 规格/任务内的条目;触及旧代码时默认"不改变既有行为",必须改变时在 PR 中显式声明并补回归测试;Phase 开工前先在新 worktree 中跑全量测试建立回归基线(基线哈希记入 Phase 文档)。

**T7 — 全量回归验收**:
```bash
<测试框架> run                    # 全量:新用例 + 全部既有用例,留存输出
git diff <基线> --stat            # 改动面只应包含本迭代相关文件
```
对照增量开发指南验收总纲逐项验收;改动文件清单与规格范围一致,无"顺手改"的无关变更。

**T8 — 收尾归档**:同场景一 S7;PR 描述必须包含:关联增量开发指南、回归基线结果、行为变更声明。

### 7.3 场景二检查清单

- [ ] 审计笔记存在;基线哈希与基线测试结果已记录
- [ ] 两条维护线已区分;项目文件升级已备份 constitution 与自定义模板
- [ ] 变更经 `brainstorming` 分类并获人工批准;不改什么已明确
- [ ] 增量开发指南(含 Constitution 引用/修订、路线图、演进模型)已评审
- [ ] 每个 Phase:文档实例化 → 回归基线建立 → 单轮流程(5.2)→ Phase 级 DoD → 路线图状态更新
- [ ] 全量回归通过且有输出证据;converge 收敛;行为变更在 PR 中声明
- [ ] 增量开发指南状态 done;worktree/分支清理;公开仓库无私有区文件泄漏

---

## 8. 模板体系

### 8.1 模板清单与存放

| 模板 | 位置 | 用途 | 生成者 |
|---|---|---|---|
| 开发指南模板 | `docs/templates/development-guide-template.md` | 生成开发指南(总纲,含 Constitution 与路线图) | Copilot Chat(经 `brainstorming` 澄清后) |
| Phase 通用模板 | `docs/templates/phase-template.md` | 由路线图条目实例化生成各 Phase 文档 | Copilot Chat(每 Phase 开工前 P0) |
| Copilot 项目指令 | `docs/templates/copilot-instructions-template.md`(复制到项目 `.github/` 后命名为 `.github/copilot-instructions.md`) | 项目级 AI 行为准则(技能强制、TDD、隔离、git 纪律、公开边界) | 团队(占位符替换后直接使用) |

三份文件随本方案配套交付,均位于 `docs/templates/`:两个文档模板复制到项目 `docs/templates/`,`copilot-instructions-template.md` 复制到 `.github/` 并命名为 `copilot-instructions.md`。三者复制后均位于私有区,不入公开仓库(见 4.7)。

### 8.2 生成链路(一致性约束)

1. **开发指南 = 总纲**:任何规格、计划、任务、代码都从它派生;它变更(评审后),下游 Phase 文档与制品相应调整。
2. **Phase 文档 = 指南的执行镜像**:其"目标与范围"逐字对应路线图条目;其"技术方案"节与 `specs/<分支>/plan.md` 同步;其"评审/验收标准"节与 4.5/4.6 对齐。
3. **Constitution 单一来源**:新项目 → 开发指南的 Constitution 章节落地为 `.specify/memory/constitution.md`;存量项目 → 指南只引用/修订,不复制全文。

### 8.3 使用须知

- **定位分离**:本方案(解决方案文档)面向**人**,指导"下一步该干什么";两个模板与 `copilot-instructions.md` 面向 **AI**,是自包含的生成/行为准则,规则全部内联,不依赖本方案,可直接复制进项目使用(三份 AI 文档之间可互相引用)。
- 模板中的 `{{占位符}}` 全部替换后再评审;占位符未替换的文档不得进入实现。
- 开发指南与 Phase 文档都要纳入 git 版本控制与人工评审,评审不通过不得开工。

---

## 9. 常见问题与风险

| 风险/问题 | 症状 | 应对 |
|---|---|---|
| spec-kit 实验性、演进快 | 命令/模板随版本变化 | 版本锚定(2.3);升级走 `self check → upgrade --dry-run → upgrade`;强制刷新前备份 |
| 开发指南与实现脱节 | 实现内容超出/偏离路线图 | Phase 文档与路线图条目逐字对应(5.3);偏离先改指南(走评审) |
| Phase 划分过粗/过细 | 单轮流程过长/上下文爆炸 | 路线图评审时把关:每个 Phase 2~5 个工作日当量;过大则拆 |
| 工具职责重叠 | brainstorming 与 `/speckit.clarify`、Phase 技术方案与 `/speckit.plan` 打架 | 分工:brainstorming 管"生成指南前的澄清",clarify 管"规格文本消歧";Phase 文档技术方案节是 plan.md 的镜像,以 plan.md 为准 |
| 无 CLI 导致技能不自动触发 | Copilot 未主动走技能流程 | `copilot-instructions.md` 强制技能条款(4.1);对话中显式点名技能名 |
| 规格漂移 | 代码与规格逐渐不一致 | `analyze` + `converge` 每 Phase 必跑;不一致先改规格(走评审)再改代码 |
| 测试被"刷绿" | 空断言/删除测试/测试从没失败过 | 红阶段必须看到真实失败;Constitution Test-First + TDD 铁律双保险;提交历史按红绿重构核查 |
| 环境互相污染 | 依赖冲突、缓存串扰 | 每个 worktree 独立环境;锁文件入库;基线测试先绿后开工 |
| 多会话并发冲突 | 同一文件互相覆盖 | 一 Phase 一分支一 worktree;子代理按任务隔离上下文 |
| 模型成本/无限重试 | 反复失败重试 | 失败即停转 `systematic-debugging`;给会话设步数/预算上限 |
| 过度自动化 | 人不再思考 | 开发指南、每 Phase 三件套、PR 三道人工闸门;DoD 的人工审查不可豁免 |
| 私有区文件泄漏 | 私有文档出现在公开提交/PR 中 | 4.7 的提交检查 + `.gitignore` 兜底;一旦泄漏按事故处理:清除公开历史并复盘 |

---

## 10. 附录

### A. 命令速查表

| 目的 | 命令 | 来源 |
|---|---|---|
| 安装 specify CLI | `uv tool install specify-cli` | spec-kit |
| 初始化(Copilot 技能模式,默认) | `specify init . --integration copilot` | spec-kit |
| 刷新项目文件(存量) | `specify init --here --force --integration copilot` | spec-kit |
| CLI 自检/升级 | `specify self check` / `specify self upgrade` | spec-kit |
| 查看集成列表 | `specify integration list` | spec-kit |
| 制定/落地宪章 | `/speckit.constitution <原则>`(内容来自开发指南) | spec-kit |
| 写规格 | `/speckit.specify <做什么>` | spec-kit |
| 消歧 | `/speckit.clarify [焦点]` | spec-kit |
| 技术方案 | `/speckit.plan <技术栈>` | spec-kit |
| 质量清单 | `/speckit.checklist` | spec-kit |
| 任务拆分 | `/speckit.tasks` | spec-kit |
| 一致性分析 | `/speckit.analyze` | spec-kit |
| 实现 | `/speckit.implement` | spec-kit |
| 收敛检查 | `/speckit.converge` | spec-kit |
| 建立隔离工作树 | `git worktree add .worktrees/<分支> -b <分支>`(先 `git check-ignore -q .worktrees`) | superpowers 约定 |
| 红阶段提交 | `git commit -m "test: add failing test for <X>"` | 本规范约定 |
| 绿阶段提交 | `git commit -m "feat: implement <X>"` | 本规范约定 |
| 重构提交 | `git commit -m "refactor: clean up <X>"` | 本规范约定 |
| 移除工作树 | `git worktree remove <路径>` + `git worktree prune` | superpowers 约定 |

### B. 关键产物速查

| 产物 | 位置 | 由谁生成 | 谁评审 |
|---|---|---|---|
| 开发指南(总纲) | `docs/dev-guides/<名称>-guide.md` | Copilot Chat(brainstorming 后) | 需求方/团队 |
| Phase 文档 | `docs/phases/<名称>-phase-<NN>.md` | Copilot Chat(由路线图条目实例化) | 团队 |
| 项目宪章 | `.specify/memory/constitution.md` | `/speckit.constitution`(内容来自开发指南) | 团队 |
| 特性规格 | `specs/<分支>/spec.md` | `/speckit.specify` | 人 |
| 技术方案 | `specs/<分支>/plan.md` | `/speckit.plan` | 人 |
| 任务清单 | `specs/<分支>/tasks.md` | `/speckit.tasks` | 人 |
| 质量清单 | `specs/<分支>/checklists/*.md` | `/speckit.checklist` | 评审人打勾 |
| 当前特性指针 | `.specify/feature.json` | 命令自动维护 | 无需评审 |
| Copilot 指令 | `.github/copilot-instructions.md` | 团队手工 | 团队 |

> 上表全部产物均位于私有区,不入公开仓库(见 4.7)。

### C. 参考资料

- spec-kit 仓库:https://github.com/github/spec-kit(本机分析副本:`research/spec-kit/`,含 `README.zh-CN.md`、`spec-driven.md`、`docs/quickstart.md`、`docs/guides/evolving-specs.md`)
- spec-kit 官方文档站:https://github.github.io/spec-kit/
- superpowers 仓库:https://github.com/obra/superpowers(本机分析副本:`research/superpowers/`,含 README、`skills/*/SKILL.md`)
- superpowers 方法论发布文:https://blog.fsck.com/2025/10/09/superpowers/

---

*本文档随工具版本演进定期复审(建议每季度一次,配合 `specify self check`),所有修订通过 git 提交留痕。*
