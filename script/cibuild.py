#!/usr/bin/env python3
#
# script/cibuild.py - Performs a CI build
#

import os
import platform
import subprocess


def main():
    prepare()

    call("cmake", "--preset", "default")
    call("cmake", "--build", "--preset", "default")


def prepare():
    if not is_ci():
        return

    if is_linux():
        call("sudo", "apt-get", "install", "-y", "ninja-build")
    elif is_macos():
        call("brew", "install", "ninja")


def is_linux() -> bool:
    return platform.system() == "Linux"


def is_macos() -> bool:
    return platform.system() == "Darwin"


def is_ci() -> bool:
    return "CI" in os.environ


def call(*args: str) -> int:
    print("+", *args)
    return subprocess.check_call(args)


if __name__ == "__main__":
    main()
