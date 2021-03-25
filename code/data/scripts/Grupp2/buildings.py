import demo, statParser, buildings
from Grupp2 import overlord

class Building:
    def __init__(self, type, builder ):
        self.type = type
        self.startTime = 0
        self.working = False

        self.entityHandle = buildings.spawnBuilding(self.type,builder.posX,builder.posY,0,demo.teamEnum.GRUPP_2)

    def Run(self):
        if self.entityHandle.Building.hasWorker:
            if not self.working:
                self.Start()
            else:
                self.Execute()

    def Produce(self):
        if self.type == demo.buildingType.KILN:
            overlord.overlord.AddCharcoal(statParser.getStat("coalReturn"))
        elif self.type == demo.buildingType.BLACKSMITH:
            overlord.overlord.Addsword(statParser.getStat("ironReturn"))
        elif self.type == demo.buildingType.SMELTERY:
            overlord.overlord.Addironbar(statParser.getStat("swordReturn"))
        elif self.type == demo.buildingType.TRAININGCAMP:
            # We will handle soldier production on the agent side
            pass

    def Execute(self):
        if self.type == demo.buildingType.KILN:
            if demo.GetTime() - self.startTime >= statParser.getStat("coalTimeCost"):
                self.Produce()
        elif self.type == demo.buildingType.BLACKSMITH:
            if demo.GetTime() - self.startTime >= statParser.getStat("swordTimeCost"):
                self.Produce()
        elif self.type == demo.buildingType.SMELTERY:
            if demo.GetTime() - self.startTime >= statParser.getStat("ironTimeCost"):
                self.Produce()

    def Start(self):
        if self.type == demo.buildingType.KILN:
            if overlord.overlord.tree >= statParser.getStat("coalWoodCost"):
                overlord.overlord.Taketree(statParser.getStat("coalWoodCost"))
                self.startTime = demo.GetTime()
                self.working = True
        elif self.type == demo.buildingType.BLACKSMITH:
            if overlord.overlord.ironbar >= statParser.getStat("swordIronCost") and overlord.charcoal >= statParser.getStat("swordCoalCost"):
                overlord.overlord.Takeironbar(statParser.getStat("swordIronCost"))
                overlord.overlord.Takecharcoal(statParser.getStat("swordCoalCost"))
                self.startTime = demo.GetTime()
                self.working = True
        elif self.type == demo.buildingType.SMELTERY:
            if overlord.overlord.ironOre >= statParser.getStat("ironOreCost") and overlord.charcoal >= statParser.getStat("ironCoalCost"):
                overlord.overlord.Takeironore(statParser.getStat("ironOreCost"))
                overlord.overlord.Takecharcoal(statParser.getStat("ironCoalCost"))
                self.startTime = demo.GetTime()
                self.working = True

    def AddWorker(self):
        buildingProperty = self.entityHandle.Building
        buildingProperty.hasWorker = True
        self.entityHandle.Building = buildingProperty
