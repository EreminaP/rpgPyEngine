from colorama import init as colorama_init
from colorama import Fore
from threading import Thread

consoleRun = True

class Console:
    def __init__(self):
        colorama_init(autoreset=True)
        #commands = {"createMap":}
    def start(self):
        def thread():
            while True:
                comand = input()
                if comand.split(" ")[0] != "createMap":
                    try:
                        exec(f"{comand}")
                    except Exception as e:
                        print(f"{Fore.RED}{e}")
                else:
                    splited = comand.split(" ")
                    name = splited[1]
                    sizeX = int(splited[2])
                    sizeY = int(splited[3])
                    map[0].create2(name, sizeX, sizeY)
        consoleThread = Thread(target=thread, args=[])
        consoleThread.start()
def console():
    colorama_init(autoreset=True)

    # commands = {"createMap":}

    def th():
        while consoleRun:
            comand = input()

            if comand.split(" ")[0] != "createMap":
                try:
                    exec(f"{comand}")
                except Exception as e:
                    print(f"{Fore.RED}{e}")
            else:
                splited = comand.split(" ")
                name = splited[1]
                sizeX = int(splited[2])
                sizeY = int(splited[3])
                map[0].create2(name, sizeX, sizeY)
    consoleThread = Thread(target=th, args=[])
    consoleThread.start()
def closeConsole():
    global consoleRun
    consoleRun = False
    exit()
    #print("Консоль закрыта !!!")
    #exit()

