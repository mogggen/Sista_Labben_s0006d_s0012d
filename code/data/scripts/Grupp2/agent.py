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
	
	#lämna, orders frome overlord
	def ChangeState(self, newState):
		self.state.Exit(self)
		self.state = newState
		self.state.Enter(self)
	def Update(self):
		self.state.Execute(self)
	# Take Damage - Method
	def TakeDamage(self, msg):
		hp = self.entityHandle.Health
		hp.hp = statParser.getStat("workerHealth")
		if hp > 1:
			hp -= 1
			self.entityHandle.Health = hp
		elif self.hp <= 1:
			overlord.overlord.KillAgent(self)
	def DealDamage(self, targetEntity):
		overlord.overlord.SendMsg(self, targetEntity)
	# pick up item
	def PickupItem(self, item, itemType):
		if demo.isValid(item):
			demo.Delete(item)
			self.holding = itemType
	# drop item
	def DropItem(self):
		if self.pos == overlord.overlord.castleEntity.Building.position:
			if self.holding == enums.ItemEnum.WOOD:
				overlord.Addtree(1)
			elif self.holding == enums.ItemEnum.IRON_ORE:
				overlord.AddironOre(1)
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
		for x in range(-radius, radius+1):
			for y in range(-radius, radius+1):
				if (x**2 + y**2) < radius**2:
					fog_of_war.grupp2.uncloud(round(p.x-x), round(p.z-y))

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
			self.itemEntity = overlord.overlord.GetCloseTree(self)
			if not self.itemEntity: return
			self.finalGoal = self.itemEntity.Tree.position
			self.ChangeState(fsm.MoveState())

		elif self.goal == enums.GoalEnum.IRON_GOAL:
			self.itemEntity = overlord.overlord.GetCloseIron(self)
			if not self.itemEntity: return
			self.finalGoal = self.itemEntity.Iron.position
			self.ChangeState(fsm.MoveState())

		elif self.goal == enums.GoalEnum.SOLDIER_GOAL:
			if self.entityHandle.Agent.type == demo.agentType.WORKER:
				self.ChangeState(fsm.UpgradeState())
			else:
				self.ChangeState(fsm.BaseState())
				
		elif self.goal == enums.GoalEnum.SCOUT_GOAL:
			if self.entityHandle.Agent.type == demo.agentType.WORKER:
				self.ChangeState(fsm.UpgradeState())

		elif self.goal == enums.GoalEnum.BUILD_SMELTER_GOAL or self.goal == enums.GoalEnum.BUILD_SMITH_GOAL or self.goal == enums.GoalEnum.BUILD_KILNS_GOAL or self.goal == enums.GoalEnum.BUILD_TRAINING_CAMP_GOAL:
			if self.entityHandle.Agent.type == demo.agentType.WORKER or self.entityHandle.agentType == demo.agentType.BUILDER:
				self.finalGoal = overlord.overlord.GetBuildPosition()
				self.ChangeState(fsm.MoveState())
