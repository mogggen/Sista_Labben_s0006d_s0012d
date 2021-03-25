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
        self.agent = agent.entity.Agent
        entity_manager.instance.removeEntity(self.agent.entity)
        buildingProperty = self.buildingEntity.Building
        buildingProperty.hasWorker = True
        self.buildingEntity.Building = buildingProperty


    def update(self):
        if self.buildingEntity.Building.hasWorker:
            if not self.working:
                self.timer = demo.GetTime()
                self.removeProductCost()
                working = True
            else:
                if demo.GetTime() - self.timer >= statParser.getStat("coalTimeCost"):
                    item_manager.instance.coal += statParser.getStat("coalReturn")
                    working = False


    def removeProductCost(self):
        item_manager.instance.logs -= statParser.getStat("coalWoodCost")


class smelter:
    working = False

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.buildingEntity = buildings.spawnBuilding(demo.buildingType.SMELTERY, self.x, self.y, 0, demo.teamEnum.GRUPP_1)


    def consumeAgent(self, agent):
        self.agent = agent.entity.Agent
        entity_manager.instance.removeEntity(self.agent.entity)
        buildingProperty = self.buildingEntity.Building
        buildingProperty.hasWorker = True
        self.buildingEntity.Building = buildingProperty

    def update(self):
        if self.buildingEntity.Building.hasWorker:
            if not self.working:
                self.timer = demo.GetTime()
                self.removeProductCost()
                working = True
            else:
                if demo.GetTime() - self.timer >= statParser.getStat("ironTimeCost"):
                    item_manager.instance.iron += statParser.getStat("ironReturn")
                    working = False

    def removeProductCost(self):
        item_manager.instance.coal -= statParser.getStat("ironCoalCost")
        item_manager.instance.ironore -= statParser.getStat("ironOreCost")


class blacksmith:
    working = False

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.buildingEntity = buildings.spawnBuilding(demo.buildingType.BLACKSMITH, self.x, self.y, 0, demo.teamEnum.GRUPP_1)


    def consumeAgent(self, agent):
        self.agent = agent.entity.Agent
        entity_manager.instance.removeEntity(self.agent.entity)
        buildingProperty = self.buildingEntity.Building
        buildingProperty.hasWorker = True
        self.buildingEntity.Building = buildingProperty

    def update(self):
        if self.buildingEntity.Building.hasWorker:
            if not self.working:
                self.timer = demo.GetTime()
                self.removeProductCost()
                working = True
            else:
                if demo.GetTime() - self.timer >= statParser.getStat("swordTimeCost"):
                    item_manager.instance.sword += statParser.getStat("swordReturn")
                    working = False

    def removeProductCost(self):
        item_manager.instance.coal -= statParser.getStat("swordCoalCost")
        item_manager.instance.iron -= statParser.getStat("swordIronCost")


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

        agentPropertyHealth = demo.Health
        agentPropertyHealth.hp = statParser.getStat("soldierHealth")
        demo.Health = agentPropertyHealth

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
                working = True
            else:
                if demo.GetTime() - self.timer >= statParser.getStat("soldierUpgradeTime"):
                    entity_manager.instance.doneUppgrading(self.agent.entity)
                    self.agent = None
                    working = False

                    buildingProperty = self.buildingEntity.Building
                    buildingProperty.hasWorker = False
                    self.buildingEntity.Building = buildingProperty

    def removeProductCost(self):
        item_manager.instance.sword -= statParser.getStat("soldierSwordCost")
