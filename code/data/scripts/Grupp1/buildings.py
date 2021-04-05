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


    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.buildingEntity = buildings.spawnBuilding(demo.buildingType.TRAININGCAMP, self.x, self.y, 0, demo.teamEnum.GRUPP_1)
        self.paid = False
        entity_manager.instance.queueUpgrade(demo.agentType.SOLDIER)
        entity_manager.instance.queueUpgrade(demo.agentType.SOLDIER)

        self.hasStartedUpgrade = False


    def consumeAgent(self, agent):
        self.agent = agent

        agentProperty = self.agent.entity.Agent
        agentProperty.type = demo.agentType.SOLDIER
        self.agent.entity.Agent = agentProperty

        agentPropertyHealth = self.agent.entity.Health
        agentPropertyHealth.hp = int(statParser.getStat("soldierHealth"))
        self.agent.entity.Health = agentPropertyHealth


        entity_manager.instance.stageForUpgrade(self.agent.entity)

        self.hasStartedUpgrade = True

        self.paid = False


    def update(self):
        if self.buildingEntity.Building.hasWorker and self.hasStartedUpgrade:
            if not self.paid:
                if item_manager.instance.swords > 0:
                    self.timer = demo.GetTime()
                    self.removeProductCost()
                    self.paid = True
            elif demo.GetTime() - self.timer >= statParser.getStat("soldierUpgradeTime"):
                entity_manager.instance.doneUpgrade(self.agent.entity)
                self.agent = None

                buildingProperty = self.buildingEntity.Building
                buildingProperty.hasWorker = False
                self.buildingEntity.Building = buildingProperty
                self.hasStartedUpgrade = False
                self.paid = False

                entity_manager.instance.queueUpgrade(demo.agentType.SOLDIER)

    def removeProductCost(self):
        item_manager.instance.swords -= statParser.getStat("soldierSwordCost")
