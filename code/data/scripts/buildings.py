import demo
import nmath
import statParser
import math


def spawnBuilding(type:demo.buildingType, x, y, rot, team:demo.teamEnum):
    if team == demo.teamEnum.GRUPP_2:
        entityHandle = demo.SpawnEntity("RedBuildingEntity/" + str(type).split(".")[1].lower())
    else:
        entityHandle = demo.SpawnEntity("BlueBuildingEntity/" + str(type).split(".")[1].lower())

    building = entityHandle.Building
    building.position = nmath.Point(x, 0, y)
    entityHandle.Building = building
    entityHandle.WorldTransform = nmath.Mat4.rotation_y(rot) * nmath.Mat4.translation(x, 0, y)

    p_team = entityHandle.Team
    p_team.team = team
    entityHandle.Team = p_team

    health = entityHandle.Health
    health.hp = int(statParser.getStat(str(type).split(".")[1].lower() + "Health"))
    entityHandle.Health = health

    return entityHandle


def initBlueCastle():
    return spawnBuilding(demo.buildingType.CASTLE, 0, 170, 0, demo.teamEnum.GRUPP_1)

def initRedCastle():
    return spawnBuilding(demo.buildingType.CASTLE, 0, -170, math.pi, demo.teamEnum.GRUPP_2)


def setHasWorker(workstation, hasWorkerIn):
    building = workstation.building
    building.hasWorker = hasWorkerIn
    workstation.building = building
