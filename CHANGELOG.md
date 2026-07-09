# Changelog

All notable changes to django-jet-calm will be documented in this file.

## [Unreleased]

## [5.4.7] - 2026-07-09

### Security
- Upgraded DOMPurify to 3.4.11 to address XSS bypass vulnerabilities
- Upgraded Django to 5.2.16 to address CVE-2026-48588, CVE-2026-53877, and CVE-2026-53878

### Changed
- Rebuilt frontend bundle (`bundle.min.js`)

## [5.4.6] - 2026-07-02

### Added
- Backend coverage gate in CI with a 75% threshold (`backend-coverage` workflow).
- Expanded tests for filter and utility helpers.

### Changed
- Configured pytest coverage defaults in `pyproject.toml` (production code only; tests omitted).

## [5.4.5] - 2026-06-26

### Changed
- Upgraded backend Python dependency constraints across package metadata and requirements.
- Bumped Django from 5.2.14 to 5.2.15.
- Aligned and pinned `six` and `django-rangefilter` declarations in backend dependency manifests.

## [5.4.4] - 2026-06-12

### Fixed
- Restored test suite compatibility with Django 5.2 admin APIs (#68)

### Changed
- Bumped `shell-quote` to 1.8.4 (#67)

## [5.4.3] - 2026-05-23

### Security
- Hardened jQuery UI timepicker against XSS (CodeQL alerts, #66)
- Upgraded Django to 5.2.14 to address CVE-2026-5766 (GHSA-w26r-rmm8-9c29)
- Pinned transitive `qs` to 6.15.2 to address CVE-2026-8723 (GHSA-q8mj-m7cp-5q26)

### Changed
- Rebuilt frontend bundle (`bundle.min.js`)
- Bumped PostCSS, DOMPurify, and js-cookie dependencies

## [5.3.14] - 2026-04-11

### Security
- Upgraded Django to 5.2.13 to address security vulnerabilities
- Fixed related popup URL encoding with `encodeURIComponent` to prevent XSS vulnerabilities (#58)

### Changed
- Updated PostCSS configuration (#57)

## [5.3.13] - Previous Release

See git history for details.
