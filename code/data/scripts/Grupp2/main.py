import buildings, pathfinder, nmath, overlord

buildings.initRedCastle()
pathfinder.pf.AStar(nmath.Point(0,0,0), nmath.Point(50,0,0))
def NebulaUpdate():
    pass

def NebulaDraw(p):
    pathfinder.pf.DrawAStar()

def HandleMessage(msg):
    for n in overlord.agents:
        if n == msg.taker:
           return #n Take damege
