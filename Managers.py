import pygame
import sys
import InputBox
import Network as Net
from Menus import GameMenu
from Constants import BLACK
from threading import Thread
from Game import RTSGame
from multiprocessing import queues

class MainMenuManager:
    def __init__(self):
        # Creating the screen
        pygame.init()
        self.screen = pygame.display.set_mode((360,240), 0, 32)

        menu_items = ['Login', 'Quit']
        funcs = {'Login': self.login,
                 'Quit': sys.exit}

        pygame.display.set_caption('Title Menu')
        self.gm = GameMenu(self.screen, menu_items, funcs)
        self.gm.run()

    def login(self):
        self.gm.mainloop = False
        self.screen.fill(BLACK)
        inp = str(InputBox.ask(self.screen, 'Username')) #inp will equal whatever the input is
        writefile = open('UserHistory.txt', 'w')
        writefile.write(inp)
        writefile.close()
        self.main_menu()

    def main_menu(self):
        # Accounts for different screen dimensions
        #disp = pygame.display.Info()
        #self.screen = pygame.display.set_mode((disp.current_w, disp.current_h), pygame.FULLSCREEN)
        self.screen = pygame.display.set_mode((1366, 768), (pygame.HWSURFACE | pygame.DOUBLEBUF))

        # Loops in-game music
        # TODO: Reinitialize music (update track?)
        #pygame.mixer.music.load('Waterflame - Glorious morning.mp3')
        #pygame.mixer.music.play(loops=-1)

        # Creates menu items and commands
        menu_items = ['Start Server', 'Connect to Server', 'Quit']
        funcs = {'Connect to Server': self.start_client,
                 'Start Server': self.start_server,
                 'Quit': sys.exit}

        # Shows and executes main menu
        pygame.display.set_caption('Game Menu')
        self.mm = GameMenu(self.screen, menu_items, funcs)
        self.mm.run()

    def start_server(self):
        send = queues.Queue()
        do = queues.Queue()

        server = Thread(target=Net.Server, args=(do, send))
        server.daemon = True
        server.start()

        # Wait until network has started
        self.screen.fill(BLACK)

        send.get()  # TODO: "Waiting for connection..." screen

        game = RTSGame(do, send)


    def start_client(self):
        send = queues.Queue()
        do = queues.Queue()

        client = Thread(target=Net.Client, args=(do, send))
        client.daemon = True
        client.start()

        # Wait until network has started
        self.screen.fill(BLACK)
        send.get()  # TODO: "Waiting for connection..." screen

        game = RTSGame(do, send)

if __name__ == '__main__':
    start = MainMenuManager()