import random as R
import navMesh
import demo
import math
import nmath

### distribution of resources occurs at a decending radius from the castles.
def placeTemps(CastleA=(0, 170), CastleB=(0, -170), temp="tree"):
    
    r = ((CastleA[0] - CastleB[0])**2 + (CastleA[1] - CastleB[1])**2)**.5
    stops, steps = None, None
    # divide the radious with mapped steps
    if temp[-4:] == "tree":
        path = "TreeEntity/" + temp[-4:]
        stop = 100
        steps = 500 + stop
        index = steps
    else:
        path = "IronEntity/iron"
        steps = 60
        stop = 0
        index = steps
    while index >= stop:
        while True:
            theta = R.uniform(-math.pi, math.pi) # theta only works for positive ratios eller nåt

            pA = CastleA[0] + r * index / steps * math.cos(theta), CastleA[1] + r * index / steps * math.sin(theta)
            pA = nmath.Float2(pA[0], pA[1])

            pB = CastleB[0] + r * index / steps * -math.cos(theta), CastleB[1] + r * index / steps * -math.sin(theta)
            pB = nmath.Float2(pB[0], pB[1])

            if navMesh.isOnNavMesh(pA) and navMesh.isOnNavMesh(pB):
                break
        index -= 1

        if temp[-4:] == "tree":
            entityHandle = demo.SpawnEntity("TreeEntity/tree")
            entityHandle.WorldTransform = nmath.Mat4.translation(pA.x, 0, pA.y)
            properity = entityHandle.Tree
            properity.position = nmath.Point(pA.x, 0, pA.y)
            entityHandle.Tree = properity
            
            
            entityHandle = demo.SpawnEntity("TreeEntity/tree")
            entityHandle.WorldTransform = nmath.Mat4.translation(pB.x, 0, pB.y)
            properity = entityHandle.Tree
            properity.position = nmath.Point(pB.x, 0, pB.y)
            entityHandle.Tree = properity
        else:
            entityHandle = demo.SpawnEntity("IronEntity/iron")
            entityHandle.WorldTransform = nmath.Mat4.translation(pA.x, 0, pA.y)
            properity = entityHandle.Iron
            properity.position = nmath.Point(pA.x, 0, pA.y)
            entityHandle.Iron = properity
            
            entityHandle = demo.SpawnEntity("IronEntity/iron")
            entityHandle.WorldTransform = nmath.Mat4.translation(pB.x, 0, pB.y)
            properity = entityHandle.Iron
            properity.position = nmath.Point(pB.x, 0, pB.y)
            entityHandle.Iron = properity