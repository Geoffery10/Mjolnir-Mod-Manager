# This installs bonelab mods
# Bonelab Mods come in two types
# MelonLoader Mods that are installed into the game folder
# Standard Mods are installed into the LocalLow mods folder

import re
import shutil
import subprocess
from colorama import Fore
import file_manager
from ui_menus import ERROR_UI, exit_app
import PySimpleGUI as pg
import os
import file_manager

def bonelab(modpack, BASE_DIR, APPDATA_PATH, FILES):
    # Check modpack to see if it has melonloader mods, locallow mods, or both
    if os.path.exists(f'{BASE_DIR}\\Downloads\\{modpack.pack_name}\\GameMods'):
        # Copy MelonLoader mods
        melon_mods_path = f'{BASE_DIR}\\Downloads\\{modpack.pack_name}\\GameMods'
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
            # Copy file structure to game folder
            done = False
            MAX_COPY = len(os.listdir(mods_path))
            copied = 0
            layout = [[pg.Text('Copying mods...')],
                    [pg.ProgressBar(MAX_COPY, orientation='h', size=(20, 20), key='progressbar_copied')]]
            window = pg.Window('ModDude', layout)
            progress_bar = window['progressbar_copied']
            while not done:
                event, values = window.read(timeout=10)
                if event in (None, 'Exit'):
                    exit_app()
                print(Fore.GREEN + 'Copying pack to game folder... \n')
                for file in os.listdir(mods_path):
                    # Copy files/folders and only delete files that conflict
                    # Copy directory structure to game folder
                    if os.path.isdir(f'{mods_path}\\{file}'):
                        shutil.copytree(f'{mods_path}\\{file}', f'{PATH}\\{file}')
                    else:
                        shutil.copy(f'{mods_path}\\{file}', f'{PATH}\\{file}')
                    copied += 1
                    progress_bar.UpdateBar(copied / MAX_COPY * 100)
                done = True
                window.close()

        # Check copy integrity
        if file_manager.check_integrity(mods_path, f'{PATH}\\Mods'):
            print(Fore.GREEN + 'Mods copied successfully!')
        else:
            ERROR_UI('ERROR', 'Mods were not copied successfully. Please try again.', True)
    return True


def bonelabSteamApps(modpack, melon_mods_path):
    found = False
    # Find Game Install Path
    # Check if Bonelab is installed
    # If it is, copy mods to game folder
    LikelyPath = f'C:\\Program Files (x86)\\Steam\\steamapps\\common\\BONELAB'
    if os.path.exists(LikelyPath):
        print(Fore.GREEN + 'Bonelab Game found!')
        PATH = LikelyPath
        found = True

    if not found:
        PATH = file_manager.path_finder('Bonelab Game Folder', 'This is the folder where Bonelab is installed')
    else:      
        # ! BACKUP NEEDS ADDED BUT IS MISSING DUE TO THE COMPLEXITY OF THE GAME FOLDER
        
        # Copy file structure to game folder
        done = False
        MAX_COPY = len(os.listdir(melon_mods_path))
        copied = 0
        layout = [[pg.Text('Copying mods...')],
                  [pg.ProgressBar(MAX_COPY, orientation='h', size=(20, 20), key='progressbar_copied')]]
        window = pg.Window('ModDude', layout)
        progress_bar = window['progressbar_copied']
        while not done:
            event, values = window.read(timeout=10)
            if event in (None, 'Exit'):
                exit_app()
            print(Fore.GREEN + 'Copying pack to game folder... \n')
            for folder in os.listdir(melon_mods_path):
                # Copy files/folders and don't delete files that conflict
                if not os.path.exists(f'{PATH}\\{folder}'):
                    if os.path.isdir(f'{melon_mods_path}\\{folder}'):
                            shutil.copytree(f'{melon_mods_path}\\{folder}', f'{PATH}\\{folder}')
                    else:
                        shutil.copy(f'{melon_mods_path}\\{folder}', f'{PATH}\\{folder}')
                copied += 1
                progress_bar.UpdateBar(copied / MAX_COPY * 100)
            done = True
            window.close()
        
        # Check copy integrity
        if file_manager.check_integrity(melon_mods_path, PATH):
            print(Fore.GREEN + 'Mods copied successfully!')
        else:
            ERROR_UI('ERROR', 'Mods were not copied successfully. Please try again.', True)

    return


# CODED BY Alex Olson (CURRENTLY JUST FOR TESTING)
def find_file(file_name):
    p = subprocess.run(f"dir \"{file_name}\" /s ", capture_output=True, shell=True, cwd="C:\\")
    val = p.stdout.decode()
    loc = re.search('Directory of .*', val)
    if loc != None:
        return val[loc.start()+13: loc.end()]
    else:
        return "couldn't find item"
