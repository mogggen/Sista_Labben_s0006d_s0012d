import buildings, pathfinder, nmath

buildings.initRedCastle()
pathfinder.pf.AStar(nmath.Point(0,0,0), nmath.Point(50,0,0))
def NebulaUpdate():
    print("grupp2")

def NebulaDraw():
    pathfinder.pf.DrawAStar()
