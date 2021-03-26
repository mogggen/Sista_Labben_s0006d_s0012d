import random, statParser, demo, msgManager, navMesh, nmath
from Grupp2 import agent, fsm, pathfinder, enums

class Overlord:
    agents = []
    buildings = []
    castleEntity = 0
    #resorses
    charcoal = 0
    ironbar = 0
    ironore = 0
    sword = 0
    tree = 0
    #agents
    nrDisc = 0
    nrKiln = 0
    nrBuild = 0
    nrIdleKilners = 0
    soldiers = 0

    kilns = []

    scoutedTrees = []
    scoutedIron = []

    # Where to place buildings
    minRadius = 20 # This should be at least half the size of castle
    maxRadius = 100 # This should not be more than half of the map
    distanceFromBuildingRadius = 10 # This needs to be at least half the size of a building

    def UpdateActors(self):
        for i in range(len(self.agents)):
            self.agents[i].Update()
        for i in range(len(self.buildings)):
            self.buildings[i].Run()

    def SpawnAgent(self):
        a = agent.Agent(len(self.agents))
        agentProperty = a.entityHandle.Agent
        agentProperty.position = self.castleEntity.Building.position
        agentProperty.targetPosition = self.castleEntity.Building.position
        a.entityHandle.Agent = agentProperty
        self.agents.append(a)

    def SpawnAllAgents(self):
        maxAgents = 50
        for i in range(maxAgents):
            self.SpawnAgent()

    # LEGACY
    def OperationCharcoal(self, nrDisc, nrKiln, nrBuild):
        self.nrDisc = nrDisc
        self.nrKiln = nrKiln
        self.nrBuild = nrBuild
        for i in range(len(self.agents)):
            if i < nrDisc:
                self.agents[i].SetGoal(enums.GoalEnum.DISCOVER_GOAL)
            elif i < nrDisc + nrKiln:
                self.agents[i].SetGoal(enums.GoalEnum.KILN_GOAL)
                self.nrIdleKilners += 1
            elif i < nrDisc + nrKiln + nrBuild:
                self.agents[i].SetGoal(enums.GoalEnum.BUILD_KILNS_GOAL)
            else:
                return

    def KillAgent(self, agent):
        self.agents.remove(agent)
        demo.Delete(agent.enityHandle)
        del agent

# FSM requests or information
    def AddScoutedTree(self, tree):
        self.scoutedTrees.append(tree)
    def AddScoutedIron(self, iron):
        self.scoutedIron.append(iron)

    # def RemoveScoutedTree(self, tree):
    #     self.scoutedTrees.remove(tree)
    # def RemoveScoutedIron(self, iron):
    #     self.scoutedIron.remove(iron)

    # A worker requests a tree or iron to gather
    def GetCastlePosition(self):
        return self.castleEntity.Building.position

    def GetCloseTree(self, agent):
        # try catch
        return self.scoutedTrees.pop(0)
    def GetCloseIron(self, agent):
        # try catch
        return self.scoutedIron.pop(0)

    def GetPosForBuilding(self, agent):
        while True:
            # Figure out the max and min values for x and z
            minX = -self.maxRadius
            maxX = self.maxRadius
            minZ = self.GetCastlePosition().z + self.minRadius
            maxZ = self.GetCastlePosition().z + self.maxRadius
            # Get a random value between the thresholds
            x = random.randrange(minX, maxX)
            z = random.randrange(minZ, maxZ)
            point = nmath.Float2(x, z)
            # Check if the point is on the navmesh
            if navMesh.isOnNavMesh(point):
                # Check if the point is too close to any other building
                for b in self.buildings:
                    vec3Pos = b.entityHandle.Building.position
                    float2Pos = nmath.Float2(vec3Pos.x, vec3Pos.z)
                    distanceFloat2 = point - float2Pos
                    absDistance = distanceFloat2.abs
                    if absDistance.length > self.distanceFromBuildingRadius:
                        return point

    def RequestWorker(self, buildingPos, buildingType):
        for a in self.agents:
            if a.type == demo.agentType.WORKER:
                if a.goal == enums.GoalEnum.WOOD_GOAL:
                    if buildingType == demo.buildingType.KILN:
                        a.SetGoal(enums.GoalEnum.KILN_GOAL)
                    elif buildingType == demo.buildingType.SMELTERY:
                        a.SetGoal(enums.GoalEnum.SMELT_GOAL)
                    elif buildingType == demo.buildingType.BLACKSMITH:
                        a.SetGoal(enums.GoalEnum.SMITH_GOAL)
                    a.finalGoal = buildingPos
                    a.ChangeState(fsm.MoveState())
                    return
            else:
                print("Worker requested but there are no more workers!")

    def AddSoldier(self, agent):
        self.soldiers += 1
        # do stuff

    def AddBuilding(self, building):
        self.buildings.append(building)
        # do stuff

    def GetBuildingAtPosition(self, pos):
        for b in self.buildings:
            if b.entityHandle.Building.position == pos:
                return b
        print("There is no building at this location!")

    #add resources
    def AddCharcoal(self, n):
        for x in range(n):    
            self.charcoal += n
    def Addironbar(self, n):
        for x in range(n):
            self.ironbar += n
    def Addironore(self, n):
        for x in range(n):
            self.ironore += n
    def Addsword(self, n):
        for x in range(n):
            self.sword += n
    def Addtree(self, n):
        for x in range(n):
            self.tree += n
    #take resources
    def Takecharcoal(self, n):
        for x in range(n):
            self.charcoal = self.charcoal - n
    def Takeironbar(self, n):
        for x in range(n):
            self.ironbar = self.ironbar - n
    def Takeironore(self,n):
        for x in range(n):
            self.ironore = self.ironore - n
    def Takeswords(self, n):
        for x in range(n):
            self.sword = self.sword - n
    def Taketree(self, n):
        for x in range(n):
            self.tree = self.tree - n


    def HandleMsg(self, msg):
        for a in self.agents:
            if a.entityHandle == msg.taker:
                a.TakeDamage(msg)
        # Reaction

    def SendMsg(self, agent, target:demo.Entity):
        msg = msgManager.message(demo.teamEnum.GRUPP_1, agent.enityHandle, target, "attack")
        msgManager.instance.sendMsg(msg)

overlord = Overlord()