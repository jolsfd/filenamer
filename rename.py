import os
import time


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

    def get_file_date(self, file):
        # check date settings
        if self.settings["date_string"]:
            # get creation time in seconds from a file path
            stat = os.stat(file)

            # Windows
            try:
                date_secs = stat.st_birthtime

            # Linux
            except AttributeError:
                date_secs = stat.st_mtime

            # Convert time in seconds into a time format
            time_struct = time.gmtime(date_secs)

            # year, month, day - time format
            year = str(time_struct[0])
            month = str(time_struct[1])
            day = str(time_struct[2])
            if len(month) < 2:
                month = "0" + month
            if len(day) < 2:
                day = "0" + day
            date = year + month + day

            # return date with spaceletter
            return self.settings["spaceletter"] + date
        else:
            return ""

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
