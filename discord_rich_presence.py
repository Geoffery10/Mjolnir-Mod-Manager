# This code initializes and updates the discord rich presence. It is called every time the user changes menus.
from pypresence import Presence
import time
from client_id import CLIENT_ID
from online import download_pack

start = time.time()


# Initialize the discord rich presence



def rpc_update(RPC, start, large_image="icon", small_image=None, large_text="Mjolnir", details="In the main menu", state="Idle"):
    print("Discord rich presence updated")
    download_url = "https://www.geoffery10.com/games.html"
    if small_image == None:
        RPC.update(large_image=large_image, large_text=large_text, details=details, state=state, start=start, buttons=[{"label": "Download Mjolnir", "url": download_url}])
    else:
        RPC.update(large_image=large_image, small_image=small_image, large_text=large_text, details=details,
                   state=state, start=start, buttons=[{"label": "Download Mjolnir", "url": download_url}])


def connect():
    RPC = Presence(CLIENT_ID)
    RPC.connect()
    print("Discord rich presence connected")
    return RPC

if __name__ == '__main__':
    start = time.time()
    RPC = connect()
    
    rpc_update(RPC, start)
