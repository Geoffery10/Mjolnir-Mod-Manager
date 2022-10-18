# This installs minecraft mods

import file_manager


def minecraft(modpack, BASE_DIR, APPDATA_PATH, FILES):
    # Check Where to Install
    PATH = file_manager.check_game_install_location(modpack, APPDATA_PATH)

    # Backup Files
    file_manager.back_up_old(modpack, (f"{PATH}\\mods"))
    file_manager.back_up_old(modpack, (f"{PATH}\\config"))
    file_manager.back_up_old(modpack, (f"{PATH}\\shaderpacks"))

    # Copy Pack Into Game
    file_manager.copy_pack(modpack, PATH, BASE_DIR)
    if not modpack.mod_loader == '':
        # Check if Mod Loader is Installed
        if not file_manager.check_launcher_profiles(modpack, PATH):
            file_manager.run_mod_loader_installer(modpack, BASE_DIR)

    # Check if Profile Has Enough RAM
    # TODO: Add RAM Check
    # This has no error handling, so it will crash if the java arguments are not found.
    # Saving also doesn't work it seems.
    # * file_manager.check_ram(modpack, PATH)

    # Check Install Integrity
    file_manager.check_install_integrity(modpack, PATH, BASE_DIR)

    return True
