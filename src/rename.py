import os
import time
from colorama import Fore, Back, Style
from datetime import datetime


class Rename:
    def __init__(self, settings, all):
        self.settings = settings
        self.safe_rename = all
        self.safe_string = self.settings["format"].partition("$")[0]
        self.file_list = []

    def build_file_dict(self, source_name):
        file_dict = {}

        # Insert data into dictonary
        file_dict["source_name"] = source_name
        file_dict["head"], file_dict["tail"] = os.path.split(source_name)
        file_dict["filename"], file_dict["file_ext"] = os.path.splitext(
            file_dict["tail"]
        )
        file_dict["modified_filename"] = self.modify_filename(file_dict["filename"])
        file_dict["new_filename"] = ""
        file_dict["new_tail"] = ""
        file_dict["target_name"] = ""
        file_dict["number_of_copy"] = 1

        return file_dict

    def new_filename(self, source_name, filename):
        # get creation time in seconds from a file path
        stat = os.stat(source_name)

        # Windows
        try:
            date_secs = stat.st_birthtime

        # Linux
        except AttributeError:
            date_secs = stat.st_mtime

        # Convert time in seconds into a time format
        datetime_object = datetime.fromtimestamp(date_secs)

        new_filename = (
            self.settings["format"]
            .replace("$Y", datetime_object.strftime("%Y"))
            .replace("$M", datetime_object.strftime("%m"))
            .replace("$D", datetime_object.strftime("%d"))
            .replace("$h", datetime_object.strftime("%H"))
            .replace("$m", datetime_object.strftime("%M"))
            .replace("$s", datetime_object.strftime("%S"))
            .replace("FILENAME", filename)
        )

        return new_filename

    def modify_filename(self, filename):
        # replace letters from setting
        for replace_letter in self.settings["replace_letters"]:
            filename = filename.replace(
                replace_letter["old_letter"], replace_letter["new_letter"]
            )

        return filename

    def rename(self, file_dict):
        while os.path.isfile(file_dict["target_name"]):
            file_dict["number_of_copy"] = file_dict["number_of_copy"] + 1
            file_dict["new_tail"] = (
                file_dict["new_filename"]
                + "~"
                + str(file_dict["number_of_copy"])
                + file_dict["file_ext"]
            )
            file_dict["target_name"] = os.path.join(
                file_dict["head"], file_dict["new_tail"]
            )

        if os.path.isfile(file_dict["source_name"]):
            os.rename(file_dict["source_name"], file_dict["target_name"])
            print(
                Fore.GREEN
                + f"{file_dict['tail']} -> {file_dict['new_tail']}"
                + Fore.RESET
            )

        else:
            print(Fore.RED + f"{file_dict['tail']} was not found" + Fore.RESET)

    def collect_files(self, path_to_files, excluded_folders):
        exclude = set(excluded_folders)
        for root, dirnames, file_list in os.walk(path_to_files, topdown=True):
            # Exclude folders
            dirnames[:] = [d for d in dirnames if d not in exclude]

            # Get files
            for file in file_list:
                # Check all rename
                if self.safe_rename:
                    # Check safe string
                    if file[: len(self.safe_string)] == self.safe_string:
                        continue

                # check file extension
                file_ext = os.path.splitext(file)[1]

                if file_ext in self.settings["document_ext"]:
                    self.file_list.append(os.path.join(root, file))

        del dirnames

        return len(self.file_list)

    def rename_file(self, source_name):
        # Build file dict
        document_dict = self.build_file_dict(source_name)

        # Set new filename
        document_dict["new_filename"] = self.new_filename(
            document_dict["source_name"], document_dict["modified_filename"]
        )

        # Set new tail
        document_dict["new_tail"] = (
            document_dict["new_filename"] + document_dict["file_ext"]
        )

        # Set target name
        document_dict["target_name"] = os.path.join(
            document_dict["head"], document_dict["new_tail"]
        )

        # Rename file
        self.rename(document_dict)

    def rename_files(self):
        for source_name in self.file_list:
            self.rename_file(source_name)

    def clear(self):
        self.file_list = []