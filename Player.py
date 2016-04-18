class Player:
    def __init__(self, bases, isEnemy):
        self.money = 1000
        self.basesLeft = len(bases)
        self.isEnemy = isEnemy

    def getBases(self):
        return self.basesLeft

    def getMoney(self):
        return int(5 * round(float(self.money)/5))

    def addMoney(self, value):
        self.money += value

    def removeMoney(self, value):
        self.money -= value