#!/usr/bin/env python3
#
# script/bootstrap.py - Installs dependencies required to build the project
#

import json
import pathlib
import platform
import shutil
import subprocess
import typing

TOP_LEVEL = pathlib.Path(__file__).parent.parent.absolute()
CONAN_DIR = TOP_LEVEL / "conan"


def main():
    install_system_packages()
    setup_conan()


def install_system_packages():
    if is_linux():
        call("sudo", "apt-get", "install", "-y", "ninja-build")
        call("pip3", "install", "--user", "conan")
    elif is_macos():
        call("brew", "install", "conan", "ninja")
    elif is_windows():
        call("choco", "install", "conan", "ninja")


def setup_conan():
    if "default" not in conan_profiles():
        call(conan(), "profile", "detect")

    # fmt: off
    call(
        conan(),
        "install",
        "--build=missing",
        "--conf", "tools.cmake.cmaketoolchain:generator=Ninja",
        "--output-folder", str(CONAN_DIR),
        str(TOP_LEVEL),
    )
    # fmt: on


def conan_profiles() -> typing.List[str]:
    return json.loads(output(conan(), "profile", "list", "--format", "json"))


def conan() -> str:
    if is_windows() and not shutil.which("conan"):
        # Freshly installed Conan may not be immediately available in PATH, especially
        # in CI.
        return r"C:\Program Files\Conan\conan\conan.exe"

    return "conan"


def is_linux() -> bool:
    return platform.system() == "Linux"


def is_macos() -> bool:
    return platform.system() == "Darwin"


def is_windows() -> bool:
    return platform.system() == "Windows"


def call(*args: str) -> int:
    print("+", *args)
    return subprocess.check_call(args)


def output(*args: str) -> bytes:
    print("+", *args)
    return subprocess.check_output(args)


if __name__ == "__main__":
    main()
