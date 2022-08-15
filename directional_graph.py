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
    def __interceptionOfEdges(self, line1, line2):
        # Simplistic Line Segment intersection algoritm only for right angles.
        def equalPoints(p1, p2):
            return p1[0] == p2[0] and p1[1] == p2[1]
        def crossInterception(p1,p2,p3,p4,i,j):
            crossX = p3[i] == p4[i] and ((p1[i] <= p3[i] and p3[i] <= p2[i]) or (p1[i] >= p3[i] and p3[i] >= p2[i]))
            crossY = p1[j] == p2[j] and ((p3[j] < p1[j] and p1[j] < p4[j]) or (p3[j] > p1[j] and p1[j] > p4[j]))
            if (crossX and crossY): 
                print("cross")
            return crossX and crossY
        def innerLineInterception(i, j) :
            if (equalPoints(line1[1], line2[0])) and line2[1][j] == line1[0][j]:
                if line1[0][i] > line1[1][i]:
                    return line1[1][i] < line2[1][i]
                else:
                    return line1[1][i] > line2[1][i]
            return False
        innerLineIntersectionXY = innerLineInterception(0, 1) or innerLineInterception(1, 0)
        crossIntersectionXY = crossInterception(line1[0], line1[1], line2[0], line2[1], 0, 1) or crossInterception(line1[0], line1[1], line2[0], line2[1], 1, 0)
        return (innerLineIntersectionXY or crossIntersectionXY)
    def __verifyInterceptionInPath(self, path):
        pathLength = len(path)
        for i in range(0, pathLength - 1):
            for j in range(0, pathLength - 1):
                if (j != i):
                    line1 = (path[i], path[i + 1])
                    line2 = (path[j], path[j + 1])
                    if (self.__interceptionOfEdges(line1, line2)):
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