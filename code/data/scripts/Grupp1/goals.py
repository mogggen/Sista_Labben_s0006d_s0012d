import Grupp1.path_manager as path_manager
import nmath, navMesh, demo, statParser
import enum
import msgManager
import random

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
                #print("Framme")
                pass
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


class follow(Goal):
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


    def dbgDraw(self):
        self.path.algorithm.visualize(self.path)


#--------------------------------------------------------------------#


class cutTree(Goal):
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

        elif demo.getTime() - self.timer >= statParser.getStat("wcSpeed"):
            agent.inventory = item.wood
            agent.popGoal()
            #tree.delete()


    def dbgDraw(self):
        self.path.algorithm.visualize(self.path)

#--------------------------------------------------------------------#


class pickupOre(Goal):
    def __init__(self, ore):
        self.ore = ore


    def enter(self, agent):
        self.active = True


    def paused(self):
        self.active = False


    def execute(self, agent):
        if not demo.IsValid(self.ore):
            # tree.delete()
            return

        agent.inventory = item.ore
        agent.popGoal()
        #ore.delete()


    def dbgDraw(self):
        self.path.algorithm.visualize(self.path)

#--------------------------------------------------------------------#


class emptyInventory(Goal):
    def __init__(self):
        pass


    def enter(self, agent):
        self.active = True


    def paused(self):
        self.active = False


    def execute(self, agent):
        # resources.addResource(agent.inventory)
        agent.inventory = item.none
        agent.popGoal()


    def dbgDraw(self):
        self.path.algorithm.visualize(self.path)

#--------------------------------------------------------------------#


class attack(Goal):
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
                messageManager.sendMsg(demo.teamEnum.GRUPP_2, agent, self.enemy, "attacked")
                self.timer = demo.GetTime()
                onCooldown = True


    def dbgDraw(self):
        self.path.algorithm.visualize(self.path)

#--------------------------------------------------------------------#


class flee(Goal):
    def __init__(self):
        pass


    def enter(self, agent):
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
        if distance >= 25:
            agent.addGoal(WalkToGoal(enemyPos[0], enemyPos[2]))
        elif distance >= pow(statParser.getStat("soldierAttackRange"), 2):
            agent.setTarget(enemyPos)
        elif not onCooldown:
            messageManager.sendMsg(demo.teamEnum.GRUPP_2, agent, self.enemy, "attacked")


    def dbgDraw(self):
        self.path.algorithm.visualize(self.path)
