# This Python File Handles All File Management for ModDude!
# Path: file_manager.py

# Import Modules
import subprocess
from colorama import Fore, Back, Style
import os
import shutil
import datetime
import PySimpleGUI as pg
from ui_menus import ERROR_UI, exit_app, UI_Setup
import json


def check_game_install_location(modpack, APPDATA_PATH, PATH):
    found = False
    print(Fore.CYAN + '\nChecking game install location...\n')
    if modpack.game == 'Minecraft':
        if os.path.exists(f'{APPDATA_PATH}\.minecraft'):
            print(Fore.GREEN + 'Minecraft found!')
            PATH = f'{APPDATA_PATH}\.minecraft'
            found = True
        else:
            print(
                Back.RED + 'Minecraft not found! Please install Minecraft if you haven\' already.')
            PATH = ''
            found = False
    else:
        layout = [
            [pg.Text(
                'Game unknown! Please check to make sure everything is downloaded correctly.')],
            [pg.Button('OK')]]
        UI_Setup(layout)
        print(Back.RED + 'Game unknown! Please check to make sure everything is downloaded correctly.')
        exit_app()

    # Check if user wants to install to a different location
    if found == False:
        layout = [[pg.Text(f'{modpack.game} not found! Where is {modpack.game} installed?')],
                    [pg.InputText(key='path'), pg.FolderBrowse()],
                    [pg.Button('OK')]]
        PATH = get_path(PATH, layout)
    else:
        layout = [[pg.Text(f'{modpack.game} found!')],
                    [pg.Text(f'Is {PATH} the correct install location?')],
                    [pg.Button('Yes'), pg.Button('No')]]
        window = pg.Window('ModDude', layout)
        while True:
            event, values = window.read()
            if event in (None, 'Exit'):
                exit_app()
            elif event == 'Yes':
                window.close()
                break
            elif event == 'No':
                window.close()
                layout = [[pg.Text(
                    f'Where is {modpack.game}? ')],
                    [pg.InputText(key='path'), pg.FolderBrowse()],
                    [pg.Button('OK')]]
                PATH = get_path(PATH, layout)
    return PATH


def get_path(PATH, layout):
    # Check for valid path
    temp_PATH = ''
    window = pg.Window('ModDude', layout)
    error_layout = [[pg.Text('Invalid Path! Please try again.')],
                    [pg.InputText(key='path'), pg.FolderBrowse()],
                    [pg.Button('OK')]]
    while True:
        event, values = window.read()
        if event in (None, 'Exit'):
            exit_app()
        elif event == 'OK':
            temp_PATH = values['path']
            if os.path.exists(temp_PATH):
                window.close()
                return temp_PATH
                break
            else:
                window.close()
                window = pg.Window('ModDude', error_layout)
    return temp_PATH


def back_up_old(modpack, PATH):
    print(Fore.CYAN + f'\n{PATH}\n')
    folder_name = os.path.basename(os.path.normpath(PATH))
    if modpack.game == 'Minecraft':
        if os.path.exists(f'{PATH}'):
            # Ask user if they want to back up old mods
            print(Fore.YELLOW +
                  f'Would you like to back up your old {folder_name}? (y/n)')
            layout = [[pg.Text(f'Would you like to back up your old {folder_name}?')],
                      [pg.Button('Yes'), pg.Button('No')]]
            window = pg.Window('ModDude', layout)
            while True:
                event, values = window.read()
                if event in (None, 'Exit'):
                    exit_app()
                elif event == 'Yes':
                    
                    # Backup Minecraft mods to new folder with date
                    current_date = datetime.datetime.now()
                    current_date = current_date.strftime("%m-%d-%Y_%H-%M-%S")
                    print(Fore.GREEN + f'Backing up old {folder_name} to ' + Fore.MAGENTA +
                          f'{folder_name}_old_{current_date}' + Fore.GREEN + '...')
                    os.rename(f'{PATH}',
                              f'{PATH}_old_{current_date}')
                    print(Fore.GREEN + 'Backup Complete!')
                    window.close()
                    break
                elif event == 'No':
                    # Not backing up old files
                    # Only Delete Old Mods
                    if folder_name == 'mods':
                        try:
                            shutil.rmtree(f'{PATH}')
                            print(Fore.GREEN + 'Old folder removed!')
                        except OSError as e:
                            ERROR_UI(
                                'Error', f'Error: {e.filename} - {e.strerror}!', FATAL=True)
                    window.close()
                    return
        else:
            print(Fore.GREEN + 'No existing mods found.')
    else:
        ERROR_UI(
            'Error', 'Game unknown! Please check to make sure everything is downloaded correctly.', FATAL=True)

    layout = [[pg.Text('Files backed up!')],
              [pg.Button('OK!')]]
    window = pg.Window('ModDude', layout)
    while True:
        event, values = window.read()
        if event in (None, 'Exit'):
            exit_app()
        elif event == 'OK!':
            window.close()
            break


