import overlord, buildings
import demo, statParser

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
                self.timer -= 1 * frameTime

    def Produce(self):
        if self.type == demo.buildingType.KILN:
            overlord.AddCharcoal(statPaser.getStat("coalReturn"))
        elif self.type == demo.buildingType.BLACKSMITH:
            overlord.Addsword(statPaser.getStat("ironReturn"))
        elif self.type == demo.buildingType.SMELTERY:
            overlord.Addironbar(statPaser.getStat("swordReturn"))
        elif self.type == demo.buildingType.TRAININGCAMP:
            overlord.Addsoilders()

    def Start(self):
        if self.type == demo.buildingType.KILN:
            if overlord.tree >= statPaser.getStat("coalWoodCost"):
                overlord.Taketree(statPaser.getStat("coalWoodCost"))
                self.timer = statPaser.getStat("coalTimeCost") * demo.GetFrameTime()  
        elif self.type == demo.buildingType.BLACKSMITH:
            if overlord.ironebar >= statPaser.getStat("swordIronCost") and overlord.charcoal >= statPaser.getStat("swordCoalCost"):
                self.timer = tatPaser.getStat("swordTimeCost") * demo.GetFrameTime()  
        elif self.type == demo.buildingType.SMELTERY:
            if overlord.ironOre >= statPaser.getStat("ironOreCost") and overlord.charcoal >= statPaser.getStat("ironCoalcost"):
                self.timer = statPaser.getStat("ironTimeCost") * demo.GetFrameTime()  
       #traingcamp dose not restart   