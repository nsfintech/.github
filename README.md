# nsfintech/.github

nsfintech 组织的公共 `.github` 仓库：存放组织级**可复用 workflow** 和**模板**，供组织内各仓库按需引入。本仓库为 **public**（内容仅为 CI/模板，不含业务代码或密钥）。

> 后续会逐步加入更多公共能力（通用社区健康文件、Rust CI 等）。当前只包含「延迟删除分支」。

---

## 已有能力：延迟删除分支（branch-cleanup）

替代 GitHub 自带的 "Automatically delete head branches"（合并即秒删），改为：**分支在 PR 合并、或 PR 关闭未合并后，保留 14 天再自动删除**。

- 跳过：默认分支、受保护分支、有 open PR 的分支、没有任何已关闭 PR 的分支。
- 保留天数可配置（默认 14）。
- 逻辑在可复用 workflow [`/.github/workflows/branch-cleanup.yml`](.github/workflows/branch-cleanup.yml) 里；各仓库通过一个 caller stub 每天定时调用它。

### 工作机制

GitHub Actions 无法「睡 14 天」，所以采用**每日定时巡扫**：每天跑一次，列出本仓库所有非受保护分支，对每个分支查其最近一个已关闭 PR 的合并/关闭时间，超过保留期就删。可复用 workflow 跑在**调用方仓库的上下文**里（用的是调用方的 token、作用于调用方仓库），所以一份逻辑服务所有仓库。

### 在某个仓库启用（以 `gateway` 为例）

1. **关闭 GitHub 自带的秒删**（必须，否则延迟无意义）：
   - 仓库 Settings → General → Pull Requests → 取消勾选 "Automatically delete head branches"；
   - 或命令行：`gh api -X PATCH repos/nsfintech/gateway -f delete_branch_on_merge=false`。
2. **添加 caller stub**，二选一：
   - 仓库 Actions 标签页 → New workflow → 搜索 "Branch cleanup" → 采用（会把 starter 模板复制进仓库）；或
   - 手动新建 `.github/workflows/branch-cleanup.yml`，内容见 [`/workflow-templates/branch-cleanup.yml`](workflow-templates/branch-cleanup.yml)。
3. **先试跑**：Actions → "Branch cleanup" → Run workflow → 勾选 `dry-run` → 查看日志里「将删除」的分支是否符合预期。
4. 确认无误后，正式的每日定时巡扫会在默认分支上自动运行。

> 注意：**定时 workflow 只在调用仓库的默认分支上生效**，stub 文件必须存在于默认分支。GitHub 没有「自动把 workflow 注入所有仓库」的机制，所以每个仓库需按上面步骤 opt-in。

### 可配置项（在 caller stub 的 `with:` 里调整）

| 输入 | 类型 | 默认 | 说明 |
| --- | --- | --- | --- |
| `retention-days` | number | `14` | 合并/关闭后保留多少天 |
| `dry-run` | boolean | `false` | 试运行，只列不删 |
| `exclude-patterns` | string | `''` | 额外永不删除的分支名 glob，逗号分隔，如 `release/*,hotfix/*` |

示例：保留 7 天、且永不删 `release/*`：

```yaml
jobs:
  sweep:
    uses: nsfintech/.github/.github/workflows/branch-cleanup.yml@main
    with:
      retention-days: 7
      exclude-patterns: 'release/*,hotfix/*'
    secrets: inherit
```

### 权限

caller stub 和可复用 workflow 都声明了 `permissions: contents: write`（删除分支引用需要）。若仓库 Settings → Actions → General → Workflow permissions 设为 "Read-only"，需改为 "Read and write permissions" 或保持 workflow 内显式声明。

---

## 让本仓库自己也清理分支（可选）

`.github` 仓库本身也有分支，若想让本仓库也按规则清理，把 caller stub 同样加到本仓库的 `.github/workflows/` 即可（自调用，作用于自身）。

## 版本管理建议

当前 caller stub 引用 `@main`。稳定后建议给本仓库打 tag（如 `v1`），各调用方改为 `@v1`，这样共享 workflow 的改动不会一次性冲击所有仓库，升级由各仓库自行决定。
