import random, statParser
from Grupp2 import agent, fsm, pathfinder

class Overlord:
    agents = []
    buildings = []
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

    def SpawnAgents(self):
        maxAgents = 50
        print(len(pathfinder.paths.pathBlocks))
        startBlock = pathfinder.paths.GetNthBlock(random.randrange(9163))
        startBlock.Discover()
        i = 0
        while i < maxAgents:
            self.agents.append(agent.Agent(i, startBlock.IdToCoordinates()))
            self.agents[i].SetHubBlock(startBlock)
            i += 1
            for j in range(len(startBlock.adjacents)):
                if i >= maxAgents:
                    return
                nBlock = pathfinder.paths.GetBlockByID(startBlock.adjacents[j])
                nBlock.Discover()
                self.agents.append(agent.Agent(i, nBlock.IdToCoordinates()))
                self.agents[i].SetHubBlock(startBlock)
                i += 1


    def UpdateAgents(self):
        for i in range(len(self.agents)):
            self.agents[i].Update()

    def GetWood(self):
        for i in range(len(self.agents)):
            if(type(self.agents[i].state) == type(fsm.IdleState())):
                self.agents[i].SetGoal(enums.GoalEnum.WOOD_GOAL)
                self.agents[i].FindWood()
                self.agents[i].ChangeState(fsm.MoveState())

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

    def SetKilnerToWorkplace(self, building):
        if self.nrIdleKilners <= 0:
            print("Need more kilners")
        else:
            for i in range(self.nrDisc, self.nrDisc + self.nrKiln):
                if self.agents[i].workPlace == 0:
                    self.agents[i].AddWorkPlace(self.kilns.pop())
                    print("Added workplace to agent")
                    return
    #add resorses
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
    #take resorses
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


    def Addsoldiers(self):
        self.soldiers += 1

    def AddKiln(self, kiln):
        self.kilns.append(kiln)
        print("Added kiln to overlord")
        self.SetKilnerToWorkplace(kiln)
   

overlord = Overlord()