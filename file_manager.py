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

def path_finder(folder, additional_info=""):
    # This code will ask the user for the correct path to an install folder and check 
    # if it is valid. If it is not valid, it will ask again.
    layout = [
        [pg.Text(f'Please select the correct path to the {folder}:')]]
    if additional_info != "":
        layout.append([pg.Text(additional_info)])
    layout.append([pg.InputText(), pg.FolderBrowse()])
    layout.append([pg.Button('OK'), pg.Button('Exit')])
    window = pg.Window('ModDude', layout)
    while True:
        event, values = window.read()
        if event in (None, 'Exit'):
            exit_app()
        elif event == 'OK':
            if os.path.exists(values[0]):
                window.close()
                return values[0]
            else:
                ERROR_UI('Error', 'Path not found!')
                window.close()
                path_finder(folder, additional_info)


def copy_folder(src, dst):
    # Copy folder to destination
    # Check if destination folder exists
    if os.path.exists(dst):
        # Remove old folder
        delete_old(dst)
    try:
        shutil.copytree(src, dst)
    except OSError as e:
        print("Error: %s : %s" % (src, e.strerror))


def check_integrity(src, destination):
    # Check if all files are in the destination folder
    for file in os.listdir(src):
        if not os.path.exists(f'{destination}\\{file}'):
            return False
    return True

def ask_for_backup(PATH):
    # Ask user if they want to backup the folder
    layout = [
        [pg.Text(f'Would you like to backup the folder {PATH}?')],
        [pg.Button('Yes'), pg.Button('No')]
    ]
    window = pg.Window('ModDude', layout)
    while True:
        event, values = window.read()
        if event in (None, 'Exit'):
            exit_app()
        elif event == 'Yes':
            backup_old(PATH)
            window.close()
            return True
        elif event == 'No':
            window.close()
            return False

def ask_for_delete(PATH):
    # Split path into list
    path_list = PATH.split('\\')
    # Ask user if they want to delete the folder
    layout = [
        [pg.Text(f'Would you like to delete the old {PATH} folder? This is only recommended if you have backed up the folder and are installing a completely different modpack.')],
        [pg.Text(f'DELETING THE FOLDER WILL PERMANENTLY DELETE ALL FILES IN THE FOLDER!')],
        [pg.Button(f'Yes Delete All of The Files in the {path_list[-1]} Folder'), pg.Button('No')]
    ]
    window = pg.Window('ModDude', layout)
    while True:
        event, values = window.read()
        if event in (None, 'Exit'):
            exit_app()
        elif event == 'Yes':
            delete_old(PATH)
            window.close()
            return True
        elif event == 'No':
            window.close()
            return False

def backup_old(PATH):
    # Backup selected folder to a folder of the same name with a timestamp
    # Get current date and time in format: YYYY-MM-DD_HH-MM-SS
    now = datetime.datetime.now()
    now = now.strftime("%Y-%m-%d_%H-%M-%S")

    # Create backup folder
    os.mkdir(f'{PATH}_{now}')

    # Copy folders to backup folder
    for folder in os.listdir(PATH):
        try:
            shutil.copytree(f'{PATH}\\{folder}', f'{PATH}_{now}\\{folder}')
        except OSError as e:
            print("Error: %s : %s" % (f'{PATH}\\{folder}', e.strerror))
    
    return

def delete_old(PATH):
    # Delete old folder
    try:
        shutil.rmtree(PATH)
    except OSError as e:
        print("Error: %s : %s" % (PATH, e.strerror))

def delete_temp_files(modpack, BASE_DIR):
    # Delete all files in the temp folder
    try:
        shutil.rmtree(f'{BASE_DIR}\\Downloads\\{modpack.pack_name}')
    except OSError as e:
        print("Error: %s : %s" %
              (f'{BASE_DIR}\\Downloads\\{modpack.pack_name}', e.strerror))
