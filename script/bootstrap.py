#!/usr/bin/env python3
#
# script/bootstrap.py - Installs dependencies required to build the project
#

import platform
import subprocess


def main():
    if is_linux():
        call("sudo", "apt-get", "install", "-y", "ninja-build")
    elif is_macos():
        call("brew", "install", "ninja")
    elif is_windows():
        call("choco", "install", "ninja")


def is_linux() -> bool:
    return platform.system() == "Linux"


def is_macos() -> bool:
    return platform.system() == "Darwin"


def is_windows() -> bool:
    return platform.system() == "Windows"


def call(*args: str) -> int:
    print("+", *args)
    return subprocess.check_call(args)


if __name__ == "__main__":
    main()
