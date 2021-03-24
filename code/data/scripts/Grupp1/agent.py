import demo, nmath
import statParser

class Agent:
    def __init__(self, pos):
        self.entity = demo.SpawnEntity("AgentEntity/agent")
        a = self.entity.Agent
        a.position = nmath.Point(pos.x, 0, pos.y)
        a.targetPosition = nmath.Point(pos.x, 0, pos.y)
        self.entity.Agent = a

        h = self.entity.Health
        h.hp = int(statParser.getStat("workerHealth"))
        self.entity.Health = h

        self.goals = []


    def update(self):
        if len(self.goals) > 0:
            self.goals[-1].execute(self)


    def addGoal(self, goal):
        if len(self.goals) > 0:
            self.goals[-1].pause(self)
        self.goals.append(goal)
        self.goals[-1].enter(self)


    def addGoals(self, goals):
        if len(self.goals) > 0:
            self.goals[-1].pause(self)
        self.goals += goals
        self.goals[-1].enter(self)


    def getPos(self):
        pos = self.entity.Agent.position
        return nmath.Float2(pos.x, pos.z)
    
    def getTarget(self):
        pos = self.entity.Agent.targetPosition
        return nmath.Float2(pos.x, pos.z)


    def setTarget(self, pos: nmath.Point):
        a = self.entity.Agent
        a.targetPosition = pos
        self.entity.Agent = a

    def dbgDraw(self):
        if len(self.goals) > 0:
            self.goals[-1].dbgDraw()
