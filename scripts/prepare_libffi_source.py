#!/usr/bin/env python3

import argparse
import os
import shutil
import subprocess
from pathlib import Path


ARCH_CONFIGS = [
    {
        "name": "arm64",
        "suffix": "arm64",
        "sdk": "iphoneos",
        "target": "arm64-apple-ios",
        "version_min": "-miphoneos-version-min=10.0",
        "condition": "defined(__arm64__) && !defined(__ILP32__)",
        "wrap_prefix": "#if defined(__arm64__) && !defined(__ILP32__)\n\n",
        "wrap_suffix": "\n\n#endif\n",
    },
    {
        "name": "arm64_32",
        "suffix": "arm64_32",
        "sdk": "watchos",
        "target": "arm64_32-apple-watchos",
        "version_min": "-mwatchos-version-min=3.0",
        "condition": "defined(__arm64__) && defined(__ILP32__)",
        "wrap_prefix": "#if defined(__arm64__) && defined(__ILP32__)\n\n",
        "wrap_suffix": "\n\n#endif\n",
    },
    {
        "name": "x86_64",
        "suffix": "x86_64",
        "sdk": "iphonesimulator",
        "target": "x86_64-apple-ios-simulator",
        "version_min": "-miphoneos-version-min=10.0",
        "condition": "defined(__x86_64__)",
        "wrap_prefix": "#ifdef __x86_64__\n\n",
        "wrap_suffix": "\n\n#endif\n",
    },
]

ARCH_BY_NAME = {entry["name"]: entry for entry in ARCH_CONFIGS}


def run(cmd, cwd=None, env=None):
    subprocess.check_call(cmd, cwd=cwd, env=env)


def copy_wrapped_file(src: Path, dst: Path, prefix: str, suffix: str):
    dst.parent.mkdir(parents=True, exist_ok=True)
    with src.open("r", encoding="utf-8") as src_file:
        data = src_file.read()
    with dst.open("w", encoding="utf-8") as dst_file:
        dst_file.write(prefix)
        dst_file.write(data)
        dst_file.write(suffix)


def write_selector_header(output_dir: Path, base_name: str, entries):
    file_path = output_dir / f"{base_name}.h"
    with file_path.open("w", encoding="utf-8") as header:
        for entry in entries:
            suffix = entry["suffix"]
            condition = entry["condition"]
            header.write(f"#if {condition}\n\n")
            header.write(f"#if __has_include(<{base_name}_{suffix}.h>)\n")
            header.write(f"#include <{base_name}_{suffix}.h>\n")
            header.write("#else\n")
            header.write(f"#include \"{base_name}_{suffix}.h\"\n")
            header.write("#endif\n\n\n")
            header.write("#endif\n")


def patch_ffi_common_include(include_dir: Path):
    ffi_common = include_dir / "ffi_common.h"
    content = ffi_common.read_text(encoding="utf-8")
    needle = "#include <fficonfig.h>"
    replacement = (
        "#if __has_include(<fficonfig.h>)\n"
        "#include <fficonfig.h>\n"
        "#elif __has_include(<ZDLibffi/fficonfig.h>)\n"
        "#include <ZDLibffi/fficonfig.h>\n"
        "#else\n"
        "#include \"fficonfig.h\"\n"
        "#endif"
    )
    if needle in content:
        content = content.replace(needle, replacement, 1)
        ffi_common.write_text(content, encoding="utf-8")


def patch_arch_ffi_header_include(header_path: Path):
    content = header_path.read_text(encoding="utf-8")
    needle = "#include <ffitarget.h>"
    replacement = (
        "#if __has_include(<ffitarget.h>)\n"
        "#include <ffitarget.h>\n"
        "#elif __has_include(<ZDLibffi/ffitarget.h>)\n"
        "#include <ZDLibffi/ffitarget.h>\n"
        "#else\n"
        "#include \"ffitarget.h\"\n"
        "#endif"
    )
    if needle in content:
        content = content.replace(needle, replacement, 1)
        header_path.write_text(content, encoding="utf-8")


