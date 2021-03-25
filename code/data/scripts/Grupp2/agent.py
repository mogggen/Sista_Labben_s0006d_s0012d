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
		self.hp = statParser.getStat("workerHealth")
	
	#lämna, orders frome overlord
	def ChangeState(self, newState):
		self.state = newState
	
	# Take Damage - Method
	def TakeDamage(self):
		if hp > 1:
			self.hp -= 1;
		else:
			#change state to dead
			pass
	# pick up item
	def PickupItem(self, item):
		holding = item
	# drop item
	def DropItem(self):
		if self.holding == "tree":
			overlord.Addtree(1)
		elif self.holding == "ironOre":
			overlord.AddironOre(1)
		self.holding = none;



#demo.GetFrameTime()
