from Grupp1 import item_manager, entity_manager
import statParser, buildings
import demo

class kiln:
    working = False

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.buildingEntity = buildings.spawnBuilding(demo.buildingType.KILN, self.x, self.y, 0, demo.teamEnum.GRUPP_1)


    def consumeAgent(self, agent):
        self.agent = agent
        entity_manager.instance.deleteEntity(self.agent.entity)
        buildingProperty = self.buildingEntity.Building
        buildingProperty.hasWorker = True
        self.buildingEntity.Building = buildingProperty


    def update(self):
        if self.buildingEntity.Building.hasWorker:
            if not self.working:
                self.timer = demo.GetTime()
                self.working = self.removeProductCost()
            else:
                if demo.GetTime() - self.timer >= statParser.getStat("coalTimeCost"):
                    item_manager.instance.coal += statParser.getStat("coalReturn")
                    self.working = False


    def removeProductCost(self):
        coalWoodCost = statParser.getStat("coalWoodCost")
        if item_manager.instance.logs >= coalWoodCost:
            item_manager.instance.logs -= coalWoodCost
            return True
        return False


class smelter:
    working = False

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.buildingEntity = buildings.spawnBuilding(demo.buildingType.SMELTERY, self.x, self.y, 0, demo.teamEnum.GRUPP_1)


    def consumeAgent(self, agent):
        self.agent = agent
        entity_manager.instance.deleteEntity(self.agent.entity)
        buildingProperty = self.buildingEntity.Building
        buildingProperty.hasWorker = True
        self.buildingEntity.Building = buildingProperty

    def update(self):
        if self.buildingEntity.Building.hasWorker:
            if not self.working:
                self.timer = demo.GetTime()
                self.working = self.removeProductCost()
            else:
                if demo.GetTime() - self.timer >= statParser.getStat("ironTimeCost"):
                    item_manager.instance.ironIngot += statParser.getStat("ironReturn")
                    self.working = False

    def removeProductCost(self):
        ironCoalCost = statParser.getStat("ironCoalCost")
        ironOreCost = statParser.getStat("ironOreCost")

        if item_manager.instance.coal >= ironCoalCost and item_manager.instance.ironore >= ironOreCost:
            item_manager.instance.coal -= ironCoalCost
            item_manager.instance.ironore -= ironOreCost
            return True
        return False


class blacksmith:
    working = False

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.buildingEntity = buildings.spawnBuilding(demo.buildingType.BLACKSMITH, self.x, self.y, 0, demo.teamEnum.GRUPP_1)


    def consumeAgent(self, agent):
        self.agent = agent
        entity_manager.instance.deleteEntity(self.agent.entity)
        buildingProperty = self.buildingEntity.Building
        buildingProperty.hasWorker = True
        self.buildingEntity.Building = buildingProperty

    def update(self):
        if self.buildingEntity.Building.hasWorker:
            if not self.working:
                self.timer = demo.GetTime()
                self.working = self.removeProductCost()
            else:
                if demo.GetTime() - self.timer >= statParser.getStat("swordTimeCost"):
                    item_manager.instance.swords += statParser.getStat("swordReturn")
                    self.working = False

    def removeProductCost(self):
        swordCoalCost = statParser.getStat("swordCoalCost")
        swordIronCost = statParser.getStat("swordIronCost")

        if item_manager.instance.coal >= swordCoalCost and item_manager.instance.ironIngot >= swordIronCost:
            item_manager.instance.coal -= swordCoalCost
            item_manager.instance.ironIngot -= swordIronCost
            return True
        return False


class trainingCamp:
    working = False

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.buildingEntity = buildings.spawnBuilding(demo.buildingType.TRAININGCAMP, self.x, self.y, 0, demo.teamEnum.GRUPP_1)


    def consumeAgent(self, agent):
        self.agent = agent

        agentProperty = self.agent.entity.Agent
        agentProperty.type = demo.agentType.SOLDIER

        agentPropertyHealth = agent.entity.Health
        agentPropertyHealth.hp = int(statParser.getStat("soldierHealth"))
        agent.entity.Health = agentPropertyHealth

        self.agent.entity.Agent = agentProperty

        entity_manager.instance.stageForUpgrade(self.agent.entity)

        buildingProperty = self.buildingEntity.Building
        buildingProperty.hasWorker = True
        self.buildingEntity.Building = buildingProperty


    def update(self):
        if self.buildingEntity.Building.hasWorker:
            if not self.working:
                self.timer = demo.GetTime()
                self.removeProductCost()
                self.working = True
            else:
                if demo.GetTime() - self.timer >= statParser.getStat("soldierUpgradeTime"):
                    entity_manager.instance.doneUpgrade(self.agent.entity)
                    entity_manager.instance.queueUpgrade(demo.agentType.SOLDIER)
                    self.agent = None
                    self.working = False

                    buildingProperty = self.buildingEntity.Building
                    buildingProperty.hasWorker = False
                    self.buildingEntity.Building = buildingProperty

    def removeProductCost(self):
        soldierSwordCost = statParser.getStat("soldierSwordCost")
        if item_manager.instance.swords >= soldierSwordCost:
            item_manager.instance.swords -= soldierSwordCost
            return True
        return False
