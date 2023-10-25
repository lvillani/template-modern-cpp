#!/usr/bin/env python3
#
# script/cibuild.py - Performs a CI build
#

import os
import pathlib
import subprocess
import sys


TOP_LEVEL = pathlib.Path(__file__).parent.parent.absolute()


def main():
    if is_ci():
        # Assuming CI always starts from scratch and needs the bootstrap script to run but allow
        # quicker runs on the developer machine.
        call(sys.executable, str(TOP_LEVEL / "script" / "bootstrap.py"))

    call("cmake", "--preset", "default")
    call("cmake", "--build", "--preset", "default")


def is_ci() -> bool:
    return "CI" in os.environ


def call(*args: str) -> int:
    print("+", *args)
    return subprocess.check_call(args)


if __name__ == "__main__":
    main()
