from table import Table

class Agent:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.alive = True
    def setCenterPosision(self, tableSize):
        self.x = int(tableSize / 2)
        self.y = self.x
    def setPosision(self, x, y):
        self.x = x
        self.y = y
    def setAgentOnTable(self, table: Table):
        table.setValue(self.x, self.y, '@')
    def __moveOnTable(self, table: Table, x, y):
        positionToMove = table.moveUsingNumber(self.x, self.y, x, y, True)
        if (positionToMove != None):
            if (positionToMove == 'Dead'):
                table.setValue(self.x, self.y, ' ')
                self.kill()
            else:
                self.x = positionToMove[0]
                self.y = positionToMove[1]
                self.setAgentOnTable(table)
    def moveUpOnTable(self, table):
        self.__moveOnTable(table, -1, 0)
    def moveDownOnTable(self, table):
        self.__moveOnTable(table, 1, 0)
    def moveLeftOnTable(self, table):
        self.__moveOnTable(table, 0, -1)
    def moveRightOnTable(self, table):
        self.__moveOnTable(table, 0, 1)
    def moveDiagonalUpRightOnTable(self, table):
        self.__moveOnTable(table, -1, 1)
    def moveDiagonalUpLeftOnTable(self, table):
        self.__moveOnTable(table, -1, -1)
    def moveDiagonalDownLeftOnTable(self, table):
        self.__moveOnTable(table, 1, -1)
    def moveDiagonalDownRightOnTable(self, table):
        self.__moveOnTable(table, 1, -1)
    def kill(self):
        self.alive = False
    def isDead(self):
        return not self.alive
    def getAgentPosition(self):
        return (self.x, self.y)