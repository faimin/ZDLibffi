# ZDLibffi

[![pod lib lint](https://github.com/faimin/ZDLibffi/actions/workflows/podliblint.yml/badge.svg)](https://github.com/faimin/ZDLibffi/actions/workflows/podliblint.yml)
[![Version](https://img.shields.io/cocoapods/v/ZDLibffi.svg?style=flat)](https://cocoapods.org/pods/ZDLibffi)
[![License](https://img.shields.io/cocoapods/l/ZDLibffi.svg?style=flat)](https://cocoapods.org/pods/ZDLibffi)
[![Platform](https://img.shields.io/cocoapods/p/ZDLibffi.svg?style=flat)](https://cocoapods.org/pods/ZDLibffi)


## Introduction：

[libffi v3.4.3](https://github.com/libffi/libffi/releases/tag/v3.4.3) source code that support `module`

## Env：

> [libffi v3.4.3](https://github.com/libffi/libffi/releases/tag/v3.4.3) 
>
> Xcode 13.4.1 
>
> MacOS 12.6

## Compile source code：

1. `sh autogen.sh`
2. `python generate-darwin-source-and-headers.py --only-ios`
3. open `libffi.xcodeproj`
4. select scheme `libffi-iOS` and device `Generic iOS Device`
4. click `Product - Build`
If success, you would see a `Product/libffi.a` in the side bar, you can right click it to get the lib in the finder.

## Installation

Libffi_iOS is available through [CocoaPods](https://cocoapods.org). To install
it, simply add the following line to your Podfile:

```ruby
pod 'ZDLibffi'
```

## Author

faimin, fuxianchao@gmail.com

## Thanks：

- [how to compile for iOS](https://github.com/libffi/libffi/issues/510#issuecomment-654689416)

## License

Libffi_iOS is available under the MIT license. See the LICENSE file for more info.
