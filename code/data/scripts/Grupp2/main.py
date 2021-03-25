import nmath, hud
import buildings as cbuildings
from Grupp2 import buildings, pathfinder, overlord

overlord.overlord.castleEntity = cbuildings.initRedCastle()
pathfinder.pf.AStar(nmath.Point(0,0,0), nmath.Point(-20,0,-60))
#overlord.overlord.SpawnAgent()

def NebulaUpdate():
    pass

def NebulaDraw(p):
    pathfinder.pf.DrawAStar()
    hud.Nebula_Draw()
    pass

def HandleMessage(msg):
    overlord.overlord.HandleMsg(msg)