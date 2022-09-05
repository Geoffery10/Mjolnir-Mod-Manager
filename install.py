from ast import For
from http.client import FOUND
from pickle import GLOBAL
import shutil
from tkinter import E, N
import zipfile
from dotenv import load_dotenv
import os
import datetime
import subprocess
import colorama
from colorama import Fore, Back, Style
import urllib.request
import json

PACK_NAME = ''
PACK_VERSION = ''
CURRENT_VERSION = ''
GAME = ''
GAME_VERSION = ''
MOD_LOADER = ''
MOD_LOADER_VERSION = ''
APPDATA_PATH = os.getenv('APPDATA')
PATH = ''
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
URL=''
PACK = {}
FILES = []

# Color Presets
# ERROR_COLOR = Back.RED + Fore.WHITE
# SUCCESS_COLOR = Back.GREEN + Fore.WHITE

def get_dotenv():
    load_dotenv()
    global CURRENT_VERSION
    global URL
    CURRENT_VERSION = os.getenv('CURRENT_VERSION')
    URL = os.getenv('URL')

def get_json():
    global CURRENT_VERSION
    global URL
    print(Fore.GREEN + 'Getting Packs from Internet...')
    response = urllib.request.urlopen(URL)
    # Check if response is valid
    if response.status == 200:
        data = json.loads(response.read())
        print(Fore.GREEN + f'Packs v{data["CURRENT_VERSION"]} received!')

        packs = []
        for pack in data['PACKS']:
            packs.append(pack)
        select_pack(packs)
    else:
        print(Back.RED + 'Invalid response from server!')
        exit()

def select_pack(packs):

    global GAME
    global GAME_VERSION
    global MOD_LOADER
    global MOD_LOADER_VERSION
    global PACK_NAME
    global PACK_VERSION
    global PACK
    print(Fore.YELLOW + 'Which pack would you like to install?')
    for i in range(len(packs)):  # Alternate between Fore.MAGENTA and Fore.WHITE
        if i % 2 == 0:
            print(Fore.MAGENTA + 
                f"\t{i+1}. {packs[i]['PACK_NAME']} - {packs[i]['GAME']} [{packs[i]['GAME_VERSION']}]")
        else:
            print(Fore.WHITE + 
                f"\t{i+1}. {packs[i]['PACK_NAME']} - {packs[i]['GAME']} [{packs[i]['GAME_VERSION']}]")
    choice = input()
    try:
        choice = int(choice)
        if choice > len(packs) or choice < 1:
            print(Back.RED + 'Invalid choice! Please try again.')
            select_pack(packs)
        else:
            selected_pack = packs[choice-1]
            GAME = selected_pack['GAME']
            GAME_VERSION = selected_pack['GAME_VERSION']
            MOD_LOADER = selected_pack['MOD_LOADER']
            MOD_LOADER_VERSION = selected_pack['MOD_LOADER_VERSION']
            PACK_NAME = selected_pack['PACK_NAME']
            PACK_VERSION = selected_pack['PACK_VERSION']
            PACK = selected_pack
            print(
                Fore.GREEN + f"Installing {selected_pack['PACK_NAME']} - {selected_pack['GAME']} [{selected_pack['GAME_VERSION']}]")
    except ValueError:
        print(Back.RED + 'Invalid choice! Please try again.')
        select_pack(packs)

def print_title():
    global PACK
    if PACK['BANNER_URL'] != '':
        response = urllib.request.urlopen(PACK['BANNER_URL'])
        data = json.loads(response.read())
        print(Fore.MAGENTA + data['Banner'])
    else:
        print('Downloading Mods for ' + GAME)


def download_pack():
    global PACK
    global PATH
    global BASE_DIR
    global FILES

    # Initialize download folder
    if not os.path.exists(f'{BASE_DIR}\\Downloads'):
        os.mkdir(f'{BASE_DIR}\\Downloads')
    if not os.path.exists(f'{BASE_DIR}\\Downloads\\{PACK_NAME}'):
        os.mkdir(f'{BASE_DIR}\\Downloads\\{PACK_NAME}')
    else:
        # Delete Anything in the Folder

    
    # Download each file in the pack
    for file in PACK['PACK_URLS']:
        # Split the file name from the URL to get the file name
        file_name = file.split('/')[-1]
        FILES.append(file_name)
        print(f'Downloading {file_name}...')
        
        if file_name.endswith('.zip'):
            # Download the file
            urllib.request.urlretrieve(
                file, f'{BASE_DIR}\\Downloads\\{PACK_NAME}\\{file_name}')
            print(Fore.GREEN + f'{file_name} downloaded!')
            # Unzip the file
            with zipfile.ZipFile(f'{BASE_DIR}\\Downloads\\{PACK_NAME}\\{file_name}', 'r') as zip_ref:
                zip_ref.extractall(f'{BASE_DIR}\\Downloads\\{PACK_NAME}')
            print(Fore.GREEN + f'{file_name} unpacked!')
            # Delete Zip File

        else:
            # Download the file
            urllib.request.urlretrieve(
                file, f'{BASE_DIR}\\Downloads\\{PACK_NAME}\\{file_name}')
            print(Fore.GREEN + f'{file_name} downloaded!')

    print(Fore.GREEN + 'All files downloaded!')


