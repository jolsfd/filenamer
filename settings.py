import json, os
from colorama import Fore, Back, Style


class Settings:
    def __init__(self, path_to_settings):
        self.path_to_settings = path_to_settings
        self.settings_template = {
            # "safe_string": "IMG_",
            # "raw_rename": True,
            # "safe_rename": True,
            # "raw_ext": [".raw", ".cr2", ".dng"],
            "document_ext": [".pdf", ".PDF", ".odt", ".doc"],
            "format": "DOC_$Y$M$D_FILENAME",
            "replace_letters": [
                {"old_letter": "\u00e4", "new_letter": "ae"},
                {"old_letter": "\u00f6", "new_letter": "oe"},
                {"old_letter": "\u00fc", "new_letter": "ue"},
                {"old_letter": " ", "new_letter": ""},
            ],
        }
        # self.json_path = os.path.join(os.path.dirname(os.path.abspath(__file__))) + '/filenamer_settings/filenamer_settings.json'

    def save_settings(self, new_settings):
        try:
            json_file = open(self.path_to_settings, "w")

            json.dump(new_settings, json_file)

            json_file.close()

            print(Fore.GREEN + f"Saved Changes into json file.\n" + Fore.RESET)

        except:
            print(Fore.RED + f"Settings could not be saved\n" + Fore.RESET)

    def load_settings(self):
        try:
            json_file = open(self.path_to_settings, "r")

            settings = json.load(json_file)

            json_file.close()

            return settings
        except FileNotFoundError:
            self.save_settings(self.settings_template)

            return self.settings_template

    def error_checking(self, settings):
        error = False
        try:
            if type(settings["working_path"]) != type(str()):
                print("Type error in working_path")
                error = True

            if type(settings["safe_string"]) != type(str()):
                print("Type error in safe_string")
                error = True

            if type(settings["file_ext"]) != type(list()):
                print("Type error in file_ext")
                error = True

            if type(settings["file_ext"][0]) != type(str()):
                print("Type error in file_ext")
                error = True

            if type(settings["date_string"]) != type(bool()):
                print("Type error in date")
                error = True

            if type(settings["old_filename"]) != type(bool()):
                print("Type error in old_filename")
                error = True

            if type(settings["spaceletter"]) != type(str()):
                print("Type error in spaceletter")
                error = True

            if type(settings["replace_letters"]) != type(list()):
                print("Type error in replace_letter")
                error = True

            if type(settings["replace_letters"][0]) != type(dict()):
                print("Type error in replace_letters dictonary")
                error = True

        except AttributeError:
            print("attributes not found check https://")
            error = True

        if error:
            print(
                "Please go to https://github.com/jolsfd/filenamer and check the filenamer_settings.json file."
            )

        return error