import Grupp1.path_manager as path_manager
import Grupp1.entity_manager as entity_manager
import Grupp1.item_manager as item_manager
import Grupp1.agent as agent
import Grupp1.goals as goals

import nmath, demo
import button_input
import buildings

left_mouse  = button_input.ButtonInput(demo.IsLeftMouseDown)
right_mouse = button_input.ButtonInput(demo.IsRightMouseDown)
y_button    = button_input.ButtonInput(demo.IsYdown)

castle = buildings.initBlueCastle()
entity_manager.instance.castle = castle

p = entity_manager.instance.getCastlePos()
for _ in range(10):
    a = agent.Agent(p);
    entity_manager.instance.workers[a.entity] = a

tree_pos = None

def NebulaUpdate():

    path_manager.instance.calc_paths(100)
    entity_manager.instance.updateAll()


def NebulaDraw(p):
    global tree_pos

    if left_mouse.pressed():
        entity_manager.instance.selectAgent(p)

    if right_mouse.pressed():
        p = demo.RayCastMousePos()
        a = entity_manager.instance.getSelectedAgent()
        if a:
            a.addGoal(goals.WalkToGoal(p.x,p.z))

    if y_button.pressed():

        tree = None
        tree_property = None

        def func(e, t):
            nonlocal tree, tree_property
            tree = e
            tree_property = t

        demo.ForTree(func)

        a = entity_manager.instance.getSelectedAgent()

        p = tree_property.position
        a.addGoal(goals.WalkToGoal(p.x,p.z))
        a.addGoal(goals.CutTree(tree))
        cp = entity_manager.instance.getCastlePos()
        a.addGoal(goals.WalkToGoal(cp.x,cp.y))
        a.addGoal(goals.EmptyInventory())

        tree_pos = p


    if tree_pos:
        demo.DrawDot(p, 10, nmath.Vec4(0,1,1,1))


            

    entity_manager.instance.dbgDraw()
    item_manager.instance.drawGui()


def HandleMessage(msg):
    pass
