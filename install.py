import sys
from packaging import version
import PySimpleGUI as pg
import shutil
import zipfile
from dotenv import load_dotenv
import os
import datetime
import subprocess
import colorama
from colorama import Fore, Back, Style
import requests
import json

CURRENT_VERSION = ''
URL = ''
PACK_NAME = ''
PACK_VERSION = ''
GAME = ''
GAME_VERSION = ''
MOD_LOADER = ''
MOD_LOADER_VERSION = ''
APPDATA_PATH = os.getenv('APPDATA')
PATH = ''
SUPPORTED_GAMES = []
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
URL=''
PACK = {}
FILES = []
CLOSE_APP = False

# Color Presets
# ERROR_COLOR = Back.RED + Fore.WHITE
# SUCCESS_COLOR = Back.GREEN + Fore.WHITE

def get_json():
    global CURRENT_VERSION
    global URL
    if not URL == '':
        print(Fore.GREEN + 'Getting Packs from Internet...')
        response = requests.get(URL)
        # Check if response is valid
        if response.status_code == 200:
            data = response.json()
            print(Fore.GREEN + f'Packs v{data["CURRENT_VERSION"]} received!')

            # Check if packs are up to date
            if version.parse(CURRENT_VERSION) < version.parse(data['CURRENT_VERSION']):
                ERROR_UI('Out of Date', 'ModDude! is out of date! Please update the installer.', FATAL=True)

            packs = []
            for pack in data['PACKS']:
                packs.append(pack)
            select_pack(packs)
        else:
            ERROR_UI('Error', 'Error getting packs from internet! Please check your internet connection and try again!', FATAL=True)
    else:
        ERROR_UI('Error', 'No URL specified! Please contact the developer!', FATAL=True)

def print_dev_info():
    print(Fore.MAGENTA + "Installer Designed by: " +
          Fore.CYAN + "Geoffery Powell")
    print(Fore.MAGENTA + "GitHub: " + Fore.CYAN +
          "https://github.com/Geoffery10")
    print(Fore.MAGENTA + "Discord: " + Fore.CYAN + "Geoffery10#6969")
    print(Fore.MAGENTA + "Installer Version: " +
          Fore.CYAN + f"v{CURRENT_VERSION}")
    print(Fore.MAGENTA + "Supported Games: " +
          Fore.CYAN + str(SUPPORTED_GAMES) + "\n\n")

def select_pack(packs):

    global GAME
    global GAME_VERSION
    global MOD_LOADER
    global MOD_LOADER_VERSION
    global PACK_NAME
    global PACK_VERSION
    global PACK
    print(Fore.YELLOW + 'Which pack would you like to install?')
    layout = [
        [pg.Text(
            'Select a pack to install:')]]
    for i in range(len(packs)):  # Alternate between Fore.MAGENTA and Fore.WHITE
        pack_name = f"{packs[i]['PACK_NAME']} v{packs[i]['PACK_VERSION']} - {packs[i]['GAME']} v{packs[i]['GAME_VERSION']}"
        layout.append([pg.Button(pack_name)])
    layout.append([pg.Button('Exit')])
    window = pg.Window('ModDude', layout)
    while True:
        event, values = window.read()
        if event in (None, 'Exit'):
            exit_app()
        else:
            PACK_NAME = event
            print(Fore.GREEN + f'Installing {PACK_NAME}...')
            break
    
    # Find pack by friendly name
    print(Fore.GREEN + 'Finding pack...')
    for pack in packs:
        pack_name = f"{pack['PACK_NAME']} v{pack['PACK_VERSION']} - {pack['GAME']} v{pack['GAME_VERSION']}"
        if pack_name == PACK_NAME:
            print(Fore.GREEN + 'Pack found!')
            selected_pack = pack
            GAME = selected_pack['GAME']
            GAME_VERSION = selected_pack['GAME_VERSION']
            MOD_LOADER = selected_pack['MOD_LOADER']
            MOD_LOADER_VERSION = selected_pack['MOD_LOADER_VERSION']
            PACK_NAME = selected_pack['PACK_NAME']
            PACK_VERSION = selected_pack['PACK_VERSION']
            PACK = selected_pack
            window.close()
            break

def print_title():
    global PACK
    if PACK['BANNER_URL'] != '':
        response = requests.get(PACK['BANNER_URL'])
        data = response.json()
        print(Fore.MAGENTA + data['Banner'])
    else:
        print('Downloading Mods for ' + GAME)


