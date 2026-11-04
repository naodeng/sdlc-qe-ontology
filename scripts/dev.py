"""Run the API and frontend on loopback, and stop both when either exits."""

from __future__ import annotations

from pathlib import Path
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    python = ROOT / ".venv/bin/python"
    if not python.exists():
        print("BLOCKED: create the project environment first with `make setup`.", file=sys.stderr)
        return 2
    if not (ROOT / "frontend/node_modules").exists():
        print("BLOCKED: install frontend dependencies first with `make setup`.", file=sys.stderr)
        return 2
    if not shutil.which("npm"):
        print("BLOCKED: npm is required to run the frontend.", file=sys.stderr)
        return 2

    commands = [
        [
            str(python),
            "-m",
            "uvicorn",
            "backend.app.main:app",
            "--host",
            "127.0.0.1",
            "--port",
            "8000",
            "--reload",
        ],
        [
            "npm",
            "--prefix",
            str(ROOT / "frontend"),
            "run",
            "dev",
            "--",
            "--host",
            "127.0.0.1",
        ],
    ]
    processes: list[subprocess.Popen[bytes]] = []
    try:
        for command in commands:
            processes.append(subprocess.Popen(command, cwd=ROOT))
        print("Workbench UI:  http://127.0.0.1:5174")
        print("Workbench API: http://127.0.0.1:8000/api/docs")
        while True:
            for process in processes:
                return_code = process.poll()
                if return_code is not None:
                    return return_code
            time.sleep(0.2)
    except KeyboardInterrupt:
        return 130
    finally:
        for process in processes:
            if process.poll() is None:
                process.terminate()
        for process in processes:
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()


if __name__ == "__main__":
    raise SystemExit(main())
