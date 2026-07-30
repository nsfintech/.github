# nsfintech/.github

nsfintech 组织的公共模板仓库，存放组织级可复用 workflow 与 starter 模板，供组织内各仓库按需引入。用 tag 做版本管理（见末尾）。

## 提供的能力

### branch-cleanup：延迟删除分支

合并或关闭未合并的分支，超过保留期（默认 14 天）后自动删除，替代 GitHub 自带的「合并即秒删」。每日定时巡扫。

- **删除**：有已合并 / 已关闭未合并 PR、且超过保留期的分支。
- **跳过**：默认分支、受保护分支、有 open PR 的分支、没有任何已关闭 PR 的分支。
- **不碰**：tag 与 release（只处理 `refs/heads/*`）。

文件：可复用 workflow [`branch-cleanup.yml`](.github/workflows/branch-cleanup.yml) / starter 模板 [`workflow-templates/branch-cleanup.yml`](workflow-templates/branch-cleanup.yml)。

**如何使用**（某仓库）：

1. 关掉仓库自带的秒删（必须）：Settings -> General -> Pull Requests -> 取消 "Automatically delete head branches"；或 `gh api -X PATCH repos/nsfintech/<repo> -F delete_branch_on_merge=false`。
2. 加 caller stub：Actions -> New workflow -> 搜 "Branch cleanup" -> 采用；或手动新建 `.github/workflows/branch-cleanup.yml`：
   ```yaml
   name: Branch cleanup
   on:
     schedule:
       - cron: '17 3 * * *'
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
       uses: nsfintech/.github/.github/workflows/branch-cleanup.yml@v1
       with:
         retention-days: 14
         dry-run: ${{ inputs.dry-run == true }}
       secrets: inherit
   ```
3. 先 dry-run 试跑确认，再让定时任务正式跑（定时 workflow 只在默认分支生效）。

可配置项（`with:`）：

| 输入 | 类型 | 默认 | 说明 |
| --- | --- | --- | --- |
| `retention-days` | number | `14` | 合并/关闭后保留多少天（`0` = 下次巡扫即删） |
| `dry-run` | boolean | `false` | 试运行，只列不删 |
| `exclude-patterns` | string | `''` | 额外永不删除的分支名 glob，逗号分隔，如 `release/*,hotfix/*` |

### release-please：自动版本发布

基于 Conventional Commits 自动管理版本号、CHANGELOG 与 GitHub release（封装 `googleapis/release-please-action@v4`）。

**工作机制**（Release-PR 门禁）：

1. 往 main 推 Conventional Commits（`feat:`/`fix:`/`BREAKING CHANGE` 等）。
2. release-please 自动算版本号（semver：feat→minor、fix→patch、breaking→major），开/更新一个 `chore(main): release X.Y.Z` PR（含 CHANGELOG）。
3. 合并该 PR → 自动打 tag + 发 GitHub release + 改版本号文件（如 `Cargo.toml`）。

文件：可复用 workflow [`release-please.yml`](.github/workflows/release-please.yml) / starter 模板 [`workflow-templates/release-please.yml`](workflow-templates/release-please.yml)。

**如何使用**（某仓库）：

1. 确保提交信息遵循 Conventional Commits（`feat:`/`fix:`/`ci:` 等）。
2. 加 caller stub：Actions -> New workflow -> 搜 "Release please" -> 采用；或手动新建 `.github/workflows/release-please.yml`：
   ```yaml
   name: release-please
   on:
     push:
       branches: [main]
   permissions:
     contents: write
     issues: write
     pull-requests: write
   jobs:
     release-please:
       uses: nsfintech/.github/.github/workflows/release-please.yml@v1
       with:
         release-type: rust   # 按项目改：rust/node/python/go/java/simple；多包 workspace 省略此项并加 release-please-config.json
       secrets: inherit
   ```
3. 之后推 `feat:`/`fix:` 到 main，release-please 会自动开 release PR；合并即发版。

可配置项（`with:`）：

| 输入 | 类型 | 默认 | 说明 |
| --- | --- | --- | --- |
| `release-type` | string | - | `rust`/`node`/`python`/`go`/`java`/`simple` 等；省略则用仓库内 `release-please-config.json`（多包 workspace） |
| `token` | string | `GITHUB_TOKEN` | 默认调用方 token；若需 release PR 触发其它 workflow，传 PAT/App token |

**Rust workspace**：单版本 workspace（如 gateway，`[workspace.package] version`）可直接 `release-type: rust`；多包独立版本则省略 `release-type`，在仓库加 `release-please-config.json` 描述各组件。

## 权限

两个 workflow 都靠 `permissions:` 键授予所需 scope（branch-cleanup 需 `contents: write` + `pull-requests: read`；release-please 需 `contents: write` + `issues: write` + `pull-requests: write`）。本组织默认 workflow 权限为只读，但 workflow 内显式声明 `permissions:` 即可，**无需 PAT / GitHub App**。

**release-please 额外前提**：它用 GITHUB_TOKEN 创建 release PR，需要组织开启「Allow GitHub Actions to create and approve pull requests」（组织 Settings -> Actions -> General）。本组织已开启；若未开启，建 PR 会报 `GitHub Actions is not permitted to create or approve pull requests`，需开启该设置或改用 PAT/App token（传 `token` 输入）。

注意：GITHUB_TOKEN 创建的 release PR 不会触发其它 workflow 的 `on: pull_request`；若需 release PR 跑 CI，传 PAT/App token。

## 版本管理

本仓库用 tag 做版本管理，调用方按需 pin：

- `@v1`：major tag，跟随 v1.x 最新稳定提交（非破坏性更新自动生效）。**推荐**。
- `@v1.1.0`：精确版本，完全固定，追求可复现时用。
- 破坏性变更发布 `@v2`，`@v1` 不会跟进。

当前最新：`v1.1.0`。本仓库自身用 release-please 自动发版（`.github/workflows/release.yml`）；每次发版自动把 `@v1` 前移到新版本，调用方 `@v1` 自动跟进非破坏性更新。

## 备注

- 各仓库需自行 opt-in（GitHub 没有「自动注入所有仓库」的机制）。
- 想保留 `release/*`、`hotfix/*` 等长期分支：传 `exclude-patterns`（branch-cleanup），或给它们加 branch protection（受保护分支会被自动跳过）。
