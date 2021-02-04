import json
import os

class SettingsfromJSON:
    '''Take settings as a JSON file and return the settings in a python dictonary'''
    def __init__(self):
        self.json_path = os.path.join(os.path.dirname(os.path.abspath(__file__))) + '/filenamer_settings/filenamer_settings.json'

    def load_json(self):
        try:
            json_settings = open(self.json_path, 'r')

            data = json.load(json_settings)

            json_settings.close()

            return data

        except FileNotFoundError:
            print('No json file found.')

    def save_json(self, data):
        try:
            json_settings = open(self.json_path, 'w')

            json.dump(data, json_settings)

            json_settings.close()

            print('Saved Changes into json file.')

        except FileNotFoundError:
            print('No json file found.')

    def error_checking(self, settings):
        error = False
        try:
            if type(settings['working_path']) != type(str()):
                print('Type error in working_path')
                error = True

            if type(settings['safe_string']) != type(str()):
                print('Type error in safe_string')
                error = True

            if type(settings['file_ext']) != type(list()):
                print('Type error in file_ext')
                error = True

            if type(settings['file_ext'][0]) != type(str()):
                print('Type error in file_ext')
                error = True

            if type(settings['date_string']) != type(bool()):
                print('Type error in date')
                error = True

            if type(settings['old_filename']) != type(bool()):
                print('Type error in old_filename')
                error = True

            if type(settings['spaceletter']) != type(str()):
                print('Type error in spaceletter')
                error = True

            if type(settings['replace_letters']) != type(list()):
                print('Type error in replace_letter')
                error = True

            if type(settings['replace_letters'][0]) != type(dict()):
                print('Type error in replace_letters dictonary')
                error = True
            
        except AttributeError:
            print('attributes not found check https://')
            error = True
        
        if error:
            print('Please go to https://github.com/jolsfd/filenamer and check the filenamer_settings.json file.')

        return error