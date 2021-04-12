import json, os
from colorama import Fore, Back, Style


class Settings:
    def __init__(self, path_to_settings):
        self.path_to_settings = path_to_settings
        self.settings_template = {
            "document_ext": [".pdf", ".PDF", ".odt", ".doc"],
            "format": "DOC_$Y$M$D_FILENAME",
            "replace_letters": [
                {"old_letter": "\u00e4", "new_letter": "ae"},
                {"old_letter": "\u00f6", "new_letter": "oe"},
                {"old_letter": "\u00fc", "new_letter": "ue"},
                {"old_letter": " ", "new_letter": ""},
            ],
        }

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

    def check_settings(self, settings):
        error = False

        # Check json file
        try:
            # format
            if type(settings["format"]) != type(str()):
                error = True

            # document ext
            if type(settings["document_ext"]) != type(list()):
                error = True

            else:
                for imgage_ext in settings["document_ext"]:
                    if type(imgage_ext) != type(str()):
                        error = True

            # replace letters
            if type(settings["replace_letters"]) != type(list()):
                error = True

            else:
                for replace_letter in settings["replace_letters"]:
                    if type(replace_letter) != type(dict()):
                        error = True

        except AttributeError:
            error = True

        except KeyError:
            error = True

        if error:
            print(
                Fore.RED
                + f"Error in settings. Please visit https://github.com/jolsfd/filenamer \n"
                + Fore.RESET
            )

        return error