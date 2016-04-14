import pygame
import sys
from Menus import GameMenu
from Network import Server
from Network import Client
from _thread import *

class MainMenuManager:
    def __init__(self):
        # Creating the screen
        screen = pygame.display.set_mode((1366,768), 0, 32)

        menu_items = ['Start', 'Connect to Server', 'Start Server', 'Quit']
        funcs = {'Start': self.start_game,
                 'Connect to Server': self.connect_server,
                 'Start Server': self.start_server,
                 'Quit': sys.exit}

        pygame.display.set_caption('Game Menu')
        gm = GameMenu(screen, menu_items, funcs)
        gm.run()

    def start_game(self):
        from Game import RTSGame
        game = RTSGame()

    def start_server(self):
        start_new_thread(Server, ())

    def connect_server(self):
        start_new_thread(Client, ())
        from Game import RTSGame
        game = RTSGame()

if __name__ == '__main__':
    start = MainMenuManager()