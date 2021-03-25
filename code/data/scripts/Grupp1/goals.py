from Grupp1 import path_manager, entity_manager, item_manager, buildingManager
import nmath, navMesh, demo, imgui
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
    def pause(self):
        pass
    def dbgDraw(self):
        pass

#--------------------------------------------------------------------#


class WalkToGoal(Goal):
    def __init__(self, goal):
        self.goal = goal
        self.target = self.goal


    def enter(self, agent):
        self.path = path_manager.instance.create_path(agent.getPos(), self.goal, lambda: self.path_is_done_callback(agent))
        agent.setTarget( nmath.Point(self.target.x, 0, self.target.y) )
        self.active = True


    def pause(self):
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


    def pause(self):
        self.active = False


    def execute(self, agent):
        if not demo.IsValid(self.lead):
            agent.popGoal()
            return

        ap = agent.entity.Agent.position
        p = self.lead.Agent.position - nmath.Vector(ap.x, ap.y, ap.z)
        distance = nmath.Vec4.length3_sq(nmath.Vec4(p.x, p.y, p.z, 0))
        if distance >= 25:
            agent.addGoal(WalkToGoal(nmath.Float2(self.lead.Agent.position.x, self.lead.Agent.position.z)))
        else:
            agent.setTarget(self.lead.Agent.position)

#--------------------------------------------------------------------#


class CutTree(Goal):
    def __init__(self, tree):
        self.tree = tree


    def enter(self, agent):
        tp = self.tree.Tree.position
        p = agent.entity.Agent.position - nmath.Vector(tp.x, tp.y, tp.z) 

        if nmath.Vec4.length3(nmath.Vec4(p.x, p.y, p.z, 0)) > 0.001:
            agent.addGoal(WalkToGoal(nmath.Float2(tp.x, tp.z)))
        else:
            self.timer = demo.GetTime()
            self.active = True


    def pause(self):
        self.active = False


    def execute(self, agent):
        if not demo.IsValid(self.tree):
            entity_manager.instance.removeEntity(self.tree)
            agent.popGoal()
            return

        elif demo.GetTime() - self.timer >= statParser.getStat("woodCuttingSpeed"):
            agent.inventory = item.wood
            entity_manager.instance.deleteEntity(self.tree)
            agent.popGoal()


#--------------------------------------------------------------------#


class PickupOre(Goal):
    def __init__(self, ore):
        self.ore = ore


    def enter(self, agent):
        op = self.ore.Iron.position
        if not agent.getPos() == op:
            agent.addGoal(WalkToGoal(nmath.Float2(op.x, op.z)))
        else:
            self.active = True


    def pause(self):
        self.active = False


    def execute(self, agent):
        if not demo.IsValid(self.ore):
            entity_manager.instance.removeEntity(self.ore)
        else:
            agent.inventory = item.ore
            entity_manager.instance.deleteEntity(self.ore)

        agent.popGoal()

#--------------------------------------------------------------------#



class EmptyInventory(Goal):
    def __init__(self):
        pass


    def enter(self, agent):
        tp = entity_manager.instance.getCastlePos()
        p = agent.entity.Agent.position - nmath.Vector(tp.x, 0, tp.y) 

        if nmath.Vec4.length3(nmath.Vec4(p.x, p.y, p.z, 0)) > 0.001:
            agent.addGoal(WalkToGoal(entity_manager.instance.getCastlePos()))
        else:
            self.active = True


    def pause(self):
        self.active = False


    def execute(self, agent):
        if agent.inventory == item.wood:
            item_manager.instance.logs += 1
        elif agent.inventory == item.ore:
            item_manager.instance.ironore += 1
        else:
            print("why tho...")

        agent.inventory = item.none
        agent.popGoal()

#--------------------------------------------------------------------#


class Attack(Goal):
    def __init__(self, enemy):
        self.enemy = enemy
        self.onCooldown = False
        self.path = None


    def enter(self, agent):
        self.timer = demo.GetTime()
        self.active = True


    def path_is_done_callback(self, agent):
        if not self.path:
            return
        if len(self.path.reverse_points) > 0:
            p = navMesh.getCenterOfFace(self.path.reverse_points[-1])
            if self.active:
                agent.setTarget(p)


    def pause(self):
        self.active = False


    def execute(self, agent):
        enemyTransform = self.enemy.WorldTransform
        enemyPos = nmath.Vector(enemyTransform[3][0], enemyTransform[3][1], enemyTransform[3][2])
        p = agent.entity.Agent.position - enemyPos
        distance = nmath.Vec4.length3_sq(nmath.Vec4(p.x, p.y, p.z, 0))

        if self.path:
            self.followPath(agent, enemyPos, distance)
        else:
            self.fight(agent, enemyPos, distance)


    def followPath(self, agent,  enemyPos, distance):
        if not self.path.is_done:
            return

        if distance < 100:
            self.path = None
            return 

        if len(self.path.reverse_points) <= 0:
            if agent.getPos() == agent.getTarget():
                self.path = None
            return

        face = self.path.reverse_points[-1]
        if navMesh.isInFace(agent.getPos(), face):
            self.path.reverse_points.pop()

            if len(self.path.reverse_points) <= 0:
                agent.setTarget(nmath.Point(self.path.goal_pos.x, 0, self.path.goal_pos.y))
            else:
                agent.setTarget(navMesh.getCenterOfFace(self.path.reverse_points[-1]))


    def fight(self, agent, enemyPos, distance):
        if not demo.IsValid(self.enemy):
            agent.popGoal()
            return


        if demo.GetTime() - self.timer >= statParser.getStat("soldierAttackSpeed"):
            self.onCooldown = False

        if distance >= 100:
            target = nmath.Float2(enemyPos.x, enemyPos.z)
            self.path = path_manager.instance.create_path(agent.getPos(), target, lambda: self.path_is_done_callback(agent))
            agent.setTarget(nmath.Point(enemyPos.x, enemyPos.y, enemyPos.z))


        elif distance > pow(statParser.getStat("soldierAttackRange"), 2):
            agent.setTarget(nmath.Point(0,0,0) + enemyPos)
        elif not self.onCooldown:
            if random.uniform(0, 1) <= statParser.getStat("hitChance"):
                #msgManager.instance.sendMsg(msgManager.message(demo.teamEnum.GRUPP_2, agent, self.enemy, "attacked"))
                print("Attacking")
                self.timer = demo.GetTime()
                self.onCooldown = True


    def dbgDraw(self):

        if self.path:
            self.path.algorithm.visualize(self.path)

        enemyTransform = self.enemy.WorldTransform
        enemyPos = nmath.Point(enemyTransform[0][3], enemyTransform[1][3], enemyTransform[2][3])
        demo.DrawDot(enemyPos, 20, nmath.Vec4(0,1,0,1))
        imgui.Begin("Attack goal", None, 0)
        try:
            members = [(attr, getattr(self,attr)) for attr in dir(self) if not callable(getattr(self,attr)) and not attr.startswith("__") ]
            for member, value in members:
                imgui.Text(member + ": " + str(value))
            
            imgui.End()

        except Exception as e:
            imgui.End()
            raise e

