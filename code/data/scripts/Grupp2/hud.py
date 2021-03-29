from Grupp2 import overlord
import imgui


def DrawHUD():
    imgui.Begin("Grupp2 (Red) Inventory", None, 0)
    imgui.Text("Agents: " + str(len(overlord.overlord.agents)))
    imgui.Text("Buildings: " + str(len(overlord.overlord.buildings)))
    imgui.Text("")
    imgui.Text("Soldier: " + str(len(overlord.overlord.soldiers)))
    imgui.Text("")
    imgui.Text("Resurser: ")
    imgui.Text("Tree: " + str(overlord.overlord.tree))
    imgui.Text("Charcoal: " + str(overlord.overlord.charcoal))
    imgui.Text("Ironbar: " + str(overlord.overlord.ironbar))
    imgui.Text("Ironore: " + str(overlord.overlord.ironore))
    imgui.Text("Sword: " + str(overlord.overlord.sword))
    imgui.End()
