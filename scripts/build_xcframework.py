#!/usr/bin/env python3

import argparse
import shutil
import subprocess
from pathlib import Path


COMMON_C_SOURCES = [
    "src/common/closures.c",
    "src/common/debug.c",
    "src/common/dlmalloc.c",
    "src/common/java_raw_api.c",
    "src/common/prep_cif.c",
    "src/common/raw_api.c",
    "src/common/tramp.c",
    "src/common/types.c",
]

ARCH_SOURCES = {
    "arm64": [
        "src/aarch64/ffi_arm64.c",
        "src/aarch64/sysv_arm64.S",
    ],
    "arm64_32": [
        "src/aarch64/ffi_arm64_32.c",
        "src/aarch64/sysv_arm64_32.S",
    ],
    "x86_64": [
        "src/x86/ffi64_x86_64.c",
        "src/x86/ffiw64_x86_64.c",
        "src/x86/unix64_x86_64.S",
    ],
}

TARGETS = [
    {
        "name": "ios-arm64",
        "sdk": "iphoneos",
        "target": "arm64-apple-ios10.0",
        "arch": "arm64",
        "output_group": "ios-device",
    },
    {
        "name": "iossim-arm64",
        "sdk": "iphonesimulator",
        "target": "arm64-apple-ios10.0-simulator",
        "arch": "arm64",
        "output_group": "ios-simulator",
    },
    {
        "name": "iossim-x86_64",
        "sdk": "iphonesimulator",
        "target": "x86_64-apple-ios10.0-simulator",
        "arch": "x86_64",
        "output_group": "ios-simulator",
    },
    {
        "name": "macos-arm64",
        "sdk": "macosx",
        "target": "arm64-apple-macos11.0",
        "arch": "arm64",
        "output_group": "macos",
    },
    {
        "name": "macos-x86_64",
        "sdk": "macosx",
        "target": "x86_64-apple-macos10.12",
        "arch": "x86_64",
        "output_group": "macos",
    },
    {
        "name": "catalyst-arm64",
        "sdk": "macosx",
        "target": "arm64-apple-ios13.1-macabi",
        "arch": "arm64",
        "output_group": "maccatalyst",
    },
    {
        "name": "catalyst-x86_64",
        "sdk": "macosx",
        "target": "x86_64-apple-ios13.1-macabi",
        "arch": "x86_64",
        "output_group": "maccatalyst",
    },
    {
        "name": "tvos-arm64",
        "sdk": "appletvos",
        "target": "arm64-apple-tvos10.0",
        "arch": "arm64",
        "output_group": "tvos-device",
    },
    {
        "name": "tvossim-arm64",
        "sdk": "appletvsimulator",
        "target": "arm64-apple-tvos10.0-simulator",
        "arch": "arm64",
        "output_group": "tvos-simulator",
    },
    {
        "name": "tvossim-x86_64",
        "sdk": "appletvsimulator",
        "target": "x86_64-apple-tvos10.0-simulator",
        "arch": "x86_64",
        "output_group": "tvos-simulator",
    },
    {
        "name": "watchos-arm64",
        "sdk": "watchos",
        "target": "arm64-apple-watchos3.0",
        "arch": "arm64",
        "output_group": "watchos-device",
    },
    {
        "name": "watchos-arm64_32",
        "sdk": "watchos",
        "target": "arm64_32-apple-watchos3.0",
        "arch": "arm64_32",
        "output_group": "watchos-device",
    },
    {
        "name": "watchsim-arm64",
        "sdk": "watchsimulator",
        "target": "arm64-apple-watchos3.0-simulator",
        "arch": "arm64",
        "output_group": "watchos-simulator",
    },
    {
        "name": "watchsim-x86_64",
        "sdk": "watchsimulator",
        "target": "x86_64-apple-watchos3.0-simulator",
        "arch": "x86_64",
        "output_group": "watchos-simulator",
    },
    {
        "name": "xros-arm64",
        "sdk": "xros",
        "target": "arm64-apple-xros1.0",
        "arch": "arm64",
        "output_group": "xros-device",
    },
    {
        "name": "xrsim-arm64",
        "sdk": "xrsimulator",
        "target": "arm64-apple-xros1.0-simulator",
        "arch": "arm64",
        "output_group": "xros-simulator",
    },
    {
        "name": "xrsim-x86_64",
        "sdk": "xrsimulator",
        "target": "x86_64-apple-xros1.0-simulator",
        "arch": "x86_64",
        "output_group": "xros-simulator",
    },
]

