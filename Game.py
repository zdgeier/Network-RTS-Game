from Units import *
from Constants import *
from Player import Player
import sys

class RTSGame:
    def __init__(self, do, send):
        self.do = do
        self.send = send

        entities = []

        # Make base entities
        self.my_bases = []
        self.my_bases.append(Base(WHITE, (100, 100, 100, 100), pygame.image.load("Images/temp.png")))
        self.my_bases.append(Base(WHITE, (100, 350, 100, 100), pygame.image.load("Images/temp.png")))
        self.my_bases.append(Base(WHITE, (100, 600, 100, 100), pygame.image.load("Images/temp.png")))
        entities.append(self.my_bases)

        # Make enemy base entities
        self.enemy_bases = []
        self.enemy_bases.append(Base(WHITE, (1200, 100, 100, 100), pygame.image.load("Images/temp.png")))
        self.enemy_bases.append(Base(WHITE, (1200, 350, 100, 100), pygame.image.load("Images/temp.png")))
        self.enemy_bases.append(Base(WHITE, (1200, 600, 100, 100), pygame.image.load("Images/temp.png")))
        entities.append(self.enemy_bases)

        # Make Players - Stores data about each player
        you = Player(self.my_bases, isEnemy=False)
        enemy = Player(self.enemy_bases, isEnemy=True)

        # Make path entities
        self.paths = []
        self.paths.append(Box(BROWN,(200,112.5,1000,75), pygame.image.load("Images/temp.png")))
        self.paths.append(Box(BROWN,(200,362.5,1000,75), pygame.image.load("Images/temp.png")))
        self.paths.append(Box(BROWN,(200,612.5,1000,75), pygame.image.load("Images/temp.png")))
        entities.append(self.paths)

        # Make button entities
        self.buttons = []
        self.buttons.append(Button(WHITE, (300,25), self.spawn_unit,pygame.image.load(MELEE_IMAGE), "Melee"))
        self.buttons.append(Button(WHITE, (500,25), self.spawn_unit,pygame.image.load(ARCHER_IMAGE), "Ranged"))
        self.buttons.append(Button(WHITE, (700,25), self.spawn_unit,pygame.image.load(RECON_IMAGE), "Recon"))
        self.buttons.append(Button(WHITE, (900,25), self.spawn_unit,pygame.image.load(TANK_IMAGE), "Tank"))
        entities.append(self.buttons)

        self.units = []
        self.enemy_units = []
        entities.append(self.units)

        # Performance improvements
        #self.screen = pygame.display.set_mode((1366, 768), (pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF))
        self.screen = pygame.display.set_mode((1366, 768), (pygame.HWSURFACE | pygame.DOUBLEBUF))
        self.screen.set_alpha(None)
        font = pygame.font.Font(None, 36)

        clock = pygame.time.Clock()

        # Main Render Loop
        while True:
            dt = clock.tick(50)

            events = pygame.event.get()
            self.screen.fill((144, 245, 0))  # Green background

            for entity in entities:
                for item in entity:
                    item.drawon(self.screen, dt)

            text = font.render(str(dt), 1, (10, 10, 10))
            self.screen.blit(text, (25,25))

            if not do.empty():
                dict = do.get()
                method = getattr(self, dict['name'])
                method(dict['type'], dict['base'])

            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    self.clicked(pos)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()

            self.checkCollision()

            pygame.display.flip()

    # TODO: Remove dependency on base class
    # TODO: ^ Do not spawn enemies based on class
    def spawn_unit(self, unit):
        i = 0
        for base in self.my_bases:
            if base.active:
                coords = base.getcoords()
                if unit == "Melee":
                    cost = MELEECOST
                    unit = Melee(GREY, (coords[0] + coords[2], coords[1] + coords[3]/2 - 25), RIGHT)
                    self.send.put("{'name': 'spawn_enemy', 'type': 'Melee', 'base': " + str(i) + "}")
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
            i += 1

    def spawn_enemy(self, type, base):
        spawnpoint = self.enemy_bases[base]
        coords = spawnpoint.getcoords()
        if type == "Melee":
            cost = MELEECOST
            unit = Melee(GREY, (coords[0] + coords[2], coords[1] + coords[3] / 2 - 25), LEFT)

        self.enemy_units.append(unit)

    def checkCollision(self):
        for unit in self.units:
            ounits = [u for u in self.units if unit.intersects(u.getpos()) and not unit == u]
            if ounits:  # list is not empty
                for u in ounits:
                    self.units.remove(u)
                    self.units.remove(unit)

    def clicked(self, pos):
        for base in self.my_bases:
            if base.intersects(pos):
                for b in self.my_bases:
                    b.setUnactive()  # Sets all bases to unactive
                base.setActive()  # Sets the active base to active
                break

        for button in self.buttons:
            if button.intersects(pos):
                button.clicked()

                break