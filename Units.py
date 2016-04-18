import pygame
from Constants import *

# BASIC UNITS

class _Unit:  # _ = implementation class

    def __init__(self, color, coords, image):
        self.color = color
        self.coords = coords
        self.image = image
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.getpos())

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
    def __init__(self, color, coords, image):
        _Unit.__init__(self, color, coords, pygame.transform.scale(image, (100, 100)))
        self.active = False
        self.health = 250

    def setActive(self):
        self.active = True
        self.color = GREY

    def setUnactive(self):
        self.active = False
        self.color = WHITE


class Box(_Unit):
    def __init__(self, color, coords, image):
        _Unit.__init__(self, color, coords, pygame.transform.scale(image, (100, 100)))


class Button(_Unit):
    def __init__(self, color, coords, command, image, unit):
        _Unit.__init__(self, color, coords, pygame.transform.scale(image, (100, 75)))
        self.command = command
        self.unit = unit

    def clicked(self):
        self.command(self.unit)

    def drawon(self, screen, dt):
        screen.blit(self.image, self.rect)

    def intersects(self, pos):
        return self.rect.x <= pos[0] <= self.rect.x + self.rect.width \
               and self.rect.y <= pos[1] <= self.rect.y + self.rect.height

# MOVING UNITS

class _MovingUnit(_Unit):
    def __init__(self, color, coords, health, range, cost, speed, damage, reward, image):
        _Unit.__init__(self, color, coords, pygame.transform.scale(image, (75, 75)))
        self.health = health
        self.range = range
        self.cost = cost
        self.speed = speed
        self.damage = damage
        self.reward = reward

    def drawon(self, screen, dt):
        # Increases x-coord in tuple by dt
        lst = list(self.coords)
        dx = (self.speed * (1 / float(dt)))
        lst[0] += dx
        self.setcoords(tuple(lst))
        self.rect = self.rect.move(dx, 0)
        screen.blit(self.image, self.rect)

    def getReward(self):
        return self.reward

    def getPlayer(self):
        return self.player

    def intersects(self, pos):
        return self.rect.x <= pos[0] <= self.rect.x + self.rect.width \
               and self.rect.y <= pos[1] <= self.rect.y + self.rect.height

class Melee(_MovingUnit):
    def __init__(self, color, coords, dir):
        '''
        if player.isEnemy:
            image = pygame.transform.flip(image, True, False)
        '''
        image = pygame.image.load("Images/Melee.png")
        _MovingUnit.__init__(self, color, coords, MELEEHP, MELEERANGE, MELEECOST, dir*23, MELEEDAMAGE, MELEEREWARD, image)

class Ranged(_MovingUnit):
    def __init__(self, color, coords, dir):
        image = pygame.image.load("Images/Archer.png")
        _MovingUnit.__init__(self, color, coords, RANGEHP, RANGERANGE, RANGECOST, dir*21, RANGEDAMAGE, RANGEREWARD, image)


class Tank(_MovingUnit):
    def __init__(self, color, coords, dir, player):
        image = pygame.image.load("Images/Tank.gif")
        _MovingUnit.__init__(self, color, coords, TANKHP, TANKRANGE, TANKCOST, dir*20, TANKDAMAGE, TANKREWARD, image)


class Recon(_MovingUnit):
    def __init__(self, color, coords, dir, player):
        image = pygame.image.load("Images/Archer.png")
        _MovingUnit.__init__(self, color, coords, RECONHP, RECONRANGE, RECONCOST, dir*30, RECONDAMAGE, RECONREWARD, image)