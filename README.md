# nsfintech/.github

nsfintech 组织的公共模板仓库，存放组织级可复用 workflow 与 starter 模板，供组织内各仓库按需引入。

## 提供的能力

### branch-cleanup：延迟删除分支

合并或关闭未合并的分支，超过保留期（默认 14 天）后自动删除，替代 GitHub 自带的「合并即秒删」。每日定时巡扫。

- **删除**：有已合并 / 已关闭未合并 PR、且超过保留期的分支。
- **跳过**：默认分支、受保护分支、有 open PR 的分支、没有任何已关闭 PR 的分支。
- **不碰**：tag 与 release（只处理 `refs/heads/*`）。

文件：

- 可复用 workflow：[`.github/workflows/branch-cleanup.yml`](.github/workflows/branch-cleanup.yml)
- starter 模板：[`workflow-templates/branch-cleanup.yml`](workflow-templates/branch-cleanup.yml)（各仓库 Actions → New workflow 搜 "Branch cleanup" 可一键添加 caller stub）

## 如何使用

以某仓库为例：

1. **关掉仓库自带的秒删**（必须，否则分支一合并就被删）：
   Settings → General → Pull Requests → 取消 "Automatically delete head branches"；或
   ```bash
   gh api -X PATCH repos/nsfintech/<repo> -F delete_branch_on_merge=false
   ```
2. **添加 caller stub**（二选一）：
   - 仓库 Actions → New workflow → 搜 "Branch cleanup" → 采用；或
   - 手动新建 `.github/workflows/branch-cleanup.yml`：
   ```yaml
   name: Branch cleanup
   on:
     schedule:
       - cron: '17 3 * * *'   # 每天 03:17 UTC 巡扫
     workflow_dispatch:
       inputs:
         dry-run:
           description: 试运行（只列不删）
           type: boolean
           default: false
   permissions:
     contents: write
     pull-requests: read
   jobs:
     sweep:
       uses: nsfintech/.github/.github/workflows/branch-cleanup.yml@main
       with:
         retention-days: 14
         dry-run: ${{ inputs.dry-run == true }}
       secrets: inherit
   ```
3. **先 dry-run 试跑**：Actions → "Branch cleanup" → Run workflow → 勾选 `dry-run`，确认日志里"将删除"的分支符合预期。
4. 正式运行后每日定时自动巡扫（定时 workflow 只在**默认分支**上生效，stub 须存在于默认分支）。

## 可配置项（caller stub 的 `with:`）

| 输入 | 类型 | 默认 | 说明 |
| --- | --- | --- | --- |
| `retention-days` | number | `14` | 合并/关闭后保留多少天（`0` = 下次巡扫即删） |
| `dry-run` | boolean | `false` | 试运行，只列不删 |
| `exclude-patterns` | string | `''` | 额外永不删除的分支名 glob，逗号分隔，如 `release/*,hotfix/*` |

## 权限

caller stub 已声明 `permissions: contents: write, pull-requests: read`（删分支引用需 `contents: write`；查 PR 需 `pull-requests: read`）。本组织默认 workflow 权限为只读，但 workflow 内显式声明 `permissions:` 即可授予所需权限，**无需 PAT / GitHub App**。

## 备注

- 各仓库需自行 opt-in（GitHub 没有「自动注入所有仓库」的机制）。
- 想保留 `release/*`、`hotfix/*` 等长期分支：传 `exclude-patterns`，或给它们加 branch protection（受保护分支会被自动跳过）。
- 稳定后建议给本仓库打 tag（如 `v1`），各调用方改用 `@v1`，避免 `@main` 的改动一次性影响所有仓库。
