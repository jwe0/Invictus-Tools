import tls_client
from pystyle import *
class General:
    def __init__(self) -> None:
        pass

    def ascii_art(self):
        art = """

██╗███╗   ██╗██╗   ██╗██╗ ██████╗████████╗██╗   ██╗███████╗    ███╗   ██╗███████╗
██║████╗  ██║██║   ██║██║██╔════╝╚══██╔══╝██║   ██║██╔════╝    ████╗  ██║██╔════╝
██║██╔██╗ ██║██║   ██║██║██║        ██║   ██║   ██║███████╗    ██╔██╗ ██║███████╗
██║██║╚██╗██║╚██╗ ██╔╝██║██║        ██║   ██║   ██║╚════██║    ██║╚██╗██║╚════██║
██║██║ ╚████║ ╚████╔╝ ██║╚██████╗   ██║   ╚██████╔╝███████║    ██║ ╚████║███████║
╚═╝╚═╝  ╚═══╝  ╚═══╝  ╚═╝ ╚═════╝   ╚═╝    ╚═════╝ ╚══════╝    ╚═╝  ╚═══╝╚══════╝

"""

        print(Colorate.Vertical(Colors.purple_to_blue, art))

    def token_check(self, token):
        api = "https://discord.com/api/v9/users/@me"
        r = tls_client.Session().get(api, headers={"Authorization": token})
        if r.status_code == 200:
            return r.json().get("username")
        else:
            return False