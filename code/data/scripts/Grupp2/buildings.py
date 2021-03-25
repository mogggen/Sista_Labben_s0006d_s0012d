import demo, statParser, buildings
from Grupp2 import overlord

class Building:
    def __init__(self, type, builder ):
        self.type = type
        self.timer = 0 * demo.GetFrameTime()

        demo.spawnBuilding(self.type,builder.posX,builder.posY,0,demo.teamEnum.GRUPP_2)

    def Run(self):
        if demo.hasWorker:
            if self.timer <= 0:
                self.Produce(self)
                self.Start()
            else:
                self.timer -= 1 * demo.GetFrameTime()

    def Produce(self):
        if self.type == demo.buildingType.KILN:
            overlord.overlord.AddCharcoal(statParser.getStat("coalReturn"))
        elif self.type == demo.buildingType.BLACKSMITH:
            overlord.overlord.Addsword(statParser.getStat("ironReturn"))
        elif self.type == demo.buildingType.SMELTERY:
            overlord.overlord.Addironbar(statParser.getStat("swordReturn"))
        elif self.type == demo.buildingType.TRAININGCAMP:
            overlord.overlord.Addsoldiers()

    def Start(self):
        if self.type == demo.buildingType.KILN:
            if overlord.overlord.tree >= statParser.getStat("coalWoodCost"):
                overlord.overlord.Taketree(statParser.getStat("coalWoodCost"))
                self.timer = statParser.getStat("coalTimeCost") * demo.GetFrameTime()
        elif self.type == demo.buildingType.BLACKSMITH:
            if overlord.overlord.ironbar >= statParser.getStat("swordIronCost") and overlord.charcoal >= statParser.getStat("swordCoalCost"):
                self.timer = statParser.getStat("swordTimeCost") * demo.GetFrameTime()
        elif self.type == demo.buildingType.SMELTERY:
            if overlord.overlord.ironOre >= statParser.getStat("ironOreCost") and overlord.charcoal >= statParser.getStat("ironCoalcost"):
                self.timer = statParser.getStat("ironTimeCost") * demo.GetFrameTime()
       #traingcamp dose not restart   