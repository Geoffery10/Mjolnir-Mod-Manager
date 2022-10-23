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
from PIL import ImageTk, Image

# Custom Functions
import online
from ui_menus import exit_app, UI_Setup
import pack
from file_manager import backup_old, delete_temp_files


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
medium_purple = '#813C98'
light_purple = '#995aae'

# PAGES 
# 0 = Main Menu
# 1 = Modpack Menu
# 2 = Downloading 


def new_app(title='ModDude!', width=1280, height=720, resizable=False, icon=f'{BASE_DIR}\\ModDude_Icon.ico'):
    global dark_purple
    global light_purple
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

def new_frame(app):
    # Main Frame
    main_frame = tk.Frame(app, bg=dark_purple)
    main_frame.pack(fill='both', expand=True, padx=28, pady=28)
    return main_frame
    

# Main Menu
def main_menu(app, games):
    # Create main menu
    app.title(f'ModDude!')
    main_frame = new_frame(app)
    # Colors
    global dark_purple
    global light_purple
    # FONTS
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
        game_button = customtkinter.CTkButton(game_list_frame, text='', image=game_image, fg_color=light_purple,
                                              border_width=0, bg_color=light_purple, hover=False, command=lambda game=game: game_button(game))
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


    def game_button(game):
        global PACK
        global GAMES_URL
        
        main_frame.destroy()
        game_data = ''
        for temp_game in games:
            if temp_game['Name'] == game:
                game = temp_game
                break
        modpack_menu(games, game, app)
            

    def open_website(url):
        # Open github in browser
        webbrowser.open(url, new=2)

# Modpack Menu


