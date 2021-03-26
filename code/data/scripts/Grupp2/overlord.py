import random, statParser, demo, msgManager, navMesh, nmath
from Grupp2 import agent, fsm, pathfinder, enums

class Overlord:
    agents = []
    availableBuilders = []
    soldiers = []
    buildings = []
    availableTrainingCamps = []
    castleEntity = 0
    enemyCastleEntity = None
    #resources
    charcoal = 0
    ironbar = 0
    ironore = 0
    sword = 0
    tree = 0
    # Amount of dudes we want for each goal
    nrWoodGatherers = 31 # At least double amount of iron collectors, ratio is 2.5 times
    nrIronGatherers = 14
    nrScouts = 3
    nrBuilder = 2

    nrKiln = 2 # At least double the amount of smelters
    nrSmelters = 1
    nrSmithy = 2 # Should be same amount as training camps
    nrTrainingCamp = 2 # Should be same amount as smithy
    # This means 7 wood gatherers will turn into building workers
    nrKilnWorkers = nrKiln
    nrSmithWorkers = nrSmithy
    nrSmelterWorkers = nrSmelters

    amountOfSoldiersForAttack = 5

    scoutedWorkers = []
    scoutedSoldiers = []
    scoutedBuildings = []
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
        a = agent.Agent(len(self.agents), self.castleEntity.Building.position)
        self.agents.append(a)

    def SpawnAllAgents(self):
        maxAgents = 50
        for i in range(maxAgents):
            self.SpawnAgent()

    # LEGACY
    def OperationKILL(self):
        for i in range(len(self.agents)):
            if i < self.nrScouts:
                self.agents[i].SetGoal(enums.GoalEnum.SCOUT_GOAL)
                if i == 0:
                    self.agents[i].SetLane(enums.LaneEnum.LEFT)
                if i == 1:
                    self.agents[i].SetLane(enums.LaneEnum.MIDDLE)
                if i == 2:
                    self.agents[i].SetLane(enums.LaneEnum.RIGHT)
            elif i < self.nrScouts + self.nrIronGatherers:
                self.agents[i].SetGoal(enums.GoalEnum.IRON_GOAL)
            else:
                return

    def KillAgent(self, agent):
        self.agents.remove(agent)
        demo.Delete(agent.entityHandle)
        del agent

    def KillBuilding(self, building):
        self.buildings.remove(building)
        demo.Delete(building.entityHandle)
        del building

    # Discover adds discovered objects here
    def AddScoutedWorkers(self, workers):
        self.scoutedWorkers = workers
    def AddScoutedSoldiers(self, soldiers):
        self.scoutedSoldiers = soldiers
    def AddScoutedBuildings(self, buildings):
        self.scoutedBuildings = buildings
    def AddScoutedTree(self, trees):
        self.scoutedTrees = trees
    def AddScoutedIron(self, iron):
        self.scoutedIron = iron
    def AddScoutedEnemyCastle(self, castleEntity):
        self.enemyCastleEntity = castleEntity

    # FSM requests or information
    def GetCastlePosition(self):
        return self.castleEntity.Building.position

    def GetEnemyCastle(self):
        return self.enemyCastleEntity

    # A worker requests a tree or iron to gather
    def GetCloseTree(self, agent):
        if len(self.scoutedTrees) > 0:
            return self.scoutedTrees.pop(0)
    def GetCloseIron(self, agent):
        if len(self.scoutedIron) > 0:
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

    def TrainSoldier(self):
        if len(self.availableTrainingCamps) > 0 and self.sword > 0:
            for a in self.agents:
                if a.type == demo.agentType.WORKER:
                    if a.goal == enums.GoalEnum.WOOD_GOAL:
                        a.SetGoal(enums.GoalEnum.SOLDIER_GOAL)
                        a.finalGoal = self.availableTrainingCamps.pop()
                        a.ChangeState(fsm.MoveState())

    def AddSoldier(self, agent):
        self.soldiers.append(agent)
        if len(self.soldiers) < self.amountOfSoldiersForAttack:
            agent.finalGoal = nmath.Point(0,0,0)
            agent.ChangeState(fsm.MoveState())
        elif self.enemyCastleEntity is not None:
            for s in self.soldiers:
                s.finalGoal = self.enemyCastleEntity.Building.position
                s.ChangeState(fsm.ChargeAndAttackState())

    def AddBuilding(self, building):
        self.buildings.append(building)
        # do stuff

    def AddAvailableTrainingCamp(self, building):
        self.availableTrainingCamps.append(building)
        self.TrainSoldier()

    def RemoveAvailableTrainingCamp(self, building):
        if building in self.availableTrainingCamps:
            self.availableTrainingCamps.remove(building)

    def AddAvailableBuilder(self, builder):
        self.availableBuilders.append(builder)
        self.CheckBuildPossibilities()

    def RemoveAvailableBuilder(self, builder):
        if builder in self.availableBuilders:
            self.availableBuilders.remove(builder)

    def GetBuildingAtPosition(self, pos):
        for b in self.buildings:
            if b.entityHandle.Building.position == pos:
                return b
        print("There is no building at this location!")

    #add resources
    def AddCharcoal(self, n):
        for x in range(n):    
            self.charcoal += 1
        self.CheckBuildPossibilities()
    def Addironbar(self, n):
        for x in range(n):
            self.ironbar += 1
        self.CheckBuildPossibilities()
    def Addironore(self, n):
        for x in range(n):
            self.ironore += 1
        self.CheckBuildPossibilities()
    def Addsword(self, n):
        for x in range(n):
            self.sword += 1
        self.TrainSoldier()
    def Addtree(self, n):
        for x in range(n):
            self.tree += 1
        self.CheckBuildPossibilities()
    #take resources
    def Takecharcoal(self, n):
        for x in range(n):
            self.charcoal = self.charcoal - 1
    def Takeironbar(self, n):
        for x in range(n):
            self.ironbar = self.ironbar - 1
    def Takeironore(self,n):
        for x in range(n):
            self.ironore = self.ironore - 1
    def Takeswords(self, n):
        for x in range(n):
            self.sword = self.sword - 1
    def Taketree(self, n):
        for x in range(n):
            self.tree = self.tree - 1

    def CheckBuildPossibilities(self):
        if len(self.availableBuilders) < 1 or self.tree < 10:
            return
        b = self.availableBuilders.pop()

        if self.GetBuiltBuildingsOfType(demo.buildingType.BLACKSMITH) < self.nrSmithy and self.tree >= statParser.getStat("blacksmithWoodCost") and self.ironbar >= statParser.getStat("blacksmithIronCost"):
            b.SetGoal(enums.GoalEnum.BUILD_SMITH_GOAL)
        elif self.GetBuiltBuildingsOfType(demo.buildingType.TRAININGCAMP) < self.nrTrainingCamp and self.tree >= statParser.getStat("trainingCampWoodCost"):
            b.SetGoal(enums.GoalEnum.BUILD_TRAINING_CAMP_GOAL)
        elif self.GetBuiltBuildingsOfType(demo.buildingType.SMELTERY) < self.nrSmelters and self.tree >= statParser.getStat("smelteryWoodCost"):
            b.SetGoal(enums.GoalEnum.BUILD_SMELTER_GOAL)
        elif self.GetBuiltBuildingsOfType(demo.buildingType.KILN) < self.nrKiln and self.tree >= statParser.getStat("kilnWoodCost"):
            b.SetGoal(enums.GoalEnum.BUILD_KILNS_GOAL)

        self.RemoveAvailableBuilder(b)
        self.finalGoal = overlord.overlord.GetBuildPosition()
        self.ChangeState(fsm.MoveState())

    def GetBuiltBuildingsOfType(self, type):
        i = 0
        for b in self.buildings:
            if b.entityHandle.Building.type == type:
                i += 1
        return i

    def HandleMsg(self, msg):
        for a in self.agents:
            if a.entityHandle == msg.taker:
                a.TakeDamage(msg)
        for b in self.buildings:
            if b.entityHandle == msg.taker:
                b.buildingTakeDamage(msg)
        # Reaction

    def SendMsg(self, agent, target:demo.Entity):
        msg = msgManager.message(demo.teamEnum.GRUPP_1, agent.enityHandle, target, "attack")
        msgManager.instance.sendMsg(msg)

overlord = Overlord()