def download_pack():
    global PACK
    global PATH
    global BASE_DIR
    global FILES
    extra_steps = 2
    progress = 0
    # if PACK['BANNER_URL'].endswith('.png'):
    #     layout = [pg.Image(PACK['BANNER_URL'])]
    layout = [
        [pg.Text('Start Downloading Mods... This may take a while!')],
        [pg.Text(f'Pack Files to Download: {len(PACK["PACK_URLS"])}')],
        [pg.ProgressBar(100, orientation='h', size=(20, 20), key='progressbar')],
        [pg.Button('Start Download')]]
    window = pg.Window('ModDude', layout)
    progress_bar = window['progressbar']
    # Get Step Size for Progress Bar
    step_size = int(100 / (len(PACK['PACK_URLS']) + extra_steps))

    while True:
        event, values = window.read(timeout=800)
        if event in (None, 'Exit'):
            exit_app()
        elif event == 'Start Download':
            progress += step_size
            progress_bar.UpdateBar(progress)
            # Initialize download folder
            if not os.path.exists(f'{BASE_DIR}\\Downloads'):
                os.mkdir(f'{BASE_DIR}\\Downloads')
            if not os.path.exists(f'{BASE_DIR}\\Downloads\\{PACK_NAME}'):
                os.mkdir(f'{BASE_DIR}\\Downloads\\{PACK_NAME}')
            else:
                # Delete Anything in the Folder
                try:
                    shutil.rmtree(f'{BASE_DIR}\\Downloads\\{PACK_NAME}')
                    os.mkdir(f'{BASE_DIR}\\Downloads\\{PACK_NAME}')
                except OSError as e:
                    ERROR_UI('Error', 'Error deleting old files! Please close any open files and try again!', FATAL=True)
            progress += step_size
            progress_bar.UpdateBar(progress)

            # Download each file in the pack
            for file in PACK['PACK_URLS']:
                # Split the file name from the URL to get the file name
                file_name = file.split('/')[-1]
                FILES.append(file_name)
                print(Fore.GREEN + f'Downloading {file_name}...')

                if file_name.endswith('.zip'):
                    # Download the file
                    r = requests.get(file, allow_redirects=True)
                    # Write the file to the downloads folder
                    if r.status_code == 200:
                        open(f'{BASE_DIR}\\Downloads\\{PACK_NAME}\\{file_name}',
                            'wb').write(r.content)
                        print(Fore.GREEN + f'{file_name} downloaded!')
                        # Unzip the file
                        with zipfile.ZipFile(f'{BASE_DIR}\\Downloads\\{PACK_NAME}\\{file_name}', 'r') as zip_ref:
                            zip_ref.extractall(f'{BASE_DIR}\\Downloads\\{PACK_NAME}')
                        print(Fore.GREEN + f'{file_name} unpacked!')
                        # Delete Zip File
                        os.remove(f'{BASE_DIR}\\Downloads\\{PACK_NAME}\\{file_name}')
                    else:
                        ERROR_UI('Error', f'Error downloading {file_name}! Please try again later!', FATAL=True)
                else:
                    # Download the file
                    r = requests.get(file, allow_redirects=True)
                    # Write the file to the downloads folder
                    if r.status_code == 200:
                        open(f'{BASE_DIR}\\Downloads\\{PACK_NAME}\\{file_name}',
                            'wb').write(r.content)
                        print(Fore.GREEN + f'{file_name} downloaded!')
                progress += step_size
                progress_bar.UpdateBar(progress)

            progress += step_size
            progress_bar.UpdateBar(progress)
            window.close()
            break
        if progress >= 100:
            break
    

    print(Fore.MAGENTA + 'All files downloaded!')


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
        layout = [
            [pg.Text(
                'Game unknown! Please check to make sure everything is downloaded correctly.')],
            [pg.Button('OK')]]
        UI_Setup(layout)
        print(Back.RED + 'Game unknown! Please check to make sure everything is downloaded correctly.')
        exit_app()

    # Check if user wants to install to a different location
    if found == False:
        layout = [[pg.Text(f'{GAME} not found! Where is {GAME} installed?')],
                [pg.InputText(key='path'), pg.FolderBrowse()],
                [pg.Button('OK')]]
        PATH = get_path(PATH, layout)
    else:
        layout = [[pg.Text(f'{GAME} found!')],
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
                    f'Where is {GAME}? ')],
                    [pg.InputText(key='path'), pg.FolderBrowse()],
                    [pg.Button('OK')]]
                PATH = get_path(PATH, layout)

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
                return temp_PATH
                window.close()
                break
            else:
                window.close()
                window = pg.Window('ModDude', error_layout)
    return temp_PATH


