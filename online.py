# This Python File Handles the Online Functionality of ModDude!
# Path: online.py

# Import Modules
from colorama import Fore, Back, Style
import PySimpleGUI as pg
import requests
import os
import shutil
from ui_menus import ERROR_UI, exit_app
from packaging import version
from pack import Pack
import zipfile
import base64


def get_json(CURRENT_VERSION, URL):
    if not URL == '':
        print(Fore.GREEN + 'Getting Packs from Internet...')
        response = requests.get(URL)
        # Check if response is valid
        if response.status_code == 200:
            data = response.json()
            print(Fore.GREEN + f'Packs v{data["CURRENT_VERSION"]} received!')

            # Check if packs are up to date
            if version.parse(CURRENT_VERSION) < version.parse(data['CURRENT_VERSION']):
                ERROR_UI(
                    'Out of Date', 'ModDude! is out of date! Please update the installer.', FATAL=True)

            packs = []
            for pack in data['PACKS']:
                packs.append(pack)
            modpack = select_pack(packs)
        else:
            ERROR_UI(
                'Error', 'Error getting packs from internet! Please check your internet connection and try again!', FATAL=True)
    else:
        ERROR_UI(
            'Error', 'No URL specified! Please contact the developer!', FATAL=True)

    return modpack


def select_pack(packs):
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

    modpack = Pack()
    # Find pack by friendly name
    print(Fore.GREEN + 'Finding pack...')
    for pack in packs:
        pack_name = f"{pack['PACK_NAME']} v{pack['PACK_VERSION']} - {pack['GAME']} v{pack['GAME_VERSION']}"
        if pack_name == PACK_NAME:
            print(Fore.GREEN + 'Pack found!')
            selected_pack = pack
            modpack.game = selected_pack['GAME']
            modpack.pack_name = selected_pack['PACK_NAME']
            modpack.game_version = selected_pack['GAME_VERSION']
            modpack.mod_loader = selected_pack['MOD_LOADER']
            modpack.mod_loader_version = selected_pack['MOD_LOADER_VERSION']
            modpack.pack_version = selected_pack['PACK_VERSION']
            modpack.pack_urls = selected_pack['PACK_URLS']
            modpack.mods = selected_pack['MODS']
            modpack.banner_url = selected_pack['BANNER_URL']
            window.close()
            return modpack


def download_pack(modpack, BASE_DIR, FILES):
    extra_steps = 2
    progress = 0
    
    layout = [
        [pg.Text('Start Downloading Mods... This may take a while!')],
        [pg.Text('Program may appear frozen, please wait...')],
        [pg.Text(f'Pack Files to Download: {len(modpack.pack_urls)}')]]
    if len(modpack.mods) > 0:
        layout.append([pg.Text(f'Mods to Download: {len(modpack.mods)}')])
    layout.append([pg.ProgressBar(100, orientation='h', size=(
        20, 20), key='progressbar')])
    layout.append([pg.Button('Start Download')])
    window = pg.Window('ModDude', layout)
    progress_bar = window['progressbar']
    # Get Step Size for Progress Bar
    step_size = int(100 / (len(modpack.pack_urls) + extra_steps))

    while True:
        window.Refresh()
        event, values = window.read(timeout=800)
        if event in (None, 'Exit'):
            exit_app()
        elif event == 'Start Download':
            progress += step_size
            progress_bar.UpdateBar(progress)
            # Initialize download folder
            if not os.path.exists(f'{BASE_DIR}\\Downloads'):
                os.mkdir(f'{BASE_DIR}\\Downloads')
            if not os.path.exists(f'{BASE_DIR}\\Downloads\\{modpack.pack_name}'):
                os.mkdir(f'{BASE_DIR}\\Downloads\\{modpack.pack_name}')
            else:
                # Delete Anything in the Folder
                try:
                    shutil.rmtree(
                        f'{BASE_DIR}\\Downloads\\{modpack.pack_name}')
                    os.mkdir(f'{BASE_DIR}\\Downloads\\{modpack.pack_name}')
                except OSError as e:
                    ERROR_UI(
                        'Error', 'Error deleting old files! Please close any open files and try again!', FATAL=True)
            progress += step_size
            progress_bar.UpdateBar(progress)

            # Download each file in the pack
            for file in modpack.pack_urls:
                # Split the file name from the URL to get the file name
                file_name = file.split('/')[-1]
                FILES.append(file_name)
                print(Fore.GREEN + f'Downloading {file_name}...')

                if file_name.endswith('.zip'):
                    # Download the file
                    r = requests.get(file, allow_redirects=True)
                    # Write the file to the downloads folder
                    if r.status_code == 200:
                        open(f'{BASE_DIR}\\Downloads\\{modpack.pack_name}\\{file_name}',
                             'wb').write(r.content)
                        print(Fore.GREEN + f'{file_name} downloaded!')
                        # Unzip the file
                        with zipfile.ZipFile(f'{BASE_DIR}\\Downloads\\{modpack.pack_name}\\{file_name}', 'r') as zip_ref:
                            zip_ref.extractall(
                                f'{BASE_DIR}\\Downloads\\{modpack.pack_name}')
                        print(Fore.GREEN + f'{file_name} unpacked!')
                        # Delete Zip File
                        os.remove(
                            f'{BASE_DIR}\\Downloads\\{modpack.pack_name}\\{file_name}')
                    else:
                        ERROR_UI(
                            'Error', f'Error downloading {file_name}! Please try again later!', FATAL=True)
                else:
                    # Download the file
                    r = requests.get(file, allow_redirects=True)
                    # Write the file to the downloads folder
                    if r.status_code == 200:
                        open(f'{BASE_DIR}\\Downloads\\{modpack.pack_name}\\{file_name}',
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