def copy_pack(modpack, PATH, BASE_DIR):
    done = False
    copied = 0
    MAX_COPY = 0
    if modpack.game == 'Minecraft':
        # Find number of files to copy
        for root, dirs, files in os.walk(f'{BASE_DIR}\\Downloads\\{modpack.pack_name}'):
            for file in files:
                MAX_COPY += 1
        if MAX_COPY == 0:
            ERROR_UI('Error', 'No files found in pack!', FATAL=True)
        # Copy pack to game folder
        # Copy mods folder

        layout = [[pg.Text('Copying mods...')],
                  [pg.ProgressBar(MAX_COPY, orientation='h', size=(20, 20), key='progressbar_copied')]]
        window = pg.Window('ModDude', layout)
        progress_bar = window['progressbar_copied']
        while not done:
            event, values = window.read(timeout=10)
            if event in (None, 'Exit'):
                exit_app()
            print(Fore.GREEN + 'Copying pack to game folder... \n')
            # Make all directories in pack if missing
            for folder in os.listdir(f'{BASE_DIR}\\Downloads\\{modpack.pack_name}'):
                if os.path.isdir(f'{BASE_DIR}\\Downloads\\{modpack.pack_name}\\{folder}'):
                    if not os.path.exists(f'{PATH}\\{folder}'):
                        os.mkdir(f'{PATH}\\{folder}')
                        print(Fore.GREEN + f'Created {folder} folder.')

            for folder in os.listdir(f'{BASE_DIR}\\Downloads\\{modpack.pack_name}'):
                # Check if it's a folder
                if os.path.isdir(f'{BASE_DIR}\\Downloads\\{modpack.pack_name}\\{folder}'):
                    print(Fore.GREEN + f'Copying {folder} folder...')
                    for file in os.listdir(f'{BASE_DIR}\\Downloads\\{modpack.pack_name}\\{folder}'):
                        shutil.copy(
                            f'{BASE_DIR}\\Downloads\\{modpack.pack_name}\\{folder}\\{file}', f'{PATH}\\{folder}')
                        copied += 1
                        progress_bar.UpdateBar(copied / MAX_COPY * 100)
                    print(Fore.MAGENTA +
                          f'\tInstalled {copied} files to {folder} folder.\n')
                    copied = 0
            done = True
        window.close()
    else:
        ERROR_UI(
            'Error', 'Game unknown! Please check to make sure everything is downloaded correctly.', FATAL=True)


