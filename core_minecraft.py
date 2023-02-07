# This installs minecraft mods

import datetime
import json
import os
import re
import shutil
import subprocess

from colorama import Back, Fore
from requests import request
import file_manager
from ui_menus import ERROR_UI, exit_app
import PySimpleGUI as pg


def minecraft(modpack, BASE_DIR, APPDATA_PATH, FILES, app=None, bonus_text=None):
    # Check Where to Install
    PATH = check_game_install_location(modpack, APPDATA_PATH)

    # Backup Files
    bonus_text.configure(text='Backing Up Old Mods')
    app.update()
    back_up_old(f"{PATH}\\mods")
    bonus_text.configure(text='Backing Up Old Configs')
    app.update()
    back_up_old(f"{PATH}\\config")
    bonus_text.configure(text='Backing Up Old Shaders')
    app.update()
    back_up_old(f"{PATH}\\shaderpacks")

    # Copy Pack Into Game
    bonus_text.configure(text='Installing Modpack Files')
    app.update()
    copy_pack(modpack, PATH, BASE_DIR, app, bonus_text)
    if not modpack.mod_loader == '':
        # Check if Mod Loader is Installed
        if not check_launcher_profiles(modpack, PATH):
            bonus_text.configure(text=f'Installing {modpack.mod_loader}')
            app.update()
            run_mod_loader_installer(modpack, BASE_DIR)

    # Check if Profile Has Enough RAM
    # TODO: Add RAM Check
    # This has no error handling, so it will crash if the java arguments are not found.
    # Saving also doesn't work it seems.
    check_ram(modpack, PATH)

    # Check Install Integrity
    check_install_integrity(modpack, PATH, BASE_DIR)

    return True


def backup_old_mods(PATH):
    back_up_old(f"{PATH}\\mods")
    back_up_old(f"{PATH}\\config")
    back_up_old(f"{PATH}\\shaderpacks")


def initialize_settings(path, APPDATA_PATH):
    if not os.path.exists(path):
        if not os.path.exists(path):
            if os.path.exists(f'{APPDATA_PATH}\\.minecraft'):
                game_path = f'{APPDATA_PATH}\\.minecraft'
                settings = {'game_path': game_path}
                with open(path, 'w') as f:
                    f.write(json.dumps(settings))
            else:
                settings = {'game_path': ''}
                with open(path, 'w') as f:
                    f.write(json.dumps(settings))


def validate_settings(settings):
    # Check if settings are valid
    valid = {'game_path': False}
    if os.path.exists(settings['game_path']):
        print(Fore.RED + 'Game path not found!')
        valid['game_path'] = True
    return valid



def check_game_install_location(modpack, APPDATA_PATH): 
    found = False
    print(Fore.CYAN + '\nChecking game install location...\n')
    # Load settings to get game path
    settings = {}
    # Check if settings exist
    if not os.path.exists(f'{APPDATA_PATH}\\Mjolnir Modpack Manager\\GameSettings\\Minecraft_Settings.json'):
        print(Fore.RED + f'Settings not found at {APPDATA_PATH}\\Mjolnir Modpack Manager\\GameSettings\\Minecraft_Settings.json')
        print(Fore.CYAN + 'Creating settings...')
        initialize_settings(f'{APPDATA_PATH}\\Mjolnir Modpack Manager\\GameSettings\\Minecraft_Settings.json', APPDATA_PATH)
        print(Fore.GREEN + 'Settings created!')
    try:
        with open(f'{APPDATA_PATH}\\Mjolnir Modpack Manager\\GameSettings\\Minecraft_Settings.json', 'r') as f:
            settings = json.load(f)
    except:
        print(Fore.RED + f'Settings not found at {APPDATA_PATH}\\Mjolnir Modpack Manager\\GameSettings\\Minecraft_Settings.json')
    if settings == {}:
        initialize_settings(f'{APPDATA_PATH}\\Mjolnir Modpack Manager\\GameSettings\\Minecraft_Settings.json', APPDATA_PATH)
        with open(f'{APPDATA_PATH}\\Mjolnir Modpack Manager\\GameSettings\\Minecraft_Settings.json', 'r') as f:
            settings = json.load(f)
    if os.path.exists(settings['game_path']):
        print(Fore.GREEN + 'Minecraft found!')
        PATH = settings['game_path']
        found = True
    else:
        print(
            Back.RED + 'Minecraft not found! Please make sure Minecraft is installed and the path is correct.')
        PATH = ''
        found = False

    # Check if user wants to install to a different location
    while not found:
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
        # Check if path is valid
        if os.path.exists(PATH):
            print(Fore.GREEN + 'Minecraft found!')
            found = True
        else:
            print(Fore.RED + 'Minecraft not found!')
            found = False
    return PATH

