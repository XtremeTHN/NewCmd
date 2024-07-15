import argparse
import os

from modules.python import create_python_script
from modules.vala import create_vala_project

from modules.utils import Args, error, info

def main():
    parser = argparse.ArgumentParser(prog="new", description="Creates a new project")

    parser.add_argument("LANGUAGE", help="The language that the project will be based on")
    parser.add_argument("TYPE", nargs="?", help="The project type that you want to work on. Example: (new python module, new python script)")
    parser.add_argument("-d", dest="directory", default=os.getcwd(), help=f"The directory where the project will live. Default {os.getcwd()}")
    parser.add_argument("-n", "--project-name", dest="project_name", help="The project name. Required for some languages, like Vala")

    args: Args = parser.parse_args()

    match args.LANGUAGE:
        case "python":
            if args.TYPE == None:
                error("You need to specify what kind of python project you want to create")

            match args.TYPE:
                case "script":
                    create_python_script(args)
                
                case "module":
                    info("Not implemented yet")

                case _:
                    info("Unknown project type")
        case "vala":
            if args.project_name is None:
                error("Project name is required")

            create_vala_project(args)

        case _:
            error("Unknown or not supported project language")

if __name__ == "__main__":
    main()
