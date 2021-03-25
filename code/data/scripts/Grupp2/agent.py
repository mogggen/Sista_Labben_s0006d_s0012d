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
		self.timeBusy = 0
		
		self.entityHandle = demo.SpawnEntity("AgentEntity/redagent")
		
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
	def TakeDamage(self):
		hp = self.entityHandle.Health
		hp.hp = statParser.getStat("workerHealth")
		if hp > 1:
			hp -= 1
			self.entityHandle.Health = hp
		elif self.hp <= 1:
			overlord.overlord.KillAgent(self)
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