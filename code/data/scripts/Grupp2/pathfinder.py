import hud as gui
import time, math, random, navmesh, demo, nmath


class PathFinder:

    def AStar(self, agentPosition, goalPosition):
        print("hello")
        goalFound = False
        visited = []
        global path
        path = []
        backtrack = {}
        ghfValues = {}  # key = face, value = (g, h, f)

        startFace = navmesh.findInNavMesh((agentPosition.x, agentPosition.z))
        ghfValues[startFace] = (0, 0, 0)
        goalFace = navmesh.findInNavMesh((goalPosition.x, goalPosition.z))

        backtrack[startFace] = 0
        openList = []
        closedList = []
        openList.append(startFace)

        while openList:
            q = openList[0]
            # find best block by f value
            for i in range(len(openList)):
                if ghfValues.get(q)[2] > ghfValues.get(openList[i])[2]:
                    q = openList[i]
            openList.remove(q)

            # go through all successors
            neighbouringFaces = self.GetNeighbouringFaces(q)
            for neighbourFace in neighbouringFaces:
                skip = False
                #neighbourBlock = paths.GetBlockByID(neighbourID)

                if (neighbourFace == goalFace):
                    path.append(navmesh.getCenterOfFace(neighbourFace))
                    prevFace = backtrack.get(q)
                    while (prevFace != 0):
                        #prevBlock = paths.GetBlockByID(prevID)
                        path.append(navmesh.getCenterOfFace(prevFace))
                        prevFace = backtrack.get(prevFace)
                    return path

                g = ghfValues.get(q) + 1 # g value addition should not be one but instead distance from this and previous center
                h = self.Euclidean(neighbourFace, goalFace)
                f = g + h
                ghf = [(g, h, f)]
                ghfValues[neighbourFace] = ghf

                for i in openList:
                    if (i == neighbourFace and ghfValues.get(neighbourFace)[2] >= ghfValues.get(i)[2]):
                        skip = True
                for i in closedList:
                    if (i == neighbourFace and ghfValues.get(neighbourFace)[2] >= ghfValues.get(i)[2]):
                        skip = True
                if skip is False:
                    # set q as parent to all neighbour blocks
                    backtrack[neighbourFace] = q
                    openList.append(neighbourFace)
            closedList.append(q)
            # gui.Clear()
            # gui.DrawAStar(openList, closedList)
            # gui.Update()
            # time.sleep(0.01)

    def Euclidean(self, currentFace, goalFace):
        # Getting Vector 3
        cPos = navmesh.getCenterOfFace(currentFace)
        gPos = navmesh.getCenterOfFace(goalFace)
        # Extracting just x and z
        xCur = cPos.x
        zCur = cPos.z
        xGoal = gPos.x
        zGoal = gPos.z

        h = math.sqrt((xCur - xGoal) ** 2 + (zCur - zGoal) ** 2)
        return h

    def GetNeighbouringFaces(self, face):
        neighbouringFaces = []
        h1 = navmesh.getHalfEdge(face)
        h2 = navmesh.getHalfEdge(h1.nextEdge)
        h3 = navmesh.getHalfEdge(h2.nextEdge)
        n1 = navmesh.getHalfEdge(h1.neighbourEdge)
        n2 = navmesh.getHalfEdge(h2.neighbourEdge)
        n3 = navmesh.getHalfEdge(h3.neighbourEdge)
        f1 = navmesh.getFace(n1.face)
        f2 = navmesh.getFace(n2.face)
        f3 = navmesh.getFace(n3.face)
        neighbouringFaces.append(f1)
        neighbouringFaces.append(f2)
        neighbouringFaces.append(f3)
        return neighbouringFaces

    def DrawAStar(self):
        for i in range(len(path)-1):
            startPoint = nmath.Point(path[i].x, 2, path[i].z)
            endPoint = nmath.Point(path[i+1].x, 2, path[i+1].z)
            demo.DrawLine(startPoint, endPoint, 1, nmath.Vec4(1, 0, 0, 1))

class PathBlock:
    prevBlockID = 0
    # A* values
    g = 0.0
    h = 0.0
    f = 0.0

    woodPile = 0
    hasWood = False
    isFogged = True
    def __init__(self, ID, adjacents, ms, hasTrees, walkable):
        self.id = ID
        self.adjacents = adjacents
        self.ms = ms  # 1 for mark and 0.5 for trees and sumpmark
        self.hasTrees = hasTrees
        if(self.hasTrees):
            self.trees = 5
        self.walkable = walkable
        self.kilns = []

    def IdToCoordinates(self):
        x = int(self.id % 100)
        y = int(self.id / 100)
        return (x,y)

    def GetPrevBlock(self):
        return paths.GetBlockByID(self.prevBlockID)

    def Discover(self):
        if self.isFogged:
            self.isFogged = False

    def RemoveTree(self):
        if(self.hasTrees):
            self.trees -= 1
            if(self.trees <= 0):
                self.hasTrees = False

    def DropWood(self):
        if self.hasWood == False:
            self.hasWood = True
        self.woodPile += 1
        #print(self.id, "GOT WOOD")

    def TakeWood(self):
        if self.hasWood:
            self.woodPile -= 1
            if self.woodPile == 0:
                self.hasWood = False
        else:
            print("This tile has no wood!!!")

class Paths:
    pathBlocks = {}
    unwalkables = {}

    def GetStart(self):
        return self.pathBlocks.get("start")

    def GetGoal(self):
        return self.pathBlocks.get("goal")

    def GetBlockByID(self, ID):
        return self.pathBlocks.get(ID)

    def GetUnwalkableByID(self, ID):
        return self.unwalkables.get(ID)

    def GetRandomBlock(self):
        r = random.choice(list(self.pathBlocks.values()))
        return r

    def GetNthBlock(self, n):
        if n < 0:
            n += len(self.pathBlocks)
        for i, block in enumerate(self.pathBlocks.values()):
            if i == n:
                return block
        raise IndexError("dictionary index out of range")

paths = Paths()
pf = PathFinder()
