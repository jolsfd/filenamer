#!/usr/bin/env python

import argparse
import os
from src.settings import Settings
from src.rename import Rename
from colorama import Fore, Back, Style


def main():
    # Path to settings
    path_to_settings = (
        os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        + "/settings/settings.json"
    )

    # Verion tag
    __version__ = 1.0

    # Parser
    parser = argparse.ArgumentParser(
        prog="FileNamer",
        description="FileNamer rename files in a directory into a format",
    )

    # path argument
    parser.add_argument(
        "-p",
        "--path",
        metavar="PATH",
        default=os.getcwd(),
        help="path where FileNamer rename files. Default: working directory",
    )

    # exclude folder argument
    parser.add_argument(
        "-e",
        "--exclude",
        metavar="FOLDER",
        nargs="*",
        help="ignore folders for renaming",
        default=[],
    )

    # rename all argument
    parser.add_argument("-a", "--all", action="store_false", help="disable Safe Rename")

    # version argument
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )

    args = parser.parse_args()

    # Check if path argument is given
    if args.path:
        # Check path
        if not os.path.isdir(args.path):
            parser.error("Path does not exist!")

        # Print Information for user
        print(f"Path: " + Fore.RED + f"{args.path}" + Fore.RESET)
        # print(f"Folders: " + Fore.RED + f"{args.folder}" + Fore.RESET)
        print(f"Exlcuded Folders: " + Fore.RED + f"{args.exclude}" + Fore.RESET)
        print(f"Safe Rename: " + Fore.RED + f"{args.all}" + Fore.RESET)

        # Generate Setting Object
        settings_object = Settings(path_to_settings)
        settings = settings_object.load_settings()

        # Check errors in settings
        if settings_object.check_settings(settings):
            parser.error("Error in settings please check URL")

        # Generate Rename Object
        rename_object = Rename(settings, args.all)

        # Collect files
        number_of_files = rename_object.collect_files(args.path, args.exclude)

        # Confirm to rename
        ask_for_rename = input(
            f"Do you confirm to rename {number_of_files} files ? [y/n]"
        )

        if ask_for_rename == "y":
            rename_object.rename_files()

        else:
            quit()


if __name__ == "__main__":
    main()