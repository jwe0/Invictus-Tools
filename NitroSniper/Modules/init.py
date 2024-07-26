import json, os

class Init:
    def __init__(self) -> None:
        pass

    def config(self):
        if not os.path.exists("Assets/Config.json"):
            token = input("Token: ")
    
            with open("Assets/Config.json", "w") as f:
                json.dump({
                    "Token" : token,
                    "ApiVersion" : "9",
                    "Delay" : 0
                }, f, indent=4)
            