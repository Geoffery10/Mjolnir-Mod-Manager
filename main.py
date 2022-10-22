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


# PAGES 
# 0 = Main Menu
# 1 = Modpack Menu
# 2 = Downloading 

# Main Menu
def main_menu():
    customtkinter.set_appearance_mode("System")
    customtkinter.set_default_color_theme("blue")
    app = customtkinter.CTk()
    # Aspect Ratio is 16:9
    app.geometry('1280x720')
    app.title('ModDude!')
    app.iconbitmap(f'{BASE_DIR}\\icon.ico')
    app.resizable(False, False)
    app.configure(bg='#380070')

    transparent = '#00000000'
    dark_purple = '#5b0079'

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
    logo_button = customtkinter.CTkButton(app, text='', fg_color=dark_purple, border_width=0, bg_color=dark_purple, hover=False, image=logo, command=lambda: webbrowser.open(
        'https://www.geoffery10.com/games.html', new=2))
    logo_button.place(x=313, y=47)


    def button_function():
        print("button pressed")

    def open_github():
        # Open github in browser
        webbrowser.open('https://www.geoffery10.com/games.html', new=2)
        

    # Use CTkButton instead of tkinter Button
    button = customtkinter.CTkButton(
        master=app, text="CTkButton", command=button_function)
    button.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)

    app.mainloop()

    

if __name__ == '__main__':
    # Load Initial Variables
    colorama.init(autoreset=True)
    pg.theme('DarkPurple1')
    pg.isAnimated = True
    CURRENT_VERSION = '1.1.1'
    URL = 'https://www.geoffery10.com/mods.json'
    GAMES_URL = 'https://www.geoffery10.com/games.json'
    SUPPORTED_GAMES = ['Minecraft', 'Bonelab']


    main_menu()



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

