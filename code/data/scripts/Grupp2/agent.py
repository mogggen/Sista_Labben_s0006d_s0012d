import demo, statParser, nmath, fog_of_war
from Grupp2 import fsm, pathfinder, overlord, enums


class Agent:
    def __init__(self, ID, spawnPos):
        self.ID = ID
        self.holding = None
        self.itemEntity = None
        self.goal = enums.GoalEnum.WOOD_GOAL
        self.type = demo.agentType.WORKER
        self.lane = None
        self.finalGoal = None
        self.pathToGoal = []
        self.state = fsm.BaseState()
        self.startTime = 0

        self.entityHandle = demo.SpawnEntity("AgentEntity/redagent")

        self.healthProperty = self.entityHandle.Health
        self.healthProperty.hp = int(statParser.getStat("workerHealth"))
        self.entityHandle.Health = self.healthProperty

        agentProperty = self.entityHandle.Agent
        agentProperty.position = spawnPos
        agentProperty.targetPosition = spawnPos
        self.entityHandle.Agent = agentProperty

        self.Discover()

    # lämna, orders frome overlord
    def ChangeState(self, newState):
        self.state.Exit(self)
        self.state = newState
        self.state.Enter(self)

    def Update(self):
        self.state.Execute(self)

    # Take Damage - Method
    def TakeDamage(self, msg):
        healthProperty = self.entityHandle.Health
        print(healthProperty.hp)
        if healthProperty.hp > 1:
            healthProperty.hp -= 1
            self.entityHandle.Health = healthProperty
        elif healthProperty.hp <= 1:
            overlord.overlord.KillAgent(self)

    def DealDamage(self, targetEntity):
        overlord.overlord.SendMsg(self, targetEntity)

    # pick up item
    def PickupItem(self, item, itemType):
        if demo.IsValid(item):
            demo.Delete(item)
            self.holding = itemType

    # drop item
    def DropItem(self):
        if self.entityHandle.Agent.position == overlord.overlord.castleEntity.Building.position:
            if self.holding == enums.ItemEnum.WOOD:
                overlord.overlord.Addtree(1)
            elif self.holding == enums.ItemEnum.IRON_ORE:
                overlord.overlord.Addironore(1)
            self.holding = None
        else:
            print("Agent not in castle keep walking")

    def Discover(self):
        p = self.entityHandle.Agent.position
        p.x = round(p.x)
        p.y += 0.5
        p.z = round(p.z)
        radius = int(statParser.getStat("normalExploreRadius"))
        if self.entityHandle.Agent.type == demo.agentType.SCOUT:
            radius = int(statParser.getStat("scoutExploreRadius"))
        for x in range(-radius, radius + 1):
            for y in range(-radius, radius + 1):
                if (x ** 2 + y ** 2) < radius ** 2:
                    fog_of_war.grupp2.uncloud(round(p.x - x), round(p.z - y))

    def SetGoal(self, newGoal):
        self.goal = newGoal

    def SetTargetPosition(self, position):
        agentProperty = self.entityHandle.Agent
        agentProperty.targetPosition = position
        self.entityHandle.Agent = agentProperty

    def SetType(self, newType):
        agentProperty = self.entityHandle.Agent
        agentProperty.type = newType
        self.entityHandle.Agent = agentProperty
        if newType == demo.agentType.SOLDIER:
            healthProperty = self.entityHandle.Health
            healthProperty.hp = statParser.getStat("soldierHealth")
            self.entityHandle.Health = healthProperty

    def SetLane(self, lane):
        if self.goal == enums.GoalEnum.SCOUT_GOAL:
            self.lane = lane
        else:
            print("agent, SetLane: This agent is not a scout")

    def GoalHandler(self):
        if self.goal == enums.GoalEnum.WOOD_GOAL:
            self.itemEntity = overlord.overlord.GetCloseTree()
            if not self.itemEntity:
                return
            # Need to check IsValid
            try:
                self.finalGoal = self.itemEntity.Tree.position
                self.ChangeState(fsm.MoveState())
            except Exception:
                print("agent, GoalHandler: Already claimed!")
                return

        elif self.goal == enums.GoalEnum.IRON_GOAL:
            self.itemEntity = overlord.overlord.GetCloseIron()
            if not self.itemEntity:
                return
            # Need to check IsValid
            try:
                self.finalGoal = self.itemEntity.Iron.position
                self.ChangeState(fsm.MoveState())
            except Exception:
                print("agent, GoalHandler: Already claimed!")
                return

        elif self.goal == enums.GoalEnum.SOLDIER_GOAL:
            if self.entityHandle.Agent.type == demo.agentType.WORKER:
                self.ChangeState(fsm.UpgradeState())
            else:
                self.ChangeState(fsm.BaseState())

        elif self.goal == enums.GoalEnum.SCOUT_GOAL:
            if self.entityHandle.Agent.type == demo.agentType.WORKER:
                self.ChangeState(fsm.UpgradeState())

        elif self.goal == enums.GoalEnum.BUILD_SMELTER_GOAL or self.goal == enums.GoalEnum.BUILD_SMITH_GOAL or self.goal == enums.GoalEnum.BUILD_KILNS_GOAL or self.goal == enums.GoalEnum.BUILD_TRAINING_CAMP_GOAL:
            print("agent, GoalHandler: goal check successful")
            if self.entityHandle.Agent.type == demo.agentType.WORKER or self.entityHandle.agentType == demo.agentType.BUILDER:
                self.finalGoal = overlord.overlord.GetPosForBuilding()
                print("got pos for building", self.finalGoal)
                self.ChangeState(fsm.MoveState())
