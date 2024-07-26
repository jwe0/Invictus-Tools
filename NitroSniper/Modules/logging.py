from colorama import Fore

class Logging:
    def __init__(self):
        pass

    def Success(self, message):
        print("[{red}>{reset}] {message}".format(red=Fore.GREEN, reset=Fore.WHITE, message=message))
    
    def Error(self, message):
        print("[{red}>{reset}] {message}".format(red=Fore.RED, reset=Fore.WHITE, message=message))

    def Info(self, message):
        print("[{red}>{reset}] {message}".format(red=Fore.CYAN, reset=Fore.WHITE, message=message))

    def BasicInput(self, message):
        input("[{red}>{reset}] {message}".format(red=Fore.CYAN, reset=Fore.WHITE, message=message))