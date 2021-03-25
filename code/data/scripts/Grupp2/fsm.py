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
		agent.entityHandle.Agent.targetPosition)
		
		
		
	def Execute(agent):
		pos = agent.entityHandle.Agent.position
		if pos != agent.finalGoal:
			if navMesh.findinNavMesh(pos) != navMesh.findinNavMesh(agent.entityHandle.Agent.targetPosition):

				current = agent.entityHandle
				current.targetPosition = navMesh.getCenter(agent.pathToGoal.pop(0))
				agent.entityHandle = current

		elif agent.entityHandle.Agent.position == agent.finalGoal:

			current = agent.entityHandle
			current.targetPosition = agent.finalGoal
			agent.entityHandle = current
			agent.ChangeState(ChoppingState) #kolla vilken resource vid finalGoal

class FleeState(BaseState):
	def Execute(agent, danger, fleeRadius):
		return
		

#Workers Agents
class ChoppingState(BaseState):
	def Execute(agent, radius):
		if not agent.timeBusy:
			#start chopping timer
			return
		print("agent is busy")

class UpgradeState(BaseState):
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
					if overlord.sword > statParser.getStat("soldierSwordCost"):
						agent.type = newtype
						agent.timeBusy = statParser.getStat("soldierUpgradeTime")
						overlord.sword -= statParser.getStat("soldierSwordCost")
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
	def Execute(agent):
		if agent.type == agentType[6]:
			if overlord.tree > statParser.getStat("kilnWoodCost"):
				agent.timeBusy = statParser.getStat("kilnBuildTime")
				return
			if overlord.tree > statParser.getStat("smelteryWoodCost"):
				agent.timeBusy = statParser.getStat("smelteryBuildTime")
				return
			if overlord.tree > statParser.getStat("blacksmithWoodCost") and overlord.ironbar > statParser.getStat("blacksmithIronCost"):
				agent.timeBusy = statParser.getStat("kilnBuildTime")
				return
		else:
			print("Wrong type of agent")
			return

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
