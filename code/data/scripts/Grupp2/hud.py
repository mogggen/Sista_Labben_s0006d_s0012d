from Grupp2 import overlord
import imgui,demo


def DrawHUD():
    builders = 0
    scouts = 0
    dScouts =0
    soldiers = 0
    nonworker = 0

    kilns = 0
    smelterys = 0
    blacksmiths = 0
    trainingcamps = 0
    for a in overlord.overlord.agents:
        if a.entityHandle.Agent.type == demo.agentType.BUILDER:
            builders += 1
        elif a.entityHandle.Agent.type == demo.agentType.SCOUT:
            scouts += 1
        elif a.entityHandle.Agent.type == demo.agentType.SOLDIER:
            soldiers += 1
        elif a.entityHandle.Agent.position == overlord.overlord.castleEntity.Building.position:
            nonworker += 1
    for b in overlord.overlord.buildings:
        if b.entityHandle.Building.type == demo.buildingType.KILN:
            kilns += 1
        elif b.entityHandle.Building.type == demo.buildingType.SMELTERY:
            smelterys += 1
        elif b.entityHandle.Building.type == demo.buildingType.BLACKSMITH:
            blacksmiths += 1
        elif b.entityHandle.Building.type == demo.buildingType.TRAININGCAMP:
            trainingcamps += 1
        else:
            pass
    imgui.Begin("Grupp2 (Red) Inventory", None, 0)
    try:
        imgui.Text("Resources: ")
        imgui.Text("Tree: " + str(overlord.overlord.tree))
        imgui.Text("Charcoal: " + str(overlord.overlord.charcoal))
        imgui.Text("Ironbar: " + str(overlord.overlord.ironbar))
        imgui.Text("Ironore: " + str(overlord.overlord.ironore))
        imgui.Text("Sword: " + str(overlord.overlord.sword))
        imgui.Text("  ")
        imgui.Text("  ")
        imgui.Text("Builders: " + str(builders))
        imgui.Text("Available Builders: " + str(len(overlord.overlord.availableBuilders)))
        imgui.Text("Scouts: " + str(scouts))
        imgui.Text("Soldiers: " + str(soldiers))
        imgui.Text("non workers: " + str(nonworker))
        imgui.Text("  ")
        imgui.Text("  ")
        imgui.Text("Total buildings: " + str(len(overlord.overlord.buildings)))
        imgui.Text("KILN: " + str(kilns))
        imgui.Text("SMELTERY: " + str(smelterys))
        imgui.Text("BLACKSMITH: " + str(blacksmiths))
        imgui.Text("TRAININGCAMP: " + str(trainingcamps))
        imgui.End()
    except Exception as e:
        imgui.End()
        raise e
