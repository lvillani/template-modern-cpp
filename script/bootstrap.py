#!/usr/bin/env python3
#
# script/bootstrap.py - Installs dependencies required to build the project
#

import json
import os
import pathlib
import subprocess
import typing

TOP_LEVEL = pathlib.Path(__file__).parent.parent.absolute()
CONAN_DIR = TOP_LEVEL / "conan"


def main():
    setup_conan()


def setup_conan():
    if "default" not in conan_profiles():
        call("uv", "run", "conan", "profile", "detect")

    # fmt: off
    call(
        "uv", "run", "conan",
        "install",
        "--build=missing",
        "--conf", "tools.cmake.cmaketoolchain:generator=Ninja",
        "--output-folder", str(CONAN_DIR),
        *conan_arch(),
        str(TOP_LEVEL),
    )
    # fmt: on


def conan_profiles() -> typing.List[str]:
    return json.loads(
        output("uv", "run", "conan", "profile", "list", "--format", "json")
    )


def conan_arch() -> typing.List[str]:
    # "conan profile detect" always reports x86_64 on AMD64 systems even if we are
    # running inside an x86 VS command prompt. We may want to force the env's arch
    # instead. Let the default profile guide us in all other cases.
    if "VSCMD_ARG_TGT_ARCH" not in os.environ:
        return []

    arch = os.environ["VSCMD_ARG_TGT_ARCH"]
    if arch == "x64":
        arch = "x86_64"

    return ["--settings", f"arch={arch}"]


def call(*args: str) -> int:
    print("+", *args)
    return subprocess.check_call(args)


def output(*args: str) -> bytes:
    print("+", *args)
    return subprocess.check_output(args)


if __name__ == "__main__":
    main()
