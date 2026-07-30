# 贡献指南

感谢为 nsfintech 贡献！本指南适用于组织内各仓库；各仓库若有自己的 `CONTRIBUTING.md`，以仓库的为准。

## 开发流程

1. **不要直接 push `main`**。从 `main` 切分支：`git checkout -b feat/<简短描述>`。
2. 按 [Conventional Commits](#提交规范) 写提交。
3. 推分支，开 PR 合并到 `main`。
4. `main` 受 branch protection 保护（要求 PR + 状态检查通过）。

## 提交规范

遵循 [Conventional Commits](https://www.conventionalcommits.org/)：

| 类型 | 用途 |
| --- | --- |
| `feat` | 新功能 |
| `fix` | bug 修复 |
| `ci` | CI / 构建 |
| `docs` | 文档 |
| `refactor` | 重构（不改行为） |
| `test` | 测试 |
| `chore` | 杂项 |

要求：

- **subject 用英文祈使句**，如 `feat: add rate-limit plugin`；可带 scope：`feat(auth): ...`。
- 破坏性变更用 `!`（`feat!:`）或 footer `BREAKING CHANGE: <说明>`。
- 提交信息**全英文**，且**不含 "claude"** 等字样。

## 发版（release-please）

启用 release-please 的仓库，发版全自动：

1. 合并 `feat:`/`fix:` 等 PR 到 `main` -> release-please 自动开 release PR（`chore(main): release X.Y.Z`，含 CHANGELOG）。
2. 合并该 release PR -> 自动打 tag + 发 GitHub release。

要点：

- 版本按提交自动 bump：`feat`->minor、`fix`->patch、breaking->major。
- 多个改动可攒进一个 release（不合并 release PR 就不发版）。
- 强制版本：在提交 body 加 `Release-As: X.Y.Z`。
- 详见 [nsfintech/.github](https://github.com/nsfintech/.github) 的 README。

## 分支清理（branch-cleanup）

启用 branch-cleanup 的仓库，已合并 / 关闭未合并的分支超过保留期（默认 14 天）会被自动删除。

- 不会删：默认分支、受保护分支、有 open PR 的分支、无已关闭 PR 的分支。
- 想 keep 的长期分支（如 `release/*`）：加 branch protection，或在 caller stub 传 `exclude-patterns`。

## 代码规范

以 Rust 仓库（如 `gateway`）为例：

- Rust edition 2024，最新 stable。
- `cargo fmt` + `cargo clippy -D warnings` 必须通过。
- `unsafe_code = "deny"`（确需时局部 `#[allow(unsafe_code)]` 并注明理由）。
- 提交前本地跑 `cargo test`。

各仓库具体规范以其 `CLAUDE.md` / `README.md` 为准。

## Issue 与 PR

- Issue 用仓库的 issue 模板（bug / feature）。
- PR 按模板 checklist 填写。
