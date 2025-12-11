# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2025-11-07

### Added
- Initial release

## [0.1.1] - 2025-11-07

### Fixed
- Fixed git action release workflows

## [0.1.2] - 2025-11-07

### Fixed
- Renamed `accounts` endpoint to correct `account`

## [0.1.3] - 2025-11-07

### Fixed
- Add `safe_countries` to `UserData` model

## [0.1.4] - 2025-12-08

### Fixed

- `UserData` model fields `safe_countries` and `proxy_access` changed to `Optional` (#5)
- `status` field validation in `DevicesEndpoint.list_all_devices()` (#6)
- types in `CreateDeviceFormData` and `ModifyDeviceFormData`

## [0.1.5] - 2025-12-11

### Fixed

- Update `do` field in `Action` model to be optional
