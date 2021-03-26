import imgui

class ItemManager:
    logs      = 0
    coal      = 0
    ironore   = 0
    ironIngot = 0
    swords    = 0

    def drawGui(self):
        imgui.Begin("Grupp1 (Blue) Inventory", None, 0)
        
        members = [(attr, getattr(self,attr)) for attr in dir(self) if not callable(getattr(self,attr)) and not attr.startswith("__") and not attr == "path"]
        try:
            for member, value in members:
                imgui.Text(member + ": " + str(value))

            imgui.End()
        except Exception as e:
            imgui.End()
            raise e

instance = ItemManager()
