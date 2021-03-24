import random, demo
from Grupp2 import pathfinder, buildings, overlord

class IdleState:
    def Execute(self, agent):
        agent.FindTask()

class MoveState:
    def Execute(self, agent):
        #neighbourCenter = navMesh.getCenter(agent.face)

        #get this
        current_face = agent.current_face # pos
        pathToGoal = Agent.goalPath
        pathToCastle = agent.CasltePath # go to Castle with Resouce

        overlord.resource += 1
        resource_pos = x, z

        #set this
        whatResource = "iron"
        whatResource = "tree"
        hasResource = True # if have res: go home
        overlord.RemoveTree(1);
        #remove_from_avalible_resources ??
        
        #if not agent.Holding: Agent.carrying = whatResource
            #pathToGoal = agent.pathToGoal
            #if not resource.Found
                #find new resource
            #move toward resource
            #get resource
            #carry resource
            #get path back to Castle

class WoodChoppingState:
    def Execute(self, agent):
        if agent.GetTouchingBlock().hasTrees:
            if agent.workTimer <= 0:
                agent.workTimer = 30 * demo.GetFrameTime()
                agent.GetTouchingBlock().RemoveTree()
                agent.PickUpItem()
                agent.SetReturnPath()
                agent.workTimer -= 1 * demo.GetFrameTime()
            if agent.goal == enums.GoalEnum.WOOD_GOAL:
                agent.FindWood()
                agent.ChangeState(MoveState())

class UpgradeState:
    def __init__(self, upgradeType):
        self.upgradeType = upgradeType

    def Execute(self, agent):
        if agent.upgradeTimer > 0:
            agent.upgradeTimer -= 1 * demo.GetFrameTime()
            # if agent.upgradeTimer%5 == 0:
            #     print(agent.upgradeTimer)
        else:
            agent.type = self.upgradeType
            agent.ChangeState(IdleState())
            print("Upgrade complete!", agent.ID, "is now a", agent.type)

#DANGER, BROKEN
class ExploreState:
    currentGoal = 0
    dirX = 0
    dirY = 0
    ms = 1
    def Execute(self, agent):
        if agent.type != enums.AgentType.DISCOVERER:
            print(agent.ID, "is not a discoverer!!!")
            agent.ChangeState(IdleState())
        if self.currentGoal == 0:
            self.currentGoal = agent.GetTouchingBlock()
        if (self.currentGoal.id % 100) * 10 + 5 == int(agent.posX) and int(self.currentGoal.id / 100) * 10 + 5 == int(agent.posY):
            agent.DiscoverTiles()
            mostFogged = 0
            currentBlock = agent.GetTouchingBlock()
            self.ms = currentBlock.ms
            if currentBlock.walkable is False:
                print("CURRENTBLOCK IS NOT WALKABLE")
            for n in currentBlock.adjacents:
                xFogged = 0
                nBlock = pathfinder.paths.GetBlockByID(n)
                for nn in nBlock.adjacents:
                    if pathfinder.paths.GetBlockByID(nn).isFogged:
                        xFogged += 1
                if mostFogged < xFogged:
                    mostFogged = xFogged
                    self.currentGoal = nBlock
            if mostFogged == 0:
                x = len(currentBlock.adjacents)
                randNeighbour = random.randrange(x)
                self.currentGoal = pathfinder.paths.GetBlockByID(currentBlock.adjacents[randNeighbour])

            self.dirX = self.currentGoal.id % 100 - agent.GetTouchingBlock().id % 100
            self.dirY = int(self.currentGoal.id / 100) - int(agent.GetTouchingBlock().id / 100)

        agent.Move(self.ms, self.dirX, self.dirY)

# class RunKilnState:
#     def Execute(self, agent):
#         if len(agent.workPlace.block.kilns) < overlord.overlord.nrKiln:
#             return
#         if agent.workTimer == 0:
#             agent.workPlace.BurnWood()
#             agent.workTimer = 30 * demo.GetFrameTime()
#         elif agent.hubBlock.woodPile < 2:
#             print("Not enough wood to burn")
#         else:
#             agent.workTimer -= 1 * demo.GetFrameTime()

class BuildState:
    def __init__(self, buildingType):
        self.buildingType = buildingType

    def Execute(self, agent):
        if agent.workTimer <= 0:
            b = agent.GetTouchingBlock()
            for i in range(10):
                b.TakeWood()

            building = buildings.Building(self.buildingType, b)
            b.kilns.append(building)
            if building.type == enums.BuildingType.KILN_BUILDING:
                overlord.overlord.AddKiln(building)

            agent.ChangeState(IdleState())
            print("KILN BUILT!!!!!")
        else:
            agent.workTimer -= 1 * demo.GetFrameTime()