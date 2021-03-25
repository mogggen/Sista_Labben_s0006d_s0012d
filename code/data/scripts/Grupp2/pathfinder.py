import time, math, random, navMesh, demo, nmath
from Grupp2 import hud
path = []

class PathFinder:

    def AStar(self, agentPosition, goalPosition):
        goalFound = False
        visited = []
        global path
        path = []
        backtrack = {}
        ghfValues = {}  # key = face, value = (g, h, f)

        startFace = navMesh.findInNavMesh(nmath.Float2(agentPosition.x, agentPosition.z))
        ghfValues[startFace] = (0, 0, 0)
        goalFace = navMesh.findInNavMesh(nmath.Float2(goalPosition.x, goalPosition.z))
        if goalFace == -1:
            print("goalFace is -1")

        backtrack[startFace] = -1
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

                if (neighbourFace == goalFace):
                    path.append(neighbourFace)
                    path.append(q)
                    prevFace = backtrack.get(q)
                    while (prevFace != -1):
                        path.append(prevFace)
                        prevFace = backtrack.get(prevFace, -1)
                    return path

                g = ghfValues.get(q)[0] + 1 # g value addition should not be one but instead distance from this and previous center
                h = self.Euclidean(neighbourFace, goalFace)
                f = g + h
                ghf = (g, h, f)
                ghfValues[neighbourFace] = ghf

                for i in openList:
                    if i == neighbourFace and ghfValues.get(neighbourFace)[2] >= ghfValues.get(i)[2]:
                        skip = True
                for i in closedList:
                    if i == neighbourFace and ghfValues.get(neighbourFace)[2] >= ghfValues.get(i)[2]:
                        skip = True
                if skip is False:
                    # set q as parent to all neighbour blocks
                    backtrack[neighbourFace] = q
                    openList.append(neighbourFace)
            closedList.append(q)

    def Euclidean(self, currentFace, goalFace):
        # Getting Vector 3
        cPos = navMesh.getCenterOfFace(currentFace)
        gPos = navMesh.getCenterOfFace(goalFace)
        # Extracting just x and z
        xCur = cPos.x
        zCur = cPos.z
        xGoal = gPos.x
        zGoal = gPos.z

        h = math.sqrt((xCur - xGoal) ** 2 + (zCur - zGoal) ** 2)
        return h

    def GetNeighbouringFaces(self, face):
        neighbouringFaces = []
        h1 = navMesh.getHalfEdge(face)
        h2 = navMesh.getHalfEdge(h1.nextEdge)
        h3 = navMesh.getHalfEdge(h2.nextEdge)
        if h1.neighbourEdge != -1:
            n1 = navMesh.getHalfEdge(h1.neighbourEdge)
            f1 = navMesh.getFace(n1.face)
            neighbouringFaces.append(f1)

        if h2.neighbourEdge != -1:
            n2 = navMesh.getHalfEdge(h2.neighbourEdge)
            f2 = navMesh.getFace(n2.face)
            neighbouringFaces.append(f2)

        if h3.neighbourEdge != -1:
            n3 = navMesh.getHalfEdge(h3.neighbourEdge)
            f3 = navMesh.getFace(n3.face)
            neighbouringFaces.append(f3)

        return neighbouringFaces

    def DrawAStar(self):
        for i in range(len(path)-1):
            point = navMesh.getCenterOfFace(path[i])
            startPoint = point + nmath.Vector(0,3,0)
            point2 = navMesh.getCenterOfFace(path[i+1])
            endPoint = point2 + nmath.Vector(0,3,0)
            demo.DrawDot(startPoint, 8, nmath.Vec4(0, 1, 0, 1))
            demo.DrawDot(endPoint, 8, nmath.Vec4(0, 0, 1, 1))
            demo.DrawLine(startPoint, endPoint, 1, nmath.Vec4(1, 0, 0, 1))

pf = PathFinder()
