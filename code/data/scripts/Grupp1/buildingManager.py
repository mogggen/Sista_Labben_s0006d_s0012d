from Grupp1 import item_manager, entity_manager
import statParser, buildings
import demo

class kiln:
    working = False

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.buildingEntity = spawnBuilding(demo.buildingType.kiln, self.x, self.y, 0, demo.teamEnum.GRUPP_1)


    def consumeAgent(self, agent):
        self.agent = agent.entity.Agent
        agent.entity.Agent.RemoveFromSystem()
        self.buildingEntity.hasWorker = True


    def update(self):
        if self.buildingEntity.hasWorker:
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
        self.buildingEntity = spawnBuilding(demo.buildingType.kiln, self.x, self.y, 0, demo.teamEnum.GRUPP_1)


    def consumeAgent(self, agent):
        self.agent = agent.entity.Agent
        agent.entity.Agent.RemoveFromSystem()
        self.buildingEntity.hasWorker = True

    def update(self):
        if self.buildingEntity.hasWorker:
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
        self.buildingEntity = spawnBuilding(demo.buildingType.kiln, self.x, self.y, 0, demo.teamEnum.GRUPP_1)


    def consumeAgent(self, agent):
        self.agent = agent.entity.Agent
        agent.entity.Agent.RemoveFromSystem()
        self.buildingEntity.hasWorker = True

    def update(self):
        if self.buildingEntity.hasWorker:
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
        self.buildingEntity = spawnBuilding(demo.buildingType.kiln, self.x, self.y, 0, demo.teamEnum.GRUPP_1)


    def consumeAgent(self, agent):
        self.agent = agent.entity.Agent
        agent.entity.Agent.RemoveFromSystem()
        self.buildingEntity.hasWorker = True

    def update(self):
        if self.buildingEntity.hasWorker:
            if not self.working:
                self.timer = demo.GetTime()
                self.removeProductCost()
                working = True
            else:
                if demo.GetTime() - self.timer >= statParser.getStat("soldierUpgradeTime"):
                    self.agent.entity.Agent.addToSystem()
                    self.agent = None
                    working = False

    def removeProductCost(self):
        item_manager.instance.logs -= statParser.getStat("soldierSwordCost")
