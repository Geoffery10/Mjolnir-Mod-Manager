# This installs bonelab mods
# Bonelab Mods come in two types
# MelonLoader Mods that are installed into the game folder
# Standard Mods are installed into the LocalLow mods folder

import re
import subprocess
from colorama import Fore
import file_manager
from ui_menus import ERROR_UI, exit_app
import PySimpleGUI as pg
import os
import file_manager

def bonelab(modpack, BASE_DIR, APPDATA_PATH, FILES):
    # Check modpack to see if it has melonloader mods, locallow mods, or both
    if os.path.exists(f'{BASE_DIR}\\Downloads\\{modpack.pack_name}\\MelonLoader'):
        # Copy MelonLoader mods
        melon_mods_path = f'{BASE_DIR}\\Downloads\\{modpack.pack_name}\\MelonLoader'
        bonelabSteamApps(modpack, melon_mods_path)
    
    if os.path.exists(f'{BASE_DIR}\\Downloads\\{modpack.pack_name}\\Mods'):
        # Copy LocalLow mods
        mods_path = f'{BASE_DIR}\\Downloads\\{modpack.pack_name}\\Mods'
        bonelabLocalLow(mods_path)
    return True


def bonelabLocalLow(mods_path):
    found = False
    # Get LocalLow install path
    username = os.getlogin()
    if os.path.exists(f'C:\\Users\\{username}\\AppData\\LocalLow\\Stress Level Zero\\BONELAB'):
        print(Fore.GREEN + 'Bonelab found!')
        PATH = f'C:\\Users\\{username}\\AppData\\LocalLow\\Stress Level Zero\\BONELAB'
        found = True

    if not found:
        PATH = file_manager.path_finder('Bonelab LocalLow Mods Folder', 'This is the folder where Bonelab mods are installed')
    else:
        # Check if mods folder exists
        if not os.path.exists(f'{PATH}\\Mods'):
            os.mkdir(f'{PATH}\\Mods')
        else:
            # Check if mods folder is empty
            if os.listdir(f'{PATH}\\Mods') == []:
                print(Fore.GREEN + 'Mods folder is empty!')
            else:
                # Check if user wants to backup mods folder
                file_manager.ask_for_backup(f'{PATH}\\Mods')

                # Check is user wants to delete old mods folder
                file_manager.ask_for_delete(f'{PATH}\\Mods')
        # Copy mods to mods folder
        for folder in os.listdir(mods_path):
            file_manager.copy_folder(mods_path, f'{PATH}\\Mods\\{folder}')

        # Check copy integrity
        if file_manager.check_integrity(mods_path, f'{PATH}\\Mods'):
            print(Fore.GREEN + 'Mods copied successfully!')
        else:
            ERROR_UI('ERROR', 'Mods were not copied successfully. Please try again.', True)
            exit_app()
    return True


def bonelabSteamApps(modpack, melon_mods_path):
    found = False
    # Find Game Install Path
    # Check if Bonelab is installed
    # If it is, copy mods to game folder
    LikelyPath = f'C:\\Program Files (x86)\\Steam\\steamapps\\common\\BONELAB'
    if os.path.exists(LikelyPath):
        print(Fore.GREEN + 'Bonelab found!')
        PATH = LikelyPath
        found = True
    return

def find_file(file_name):
    p = subprocess.run(f"dir \"{file_name}\" /s ", capture_output=True, shell=True, cwd="C:\\")
    val = p.stdout.decode()
    loc = re.search('Directory of .*', val)
    if loc != None:
        return val[loc.start()+13: loc.end()]
    else:
        return "couldn't find item"
