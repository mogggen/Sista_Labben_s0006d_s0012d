import nmath
import buildings as cbuildings
from Grupp2 import buildings, pathfinder, overlord, hud

overlord.overlord.castleEntity = cbuildings.initRedCastle()
pathfinder.pf.AStar(nmath.Point(0,0,0), nmath.Point(-20,0,-60))
overlord.overlord.SpawnAgent()

def NebulaUpdate():
    overlord.overlord.UpdateActors()
    pass

def NebulaDraw(p):
    pathfinder.pf.DrawAStar()
    hud.DrawHUD()
    pass

def HandleMessage(msg):
    overlord.overlord.HandleMsg(msg)