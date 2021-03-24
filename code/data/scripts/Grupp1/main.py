import Grupp1.path_manager as path_manager
import Grupp1.agent as agent
import Grupp1.goals as goals

import nmath, demo
import button_input
import buildings

y_button = button_input.ButtonInput(demo.IsYDown)
left_mouse = button_input.ButtonInput(demo.IsRightMouseDown)

castle = buildings.initBlueCastle()

p = castle.Building.position
a = agent.Agent(nmath.Float2(p.x,p.z));

def NebulaUpdate():
    global path

    path_manager.instance.calc_paths(10)

    a.update()

def NebulaDraw(p):

    if left_mouse.pressed():
        p = demo.RayCastMousePos()
        a.addGoal(goals.WalkToGoal(p.x,p.z))

    a.dbgDraw()
