from Grupp1 import entity_manager, goals
import nmath, demo

defendState = True

standPos = nmath.Float2(0,150)

def keyFunc(enemy):
    cp = entity_manager.instance.getCastlePos()
    tp = enemy.Agent.position
    return (cp.x - tp.x)**2 + (cp.y - tp.z)**2

def defendMode():

    free_soldiers     = []
    non_free_soldiers = []

    for soldier in entity_manager.instance.soldiers.values():
        if soldier.isFree() or not isinstance(soldier.getGoal(), goals.Attack): 
            free_soldiers.append(soldier)
        else:
            non_free_soldiers.append(soldier)

    enemies = []

    closest_enemy = 340**2
    
    for enemy_i in entity_manager.instance.enemy_soldiers:
        enemy = demo.Entity.fromInt(enemy_i)
        if not demo.IsValid(enemy):
            continue
        ep = enemy.Agent.position
        cp = entity_manager.instance.getCastlePos()
        dist_sq = (cp.x - ep.x)**2 + (cp.y - ep.z)**2
        if dist_sq < 70**2:
            enemies.append(enemy)

        if dist_sq < closest_enemy:
            closest_enemy = dist_sq

    if len(enemies) > 0:

        enemies.sort(key=keyFunc)
        

        for enemy in enemies:
            for _ in range(3):
                if not free_soldiers:
                    break
                soldier = free_soldiers.pop()
                soldier.addGoals([goals.WalkToGoal(standPos), goals.Attack(enemy)])

        return

    enemies = []

    for enemy_i in entity_manager.instance.enemy_workers:
        enemy = demo.Entity.fromInt(enemy_i)
        if not demo.IsValid(enemy):
            continue
        ep = enemy.Agent.position
        cp = entity_manager.instance.getCastlePos()
        dist_sq = (cp.x - ep.x)**2 + (cp.y - ep.z)**2
        if dist_sq < 70**2:
            enemies.append(enemy)

        if dist_sq < closest_enemy:
            closest_enemy = dist_sq

    if len(enemies) > 0:

        enemies.sort(reverse=True, key=keyFunc)

        for enemy in enemies:
            for _ in range(3):
                if not free_soldiers:
                    break
                soldier = free_soldiers.pop()
                soldier.addGoals([goals.WalkToGoal(standPos), goals.Attack(enemy)])

        return


    if closest_enemy > 110**2:
        for soldier in non_free_soldiers:
            if isinstance(soldier.getGoal(), goals.Attack):
                soldier.popGoal()



def assultMode():
    free_soldiers     = []
    non_free_soldiers = []

    for soldier in entity_manager.instance.soldiers.values():
        if soldier.isFree() or not isinstance(soldier.getGoal(), goals.Attack): 
            free_soldiers.append(soldier)
        else:
            non_free_soldiers.append(soldier)

    enemies = []

    
    for enemy_i in entity_manager.instance.enemy_soldiers:
        enemy = demo.Entity.fromInt(enemy_i)
        if not demo.IsValid(enemy):
            continue
        enemies.append(enemy)

    if len(enemies):

        enemies.sort(key=keyFunc)
        #print("enemies: ", enemies)
        

        for enemy in enemies:
            for _ in range(3):
                if not free_soldiers:
                    break
                soldier = free_soldiers.pop()
                soldier.addGoal(goals.Attack(enemy))

        if len(enemies) > len(entity_manager.instance.soldiers) / 4:
            return

    enemies = []



    castle = None
    for building_i in entity_manager.instance.enemy_buildings:
        building = demo.Entity.fromInt(building_i)
        if building.Building.type == demo.buildingType.CASTLE:
            castle = building
            break

    if castle:
        for _ in range(int(len(free_soldiers) * 0.2)):
            free_soldiers.pop().addGoal(goals.Attack(castle))


    for enemy_i in entity_manager.instance.enemy_workers:
        enemy = demo.Entity.fromInt(enemy_i)
        if not demo.IsValid(enemy):
            print("NOT VALIDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD")
            continue

        if enemy.Agent.type != demo.agentType.WORKER:
            continue

        enemies.append(enemy)

    if len(enemies) > 0:

        enemies.sort(reverse=True, key=keyFunc)

        for enemy in enemies:
            for _ in range(3):
                if not free_soldiers:
                    break
                soldier = free_soldiers.pop()
                soldier.addGoal(goals.Attack(enemy))

        return

    if castle:
        for soldier in free_soldiers:
            soldier.addGoal(goals.Attack(castle))
    else:
        soldier.addGoal(goals.WalkToGoal(nmath.Float2(0,-170)))


def update():

    if defendState:
        defendMode()
    else:
        assultMode()


def launchAssult():
    global defendState
    defendState = False
