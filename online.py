# This Python File Handles the Online Functionality of ModDude!
# Path: online.py

# Import Modules
import time
from colorama import Fore, Back, Style
import PySimpleGUI as pg
import requests
import os
import shutil
from ui_menus import ERROR_UI, exit_app
from packaging import version
from pack import Pack
import zipfile


def check_for_updates(CURRENT_VERSION, URL):
    if not URL == '':
        print(Fore.GREEN + 'Checking for updates...')
        response = requests.get(URL)
        # Check if response is valid
        if response.status_code == 200:
            data = response.json()
            print(Fore.GREEN + f'Packs v{data["CURRENT_VERSION"]} received!')

            # Check if packs are up to date
            if version.parse(CURRENT_VERSION) < version.parse(data['CURRENT_VERSION']):
                print(Fore.GREEN + 'Update found!')
                return True, data['CURRENT_VERSION']
            else:
                print(Fore.GREEN + 'No updates found!')
                return False, data['CURRENT_VERSION']
        else:
            ERROR_UI(
                'Error', 'Error getting packs from internet! Please check your internet connection and try again!', FATAL=True)
    else:
        ERROR_UI(
            'Error', 'No URL specified! Please contact the developer!', FATAL=True)


def get_games(URL):
    if not URL == '':
        print(Fore.GREEN + 'Getting Games from Internet...')
        response = requests.get(URL)
        # Check if response is valid
        if response.status_code == 200:
            data = response.json()
            print(Fore.GREEN + f'Games received!')

            games = []
            for game in data['Games']:
                games.append(game)
            game = select_game(games)
        else:
            ERROR_UI(
                'Error', 'Error getting games from internet! Please check your internet connection and try again!', FATAL=True)
    else:
        ERROR_UI(
            'Error', 'No URL specified! Please contact the developer!', FATAL=True)

    return game


def get_games_list(URL):
    if not URL == '':
        print(Fore.GREEN + 'Getting Games from Internet...')
        response = requests.get(URL)
        # Check if response is valid
        if response.status_code == 200:
            data = response.json()
            print(Fore.GREEN + f'Games received!')

            games = []
            for game in data['Games']:
                games.append(game)
        else:
            ERROR_UI(
                'Error', 'Error getting games from internet! Please check your internet connection and try again!', FATAL=True)
    else:
        ERROR_UI(
            'Error', 'No URL specified! Please contact the developer!', FATAL=True)
    return games

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

def get_packs_list(URL):
    if not URL == '':
        print(Fore.GREEN + 'Getting Packs from Internet...')
        response = requests.get(URL)
        # Check if response is valid
        if response.status_code == 200:
            data = response.json()
            print(Fore.GREEN + f'Packs v{data["CURRENT_VERSION"]} received!')
            packs = []
            for pack in data['PACKS']:
                packs.append(pack)
        else:
            ERROR_UI(
                'Error', 'Error getting packs from internet! Please check your internet connection and try again!', FATAL=True)
    else:
        ERROR_UI(
            'Error', 'No URL specified! Please contact the developer!', FATAL=True)

    return packs


def select_game(games):
    print(Fore.YELLOW + 'Which game would you like to mod?')
    layout = [
        [pg.Text(
            'Select a game to mod:')]]
    for i in range(len(games)):  # Alternate between Fore.MAGENTA and Fore.WHITE
        game_name = f"{games[i]['Name']}"
        layout.append([pg.Button(game_name)])
    layout.append([pg.Button('Exit')])
    window = pg.Window('ModDude', layout)
    while True:
        event, values = window.read()
        if event in (None, 'Exit'):
            exit_app()
        else:
            GAME_NAME = event
            print(Fore.GREEN + f'Modding {GAME_NAME}...')
            # Get game info from json using game name
            for i in range(len(games)):
                if games[i]['Name'] == GAME_NAME:
                    game = games[i]
                    break
            window.close()
            return game


def get_image(URL, path):
    if not URL == '':
        response = requests.get(URL, stream=True)
        if response.status_code == 200:
            with open(path, 'wb') as f:
                response.raw.decode_content = True
                shutil.copyfileobj(response.raw, f)
            return True
        else:
            return False

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
            modpack.recommended_ram = selected_pack['RECOMMEND_RAM']
            modpack.mods = selected_pack['MODS']
            modpack.banner_url = selected_pack['BANNER_URL']
            window.close()
            return modpack


def download_pack(modpack, BASE_DIR, FILES, app, bonus_text=None):
    extra_steps = 2
    progress = 0
    count = 1

    # Get Step Size for Progress Bar
    step_size = int(100 / (len(modpack.pack_urls) + extra_steps))

    progress += step_size
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
    app.update()

    # Download each file in the pack
    for file in modpack.pack_urls:
        progress = 0
        # Split the file name from the URL to get the file name
        file_name = file.split('/')[-1]
        FILES.append(file_name)
        print(Fore.GREEN + f'Downloading {file_name}...')
        if bonus_text:
            bonus_text.configure(text=f'{file_name} ({count}/{len(modpack.pack_urls)})')
        count += 1
        # Start async timer to record download speed
        start = time.time()
        app.update()

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
                    app.update()
                print(Fore.GREEN + f'{file_name} unpacked!')
                # Delete Zip File
                os.remove(
                    f'{BASE_DIR}\\Downloads\\{modpack.pack_name}\\{file_name}')
                app.update()
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
                app.update()
                print(Fore.GREEN + f'{file_name} downloaded! Took {time.time() - start} seconds!')
        app.update()
        progress += step_size

    progress += step_size
    print(Fore.MAGENTA + 'All files downloaded!')