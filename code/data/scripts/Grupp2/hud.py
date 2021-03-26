from Grupp2 import overlord
import imgui

def DrawHUD():

    imgui.Begin("Grupp2 (Red) Inventory", None, 0)
    imgui.Text("Agents: " + str(len(overlord.overlord.agents)))
    imgui.Text("Buildings: " + str(len(overlord.overlord.buildings)))
    imgui.Text("")
    imgui.Text("Agents: ")
    imgui.Text("Scout: " + str(overlord.overlord.nrDisc))
    imgui.Text("Soldier: "+ str(len(overlord.overlord.soldiers)))
    imgui.Text("Builder: " + str(overlord.overlord.nrBuild))
    imgui.Text("Kilners: " + str(overlord.overlord.nrKiln))
    imgui.Text("Idle Kilners: " + str(overlord.overlord.nrIdleKilners))
    imgui.Text("")
    imgui.Text("Resurser: ")
    imgui.Text("Charcoal: " + str(overlord.overlord.charcoal))
    imgui.Text("Ironbar: " + str(overlord.overlord.ironbar))
    imgui.Text("Ironore: " + str(overlord.overlord.ironore))
    imgui.Text("Sword: " + str(overlord.overlord.sword))
    imgui.Text("Tree: " + str(overlord.overlord.tree))
    imgui.End()











