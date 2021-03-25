from Grupp1 import entity_manager, goals, agent
import navMesh
import nmath
import random

startupGoals = [
            [goals.WalkToGoal(entity_manager.EntityManager.getCastlePos())],
            [goals.WalkToGoal(nmath.float2(-125, -20)), goals.WalkToGoal(nmath.float2(140, -20))]
        ]

def startup():
    Agent.addGoal(goals.Upgrade(Agent.agentType.SCOUT))
    Agent.addGoal(goals.Upgrade(Agent.agentType.SCOUT))

def Update():
    if len(entity_manager.EntityManager.explorers) > 0:
        for scout in entity_manager.EntityManager.explorers:
            if agent.Agent.availible(scout):
                if startupGoals:
                    scout.addGoals(startupGoals[0])
                    startupGoals.pop(0)

                else:
                    roam(scout)

def roam(scout):
    while true:
        offset = nmath.float2(random.randrange(-25, 25), random.randrange(-50, 50))
        pos = nmath.float2(scout.position + offset)
        if navMesh.isOnNavMesh(pos):
            scout.addGoal(goals.WalkToGoal(pos))
            break
