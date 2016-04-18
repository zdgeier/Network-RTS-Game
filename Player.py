class Player:
    def __init__(self, bases, name):
        self.money = 1000
        self.basesLeft = len(bases)
        self.name = name

    def getBases(self):
        return self.basesLeft

    def getMoney(self):
        return self.money

    def getName(self):
        return self.name

    def addMoney(self, value):
        self.money += value

    def removeMoney(self, value):
        self.money -= value