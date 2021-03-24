from Grupp2 import overlord

class Building:
    def __init__(self, type, block):
        self.type = type
        self.block = block

    def BurnWood(self):
        if self.type is not enums.BuildingType.KILN_BUILDING:
            print("This building is not a kiln!!!")
            return
        if self.block.hasWood is False:
            print("This block is out of wood!!!")

        self.block.TakeWood()
        self.block.TakeWood()
        overlord.overlord.AddCharcoal()