#--------------------------------------------------------------------#


class Flee(Goal):
    def __init__(self, enemy):
        self.enemy = enemy


    def enter(self, agent):
        self.active = True
        target = entity_manager.instance.getCastlePos()
        self.path = path_manager.instance.create_path(agent.getPos(), target, lambda: self.path_is_done_callback(agent))
        agent.setTarget(nmath.Point(target.x, 0, target.y))

    def path_is_done_callback(self, agent):
        if len(self.path.reverse_points) > 0:
            p = navMesh.getCenterOfFace(self.path.reverse_points[-1])
            if self.active:
                agent.setTarget(p)

    def pause(self):
        self.active = False


    def execute(self, agent):
        if not demo.IsValid(self.enemy):
            agent.popGoal()
            return

        #Check distance to enemy
        enemyTransform = self.enemy.WorldTransform
        enemyPos = nmath.Vector(enemyTransform[0][3], enemyTransform[1][3], enemyTransform[2][3])
        p = agent.entity.Agent.position - enemyPos
        distance = nmath.Vec4.length3_sq(nmath.Vec4(p.x, p.y, p.z, 0))
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
                t = entity_manager.instance.getCastlePos()
                agent.setTarget(nmath.Point(t.x, 0, t.y)) # Maybe calculate height from navmesh???
            else:
                agent.setTarget(navMesh.getCenterOfFace(self.path.reverse_points[-1]))


    def dbgDraw(self):
        self.path.algorithm.visualize(self.path)
        enemyTransform = self.enemy.WorldTransform
        enemyPos = nmath.Point(enemyTransform[0][3], enemyTransform[1][3], enemyTransform[2][3])
        demo.DrawDot(enemyPos, 20, nmath.Vec4(0,1,0,1))
        pass

#--------------------------------------------------------------------#


class Build(Goal):
    def __init__(self, type:demo.buildingType, pos:nmath.Float2):
        self.toBuild = type
        self.pos = pos
        self.working = False


    def enter(self, agent):
        self.active = True
        self.timer = demo.GetTime()


    def pause(self):
        self.active = False


    def execute(self, agent):
        if not self.working:
            self.timer = demo.GetTime()
            self.working = True
        elif self.working:
            if demo.GetTime() - self.timer >= statParser.getStat(str(self.toBuild).split(".")[1].lower() + "BuildTime"):
                if self.toBuild == demo.buildingType.KILN:
                    newBuilding = buildingManager.kiln(self.pos.x, self.pos.y)

                elif self.toBuild == demo.buildingType.SMELTERY:
                    newBuilding = buildingManager.smelter(self.pos.x, self.pos.y)

                elif self.toBuild == demo.buildingType.BLACKSMITH:
                    newBuilding = buildingManager.blacksmith(self.pos.x, self.pos.y)

                elif self.toBuild == demo.buildingType.TRAININGCAMP:
                    newBuilding = buildingManager.trainingCamp(self.pos.x, self.pos.y)

                entity_manager.instance.addBuildings(newBuilding.buildingEntity, newBuilding)

#--------------------------------------------------------------------#


class Upgrade(Goal):
    def __init__(self, type:demo.agentType):
        self.type = type
        self.timer = 0

    def enter(self, agent):
        a = agent.entity.Agent
        a.type = self.type
        agent.entity.Agent = a
        self.timer = demo.GetTime()
        self.active = True


    def pause(self):
        self.active = False


    def execute(self, agent):
        if demo.GetTime() - self.timer >= statParser.getStat(str(self.type).split(".")[1].lower() + "UpgradeTime"):
            entity_manager.instance.doneUpgrade(agent.entity)
            if agent.entity.Agent.type == demo.agentType.SCOUT:
                agent.setDiscoverRadius(int(statParser.getStat("scoutExploreRadius")))
            agent.popGoal()


