<<<<<<< HEAD
import Grupp1.path_manager as path_manager
import Grupp1.entity_manager as entity_manager
import Grupp1.agent as agent
import Grupp1.goals as goals

import nmath, demo
import button_input
import buildings

left_mouse   = button_input.ButtonInput(demo.IsLeftMouseDown)
right_mouse = button_input.ButtonInput(demo.IsRightMouseDown)

castle = buildings.initBlueCastle()

p = castle.Building.position
a = agent.Agent(nmath.Float2(p.x,p.z));

entity_manager.instance.workers[a.entity] = a

def NebulaUpdate():

    path_manager.instance.calc_paths(100)
    entity_manager.instance.updateAll()


def NebulaDraw(p):

    if left_mouse.pressed():
        entity_manager.instance.selectAgent(p)

    if right_mouse.pressed():
        p = demo.RayCastMousePos()
        a.addGoal(goals.WalkToGoal(p.x,p.z))

    entity_manager.instance.dbgDraw()


def HandleMessage(msg):
    pass