def run_mod_loader_installer(modpack, BASE_DIR):
    found = False
    # Ask user if they want to install mod loader
    print(Fore.YELLOW + f'Would you like to install {modpack.mod_loader}? ' + Fore.CYAN +
          '(Recommended Unless You Are Reinstalling Pack)' + Fore.YELLOW + ' (y/n)')
    layout = [[pg.Text(f'Would you like to install {modpack.mod_loader} v{modpack.mod_loader_version}?')],
              [pg.Text('(Recommended Unless You Are Reinstalling Pack)')],
              [pg.Button('Yes'), pg.Button('No')]]
    window = pg.Window('ModDude', layout)
    while True:
        event, values = window.read()
        if event in (None, 'Exit'):
            exit_app()
        elif event == 'Yes':
            window.close()
            break
        elif event == 'No':
            window.close()
            return

    # Give install instructions
    layout = [[pg.Text('Installing Mod Loader...')],
              [pg.Text('Please follow the instructions on the screen.')],
              [pg.Text('Once the installer is finished it will say "Done"')],
              [pg.Text(
                  f'Please close {modpack.mod_loader} when it says "Done"')],
              [pg.Button('OK!')]]
    window = pg.Window('ModDude', layout)
    while True:
        event, values = window.read()
        if event in (None, 'Exit'):
            exit_app()
        elif event == 'OK!':
            window.close()
            break

    # Check if mod loader is already installed
    if modpack.mod_loader == 'Forge':
        # ! This is not expected to work and needs a rewrite
        for file in os.listdir(f'{BASE_DIR}\\Downloads'):
            if file.startswith('forge-'):
                found = True
                print(Fore.GREEN + 'Mod loader already installed!')
                break
        if not found:
            print(Fore.GREEN + 'Downloading mod loader...')
            # Download mod loader
            # ! THIS IS OUT OF DATE AND NEEDS TO BE UPDATED
            try:
                request.urlretrieve(
                    f'{FORGE_URL}', f'{BASE_DIR}\\Downloads\\forge-{FORGE_VERSION}-installer.jar')
            except Exception as e:
                ERROR_UI('Error', f'Error: {e}', FATAL=True)
            print(Fore.GREEN + 'Mod loader downloaded!')

            # Run mod loader installer
            print(Fore.GREEN + 'Running mod loader installer...')
            os.system(
                f'java -jar {BASE_DIR}\\Downloads\\forge-{FORGE_VERSION}-installer.jar')
            print(Fore.GREEN + 'Mod loader installed!')
        else:
            ERROR_UI(
                'Error', 'Mod loader unknown! Please check to make sure everything is downloaded correctly.', FATAL=True)
    else:
        # Run mod loader installer executable
        print(Fore.GREEN + f'Running {modpack.mod_loader} installer...')
        for file in os.listdir(f'{BASE_DIR}\\Downloads\\{modpack.pack_name}'):
            if file.endswith('.exe') or file.endswith('.jar'):
                print(Fore.GREEN + f'{modpack.mod_loader} installer found!')
                print(
                    Back.MAGENTA + f'Please install {modpack.mod_loader} {modpack.mod_loader_version} to the game folder.\n')
                if file.endswith('.exe'):
                    subprocess.check_call(
                        [f'{BASE_DIR}\\Downloads\\{modpack.pack_name}\\{file}'])
                elif file.endswith('.jar'):
                    subprocess.call(
                        ['java', '-jar', f'{BASE_DIR}\\Downloads\\{modpack.pack_name}\\{file}'])
                else:
                    print(Back.RED + 'Mod loader unable to run!')
                    print(Back.RED + 'Please install manually.')
                found = True
        if found == False:
            ERROR_UI(
                'Error', f'Unable to find {modpack.mod_loader} installer!', FATAL=True)


def check_launcher_profiles(modpack, PATH):
    print(Fore.GREEN + f'{modpack.game} - {modpack.game_version} [{modpack.mod_loader} - {modpack.mod_loader_version}]')
    print(Fore.GREEN + 'Checking launcher profiles...')
    # Check if launcher profiles exist
    if os.path.exists(f'{PATH}\\launcher_profiles.json'):
        # Check if mod loader is already installed
        with open(f'{PATH}\\launcher_profiles.json', 'r') as f:
            data = json.load(f)
            for profile in data['profiles']:
                print (Fore.GREEN + f'Checking {profile} profile...')
                if modpack.mod_loader.lower() in data['profiles'][profile]['name'].lower():
                    print(Fore.GREEN + 'Mod loader found installed!')
                    if modpack.mod_loader_version in data['profiles'][profile]['lastVersionId']:
                        print(Fore.GREEN + 'Mod loader version installed!')
                        return True
    print(Fore.YELLOW + 'Mod loader not installed!')
    return False


