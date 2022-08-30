import random
WALL_CHAR = '#'

class Table:
    FLAG_SIMBOL = 'F'
    BONUS = 'B'
    def __init__(self, width, height, maxValue=0):
        self.sizeHeight = height
        self.sizeWidth= width
        self.list = [[0]*(height) for _ in range(width)]
        self.maxValue = maxValue
        self.listOfNumericPositions = set()
        self.randomizeTable()
    def randomizeTable(self):
        if self.maxValue == 0:
            self.maxValue = int(self.sizeWidth / 2)
        for x in range(0, self.sizeWidth):
            for y in range(0, self.sizeHeight):
                self.setValue(x, y, random.randint(1, self.maxValue))
    def loadFromList(self, list):
        for x in range(0, self.sizeWidth):
            for y in range(0, self.sizeHeight):
                self.setValue(x, y, list[x][y])
    def getList(self):
        return self.list
    def getSize(self):
        return (self.sizeWidth + self.sizeHeight) / 2
    def getHeight(self):
        return self.sizeHeight
    def getWidth(self):
        return self.sizeWidth
    def setMaxValue(self, value):
        self.maxValue = value
    def setValue(self, x, y, value):
        self.list[x][y] = value
        position = (x, y)
        char = self.list[x][y]
        if (isinstance(char, int) or char == self.FLAG_SIMBOL):
            if not (position in self.listOfNumericPositions):
                self.listOfNumericPositions.add(position)
        else:
            if position in self.listOfNumericPositions and (not value or value == ' '):
                self.listOfNumericPositions.remove(position)
    def createFlag(self,x, y):
        self.setValue(x, y, self.FLAG_SIMBOL)
    def createFlagOnRandomNumericLocation(self):
        xRandom = random.randint(0, self.sizeWidth - 1)
        yRandom = random.randint(0, self.sizeHeight - 1)
        char = self.list[xRandom][yRandom]
        if (isinstance(char, int)):
            self.createFlag(xRandom, yRandom)
        else:
            self.createFlagOnRandomNumericLocation()
    def getFlagCoords(self):
        return self.__getCoordsFromCharacter(self.FLAG_SIMBOL)
    def getValue(self, x, y):
        return self.list[x][y]
    def addWallsOnBorders(self):
        borderPos = self.sizeWidth - 1
        sizeDiff = self.sizeHeight - self.sizeWidth
        for i in range(0, self.sizeWidth):
            self.setValue(i , 0, WALL_CHAR)
            self.setValue(i, borderPos + sizeDiff, WALL_CHAR)
            self.setValue(0, i + sizeDiff, WALL_CHAR)
            self.setValue(borderPos, i + sizeDiff, WALL_CHAR)
    def getListOfNumericTablePositions(self):
        return list(self.listOfNumericPositions)
    def __getCoordsFromCharacter(self, char):
        xCoord = -1; yCoord = -1
        for x in range(0, self.sizeWidth - 1):
            for y in range(0, self.sizeHeight - 1):
                if (self.list[x][y] == char):
                    xCoord = x
                    yCoord = y
        return (xCoord, yCoord)
    def __isValidMovementCharacter(self, x, y):
        try:
            if (x < self.sizeWidth and x >= 0 and y < self.sizeHeight and y >= 0):
                int(self.list[x][y])
                return True
            return False
        except ValueError:
            return False
    def stopChars(self, nextPositionChar):
        return nextPositionChar == self.FLAG_SIMBOL or nextPositionChar == self.BONUS
    def moveUsingNumber(self, x, y, movX, movY, removeMovedTiles = False):
        sign = lambda x: (1, -1)[x<0]
        posX = x; posY = y
        if (self.__isValidMovementCharacter(x + movX, y + movY)):
            numberOnTable = int(self.getValue(x + movX, y + movY))
            xNumber = 0 if movX==0 else sign(movX)
            yNumber = 0 if movY==0 else sign(movY)
            for _ in range(numberOnTable):
                nextPositionChar = self.getValue(posX + xNumber, posY + yNumber)
                if (nextPositionChar != WALL_CHAR):
                    stop = False
                    if (self.stopChars(nextPositionChar)):
                        stop = True
                    if (removeMovedTiles):
                        self.setValue(posX, posY, ' ')
                    posX+=xNumber
                    posY+=yNumber
                    if (self.getValue(posX, posY) == ' '):
                        # Returns String Dead in case of bad movement
                        return 'Dead'
                    if stop:
                        break
            return (posX, posY)
        else:
            return None
    def __addDiagonalMovementToListOfMovements(self, posX, posY, listOfMovements):
        topLeftPos= self.moveUsingNumber(posX, posY, -1, -1)
        topRightPos= self.moveUsingNumber(posX, posY, -1, 1)
        bottomLeftPos= self.moveUsingNumber(posX, posY, 1, -1)
        bottomRightPos= self.moveUsingNumber(posX, posY, 1, 1)
        if (topLeftPos != None):
            listOfMovements.append(topLeftPos)
        if (topRightPos != None):
            listOfMovements.append(topRightPos)
        if (bottomLeftPos != None):
            listOfMovements.append(bottomLeftPos)
        if (bottomRightPos != None):
            listOfMovements.append(bottomRightPos)
            
    def getListOfMovementsInPosition(self, posX, posY):
        listOfMovements = []
        topPos= self.moveUsingNumber(posX, posY, -1, 0)
        bottomPos = self.moveUsingNumber(posX, posY, 1, 0)
        leftPos = self.moveUsingNumber(posX, posY, 0, -1)
        rightPos = self.moveUsingNumber(posX, posY, 0, 1)
        if (topPos != None):
            listOfMovements.append(topPos)
        if (bottomPos != None):
            listOfMovements.append(bottomPos)
        if (leftPos != None):
            listOfMovements.append(leftPos)
        if (rightPos != None):
            listOfMovements.append(rightPos)
        self.__addDiagonalMovementToListOfMovements(posX, posY, listOfMovements)
        return listOfMovements