# ZDLibffi

[![pod lib lint](https://github.com/faimin/ZDLibffi/actions/workflows/podliblint.yml/badge.svg)](https://github.com/faimin/ZDLibffi/actions/workflows/podliblint.yml)
[![Version](https://img.shields.io/cocoapods/v/ZDLibffi.svg?style=flat)](https://cocoapods.org/pods/ZDLibffi)
[![License](https://img.shields.io/cocoapods/l/ZDLibffi.svg?style=flat)](https://cocoapods.org/pods/ZDLibffi)
[![Platform](https://img.shields.io/cocoapods/p/ZDLibffi.svg?style=flat)](https://cocoapods.org/pods/ZDLibffi)

## Introduction

`ZDLibffi` packages [libffi v3.5.2](https://github.com/libffi/libffi/releases/tag/v3.5.2) for Apple platforms and supports modular imports.

## Installation

Add the pod in your `Podfile`:

```ruby
pod 'ZDLibffi'
```

## One-Click Upgrade

Use the built-in script to upgrade libffi source and regenerate the xcframework:

```bash
./scripts/upgrade_libffi.sh --libffi-version 3.5.2 --pod-version 0.352.0
```

What this script does:

1. Downloads the official `libffi` release tarball.
2. Regenerates `Source/` headers and source files for modern Apple architectures.
3. Builds `XCFramework/ZDLibffi.xcframework`.
4. Updates version references in `ZDLibffi.podspec` and `README.md`.

## XCFramework Coverage

Generated `XCFramework/ZDLibffi.xcframework` contains slices for:

- iOS (device)
- iOS Simulator
- macOS
- Mac Catalyst
- tvOS (device)
- tvOS Simulator
- watchOS (device)
- watchOS Simulator
- visionOS (device)
- visionOS Simulator

## Author

faimin, fuxianchao@gmail.com

## Thanks

- [how to compile for iOS](https://github.com/libffi/libffi/issues/510#issuecomment-654689416)

## License

ZDLibffi is available under the MIT license. See the LICENSE file for more info.
