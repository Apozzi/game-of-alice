from pymeow import *
from time import sleep

class AliceGameExeBoardData:
    def __init__(self):
        self.list = []
        self.acProc = process_by_name("AaY_InThePlanetOfNumber.exe")
        self.acBase = self.acProc["baseaddr"] ## 0x002E0000

    def convertToIntToItem(self, value):
        if value == 13:
          return '#'
        if value == 12:
          return 'F'
        if value > 10:
          return '1'
        return str(value)

    def loadBoard(self):
        classePointer = read_int(self.acProc, self.acBase + 0x1CC034)
        offsetAddress = 0x005005F4
        offsetX = 0x64
        offsetY = 2
        changeCenterOffset = - 10*offsetX - 3*offsetY
        for y in range(0, 20):
            self.list.append([])
            for x in range(0, 32):
                try:
                    boardPositionOffset = changeCenterOffset + x*offsetX + y*offsetY
                    valor = read_byte(self.acProc, classePointer + offsetAddress*2 + boardPositionOffset)
                    if (valor != 240):
                        self.list[y].append(valor)
                except:
                    continue
        def removeLeftZeros(L):
            while L and L[-1] == 0:
                L.pop(-1)
                removeLeftZeros(L)
            return L
        def convertToIntToItem(value):
            if value == 0:
                return ' '
            if value == 13:
                return '#'
            if value == 12:
                return 'F'
            if value == 254 or value == 255:
                return '@'
            if value > 10:
                return 'B'
            return str(value)
        self.list = [list(map(convertToIntToItem, x)) for x in [removeLeftZeros(l) for l in self.list] if x != [] and x != [0, 0]]
    def getBoard(self):
        return self.list
    def getBoardHeight(self):
        return len(self.list[0])
    def getBoardWidth(self):
        return len(self.list)
    def getPlayerPosition(self):
        for x in range(0, self.getBoardWidth()):
            for y in range(0, self.getBoardHeight()):
                if self.list[x][y] == '@':
                    return (x, y)
        
