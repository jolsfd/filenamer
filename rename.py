import os
import time, datetime
from colorama import Fore, Back, Style


class Rename:
    def __init__(self, settings):
        self.settings = settings

    def build_file_dict(self, source_name):
        file_dict = {}

        # Insert data into dictonary
        file_dict["source_name"] = source_name
        file_dict["head"], file_dict["tail"] = os.path.split(source_name)
        file_dict["filename"], file_dict["file_ext"] = os.path.splitext(
            file_dict["tail"]
        )
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

    def get_filename(self, tail):
        if self.settings["old_filename"]:
            # get filename
            filename = os.path.splitext(tail)[0]

            # replace letters from setting
            for replace_letter in self.settings["replace_letters"]:
                filename = filename.replace(
                    replace_letter["old_letter"], replace_letter["new_letter"]
                )

            # return filename with spaceletter
            return self.settings["spaceletter"] + filename
        else:
            return ""

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

    def collect_files(self, path):
        files = []

        for root, dirnames, filenames in os.walk(path):
            for file in filenames:
                # check safe string
                if (
                    file[: len(self.settings["safe_string"])]
                    == self.settings["safe_string"]
                ):
                    continue

                # check file extension
                file_ext = os.path.splitext(file)[1]

                if file_ext in self.settings["file_ext"]:
                    files.append(os.path.join(root, file))

        del dirnames

        return files

    def rename_files(self, files):
        for old_file in files:
            # get safe string from settings
            safe_string = self.settings["safe_string"]

            # split file into dir and filename
            head, old_tail = os.path.split(old_file)

            # date from file
            date = self.get_file_date(old_file)

            # filename without a extension
            filename = self.get_filename(old_tail)

            # file extension from file tail
            file_ext = os.path.splitext(old_tail)[1]

            # build new file tail
            new_tail = safe_string + date + filename + file_ext
            new_file = head + "/" + new_tail

            if os.path.isfile(new_file):
                print(old_file + " is not renamed")
                continue

            if os.path.isfile(old_file):
                # rename file
                os.rename(old_file, new_file)

            # visualization for user
            print(old_tail + " -> " + new_tail)
