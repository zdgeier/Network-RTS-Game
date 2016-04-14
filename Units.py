import pygame
from Constants import GREY
from Constants import WHITE


# BASIC UNITS

class _Unit:  # _ = implementation class

    def __init__(self, color, coords):
        self.color = color
        self.coords = coords

    def intersects(self, pos):
        return self.coords[0] <= pos[0] <= self.coords[0] + self.coords[2] \
               and self.coords[1] <= pos[1] <= self.coords[1] + self.coords[3]

    def getpos(self):
        return self.coords[0], self.coords[1]

    def getcoords(self):
        return self.coords

    def getcolor(self):
        return self.color

    def setcoords(self, coords):
        self.coords = coords

    def setcolor(self, color):
        self.color = color

    def drawon(self, screen, dt):
        pygame.draw.rect(screen, self.getcolor(), self.getcoords())


class Base(_Unit):
    def __init__(self, color, coords):
        _Unit.__init__(self, color, coords)
        self.active = False

    def setActive(self):
        self.active = True
        self.color = GREY

    def setUnactive(self):
        self.active = False
        self.color = WHITE


class Box(_Unit):
    def __init__(self, color, coords):
        _Unit.__init__(self, color, coords)


class Button(_Unit):
    def __init__(self, color, coords, command):
        _Unit.__init__(self, color, coords)
        self.command = command

    def clicked(self):
        self.command()


# MOVING UNITS


class _MovingUnit(_Unit):
    def __init__(self, color, coords, health, rnge, cost, speed, damage):
        _Unit.__init__(self, color, coords)
        self.health = health
        self.range = rnge
        self.cost = cost
        self.speed = speed
        self.damage = damage

    def drawon(self, screen, dt):
        # Increases x-coord in tuple by dt
        lst = list(self.coords)
        lst[0] += self.speed * (1 / float(dt))
        self.setcoords(tuple(lst))
        pygame.draw.rect(screen, self.getcolor(), self.getcoords())

class Melee(_MovingUnit):
    def __init__(self, color, coords, dir):
        _MovingUnit.__init__(self, color, coords, 100, 1, 100, dir*20, 5)


class Ranged(_MovingUnit):
    def __init__(self, color, coords, dir):
        _MovingUnit.__init__(self, color, coords, 100, 1, 100, dir*20, 5)


class Tank(_MovingUnit):
    def __init__(self, color, coords, dir):
        _MovingUnit.__init__(self, color, coords, 100, 1, 100, dir*20, 5)


class Recon(_MovingUnit):
    def __init__(self, color, coords, dir):
        _MovingUnit.__init__(self, color, coords, 100, 1, 100, dir*20, 5)