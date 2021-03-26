from Grupp1 import item_manager, explorerManager, entity_manager, agent, goals, build_Manager
import statParser
import demo

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
    for i in range(5):
        worker = demo.Entity.fromInt(list(entity_manager.instance.workers.keys())[0])
        if i <= 2:
            addScout(worker)
        elif i > 2 and i <= 4:
            addBuilder(worker)
        else:
            addKilner(worker)

    if item_manager.logs >= statParser.getStat("kilnWoodCost"):
        build_Manager.addToBuildList()


def phase1_2():
    if item_manager.logs <= 100:
        workers.focusTrees()


def phase2_1():
    if item_manager.logs <= 100:
        workers.focusTrees()


def phase2_2():
    if item_manager.logs <= 100:
        workers.focusTrees()


def phase3_1():
    if item_manager.logs <= 100:
        workers.focusTrees()


def phase3_2():
    if item_manager.logs <= 100:
        workers.focusTrees()


phases = [
    [phase1_1(), phase1_2()],
    [phase2_1(), phase2_2()],
    [phase3_1(), phase3_2()],
]

def update():
    global phases
    for phase in phases[0]:
        if phase():
            phases[0].remove(phase)

    phases.pop(0)
