from Grupp2 import overlord
import imgui,demo


def DrawHUD():
    builders = 0
    for a in overlord.overlord.agents:
        if a.entityHandle.Agent.type == demo.agentType.BUILDER:
            builders +=1

    imgui.Begin("Grupp2 (Red) Inventory", None, 0)
    try:
        imgui.Text("Resorses: ")
        imgui.Text("Tree: " + str(overlord.overlord.tree))
        imgui.Text("Charcoal: " + str(overlord.overlord.charcoal))
        imgui.Text("Ironbar: " + str(overlord.overlord.ironbar))
        imgui.Text("Ironore: " + str(overlord.overlord.ironore))
        imgui.Text("Sword: " + str(overlord.overlord.sword))
        imgui.Text("  ")
        imgui.Text("  ")
        imgui.Text("Builders: "+ str(builders))
        imgui.End()
    except Exception as e:
        imgui.End()
        raise e