def prepare_source_tree(libffi_dir: Path, output_dir: Path):
    if output_dir.exists():
        shutil.rmtree(output_dir)

    include_dir = output_dir / "include"
    src_common_dir = output_dir / "src" / "common"
    src_aarch64_dir = output_dir / "src" / "aarch64"
    src_x86_dir = output_dir / "src" / "x86"

    include_dir.mkdir(parents=True, exist_ok=True)
    src_common_dir.mkdir(parents=True, exist_ok=True)
    src_aarch64_dir.mkdir(parents=True, exist_ok=True)
    src_x86_dir.mkdir(parents=True, exist_ok=True)

    # Common sources used across all Apple targets.
    for src_file in sorted((libffi_dir / "src").glob("*.c")):
        shutil.copy2(src_file, src_common_dir / src_file.name)

    arm64 = ARCH_BY_NAME["arm64"]
    arm64_32 = ARCH_BY_NAME["arm64_32"]
    x86_64 = ARCH_BY_NAME["x86_64"]

    # aarch64 source files for arm64 + arm64_32.
    aarch64_src = libffi_dir / "src" / "aarch64"
    copy_wrapped_file(
        aarch64_src / "ffi.c",
        src_aarch64_dir / "ffi_arm64.c",
        arm64["wrap_prefix"],
        arm64["wrap_suffix"],
    )
    copy_wrapped_file(
        aarch64_src / "sysv.S",
        src_aarch64_dir / "sysv_arm64.S",
        arm64["wrap_prefix"],
        arm64["wrap_suffix"],
    )
    copy_wrapped_file(
        aarch64_src / "ffi.c",
        src_aarch64_dir / "ffi_arm64_32.c",
        arm64_32["wrap_prefix"],
        arm64_32["wrap_suffix"],
    )
    copy_wrapped_file(
        aarch64_src / "sysv.S",
        src_aarch64_dir / "sysv_arm64_32.S",
        arm64_32["wrap_prefix"],
        arm64_32["wrap_suffix"],
    )
    shutil.copy2(aarch64_src / "internal.h", src_aarch64_dir / "internal_arm64.h")
    # Keep upstream include name so copied sources compile without patching includes.
    shutil.copy2(aarch64_src / "internal.h", src_aarch64_dir / "internal.h")

    # x86_64 source files.
    x86_src = libffi_dir / "src" / "x86"
    copy_wrapped_file(
        x86_src / "ffi64.c",
        src_x86_dir / "ffi64_x86_64.c",
        x86_64["wrap_prefix"],
        x86_64["wrap_suffix"],
    )
    copy_wrapped_file(
        x86_src / "ffiw64.c",
        src_x86_dir / "ffiw64_x86_64.c",
        x86_64["wrap_prefix"],
        x86_64["wrap_suffix"],
    )
    copy_wrapped_file(
        x86_src / "unix64.S",
        src_x86_dir / "unix64_x86_64.S",
        x86_64["wrap_prefix"],
        x86_64["wrap_suffix"],
    )
    copy_wrapped_file(
        x86_src / "win64.S",
        src_x86_dir / "win64_x86_64.S",
        x86_64["wrap_prefix"],
        x86_64["wrap_suffix"],
    )
    shutil.copy2(x86_src / "internal64.h", src_x86_dir / "internal64.h")
    shutil.copy2(x86_src / "asmnames.h", src_x86_dir / "asmnames.h")

    # Common public headers.
    for header in ["ffi_cfi.h", "ffi_common.h", "tramp.h"]:
        shutil.copy2(libffi_dir / "include" / header, include_dir / header)

    patch_ffi_common_include(include_dir)


def configure_and_generate_headers(libffi_dir: Path, output_dir: Path):
    host_machine = os.uname().machine
    include_output = output_dir / "include"

    for arch in ARCH_CONFIGS:
        build_dir = libffi_dir / f"build_zd_{arch['name']}"
        if build_dir.exists():
            shutil.rmtree(build_dir)
        build_dir.mkdir(parents=True, exist_ok=True)

        env = os.environ.copy()
        env["CC"] = f"xcrun -sdk {arch['sdk']} clang -target {arch['target']}"
        env["LD"] = f"xcrun -sdk {arch['sdk']} ld -target {arch['target']}"
        env["CFLAGS"] = arch["version_min"]

        configure_cmd = [
            "../configure",
            f"--host={arch['target']}",
            f"--build={host_machine}-apple-darwin",
        ]
        run(configure_cmd, cwd=build_dir, env=env)

        suffix = arch["suffix"]
        copy_wrapped_file(
            build_dir / "include" / "ffi.h",
            include_output / f"ffi_{suffix}.h",
            arch["wrap_prefix"],
            arch["wrap_suffix"],
        )
        patch_arch_ffi_header_include(include_output / f"ffi_{suffix}.h")
        copy_wrapped_file(
            build_dir / "fficonfig.h",
            include_output / f"fficonfig_{suffix}.h",
            arch["wrap_prefix"],
            arch["wrap_suffix"],
        )
        copy_wrapped_file(
            build_dir / "include" / "ffitarget.h",
            include_output / f"ffitarget_{suffix}.h",
            arch["wrap_prefix"],
            arch["wrap_suffix"],
        )

    write_selector_header(include_output, "ffi", ARCH_CONFIGS)
    write_selector_header(include_output, "fficonfig", ARCH_CONFIGS)
    write_selector_header(include_output, "ffitarget", ARCH_CONFIGS)


def main():
    parser = argparse.ArgumentParser(
        description="Prepare Source/ tree for ZDLibffi from a libffi release tarball source"
    )
    parser.add_argument("--libffi-dir", required=True, help="Path to extracted libffi source directory")
    parser.add_argument("--output", required=True, help="Output Source directory path")
    args = parser.parse_args()

    libffi_dir = Path(args.libffi_dir).resolve()
    output_dir = Path(args.output).resolve()

    if not libffi_dir.exists():
        raise FileNotFoundError(f"libffi directory not found: {libffi_dir}")

    prepare_source_tree(libffi_dir, output_dir)
    configure_and_generate_headers(libffi_dir, output_dir)


if __name__ == "__main__":
    main()