def check_pack_integrity():
    global GAME
    print(Fore.CYAN + '\nChecking pack integrity...\n')
    if GAME == 'Minecraft':
        found_mods = 0
        found_config = 0
        found_shaders = 0
        found_fabric = 0
        # Check for folders
        if os.path.exists(f'{BASE_DIR}/mods'):
            print(Back.GREEN + '\tMods folder found!')
            found_mods = 1
        else:
            print(Back.RED +
                  '\tMods folder not found! Please try again.')
            exit()
        if os.path.exists(f'{BASE_DIR}/config'):
            print(Back.GREEN + '\tConfig folder found!')
            found_config = 1
        else:
            print(Back.RED +
                  '\tConfig folder not found! It might not be needed.')
        if os.path.exists(f'{BASE_DIR}/shaderpacks'):
            print(Back.GREEN + '\tShaderpacks folder found!')
            found_shaders = 1
        else:
            print(Back.RED +
                  '\tShaderpacks folder not found! It might not be needed.')
        if os.path.exists(f'{BASE_DIR}/fabric-installer.exe'):
            print(Back.GREEN + '\tFabric installer found!')
            found_fabric = 1
        else:
            print(Back.RED + '\tFabric installer not found!\nPlease download the latest version of the fabric installer from https://fabricmc.net/use/installer/')
        
        # Print percentage of found folders
        percent_found = ((found_mods + found_config + found_shaders + found_fabric) / 4) * 100
        print(Back.MAGENTA + f'\t{percent_found}% of folders found.')
    else:
        print(Back.RED +
              'Game unknown! Please check to make sure everything is downloaded correctly from my Discord server.')
        exit()
    print(Back.RESET + Fore.RESET)


""" 
def checkPackIntegrity():
    global PACK_NAME
    global CURRENT_VERSION
    if os.path.exists(f'{PACK_NAME}_v{CURRENT_VERSION}.zip'):
        print(f'Found {PACK_NAME}_v{CURRENT_VERSION}.zip!')
    else:
        print(
            f'Pack {PACK_NAME}_v{CURRENT_VERSION}.zip not found! Please download the latest pack from my Discord server.')
        exit()
"""

def check_game_install_location():
    global GAME
    global APPDATA_PATH
    global PATH
    found = False
    print(Fore.CYAN + '\nChecking game install location...\n')
    if GAME == 'Minecraft':
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
        print(Back.RED + 'Game unknown! Please check to make sure everything is downloaded correctly from my Discord server.')
        exit()

    # Check if user wants to install to a different location
    if found == False:
        print(Back.RED + f'{GAME} not found! Where is {GAME} installed?')
        PATH = get_path(PATH)
    else:
        print(
            Fore.GREEN + f'Found {GAME} installed in {PATH}. ' + Fore.YELLOW + '\nWould you like to install mods here? (y/n)')
        PATH = get_path(PATH)

def get_path(PATH):
    # Check for valid path
    temp_PATH = ''
    choice = input()
    if choice == 'n' or PATH == '':
        print(Fore.YELLOW + 'Please enter the path to the game folder.')
        temp_PATH = input()
        print(Fore.GREEN + f'Installing to {temp_PATH}')
        if os.path.exists(temp_PATH):
            print(Fore.GREEN + 'Path found!')
            PATH = temp_PATH
        else:
            print(Back.RED + 'Path not found! Please try again.')
            get_path(PATH)
    else:
        print(Fore.GREEN + f'Installing to {PATH}')
    return PATH


