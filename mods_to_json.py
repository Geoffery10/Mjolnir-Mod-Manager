# this Python File is Not Used in ModDude!
# Print out all mods in folder to list
import os

folder = 'C:\\Users\\powel\\AppData\\Roaming\\.minecraft\\mods'

mods = []
# Get all files in folder
for file in os.listdir(folder):
    # Check if file is a mod
    if file.endswith('.jar'):
        mods.append(file)

# Print out all mods in folder to list
for mod in mods:
    print(f"\"{mod}\", ")