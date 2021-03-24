from Grupp1 import path_manager, entity_manager, item_manager
import nmath, navMesh, demo
import statParser, msgManager
import enum, random

class item(enum.Enum):
    none = 0
    wood = 1
    ore = 2

class Goal:
    def enter(self, agent):
        pass
    def execute(self, agent):
        pass
    def pause(self, agent):
        pass
    def dbgDraw(self):
        pass

#--------------------------------------------------------------------#


class WalkToGoal(Goal):
    def __init__(self, x, y):
        self.goal = nmath.Float2(x,y)
        self.target = self.goal


    def enter(self, agent):
        self.path = path_manager.instance.create_path(agent.getPos(), self.goal, lambda: self.path_is_done_callback(agent))
        agent.setTarget( nmath.Point(self.target.x, 0, self.target.y) )
        self.active = True


    def paused(self):
        self.active = False


    def path_is_done_callback(self, agent):
        if len(self.path.reverse_points) > 0:
            p = navMesh.getCenterOfFace(self.path.reverse_points[-1])
            self.target = nmath.Float2(p.x, p.z)
            if self.active:
                agent.setTarget(p)

    
    def execute(self, agent):
        if not self.path.is_done:
            return

        if len(self.path.reverse_points) <= 0:
            if agent.getPos() == agent.getTarget():
                agent.popGoal()
            return

        face = self.path.reverse_points[-1]
        if navMesh.isInFace(agent.getPos(), face):
            self.path.reverse_points.pop()

            if len(self.path.reverse_points) <= 0:
                agent.setTarget( nmath.Point(self.goal.x, 0, self.goal.y) ) # Maybe calculate height from navmesh???
            else:
                agent.setTarget(navMesh.getCenterOfFace(self.path.reverse_points[-1]))

    def dbgDraw(self):
        self.path.algorithm.visualize(self.path)

#--------------------------------------------------------------------#


class Follow(Goal):
    def __init__(self, lead):
        self.lead = lead

    def enter(self, agent):
        self.active = True


    def paused(self):
        self.active = False


    def execute(self, agent):
        if demo.IsValid(self.lead):
            agent.popGoal()
            return
        p = self.lead.Agent.position - agent.position
        distance = nmath.Vec4.length3_sq(nmath.Vec4(p.x, p.y, p.z))
        if distance >= 25:
            agent.addGoal(WalkToGoal(self.lead.Agent.position.x, self.lead.Agent.position.z))
        else:
            agent.setTarget(self.lead.Agent.position)




#--------------------------------------------------------------------#


class CutTree(Goal):
    def __init__(self, tree):
        self.tree = tree


    def enter(self, agent):
        self.timer = demo.GetTime()
        self.active = True


    def paused(self):
        self.active = False


    def execute(self, agent):
        if not demo.IsValid(self.tree):
            # tree.delete()
            return

        elif demo.GetTime() - self.timer >= statParser.getStat("woodCuttingSpeed"):
            agent.inventory = item.wood
            agent.popGoal()
            # tree.delete()



#--------------------------------------------------------------------#


class PickupOre(Goal):
    def __init__(self, ore):
        self.ore = ore


    def enter(self, agent):
        self.active = True


    def paused(self):
        self.active = False


    def execute(self, agent):
        if not demo.IsValid(self.ore):
            # ore.delete()
            return

        agent.inventory = item.ore
        agent.popGoal()
        # ore.delete()



#--------------------------------------------------------------------#


class Attack(Goal):
    def __init__(self, enemy):
        self.enemy = enemy


    def enter(self, agent):
        self.timer = demo.GetTime()
        self.active = True


    def paused(self):
        self.active = False


    def execute(self, agent):
        if not demo.IsValid(self.enemy):
            agent.popGoal()
            return

        enemyTransform = self.enemy.WorldTransform
        enemyPos = nmath.Vec3(enemyTransform[0][3], enemyTransform[1][3], enemyTransform[2][3])
        p = enemyPos - agent.position
        distance = nmath.Vec4.length3_sq(nmath.Vec4(p.x, p.y, p.z))

        if demo.GetTime - self.timer >= statParser.getState("soldierAttackSpeed"):
            onCooldown = False

        if distance >= 25:
            agent.addGoal(WalkToGoal(enemyPos[0], enemyPos[2]))
        elif distance > pow(statParser.getStat("soldierAttackRange"), 2):
            agent.setTarget(enemyPos)
        elif not onCooldown:
            if random.uniform(0, 1) <= statParser.getStat("hitChance"):
                msgManager.messageManager.sendMsg(msgManager.message(demo.teamEnum.GRUPP_2, agent, self.enemy, "attacked"))
                self.timer = demo.GetTime()
                onCooldown = True



#--------------------------------------------------------------------#


class Flee(Goal):
    def __init__(self):
        pass


    def enter(self, agent):
        self.active = True
        self.path = path_manager.instance.create_path(agent.getPos(), self.goal,lambda: self.path_is_done_callback(agent))
        agent.setTarget(nmath.Point(self.target.x, 0, self.target.y))

    def path_is_done_callback(self, agent):
        if len(self.path.reverse_points) > 0:
            p = navMesh.getCenterOfFace(self.path.reverse_points[-1])
            self.target = nmath.Float2(p.x, p.z)
            if self.active:
                agent.setTarget(p)

    def paused(self):
        self.active = False


    def execute(self, agent):
        if not demo.IsValid(self.enemy):
            agent.popGoal()
            return

        #Check distance to enemy
        enemyTransform = self.enemy.WorldTransform
        enemyPos = nmath.Vec3(enemyTransform[0][3], enemyTransform[1][3], enemyTransform[2][3])
        p = enemyPos - agent.position
        distance = nmath.Vec4.length3_sq(nmath.Vec4(p.x, p.y, p.z))
        if distance >= 2500:
            agent.popGoal()

        # Flee home
        if not self.path.is_done:
            return

        if len(self.path.reverse_points) <= 0:
            if agent.getPos() == agent.getTarget():
                pass
            return

        face = self.path.reverse_points[-1]
        if navMesh.isInFace(agent.getPos(), face):
            self.path.reverse_points.pop()

            if len(self.path.reverse_points) <= 0:
                agent.setTarget(nmath.Point(self.BasePos.x, 0, self.BasePos.y)) # Maybe calculate height from navmesh???
            else:
                agent.setTarget(navMesh.getCenterOfFace(self.path.reverse_points[-1]))


    def dbgDraw(self):
        self.path.algorithm.visualize(self.path)

#--------------------------------------------------------------------#


class Upgrade(Goal):
    def __init__(self, type:demo.agentType):
        self.type = type
        pass

    def enter(self, agent):
        a = agent.Entity.Agent
        a.type = self.type
        agent.Entity.Agent = a
        self.timer = demo.GetTime()
        self.active = True


    def paused(self):
        self.active = False


    def execute(self, agent):
        if demo.GetTime() - self.timer >= statParser.getStat(str(self.type).lower + "UpgradeTime"):
            entity_manager.instance.doneUpgrade(agent.entity)
            agent.popGoal()


