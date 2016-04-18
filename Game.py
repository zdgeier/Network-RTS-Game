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
        self.you = Player(self.my_bases, isEnemy=False)
        self.enemy = Player(self.enemy_bases, isEnemy=True)

        # Make path entities
        self.paths = []
        self.paths.append(Box(BROWN,(200,112.5,1000,75), pygame.image.load("Images/temp.png")))
        self.paths.append(Box(BROWN,(200,362.5,1000,75), pygame.image.load("Images/temp.png")))
        self.paths.append(Box(BROWN,(200,612.5,1000,75), pygame.image.load("Images/temp.png")))
        entities.append(self.paths)

        # Make button entities
        self.buttons = []
        self.buttons.append(Button(WHITE, (300,25), self.spawn_unit,pygame.image.load(MELEE_IMAGE), "Melee"))
        self.buttons.append(Button(WHITE, (700,25), self.spawn_unit,pygame.image.load(TANK_IMAGE), "Tank"))
        entities.append(self.buttons)

        self.units = []
        self.enemy_units = []
        entities.append(self.units)
        entities.append(self.enemy_units)

        # Performance improvements
        #self.screen = pygame.display.set_mode((1366, 768), (pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF))
        self.screen = pygame.display.set_mode((1366, 768), (pygame.HWSURFACE | pygame.DOUBLEBUF))
        self.screen.set_alpha(None)
        font = pygame.font.Font(None, 36)

        clock = pygame.time.Clock()

        # Main Render Loop
        while True:
            dt = clock.tick(50)
            ms = dt / 1000.0 # dt in seconds

            events = pygame.event.get()
            self.screen.fill((144, 245, 0))  # Green background

            for entity in entities:
                for item in entity:
                    item.drawon(self.screen, dt)

            text = font.render(str(self.you.getMoney()), 1, (10, 10, 10))
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

            self.checkCollision(ms)

            pygame.display.flip()

    def spawn_unit(self, unit):
        i = 0
        for base in self.my_bases:
            if base.active:
                coords = base.getcoords()
                if unit == "Melee":
                    cost = MELEECOST
                    unit = Melee(GREY, (coords[0] + coords[2], coords[1] + coords[3]/2 - 25), RIGHT)
                    self.send.put("{'name': 'spawn_enemy', 'type': 'Melee', 'base': " + str(i) + "}")
                elif unit == "Tank":
                    cost = TANKCOST
                    unit = Tank(RED, (coords[0] + coords[2], coords[1] + coords[3]/2 - 25), RIGHT)
                    self.send.put("{'name': 'spawn_enemy', 'type': 'Tank', 'base': " + str(i) + "}")

                if self.you.getMoney() > cost:
                    self.you.removeMoney(cost)
                    self.units.append(unit)
            i += 1

    def spawn_enemy(self, type, base):
        spawnpoint = self.enemy_bases[base]
        coords = spawnpoint.getcoords()
        if type == "Melee":
            cost = MELEECOST
            unit = Melee(GREY, (coords[0] + coords[2], coords[1] + coords[3] / 2 - 25), LEFT)
        if type == "Tank":
            unit = Tank(GREY, (coords[0] + coords[2], coords[1] + coords[3] / 2 - 25), LEFT)

        self.enemy_units.append(unit)

    def checkCollision(self, dt):
        for unit in self.units:
            en_units = [u for u in self.enemy_units if unit.intersects(u.getpos()) and not unit == u]
            my_units = [u for u in self.units if unit.intersects(u.getpos()) and not unit == u]

            if unit.getpos()[0] > 1200:
                sys.exit()

            unit.resumeSpeed()

            if en_units:  # list is not empty
                for u in en_units:  # u is enemies that intersect
                    u.attack(unit, dt)
                    unit.attack(u, dt)

                    u.setSpeed(0)
                    unit.setSpeed(0)

                    if u.getHealth() < 0:
                        self.enemy_units.remove(u)
                        self.you.addMoney(u.getReward())
                        unit.resumeSpeed()
                    if unit.getHealth() < 0:
                        self.units.remove(unit)
                        self.enemy.addMoney(unit.getReward())
                        u.resumeSpeed()

            if my_units:
                for u in my_units:
                    u.setSpeed(0)

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