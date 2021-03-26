from Grupp1 import entity_manager, goals, agent
import navMesh
import nmath, demo
import random

startupGoals = [
            [goals.WalkToGoal(nmath.Float2(0, -170))],
            [goals.WalkToGoal(nmath.Float2(0, 170)), goals.WalkToGoal(nmath.Float2(-125, -20)), goals.WalkToGoal(nmath.Float2(140, -20))]
        ]

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
