# This Python File Handles the Pack Object of ModDude!
# Path: pack.py

# Import Modules

class Pack:
    url = ""
    pack_name = ""
    pack_description = ""
    pack_version = ""
    game = ""
    game_version = ""
    mod_loader = ""
    mod_loader_version = ""
    pack_urls = []
    recommended_ram = 0
    mods = []
    mods_count = 0
    banner_url = ""
    size = 0 # Size of the pack in MB

    def __init__(self):
        self.url = ""
        self.pack_name = ""
        self.pack_description = ""
        self.pack_version = ""
        self.game = ""
        self.game_version = ""
        self.mod_loader = ""
        self.mod_loader_version = ""
        self.pack_urls = []
        self.recommended_ram = 0
        self.mods = []
        self.mods_count = 0
        self.banner_url = ""
        self.size = 0