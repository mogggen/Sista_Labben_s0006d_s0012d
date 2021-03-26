from Grupp1 import buildings, entity_manager, goals, item_manager
import navMesh, demo, random, nmath
import buildings as common_buildings
import statParser

radX = 30
maxRadZ = 160
minRadZ = 125
distFromHouseRad = 5

building_queue = []

def canBuild(type):

    woodCost = statParser.getStat(str(type).split(".")[1].lower() + "WoodCost")
    if item_manager.instance.logs >= woodCost:
        if type in (demo.buildingType.KILN, demo.buildingType.SMELTERY, demo.buildingType.TRAININGCAMP):
            item_manager.instance.logs -= woodCost
            return True

        ironCost = statParser.getStat("blacksmithIronCost")
        if type == demo.buildingType.BLACKSMITH and item_manager.instance.ironIngot >= ironCost:
            item_manager.instance.logs -= woodCost
            item_manager.instance.ironIngot -= ironCost
            return True

        return False

def update():
    for builder in entity_manager.instance.builders.values():
        if builder.isFree():
            if len(building_queue) <= 0:
                break

            if canBuild(building_queue[0][0]):
                type,pos = building_queue.pop(0)
                builder.addGoals([goals.Build(type, pos), goals.WalkToGoal(pos)])

                if type == demo.buildingType.TRAININGCAMP:
                    entity_manager.instance.queueUpgrade(demo.agentType.SOLDIER)

                break


    for building in entity_manager.instance.buildings.values():
        if not building.buildingEntity.Building.hasWorker:
            for craftsmen in entity_manager.instance.craftsmen.values():
                if craftsmen.entity.Agent.type == demo.agentType.KILNER and building.buildingEntity.Building.type == demo.buildingType.KILN:
                    craftsmen.addGoal(goals.EnterBuilding(building.buildingEntity))
                    break;
                elif craftsmen.entity.Agent.type == demo.agentType.SMELTER and building.buildingEntity.Building.type == demo.buildingType.SMELTERY:
                    craftsmen.addGoal(goals.EnterBuilding(building.buildingEntity))
                    break;
                elif craftsmen.entity.Agent.type == demo.agentType.SMITH and building.buildingEntity.Building.type == demo.buildingType.BLACKSMITH:
                    craftsmen.addGoal(goals.EnterBuilding(building.buildingEntity))
                    break;

def placing(type:demo.buildingType):
    maxZ = maxRadZ
    minZ = minRadZ
    maxX = entity_manager.instance.getCastlePos().x + radX
    minX = entity_manager.instance.getCastlePos().x - radX

    while True:
        x = random.randrange(minX, maxX)
        z = random.randrange(minZ, maxZ)
        point = nmath.Float2(x, z)
        if navMesh.isOnNavMesh(point):
            for b in entity_manager.instance.buildings.values():
                p = b.buildingEntity.Building.position
                if (point - nmath.Float2(p.x, p.z)).length() < distFromHouseRad:
                    break

            else:

                building_queue.append((type, point))

                if type == demo.buildingType.KILN:
                    entity_manager.instance.queueUpgrade(demo.agentType.KILNER)
                elif type == demo.buildingType.SMELTERY:
                    entity_manager.instance.queueUpgrade(demo.agentType.SMELTER)
                elif type == demo.buildingType.BLACKSMITH:
                    entity_manager.instance.queueUpgrade(demo.agentType.SMITH)
                return




