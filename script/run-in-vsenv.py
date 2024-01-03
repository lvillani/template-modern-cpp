#!/usr/bin/env python3
#
# script/run-in-vsenv.py - Runs a command inside Visual Studio Command Prompt's environment
#

import argparse
import dataclasses
import enum
import os
import pathlib
import platform
import subprocess
import sys
import typing

# See also: https://github.com/microsoft/vswhere
VSWHERE_LOCATION = r"%ProgramFiles(x86)%\Microsoft Visual Studio\Installer\vswhere.exe"


class Arch(enum.Enum):
    DEFAULT = "default"
    X64 = "x64"
    X86 = "x86"

    def __str__(self) -> str:
        return self.value


class Version(enum.Enum):
    LATEST = "latest"
    VS2017 = "2017"
    VS2019 = "2019"
    VS2022 = "2022"

    def __str__(self) -> str:
        return self.value


@dataclasses.dataclass
class Args:
    arch: Arch
    version: Version


VERSION_TO_RANGE = {
    Version.LATEST: "latest",
    Version.VS2017: "[15.0, 16.0)",
    Version.VS2019: "[16.0, 17.0)",
    Version.VS2022: "[17.0, 18.0)",
}


def main():
    args, rest = parse_args()

    if not rest:
        print("Must specify a command to run inside the Visual Studio environment.")
        sys.exit(1)

    if not is_windows():
        print("This script only works on Windows.")
        sys.exit(1)

    if not "COMSPEC" in os.environ:
        print("COMSPEC environment variable is not defined, cannot proceed.")
        sys.exit(1)

    vswhere_exe = pathlib.Path(os.path.expandvars(VSWHERE_LOCATION))
    if not vswhere_exe.exists():
        print(f"Could not find {vswhere_exe}.")
        sys.exit(1)

    vsdevcmd = vsdevcmd_path(vswhere_exe, args.version)
    if not vsdevcmd:
        print(f"Could not find requested Visual Studio version: {args.version}")
        sys.exit(1)
    if not vsdevcmd.exists():
        print(f"Could not find {vsdevcmd}.")
        sys.exit(1)

    vsdevcmd_args = []
    if args.arch != Arch.DEFAULT:
        vsdevcmd_args.append(f"-arch={args.arch}")

    call(os.environ["COMSPEC"], "/c", str(vsdevcmd), *vsdevcmd_args, "&&", *rest)


def parse_args() -> typing.Tuple[Args, typing.List[str]]:
    parser = argparse.ArgumentParser()
    parser.add_argument("--arch", choices=Arch, default=Arch.DEFAULT, type=Arch)
    parser.add_argument(
        "--version", choices=Version, default=Version.LATEST, type=Version
    )

    args, rest = parser.parse_known_args()

    return (Args(**vars(args)), rest)


def is_windows() -> bool:
    return platform.system() == "Windows"


def vsdevcmd_path(
    vswhere_exe: pathlib.Path, version: Version
) -> typing.Optional[pathlib.Path]:
    install_dir = vs_install_dir(vswhere_exe, version)

    return install_dir / "Common7" / "Tools" / "vsdevcmd.bat" if install_dir else None


def vs_install_dir(
    vswhere_exe: pathlib.Path, version: Version
) -> typing.Optional[pathlib.Path]:
    # See also: https://github.com/microsoft/vswhere/wiki/Find-VC
    version_arg = (
        ["-latest"]
        if version == Version.LATEST
        else ["-version", VERSION_TO_RANGE[version]]
    )

    install_dir = output(
        f"{vswhere_exe}",
        *version_arg,
        "-products",
        "*",
        "-requires",
        "Microsoft.VisualStudio.Component.VC.Tools.x86.x64",  # x86 and AMD64
        "-property",
        "installationPath",
    )

    # NOTE: vswhere.exe doesn't seem to exit with an error if the requested VS version
    # is not found. It just doesn't return any output.
    return pathlib.Path(install_dir) if install_dir else None


def output(*args: str) -> str:
    print("+", *args)
    return subprocess.check_output(args).decode("utf-8").strip()


def call(*args: str) -> int:
    print("+", *args)
    return subprocess.check_call(args)


if __name__ == "__main__":
    main()