def back_up_old():
    global PATH
    global GAME
    if GAME == 'Minecraft':
        if os.path.exists(f'{PATH}\\mods'):
            # Ask user if they want to back up old mods
            print(Fore.YELLOW + 'Would you like to back up your old mods? (y/n)')
            choice = input()
            if choice == 'y':
                # Backup Minecraft mods to new folder with date
                current_date = datetime.datetime.now()
                current_date = current_date.strftime("%m-%d-%Y_%H-%M-%S")
                print(Fore.GREEN + f'Backing up old mods to ' + Fore.MAGENTA + '"mods_old_{current_date}"' + Fore.GREEN + '...')
                os.rename(f'{PATH}\\mods', f'{PATH}\\mods_old_{current_date}')
                print(Fore.GREEN + 'Done!')
        else:
            print(Fore.GREEN + 'No existing mods found.')
    else:
        print(Back.RED + 'Game unknown! Please check to make sure everything is downloaded correctly from my Discord server.')
        exit()

def copy_pack():
    global PACK_NAME
    global CURRENT_VERSION
    global PATH
    global GAME
    copied = 0
    if GAME == 'Minecraft':
        # Copy pack to game folder
        # Copy mods folder
        print(Fore.GREEN + 'Copying pack to game folder... \n')
        if not os.path.exists(f'{PATH}\\mods'):
            os.makedirs(f'{PATH}\\mods')
        for file in os.listdir(f'{BASE_DIR}\\mods'):
            if file.endswith('.jar'):
                shutil.copy(f'{BASE_DIR}\\mods\\{file}', f'{PATH}\\mods')
                print(Back.GREEN + f'\tCopied {file} to mods folder.')
                copied += 1
        print(Fore.GREEN + f'Copied {copied} files to mods folder.\n')
        copied = 0
        # Copy config folder
        if not os.path.exists(f'{PATH}\\config'):
            os.makedirs(f'{PATH}\\config')
        for file in os.listdir(f'{BASE_DIR}\\config'):
            shutil.copy(f'{BASE_DIR}\\config\\{file}', f'{PATH}\\config')
            print(Back.GREEN + f'\tCopied {file} to config folder.')
            copied += 1
        print(Fore.GREEN + f'Copied {copied} files to config folder.\n')
        copied = 0
        # Copy shaderpacks folder
        if not os.path.exists(f'{PATH}\\shaderpacks'):
            os.makedirs(f'{PATH}\\shaderpacks')
        for file in os.listdir(f'{BASE_DIR}\\shaderpacks'):
            shutil.copy(f'{BASE_DIR}\\shaderpacks\\{file}', f'{PATH}\\shaderpacks')
            print(Back.GREEN + f'\tCopied {file} to shaderpacks folder.')
            copied += 1
        print(Fore.GREEN + f'Copied {copied} files to shaderpacks folder.\n')
        copied = 0
        print(Fore.GREEN + 'Done installing pack!\n')
    else:
        print(Back.RED + 'Game unknown! Please check to make sure everything is downloaded correctly from my Discord server.')
        exit()

def unzip_pack():
    global PACK_NAME
    global CURRENT_VERSION
    global PATH
    print('Unzipping pack...')
    with zipfile.ZipFile(f'{PACK_NAME}_v{CURRENT_VERSION}.zip', 'r') as zip_ref:
        zip_ref.extractall(f'{PATH}\\')
    print('Pack unzipped!')


def run_fabric_installer():
    global PATH
    # Ask user if they want to install Fabric
    print(Fore.YELLOW + 'Would you like to install Fabric? ' + Fore.CYAN +
          '(Recommended Unless You Are Reinstalling Pack)' + Fore.YELLOW + ' (y/n)')
    choice = input()
    if choice == 'y':
        # Run Fabric installer executable
        print(Fore.GREEN + 'Running Fabric installer...')
        if os.path.exists(f'{BASE_DIR}\\fabric-installer.exe'):
            print(Fore.GREEN + 'Fabric installer found!')
            print(Back.MAGENTA + f'Please install Fabric {FABRIC_VERSION} to the game folder.')
            subprocess.check_call([f'{BASE_DIR}\\fabric-installer.exe'])
        else:
            print(Back.RED + 'Fabric installer not found! Please check to make sure everything is downloaded correctly from my Discord server.')


