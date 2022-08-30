import colorful as cf

class ConsoleInterface:
    def __init__(self, table):
        self.table = table
        self.positionsOfPathToDraw = []
    def tableColor(self, str):
        return cf.italic_coral_on_beige(str)
    def pathColor(self, str):
        return cf.red_on_yellow(str)
    def createPath(self, path: list[tuple]):
        resultPosPathToDraw = []
        previousPos = None
        for pos in path:
            if previousPos:
                resultPosPathToDraw.append(previousPos)
                xPos = pos[0]; xPreviousPos = previousPos[0]
                yPos = pos[1]; yPreviousPos = previousPos[1]
                xMove = 0
                yMove = 0
                if xPos < xPreviousPos: xMove = 1
                if xPos > xPreviousPos: xMove = -1
                if yPos < yPreviousPos: yMove = 1
                if yPos > yPreviousPos: yMove = -1
                while (xPos != xPreviousPos or yPos != yPreviousPos):
                    resultPosPathToDraw.append((xPos, yPos))
                    xPos += xMove
                    yPos += yMove
            previousPos = pos
        self.positionsOfPathToDraw = resultPosPathToDraw
    def clearPath(self):
        self.positionsOfPathToDraw = []
    def draw(self):
        toPrint = ''
        emptyLine = self.tableColor(' '.join([' ']*(self.table.getHeight() + 1))) + '\n'
        toPrint += emptyLine
        table = self.table.getList()
        for x in range(len(table)):
            columnToPrint = ''
            for y in range(len(table[x])):
                isPath = (x,y) in self.positionsOfPathToDraw
                columnToPrint += self.tableColor(' ') 
                if isPath:
                    columnToPrint += self.pathColor(str(table[x][y]))
                else:
                    columnToPrint += self.tableColor(str(table[x][y]))
            toPrint += columnToPrint + self.tableColor(' ') + '\n'
        toPrint += emptyLine
        print(toPrint)