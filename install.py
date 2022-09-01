import imp
import zipfile
from dotenv import load_dotenv
import os
import datetime
import subprocess

PACK_NAME = ''
CURRENT_VERSION = ''
GAME = ''
GAME_VERSION = ''
FABRIC_VERSION = ''
APPDATA_PATH = os.getenv('APPDATA')
PATH = ''

def get_dotenv():
    load_dotenv()
    global PACK_NAME
    global CURRENT_VERSION
    global GAME
    global GAME_VERSION
    PACK_NAME = os.getenv('PACK_NAME')
    CURRENT_VERSION = os.getenv('CURRENT_VERSION')
    GAME = os.getenv('GAME')
    GAME_VERSION = os.getenv('GAME_VERSION')
    if GAME == 'Minecraft':
        global FABRIC_VERSION
        FABRIC_VERSION = os.getenv('FABRIC_VERSION')

def printTitle():
    if GAME == 'Minecraft':
        print('')
        print('██╗   ██╗ ██████╗  ██████╗ ██████╗ ██████╗  █████╗ ███████╗██╗██╗         ███╗   ███╗ ██████╗ ██████╗ ███████╗')
        print('╚██╗ ██╔╝██╔════╝ ██╔════╝ ██╔══██╗██╔══██╗██╔══██╗██╔════╝██║██║         ████╗ ████║██╔═══██╗██╔══██╗██╔════╝')
        print(' ╚████╔╝ ██║  ███╗██║  ███╗██║  ██║██████╔╝███████║███████╗██║██║         ██╔████╔██║██║   ██║██║  ██║███████╗')
        print('  ╚██╔╝  ██║   ██║██║   ██║██║  ██║██╔══██╗██╔══██║╚════██║██║██║         ██║╚██╔╝██║██║   ██║██║  ██║╚════██║')
        print('   ██║   ╚██████╔╝╚██████╔╝██████╔╝██║  ██║██║  ██║███████║██║███████╗    ██║ ╚═╝ ██║╚██████╔╝██████╔╝███████║')
        print('   ╚═╝    ╚═════╝  ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝╚══════╝    ╚═╝     ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝')
        print('                                                                                                              ')
    else:
        print('Downloading Mods for ' + GAME)
                                                                                                                
   
def checkPackIntegrity():
    global PACK_NAME
    global CURRENT_VERSION
    if os.path.exists(f'{PACK_NAME}_v{CURRENT_VERSION}.zip'):
        print(f'Found {PACK_NAME}_v{CURRENT_VERSION}.zip!')
    else:
        print(
            f'Pack {PACK_NAME}_v{CURRENT_VERSION}.zip not found! Please download the latest pack from my Discord server.')
        exit()

def checkGameInstallLocation():
    global GAME
    global APPDATA_PATH
    global PATH
    found = False
    if GAME == 'Minecraft':
        if os.path.exists(f'{APPDATA_PATH}\.minecraft'):
            print('Minecraft found!')
            PATH = f'{APPDATA_PATH}\.minecraft'
            found = True
        else:
            print('Minecraft not found! Please install Minecraft if you haven\' already.')
            PATH = ''
            found = False
    else:
        print('Game unknown! Please check to make sure everything is downloaded correctly from my Discord server.')
        exit()

    # Check if user wants to install to a different location
    if found == False:
        print(f'{GAME} not found! Where is {GAME} installed?')
        PATH = getPath(PATH)
    else:
        print(f'Found {GAME} installed in {PATH}. \nWould you like to install mods somewhere else? (y/n)')
        PATH = getPath(PATH)

def getPath(PATH):
    # Check for valid path
    temp_PATH = ''
    choice = input()
    if choice == 'y' or PATH == '':
        print('Please enter the path to the game folder.')
        temp_PATH = input()
        print(f'Installing to {temp_PATH}')
        if os.path.exists(temp_PATH):
            print('Path found!')
            PATH = temp_PATH
        else:
            print('Path not found! Please try again.')
            getPath(PATH)
    else:
        print(f'Installing to {PATH}')
    return PATH

def backUpOld():
    global PATH
    global GAME
    if GAME == 'Minecraft':
        if os.path.exists(f'{PATH}\\mods'):
            # Ask user if they want to back up old mods
            print('Would you like to back up your old mods? (y/n)')
            choice = input()
            if choice == 'y':
                print('Backing up old mods...')

                # Backup Minecraft mods to new folder with date
                current_date = datetime.datetime.now()
                current_date = current_date.strftime("%m-%d-%Y_%H-%M-%S")
                os.rename(f'{PATH}\\mods', f'{PATH}\\mods_old_{current_date}')
        else:
            print('No mods found!')
    else:
        print('Game unknown! Please check to make sure everything is downloaded correctly from my Discord server.')
        exit()


def unzipPack():
    global PACK_NAME
    global CURRENT_VERSION
    global PATH
    print('Unzipping pack...')
    with zipfile.ZipFile(f'{PACK_NAME}_v{CURRENT_VERSION}.zip', 'r') as zip_ref:
        zip_ref.extractall(f'{PATH}\\')
    print('Pack unzipped!')


def runFabricInstaller():
    global PATH
    # Run Fabric installer executable
    print('Running Fabric installer...')
    if os.path.exists(f'{PATH}\\fabric-installer.exe'):
        print('Fabric installer found!')
        print(f'Please install Fabric {FABRIC_VERSION} to the game folder.')
        subprocess.check_call([f'{PATH}\\fabric-installer.exe'])

if __name__ == '__main__':
    get_dotenv()
    printTitle()
    checkPackIntegrity()
    checkGameInstallLocation()
    backUpOld()
    unzipPack()
    runFabricInstaller()

    print('\nAll Done! Thank you for using my modpack installer!')