def check_install_integrity():
    global PATH
    global GAME
    # Ask user if they want to check install integrity
    print(Fore.YELLOW + 'Would you like to check install integrity? (y/n)')
    choice = input()
    if choice == 'y':
        print(Fore.CYAN + '\nChecking install integrity...')
        if GAME == 'Minecraft':
            tests = [0, 0, 0]
            # Check if mods folder exists
            if os.path.exists(f'{PATH}\\mods'):
                print(Fore.GREEN + 'Mods folder found!')

                # Check if mods are the same as the ones in the pack
                installed_files = [f for f in os.listdir(
                    f"{PATH}\\mods") if os.path.isfile(f)]
                pack_files = [f for f in os.listdir(
                    f"{BASE_DIR}\\mods") if os.path.isfile(f)]
                if installed_files == pack_files:
                    print(Fore.GREEN + 'Mods are the same as the ones in the pack!')
                    tests[0] = 1
                else:
                    print(Back.RED + 'Mods are not the same as the ones in the pack!')
                    print(
                        Back.RED + 'Please check to make sure everything is downloaded correctly from my Discord server.')
            else:
                print(Back.RED + 'Mods folder not found! Please check to make sure everything is downloaded correctly from my Discord server.')
            
            # Check if config folder exists
            if os.path.exists(f'{PATH}\\config'):
                print(Fore.GREEN + 'Config folder found!')

                # Check if config from pack is the same as the one in the game
                installed_files = [f for f in os.listdir(
                    f"{PATH}\\config") if os.path.isfile(f)]
                pack_files = [f for f in os.listdir(
                    f"{BASE_DIR}\\config") if os.path.isfile(f)]
                tests[1] = 1
                for file in pack_files:
                    if file in pack_files:
                        print(Fore.GREEN + f'{file} found in pack!')
                    else:
                        print(Back.RED + f'{file} not found in pack!')
                        print(
                            Back.RED + 'Please check to make sure everything is downloaded correctly from my Discord server.')
                        tests[1] = 0
                if tests[1] == 1:
                    print(Fore.GREEN +
                          'Config from pack is the same as the one in the game!')
            else:
                print(Back.RED + 'Config folder not found! Please check to make sure everything is downloaded correctly from my Discord server.')
            
            # Check if shaderpacks folder exists
            if os.path.exists(f'{PATH}\\shaderpacks'):
                print(Fore.GREEN + 'Shaderpacks folder found!')

                # Check if shaderpacks from pack is the same as the one in the game
                installed_files = [f for f in os.listdir(
                    f"{PATH}\\shaderpacks") if os.path.isfile(f)]
                pack_files = [f for f in os.listdir(
                    f"{BASE_DIR}\\shaderpacks") if os.path.isfile(f)]
                tests[2] = 1
                for file in pack_files:
                    if file in pack_files:
                        print(Fore.GREEN + f'{file} found in pack!')
                    else:
                        print(Back.RED + f'{file} not found in pack!')
                        print(
                            Back.RED + 'Please check to make sure everything is downloaded correctly from my Discord server.')
                        tests[2] = 0
                if tests[2] == 1:
                    print(Fore.GREEN + 'Shaderpacks are the same as the ones in the pack!')
            else:
                print(Back.RED + 'Shaderpacks folder not found! Please check to make sure everything is downloaded correctly from my Discord server.')

            percent_passed = 0
            for test in tests:
                if test == 1:
                    percent_passed += 1.0
            percent_passed = int((percent_passed / len(tests)) * 100)
            print(Fore.MAGENTA + f'{percent_passed}% of tests passed.')
    else:
        print(Back.RED + f'Game "{GAME}" was unknown. Skipping install integrity check...')
                


    

if __name__ == '__main__':
    # Load Initial Variables
    colorama.init(autoreset=True)
    get_dotenv()

    # Print Developer Info
    print(Fore.MAGENTA + "Installer Designed by: " +
          Fore.CYAN + "Geoffery Powell")
    print(Fore.MAGENTA + "GitHub: " + Fore.CYAN +
          "https://github.com/Geoffery10")
    print(Fore.MAGENTA + "Discord: " + Fore.CYAN + "Geoffery10#6969")
    print(Fore.MAGENTA + "Installer Version: " +
          Fore.CYAN + f"v{CURRENT_VERSION}\n\n")

    # Load Pack Info 
    get_json()
    print_title()

    # Download Pack
    download_pack()
    check_pack_integrity()
    check_game_install_location()
    back_up_old()
    copy_pack()
    if GAME == 'Minecraft':
        run_fabric_installer()
    check_install_integrity()

    print(Fore.MAGENTA + '\nAll Done! Thank you for using my modpack installer!')
    print(Fore.GREEN + 'Press Enter to exit...')
    # Wait for user to close with enter key
    input()

