# Changelog

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
