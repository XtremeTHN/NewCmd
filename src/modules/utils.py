from subprocess import Popen
import sys

class Args:
    LANGUAGE: str
    TYPE: str
    directory: str
    project_name: str | None

class Style:
    INFO="\033[32;1;4mInfo:\033[0m"
    ERROR="\033[31;1;4mError:\033[0m"

def execute(*args):
    with Popen(args=args, stdout=sys.stdout, stderr=sys.stderr) as proc:
        proc.communicate()
        return proc.poll() == 0

def info(msg):
    print(Style.INFO, msg)

def error(msg, code=1):
    print(Style.ERROR, msg)
    sys.exit(code)