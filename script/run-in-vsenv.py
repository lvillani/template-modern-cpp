#!/usr/bin/env python3
#
# script/run-in-vsenv.py - Runs a command inside Visual Studio Command Prompt's x64 environment
#

import os
import pathlib
import platform
import subprocess
import sys

# See also: https://github.com/microsoft/vswhere
VSWHERE_LOCATION = r"%ProgramFiles(x86)%\Microsoft Visual Studio\Installer\vswhere.exe"


def main():
    if not is_windows():
        print("This script only works on Windows.")
        sys.exit(1)

    if not "COMSPEC" in os.environ:
        print("COMSPEC environment variable is not defined, cannot proceed.")
        sys.exit(1)

    vswhere = pathlib.Path(os.path.expandvars(VSWHERE_LOCATION))
    if not vswhere.exists():
        print(f"Could not find {vswhere}.")
        sys.exit(1)

    vsdevcmd = vsdevcmd_path()
    if not vsdevcmd.exists():
        print(f"Could not find {vsdevcmd}.")
        sys.exit(1)

    call(
        os.environ["COMSPEC"],
        "/c",
        str(vsdevcmd),
        "-arch=x64",
        "-host_arch=x64",
        "&&",
        *sys.argv[1:],
    )


def is_windows() -> bool:
    return platform.system() == "Windows"


def vsdevcmd_path() -> pathlib.Path:
    # See also: https://github.com/microsoft/vswhere/wiki/Find-VC
    return vs_install_dir() / "Common7" / "Tools" / "vsdevcmd.bat"


def vs_install_dir() -> pathlib.Path:
    # See also: https://github.com/microsoft/vswhere/wiki/Find-VC
    return pathlib.Path(
        output(
            "vswhere",
            "-latest",
            "-products",
            "*",
            "-requires",
            "Microsoft.VisualStudio.Component.VC.Tools.x86.x64",
            "-property",
            "installationPath",
        )
    )


def output(*args: str) -> str:
    print("+", *args)
    return subprocess.check_output(args).decode("utf-8").strip()


def call(*args: str) -> int:
    print("+", *args)
    return subprocess.check_call(args)


if __name__ == "__main__":
    main()
