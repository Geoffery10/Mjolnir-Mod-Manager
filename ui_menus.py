# This Python File Handles the UI Menus of ModDude!
# These are predefined menus that are used throughout the program.

# Import Modules
from colorama import Fore, Back, Style
import PySimpleGUI as pg
import os 
import sys


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
              [pg.Text(
                  f"Please check to make sure you have the latest version of ModDude.")],
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


def exit_app():
    # print(Fore.GREEN + 'Press Enter to exit...')
    # Wait for user to close with enter key
    # input()
    try:
        sys.exit()
    except SystemExit:
        os._exit(0)
