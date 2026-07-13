# ZDLibffi

[![CI](https://github.com/faimin/ZDLibffi/actions/workflows/CI.yml/badge.svg)](https://github.com/faimin/ZDLibffi/actions/workflows/CI.yml)
[![Version](https://img.shields.io/cocoapods/v/ZDLibffi.svg?style=flat)](https://cocoapods.org/pods/ZDLibffi)
[![License](https://img.shields.io/cocoapods/l/ZDLibffi.svg?style=flat)](https://cocoapods.org/pods/ZDLibffi)
[![Platform](https://img.shields.io/cocoapods/p/ZDLibffi.svg?style=flat)](https://cocoapods.org/pods/ZDLibffi)

## Introduction

`ZDLibffi` packages [libffi v3.7.1](https://github.com/libffi/libffi/releases/tag/v3.7.1) for Apple platforms and supports modular imports.

## Installation

### CocoaPods

Add the pod in your `Podfile`:

```ruby
pod 'ZDLibffi'
```

### Swift Package Manager

Add the dependency in your `Package.swift`:

```swift
dependencies: [
    .package(url: "https://github.com/faimin/ZDLibffi.git", from: "0.371.0")
]
```

Or add it via Xcode: File → Add Package Dependencies, then enter the repository URL.

## CI

This project uses GitHub Actions for continuous integration. The workflow runs automatically on pushes to `main`/`master` and on all pull requests.

### What CI Checks

| Job | Description |
|-----|-------------|
| **Pod Lib Lint** | Validates the podspec on each Apple platform (ios, macos, watchos, tvos, visionos), both with and without modular headers |
| **SPM Build** | Validates `Package.swift` and builds the package with SwiftPM |

### Running CI Locally

You can replicate the CI checks on your machine:

```bash
# CocoaPods lint (replace PLATFORM with ios/macos/watchos/tvos/visionos)
pod lib lint ZDLibffi.podspec --allow-warnings --platforms=ios --skip-tests
pod lib lint ZDLibffi.podspec --allow-warnings --platforms=ios --use-modular-headers --skip-tests

# SwiftPM
swift package describe
swift build
```

### Triggering CI

- Push to `main` or `master` branch
- Open or update a pull request targeting any branch

## One-Click Upgrade

Use the built-in script to upgrade libffi source and regenerate the xcframework:

```bash
./scripts/upgrade_libffi.sh --libffi-version 3.7.1 --pod-version 0.371.0
```

What this script does:

1. Downloads the official `libffi` release tarball.
2. Regenerates `Source/` headers and source files for modern Apple architectures.
3. Builds `XCFramework/ZDLibffi.xcframework`.
4. Updates version references in `ZDLibffi.podspec` and `README.md`.

Options:

| Flag | Description |
|------|-------------|
| `--libffi-version` | Target libffi version (e.g. `3.7.1`) |
| `--pod-version` | Pod version string (defaults to `0.<version_digits>.0`) |
| `--skip-xcframework` | Skip the xcframework build step |

## XCFramework

`ZDLibffi.xcframework` is no longer committed to the repository. You can build it locally or download it from CI.

### Build Locally

```bash
python3 scripts/build_xcframework.py \
  --source Source \
  --output XCFramework/ZDLibffi.xcframework \
  --build-dir build/xcframework
```

### Download from CI

Go to **Actions → CI → Run workflow** and trigger a manual build. The xcframework will be available as a downloadable artifact.

### Supported Slices

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
