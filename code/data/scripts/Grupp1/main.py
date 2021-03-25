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
r_button    = button_input.ButtonInput(demo.IsRdown)

castle = buildings.initBlueCastle()
entity_manager.instance.castle = castle
        
dummy_enemy = demo.SpawnEntity("AgentEntity/agent")
a = dummy_enemy.Agent
a.position = nmath.Point(0, 0, 0)
a.targetPosition = nmath.Point(0, 0, 0)
dummy_enemy.Agent = a

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
    
    if r_button.pressed():
        _a = dummy_enemy.Agent
        _a.targetPosition = p
        dummy_enemy.Agent = _a

    if y_button.pressed():

        a = entity_manager.instance.getSelectedAgent()
        entity_manager.instance.stageForUpgrade(a.entity)
        a.addGoal(goals.Upgrade(demo.agentType.SCOUT))

        #tree = None
        #tree_property = None

        #def func(e, t):
        #    nonlocal tree, tree_property
        #    tree = e
        #    tree_property = t

        #demo.ForTree(func)

        #a = entity_manager.instance.getSelectedAgent()

        #tp = tree_property.position
        #cp = entity_manager.instance.getCastlePos()
        #a.addGoals([goals.EmptyInventory(),\
        #            goals.WalkToGoal(cp.x,cp.y),\
        #            goals.CutTree(tree),\
        #            goals.WalkToGoal(tp.x,tp.z)])

        #tree_pos = tp


    if tree_pos:
        demo.DrawDot(tree_pos, 10, nmath.Vec4(0,1,1,1))

    entity_manager.instance.dbgDraw()
    item_manager.instance.drawGui()


def HandleMessage(msg):
    if entity_manager.instance.findAgent(msg[2]):
        agentHealth = msg[2].Health
        agentHealth.hp -= 1
        msg[2].Health = agentHealth

        if agentHealth.hp <= 0:
            entity_manager.instance.removeEntity(entity_manager.instance.findAgent(msg[2]))


    elif entity_manager.instance.findBuilding(msg[2]):
        buildingHealth = msg[2].Health
        buildingHealth.hp -= 1
        msg[2].Health = buildingHealth

        if buildingHealth.hp <= 0:
            entity_manager.instance.removeEntity(entity_manager.instance.findBuilding(msg[2]))

    elif entity_manager.instamce.castle == msg[2]:
        castleHealth = msg[2].Health
        castleHealth.hp -= 1
        msg[2].Health = castleHealth

        if castleHealth.hp <= 0:
            demo.SetTimeFactor(0)
            print("Defeat")
