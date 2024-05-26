import argparse
import venv

import sys
import os

from modules.spinner import Spinner

class Args:
    LANGUAGE: str
    TYPE: str
    directory: str

def main():
    parser = argparse.ArgumentParser(prog="new", description="Creates a new project")

    parser.add_argument("LANGUAGE", help="The language that the project will be based on")
    parser.add_argument("TYPE", help="The project type that you want to work on. Example: (new python module, new python script)")
    parser.add_argument("-d", dest="directory", default=os.getcwd(), help=f"The directory where the project will live. Default {os.getcwd()}")

    args: Args = parser.parse_args()

    match args.LANGUAGE:
        case "python":
            match args.TYPE:
                case "script":
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

                        venv.create(os.path.join(path, ".venv"), with_pip=True, symlinks=True)
                    
                        spin.text = "Creating project root..."
                        
                        os.makedirs(os.path.join(path, "src", "modules"), exist_ok=True)
                        open(os.path.join(path, "src", "main.py"), "x").close()

                    print("Done!")
                
                case "module":
                    print("Not implemented yet")

                case _:
                    print("Unknown project type")
        case _:
            print("Unknown project language")

if __name__ == "__main__":
    main()
