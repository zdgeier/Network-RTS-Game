from Units import *
from Constants import *
from Player import Player
import sys

class RTSGame:
    def __init__(self, do, send):
        self.do = do
        self.send = send

        global player1, player2
        entities = []

        self.basesP1 = []
        self.basesP1.append(Base(WHITE,(100,100,100,100), pygame.image.load("Images/temp.png")))
        self.basesP1.append(Base(WHITE,(100,350,100,100), pygame.image.load("Images/temp.png")))
        self.basesP1.append(Base(WHITE,(100,600,100,100), pygame.image.load("Images/temp.png")))

        self.basesP2 = []
        self.basesP2.append(Base(WHITE,(1200,100,100,100), pygame.image.load("Images/temp.png")))
        self.basesP2.append(Base(WHITE,(1200,350,100,100), pygame.image.load("Images/temp.png")))
        self.basesP2.append(Base(WHITE,(1200,600,100,100), pygame.image.load("Images/temp.png")))
        entities.append(self.basesP1)
        entities.append(self.basesP2)

        paths = []
        paths.append(Box(BROWN,((200,112.5,1000,75)), pygame.image.load("Images/temp.png")))
        paths.append(Box(BROWN,((200,362.5,1000,75)), pygame.image.load("Images/temp.png")))
        paths.append(Box(BROWN,((200,612.5,1000,75)), pygame.image.load("Images/temp.png")))
        entities.append(paths)

        self.units = []
        entities.append(self.units)

        self.buttons = []
        self.buttons.append(Button(WHITE, (300,25), self.spawn_unit,pygame.image.load("Images/Melee_B.png"), "Melee"))
        self.buttons.append(Button(WHITE, (500,25), self.spawn_unit,pygame.image.load("Images/Archer_B.png"), "Ranged"))
        self.buttons.append(Button(WHITE, (700,25), self.spawn_unit,pygame.image.load("Images/Recon_B.png"), "Recon"))
        self.buttons.append(Button(WHITE, (900,25), self.spawn_unit,pygame.image.load("Images/Tank_B.png"), "Tank"))
        entities.append(self.buttons)

        # Performance improvements
        #self.screen = pygame.display.set_mode((1366, 768), (pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF))
        self.screen = pygame.display.set_mode((1366, 768), (pygame.HWSURFACE | pygame.DOUBLEBUF))
        self.screen.set_alpha(None)

        clock = pygame.time.Clock()

        # Main Render Loop
        while True:
            dt = clock.tick(50)

            events = pygame.event.get()
            self.screen.fill((144, 245, 0))  # Green background

            for entity in entities:
                for item in entity:
                    item.drawon(self.screen, dt)

            if not do.empty():
                dict = do.get()
                method = getattr(self, dict['name'])
                method(dict['params'])

            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    self.checkBounds(pos)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()

            self.checkCollision()

            pygame.display.flip()

    # TODO: Remove dependency on base class
    # TODO: ^ Do not spawn enemies based on class
    def spawn_unit(self, unit):
        for base in self.basesP1:
            if base.active:
                coords = base.getcoords()
                if unit == "Melee":
                    cost = MELEECOST
                    unit = Melee(GREY, (coords[0] + coords[2], coords[1] + coords[3]/2 - 25), RIGHT)

                '''
                elif unit == "Ranged":
                    cost = RANGECOST
                    if player.getName() == "player1":
                        unit = Ranged(BLACK, (coords[0] + coords[2], coords[1] + coords[3]/2 - 25), RIGHT, player1)
                    else:
                        unit = Ranged(BLACK, (coords[0] + coords[2] + 975, coords[1] + coords[3] / 2 - 25), LEFT, player2)
                elif unit == "Tank":
                    cost = TANKCOST
                    if player.getName() == "player1":
                        unit = Tank(RED, (coords[0] + coords[2], coords[1] + coords[3]/2 - 25), RIGHT, player1)
                    else:
                        unit = Tank(RED, (coords[0] + coords[2] + 975, coords[1] + coords[3] / 2 - 25), LEFT, player2)
                elif unit == "Recon":
                    cost = RECONCOST
                    if player.getName() == "player1":
                        unit = Recon(BROWN, (coords[0] + coords[2], coords[1] + coords[3]/2 - 25), RIGHT, player1)
                    else:
                        unit = Recon(BROWN, (coords[0] + coords[2] + 975, coords[1] + coords[3] / 2 - 25), LEFT, player2)
                '''
                '''
                if player.getMoney() > cost:
                    player.removeMoney(cost)
                    self.units.append(unit)
                '''
                self.units.append(unit)

    def checkCollision(self):
        for unit in self.units:
            ounits = [u for u in self.units if unit.intersects(u.getpos()) and not unit == u]
            if ounits:  # list is not empty
                for u in ounits:
                    #if u.getPlayer() != unit.getPlayer():
                    self.units.remove(u)
                    self.units.remove(unit)

    def checkBounds(self, pos):
        for base in self.basesP1:
            if base.intersects(pos):
                for b in self.basesP1:
                    b.setUnactive()  # Sets all bases to unactive
                base.setActive()  # Sets the active base to active
                break

        for button in self.buttons:
            if button.intersects(pos):
                button.clicked()
                self.send.put('Spawn Melee') ## rEMOVE
                break

        return