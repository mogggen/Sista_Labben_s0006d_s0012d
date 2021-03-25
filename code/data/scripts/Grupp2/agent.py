import demo, statParser
from Grupp2 import fsm, pathfinder, overlord, enums

class Agent:
	def __init__(self, ID):
		self.ID = ID
		self.holding = None
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
		self.state.Execute()
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
	def PickupItem(self, item):
		holding = item
	# drop item
	def DropItem(self):
		if self.pos == overlord.overlord.castleEntity.Building.position:
			if self.holding == enums.ItemEnum.WOOD:
				overlord.Addtree(1)
			elif self.holding == enums.ItemEnum.IRON_ORE:
				overlord.AddironOre(1)
			self.holding = None;
		else:
			print("Agent not in castle keep walking")

	def SetGoal(self, newGoal):
		self.goal = newGoal


	def goalHandler(self):
		if self.goal == enums.WOOD_GOAL:
			self.finalGoal = overlord.overlord.getwoodposition() #check method name
			self.ChangeState(MoveState)

		elif self.goal == enums.IRON_GOAL:
			self.finalGoal = overlord.overlord.getironposition() #check method name
			self.ChangeState(MoveState)
		
			
		elif self.goal == enums.KILN_GOAL:
			if self.entityHandle.agentType == demo.agentType.WORKER:
				self.ChangeState(fsm.UpgradeState(demo.agentType.WORKER))
		
		elif self.goal == enums.SMITH_GOAL:
			if self.entityHandler.agentType == demo.agentType.WORKER:
				self.ChangeState(fsm.UpgradeState())
		

		elif self.goal == enum.SMELT_GOAL:
			if self.entityHandler.agentType == demo.agentType.WORKER:
				self.ChangeState(fsm.UpgradeState)
		
		elif self.goal == enum.BUILD_KILNS_GOAL:
			if self.entityHandler.agentType == demo.agentType.WORKER:
				self.finalGoal = overlord.overlord.getbuildposition() #check method name
				self.ChangeState(MoveState)
		
		elif self.goal == enum.BUILD_SMITH_GOAL:
			if self.entityHandler.agentType == demo.agentType.WORKER:
				self.finalGoal = overlord.overlord.getbuildposition() #check method name
				self.ChangeState(MoveState)

		elif self.goal == enum.BUILD_SMELTER_GOAL:
			if self.entityHandler.agentType == demo.agentType.WORKER:
				self.finalGoal = overlord.overlord.getbuildposition() #check method name
				self.ChangeState(MoveState)
		
		elif self.goal == enum.BUILD_TRAINING_CAMP_GOAL:
			if self.entityHandler.agentType == demo.agentType.WORKER:
				self.finalGoal = overlord.overlord.getbuildposition() #check method name
				self.ChangeState(MoveState)
		