# This Python File Runs Independently of the Main Program and Updates the Program
# Path: auto-update.py

# Import Modules
import requests
import os
import PySimpleGUI as pg
from subprocess import Popen


if __name__ == '__main__':
    pg.theme('DarkPurple1')
    # Create Windows
    BASE_DIR = os.path.dirname(os.path.realpath(__file__))
    URL = 'https://mcweb.geoffery10.com/mods.json'
    layout = [[pg.Text("Downloading ModDude! Update...")]]
    window = pg.Window("ModDude! Update", layout, finalize=True)
    # This only runs if ModDude! is out of date
    print('ModDude! is out of date! Updating...')
    # Download the latest version of ModDude!
    response = requests.get(URL)
    # Check if response is valid
    if response.status_code == 200:
        data = response.json()
        print(f'Packs v{data["CURRENT_VERSION"]} received!')
        
        # Check for ModDude! download URL
        if len(data['MODDUDE_DOWNLOAD_URL']) > 0:
            # Download ModeDude! files to current directory
            print('Downloading ModDude!...')
            for file in data['MODDUDE_DOWNLOAD_URL']:
                response = requests.get(file)
                if response.status_code == 200:
                    # Download file
                    with open(os.path.join(BASE_DIR, os.path.basename(file)), 'wb') as f:
                        f.write(response.content)
                else:
                    print('Error downloading ModDude! files! Please try again!')
                    exit(1)
        else:
            print('Error downloading ModDude! files! Please try again!')
            exit(1)

    pg.popup("ModDude! has been updated! Please restart the program.")
    window.close()
    # Open the new version of ModDude! 
    # Check for exe or py file
    print('Opening ModDude!...')
    if os.path.isfile(os.path.join(BASE_DIR, 'ModDude.exe')):
        try:
            Popen([os.path.join(BASE_DIR, 'ModDude.exe')])
            exit(0)
        except:
            print('Error opening ModDude! Please try again!')
            exit(1)
    elif os.path.isfile(os.path.join(BASE_DIR, 'main.py')):
        try:
            Popen([os.path.join(BASE_DIR, 'main.py')])
            exit(0)
        except:
            print('Error opening ModDude! Please try again!')
            exit(1)
    exit()
