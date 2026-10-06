from __future__ import annotations

import shlex
import subprocess


def run(command: str, with_console: bool = True, line_limit: int | None = None) -> None:
    output = subprocess.run(
        shlex.split(command), capture_output=True, text=True, check=True
    )
    print()
    if with_console:
        print("```console")
        print(f"$ {command}")

    output = output.stdout.strip()
    if line_limit:
        output = "".join(output.splitlines(keepends=True)[:line_limit]) + "..."
    print(output)

    if with_console:
        print("```")
    print()
