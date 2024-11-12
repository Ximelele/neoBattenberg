import shlex
import subprocess

def safe_run(command: str) -> None:
    args = shlex.split(command)
    subprocess.run(args, check=True)