import hud as gui
import time, math, random, navmesh


class PathFinder:
    goalFound = False
    visited = []
    path = []
    backtrack = {}

    # Resets all values so the next run wont be affected by the previous one
    def Reset(self):
        self.visited = []
        self.path = []
        self.backtrack = {}
        self.goalFound = False

    def bfs(self, startBlock):
        self.backtrack[startBlock.id] = 0
        self.visited.append(startBlock)
        bfsQ = []
        bfsQ.append(startBlock)
        while bfsQ:
            s = bfsQ.pop(0)
            for neighbour in s.adjacents:
                neighbourBlock = paths.GetBlockByID(neighbour)
                if neighbourBlock not in self.visited and neighbourBlock.isFogged is False:
                    self.visited.append(neighbourBlock)
                    bfsQ.append(neighbourBlock)
                    self.backtrack[neighbourBlock.id] = s.id
                    # neighbourBlock.prevBlockID = s.id
                    if (neighbourBlock.hasTrees):
                        self.path.append(neighbourBlock)
                        prevID = self.backtrack.get(neighbourBlock.id)
                        #prevID = neighbourBlock.prevBlockID
                        while (prevID != 0):
                            prevBlock = paths.GetBlockByID(prevID)
                            self.path.append(prevBlock)
                            prevID = self.backtrack.get(prevBlock.id)
                            #prevID = prevBlock.prevBlockID
                        return self.path
            # gui.Clear()
            # gui.DrawVisited(self.visited)
            # gui.Update()
            # time.sleep(0.01)

    def AStar(self, startBlock, goalBlock):
        self.backtrack[startBlock.id] = 0
        openList = []
        closedList = []
        openList.append(startBlock)

        while openList:
            q = openList[0]
            # find best block by f value
            for i in range(len(openList)):
                if (q.f > openList[i].f):
                    q = openList[i]
            openList.remove(q)
            # go through all successors
            for neighbourID in q.adjacents:
                skip = False
                neighbourBlock = paths.GetBlockByID(neighbourID)

                if (neighbourBlock == goalBlock):
                    self.path.append(neighbourBlock)
                    prevID = self.backtrack.get(q.id)
                    #prevID = q.prevBlockID
                    while (prevID != 0):
                        prevBlock = paths.GetBlockByID(prevID)
                        self.path.append(prevBlock)
                        prevID = self.backtrack.get(prevBlock.id)
                        #prevID = prevBlock.prevBlockID
                    return self.path
                if (neighbourBlock.id % 100 != q.id % 100 and neighbourBlock.id / 100 != q.id / 100):
                    #neighbourBlock.g = 1.4
                    # Byt till denna undre rad för fullständig A*
                    neighbourBlock.g = q.g + 1.4
                    # add support for different ms on tiles
                else:
                    #neighbourBlock.g = 1
                    # Byt till denna undre rad för fullständig A*
                    neighbourBlock.g = q.g + 1
                neighbourBlock.h = self.Euclidean(neighbourID, goalBlock)
                neighbourBlock.f = neighbourBlock.g + neighbourBlock.h
                for i in openList:
                    if (i.id == neighbourBlock.id and neighbourBlock.f >= i.f):
                        skip = True
                for i in closedList:
                    if (i.id == neighbourBlock.id and neighbourBlock.f >= i.f):
                        skip = True
                if neighbourBlock.isFogged:
                    skip = True
                if skip is False:
                    # set q as parent to all neighbour blocks
                    self.backtrack[neighbourBlock.id] = q.id
                    #neighbourBlock.prevBlockID = q.id
                    openList.append(neighbourBlock)
            closedList.append(q)
            # gui.Clear()
            # gui.DrawAStar(openList, closedList)
            # gui.Update()
            # time.sleep(0.01)

    def Euclidean(self, currentID, goal):
        xCur = currentID % 100
        yCur = currentID / 100
        # Converting ID to coordinates
        xGoal = goal.id % 100
        yGoal = goal.id / 100

        h = math.sqrt((xCur - xGoal) ** 2 + (yCur - yGoal) ** 2)
        return h


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
