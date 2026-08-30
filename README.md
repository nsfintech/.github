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
| `exclude-patterns` | string | `''` | 额外永不删除的分支名 glob，逗号分隔，如 `release/*,hotfix/*,test` |

### release-please：自动版本发布

基于 Conventional Commits 自动管理版本号、CHANGELOG 与 GitHub release（基于自建 fork [`nsfintech/release-please`](https://github.com/nsfintech/release-please)，编译后通过内联 JS driver 直接调其 JS API `Manifest.fromConfig` / `createReleases` / `createPullRequests`——与官方 `googleapis/release-please-action` 同款入口；这样组织内可用上 fork 里对 Rust workspace 共享版本 `version.workspace = true` 的修复，也能按分支切 rc 预发布）。

**工作机制**（Release-PR 门禁，stable + rc 双通道）：

- **stable（main）**：往 main 推 Conventional Commits -> release-please 自动算版本号（semver：feat->minor、fix->patch、breaking->major），开/更新 `chore(main): release X.Y.Z` PR -> 合并 -> 自动打 `vX.Y.Z` tag + 发 GitHub release + 改版本号文件（如 `Cargo.toml`）。
- **rc 预发布（test）**：往 test 推 Conventional Commits -> release-please 开/更新 `chore(test): release X.Y.Z-rc.N` PR -> 合并 -> 自动打 `vX.Y.Z-rc` / `vX.Y.Z-rc.1` / `vX.Y.Z-rc.2` ... tag（首个 rc 无编号，后续递增）+ 发 **GH prerelease**。rc **不写 `CHANGELOG.md`**（留 GH Release notes，避免与 main 的 CHANGELOG 冲突）、**不前移 major tag**、**不打 docker `latest`**。test 合并到 main 后**自动 graduation**（见下）。

**分支与发布模型**（采用 rc 通道的仓库）：

| 分支 | 从哪拉 | 合并到 | release-please | 产出 |
| --- | --- | --- | --- | --- |
| `feature/*` | `test` | `test` | 不跑 | - |
| `hotfix/*` | `main` | `main` + `test` | 不跑 | - |
| `test` | - | `main`（晋升时） | prerelease 模式 | `vX.Y.Z-rc.N` |
| `main` | - | - | stable 模式 | `vX.Y.Z` |

- feature 从 test 拉（test 是集成分支，承载在途工作）；合并到 test 切 rc。
- **hotfix 从 main 拉**（不碰 test 未验证工作），修完合并回 main（切 patch stable）**并回合并到 test**（让 test 不落后于 main）。hotfix 的验证在 hotfix 分支自身 CI 完成，不进 test 的验证队列。
- `test` 是长期分支，需在 branch-cleanup 里 `exclude-patterns: test` 排除。

**graduation（test -> main 晋升 stable，自动）**：合并 test -> main 后，main 上 release-please **自动**开 `chore(main): release X.Y.Z` PR（合并即打 `vX.Y.Z` stable tag）。这依赖自建 fork（[`nsfintech/release-please`](https://github.com/nsfintech/release-please)）的改动：stable 模式找 baseline 时跳过 prerelease tag，所以 rc tag 进 main 后不会被当作"最近 release"，main 仍以最近 stable 为基线、从其后的 conventional commit 算出 stable 版本（`rc.N -> X.Y.Z`）。mainline release-please 做不到（[googleapis/release-please#2515](https://github.com/googleapis/release-please/issues/2515)），故 fork 加了此能力。

人工门禁是"合并 test -> main"这个动作本身--stable 发版时机由人决定（合并即发）。rc 本身也全自动（`rc` -> `rc.1` -> `rc.2`）。

文件：可复用 workflow [`release-please.yml`](.github/workflows/release-please.yml) / starter 模板 [`workflow-templates/release-please.yml`](workflow-templates/release-please.yml)。

**App token（GitHub App 认证）**：本 workflow 不用默认 `GITHUB_TOKEN`，而是自动从**自托管 runner** 读 GitHub App 凭证（Client ID 走 `.env`，私钥 PEM 以文件放 runner 上），用 `actions/create-github-app-token@v3` 换 installation token 来开 release PR / 推 tag。原因：`GITHUB_TOKEN` 开的 PR 是 `github-actions[bot]`，其触发的 `pull_request` workflow 会被 GitHub 挂成 `action_required` 待 maintainer 审批（如各仓 rust-ci 就被挡）；`GITHUB_TOKEN` 推的 tag 也不触发下游 `on: push: tags` workflow（如 docker-build-push）。换成 App 身份（可信协作者）后两者都通。凭证放 runner 是因为 nsfintech 是 Free 组织、无私有仓 org 级 secrets（与 `DOCKER_*` 同一思路）；**caller 仓库无需再配 token / secret**。

**一次性组织配置**（org admin 做一次，所有仓库通用）：

1. 建 GitHub App：`github.com/organizations/nsfintech/settings/apps` -> New GitHub App。Webhook 取消 Active；Repository permissions 只把 Contents / Pull requests / Issues 三项设为 **Read and write**，其余 No access。Create。
2. 记下 **Client ID**（形如 `Iv1.xxxxx`）；General 页底部 Private keys -> Generate a private key（`.pem`）下载。
3. 安装 App：App 设置 -> Install App -> nsfintech -> **All repositories**（或所有当前+未来仓库）-> Install。
4. 把凭证配到**每台**自托管 runner 上，改完重启 runner 加载：
   - Client ID 放 runner `.env`（与 `DOCKER_*` 同处）：
     ```
     RELEASE_PLEASE_APP_CLIENT_ID=Iv1.xxxxx
     ```
   - 私钥 PEM **以文件**放 runner 上（如 `/etc/nsfintech/release-please-app.pem`，`chmod 600`），`.env` 里配路径：
     ```
     RELEASE_PLEASE_APP_PRIVATE_KEY_FILE=/etc/nsfintech/release-please-app.pem
     ```
     私钥不塞 env 变量、不做任何编码——PEM 本来就是多行文件，直接 cat 读最稳。

未配凭证时本 workflow 自动回退 `GITHUB_TOKEN`（旧行为：release PR 被审批门禁挡、tag 不触发下游），不影响运行。App token 在同一 job 内换取并使用，无需 `skip-token-revoke`。

**如何使用**（某仓库）：

1. 确保提交信息遵循 Conventional Commits（`feat:`/`fix:`/`ci:` 等）。
2. 加 caller stub：Actions -> New workflow -> 搜 "Release please" -> 采用；或手动新建 `.github/workflows/release-please.yml`：
   ```yaml
   name: release-please
   on:
     push:
       branches: [main, test]
   permissions:
     contents: write
     issues: write
     pull-requests: write
   jobs:
     release-please:
       uses: nsfintech/.github/.github/workflows/release-please.yml@v1
       with:
         release-type: rust   # 按项目改：rust/node/python/go/java/simple；多包 workspace 省略此项并加 release-please-config.json
         prerelease: ${{ github.ref_name == 'test' }}   # test 切 rc，main 切 stable
         prerelease-type: rc
       secrets: inherit
   ```
3. 推 `feat:`/`fix:` 到 test -> 合并 rc release PR 切 `vX.Y.Z-rc.N`；test 合并到 main -> 合并 stable release PR 切 `vX.Y.Z`。只想要 stable、不要 rc 通道的仓库，`branches: [main]` 并去掉 `prerelease` 两行即可。

可配置项（`with:`）：

| 输入 | 类型 | 默认 | 说明 |
| --- | --- | --- | --- |
| `release-type` | string | - | `rust`/`node`/`python`/`go`/`java`/`simple` 等；省略则用仓库内 `release-please-config.json`（多包 workspace） |
| `release-please-ref` | string | `main` | fork（`nsfintech/release-please`）的分支/commit/tag；默认 `main` 跟随最新，需要可复现时固定到 commit |
| `token` | string | `GITHUB_TOKEN` | 默认调用方 token；若需 release PR/tag 触发其它 workflow，传 PAT/App token |
| `prerelease` | boolean | `false` | `true`=预发布模式，切 `vX.Y.Z-rc.N`（不前移 major tag、不写 `CHANGELOG.md`）；caller 按分支传，如 `${{ github.ref_name == 'test' }}` |
| `prerelease-type` | string | `rc` | 预发布类型，生成 `vX.Y.Z-rc.N` |

**输出**（供 caller 发版后处理用）：`release_created`（本次是否创建 release）、`tag_name`（如 `v1.1.0` 或 `v1.1.0-rc.3`）、`prerelease`（本次 release 是否预发布——caller 前移 major tag 等作业据此跳过 rc）。

**多包 workspace 限制**：省略 `release-type`、用 `release-please-config.json` 的多包仓库，`prerelease`/`prerelease-type` 输入不生效（CLI 非 manifest 路径不走 input）；需在该 config 文件里配 `prerelease`/`prerelease-type`，但这是全局的（main 也会跟着 rc），故多包仓库暂不建议用 per-branch rc 通道。

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
| `prebuilt-artifact` | string | `''` | 前置构建产物 artifact 名（如 `web-dist`）；非空则 clippy job 先下载并解压到 `prebuilt-path`，用于「Rust 编译期嵌入前端产物」场景（见下） |
| `prebuilt-path` | string | `''` | 前置产物解压目标路径，相对仓库根（如 `web/dist`）；仅 `prebuilt-artifact` 非空时生效 |

**cargo-deny 审计范围**：

- `advisories`：依赖是否命中 RUSTSEC 已知漏洞 / yanked 版本。
- `licenses`：依赖许可证是否在 `deny.toml` 白名单（防意外引入 GPL/AGPL 等传染性 license）。
- `bans`：禁用特定 crate（默认 deny `openssl`/`openssl-sys`，强制 rustls；可按仓库在 `deny.toml` 调整）。
- `sources`：限制依赖来源（只允许 crates.io，禁 git 依赖）。

**前后端混合仓库（Rust 嵌入前端产物）**：rsflow 这类 monorepo 用 rust-embed 把 `web/dist` 嵌进二进制，clippy 编译期需要 dist 存在，但 CI 机器不该为跑 Rust 门禁装 node。做法：同 run 内先用 node-ci 模板构建前端并上传 artifact，再 `needs` 串联 rust-ci 并传 `prebuilt-artifact`，clippy job 会把产物解压到 `web/dist` 后再编译：

```yaml
jobs:
  web-build:
    uses: nsfintech/.github/.github/workflows/node-ci.yml@v1
    with:
      node-version: '24'
      working-directory: web
      build: pnpm run build
      artifact-name: web-dist
      artifact-path: dist
  rust-ci:
    needs: web-build
    uses: nsfintech/.github/.github/workflows/rust-ci.yml@v1
    with:
      prebuilt-artifact: web-dist
      prebuilt-path: web/dist
    secrets: inherit
```

（调用方仓库需自行保证 build.rs 在「有 dist 无 node_modules」时跳过前端构建，参考 `nsfintech/rsflow` 的 `crates/rsflow-agent/build.rs`。）

### node-ci：Node 质量门禁 + 构建

对 Node/前端项目跑统一 CI：安装依赖，可选 lint / test / build，可选上传构建产物 artifact。环境用 setup action 引入（`actions/setup-node` + `pnpm/action-setup`），**不要求 runner 宿主机预装 node**；pnpm 版本优先读 `package.json` 的 `packageManager` 字段（推荐用它固定版本），否则用 `pnpm-version` 输入。

两种用法：

- **纯前端仓库**：直接当 CI 用，配 `lint` / `test` / `build` 命令。
- **前后端混合仓库**：只配 `build` + `artifact-name`，产物交给同 run 的 rust-ci clippy job 消费（见上一节示例，首个用户 `nsfintech/rsflow`）。

文件：可复用 workflow [`node-ci.yml`](.github/workflows/node-ci.yml) / starter 模板 [`workflow-templates/node-ci.yml`](workflow-templates/node-ci.yml)。

**前提**：仓库有对应包管理器的 lockfile（pnpm-lock.yaml / package-lock.json，安装用 frozen/ci 模式保证可复现）；用 pnpm 时建议在 `package.json` 加 `"packageManager": "pnpm@<版本>"`。

**如何使用**（某前端仓库）：

1. 加 caller stub：Actions -> New workflow -> 搜 "Node CI" -> 采用；或手动新建 `.github/workflows/node-ci.yml`：
   ```yaml
   name: node-ci
   on:
     push:
       branches: [main]
     pull_request:
   permissions:
     contents: read
   jobs:
     node-ci:
       uses: nsfintech/.github/.github/workflows/node-ci.yml@v1
       secrets: inherit
   ```
2. 按项目配 `with:` 输入（命令、目录、产物等，见下表）。

可配置项（`with:`）：

| 输入 | 类型 | 默认 | 说明 |
| --- | --- | --- | --- |
| `node-version` | string | `22` | Node 版本（传给 actions/setup-node） |
| `working-directory` | string | `.` | 前端项目目录，相对仓库根（monorepo 子目录如 `web`） |
| `package-manager` | string | `pnpm` | `pnpm` 或 `npm`（决定 action-setup 与缓存方式；各命令输入需自行匹配） |
| `pnpm-version` | string | `''` | pnpm 版本；空则读 `package.json` 的 `packageManager` 字段 |
| `install` | string | `''` | 安装命令；空则按包管理器取默认（pnpm: `pnpm install --frozen-lockfile` / npm: `npm ci`） |
| `lint` | string | `''` | lint 命令；空则跳过 |
| `test` | string | `''` | test 命令；空则跳过（需外部服务的 e2e 不适用） |
| `build` | string | `''` | 构建命令；空则跳过 |
| `artifact-name` | string | `''` | 构建产物 artifact 名；空则不上传 |
| `artifact-path` | string | `dist` | 构建产物路径，相对 `working-directory` |

### docker-build-push：构建并推送 Docker 镜像

构建 Docker 镜像并推送到腾讯云 TCR 私有仓库。release-please 打 `v*` tag 时触发（含 stable `v1.2.3` 与预发布 `v1.2.3-rc.1`），打 `semver`/`sha`/`latest` 标签；也支持手动 `workflow_dispatch` 测试构建。

**认证不走 GitHub secret**：nsfintech 是 Free 组织，私有仓库用不了 org 级 secrets；凭证（`DOCKER_REGISTRY`/`DOCKER_NAMESPACE`/`DOCKER_USERNAME`/`DOCKER_PASSWORD`）配在**自托管 runner 的 `.env`** 里，workflow 启动时桥接到 `$GITHUB_ENV`（并 `add-mask`）。`DOCKER_USERNAME`/`DOCKER_PASSWORD` 用 **TCR 服务级账号**（永不过期），不是 1h 临时登录指令。

**tag 策略**（metadata-action）：

| 触发 | 产出 tag |
| --- | --- |
| 所有 | `sha-<短sha>`（可追溯）|
| `v*` stable tag（release-please 发版）| `v1.2.3` / `1.2.3` / `1.2` / `1`（semver）|
| `v*` 预发布 tag（`v1.2.3-rc.1`）| `v1.2.3-rc.1` / `1.2.3-rc.1`（semver，**不打 `latest`**，适合测试环境）|
| `v*` stable tag（非预发布）| `latest`（`flavor: latest=auto`，手动 dispatch / 预发布 tag 不打）|

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

**注意（tag 触发的坑）**：release-please 用默认 `GITHUB_TOKEN` 打的 tag **不会**触发本 stub 的 `on: push: tags`（`GITHUB_TOKEN` 推送不触发下游 workflow）。要让 stable/rc tag 自动构建镜像，需给 release-please 传 PAT/GitHub App token（见「权限」节）；否则用 `workflow_dispatch` 手动构建。

可配置项（`with:`）：

| 输入 | 类型 | 默认 | 说明 |
| --- | --- | --- | --- |
| `image-name` | string | 仓库名 | 镜像名（不含 registry/namespace）；需子分组传 `team/repo` |
| `context` | string | `.` | 构建上下文 |
| `file` | string | `./Dockerfile` | Dockerfile 路径 |
| `target` | string | 空 | 多阶段构建目标 stage |
| `platforms` | string | `linux/amd64` | 构建平台；多架构需调用方自行加 `setup-qemu` |
| `push` | boolean | `true` | 是否推送；`false` 只构建（测 Dockerfile）|
| `cache-type` | string | `registry` | 缓存后端：`registry`（存 TCR `:buildcache`，无限制，默认）/ `gha`（GitHub cache，self-hosted 易 400）/ `none` |
| `latest` | boolean | `true` | `true`=`auto`（跟最新非预发布 tag）/ `false`=不打 `latest` |
| `build-args` | string | 空 | 多行 `KEY=VALUE` |
| `build-command` | string | 空 | 可选：buildx 前在 runner 上执行的多行命令（默认空）。用于先编译/生成产物再打包（如 `cargo build` 后把二进制拷进 context 目录，再让 `context` 指向该目录只做运行镜像），编译复用 runner 的 `~/.cargo/registry` + `target` 缓存，镜像不装编译器。执行前会用 `dtolnay/rust-toolchain` 装 Rust（版本见 `build-command-toolchain`） |
| `build-command-toolchain` | string | `stable` | `build-command` 用的 Rust toolchain（默认 `stable`）；仅 `build-command` 非空时生效 |
| `provenance` | boolean | `false` | OCI provenance attestation（TCR 默认关）|

**输出**（供下游消费）：`image` —— 本次构建推送的主镜像完整地址 `registry/namespace/name:tag`。tag 规则：push tag 事件=`github.ref_name`（如 `v1.2.3` / `v1.2.3-rc.1`），`workflow_dispatch`=`sha-<短sha>`。下游（如 deploy-tke）用 `needs.<build>.outputs.image` 拿到。

**缓存**：默认 `type=registry,mode=max`（缓存存 TCR `<image>:buildcache` tag，mode=max 含多阶段中间层；无 10G/7天 限制，不依赖 GitHub cache 服务）。self-hosted runner 上 `type=gha` 易因 GitHub cache 服务 400 报错导致构建失败，故默认走 registry；可选 `gha`（GitHub-hosted runner 适用）或 `none`（关缓存）。

### deploy-tke：构建后自动部署到 TKE

构建完镜像后，把完整镜像地址自动部署到腾讯云 TKE 集群。与 docker-build-push 串成一条链：release-please 打 `v*` tag → 构建推送 → 拿 `outputs.image` → 部署。

**关键是覆盖首次部署**：集群里可能完全没有该服务，所以不是 `kubectl set image`，而是把调用方仓库里的**全套清单**（kustomize 渲染 + `${IMAGE}` 注入）一次 `kubectl apply --wait`，Namespace/Deployment/Service/ConfigMap/Secret 等全部就位。

文件：可复用 workflow [`deploy-tke.yml`](.github/workflows/deploy-tke.yml) / starter 模板 [`workflow-templates/deploy-tke.yml`](workflow-templates/deploy-tke.yml)。

**前提**（自托管 runner `.env`，与 docker-build-push 同一套思路，Free 组织私有仓库用不了 org 级 secrets）：

- 必填：`TKE_SECRET_ID` / `TKE_SECRET_KEY`（腾讯云 API 凭证，TKE 专用；workflow 内桥接到 `TENCENTCLOUD_SECRET_ID/KEY` 供 tccli 认证。改完重启 runner 加载）。
- 可选：`DOCKER_REGISTRY` / `DOCKER_NAMESPACE` / `DOCKER_USERNAME` / `DOCKER_PASSWORD`（复用于 docker-build-push 的服务级账号，用于自动确保 `imagePullSecret`）。
- 腾讯云账号需为集群 owner，或已给 TKE RBAC 授权的子账号（取 kubeconfig 后才有权限 apply）。
- 默认走**内网** kubeconfig：自托管 runner 需与集群在同一 VPC / 已打通内网；跨公网连需集群开公网访问并传 `extranet: true`。

**清单契约**（调用方服务仓库需满足）：

1. 仓库有 kustomization 目录（默认 `deploy/`，含 `kustomization.yaml` 与 Deployment/Service 等）。
2. Deployment 的 `image` 字段写占位 `image: ${IMAGE}`（envsubst 只认 `${IMAGE}` 这种形式）。
3. Deployment 引用 `imagePullSecrets`，名字与模板 `image-pull-secret` 输入一致（默认 `regcred`）。

**如何使用**（某仓库）：

1. 满足上面「清单契约」，把部署清单放进 `deploy/`（或改 `manifests` 输入指向其它目录）。
2. 加 caller stub：Actions -> New workflow -> 搜 "Build & deploy to TKE" -> 采用；或手动新建 `.github/workflows/build-and-deploy-tke.yml`：
   ```yaml
   name: build-and-deploy-tke
   on:
     push:
       tags: ['v*']
     workflow_dispatch:
       inputs:
         push:
           description: '推送镜像到 TCR(false 则只构建)'
           type: boolean
           default: true
         deploy:
           description: '推完是否部署到 TKE(false 防误部署)'
           type: boolean
           default: false
   concurrency:
     group: deploy-${{ github.ref }}
     cancel-in-progress: false
   permissions:
     contents: read
   jobs:
     build:
       uses: nsfintech/.github/.github/workflows/docker-build-push.yml@v1
       with:
         push: ${{ github.event_name == 'push' || inputs.push }}
     deploy:
       needs: build
       if: ${{ github.event_name == 'push' || inputs.deploy }}
       uses: nsfintech/.github/.github/workflows/deploy-tke.yml@v1
       with:
         image: ${{ needs.build.outputs.image }}
         cluster-id: cls-xxxxxxxx   # 改成目标集群 ID
         region: ap-guangzhou       # 集群所在地域
         namespace: default
         manifests: deploy
   ```
3. release-please 合并 release PR -> 自动打 `v*` tag -> 构建推送 + 部署。手动测试：Actions -> Run workflow（`deploy`=true 才部署）。

**rc/stable 分环境**：默认所有 `v*` tag 部署到同一个 cluster-id。想 rc→测试、stable→生产（各一个 TKE 集群），复制 deploy job：

```yaml
  deploy-test:
    needs: build
    if: ${{ contains(github.ref_name, '-rc') }}
    uses: nsfintech/.github/.github/workflows/deploy-tke.yml@v1
    with:
      image: ${{ needs.build.outputs.image }}
      cluster-id: cls-test    # 测试集群
      namespace: default
      manifests: deploy

  deploy-prod:
    needs: build
    if: ${{ !contains(github.ref_name, '-rc') }}
    uses: nsfintech/.github/.github/workflows/deploy-tke.yml@v1
    with:
      image: ${{ needs.build.outputs.image }}
      cluster-id: cls-prod    # 生产集群
      namespace: default
      manifests: deploy
```

可配置项（`with:`）：

| 输入 | 类型 | 默认 | 说明 |
| --- | --- | --- | --- |
| `image` | string | - | 要部署的镜像完整地址（来自 `needs.<build>.outputs.image`） |
| `cluster-id` | string | - | TKE 集群 ID（形如 `cls-xxxxxxxx`），`DescribeClusterKubeconfig` 按此取 kubeconfig |
| `region` | string | `ap-guangzhou` | 集群所在地域 |
| `namespace` | string | `default` | 目标命名空间；确保存在（无则创建）。资源实际落点由清单决定 |
| `manifests` | string | `deploy` | 调用方仓库内 kustomization 根目录 |
| `image-pull-secret` | string | `regcred` | TCR 拉取凭证 Secret 名；runner `.env` 有 `DOCKER_*` 时自动确保存在 |
| `extranet` | boolean | `false` | `true` 用公网 kubeconfig（需集群开公网访问）；默认内网（runner 需在集群 VPC 内） |
| `timeout` | string | `5m` | `kubectl apply --wait` 超时（仅普通资源） |
| `create-only-kinds` | string | -（空） | 仅首次创建、已存在则跳过不覆盖的资源类型（逗号分隔，如 `ConfigMap,Secret`）；该 kind 的资源只在集群中不存在时才 apply。也可不传，改在单个资源上加 annotation `deploy-tke.nsfintech.io/create-only: "true"` 标记（两者取并集） |

**create-only（仅首次创建，不覆盖已有）**：有些资源（典型 `ConfigMap`/`Secret` 这类初始化配置）部署后可能被运维手动调整，不该被流水线每次 apply 覆盖。本 workflow 渲染后按标记分流——普通资源照常 `kubectl apply --wait`（声明式同步）；create-only 资源逐个 `kubectl get` 判断，集群中不存在才 apply，已存在则跳过。两种标记方式（取并集）：

1. **按 kind 批量**：传 `create-only-kinds: ConfigMap,Secret`，该 kind 全部资源视为 create-only。
2. **精确到单个资源**：在资源 `metadata.annotations` 加 `deploy-tke.nsfintech.io/create-only: "true"`，只标记这一个资源（同 kind 下可个别例外）。

```yaml
# 例 1:所有 ConfigMap/Secret 都只在首次创建(caller stub 的 with:)
deploy:
  uses: nsfintech/.github/.github/workflows/deploy-tke.yml@v1
  with:
    create-only-kinds: ConfigMap,Secret

# 例 2:只标记某个 ConfigMap(调用方清单里)
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
  annotations:
    deploy-tke.nsfintech.io/create-only: "true"
data:
  log-level: info   # 首次部署写入,后续运维手动改 log-level 不会被流水线覆盖
```

分流依赖 yq（把 kustomize 的 YAML 多文档转 JSON Lines）+ jq（按 annotation/kind 筛选）；yq 由 `step-security/setup-yq@v1` 自动安装（pin 到 v4，setup-yq 默认的 v3 语法不兼容），无需 runner 预装。

**注意（tag 触发的坑）**：与 docker-build-push 相同——release-please 用默认 `GITHUB_TOKEN` 打的 tag 不会触发本 stub 的 `on: push: tags`。需给 release-please 传 PAT/App token（见「权限」节）；否则用 `workflow_dispatch` 手动构建+部署。

## 权限

六个 workflow 都靠 `permissions:` 键授予所需 scope（branch-cleanup 需 `contents: write` + `pull-requests: read`；release-please 需 `contents: write` + `issues: write` + `pull-requests: write`；rust-ci、node-ci 与 deploy-tke 需 `contents: read`，rust-ci 的 clippy job 另需 `actions: read` 以取同 run 前置 job 的 artifact；docker-build-push 需 `contents: read`）。本组织默认 workflow 权限为只读，但 workflow 内显式声明 `permissions:` 即可，**无需 PAT / GitHub App**。**docker-build-push 推 TCR、deploy-tke 取 kubeconfig，都用 runner `.env` 里的服务级账号凭证（`DOCKER_*` / `TKE_SECRET_*`），不需要 GitHub secret 或 `packages: write`。**

**release-please 额外前提**：它用 GITHUB_TOKEN 创建 release PR，需要组织开启「Allow GitHub Actions to create and approve pull requests」（组织 Settings -> Actions -> General）。本组织已开启；若未开启，建 PR 会报 `GitHub Actions is not permitted to create or approve pull requests`，需开启该设置或改用 PAT/App token（传 `token` 输入）。

注意：GITHUB_TOKEN 创建的 release PR 不会触发其它 workflow 的 `on: pull_request`；同样，GITHUB_TOKEN 推的 tag 不会触发 `on: push: tags`（如 docker-build-push stub）。若需 release PR 跑 CI、或 tag 自动触发下游构建，传 PAT/App token。

## 版本管理

本仓库用 tag 做版本管理，调用方按需 pin：

- `@v1`：major tag，跟随 v1.x 最新稳定提交（非破坏性更新自动生效）。**推荐**。
- `@v1.1.0`：精确版本，完全固定，追求可复现时用。
- 破坏性变更发布 `@v2`，`@v1` 不会跟进。

当前最新：`v1.1.0`。本仓库自身用 release-please 自动发版（`.github/workflows/release.yml`）；每次发版自动把 `@v1` 前移到新版本，调用方 `@v1` 自动跟进非破坏性更新。

## 备注

- 各仓库需自行 opt-in（GitHub 没有「自动注入所有仓库」的机制）。
- 想保留 `release/*`、`hotfix/*`、`test` 等长期分支：传 `exclude-patterns`（branch-cleanup），或给它们加 branch protection（受保护分支会被自动跳过）。
