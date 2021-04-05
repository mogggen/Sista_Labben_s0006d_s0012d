import Grupp1.path_manager as path_manager
import Grupp1.entity_manager as entity_manager
import Grupp1.item_manager as item_manager
import Grupp1.agent as agent
import Grupp1.goals as goals
import Grupp1.worker_manager as worker_manager
import Grupp1.explorerManager as explorerManager
import Grupp1.build_manager as build_manager
import Grupp1.soldierManager as soldierManager
import Grupp1.godManager as godManager
import Grupp1.pathFinder as pathFinder


import nmath, demo
import button_input
import buildings
import msgManager
import cProfile


left_mouse  = button_input.ButtonInput(demo.IsLeftMouseDown)
right_mouse = button_input.ButtonInput(demo.IsRightMouseDown)
y_button    = button_input.ButtonInput(demo.IsYdown)
t_button    = button_input.ButtonInput(demo.IsTdown)
r_button    = button_input.ButtonInput(demo.IsRdown)

castle = buildings.initBlueCastle()
entity_manager.instance.castle = castle
        

p = entity_manager.instance.getCastlePos()
for _ in range(50):
    a = agent.Agent(p);
    entity_manager.instance.addWorker(a.entity, a)

def NebulaUpdate():

    path_manager.instance.calc_paths(100)

    godManager.update()

    ## update managers
    worker_manager.instance.update()
    explorerManager.update()
    soldierManager.update()
    build_manager.update()



    entity_manager.instance.updateAll()

    if entity_manager.instance.updateState == entity_manager.UpdateState.TREES:
        cProfile.run("from Grupp1 import entity_manager; entity_manager.instance.updateUnManagedEntities()")
    else:
        entity_manager.instance.updateUnManagedEntities()


def NebulaDraw(p):

    demo.DrawDot(nmath.Point(-30, 0, 125), 10, nmath.Vec4(1, 0, 0, 1))
    demo.DrawDot(nmath.Point(30, 0, 125), 10, nmath.Vec4(1, 0, 0, 1))
    demo.DrawDot(nmath.Point(30, 0, 160), 10, nmath.Vec4(1, 0, 0, 1))
    demo.DrawDot(nmath.Point(-30, 0, 160), 10, nmath.Vec4(1, 0, 0, 1))

    if left_mouse.pressed():
        entity_manager.instance.selectAgent(p)

    if right_mouse.pressed():
        p = demo.RayCastMousePos()
        a = entity_manager.instance.getSelectedAgent()
        if a:
            a.addGoal(goals.WalkToGoal(nmath.Float2(p.x,p.z)))
    
    if r_button.pressed():
        _a = dummy_enemy.Agent
        _a.targetPosition = p
        dummy_enemy.Agent = _a

        
        #a = entity_manager.instance.getSelectedAgent()
        #a.addGoal(goals.Build(demo.buildingType.BLACKSMITH, nmath.Float2(0,0) ))
    
    if t_button.pressed():
        #dummy_enemy = demo.SpawnEntity("AgentEntity/redagent")
        #a = dummy_enemy.Agent
        #a.position = nmath.Point(0, 0, 0)
        #a.targetPosition = nmath.Point(0, 0, 0)
        #dummy_enemy.Agent = a


        a = entity_manager.instance.getSelectedAgent()
        msgManager.instance.sendMsg(msgManager.message(demo.teamEnum.GRUPP_1, None, a.entity, "jkh"))

        #demo.Delete(dummy_enemy)

    if y_button.pressed():

        a = entity_manager.instance.getSelectedAgent()
        entity_manager.instance.stageForUpgrade(a.entity)
        a.addGoal(goals.Upgrade(demo.agentType.SOLDIER))


        
    p.x = round(p.x)
    p.y += 0.5
    p.z = round(p.z)

    entity_manager.instance.dbgDraw()
    item_manager.instance.drawGui()

    godManager.dbgDraw()

    for point in pathFinder.invalid_points:
        demo.DrawDot(nmath.Point(point.x, 0, point.y), 10, nmath.Vec4(1,0,0.5,1))



def HandleMessage(msg):
    if entity_manager.instance.findAgent(msg.taker):
        agentHealth = msg.taker.Health
        agentHealth.hp -= 1
        msg.taker.Health = agentHealth

        if agentHealth.hp <= 0:
            entity_manager.instance.deleteEntity(msg.taker)


    elif entity_manager.instance.findBuilding(msg.taker):
        buildingHealth = msg.taker.Health
        buildingHealth.hp -= 1
        msg.taker.Health = buildingHealth

        if buildingHealth.hp <= 0:
            entity_manager.instance.deleteEntity(msg.taker)

    elif entity_manager.instamce.castle.toInt() == msg.taker.toInt():
        castleHealth = msg.taker.Health
        castleHealth.hp -= 1
        msg.taker.Health = castleHealth

        if castleHealth.hp <= 0:
            demo.SetTimeFactor(0)
            print("Blue Defeat")
