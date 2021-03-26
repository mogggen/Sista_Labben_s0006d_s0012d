from Grupp1 import item_manager, explorerManager, entity_manager, agent, goals, build_manager, worker_manager, soldierManager
import statParser
import demo, imgui

start_phase4 = 0

def addScout(worker):
    entity_manager.instance.stageForUpgrade(worker)
    entity_manager.instance.findAgent(worker).addGoal(goals.Upgrade(demo.agentType.SCOUT))

def addBuilder(worker):
    entity_manager.instance.stageForUpgrade(worker)
    entity_manager.instance.findAgent(worker).addGoal(goals.Upgrade(demo.agentType.BUILDER))

def addKilner(worker):
    entity_manager.instance.stageForUpgrade(worker)
    entity_manager.instance.findAgent(worker).addGoal(goals.Upgrade(demo.agentType.KILNER))

def addSmelter(worker):
    entity_manager.instance.stageForUpgrade(worker)
    entity_manager.instance.findAgent(worker).addGoal(goals.Upgrade(demo.agentType.SMELTER))

def addBlacksmith(worker):
    entity_manager.instance.stageForUpgrade(worker)
    entity_manager.instance.findAgent(worker).addGoal(goals.Upgrade(demo.agentType.BLACKSMITH))

def addSoldier(worker):
    pass

def phase1_1():
    entity_manager.instance.queueUpgrade(demo.agentType.SCOUT)
    entity_manager.instance.queueUpgrade(demo.agentType.SCOUT)
    entity_manager.instance.queueUpgrade(demo.agentType.BUILDER)
    entity_manager.instance.queueUpgrade(demo.agentType.BUILDER)
    build_manager.placing(demo.buildingType.KILN)
    build_manager.placing(demo.buildingType.KILN)

    worker_manager.instance.tree_focus = 1


    return True


def phase1_2():
    if len(entity_manager.instance.buildings) >= 2:
        worker_manager.instance.tree_focus = 0.8
        return True


def phase2_1():
    build_manager.placing(demo.buildingType.SMELTERY)
    return True


def phase2_2():
    if len(entity_manager.instance.buildings) >= 3 :
        build_manager.placing(demo.buildingType.TRAININGCAMP)
        build_manager.placing(demo.buildingType.TRAININGCAMP)
        build_manager.placing(demo.buildingType.BLACKSMITH)
        build_manager.placing(demo.buildingType.KILN)

        return True
        


def phase3_1():
    global start_phase4
    if len(entity_manager.instance.buildings) >= 6 :
        build_manager.placing(demo.buildingType.KILN)
        build_manager.placing(demo.buildingType.KILN)
        start_phase4 = demo.GetTime()
        return True


def phase4_1():
    n_guys = len(entity_manager.instance.upgrading) + \
             len(entity_manager.instance.workers) + \
             len(entity_manager.instance.craftsmen) + \
             len(entity_manager.instance.explorers) + \
             len(entity_manager.instance.builders) + \
             len(entity_manager.instance.soldiers)

    if len(entity_manager.instance.soldiers) > 20 or n_guys <= 26:
        soldierManager.launchAssult()
        return True

def phase5_1():
    if item_manager.instance.ironore + item_manager.instance.ironIngot * 2 > 50:
        worker_manager.instance.tree_focus = 0.9
        return True


phases = [
    [phase1_1, phase1_2],
    [phase2_1, phase2_2],
    [phase3_1],
    [phase4_1],
    [phase5_1],
]

def update():
    global phases

    if len(phases) <= 0:
        return

    for phase in phases[0]:
        if phase():
            phases[0].remove(phase)

    if len(phases[0]) <= 0:
        phases.pop(0)

def dbgDraw():
     
    imgui.Begin("phase", None, 0)

    try:
        imgui.Text(str(phases))

        if start_phase4 > 0:
            imgui.Text(str(demo.GetTime() - start_phase4))
        imgui.End()

    except Exception as e:
        imgui.End()
        raise e
