'''from Units import *

class _Player:
    def __init__(self):
        self.bases = []
        self.units = []

        base_img = pygame.image.load("Images/temp.png")
        self.bases.append(Base(WHITE, (100, 100, 100, 100), base_img))
        self.bases.append(Base(WHITE, (100, 350, 100, 100), base_img))
        self.bases.append(Base(WHITE, (100, 600, 100, 100), base_img))
        
        self.money = 1000
        self.active_base = self.bases[0]
        
    def add_money(self, amount):
        self.money += amount
        
    def get_money(self):
        return self.money
    
    def add_unit(self, type):
        if type == 'Melee':

    
    def set_active_base(self, i):
        pass
        
    def draw_bases(self):
        base_img = pygame.image.load("Images/temp.png")
        self.bases.append(Base(WHITE, (100, 100, 100, 100), base_img))
        self.bases.append(Base(WHITE, (100, 350, 100, 100), base_img))
        self.bases.append(Base(WHITE, (100, 600, 100, 100), base_img))
        
    def draw_units(self):
        
        
        
        
class Self(_Player):
    
class Enemy(_Player):
'''