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

基于 Conventional Commits 自动管理版本号、CHANGELOG 与 GitHub release（基于自建 fork [`nsfintech/release-please`](https://github.com/nsfintech/release-please) 跑 release-please CLI，非官方 `googleapis/release-please-action`；这样组织内可用上 fork 里对 Rust workspace 共享版本 `version.workspace = true` 的修复）。

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
| `release-please-ref` | string | `main` | fork（`nsfintech/release-please`）的分支/commit/tag；默认 `main` 跟随最新，需要可复现时固定到 commit |
| `token` | string | `GITHUB_TOKEN` | 默认调用方 token；若需 release PR 触发其它 workflow，传 PAT/App token |

**Rust workspace**：单版本 workspace（如 gateway，`[workspace.package] version`）可直接 `release-type: rust`；多包独立版本则省略 `release-type`，在仓库加 `release-please-config.json` 描述各组件。

**主动指定版本号**（`Release-As`）：需要强制某个版本（如新项目从 `0.1.0` 起、或某次跳到 `1.0.0`）时，在提交 body 加 `Release-As: X.Y.Z`（大小写不敏感），release-please 下次发版即用该版本、忽略 commit 类型；一次性，发完恢复自动 bump。

```bash
# 新项目从 0.1.0 起
git commit --allow-empty -m "chore: start versioning at 0.1.0" -m "Release-As: 0.1.0"
# 某次跳到 1.0.0
git commit --allow-empty -m "chore: graduate to 1.0.0" -m "Release-As: 1.0.0"
```

持久/初始配置，或 0.x 的 bump 策略（`bump-minor-pre-major` 等），可在仓库内 `release-please-config.json` 设置（此时 caller stub 省略 `release-type`）。

### rust-ci：Rust 质量门禁

对 Rust 项目跑统一质量门禁：`cargo fmt --check` + `cargo clippy -D warnings` + `cargo deny check`（供应链审计：漏洞 / 许可证 / 禁用 crate / 来源）。三个 job 并行，只读权限，无需 PAT。

**不含测试**——测试模式因项目而异（单 crate / workspace / nextest / e2e 需外部服务），后续单独做测试模板；需要测试的仓库自行加 job。

文件：可复用 workflow [`rust-ci.yml`](.github/workflows/rust-ci.yml) / starter 模板 [`workflow-templates/rust-ci.yml`](workflow-templates/rust-ci.yml)。

**前提**：调用方仓库根需有 `deny.toml`（cargo-deny 配置，per-repo；各仓库依赖不同，不共享）。无则 cargo-deny 用内置默认（较严格，可能直接红），可参考 `nsfintech/gateway` 的 deny.toml 起一份。

**如何使用**（某 Rust 仓库）：

1. 在仓库根加 `deny.toml`（参考 gateway，或 `cargo deny init` 生成模板后定制）。
2. 加 caller stub：Actions -> New workflow -> 搜 "Rust CI" -> 采用；或手动新建 `.github/workflows/rust-ci.yml`：
   ```yaml
   name: rust-ci
   on:
     push:
       branches: [main]
     pull_request:
   permissions:
     contents: read
   jobs:
     rust-ci:
       uses: nsfintech/.github/.github/workflows/rust-ci.yml@v1
       secrets: inherit
   ```
3. 推 main 或开 PR，fmt / clippy / deny 三个 job 并行跑；任一失败即门禁红。

可配置项（`with:`）：

| 输入 | 类型 | 默认 | 说明 |
| --- | --- | --- | --- |
| `toolchain` | string | `stable` | Rust toolchain channel（stable/beta/nightly 或具体版本）；edition 2024 需 1.85+ |

**cargo-deny 审计范围**：

- `advisories`：依赖是否命中 RUSTSEC 已知漏洞 / yanked 版本。
- `licenses`：依赖许可证是否在 `deny.toml` 白名单（防意外引入 GPL/AGPL 等传染性 license）。
- `bans`：禁用特定 crate（默认 deny `openssl`/`openssl-sys`，强制 rustls；可按仓库在 `deny.toml` 调整）。
- `sources`：限制依赖来源（只允许 crates.io，禁 git 依赖）。

### docker-build-push：构建并推送 Docker 镜像

构建 Docker 镜像并推送到腾讯云 TCR 私有仓库。release-please 打 `v*` tag 时触发，打 `semver`/`sha`/`latest` 标签；也支持手动 `workflow_dispatch` 测试构建。

**认证不走 GitHub secret**：nsfintech 是 Free 组织，私有仓库用不了 org 级 secrets；凭证（`DOCKER_REGISTRY`/`DOCKER_NAMESPACE`/`DOCKER_USERNAME`/`DOCKER_PASSWORD`）配在**自托管 runner 的 `.env`** 里，workflow 启动时桥接到 `$GITHUB_ENV`（并 `add-mask`）。`DOCKER_USERNAME`/`DOCKER_PASSWORD` 用 **TCR 服务级账号**（永不过期），不是 1h 临时登录指令。

**tag 策略**（metadata-action）：

| 触发 | 产出 tag |
| --- | --- |
| 所有 | `sha-<短sha>`（可追溯）|
| `v*` tag（release-please 发版）| `v1.2.3` / `1.2.3` / `1.2` / `1`（semver）|
| `v*` tag（非预发布）| `latest`（`flavor: latest=auto`，手动 dispatch / 预发布 tag 不打）|

文件：可复用 workflow [`docker-build-push.yml`](.github/workflows/docker-build-push.yml) / starter 模板 [`workflow-templates/docker-build-push.yml`](workflow-templates/docker-build-push.yml)。

**前提**：自托管 runner 已配 `.env`（4 个 `DOCKER_*` 变量、服务级账号凭证、已重启加载）；调用方仓库根有 `Dockerfile`（默认 `./Dockerfile`）。

**如何使用**（某仓库）：

1. 确认仓库已有 `Dockerfile`（路径非默认则用 `file` 输入指定）。
2. 加 caller stub：Actions -> New workflow -> 搜 "Docker build & push" -> 采用；或手动新建 `.github/workflows/docker-build-push.yml`：
   ```yaml
   name: docker-build-push
   on:
     push:
       tags: ['v*']
     workflow_dispatch:
       inputs:
         push:
           description: '推送镜像(false 则只构建,用于测试 Dockerfile)'
           type: boolean
           default: true
   permissions:
     contents: read
   jobs:
     docker:
       uses: nsfintech/.github/.github/workflows/docker-build-push.yml@v1
       with:
         push: ${{ github.event_name == 'push' || inputs.push }}
   ```
3. release-please 合并 release PR -> 自动打 `v*` tag -> 本 workflow 触发，构建并推送 `semver`/`sha`/`latest` 镜像。手动测试：Actions -> Run workflow（`push`=true 推 `sha` 测试镜像可拉取运行；`push`=false 只构建验证 Dockerfile）。

可配置项（`with:`）：

| 输入 | 类型 | 默认 | 说明 |
| --- | --- | --- | --- |
| `image-name` | string | 仓库名 | 镜像名（不含 registry/namespace）；需子分组传 `team/repo` |
| `context` | string | `.` | 构建上下文 |
| `file` | string | `./Dockerfile` | Dockerfile 路径 |
| `target` | string | 空 | 多阶段构建目标 stage |
| `platforms` | string | `linux/amd64` | 构建平台；多架构需调用方自行加 `setup-qemu` |
| `push` | boolean | `true` | 是否推送；`false` 只构建（测 Dockerfile）|
| `cache-type` | string | `gha` | 缓存后端：`gha`（10G/7天）/ `registry`（存 TCR `:buildcache`，无限制）/ `none` |
| `latest` | boolean | `true` | `true`=`auto`（跟最新非预发布 tag）/ `false`=不打 `latest` |
| `build-args` | string | 空 | 多行 `KEY=VALUE` |
| `provenance` | boolean | `false` | OCI provenance attestation（TCR 默认关）|

**缓存**：默认 `type=gha,mode=max`（缓存多阶段中间层）。tag 触发间隔 >7 天时 gha 会 evict 导致冷构建，可切 `cache-type: registry`（缓存存 TCR `<image>:buildcache` tag，无大小/时间限制）。

## 权限

四个 workflow 都靠 `permissions:` 键授予所需 scope（branch-cleanup 需 `contents: write` + `pull-requests: read`；release-please 需 `contents: write` + `issues: write` + `pull-requests: write`；rust-ci 与 docker-build-push 只需 `contents: read`）。本组织默认 workflow 权限为只读，但 workflow 内显式声明 `permissions:` 即可，**无需 PAT / GitHub App**。**docker-build-push 推 TCR 用 runner `.env` 里的服务级账号凭证，不需要 GitHub secret 或 `packages: write`。**

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
