import demo, statParser, nmath
from Grupp2 import fsm, pathfinder, overlord, enums

class Agent:
	def __init__(self, ID):
		self.ID = ID
		self.holding = None
		self.itemEntity = None
		self.goal = enums.GoalEnum.WOOD_GOAL
		self.type = demo.agentType.WORKER
		self.finalGoal = None
		self.pathToGoal = []
		self.state = fsm.BaseState()
		self.Starttime = 0
		
		self.entityHandle = demo.SpawnEntity("AgentEntity/agent")
		
		self.healthProperty = self.entityHandle.Health
		self.healthProperty.hp = int(statParser.getStat("workerHealth"))
		self.entityHandle.Health = self.healthProperty
	
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
	def DealDamage(self, target):
		overlord.overlord.SendMsg(self, target)
	# pick up item
	def PickupItem(self, item, itemType):
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
		self.p = self.entityHandle.Agent.position
		self.p.x = round(self.p.x)
		self.p.y += 0.5
		self.p.z = round(self.p.z)
		self.radius = statParser.getStat("normalExploreRadius")
		if self.entityhandel.agentType == demo.agentType[1]:
			self.radius = statParser.getStat("scoutExploreRadius")
		for x in range(-radius, radius+1):
			for y in range(-radius, radius+1):
				if (x**2 + y**2) < radius**2:
					fog_of_war.visual.uncloud(round(self.p.x-x),round(self.p.z-y))

	def SetGoal(self, newGoal):
		self.goal = newGoal

	def SetTargetPosition(self, position):
		agentProperty = self.entityHandle.Agent
		agentProperty.targetPosition = position
		self.entityHandle.Agent = agentProperty

	def goalHandler(self):
		if self.goal == enums.WOOD_GOAL:
			self.itemEntity = overlord.overlord.GetCloseTree()
			self.finalGoal = self.itemEntity.Tree.position
			self.ChangeState(fsm.MoveState())

		elif self.goal == enums.IRON_GOAL:
			self.itemEntity = overlord.overlord.GetCloseIron()
			self.finalGoal = self.itemEntity.Iron.position
			self.ChangeState(fsm.MoveState())
		
		# Soldier goal needs fix maybe
		elif self.goal == enums.SOLDIER_GOAL:
			if self.entityHandler.agentType == demo.agentType.WORKER:
				self.ChangeState(fsm.UpgradeState())


		elif self.goal == enums.BUILD_SMELTER_GOAL or self.goal == enums.BUILD_SMITH_GOAL or self.goal == enums.BUILD_KILNS_GOAL or self.goal == enums.BUILD_TRAINING_CAMP_GOAL:
			if self.entityHandler.agentType == demo.agentType.WORKER or self.entityHandle.agentType == demo.agentType.BUILDER:
				self.finalGoal = overlord.overlord.GetBuildPosition()
				self.ChangeState(fsm.MoveState())
