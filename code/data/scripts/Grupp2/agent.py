import demo, statParser
from Grupp2 import fsm, pathfinder, overlord


agentType = (
	"WORKER",
	"SCOUT",
	"SOLDIER",
	"KILNER",
	"SMITH",
	"SMELTER",
	"BUILDER",
)


class Agent:
	def __init__(self, ID, pos):
		self.ID = ID
		self.pos = pos
		self.holding = None
		self.type = agentType.WORKER
		self.pathToGoal = []
		self.pathToCastle = []
		self.state = None
		self.goalPos = None
		self.timeBusy = 0
		
		self.entityHandle = demo.SpawnEntity("AgentEntity/agent")
		
		self.hp = self.entityHandle.Health
		self.hp.hp = statParser.getStat("workerHealth")
		self.entityHandle.Health = self.hp
	
	#lämna, orders frome overlord
	def ChangeState(self, newState):
		self.state.Exit(this)
		self.state =newState
		self.state.Enter(self)
	
	# Take Damage - Method
	def TakeDamege(self):
		if hp > 1:
			self.hp -= 1;
		else:
			overlord.overlord.KillAgent(self)
	# pick up item
	def PickupItem(self, item):
		holding = item
	# drop item
	def DropItem(self):
		if self.pos == overlord.overlord.castleEntity.Building.position:
			if self.holding == "tree":
				overlord.Addtree(1)
			elif self.holding == "ironOre":
				overlord.AddironOre(1)
			self.holding = none;
		else:
			print("Agent not in casle keep walking")



#demo.GetFrameTime()