def copy_pack(modpack, PATH, BASE_DIR, app, bonus_text):
    done = False
    copied = 0
    MAX_COPY = 0
    # Find number of files to copy
    for root, dirs, files in os.walk(f'{BASE_DIR}\\Downloads\\{modpack.pack_name}'):
        for file in files:
            MAX_COPY += 1
    if MAX_COPY == 0:
        ERROR_UI('Error', 'No files found in pack!', FATAL=True)
    # Copy pack to game folder
    # Copy mods folder

    bonus_text.configure(text='Copying mods...')
    app.update()

    print(Fore.GREEN + 'Copying pack to game folder... \n')
    # Make all directories in pack if missing
    for folder in os.listdir(f'{BASE_DIR}\\Downloads\\{modpack.pack_name}'):
        if os.path.isdir(f'{BASE_DIR}\\Downloads\\{modpack.pack_name}\\{folder}'):
            if not os.path.exists(f'{PATH}\\{folder}'):
                os.mkdir(f'{PATH}\\{folder}')
                print(Fore.GREEN + f'Created {folder} folder.')

    for folder in os.listdir(f'{BASE_DIR}\\Downloads\\{modpack.pack_name}'):
        # Check if it's a folder
        src_folder = f'{BASE_DIR}\\Downloads\\{modpack.pack_name}\\{folder}'
        if os.path.isdir(src_folder):
            print(Fore.GREEN + f'Copying {folder} folder...')
            bonus_text.configure(text=f'Copying {folder} folder...')
            app.update()
            dst_folder = f'{PATH}\\{folder}'
            copied = copy_folder_with_subfolders(
                src_folder, dst_folder, MAX_COPY, copied, app, bonus_text)
            print(Fore.MAGENTA +
                f'\tInstalled {copied} files to {folder} folder.\n')
            copied = 0

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


def copy_folder_with_subfolders(src, dst, MAX_COPY, copied, app, bonus_text):
    for item in os.listdir(src):
        bonus_text.configure(text=f'Copying {item}')
        app.update()
        copied += 1
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            if not os.path.exists(d):
                os.makedirs(d)
            copied = copy_folder_with_subfolders(
                s, d, MAX_COPY, copied, app, bonus_text)
        else:
            try:
                shutil.copy(s, d)
                copied += 1
            except PermissionError:
                # If file already exists, skip
                pass
    return copied


def run_mod_loader_installer(modpack, BASE_DIR):
    found = False
    # Ask user if they want to install mod loader
    print(Fore.YELLOW + f'Would you like to install {modpack.mod_loader}? ' + Fore.CYAN +
          '(Recommended Unless You Are Reinstalling Pack)' + Fore.YELLOW + ' (y/n)')
    layout = [[pg.Text(f'Would you like to install {modpack.mod_loader} v{modpack.mod_loader_version}?')],
              [pg.Text('(Recommended Unless You Are Reinstalling Pack)')],
              [pg.Button('Yes'), pg.Button('No')]]
    window = pg.Window('Mjolnir Mod Manager', layout)
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
    window = pg.Window('Mjolnir Mod Manager', layout)
    while True:
        event, values = window.read()
        if event in (None, 'Exit'):
            exit_app()
        elif event == 'OK!':
            window.close()
            break

    # Check if mod loader is already installed
    if modpack.mod_loader == 'Forge':
        install_forge(modpack, BASE_DIR)
    elif modpack.mod_loader == 'Fabric':
        install_fabric(modpack, BASE_DIR)
    else:
        print(Fore.YELLOW + 'Mod loader not found!')
        
        


def install_forge(modpack, BASE_DIR):
    found = False
    pattern = re.compile(r"forge-[\d.]+-[\d.]+-installer.jar")
    for file in os.listdir(f'{BASE_DIR}\\Downloads'):
        if re.match(pattern, file):
            found = True
            print(Fore.GREEN + 'Mod loader already downloaded!')
            break

    if found:
        # Run mod loader installer
        print(Fore.GREEN + 'Running mod loader installer...')
        # Check if user has java installed
        if not shutil.which('java'):
            print(Fore.RED + 'Java not found! Please install Java.')
            # Ask user to install java if not found (Show link to java download)
            layout = [[pg.Text('Java not found! After installing Java, press OK.')],
                        [pg.Text('https://www.java.com/en/download/')],
                        [pg.Button('OK')]]
            window = pg.Window('Mjolnir Mod Manager', layout)
            while True:
                event, values = window.read()
                if event == 'OK':
                    window.close()
                    break
        
        # Run mod loader installer jar file with java command
        os.system(f'java -jar {BASE_DIR}\\Downloads\\{file}')
    
        print(Fore.GREEN + 'Mod loader installed!')
    else:
        ERROR_UI(
            'Error', f'Unable to find {modpack.mod_loader} installer!', FATAL=True)
    return



