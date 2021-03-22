import random as R
import navMesh
import demo
import math
import nmath

def stuff(p):
    for f in range(navMesh.getNumFace()):
        if navMesh.isInTriangle(p, f):
            return True
    return False

### distribution of resources occurs at a decending radius from the castles.
def placeTrees(CastleA, CastleB, n=600):
    
    r = ((CastleA[0] - CastleB[0])**2 + (CastleA[1] - CastleB[1])**2)**.5
    
    # divide the radious with mapped steps
    index = n
    while index >= 100:
        while True:
            theta = R.uniform(-math.pi, math.pi) # theta only works for positive ratios eller nåt

            pA = CastleA[0] + r * index / n * math.cos(theta), CastleA[1] + r * index / n * math.sin(theta)
            pA = nmath.Float2(pA[0], pA[1])

            pB = CastleB[0] + r * index / n * -math.cos(theta), CastleB[1] + r * index / n * -math.sin(theta)
            pB = nmath.Float2(pB[0], pB[1])

            if navMesh.isOnNavMesh(pA) and navMesh.isOnNavMesh(pB):
                break
        index -= 1

        entityHandle = demo.SpawnEntity("AgentEntity/agent")
        agent = entityHandle.Agent
        agent.position = nmath.Point(pA.x, 0, pA.y)
        entityHandle.Agent = agent

        entityHandle = demo.SpawnEntity("AgentEntity/agent")
        agent = entityHandle.Agent
        agent.position = nmath.Point(pB.x, 0, pB.y)
        entityHandle.Agent = agent
    