GROUP_ORDER = [
    "ios-device",
    "ios-simulator",
    "macos",
    "maccatalyst",
    "tvos-device",
    "tvos-simulator",
    "watchos-device",
    "watchos-simulator",
    "xros-device",
    "xros-simulator",
]


def run(cmd):
    subprocess.check_call(cmd)


def sdk_path(sdk):
    return subprocess.check_output(
        ["xcrun", "--sdk", sdk, "--show-sdk-path"],
        text=True,
    ).strip()


def compile_static_lib(source_root: Path, build_root: Path, target_def):
    name = target_def["name"]
    sdk = target_def["sdk"]
    triple = target_def["target"]
    arch_key = target_def["arch"]

    target_dir = build_root / name
    if target_dir.exists():
        shutil.rmtree(target_dir)
    obj_dir = target_dir / "objects"
    obj_dir.mkdir(parents=True, exist_ok=True)

    include_flags = [
        f"-I{source_root / 'include'}",
        f"-I{source_root / 'src' / 'aarch64'}",
        f"-I{source_root / 'src' / 'x86'}",
        f"-I{source_root / 'src' / 'common'}",
    ]

    common_flags = [
        "-target",
        triple,
        "-isysroot",
        sdk_path(sdk),
        "-fembed-bitcode-marker",
        "-fvisibility=hidden",
        "-DUSE_DL_PREFIX=1",
        "-DHAVE_MORECORE=0",
        "-Wno-unused-command-line-argument",
    ] + include_flags

    sources = COMMON_C_SOURCES + ARCH_SOURCES[arch_key]
    objects = []

    for src_rel in sources:
        src_path = source_root / src_rel
        obj_path = obj_dir / (src_path.stem + ".o")
        cmd = [
            "xcrun",
            "--sdk",
            sdk,
            "clang",
        ] + common_flags + [
            "-c",
            str(src_path),
            "-o",
            str(obj_path),
        ]
        run(cmd)
        objects.append(obj_path)

    out_lib = target_dir / "libZDLibffi.a"
    run([
        "xcrun",
        "--sdk",
        sdk,
        "libtool",
        "-static",
        "-o",
        str(out_lib),
    ] + [str(obj) for obj in objects])

    return out_lib


def lipo_merge(output: Path, inputs):
    if len(inputs) == 1:
        shutil.copy2(inputs[0], output)
        return

    output.parent.mkdir(parents=True, exist_ok=True)
    run([
        "xcrun",
        "lipo",
        "-create",
        *[str(lib) for lib in inputs],
        "-output",
        str(output),
    ])


def main():
    parser = argparse.ArgumentParser(description="Build all-platform ZDLibffi.xcframework")
    parser.add_argument("--source", default="Source", help="Path to Source directory")
    parser.add_argument("--output", default="XCFramework/ZDLibffi.xcframework", help="Output xcframework path")
    parser.add_argument("--build-dir", default="build/xcframework", help="Temporary build directory")
    args = parser.parse_args()

    source_root = Path(args.source).resolve()
    output_path = Path(args.output).resolve()
    build_root = Path(args.build_dir).resolve()
    headers_path = source_root / "include"

    if not source_root.exists():
        raise FileNotFoundError(f"source dir not found: {source_root}")

    if build_root.exists():
        shutil.rmtree(build_root)
    build_root.mkdir(parents=True, exist_ok=True)

    libs_by_group = {group: [] for group in GROUP_ORDER}

    for target in TARGETS:
        lib_path = compile_static_lib(source_root, build_root, target)
        libs_by_group[target["output_group"]].append(lib_path)

    final_libs = []
    merged_dir = build_root / "merged"
    merged_dir.mkdir(parents=True, exist_ok=True)

    for group in GROUP_ORDER:
        libs = libs_by_group[group]
        if not libs:
            continue
        merged = merged_dir / f"libZDLibffi-{group}.a"
        lipo_merge(merged, libs)
        final_libs.append(merged)

    if output_path.exists():
        shutil.rmtree(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    cmd = ["xcodebuild", "-create-xcframework"]
    for lib in final_libs:
        cmd.extend(["-library", str(lib), "-headers", str(headers_path)])
    cmd.extend(["-output", str(output_path)])
    run(cmd)


if __name__ == "__main__":
    main()