def check_ram(modpack, PATH):
    # ? This method should probably be simplified
    print(Fore.GREEN + 'Checking RAM...')
    # Check if launcher profiles exist
    if os.path.exists(f'{PATH}\\launcher_profiles.json'):
        # Check if mod loader is already installed
        with open(f'{PATH}\\launcher_profiles.json', 'r') as f:
            data = json.load(f)
            for profile in data['profiles']:
                print (Fore.GREEN + f'Checking {profile} profile...')
                if modpack.mod_loader.lower() in data['profiles'][profile]['name'].lower():
                    print(Fore.GREEN + 'Mod loader found installed!')
                    if modpack.mod_loader_version in data['profiles'][profile]['lastVersionId']:
                        print(Fore.GREEN + 'Mod loader version installed!')
                        # Get Current RAM
                        current_ram = data['profiles'][profile]['javaArgs']
                        current_ram = current_ram.split(' ')
                        for arg in current_ram:
                            if arg.startswith('-Xmx'):
                                # Get number out of argument
                                current_ram = arg[4:]
                                current_ram = current_ram[:-1]
                                current_ram = int(current_ram)
                                print(Fore.GREEN + f'Current RAM: {current_ram}GB')
                                print(
                                    Fore.GREEN + f'Modpack RAM: {modpack.recommended_ram}GB')
                                if current_ram < modpack.recommended_ram:
                                    print(Fore.YELLOW + 'RAM is too low!')
                                    # Ask if user wants to change RAM
                                    layout = [[pg.Text('RAM is too low!')],
                                              [pg.Text(
                                                  f'Current RAM: {current_ram}GB')],
                                              [pg.Text(
                                                  f'Recommended RAM: {modpack.recommended_ram}GB')],
                                              [pg.Text('Do you want to change the RAM?')],
                                              [pg.Button('Yes'), pg.Button('No')]]
                                    window = pg.Window('ModDude', layout)
                                    while True:
                                        event, values = window.read()
                                        if event in (None, 'Exit'):
                                            exit_app()
                                        elif event == 'Yes':
                                            # Change RAM in launcher profile
                                            print(Fore.GREEN + 'Changing RAM...')
                                            data['profiles'][profile]['javaArgs'].replace(
                                                f"-Xmx{current_ram}G", f"-Xmx{modpack.recommended_ram}G")
                                            with open(f'{PATH}\\launcher_profiles.json', 'w') as f:
                                                json.dump(data, f)
                                            print(Fore.GREEN + 'RAM changed!')
                                            window.close()
                                            return True
                                        elif event == 'No':
                                            window.close()
                                            return False
                                    
    print(Fore.YELLOW + 'Mod loader not installed!')
    return False

def check_install_integrity(modpack, PATH, BASE_DIR):
    passed_files = 0
    failed_files = 0
    

    print(Fore.CYAN + '\nChecking install integrity...')
    if modpack.game == 'Minecraft':
        # Check if mods folder exists
        for folder in os.listdir(f'{BASE_DIR}\\Downloads\\{modpack.pack_name}'):
            if os.path.exists(f'{PATH}\\{folder}'):
                # Check if all files are in folder if it's a folder
                if os.path.isdir(f'{BASE_DIR}\\Downloads\\{modpack.pack_name}\\{folder}'):
                    print(Fore.GREEN + f'\t{folder} folder found!')
                    passed_files += 1
                    for file in os.listdir(f'{BASE_DIR}\\Downloads\\{modpack.pack_name}\\{folder}'):
                        if os.path.exists(f'{PATH}\\{folder}\\{file}'):
                            passed_files += 1
                        else:
                            print(Back.RED + f'\t\t{file} not found!')
                            failed_files += 1
                else:
                    print(Back.RED + f'\t{folder} folder not found!')
                    failed_files += 1
        percent_passed = int(
            passed_files / (passed_files + failed_files)) * 100
        print(Fore.MAGENTA + f'{percent_passed}% of tests passed.')

        # Display results
        layout = [[pg.Text(f'{percent_passed}% of tests passed.')],
                  [pg.Button('OK')]]
        window = pg.Window('ModDude', layout)
        while True:
            event, values = window.read()
            if event in (None, 'Exit'):
                exit_app()
            elif event == 'OK':
                window.close()
                break
    else:
        ERROR_UI('Error', 'Game not supported!', FATAL=False)


def delete_temp_files(modpack, BASE_DIR):
    # Delete all files in the temp folder
    for file in os.listdir(f'{BASE_DIR}\\Downloads\\{modpack.pack_name}'):
        try:
            os.remove(f'{BASE_DIR}\\Downloads\\{modpack.pack_name}\\{file}')
        except Exception as e:
            print(Back.RED + f'Error: {e}')
