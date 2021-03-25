import random
from Grupp2 import agent, pathfinder, buildings, overlord
import navMesh, demo, statParser

class BaseState:
	def Enter(agent):
		pass
	def Execute(agent):
		pass
	def Exit(agent):
		pass

#All Agents
class MoveState(BaseState):
	def Enter(agent):
		agent.pathToGoal = pathfinder.Astar(agent.entityHandle.Agent.position,
		agent.entityHandle.Agent.targetPosition)#goal position eller target position?
		
		
		
	def Execute(agent):
		pos = agent.entityHandle.Agent.position
		if pos != agent.finalGoal:
			if navMesh.findinNavMesh(pos) != navMesh.findinNavMesh(agent.entityHandle.Agent.targetPosition):

				current = agent.entityHandle.Agent.targetPosition
				current = navMesh.getCenter(agent.pathToGoal.pop(0))
				agent.entityHandle.Agent.targetPosition = current

		elif agent.entityHandle.Agent.position == agent.finalGoal:

			current = agent.entityHandle.Agent.targetPosition
			current = agent.finalGoal
			agent.entityHandle.Agent.targetPosition = current
			agent.ChangeState(ChoppingState) #kolla vilken resource vid finalGoal

class FleeState(BaseState):
	def Execute(agent, danger, fleeRadius):
		return
		

#Workers Agents
class ChoppingState(BaseState):
	def Enter(agent):
		#starta timer typ / ta start tid
		pass
	def Execute(agent, radius):
		#look if timer is done
		if not agent.timeBusy:
			#start chopping timer
			return
		print("agent is busy")

class UpgradeState(BaseState):
	def Enter(agent, newType):
		#kolla att kan upgrada
		#starta timer typ / ta start tid
		pass
	def Execute(agent, newtype):
		if not agent.timeBusy:
			if agent.type == agentType[0]:
				if newtype == agentType[0]:
					agent.type = newtype
					print("Nice One!")
					return
			
				if newtype == agentType[1]:
					agent.type = newtype
					agent.timeBusy == statParser.getStat("scoutUpgradeTime")
				if newtype == agentType[2]:
					if overlord.overlord.sword > statParser.getStat("soldierSwordCost"):
						agent.type = newtype
						agent.timeBusy = statParser.getStat("soldierUpgradeTime")
						overlord.overlord.sword -= statParser.getStat("soldierSwordCost")
					else:
						print("no spare swords in castle")
						return
				if newtype == agentType[3]:
					agent.type = newtype
					agent.timeBusy = statParser.getStat("kilnerUpgradeTime")
					return
				if newtype == agentType[4]:
					agent.type = newtype
					agent.timeBusy = statParser.getStat("smithUpgradeTime")
					return
				if newtype == agentType[5]:
					agent.type = newtype
					agent.timeBusy = statParser.getStat("smelterUpgradeTime")
					return
				if newtype == agentType[6]:
					agent.type = newtype
					agent.timeBusy = statParser.getStat("builderUpgradeTime")
					return
			else:
				print("Only workers can be upgraded")
				return
	print("agent is busy")

#Scout Agents
class ExploreState(BaseState):
	def Execute(agent, fog):
		agent.goal = random.randint()
		return

		
#artisan Agents
class BuildState(BaseState):
	startTime = 0
	buildingtype = None
	def Enter(agent, buildingtypeIn):
		#kolla om nog med resurser
		#starta timer typ / ta start tid
		buildingtype = buildingtypeIn;
		if agent.entityHandle.agentType[6]:#builder
			if buildingtype == demo.buildingType[0]:#kiln
				if overlord.overlord.tree >= statParser.getStat("kilnWoodCost"):
					startTimer = demo.GetTime()
				else:
					print("Not enogh resorses for a Kiln")
			elif buildingtype == demo.buildingType[1]:#Smeltery
				if overlord.overlord.tree >= statParser.getStat("smelteryWoodCost"):
					startTimer = demo.GetTime()
				else:
					print("Not enogh resorses for a Smeltery")
			elif buildingtype == demo.buildingType[2]:#Blacksmith
				if overlord.overlord.tree >= statParser.getStat("blacksmithWoodCost") and overlord.overlord.ironore >= statParser.getStat("blacksmithOreCost"):
					startTimer = demo.GetTime()
				else:
					print("Not enogh resorses for a blacksmith")
			elif buildingtype == demo.buildingType[3]:#Trainingcamp
				if overlord.overlord.tree >= statParser.getStat("trainingCampWoodCost"):
					startTimer = demo.GetTime()
				else:
					print("Not enogh resorses for a Trainingcamp")
		else:
			print("Agent is not a builder")
	def Execute(agent):
		if buildingtype == demo.buildingType[0]:#kiln
			if startTime - demo.GetTime >= statParser.getStat("kilnBuildTime"):
				building(demo.buildingtype[0],agent)
#Soldier Agents
class AttackState(BaseState):
	def Execute(agent, enemy):
		if agent.type == agentType[2]:
			if not agent.timeBusy:
				agent.timeBusy = statParser.getStat("soldierAttackSpeed")
				if ((agent.pos[0] - enemy.pos[0])**2 + (agent.pos[1] - enemy.pos[1])**2)**.5 < statParser.getStat("solider") and random.random() < statParser.getStat("hitChance"):
					#sent message to enemy team
					print("CHAARGE")
					return
		else:
			print("Wrong type of agent")
		return