def back_up_old():
    global PATH
    global GAME
    if GAME == 'Minecraft':
        if os.path.exists(f'{PATH}\\mods'):
            # Ask user if they want to back up old mods
            print(Fore.YELLOW + 'Would you like to back up your old mods? (y/n)')
            layout = [[pg.Text('Would you like to back up your old mods?')],
                    [pg.Button('Yes'), pg.Button('No')]]
            window = pg.Window('ModDude', layout)
            while True:
                event, values = window.read()
                if event in (None, 'Exit'):
                    exit_app()
                elif event == 'Yes':
                    # Create backup folder
                    if not os.path.exists(f'{PATH}\\mods\\backup'):
                        os.mkdir(f'{PATH}\\mods\\backup')
                    # Move old mods to backup folder
                    for file in os.listdir(f'{PATH}\\mods'):
                        if file.endswith('.jar'):
                            shutil.move(f'{PATH}\\mods\\{file}',
                                        f'{PATH}\\mods\\backup\\{file}')
                    print(Fore.GREEN + 'Old mods backed up!')

                    # Backup Minecraft mods to new folder with date
                    current_date = datetime.datetime.now()
                    current_date = current_date.strftime("%m-%d-%Y_%H-%M-%S")
                    print(Fore.GREEN + f'Backing up old mods to ' + Fore.MAGENTA +
                        f'mods_old_{current_date}' + Fore.GREEN + '...')
                    os.rename(f'{PATH}\\mods', f'{PATH}\\mods_old_{current_date}')
                    print(Fore.GREEN + 'Backup Complete!')
                    window.close()
                    break
                elif event == 'No':
                    try:
                        shutil.rmtree(f'{PATH}\\mods')
                        print(Fore.GREEN + 'Old mods folder removed!')
                    except OSError as e:
                        ERROR_UI('Error', f'Error: {e.filename} - {e.strerror}!', FATAL=True)
                    window.close()
                    return
        else:
            print(Fore.GREEN + 'No existing mods found.')
    else:
        ERROR_UI('Error', 'Game unknown! Please check to make sure everything is downloaded correctly.', FATAL=True)

    layout = [[pg.Text('Mods backed up!')],
              [pg.Button('OK!')]]
    window = pg.Window('ModDude', layout)
    while True:
        event, values = window.read()
        if event in (None, 'Exit'):
            exit_app()
        elif event == 'OK!':
            window.close()
            break

def copy_pack():
    global PACK_NAME
    global CURRENT_VERSION
    global PATH
    global GAME
    done = False
    copied = 0
    MAX_COPY = 0
    if GAME == 'Minecraft':
        # Find number of files to copy
        for root, dirs, files in os.walk(f'{BASE_DIR}\\Downloads\\{PACK_NAME}'):
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
            for folder in os.listdir(f'{BASE_DIR}\\Downloads\\{PACK_NAME}'): # Make all directories in pack if missing
                if os.path.isdir(f'{BASE_DIR}\\Downloads\\{PACK_NAME}\\{folder}'):
                    if not os.path.exists(f'{PATH}\\{folder}'):
                        os.mkdir(f'{PATH}\\{folder}')
                        print(Fore.GREEN + f'Created {folder} folder.')

            for folder in os.listdir(f'{BASE_DIR}\\Downloads\\{PACK_NAME}'):
                # Check if it's a folder
                if os.path.isdir(f'{BASE_DIR}\\Downloads\\{PACK_NAME}\\{folder}'):
                    print(Fore.GREEN + f'Copying {folder} folder...')
                    for file in os.listdir(f'{BASE_DIR}\\Downloads\\{PACK_NAME}\\{folder}'):
                        shutil.copy(f'{BASE_DIR}\\Downloads\\{PACK_NAME}\\{folder}\\{file}', f'{PATH}\\{folder}')
                        copied += 1
                        progress_bar.UpdateBar(copied / MAX_COPY * 100)
                    print(Fore.MAGENTA + f'\tInstalled {copied} files to {folder} folder.\n')
                    copied = 0
            done = True
        window.close()
    else:
        ERROR_UI('Error', 'Game unknown! Please check to make sure everything is downloaded correctly.', FATAL=True)

