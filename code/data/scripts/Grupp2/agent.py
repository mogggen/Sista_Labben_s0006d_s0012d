import fsm, pathfinder, demo, statParser
from Grupp2 import fsm, pathfinder

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
	
	#lämna
	def ChangeState(self, newState):
		self.state = newState
	
	# Take Damage - Method

	# pick up item

	# drop item



#demo.GetFrameTime()
