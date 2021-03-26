from Grupp1 import buildings, entity_manager, goals
import navMesh, demo, random, nmath
import buildings as common_buildings

radX = 21
maxRadZ = 150
minRadZ = 125
distFromHouseRad = 5

building_queue = []


def update():
    for builder in entity_manager.instance.builders.values():
        if builder.isFree():
            if len(building_queue) <= 0:
                break

            type,pos = building_queue.pop(0)
            builder.addGoal(goals.Build(type, pos))

def placing(type:demo.buildingType):
    maxZ = maxRadZ
    minZ = minRadZ
    maxX = entity_manager.instance.getCastlePos().x + radX
    minX = entity_manager.instance.getCastlePos().x - radX

    while True:
        x = random.randrange(minX, maxX)
        z = random.randrange(minZ, maxZ)
        print(x, z)
        point = nmath.Float2(x, z)
        if navMesh.isOnNavMesh(point):
            for b in entity_manager.instance.buildings.values():
                p = b.buildingEntity.Building.position
                if (point - nmath.Float2(p.x, p.z)).length() < distFromHouseRad:
                    break

            else:

                building_queue.append((type, point))
                common_buildings.spawnBuilding(type, point.x, point.y, 0, demo.teamEnum.GRUPP_1)
                return




