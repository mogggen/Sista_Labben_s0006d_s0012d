import nmath
import buildings as cbuildings
from Grupp2 import buildings, pathfinder, overlord, hud, EntityManager

overlord.overlord.castleEntity = cbuildings.initRedCastle()
overlord.overlord.SpawnAllAgents()
overlord.overlord.OperationKILL()

def NebulaUpdate():
    overlord.overlord.UpdateActors()
    EntityManager.entitymanger.updatetUnManageEntities()
    pass

def NebulaDraw(p):
    hud.DrawHUD()
    pass

def HandleMessage(msg):
    overlord.overlord.HandleMsg(msg)