# Changelog

All notable changes to django-jet-calm will be documented in this file.

## [Unreleased]

### Security
- Pinned transitive `qs` to 6.15.2 to address CVE-2026-8723 (GHSA-q8mj-m7cp-5q26)

## [5.3.14] - 2026-04-11

### Security
- Upgraded Django to 5.2.13 to address security vulnerabilities
- Fixed related popup URL encoding with `encodeURIComponent` to prevent XSS vulnerabilities (#58)

### Changed
- Updated PostCSS configuration (#57)

## [5.3.13] - Previous Release

See git history for details.
