from tkinter import ttk
import PySimpleGUI as pg
import os
import colorama
from colorama import Fore, Back
from subprocess import Popen
import sys
import requests
import customtkinter
import tkinter as tk
import webbrowser
import pyglet

# Custom Functions
import online
from ui_menus import exit_app, UI_Setup
import pack
from file_manager import delete_temp_files


modpack = pack.Pack()
CURRENT_VERSION = ''
URL = ''
APPDATA_PATH = os.getenv('APPDATA')
PATH = ''
SUPPORTED_GAMES = []
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
PACK = {}
FILES = []
FONTS = []

# Colors
transparent = '#00000000'
dark_purple = '#5b0079'
light_purple = '#995aae'

# PAGES 
# 0 = Main Menu
# 1 = Modpack Menu
# 2 = Downloading 


def new_app(title='ModDude!', width=1280, height=720, resizable=False, icon=f'{BASE_DIR}\\icon.ico'):
    customtkinter.set_appearance_mode("System")
    customtkinter.set_default_color_theme("blue")
    app = customtkinter.CTk()
    # Aspect Ratio is 16:9
    app.geometry(f"{width}x{height}")
    app.title(title)
    app.iconbitmap(icon)
    app.resizable(resizable, resizable)
    app.configure(bg='#380070')
    return app
    



# Main Menu
def main_menu():
    # Create main menu
    app = new_app()
    
    # Colors
    global dark_purple
    global light_purple
    

    global FONTS

    # Main Menu
    # Page Breakdown:
    # Logo
    # App Info
    # Select Game 
    # Games List
    # Footer
    ## Current Version
    ## Github Link
    ## Discord Link

    # Main Frame
    main_frame = tk.Frame(app, bg=dark_purple)
    main_frame.pack(fill='both', expand=True, padx=28, pady=28)
    # Logo (Image Button that links to website)
    # Logo is 655x98
    logo = tk.PhotoImage(file=f'{BASE_DIR}\\logo.png')
    logo_button = customtkinter.CTkButton(app, text='', fg_color=dark_purple, border_width=0, bg_color=dark_purple,
                                          hover=False, image=logo, command=lambda: open_website('https://www.geoffery10.com/games.html'))
    logo_button.place(x=313, y=47)

    # App Info
    app_info = tk.Label(app, text='This program was developed by Geoffery10 to help you install mods for your games.\n This app is currently in beta, so please report any bugs to me on Discord.', bg=dark_purple, fg='white', font=(FONTS[3], 20))
    app_info.place(x=67, y=182, width=1146, height=100)

    # Select Game
    select_game = tk.Label(app, text='Please Select A Game', bg=dark_purple, fg='white', font=(FONTS[3], 30))
    select_game.place(x=67, y=265, width=1146, height=100)

    # Games List
    game_list_frame = tk.Frame(main_frame, bg=light_purple)
    game_list_frame.place(x=0, y=340, width=1280, height=258)

    # Games in List
    global SUPPORTED_GAMES
    for game in SUPPORTED_GAMES:
        game_image = tk.PhotoImage(file=f'{BASE_DIR}\\images\\covers\\{game}.png')
        game_button = customtkinter.CTkButton(game_list_frame, text='', image=game_image, fg_color=light_purple, border_width=0, bg_color=light_purple, hover=False, command=lambda game=game: modpack_menu(game))
        game_button.pack(side='left', padx=20, pady=10)

    # Footer
    footer_frame = tk.Frame(main_frame, bg=dark_purple)
    footer_frame.place(x=0, y=598, width=1223, height=70)
    global CURRENT_VERSION
    current_version = tk.Label(footer_frame, text=f'Current Version: v{CURRENT_VERSION}', bg=dark_purple, fg='white', font=(FONTS[3], 25))
    current_version.pack(side='left', padx=20, pady=0)
    # Links on right side
    github_icon = tk.PhotoImage(file=f'{BASE_DIR}\\images\\github.png')
    github_link = customtkinter.CTkButton(footer_frame, text='', fg_color=dark_purple, image=github_icon, hover=False, command=lambda: open_website('https://github.com/Geoffery10/ModDude'))
    github_link.pack(side='right', padx=0, pady=0)

    discord_icon = tk.PhotoImage(file=f'{BASE_DIR}\\images\\discord.png')
    discord_link = customtkinter.CTkButton(footer_frame, text='', fg_color=dark_purple, image=discord_icon,
                                           hover=False, command=lambda: open_website('https://discordapp.com/users/253710834553847808'))
    discord_link.pack(side='right', padx=0, pady=0)


    def modpack_menu(game):
        global PACK
        global GAMES_URL
        modpack_menu(game)

    def open_website(url):
        # Open github in browser
        webbrowser.open(url, new=2)

    app.mainloop()