def install_fabric(modpack, BASE_DIR):
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
    return


def check_launcher_profiles(modpack, PATH):
    print(Fore.GREEN +
          f'{modpack.game} - {modpack.game_version} [{modpack.mod_loader} - {modpack.mod_loader_version}]')
    print(Fore.GREEN + 'Checking launcher profiles...')
    # Check if launcher profiles exist
    if os.path.exists(f'{PATH}\\launcher_profiles.json'):
        # Check if mod loader is already installed
        with open(f'{PATH}\\launcher_profiles.json', 'r') as f:
            data = json.load(f)
            for profile in data['profiles']:
                print(Fore.GREEN + f'Checking {profile} profile...')
                if modpack.mod_loader.lower() in data['profiles'][profile]['name'].lower():
                    print(Fore.GREEN + 'Mod loader found installed!')
                    if modpack.mod_loader_version in data['profiles'][profile]['lastVersionId']:
                        print(Fore.GREEN + 'Mod loader version installed!')
                        return True
    print(Fore.YELLOW + 'Mod loader not installed!')
    return False

def check_ram(modpack, PATH):
    print("Checking RAM...")

    if not os.path.exists(f"{PATH}\\launcher_profiles.json"):
        return

    with open(f"{PATH}\\launcher_profiles.json", "r") as f:
        data = json.load(f)
    profile = next((p for p in data["profiles"] if modpack.mod_loader.lower() in data["profiles"][p]["name"].lower()), None)
    if profile:
        current_ram = int(next(arg[4:-1] for arg in data["profiles"][profile]["javaArgs"].split(" ") if arg.startswith("-Xmx")))
        if current_ram < modpack.recommended_ram:
            layout = [[pg.Text(f'RAM is too low!')],
            [pg.Text(f'Current RAM: {current_ram}GB')],
            [pg.Text(f"Recommended RAM: {modpack.recommended_ram}GB")],
            [pg.Text("Would you like to update the RAM to the recommended?")],
            [pg.Button('Yes'), pg.Button('No')]]
            window = pg.Window('Mjolnir Mod Manager', layout)
            while True:
                event, values = window.read()
                if event in (None, 'Exit'):
                    exit_app()
                elif event == 'Yes':
                    window.close()
                    data["profiles"][profile]["javaArgs"] = data["profiles"][profile]["javaArgs"].replace(
                    f"-Xmx{current_ram}G", f"-Xmx{modpack.recommended_ram}G")
                    # Make a copy before updating
                    shutil.copyfile(f"{PATH}\\launcher_profiles.json", f"{PATH}\\launcher_profiles.json.bak")
                    
                    with open(f"{PATH}\\launcher_profiles.json", "w") as f:
                        json.dump(data, f)
                    window.close()
                    break
                elif event == 'No':
                    window.close()
                    break


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
    else:
        ERROR_UI('Error', 'Game not supported!', FATAL=False)

def back_up_old(PATH):
    print(Fore.CYAN + f'\n{PATH}\n')
    folder_name = os.path.basename(os.path.normpath(PATH))
    if os.path.exists(f'{PATH}'):
        # Backup Minecraft mods to new folder with date
        current_date = datetime.datetime.now()
        current_date = current_date.strftime("%m-%d-%Y_%H-%M-%S")
        print(Fore.GREEN + f'Backing up old {folder_name} to ' + Fore.MAGENTA +
                f'{folder_name}_old_{current_date}' + Fore.GREEN + '...')
        shutil.copytree(f'{PATH}',
                    f'{PATH}_old_{current_date}')
        print(Fore.GREEN + 'Backup Complete!')
    else:
        print(Fore.GREEN + 'No existing mods found.')


def delete_old_mods(PATH):
    folder_name = os.path.basename(os.path.normpath(PATH))
    if os.path.exists(f'{PATH}'):
        # Delete old mods
        print(Fore.GREEN + f'Deleting old {folder_name}...')
        shutil.rmtree(f'{PATH}')
        print(Fore.GREEN + f'Old {folder_name} deleted!')
    else:
        print(Fore.GREEN + f'No existing {folder_name} found.')