def modpack_menu(games, game, app):
    # Create modpack menu
    app.title(f'ModDude! - {game["Name"]}')
    main_frame = new_frame(app)
    # Colors
    global dark_purple
    global light_purple
    global medium_purple
    # FONTS
    global FONTS

    # Modpack Menu
    # Page Breakdown:
    # Two Columns

    ## Left Column (Width: 506)
    ## Logo (Small)
    ## Select Packs
    ## Pack info
    ### Select Packs
    ### Download Size
    ### Total Mods 
    ## Extra Options
    ### Backup Old Mods (Checkbox)
    ### Delete Old Mods (Checkbox)
    ## Install Selected Packs
    ## Back Button

    left_frame = tk.Frame(main_frame, bg=dark_purple)
    left_frame.place(x=0, y=0, width=560, height=730)

    # Logo (Small)
    logo = tk.PhotoImage(file=f'{BASE_DIR}\\logo_small.png')
    logo_button = customtkinter.CTkButton(left_frame, text='', fg_color=dark_purple, border_width=0, image=logo, bg_color=dark_purple, hover=False)
    logo_button.place(x=0, y=10, width=560, height=98)

    # Select Packs
    select_packs = tk.Label(left_frame, text='Please Select Packs to Install', bg=dark_purple, fg='white', font=(FONTS[3], 20))
    select_packs.place(x=0, y=98, width=560, height=100)

    # Pack Info
    pack_info_frame = tk.Frame(left_frame, bg=medium_purple)
    pack_info_frame.place(x=20, y=170, width=520, height=180)
    pack_info_background_image = tk.PhotoImage(file=f'{BASE_DIR}\\images\\ui\\info_window_01.png')
    pack_info_background = tk.Label(
        pack_info_frame, image=pack_info_background_image, bg=dark_purple)
    pack_info_background.place(x=0, y=0, width=520, height=180)
    pack_info_background.image = pack_info_background_image

    selected_packs = tk.Label(pack_info_frame, text='Selected Packs: 0',
                              bg=medium_purple, fg='white', font=(FONTS[3], 20))
    selected_packs.pack(side='top', padx=0, pady=12)
    download_size = tk.Label(pack_info_frame, text='Download Size: 0 MB',
                             bg=medium_purple, fg='white', font=(FONTS[3], 20))
    download_size.pack(side='top', padx=0, pady=12)
    total_mods = tk.Label(pack_info_frame, text='Total Mods: 0',
                          bg=medium_purple, fg='white', font=(FONTS[3], 20))
    total_mods.pack(side='top', padx=0, pady=12)

    # Extra Options
    extra_options_frame = tk.Frame(left_frame, bg=medium_purple)
    extra_options_frame.place(x=20, y=368, width=520, height=120)
    extra_options_background_image = tk.PhotoImage(file=f'{BASE_DIR}\\images\\ui\\info_window_02.png')
    extra_options_background = tk.Label(
        extra_options_frame, image=extra_options_background_image, bg=dark_purple)
    extra_options_background.place(x=0, y=0, width=520, height=120)
    extra_options_background.image = extra_options_background_image
    # Options
    # TODO: IMPROVE CHECKBOXES
    backup_old_mods = tk.IntVar()
    backup_old_mods = tk.Checkbutton(extra_options_frame, text='Backup Old Mods', bg=medium_purple, fg='white', font=(
        FONTS[3], 20), selectcolor=medium_purple, activebackground=medium_purple, activeforeground='white')
    backup_old_mods.pack(side='top', padx=0, pady=10)
    delete_old_mods = tk.IntVar()
    delete_old_mods = tk.Checkbutton(extra_options_frame, text='Delete Old Mods', bg=medium_purple, fg='white', font=(
        FONTS[3], 20), selectcolor=medium_purple, activebackground=medium_purple, activeforeground='white')
    delete_old_mods.pack(side='top', padx=0, pady=10)

    # Install Selected Packs
    install_selected_packs = customtkinter.CTkButton(left_frame, text='Install Selected Packs', text_font=(
        FONTS[3], 20), fg_color=medium_purple, bg_color=dark_purple, hover=False, command=lambda: install_selected_packs_button())
    install_selected_packs.place(x=79, y=510, width=393, height=80)

    # Back Button
    back_button = customtkinter.CTkButton(left_frame, text='Back', text_font=(
        FONTS[3], 15), fg_color=medium_purple, bg_color=dark_purple, hover=False, command=lambda: back())
    back_button.place(x=12, y=610, width=80, height=40)
    

    ## Right Column (Width 667)
    ## Packs List (Scrollable)
    ### pack_frame
    #### Pack Image
    #### Pack Name
    #### Pack Description
    #### Pack Size
    #### Pack Mods
    #### Pack Checkbox

    right_frame = tk.Frame(main_frame, bg=light_purple)
    right_frame.place(x=560, y=0, width=664, height=724)

    # Packs List (Pages)
    ## Get Packs from API
    packs = online.get_packs_list(game['Mod URL'])
    
    images = []

    # Download first 4 pack images (or how however many are in the pack) into the images\packs folder using the pack name as the file name
    for pack in packs:
        if len(images) < 4:
            image_valid = online.get_image(pack['BANNER_URL'], f'{BASE_DIR}\\images\\packs\\{pack["PACK_NAME"]}.png')
            if image_valid:
                images.append(f'{BASE_DIR}\\images\\packs\\{pack["PACK_NAME"]}.png')
            else:
                images.append(f'{BASE_DIR}\\images\\packs\\default.png')
                print(f'Failed to download image for {pack["PACK_NAME"]}')
        else:
            break

    print(images)

    # Initialize frames
    PACK_HEIGHT = 200

    # Pack Frame 1
    pack_frame_1 = tk.Frame(right_frame, bg=light_purple)
    pack_frame_1.place(x=0, y=0, width=664, height=PACK_HEIGHT)
    pack_checkbox = tk.Checkbutton(
        pack_frame_1, text='', bg=light_purple, fg='white')
    pack_checkbox.pack(side='left', padx=10, pady=10)

    image1 = Image.open(images[0])
    image1 = image1.resize(
        (100, 100), Image.Resampling.LANCZOS)
    image1 = ImageTk.PhotoImage(image1)
    pack_image_label = tk.Label(pack_frame_1, image=image1, bg=light_purple)
    pack_image_label.pack(side='left', padx=10, pady=10)
    pack_image_label.image = image1

    pack_details_frame = tk.Frame(pack_frame_1, bg=light_purple)
    pack_details_frame.pack(side='left', padx=10, pady=10)
    pack_name = tk.Label(pack_details_frame, text=packs[0]['PACK_NAME'], bg=light_purple, fg='white', font=(FONTS[3], 20))
    pack_name.pack(side='top', padx=10, pady=10)
    pack_description = tk.Label(
        pack_details_frame, text=packs[0]['PACK_DESCRIPTION'], bg=light_purple, fg='white', font=(FONTS[3], 10), wraplength=400, justify='left')
    pack_description.pack(side='top', padx=0, pady=10)
    if packs[0]['PACK_SIZE'] >= 1000:
        pack_size = tk.Label(pack_details_frame, text=f'{round(packs[0]["PACK_SIZE"]/1000, 1)} GB', bg=light_purple, fg='white')
    else:
        pack_size = tk.Label(pack_details_frame, text=f'{round(packs[0]["PACK_SIZE"], 1)} MB', bg=light_purple, fg='white')
    pack_size.pack(side='left', padx=10, pady=10)
    pack_mods = tk.Label(
        pack_details_frame, text=f'Mods: {len(packs[0]["MODS"])}', bg=light_purple, fg='white')
    pack_mods.pack(side='right', padx=10, pady=10)

    # Pack Frame 2
    pack_frame_2 = tk.Frame(right_frame, bg=light_purple)
    pack_frame_2.place(x=0, y=PACK_HEIGHT, width=664, height=PACK_HEIGHT)
    pack_checkbox = tk.Checkbutton(
        pack_frame_2, text='', bg=light_purple, fg='white')
    pack_checkbox.pack(side='left', padx=10, pady=10)

    image2 = Image.open(images[1])
    image2 = image2.resize(
        (100, 100), Image.Resampling.LANCZOS)
    image2 = ImageTk.PhotoImage(image2)
    pack_image_label = tk.Label(pack_frame_2, image=image2, bg=light_purple)
    pack_image_label.pack(side='left', padx=10, pady=10)
    pack_image_label.image = image2

    pack_details_frame = tk.Frame(pack_frame_2, bg=light_purple)
    pack_details_frame.pack(side='left', padx=10, pady=10)
    pack_name = tk.Label(
        pack_details_frame, text=packs[1]['PACK_NAME'], bg=light_purple, fg='white', font=(FONTS[3], 20))
    pack_name.pack(side='top', padx=10, pady=10)
    pack_description = tk.Label(
        pack_details_frame, text=packs[1]['PACK_DESCRIPTION'], bg=light_purple, fg='white', font=(FONTS[3], 10), wraplength=400, justify='left')
    pack_description.pack(side='top', padx=0, pady=10)
    if packs[1]['PACK_SIZE'] >= 1000:
        pack_size = tk.Label(
            pack_details_frame, text=f'{round(packs[1]["PACK_SIZE"]/1000, 1)} GB', bg=light_purple, fg='white')
    else:
        pack_size = tk.Label(
            pack_details_frame, text=f'{round(packs[1]["PACK_SIZE"], 1)} MB', bg=light_purple, fg='white')
    pack_size.pack(side='left', padx=10, pady=10)
    pack_mods = tk.Label(
        pack_details_frame, text=f'Mods: {len(packs[1]["MODS"])}', bg=light_purple, fg='white')
    pack_mods.pack(side='right', padx=10, pady=10)
    
    



    # Functions
    def back():
        # Return to main menu
        main_frame.destroy()
        main_menu(app=app, games=games)

    def install_selected_packs_button():
        # Install selected packs
        pass

    


    

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
    except Exception as e:
        print(f"Failed to load fonts")
        FONTS = ['Arial', 'Arial', 'Arial', 'Arial']

    app = new_app()
    games = online.get_games_list(GAMES_URL)
    main_menu(app, games)
    app.mainloop()
    exit_app()

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

