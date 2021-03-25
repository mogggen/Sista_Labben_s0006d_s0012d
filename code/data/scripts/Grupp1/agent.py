import demo, nmath, imgui
import statParser, fog_of_war

class Agent:
    def __init__(self, pos):
        self.entity = demo.SpawnEntity("AgentEntity/blueagent")
        a = self.entity.Agent
        a.position = nmath.Point(pos.x, 0, pos.y)
        a.targetPosition = nmath.Point(pos.x, 0, pos.y)
        self.entity.Agent = a
        
        self.inventory = 0

        h = self.entity.Health
        h.hp = int(statParser.getStat("workerHealth"))
        self.entity.Health = h

        self.goals = []

        self.setDiscoverRadius(int(statParser.getStat("normalExploreRadius")))


    def update(self):
        if len(self.goals) > 0:
            self.goals[-1].execute(self)

        p = self.entity.Agent.position

        for x, y in self.uncloudTiles:
            fog_of_war.grupp1.uncloud(round(p.x-x),round(p.z-y))


    def addGoal(self, goal):
        if len(self.goals) > 0:
            self.goals[-1].pause()
        self.goals.append(goal)
        self.goals[-1].enter(self)


    def addGoals(self, goals):
        if len(self.goals) > 0:
            self.goals[-1].pause()
        self.goals += goals
        self.goals[-1].enter(self)

    def clearGoals(self):
        self.goals.clear()


    def popGoal(self):
        self.goals.pop()
        if len(self.goals) > 0:
            self.goals[-1].enter(self)


    def getPos(self):
        pos = self.entity.Agent.position
        return nmath.Float2(pos.x, pos.z)
    

    def getTarget(self):
        pos = self.entity.Agent.targetPosition
        return nmath.Float2(pos.x, pos.z)

    def setDiscoverRadius(self, radius: int):
        self.uncloudTiles = []
        for x in range(-radius, radius+1):
            for y in range(-radius, radius+1):
                if (x**2 + y**2) < radius**2:
                    self.uncloudTiles.append((x,y))



    def setTarget(self, pos: nmath.Point):
        a = self.entity.Agent
        a.targetPosition = pos
        self.entity.Agent = a


    def dbgDraw(self):
        if len(self.goals) > 0:
            self.goals[-1].dbgDraw()

        imgui.Begin("Agent", None, 0)
        try:
            members = [(attr, getattr(self,attr)) for attr in dir(self) if not callable(getattr(self,attr)) and not attr.startswith("__") and not attr == "goals"]
            for member, value in members:
                imgui.Text(member + ": " + str(value))
            
            members = [(attr, getattr(self.entity.Agent,attr)) for attr in dir(self.entity.Agent) if not callable(getattr(self.entity.Agent,attr)) and not attr.startswith("__") and not attr == "goals"]
            for member, value in members:
                imgui.Text("Agent: " + member + ": " + str(value))
            members = [(attr, getattr(self.entity.Team,attr)) for attr in dir(self.entity.Team) if not callable(getattr(self.entity.Team,attr)) and not attr.startswith("__") and not attr == "goals"]
            for member, value in members:
                imgui.Text("Team: " + member + ": " + str(value))
            members = [(attr, getattr(self.entity.Health,attr)) for attr in dir(self.entity.Health) if not callable(getattr(self.entity.Health,attr)) and not attr.startswith("__") and not attr == "goals"]
            for member, value in members:
                imgui.Text("Health: " + member + ": " + str(value))

            imgui.Text("-- GOALS --")
            for goal in self.goals:
                imgui.Text(" " * 4 + str(goal))
            

            imgui.End()

        except Exception as e:
            imgui.End()
            raise e
