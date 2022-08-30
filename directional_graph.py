from point import Point
from line import Line

#------------------------------
#  https://algs4.cs.princeton.edu/42digraph/AdjMatrixDigraph.java.html
#------------------------------

class DirectionalGraph:
    def __init__(self):
        self.size = 0
        self.vertices = []
        self.edges = []
        self.adjMatrix:list[list] = []
        self.previousVertexDict = {}
    def addVertex(self, vertex):
        self.size+=1
        self.vertices.append(vertex)
        self.adjMatrix.append([])
        for i in range(0, len(self.adjMatrix)):
            for _ in range(len(self.adjMatrix[i]), len(self.adjMatrix)):
                self.adjMatrix[i].append(False)
    def addVerticesFrom(self, vertices):
        for vertex in vertices:
            self.addVertex(vertex)
    def addEdge(self, vertexIn, vertexOut):
        if (vertexIn not in self.vertices) or (vertexOut not in self.vertices):
            return
        posVertexStart = self.vertices.index(vertexIn)
        posVertexEnd = self.vertices.index(vertexOut)
        if not self.adjMatrix[posVertexStart][posVertexEnd]:
            self.edges.append([vertexIn, vertexOut])
            self.adjMatrix[posVertexStart][posVertexEnd] = True
    def removeEdge(self, vertexIn, vertexOut):
        posVertexStart = self.vertices.index(vertexIn)
        posVertexEnd = self.vertices.index(vertexOut)
        if self.adjMatrix[posVertexStart][posVertexEnd]:
            self.edges.remove([vertexIn, vertexOut])
            self.adjMatrix[posVertexStart][posVertexEnd] = False
    def __getAdjInOut(self, isIn, isOut, vertex):
        posVertex = self.vertices.index(vertex)
        edgesList = []
        for i in range(0, self.size):
            if isIn:
                if self.adjMatrix[posVertex][i]:
                    edgesList.append(self.vertices[i])
            if isOut:
                if self.adjMatrix[i][isOut]:
                    edgesList.append(self.vertices[i])
        return edgesList
    def inEdges(self, vertex):
        return self.__getAdjInOut(True, False, vertex)
    def outEdges(self, vertex):
        return self.__getAdjInOut(False, True, vertex)
    def adj(self, vertex):
        return self.__getAdjInOut(True, True, vertex)
    def __boundingRectCollision(self, line1, line2):
        xver = (line1.getMinX() <= line2.getMaxX() and line1.getMaxX() >= line2.getMinX())
        yver = (line1.getMinY() <= line2.getMaxY() and line1.getMaxY() >= line2.getMinY())
        xvern = (line1.getMinX() < line2.getMaxX() and line1.getMaxX() > line2.getMinX())
        yvern = (line1.getMinY() < line2.getMaxY() and line1.getMaxY() > line2.getMinY())
        return (xver and yvern) or (xvern and yver)
    def __verifyDiagonalsParity(self, line1, line2):
        parityCheck = ((line1.start_point.x + line1.start_point.y) % 2) == ((line2.start_point.x + line2.start_point.y) % 2)
        verifyDiffDiagonals = (line1.isAscendingLine() and line2.isDescendingLine()) or (line2.isAscendingLine() and line1.isDescendingLine()) 
        return parityCheck and verifyDiffDiagonals
    def __interseptionOfEdges(self, line1, line2):
        line1Obj = Line(line1)
        line2Obj = Line(line2)
        if (not self.__boundingRectCollision(line1Obj, line2Obj)):
            return False
        if (line1Obj.continuityBetween(line2Obj) and line1Obj.getAngle() != line2Obj.getAngle()):
            return False
        if (self.__verifyDiagonalsParity(line1Obj, line2Obj)):
            return False
        p1 = Point(line1[0]); p2 = Point(line1[1])
        p3 = Point(line2[0]); p4 = Point(line2[1])
        div = ((p1.x - p2.x)*(p3.y - p4.y) - (p1.y - p2.y)*(p3.x - p4.x))
        if (div == 0) : return True
        t = ((p1.x - p3.x)*(p1.y - p2.y) - (p1.y - p3.y)*(p1.x-p2.x))/div
        return (t >= 0 and t <= 1)
    def __verifyInterceptionInPath(self, path):
        pathLength = len(path)
        for i in range(0, pathLength - 1):
            for j in range(0, pathLength - 1):
                if (j != i):
                    line1 = (path[i], path[i + 1])
                    line2 = (path[j], path[j + 1])
                    if (self.__interseptionOfEdges(line1, line2)):
                        return j
        return None
    def shortestPath(self, startVertex, endVertex, recalc = True):
        if (recalc):
            self.previousVertexDict = {}
        # Uses BFS algorithm to determine the shortest path with a previous dictionary.
        queue = [startVertex]
        visited = {}
        visited[startVertex] = True
        while queue:
            vt = queue.pop(0)
            adj = self.inEdges(vt)
            for adjecent in adj:
                if (not visited.get(adjecent)):
                    visited[adjecent] = True
                    self.previousVertexDict[adjecent] = vt
                    queue.append(adjecent)
        
        # Getting the path.
        reversePath = [endVertex]
        previous = self.previousVertexDict.get(endVertex)
        while previous:
            reversePath.append(previous)
            previous = self.previousVertexDict.get(previous)
        # Uses my own algoritm to detect interception and correct to not move same node or position two times.
        interceptedVertexesPos = self.__verifyInterceptionInPath(reversePath)
        if (interceptedVertexesPos != None):
            print("entrou")
            startVi = reversePath[interceptedVertexesPos]
            endVi= reversePath[interceptedVertexesPos + 1]
            self.removeEdge(startVi, endVi)
            self.removeEdge(endVi, startVi)
            reversePath = self.shortestPath(startVertex, endVertex)[::-1]
        return reversePath[::-1]