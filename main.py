from settings import SettingsfromJSON
from rename import Rename
import os

class Menu:
    def __init__(self):
        self.settings_object = SettingsfromJSON()
        self.settings = self.settings_object.load_json()
        self.rename = Rename(self.settings)
        self.error = self.settings_object.error_checking(self.settings)

    def rename_files(self):
        path_input = ''

        print('Please input a path.')
        path_input = input('>>>' + self.settings['working_path'])
        path = self.settings['working_path'] + path_input

        if '\\' in path:
            path = path.replace('\\','/')

        if os.path.exists(path):
            files = self.rename.collect_files(path)
            
            print('Rename ' + str(len(files)) + ' files.')

            user_input = input('Yes/No [Y/n]')

            if user_input == 'Y':
                self.rename.rename_files(files)

        else:
            print('Path do not exist.')

    def change_working_path(self):
        working_path_input = ''

        while len(working_path_input) < 1:
            print('Please input a path.')
            working_path_input = input('>>> ')

        if '\\' in working_path_input:
            working_path_input = working_path_input.replace('\\','/')

        if working_path_input[-1] != '/':
            working_path_input = working_path_input + '/'
        
        if os.path.exists(working_path_input):
            self.settings['working_path'] = working_path_input
            self.settings_object.save_json(self.settings)

            self.settings = self.settings_object.load_json()

            print()

        else:
            print('Path do not exist.')

    def help(self):
        print('Please visit https://github.com/jolsfd/filenamer')

def run():
    menu = Menu()

    while not menu.error:
        print(13*' ','Menu',13*' ')
        print(30*'-')
        print('  1. Rename files')
        print('  2. Working path')
        print('  3. Help')
        print('  4. Quit')
        print(30*'-')
        print()

        menu_input = input('>>> ')

        if menu_input == '1':
            menu.rename_files()

        elif menu_input == '2':
            menu.change_working_path()

        elif menu_input == '3':
            menu.help()

        elif menu_input == '4':
            quit()

if __name__ == '__main__':
    run()