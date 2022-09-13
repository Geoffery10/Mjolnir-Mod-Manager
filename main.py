import PySimpleGUI as pg
import shutil
import os
import colorama
from colorama import Fore, Back

# Custom Functions
import online
from ui_menus import exit_app, ERROR_UI, UI_Setup
import pack
import file_manager

modpack = pack.Pack()
CURRENT_VERSION = ''
URL = ''
APPDATA_PATH = os.getenv('APPDATA')
PATH = ''
SUPPORTED_GAMES = []
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
PACK = {}
FILES = []

    

if __name__ == '__main__':
    # Load Initial Variables
    colorama.init(autoreset=True)
    pg.theme('DarkPurple1')
    pg.isAnimated = True
    CURRENT_VERSION = '1.0.6'
    URL = 'https://mcweb.geoffery10.com/mods.json'
    SUPPORTED_GAMES = ['Minecraft']

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
    modpack = online.get_json(CURRENT_VERSION, URL)


    # Download Pack
    online.download_pack(modpack, BASE_DIR, FILES)

    # Check Where to Install
    PATH = file_manager.check_game_install_location(modpack, APPDATA_PATH, PATH)

    # Backup Files
    file_manager.back_up_old(modpack, (f"{PATH}\\mods"))
    file_manager.back_up_old(modpack, (f"{PATH}\\config"))
    file_manager.back_up_old(modpack, (f"{PATH}\\shaderpacks"))

    # Copy Pack Into Game
    file_manager.copy_pack(modpack, PATH, BASE_DIR)
    if modpack.game == 'Minecraft':
        if not modpack.mod_loader == '':
            file_manager.run_mod_loader_installer(modpack, BASE_DIR)

    
    # Check Install Integrity
    file_manager.check_install_integrity(modpack, PATH, BASE_DIR)

    
    # Delete Temp Files
    file_manager.delete_temp_files(modpack, BASE_DIR, FILES)

    # Finished
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

