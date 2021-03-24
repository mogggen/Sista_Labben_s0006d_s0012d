import demo, nmath, imgui
import statParser, fog_of_war

class Agent:
    def __init__(self, pos):
        self.entity = demo.SpawnEntity("AgentEntity/agent")
        a = self.entity.Agent
        a.position = nmath.Point(pos.x, 0, pos.y)
        a.targetPosition = nmath.Point(pos.x, 0, pos.y)
        self.entity.Agent = a
        
        self.inventory = 0

        h = self.entity.Health
        h.hp = int(statParser.getStat("workerHealth"))
        self.entity.Health = h

        self.goals = []



    def update(self):
        if len(self.goals) > 0:
            self.goals[-1].execute(self)

        p = self.entity.Agent.position

        radius = 4 
        for x in range(-radius, radius+1):
            for y in range(-radius, radius+1):
                if (x**2 + y**2) < radius**2:
                    fog_of_war.grupp1.uncloud(round(p.x-x),round(p.z-y))


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


    def popGoal(self):
        self.goals.pop()


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

        imgui.Begin("Agent", None, 0)
        try:
            members = [(attr, getattr(self,attr)) for attr in dir(self) if not callable(getattr(self,attr)) and not attr.startswith("__") and not attr == "item_map"]
            for member, value in members:
                imgui.Text(member + ": " + str(value))
            
            imgui.End()

        except Exception as e:
            imgui.End()
            raise e
