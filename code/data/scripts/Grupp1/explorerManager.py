from Grupp1 import entity_manager, goals, agent
import navMesh
import nmath, demo
import random

startupGoals = [
            [goals.WalkToGoal(nmath.Float2(0, -170))],
            [goals.WalkToGoal(nmath.Float2(0, 170)), goals.WalkToGoal(nmath.Float2(-125, -20)), goals.WalkToGoal(nmath.Float2(140, -20))]
        ]

def startup():
    for i in range(2):
        worker = demo.Entity.fromInt(list(entity_manager.instance.workers.keys())[0])
        entity_manager.instance.stageForUpgrade(worker)
        entity_manager.instance.findAgent(worker).addGoal(goals.Upgrade(demo.agentType.SCOUT))

def update():
    if len(entity_manager.instance.explorers) > 0:
        for scout in entity_manager.instance.explorers.values():
            if scout.isFree():
                if startupGoals:
                    scout.addGoals(startupGoals.pop(0))

                else:
                    roam(scout)

def roam(scout):
    while True:
        offset = nmath.Float2(random.randrange(-25, 25), random.randrange(-25, 25))
        pos = scout.getPos() + offset
        if navMesh.isOnNavMesh(pos):
            scout.addGoal(goals.WalkToGoal(pos))
            break
