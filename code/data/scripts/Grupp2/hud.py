from Grupp2 import overlord

def Nebula_Draw():

    imgui.Begin("HUD", None, 0)
    imgui.Text("Agents: " + len(overlord.Overlord.agents))
    imgui.Text("Buildings: " + len(overlord.Overlord.buildings))
    imgui.Text("")
    imgui.Text("")
    imgui.Text("")
    imgui.Text("Agents: " + overlord.Overlord.nrDisc)
    imgui.Text("Scout: " + overlord.Overlord.nrDisc)
    imgui.Text("Soldier: "+ overlord.Overlord.soldier)
    imgui.Text("Builder: " + overlord.Overlord.nrBuild)
    imgui.Text("Kilners: " + overlord.Overlord.nrKiln)
    imgui.Text("Idle Kilners: " + overlord.Overlord.nrIdleKilners)
    imgui.Text("")
    imgui.Text("")
    imgui.Text("")
    imgui.Text("Resurser: " + reurser)
    imgui.Text("Charcoal: " + overlord.Overlord.charcoal)
    imgui.Text("Ironbar: " + overlord.Overlord.ironbar)
    imgui.Text("Ironore: " + overlord.Overlord.ironore)
    imgui.Text("Sword: " + overlord.Overlord.sword)
    imgui.Text("Tree: " + overlord.Overlord.tree)
    imgui.End()