def unzip_pack():
    global PACK_NAME
    global CURRENT_VERSION
    global PATH
    print('Unzipping pack...')
    with zipfile.ZipFile(f'{PACK_NAME}_v{CURRENT_VERSION}.zip', 'r') as zip_ref:
        zip_ref.extractall(f'{PATH}\\')
    print('Pack unzipped!')


def run_modloader_installer():
    global BASE_DIR
    global MOD_LOADER
    found = False
    # Ask user if they want to install mod loader
    print(Fore.YELLOW + f'Would you like to install {MOD_LOADER}? ' + Fore.CYAN +
          '(Recommended Unless You Are Reinstalling Pack)' + Fore.YELLOW + ' (y/n)')
    layout = [[pg.Text(f'Would you like to install {MOD_LOADER} v{MOD_LOADER_VERSION}?')],
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
    [pg.Text(f'Please close {MOD_LOADER} when it says "Done"')],
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
    if MOD_LOADER == 'Forge':
        for file in os.listdir(f'{BASE_DIR}\\Downloads'):
            if file.startswith('forge-'):
                found = True
                print(Fore.GREEN + 'Mod loader already installed!')
                break
        if not found:
            print(Fore.GREEN + 'Downloading mod loader...')
            # Download mod loader
            try:
                urllib.request.urlretrieve(f'{FORGE_URL}', f'{BASE_DIR}\\Downloads\\forge-{FORGE_VERSION}-installer.jar')
            except urllib.error.URLError as e:
                ERROR_UI('Error', f'Error: {e}', FATAL=True)
            print(Fore.GREEN + 'Mod loader downloaded!')

            # Run mod loader installer
            print(Fore.GREEN + 'Running mod loader installer...')
            os.system(f'java -jar {BASE_DIR}\\Downloads\\forge-{FORGE_VERSION}-installer.jar')
            print(Fore.GREEN + 'Mod loader installed!')
        else:
            ERROR_UI('Error', 'Mod loader unknown! Please check to make sure everything is downloaded correctly.', FATAL=True)
    else:
        # Run mod loader installer executable
        print(Fore.GREEN + f'Running {MOD_LOADER} installer...')
        for file in os.listdir(f'{BASE_DIR}\\Downloads\\{PACK_NAME}'):
            if file.endswith('.exe') or file.endswith('.jar'):
                print(Fore.GREEN + f'{MOD_LOADER} installer found!')
                print(Back.MAGENTA + f'Please install {MOD_LOADER} {MOD_LOADER_VERSION} to the game folder.\n')
                if file.endswith('.exe'):
                    subprocess.check_call(
                        [f'{BASE_DIR}\\Downloads\\{PACK_NAME}\\{file}'])
                elif file.endswith('.jar'):
                    subprocess.call(['java', '-jar', f'{BASE_DIR}\\Downloads\\{PACK_NAME}\\{file}'])
                else:
                    print(Back.RED + 'Mod loader unable to run!')
                    print(Back.RED + 'Please install manually.')
                found = True
        if found == False:
            ERROR_UI('Error', f'Unable to find {MOD_LOADER} installer!', FATAL=True)


def check_install_integrity():
    global PATH
    global BASE_DIR
    global GAME
    passed_files = 0
    failed_files = 0
    # Ask user if they want to check install integrity
    print(Fore.YELLOW + 'Would you like to check install integrity? (y/n)')
    layout = [[pg.Text('Would you like to check install integrity?')],
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
    
    print(Fore.CYAN + '\nChecking install integrity...')
    if GAME == 'Minecraft':
        # Check if mods folder exists
        for folder in os.listdir(f'{BASE_DIR}\\Downloads\\{PACK_NAME}'):
            if os.path.exists(f'{PATH}\\{folder}'):
                # Check if all files are in folder if it's a folder
                if os.path.isdir(f'{BASE_DIR}\\Downloads\\{PACK_NAME}\\{folder}'):
                    print(Fore.GREEN + f'\t{folder} folder found!')
                    passed_files += 1
                    for file in os.listdir(f'{BASE_DIR}\\Downloads\\{PACK_NAME}\\{folder}'):
                        if os.path.exists(f'{PATH}\\{folder}\\{file}'):
                            passed_files += 1
                        else:
                            print(Back.RED + f'\t\t{file} not found!')
                            failed_files += 1
                else:
                    print(Back.RED + f'\t{folder} folder not found!')
                    failed_files += 1
        percent_passed = int(passed_files / (passed_files + failed_files)) * 100
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
                

def exit_app():
    # print(Fore.GREEN + 'Press Enter to exit...')
    # Wait for user to close with enter key
    # input()
    try:
        sys.exit()
    except SystemExit:
        os._exit(0)


def UI_Setup(layout):
    # Variables
    global CLOSE_APP
    CLOSE_APP = False
    # Set Theme
    pg.theme('DarkPurple1')
    # Create Windows
    window = pg.Window(f"ModDude!", layout)
    # Event Loop
    while True:
        event, values = window.read()
        if event == pg.WIN_CLOSED or CLOSE_APP == True:
            exit_app()
        if event == "Start!" or event == "Ok":
            window.close()
            break
    # Close Windows


def ERROR_UI(ERROR_NAME, ERROR_MESSAGE, FATAL):
    # Set Theme
    pg.theme('DarkPurple1')
    # Create Windows
    layout = [[pg.Text(f"ERROR: {ERROR_NAME}")],
                [pg.Text(f"{ERROR_MESSAGE}")],
                [pg.Text("")],
                [pg.Text("Additional Support:")],
                [pg.Text(f"Please check to make sure everything is downloaded correctly.")],
                [pg.Text(f"Please check to make sure you have the latest version of ModDude.")],
                [pg.Text(f"If you are still having issues, please contact me on Discord.")],
                [pg.Text(f"Discord: Geoffery10#6969")],
                [pg.Button("Ok")]]
    window = pg.Window(f"ModDude!", layout)
    # Event Loop
    while True:
        event, values = window.read()
        if event == pg.WIN_CLOSED:
            if FATAL == True:
                exit_app()
        if event == "Ok":
            window.close()
            if FATAL == True:
                exit_app()
    # Close Windows

    

if __name__ == '__main__':
    # Load Initial Variables
    colorama.init(autoreset=True)
    pg.theme('DarkPurple1')
    CURRENT_VERSION = '1.0.5'
    URL = 'https://mcweb.geoffery10.com/mods.json'
    SUPPORTED_GAMES = ['Minecraft']

    # Print Developer Info
    print_dev_info()

    # Open UI
    layout = [
        [pg.Text("Welcome to ModDude!")],
        [pg.Text(" ")],
        [pg.Text(
            "This program was developed by Geoffery10 to help you install mods for your games.")],
        [pg.Text("It is currently in beta, so please report any bugs to me on Discord.")],
        [pg.Text("Discord: Geoffery10#6969")],
        [pg.Text(" ")],
        [pg.Text("Current Version: " + CURRENT_VERSION)],
        [pg.Button("Ok", key="Ok")]]
    UI_Setup(layout)

    # Load Pack Info
    get_json()

    '''
    if page == 2:
        try:
            print_title()
        except:
            print(Back.RED + 'Unable to print title! Please check to make sure everything is downloaded correctly and you are connected to the internet.')
    '''

    # Download Pack
    download_pack()

    # Check Where to Install
    check_game_install_location()

    back_up_old()

    # Copy Pack Into Game
    copy_pack()
    if GAME == 'Minecraft':
        if not MOD_LOADER == '':
            run_modloader_installer()

    
    # Check Install Integrity
    check_install_integrity()

    
    # Check if user wants to delete temporary files
    print(Fore.GREEN + 'Deleting temporary files...')
    try:
        shutil.rmtree(f'{BASE_DIR}\\Downloads\\{PACK_NAME}')
        print(Fore.GREEN + 'Temporary files deleted!')
    except:
        print(Back.RED + 'Temporary failed files to deleted!')

    
    CLOSE_APP = True
    layout = [
        [pg.Text("ModDude has finished installing your modpack!")],
        [pg.Text("Thank you for using ModDude!")],
        [pg.Text("Please contact me on Discord if you have any issues.")],
        [pg.Text("Discord: Geoffery10#6969")],
        [pg.Button("Ok", key="Ok")]]
    window = pg.Window(f"ModDude!", layout)
    while True:
        event, values = window.read()
        if event == pg.WIN_CLOSED:
            exit_app()
        if event == "Ok":
            window.close()
            exit_app()
    # Wait for user to close with enter key
    # input()

