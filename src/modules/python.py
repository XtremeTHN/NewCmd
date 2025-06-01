from modules.spinner import Spinner
from modules.utils import execute

import sys
import os


def create_python_script(args):
    print("Creating a new python script...")

    with Spinner("Creating directory...") as spin:
        path = args.directory
        if os.path.exists(path):
            if path != ".":
                spin.stop()
                print("The project already exists")
                sys.exit(1)

        os.makedirs(path, exist_ok=True)

        spin.text = "Creating virtual environment..."
        execute("python3", "-m", "venv", os.path.join(path, ".venv"))

        spin.text = "Creating project root..."

        os.makedirs(os.path.join(path, "src", "modules"), exist_ok=True)
        open(os.path.join(path, "src", "main.py"), "x").close()

    print("Done!")
