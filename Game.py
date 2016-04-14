import os
from Units import *
from GifImage import GIFImage
from Constants import BROWN
from Constants import WHITE
from Constants import RIGHT
from Constants import LEFT


class RTSGame:
    def __init__(self):
        entities = []

        self.basesP1 = []
        self.basesP1.append(Base(WHITE, (100, 100, 100, 100)))
        self.basesP1.append(Base(WHITE, (100, 350, 100, 100)))
        self.basesP1.append(Base(WHITE, (100, 600, 100, 100)))

        self.basesP2 = []
        self.basesP2.append(Base(WHITE, (1200, 100, 100, 100)))
        self.basesP2.append(Base(WHITE, (1200, 350, 100, 100)))
        self.basesP2.append(Base(WHITE, (1200, 600, 100, 100)))
        entities.append(self.basesP1)
        entities.append(self.basesP2)

        paths = []
        paths.append(Box(BROWN, ((200, 112.5, 1000, 75))))
        paths.append(Box(BROWN, ((200, 362.5, 1000, 75))))
        paths.append(Box(BROWN, ((200, 612.5, 1000, 75))))
        entities.append(paths)

        self.units = []
        entities.append(self.units)

        self.buttons = []
        self.buttons.append(Button(WHITE, (100, 25, 50, 40), self.spawn_unit))
        entities.append(self.buttons)

        self.screen = pygame.display.set_mode((1366, 768))
        clock = pygame.time.Clock()

        running = True
        while running:
            dt = clock.tick(50)

            events = pygame.event.get()
            self.screen.fill((144, 245, 0))

            for entity in entities:
                for item in entity:
                    item.drawon(self.screen, dt)

            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    self.checkBounds(pos)

            self.checkCollision()

            pygame.display.flip()

    def spawn_unit(self):
        for base in self.basesP1:
            if base.active:
                coords = base.getcoords()
                self.units.append(Melee(GREY, (coords[0] + coords[2], coords[1] + coords[3] / 2, 25, 25), RIGHT))
                self.units.append(Melee(GREY, (coords[0] + coords[2] + 975, coords[1] + coords[3] / 2, 25, 25), LEFT))

    def checkCollision(self):
        for unit in self.units:
            ounits = [u for u in self.units if unit.intersects(u.getpos()) and not unit == u]
            if ounits:  # list is not empty
                for u in ounits:
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
                break

        return