# Modpack Menu
def modpack_menu(game, app):
    # Create modpack menu
    app.title(f'ModDude! - {game}')

    # Colors
    global dark_purple
    global light_purple
    


    

if __name__ == '__main__':
    # Load Initial Variables
    colorama.init(autoreset=True)
    pg.theme('DarkPurple1')
    pg.isAnimated = True
    CURRENT_VERSION = '1.1.1'
    URL = 'https://www.geoffery10.com/mods.json'
    GAMES_URL = 'https://www.geoffery10.com/games.json'
    SUPPORTED_GAMES = ['Minecraft', 'Bonelab']

    # Custom Fonts
    try:
        if os.path.exists(f'{BASE_DIR}\\fonts'):
            for file in os.listdir(f'{BASE_DIR}\\fonts'):
                if file.endswith('.ttf'):
                    pyglet.font.add_directory(f'{BASE_DIR}\\fonts')
                    file_name = file.split('.')[0]
                    FONTS.append(file_name)
        print(Fore.GREEN + 'Loaded Custom Fonts')
        print(Fore.GREEN + f'Fonts: {FONTS}')
    except Exception as e:
        print(f"Failed to load fonts")
        FONTS = ['Arial', 'Arial', 'Arial', 'Arial']


    main_menu()

    # Check for Updates or Install Packs
    # Run auto-update.py to download the latest version of ModDude!
    # This will overwrite the current version of ModDude! with the latest version
    # This will close the current instance of ModDude! and open the new one
    # ! This will not work if ModDude! is running from a .exe file
    if online.check_for_updates(CURRENT_VERSION, URL):
        # check for update script
        if os.path.isfile(os.path.join(BASE_DIR, 'auto-update.py')):
            try:
                Popen([os.path.join(BASE_DIR, 'auto-update.py')])
                exit_app()
            except:
                print('Error updating ModDude! Please try again!')
                exit_app()
        else:
            # Download auto-update.py
            print('Downloading auto-update.py...')
            response = requests.get('https://www.geoffery10.com/auto-update.py')
            if response.status_code == 200:
                # Download file
                with open(os.path.join(BASE_DIR, 'auto-update.py'), 'wb') as f:
                    f.write(response.content)
            else:
                print('Error downloading auto-update.py! Please try again!')
                exit_app()
        # Run auto-update.py
        Popen([sys.executable, os.path.join(BASE_DIR, 'auto-update.py')])
        exit_app()
    # Delete auto-update.py
    if os.path.isfile(os.path.join(BASE_DIR, 'auto-update.py')):
        try:
            os.remove(os.path.join(BASE_DIR, 'auto-update.py'))
        except:
            print('Error deleting auto-update.py!')
    
    
    # Load Games
    game = online.get_games(GAMES_URL)


    # Load Pack Info
    modpack = online.get_json(CURRENT_VERSION, game['Mod URL'])


    # Download Pack
    online.download_pack(modpack, BASE_DIR, FILES)

    # Open Core
    if game['Name'] == 'Minecraft':
        # Minecraft
        import core_minecraft
        valid = core_minecraft.minecraft(modpack, BASE_DIR, APPDATA_PATH, FILES)
    elif game['Name'] == 'Bonelab':
        # Bonelab
        import core_bonelab
        valid = core_bonelab.bonelab(modpack, BASE_DIR, APPDATA_PATH, FILES)
    else:
        print('Error: Invalid Game!')
        exit_app()

    # Delete Temp Files
    delete_temp_files(modpack, BASE_DIR)

    # Finished
    if valid:
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
    else:
        layout = [
            [pg.Text("ModDude has encountered an error while installing your modpack!")],
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

