# Changelog

## [1.14.0](https://github.com/nsfintech/.github/compare/v1.13.1...v1.14.0) (2026-09-10)


### Features

* repsy-publish npm 段支持 napi 标准多平台分包(npm-platform-packages) ([#53](https://github.com/nsfintech/.github/issues/53)) ([763c364](https://github.com/nsfintech/.github/commit/763c364f363e42fd403e0ec01b5c301d502954dc))

## [1.13.1](https://github.com/nsfintech/.github/compare/v1.13.0...v1.13.1) (2026-09-10)


### Bug Fixes

* repsy-publish 交叉工具链改用 nsfintech/actions 的 setup-cross-tools 供给 ([#51](https://github.com/nsfintech/.github/issues/51)) ([ebfd3e3](https://github.com/nsfintech/.github/commit/ebfd3e35eead747a74e65e451e9ecb5ba40a33e0))

## [1.13.0](https://github.com/nsfintech/.github/compare/v1.12.4...v1.13.0) (2026-09-09)


### Features

* repsy-publish 支持交叉编译多平台产物(cross-targets)+ tag 血统校验(require-branch) ([#48](https://github.com/nsfintech/.github/issues/48)) ([451732d](https://github.com/nsfintech/.github/commit/451732dfa0893318d362ec3d566a3d424f6f8389))


### Bug Fixes

* 交叉工具链改 runner 预置,workflow 不装只用 ([#50](https://github.com/nsfintech/.github/issues/50)) ([e2ccbc4](https://github.com/nsfintech/.github/commit/e2ccbc4fdef3508340bdae03db0c8ca69609d305))

## [1.12.4](https://github.com/nsfintech/.github/compare/v1.12.3...v1.12.4) (2026-09-08)


### Bug Fixes

* repsy-publish npm 段补 setup-node(发布 job 独立环境没有 npm) ([#46](https://github.com/nsfintech/.github/issues/46)) ([0c3560e](https://github.com/nsfintech/.github/commit/0c3560e8c3be7add3fa03d13e1788b5e8adea308))

## [1.12.3](https://github.com/nsfintech/.github/compare/v1.12.2...v1.12.3) (2026-09-08)


### Bug Fixes

* repsy cargo registry 补 credential-provider(私有 index 读取必需) ([#43](https://github.com/nsfintech/.github/issues/43)) ([44e555d](https://github.com/nsfintech/.github/commit/44e555d77ce292fc6b0456b64b7528e918de9eae))

## [1.12.2](https://github.com/nsfintech/.github/compare/v1.12.1...v1.12.2) (2026-09-07)


### Bug Fixes

* repsy-publish 加公共 Rust toolchain setup(cargo 段不再裸跑) ([#41](https://github.com/nsfintech/.github/issues/41)) ([bd118cc](https://github.com/nsfintech/.github/commit/bd118ccd6bce7378a8f8ce28b050b1e25b778449))

## [1.12.1](https://github.com/nsfintech/.github/compare/v1.12.0...v1.12.1) (2026-09-07)


### Bug Fixes

* repsy-publish 注入对象修正 + cargo publish 跳过隔离重建 ([#39](https://github.com/nsfintech/.github/issues/39)) ([38b7139](https://github.com/nsfintech/.github/commit/38b7139886fa0814b02e6bb3740df0d02b50f1d0))

## [1.12.0](https://github.com/nsfintech/.github/compare/v1.11.0...v1.12.0) (2026-09-07)


### Features

* 新增 pg-rust-tests 可复用 workflow 与 starter 模板 ([#37](https://github.com/nsfintech/.github/issues/37)) ([d965fd9](https://github.com/nsfintech/.github/commit/d965fd9335c1fc25262ff259a54beff7b912d7a2))

## [1.11.0](https://github.com/nsfintech/.github/compare/v1.10.0...v1.11.0) (2026-09-07)


### Features

* 新增 repsy-publish 可复用 workflow 与 starter 模板 ([#35](https://github.com/nsfintech/.github/issues/35)) ([c74c896](https://github.com/nsfintech/.github/commit/c74c896891684f0e0688e37db44ebbf2eebe3629))

## [1.10.0](https://github.com/nsfintech/.github/compare/v1.9.1...v1.10.0) (2026-09-02)


### Features

* 新增 python-ci 可复用 workflow 与 starter 模板 ([#33](https://github.com/nsfintech/.github/issues/33)) ([8c54fc5](https://github.com/nsfintech/.github/commit/8c54fc5ee775d6da97342140c89187e4221f350e))

## [1.9.1](https://github.com/nsfintech/.github/compare/v1.9.0...v1.9.1) (2026-08-30)


### Bug Fixes

* **rust-ci:** drop clippy job permissions declaration to avoid caller startup_failure ([e8bfbe6](https://github.com/nsfintech/.github/commit/e8bfbe64e49e921aa46f2cb3b6e3f7e28af051de))
* **rust-ci:** drop clippy job permissions declaration to avoid caller startup_failure ([cb2b5e7](https://github.com/nsfintech/.github/commit/cb2b5e7d6e485d20b98c6b2df175a642e3cc97be))

## [1.9.0](https://github.com/nsfintech/.github/compare/v1.8.0...v1.9.0) (2026-08-30)


### Features

* add node-ci reusable workflow and prebuilt-artifact input for rust-ci ([#29](https://github.com/nsfintech/.github/issues/29)) ([1adbcfc](https://github.com/nsfintech/.github/commit/1adbcfc73692de450d277e535c306a77121b7ad6))

## [1.8.0](https://github.com/nsfintech/.github/compare/v1.7.2...v1.8.0) (2026-08-29)


### Features

* **deploy-tke:** envsubst-vars input for cluster-specific manifest injection ([#27](https://github.com/nsfintech/.github/issues/27)) ([6b8071e](https://github.com/nsfintech/.github/commit/6b8071ee2cf7e818774bd60f3740dd7e338e80fe))

## [1.7.2](https://github.com/nsfintech/.github/compare/v1.7.1...v1.7.2) (2026-08-20)


### Bug Fixes

* **ci:** switch setup-yq to nsfintech fork without subscription check ([#25](https://github.com/nsfintech/.github/issues/25)) ([2e0638f](https://github.com/nsfintech/.github/commit/2e0638f0d48e8f63be9738021d98bfd95159d8d8))

## [1.7.1](https://github.com/nsfintech/.github/compare/v1.7.0...v1.7.1) (2026-08-11)


### Bug Fixes

* **ci:** add create-only mode to deploy-tke to skip existing resources ([#23](https://github.com/nsfintech/.github/issues/23)) ([66a0f08](https://github.com/nsfintech/.github/commit/66a0f081f7c9ea8183b69f4842df2837f01666dc))

## [1.7.0](https://github.com/nsfintech/.github/compare/v1.6.0...v1.7.0) (2026-08-10)


### Features

* **ci:** add deploy-tke reusable workflow ([#21](https://github.com/nsfintech/.github/issues/21)) ([e5bba23](https://github.com/nsfintech/.github/commit/e5bba2375f8d8e9a92393ae86da9ad1d8804315d))

## [1.6.0](https://github.com/nsfintech/.github/compare/v1.5.1...v1.6.0) (2026-08-07)


### Features

* **ci:** add optional build-command to docker-build-push reusable workflow ([#19](https://github.com/nsfintech/.github/issues/19)) ([c19a4e0](https://github.com/nsfintech/.github/commit/c19a4e0352de5513a0251e0781782fce734e564d))

## [1.5.1](https://github.com/nsfintech/.github/compare/v1.5.0...v1.5.1) (2026-08-07)


### Bug Fixes

* **ci:** read App private key from a PEM file on the runner, not base64 in .env ([#17](https://github.com/nsfintech/.github/issues/17)) ([238585c](https://github.com/nsfintech/.github/commit/238585cf513ea00cd630fc801951c42e61baf57b))

## [1.5.0](https://github.com/nsfintech/.github/compare/v1.4.0...v1.5.0) (2026-08-07)


### Features

* **ci:** use GitHub App token for release-please ([#15](https://github.com/nsfintech/.github/issues/15)) ([b228f91](https://github.com/nsfintech/.github/commit/b228f91a7f842b401addb413ce2b501a82f5d9b3))

## [1.4.0](https://github.com/nsfintech/.github/compare/v1.3.1...v1.4.0) (2026-08-07)


### Features

* **ci:** add docker build/push reusable workflow ([#12](https://github.com/nsfintech/.github/issues/12)) ([4f6d546](https://github.com/nsfintech/.github/commit/4f6d546a1cf9b7349ae03ed797fca2a47b29918a))
* **ci:** add rc prerelease channel to release-please workflow ([#14](https://github.com/nsfintech/.github/issues/14)) ([728b898](https://github.com/nsfintech/.github/commit/728b898f004e5e6250532e6262d595d60fede996))

## [1.3.1](https://github.com/nsfintech/.github/compare/v1.3.0...v1.3.1) (2026-08-05)


### Bug Fixes

* **ci:** drop rust-cache step from clippy job ([#10](https://github.com/nsfintech/.github/issues/10)) ([89c6d17](https://github.com/nsfintech/.github/commit/89c6d17d95b3944f0ce17c9de157588f35f23975))

## [1.3.0](https://github.com/nsfintech/.github/compare/v1.2.1...v1.3.0) (2026-08-04)


### Features

* **ci:** support self-hosted runner for org workflows ([#8](https://github.com/nsfintech/.github/issues/8)) ([bdc1b72](https://github.com/nsfintech/.github/commit/bdc1b72f95d32ea2680596f8f8dcf173d2add2b0))

## [1.2.1](https://github.com/nsfintech/.github/compare/v1.2.0...v1.2.1) (2026-08-02)


### Bug Fixes

* enable releases for shared-version rust workspaces ([#5](https://github.com/nsfintech/.github/issues/5)) ([81ee586](https://github.com/nsfintech/.github/commit/81ee586df8d943395ed643b980206e22d2c40119))

## [1.2.0](https://github.com/nsfintech/.github/compare/v1.1.0...v1.2.0) (2026-07-31)


### Features

* **ci:** add rust-ci reusable workflow for rust quality gates ([#3](https://github.com/nsfintech/.github/issues/3)) ([6ee2e77](https://github.com/nsfintech/.github/commit/6ee2e77f7dbf7409427054533e774a0abecbda5b))


### Bug Fixes

* place issue templates in .github/ISSUE_TEMPLATE for this repo's own issues ([ea33d8f](https://github.com/nsfintech/.github/commit/ea33d8f5b888d262d9142440f709648c7117db82))
* place PR template in .github/ for this repo's own PRs ([4a2953d](https://github.com/nsfintech/.github/commit/4a2953d07561c96cd9b1856a8a7f5c3a14f39a8f))

## [1.1.0](https://github.com/nsfintech/.github/compare/v1.0.0...v1.1.0) (2026-07-30)


### Features

* **ci:** add release-please reusable workflow and self-release for this repo ([5ad0723](https://github.com/nsfintech/.github/commit/5ad0723711d3693865664b8808a8857ff5f82c4a))
