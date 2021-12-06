#!/bin/env python3

import sys
import pathlib
import subprocess


def main(cli_args: list[str]) -> int:
    repo_root = pathlib.Path(__file__).resolve().parent.parent
    for soln in sorted(repo_root.glob('src/d*.py')):
        day_input = repo_root / 'input' / soln.stem
        print(f"{soln.stem} example input:")
        subprocess.run([soln, day_input.with_stem(f"{soln.stem}-example")], check=True)
        print(f"{soln.stem} full input:")
        subprocess.run([soln, day_input], check=True)

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))